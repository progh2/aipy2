/* 교사용 성취수준 참고 지표(#145-B). 반을 고르고 '반 전체 불러오기'를 누르면 학생마다
   students/{uid}/state/current를 한 번씩 읽어(class-state-loader.js) 성취기준 13개의 이해·적용·
   성찰·참여 지표와 A~E 수준을 계산한다(achievement-model.js). 코드 수정 여부는 그 반 학생이
   손댄 예제가 속한 단원의 data/unit{n}.json만 받아 와 원본과 비교한다(답변 내역 화면의
   ensureUnitFiles 패턴과 동일 — 반 전체를 한꺼번에 조회하므로 최초 1회에 몰아서 받는다).
   이 화면이 내는 점수는 참고 지표이며 최종 성취수준은 교사가 판단한다(화면 고정 안내 참고). */
import {ready} from './firebase-config.js?v=a144';
import {load} from './auth.js?v=a144';
import {parseClassId} from './class-picker.js';
import {titlesFromCatalog, tasksFromCatalog, topicTitle} from './understanding-model.js';
import {buildStudentCards, sortStudentCards, exampleIndexFromCatalog} from './board-model.js?v=q135b';
import {projectDiffSummary} from './code-diff-model.js?v=q135d';
import {loadClassStates} from './class-state-loader.js?v=a145';
import {
 defaultSettings, loadSettings, saveSettings, mergeSettings, studentStandardScores,
 classDistribution, overallAverage, strengthsWeaknesses, achievementCsvHeader, achievementCsvRow,
 INSUFFICIENT, LEVELS
} from './achievement-model.js?v=a145';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let classIdValue = '';
let rosterRows = [];
let progressRows = [];
let rosterUnsub = null;
let progressUnsub = null;

let standardsNote = '';
let standards = [];
let questions = [];
let exampleIndex = {};
let titles = {};
let tasks = {};

let settings = defaultSettings();
// uid -> state(student current doc) | null. 반 전체 불러오기를 할 때만 채워진다(상시 구독 아님).
let studentStates = new Map();
// uid -> [standardResult, ...]. settings가 바뀌면 studentStates는 그대로 두고 다시 계산한다.
let studentResultsByUid = new Map();
let loadedCards = []; // '반 전체 불러오기' 시점의 카드 목록(학번순)
let selectedUid = '';
let loadBusy = false;

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

function isDemo() {
 return new URLSearchParams(location.search).get('demo') === '1';
}

function liveCards() {
 return sortStudentCards(buildStudentCards({roster: rosterRows, progress: progressRows, classId: classIdValue, titles}));
}

function setLoadButtonsEnabled() {
 const hasClass = !!classIdValue || isDemo();
 const hasResults = studentResultsByUid.size > 0;
 if ($('load-class')) $('load-class').disabled = !hasClass || loadBusy;
 if ($('csv-export')) $('csv-export').disabled = !hasResults;
 if ($('print-report')) $('print-report').disabled = !hasResults;
}

// ── 설정 패널 ──────────────────────────────────────────────────────────
function paintSettingsForm() {
 const map = {
  'w-understand': settings.weights.understand,
  'w-apply': settings.weights.apply,
  'w-reflect': settings.weights.reflect,
  'w-participate': settings.weights.participate,
  'cutoff-a': settings.cutoffs.A,
  'cutoff-b': settings.cutoffs.B,
  'cutoff-c': settings.cutoffs.C,
  'cutoff-d': settings.cutoffs.D,
  'advanced-weight': settings.advancedWeight,
  'min-reflect-len': settings.minReflectLen
 };
 for (const [id, value] of Object.entries(map)) {
  const el = $(id);
  if (el) el.value = value;
 }
}

function readSettingsForm() {
 const num = (id, fallback) => {
  const el = $(id);
  const v = el ? Number(el.value) : NaN;
  return Number.isFinite(v) ? v : fallback;
 };
 return mergeSettings({
  weights: {
   understand: num('w-understand', settings.weights.understand),
   apply: num('w-apply', settings.weights.apply),
   reflect: num('w-reflect', settings.weights.reflect),
   participate: num('w-participate', settings.weights.participate)
  },
  cutoffs: {
   A: num('cutoff-a', settings.cutoffs.A),
   B: num('cutoff-b', settings.cutoffs.B),
   C: num('cutoff-c', settings.cutoffs.C),
   D: num('cutoff-d', settings.cutoffs.D)
  },
  advancedWeight: num('advanced-weight', settings.advancedWeight),
  minReflectLen: num('min-reflect-len', settings.minReflectLen)
 });
}

function onSettingsChanged() {
 settings = readSettingsForm();
 saveSettings(window.localStorage, settings);
 recomputeAll();
 renderAll();
}

function onSettingsReset() {
 settings = defaultSettings();
 saveSettings(window.localStorage, settings);
 paintSettingsForm();
 recomputeAll();
 renderAll();
}

// ── 코드 수정 여부(원본 비교) ──────────────────────────────────────────
// 반 학생들이 손댄 예제가 속한 단원의 data/unit{n}.json만 모아 원본 files를 얻는다.
async function fetchOriginalFiles(statesByUid) {
 const neededUnits = new Set();
 for (const state of statesByUid.values()) {
  for (const eid of Object.keys((state && state.projects) || {})) {
   const meta = exampleIndex[eid];
   if (meta) neededUnits.add(meta.unit);
  }
 }
 const filesByEid = {};
 await Promise.all([...neededUnits].map(async (unit) => {
  try {
   const data = await (await fetch(`${prefix}data/unit${unit}.json`)).json();
   for (const [eid, ex] of Object.entries(data.examples || {})) {
    if (ex && ex.files) filesByEid[eid] = ex.files;
   }
  } catch (error) {
   console.warn('[teacher-achievement] unit', unit, error);
  }
 }));
 return filesByEid;
}

function modifiedExampleIdsFor(state, originalFilesById) {
 const set = new Set();
 for (const [eid, proj] of Object.entries((state && state.projects) || {})) {
  const orig = originalFilesById[eid];
  if (!orig) continue;
  const diff = projectDiffSummary(orig, (proj && proj.files) || {});
  if (!diff.same) set.add(eid);
 }
 return set;
}

let originalFilesCache = {};

function recomputeAll() {
 studentResultsByUid = new Map();
 for (const card of loadedCards) {
  if (!card.uid) continue;
  const state = studentStates.get(card.uid) || {};
  const ctx = {
   state, questions, exampleIndex, tasks,
   modifiedExampleIds: modifiedExampleIdsFor(state, originalFilesCache)
  };
  studentResultsByUid.set(card.uid, studentStandardScores(standards, ctx, settings));
 }
}

// ── 반 전체 불러오기 ───────────────────────────────────────────────────
async function runLoadClass() {
 if (loadBusy || isDemo()) return;
 if (!classIdValue) return;
 const confirmed = window.confirm(
  '이 반 학생의 학습 기록(문항 답·코드·저널)을 모두 불러옵니다. 교사 본인 확인과 개인정보 보호 책임을 동의하면 계속하세요.'
 );
 if (!confirmed) return;
 loadBusy = true;
 setLoadButtonsEnabled();
 loadedCards = liveCards().filter((c) => c.uid);
 note('load-progress', `0 / ${loadedCards.length}명 불러오는 중…`);
 try {
  const {db, store} = await load();
  studentStates = await loadClassStates({
   db, store, students: loadedCards, concurrency: 5,
   onProgress: (done, total) => note('load-progress', `${done} / ${total}명 불러왔습니다.`)
  });
  originalFilesCache = await fetchOriginalFiles(studentStates);
  recomputeAll();
  note('load-progress', `${loadedCards.length}명 불러오기 완료.`);
 } catch (error) {
  console.error('[teacher-achievement]', error);
  note('load-progress', '불러오기에 실패했습니다. 다시 시도하세요.');
 } finally {
  loadBusy = false;
  setLoadButtonsEnabled();
  renderAll();
 }
}

// ── 렌더링 ────────────────────────────────────────────────────────────
function levelBadge(level, score) {
 const span = node('span', `ach-level ach-level--${(level || '').replace(/[^A-E]/g, '') || 'x'}`);
 span.textContent = level === INSUFFICIENT ? '보류' : level || '—';
 if (score != null) span.title = `점수 ${score}`;
 return span;
}

function renderDistribution() {
 const host = $('distribution-table');
 if (!host) return;
 if (!standards.length || !studentResultsByUid.size) {
  host.replaceChildren(node('p', 'small', '반 전체를 불러오면 분포가 나타납니다.'));
  return;
 }
 const allResults = loadedCards.filter((c) => c.uid).map((c) => studentResultsByUid.get(c.uid) || []);
 const rows = classDistribution(allResults, standards);
 const table = node('table');
 const thead = node('thead');
 const headRow = node('tr');
 for (const label of ['성취기준', '영역', ...LEVELS, '판단보류', '평균']) headRow.append(node('th', '', label));
 thead.append(headRow);
 const tbody = node('tbody');
 for (const row of rows) {
  const tr = node('tr');
  tr.append(node('td', '', row.code), node('td', '', row.area || ''));
  for (const lv of LEVELS) tr.append(node('td', '', String(row.counts[lv] || 0)));
  tr.append(node('td', '', String(row.counts.insufficient || 0)));
  tr.append(node('td', '', row.average != null ? `${row.average}` : '—'));
  tbody.append(tr);
 }
 table.append(thead, tbody);
 host.replaceChildren(table);
}

function dimTitle(results) {
 if (!results) return '';
 const d = results.dimensions || {};
 const fmt = (v) => (v && v.score != null ? `${v.score}%` : '기록 없음');
 return `이해 ${fmt(d.understand)} · 적용 ${fmt(d.apply)} · 성찰 ${fmt(d.reflect)} · 참여 ${fmt(d.participate)}`;
}

function renderMatrix() {
 const host = $('student-matrix');
 if (!host) return;
 if (!standards.length || !studentResultsByUid.size) {
  host.replaceChildren(node('p', 'small', '반 전체를 불러오면 학생별 표가 나타납니다.'));
  return;
 }
 const table = node('table');
 const thead = node('thead');
 const headRow = node('tr');
 headRow.append(node('th', '', '학생'));
 for (const s of standards) headRow.append(node('th', '', s.code));
 headRow.append(node('th', '', '전체'));
 thead.append(headRow);
 const tbody = node('tbody');
 for (const card of loadedCards) {
  if (!card.uid) continue;
  const results = studentResultsByUid.get(card.uid) || [];
  const tr = node('tr');
  tr.dataset.uid = card.uid;
  if (card.uid === selectedUid) tr.classList.add('is-selected');
  const nameTd = node('td');
  const btn = node('button', 'assign-sub-btn', card.label);
  btn.type = 'button';
  btn.addEventListener('click', () => { selectedUid = card.uid; renderReport(); renderMatrix(); });
  nameTd.append(btn);
  tr.append(nameTd);
  for (const s of standards) {
   const r = results.find((x) => x.code === s.code);
   const td = node('td');
   td.title = dimTitle(r);
   td.append(levelBadge(r ? r.level : INSUFFICIENT, r ? r.score : null));
   tr.append(td);
  }
  const overall = overallAverage(results, settings);
  const overallTd = node('td');
  overallTd.append(levelBadge(overall.level, overall.score));
  tr.append(overallTd);
  tbody.append(tr);
 }
 table.append(thead, tbody);
 host.replaceChildren(table);
}

function renderReport() {
 const host = $('student-report');
 if (!host) return;
 if (!selectedUid) {
  host.replaceChildren(node('p', 'small', '위 표에서 학생을 선택하면 리포트를 봅니다.'));
  return;
 }
 const card = loadedCards.find((c) => c.uid === selectedUid);
 const results = studentResultsByUid.get(selectedUid) || [];
 if (!card || !results.length) {
  host.replaceChildren(node('p', 'small', '이 학생의 결과를 찾을 수 없습니다.'));
  return;
 }
 const wrap = node('div', 'ach-report');
 wrap.append(node('h3', '', card.label));
 const overall = overallAverage(results, settings);
 wrap.append(node('p', '', `전체 평균: ${overall.level}${overall.score != null ? ` (${overall.score}점)` : ''}`));
 const list = node('div', 'ach-report-list');
 for (const r of results) {
  const std = standards.find((s) => s.code === r.code);
  const box = node('div', 'ach-report-item');
  box.append(node('h4', '', `${r.code} ${std ? std.area : ''}`));
  box.append(node('p', '', `${std ? std.statement : ''}`));
  const badgeLine = node('p', '');
  badgeLine.append(levelBadge(r.level, r.score), node('span', 'small', ` ${dimTitle(r)}`));
  box.append(badgeLine);
  if (!r.insufficient && std && std.levels && std.levels[r.level]) {
   box.append(node('p', 'small', `성취수준 기술(교사 검토용 초안): ${std.levels[r.level]}`));
  } else if (r.insufficient) {
   box.append(node('p', 'small', '해당 소단원 문항 시도 기록이 없어 판단을 보류합니다.'));
  }
  list.append(box);
 }
 wrap.append(list);
 const sw = strengthsWeaknesses(results, standards);
 if (sw.strengths.length || sw.weaknesses.length) {
  wrap.append(node('h4', '', '강점·보완점(자동 생성 — 과장 없이 수치 근거만)'));
  const ul = node('ul', 'report-list');
  for (const s of sw.strengths) ul.append(node('li', '', s));
  for (const s of sw.weaknesses) ul.append(node('li', '', s));
  wrap.append(ul);
 } else if (sw.note) {
  wrap.append(node('p', 'small', sw.note));
 }
 host.replaceChildren(wrap);
}

function renderAll() {
 setLoadButtonsEnabled();
 renderDistribution();
 renderMatrix();
 renderReport();
}

// ── CSV·인쇄 ──────────────────────────────────────────────────────────
function downloadCsv() {
 if (!standards.length) return;
 const header = achievementCsvHeader(standards);
 const lines = [header];
 for (const card of loadedCards) {
  if (!card.uid) continue;
  const results = studentResultsByUid.get(card.uid) || [];
  lines.push(achievementCsvRow(card, results, standards));
 }
 const csv = lines.map((row) => row.map((cell) => `"${String(cell ?? '').replace(/"/g, '""')}"`).join(',')).join('\n');
 const blob = new Blob([`﻿${csv}`], {type: 'text/csv;charset=utf-8'});
 const a = document.createElement('a');
 a.href = URL.createObjectURL(blob);
 a.download = `성취수준_${classIdValue || 'demo'}.csv`;
 a.click();
 URL.revokeObjectURL(a.href);
}

function printReport() {
 window.print();
}

// ── 구독·데모 ─────────────────────────────────────────────────────────
function stopListen() {
 if (rosterUnsub) { rosterUnsub(); rosterUnsub = null; }
 if (progressUnsub) { progressUnsub(); progressUnsub = null; }
 rosterRows = [];
 progressRows = [];
}

function listen(id) {
 stopListen();
 classIdValue = id || '';
 const parsed = parseClassId(id);
 setLoadButtonsEnabled();
 if (!id || !parsed || !ready) return;
 load().then(({db, store}) => {
  const byGrade = (name) => store.query(store.collection(db, name), store.where('grade', '==', parsed.grade));
  rosterUnsub = store.onSnapshot(byGrade('roster'), (snap) => {
   rosterRows = [];
   snap.forEach((doc) => rosterRows.push({id: doc.id, email: doc.data().email || doc.id, ...doc.data()}));
   setLoadButtonsEnabled();
  }, (error) => console.error('[teacher-achievement]', error));
  progressUnsub = store.onSnapshot(byGrade('progress'), (snap) => {
   progressRows = [];
   snap.forEach((doc) => progressRows.push({id: doc.id, uid: doc.data().uid || doc.id, ...doc.data()}));
   setLoadButtonsEnabled();
  }, (error) => console.error('[teacher-achievement]', error));
 }).catch((error) => console.error('[teacher-achievement]', error));
}

function onClass(detail) {
 if (isDemo()) return;
 listen((detail && detail.classId) || '');
}

// ?demo=1 미리보기 — 4~6명의 성취수준이 고르게 다르도록 기록을 구성한다.
function renderDemo() {
 classIdValue = '2-3';
 const demoAnswers = (pairs) => {
  const answers = {};
  for (const [id, status] of pairs) answers[id] = {status, attempts: 1};
  return answers;
 };
 rosterRows = [
  {email: 'd1@e-mirim.hs.kr', name: '김가온', studentId: '20301', grade: 2, classroom: 3},
  {email: 'd2@e-mirim.hs.kr', name: '이나래', studentId: '20302', grade: 2, classroom: 3},
  {email: 'd3@e-mirim.hs.kr', name: '박다솜', studentId: '20303', grade: 2, classroom: 3},
  {email: 'd4@e-mirim.hs.kr', name: '최라온', studentId: '20304', grade: 2, classroom: 3},
  {email: 'd5@e-mirim.hs.kr', name: '정마루', studentId: '20305', grade: 2, classroom: 3}
 ];
 progressRows = rosterRows.map((r, i) => ({email: r.email, uid: `demo-${i + 1}`, grade: 2, classroom: 3, counts: {}}));
 studentStates = new Map([
  ['demo-1', {
   answers: demoAnswers([['u1-q001', 'done'], ['u1-q002', 'done'], ['u1-q003', 'done']]),
   journals: {'j-u1-overview': '모듈과 패키지를 나눠 쓰는 이유를 배웠다는 내용으로 충분히 적었습니다.', 'm-reuse-1': '2026-09-01'},
   complete: {'u1-overview': true, 'u1-define': true},
   projects: {'copy-twice': {files: {'main.py': 'print("고쳐 봤어요")\n'}}}
  }],
  ['demo-2', {
   answers: demoAnswers([['u1-q001', 'done'], ['u1-q002', 'retry']]),
   journals: {'j-u1-overview': '모듈 개념을 배웠다.'},
   complete: {'u1-overview': true},
   projects: {}
  }],
  ['demo-3', {
   answers: demoAnswers([['u1-q001', 'retry']]),
   journals: {},
   complete: {},
   projects: {}
  }],
  ['demo-4', {answers: {}, journals: {}, complete: {}, projects: {}}],
  ['demo-5', {
   answers: demoAnswers([['u1-q001', 'done'], ['u1-q002', 'done'], ['u1-q003', 'retry']]),
   journals: {'j-u1-overview': '모듈과 패키지의 차이를 예시로 정리했다.'},
   complete: {'u1-overview': true},
   projects: {'copy-twice': {files: {'main.py': 'import homework1\nimport homework2\n'}}}
  }]
 ]);
 originalFilesCache = {'copy-twice': {'main.py': 'import homework1\nimport homework2\nprint("두 숙제가 각자 add를 가지고 있습니다.")\n'}};
 loadedCards = liveCards().filter((c) => c.uid);
 recomputeAll();
 note('load-progress', `${loadedCards.length}명(데모) 불러오기 완료.`);
 renderAll();
}

if (typeof window !== 'undefined') window.aipyAchievementDemo = renderDemo;

async function start() {
 if (!$('distribution-table')) return;
 settings = loadSettings(window.localStorage);
 paintSettingsForm();
 try {
  const [catalog, standardsData] = await Promise.all([
   fetch(`${prefix}data/catalog.json`).then((r) => r.json()),
   fetch(`${prefix}data/standards.json`).then((r) => r.json())
  ]);
  titles = titlesFromCatalog(catalog);
  tasks = tasksFromCatalog(catalog);
  exampleIndex = exampleIndexFromCatalog(catalog);
  questions = Array.isArray(catalog.questions) ? catalog.questions : [];
  standardsNote = standardsData.note || '';
  standards = Array.isArray(standardsData.standards) ? standardsData.standards : [];
  note('standards-note', standardsNote);
 } catch (error) {
  console.warn('[teacher-achievement] data', error);
 }
 if ($('load-class')) $('load-class').addEventListener('click', runLoadClass);
 if ($('csv-export')) $('csv-export').addEventListener('click', downloadCsv);
 if ($('print-report')) $('print-report').addEventListener('click', printReport);
 if ($('settings-reset')) $('settings-reset').addEventListener('click', onSettingsReset);
 for (const id of ['w-understand', 'w-apply', 'w-reflect', 'w-participate', 'cutoff-a', 'cutoff-b', 'cutoff-c', 'cutoff-d', 'advanced-weight', 'min-reflect-len']) {
  const el = $(id);
  if (el) el.addEventListener('change', onSettingsChanged);
 }
 renderAll();
 if (isDemo()) {
  renderDemo();
  return;
 }
 if (!ready) note('load-progress', '로그인 설정이 없어 불러올 수 없습니다.');
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
}

start();
