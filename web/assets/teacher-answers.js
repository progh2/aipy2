/* 교사용 답변 내역(#128, #145 A). 반을 고르면 학번순 학생 목록이 나오고, 학생을 누르면 그 학생의
   문항 답·저널을 단원→소단원 순으로 본다(학생별 보기). '반 전체 보기' 탭은 버튼을 눌렀을 때만
   반 학생 전원의 state/current를 한꺼번에 조회해 소단원별 한눈 표로 보여 준다. roster·progress는
   board.js와 같은 방식으로 학년 단위로 구독하고 화면에서 이 반(classIdValue)만 골라 보여 준다.
   학생 상세는 board.js 학생 상세 패널(#104)과 같은 규칙으로 students/{uid}/state/current를
   학생당 1회만 읽고 캐시한다(반 전체 조회와 캐시를 공유해 중복 조회하지 않는다). 답안 줄·저널·
   소단원 섹션·반 전체 표 렌더링은 answer-view.js를 공유해 중복 구현하지 않는다. */
import {ready} from './firebase-config.js?v=a144';
import {load} from './auth.js?v=a144';
import {parseClassId} from './class-picker.js';
import {titlesFromCatalog, tasksFromCatalog} from './understanding-model.js';
import {topicListFromCatalog, buildStudentCards, sortStudentCards, exampleIndexFromCatalog} from './board-model.js?v=q135b';
import {renderUnitSection, renderStudentSummary, renderClassOverviewTable} from './answer-view.js?v=q145a';
import {
 studentSummaryLabel, hasAnswerRecord, groupProjectRowsBySubunit, pendingProjectUnits,
 buildStudentDetailSections, mergeProjectGroupsIntoSections, summarizeStudentActivity,
 classOverviewColumns, buildClassOverviewRow, classSummaryCsv, classLongCsv
} from './teacher-answers-model.js?v=q145a';
import {loadStatesForUids} from './class-state-loader.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let classIdValue = '';
let titles = {};
let tasks = {};
let exampleIndex = {};
let topics = [];
let questions = [];
let rosterUnsub = null;
let progressUnsub = null;
let rosterRows = [];
let progressRows = [];
let selectedKey = '';
let activeTab = 'student';
// uid -> {status: 'loading'|'ready'|'empty'|'error', data?}. students/{uid}/state/current를 학생당 1회만 조회(#104와 동일 규칙).
// 학생별 보기와 반 전체 보기가 이 캐시를 함께 쓴다 — 한 번 읽은 학생은 다시 읽지 않는다.
let detailStateCache = new Map();
// unit(1~4) -> {status: 'loading'|'ready'|'error', data?}. 예제 원본 코드는 catalog.json에 없고
// data/unit{n}.json에만 있어(#135-4), 학생 프로젝트가 있는 단원만 그때 그때 받아 캐시한다.
let unitFilesCache = new Map();
let classOverviewLoading = false;

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

function liveCards() {
 return sortStudentCards(buildStudentCards({roster: rosterRows, progress: progressRows, classId: classIdValue, topics, titles}));
}

// -------------------------------------------------------------------------
// 탭 전환 (학생별 보기 / 반 전체 보기)
// -------------------------------------------------------------------------

function paintTabs() {
 const studentTab = $('answers-tab-student');
 const classTab = $('answers-tab-class');
 const studentPanel = $('answers-panel-student');
 const classPanel = $('answers-panel-class');
 if (!studentTab || !classTab || !studentPanel || !classPanel) return;
 const isClass = activeTab === 'class';
 studentTab.classList.toggle('is-active', !isClass);
 classTab.classList.toggle('is-active', isClass);
 studentTab.setAttribute('aria-selected', String(!isClass));
 classTab.setAttribute('aria-selected', String(isClass));
 studentPanel.hidden = isClass;
 classPanel.hidden = !isClass;
}

function setTab(tab) {
 activeTab = tab === 'class' ? 'class' : 'student';
 paintTabs();
}

// -------------------------------------------------------------------------
// 학생별 보기
// -------------------------------------------------------------------------

function paintRosterList() {
 const list = $('answers-roster-list');
 if (!list) return;
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  paintDetail(null);
  paintClassPanel();
  return;
 }
 const cards = liveCards();
 if (!cards.length) {
  list.replaceChildren(node('p', 'small', '이 반 명단·진행 기록이 없습니다.'));
  paintDetail(null);
  paintClassPanel();
  return;
 }
 const wrap = node('div', 'student-card-grid');
 for (const card of cards) {
  const btn = node('button', 'student-card');
  btn.type = 'button';
  btn.dataset.studentKey = card.key;
  if (card.key === selectedKey) {
   btn.classList.add('is-selected');
   btn.setAttribute('aria-current', 'true');
  }
  btn.setAttribute('aria-label', `${card.label} 답변 보기`);
  btn.append(node('strong', '', card.label), node('p', 'small', studentSummaryLabel(card)));
  btn.addEventListener('click', () => openDetail(card.key));
  wrap.append(btn);
 }
 list.replaceChildren(wrap);
 if (selectedKey) {
  const selected = cards.find((item) => item.key === selectedKey);
  if (selected) paintDetail(selected);
 }
 paintClassPanel();
}

// #129: 학생을 바꾸면 오른쪽 내용 열을 맨 위로 스크롤한다(좁은 화면에서 위아래로 쌓일 때도
// 오른쪽 열 시작 지점으로 이동하면 자연스럽다).
function scrollDetailToTop() {
 const col = document.getElementById('answers-detail');
 if (col && typeof col.scrollIntoView === 'function') col.scrollIntoView({block: 'start'});
 else window.scrollTo(0, 0);
}

function openDetail(key) {
 const changed = key !== selectedKey;
 selectedKey = key;
 setTab('student');
 const card = liveCards().find((item) => item.key === key);
 paintRosterList();
 if (changed) scrollDetailToTop();
 if (card && card.uid) ensureStudentState(card.uid);
}

// students/{uid}/state/current를 학생당 1회만 읽는다. 실패·미존재는 캐시에 남겨 재요청하지 않는다.
async function ensureStudentState(uid) {
 if (!uid || detailStateCache.has(uid)) return;
 detailStateCache.set(uid, {status: 'loading'});
 refreshAfterStateChange(uid);
 try {
  const {db, store} = await load();
  const snap = await store.getDoc(store.doc(db, 'students', uid, 'state', 'current'));
  detailStateCache.set(uid, snap.exists() ? {status: 'ready', data: snap.data()} : {status: 'empty'});
 } catch (error) {
  console.error('[teacher-answers]', error);
  detailStateCache.set(uid, {status: 'error', error});
 }
 refreshAfterStateChange(uid);
}

function refreshAfterStateChange(uid) {
 const card = liveCards().find((item) => item.uid === uid);
 if (card && card.key === selectedKey) paintDetail(card);
 if (activeTab === 'class') paintClassPanel();
}

// data/unit{n}.json을 단원당 1회만 받아 캐시한다. 실패해도 다시 시도하지 않는다(다른 캐시들과 동일 규칙).
async function ensureUnitFiles(unit) {
 if (!unit || unitFilesCache.has(unit)) return;
 unitFilesCache.set(unit, {status: 'loading'});
 try {
  const data = await (await fetch(`${prefix}data/unit${unit}.json`)).json();
  unitFilesCache.set(unit, {status: 'ready', data});
 } catch (error) {
  console.warn('[teacher-answers] unit', unit, error);
  unitFilesCache.set(unit, {status: 'error'});
 }
 if (selectedKey) {
  const card = liveCards().find((item) => item.key === selectedKey);
  if (card) paintDetail(card);
 }
}

// state.projects에 있는 예제마다 원본 files를 모은다. 아직 못 받은 단원은 fetch를 걸어 두고
// (도착하면 다시 그린다) 이번 그리기에서는 조용히 건너뛴다.
function originalFilesFor(state) {
 const result = {};
 for (const eid of Object.keys((state && state.projects) || {})) {
  const meta = exampleIndex[eid];
  if (!meta) continue;
  const entry = unitFilesCache.get(meta.unit);
  if (entry && entry.status === 'ready') {
   const files = entry.data.examples && entry.data.examples[eid] && entry.data.examples[eid].files;
   if (files) result[eid] = files;
  }
 }
 return result;
}

function reloadButton(card) {
 const again = node('button', 'answer-filter-btn answer-reload', '↻ 새로 읽기');
 again.type = 'button';
 again.title = '이 학생의 답안을 다시 읽습니다';
 again.addEventListener('click', () => {
  detailStateCache.delete(card.uid);
  ensureStudentState(card.uid);
  paintDetail(card);
 });
 return again;
}

function printButton() {
 const btn = node('button', 'answer-filter-btn answers-print-btn', '🖨 인쇄');
 btn.type = 'button';
 btn.title = '지금 보는 학생 상세를 인쇄합니다';
 btn.addEventListener('click', () => window.print());
 return btn;
}

function paintDetail(card) {
 const body = $('answers-detail-body');
 if (!body) return;
 if (!card) {
  body.replaceChildren(node('p', 'small', '학생을 선택하면 답변과 저널을 봅니다.'));
  return;
 }
 const wrap = node('div', 'student-detail-answers');
 const head = node('div', 'answer-row-head');
 head.append(node('h3', '', card.label));
 const btnRow = node('div', '', undefined);
 btnRow.append(reloadButton(card), printButton());
 head.append(btnRow);
 wrap.append(head);
 const entry = detailStateCache.get(card.uid) || {status: 'loading'};
 if (entry.status === 'loading') {
  wrap.append(node('p', 'small', '학습 기록을 불러오는 중입니다…'));
  body.replaceChildren(wrap);
  return;
 }
 if (entry.status === 'error') {
  wrap.append(node('p', 'small', '학습 기록을 불러오지 못했습니다.'));
  body.replaceChildren(wrap);
  return;
 }
 if (entry.status === 'empty') {
  wrap.append(node('p', 'small', '이 학생의 학습 기록 미러가 아직 없습니다(로그인 후 학습하면 생깁니다).'));
  body.replaceChildren(wrap);
  return;
 }
 const state = entry.data || {};
 if (!hasAnswerRecord(state)) {
  wrap.append(node('p', 'small', '아직 제출한 답변이 없습니다.'));
  body.replaceChildren(wrap);
  return;
 }
 const summary = summarizeStudentActivity(state, card, {titles, tasks, exampleIndex});
 wrap.append(renderStudentSummary(summary));

 let sections = buildStudentDetailSections(state, {titles, tasks, exampleIndex, questions, topics});
 const originalFiles = originalFilesFor(state);
 for (const unit of pendingProjectUnits(state.projects, exampleIndex, originalFiles)) ensureUnitFiles(unit);
 const projectGroups = groupProjectRowsBySubunit(state.projects, exampleIndex, originalFiles, titles);
 sections = mergeProjectGroupsIntoSections(sections, projectGroups);

 for (const unitEntry of sections) {
  wrap.append(renderUnitSection(unitEntry, titles, {openByDefault: sections.length <= 2}));
 }
 body.replaceChildren(wrap);
}

// -------------------------------------------------------------------------
// 반 전체 보기
// -------------------------------------------------------------------------

function paintClassPanel() {
 const host = $('answers-class-table-host');
 if (!host) return;
 const cards = liveCards();
 if (!cards.length) {
  host.replaceChildren(node('p', 'small', classIdValue ? '이 반 명단·진행 기록이 없습니다.' : '위에서 수업할 반을 먼저 선택하세요.'));
  return;
 }
 const anyLoaded = cards.some((c) => c.uid && detailStateCache.has(c.uid));
 if (!anyLoaded && !classOverviewLoading) {
  host.replaceChildren(node('p', 'small', '아직 불러오지 않았습니다. 위 [반 전체 불러오기]를 누르세요.'));
  return;
 }
 const columns = classOverviewColumns(topics);
 const rows = cards.map((card) => buildClassOverviewRow(card, card.uid ? detailStateCache.get(card.uid) : null, {titles, tasks, exampleIndex, questions, topics}));
 const table = renderClassOverviewTable(columns, rows, {
  onCellClick: (row) => openDetail(row.key)
 });
 host.replaceChildren(table);
}

async function loadClassOverview() {
 if (classOverviewLoading) return;
 const cards = liveCards();
 const uids = cards.map((c) => c.uid).filter(Boolean);
 if (!uids.length) return;
 const todo = uids.filter((uid) => !detailStateCache.has(uid));
 if (!todo.length) { paintClassPanel(); return; }
 classOverviewLoading = true;
 note('answers-class-progress', `0/${todo.length}명 불러오는 중…`);
 paintClassPanel();
 try {
  const {db, store} = await load();
  const result = await loadStatesForUids(
   todo,
   (uid) => store.getDoc(store.doc(db, 'students', uid, 'state', 'current')),
   {
    concurrency: 5,
    onProgress: ({done, total}) => note('answers-class-progress', `${done}/${total}명 불러오는 중…`)
   }
  );
  for (const [uid, entry] of result.entries()) detailStateCache.set(uid, entry);
  const failed = [...result.values()].filter((e) => e.status === 'error').length;
  note('answers-class-progress', failed ? `완료 (${failed}명 실패 — 학생 상세에서 ↻ 새로 읽기)` : '완료');
 } catch (error) {
  console.error('[teacher-answers] class overview', error);
  note('answers-class-progress', '불러오지 못했습니다.');
 } finally {
  classOverviewLoading = false;
  paintClassPanel();
 }
}

function confirmPersonalData() {
 return window.confirm('학생 개인정보가 포함됩니다. 내려받으시겠습니까?');
}

function downloadCsv(filename, text) {
 const blob = new Blob([text], {type: 'text/csv;charset=utf-8'});
 const url = URL.createObjectURL(blob);
 const a = node('a');
 a.href = url;
 a.download = filename;
 document.body.append(a);
 a.click();
 a.remove();
 setTimeout(() => URL.revokeObjectURL(url), 5000);
}

function exportSummaryCsv() {
 if (!confirmPersonalData()) return;
 const cards = liveCards();
 const summaries = new Map();
 for (const card of cards) {
  if (!card.uid) continue;
  const entry = detailStateCache.get(card.uid);
  if (entry && entry.status === 'ready') summaries.set(card.uid, summarizeStudentActivity(entry.data || {}, card, {titles, tasks, exampleIndex}));
 }
 downloadCsv(`answers-summary-${classIdValue || 'class'}.csv`, classSummaryCsv(cards, summaries));
}

function exportLongCsv() {
 if (!confirmPersonalData()) return;
 const cards = liveCards();
 downloadCsv(`answers-detail-${classIdValue || 'class'}.csv`, classLongCsv(cards, detailStateCache, {titles, tasks, exampleIndex, questions}));
}

function stop() {
 if (rosterUnsub) { rosterUnsub(); rosterUnsub = null; }
 if (progressUnsub) { progressUnsub(); progressUnsub = null; }
 rosterRows = [];
 progressRows = [];
 selectedKey = '';
 detailStateCache = new Map();
 unitFilesCache = new Map();
}

// roster·progress는 학년 단위로만 구독하고(#125-4 패턴), 화면 필터는 buildStudentCards의
// classId로 한다 — 반을 옮긴 학생을 이메일로 계속 매칭하려는 이유는 board.js listen() 주석 참고.
function listen(id) {
 stop();
 classIdValue = id || '';
 const parsed = parseClassId(id);
 if (!id || !parsed || !ready) {
  paintRosterList();
  return;
 }
 load().then(({db, store}) => {
  const byGrade = (name) => store.query(store.collection(db, name), store.where('grade', '==', parsed.grade));
  rosterUnsub = store.onSnapshot(byGrade('roster'), (snap) => {
   rosterRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    rosterRows.push({id: doc.id, email: data.email || doc.id, ...data});
   });
   paintRosterList();
  }, (error) => {
   console.error('[teacher-answers]', error);
   note('answers-roster-note', '명단을 읽지 못했습니다.');
  });
  progressUnsub = store.onSnapshot(byGrade('progress'), (snap) => {
   progressRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    progressRows.push({id: doc.id, uid: data.uid || doc.id, ...data});
   });
   paintRosterList();
  }, (error) => {
   console.error('[teacher-answers]', error);
   note('answers-roster-note', '진행 요약을 읽지 못했습니다.');
  });
 }).catch((error) => {
  console.error('[teacher-answers]', error);
 });
}

function isDemo() {
 return new URLSearchParams(location.search).get('demo') === '1';
}

function onClass(detail) {
 if (isDemo()) return;
 listen((detail && detail.classId) || '');
}

// ?demo=1 미리보기 — 다른 교사 화면(teacher-session.js 등)과 같은 방식으로 로그인 없이 확인한다.
// #145-A: 학생 상세 섹션(연습문제·직접 해 보세요·소단원 저널·예측·코드 읽기·미션·예제 코드 수정 배지·
// 빈 소단원 접기)과 반 전체 표·CSV 미리보기를 확인할 수 있도록 유형별 입력을 모두 채운 학생 4명을 둔다.
function renderAnswersDemo() {
 classIdValue = '2-3';
 rosterRows = [
  {email: '20301@e-mirim.hs.kr', name: '김가', studentId: '20301', grade: 2, classroom: 3},
  {email: '20302@e-mirim.hs.kr', name: '이나', studentId: '20302', grade: 2, classroom: 3},
  {email: '20303@e-mirim.hs.kr', name: '박다', studentId: '20303', grade: 2, classroom: 3},
  {email: '20304@e-mirim.hs.kr', name: '최라', studentId: '20304', grade: 2, classroom: 3}
 ];
 progressRows = [
  {email: '20301@e-mirim.hs.kr', uid: 'demo-1', grade: 2, classroom: 3, counts: {done: ['u1-overview', 'u1-define'], answers: {'u1-q001': {attempts: 1, correct: 1}}}},
  {email: '20302@e-mirim.hs.kr', uid: 'demo-2', grade: 2, classroom: 3, counts: {done: [], answers: {}}},
  {email: '20303@e-mirim.hs.kr', uid: 'demo-3', grade: 2, classroom: 3, counts: {done: ['u1-overview'], answers: {}}},
  {email: '20304@e-mirim.hs.kr', uid: 'demo-4', grade: 2, classroom: 3, counts: {done: [], answers: {}}}
 ];
 // demo-1: 문항·단원 저널·소단원 저널·직접 해 보세요(제출됨)·예측·코드 읽기·미션 통과·수정한 예제 코드까지 전부.
 detailStateCache.set('demo-1', {
  status: 'ready',
  data: {
   answers: {
    'u1-q001': {status: 'done', attempts: 1, value: '저장한 Python 파일은 모듈이 될 수 없습니다.'}
   },
   journals: {
    'u1-learn': '모듈을 나눠 쓰는 이유를 배웠다.',
    'u1-error': 'import 경로를 헷갈렸다.',
    'u1-next': '패키지도 더 연습하고 싶다.',
    'j-u1-define': '모듈 정의를 한 줄로 설명할 수 있게 됐다.',
    'd-u1-define-1': '내가 만든 answer.py를 import했다.',
    'd-u1-define-submitted': '2026-09-29T01:00:00.000Z',
    'p-copy-twice': '둘 다 add를 각자 갖고 있어서 결과가 다를 것 같다.',
    'p-copy-twice-match': 'same',
    'p-copy-twice-actual': '예상대로 8, 8이 나왔다.',
    'c-copy-twice-l3': '이 줄은 homework1의 add를 부른다.',
    'm-copy-twice-1': '2026-09-30T02:00:00.000Z'
   },
   // #135-4 데모: 원본을 고친 예제(copy-twice) 배지가 보이도록 print 한 줄을 더했다.
   projects: {
    'copy-twice': {
     files: {
      'main.py': 'import homework1\nimport homework2\nprint("두 숙제가 각자 add를 가지고 있습니다.")\nprint("고쳐 봤어요")\n',
      'homework1.py': 'def add(a, b):\n    return a + b\n\nprint("숙제1:", add(3, 5))\n',
      'homework2.py': 'def add(a, b):\n    return a + b\n\nprint("숙제2:", add(10, -2))\n'
     },
     entry: 'main.py'
    }
   }
  }
 });
 // demo-2: 예제 코드만 원본과 동일하게 저장 — 다른 섹션은 비어서 전부 '입력 없음' 접힘을 보여 준다.
 detailStateCache.set('demo-2', {
  status: 'ready',
  data: {
   answers: {},
   journals: {},
   projects: {
    'copy-twice': {
     files: {
      'main.py': 'import homework1\nimport homework2\nprint("두 숙제가 각자 add를 가지고 있습니다.")\n',
      'homework1.py': 'def add(a, b):\n    return a + b\n\nprint("숙제1:", add(3, 5))\n',
      'homework2.py': 'def add(a, b):\n    return a + b\n\nprint("숙제2:", add(10, -2))\n'
     },
     entry: 'main.py'
    }
   }
  }
 });
 // demo-3: 문항만 틀려서 다시 풀기 상태 — 정답률·완료율이 낮은 케이스.
 detailStateCache.set('demo-3', {
  status: 'ready',
  data: {
   answers: {
    'u1-q001': {status: 'retry', attempts: 2, value: '모듈은 import할 수 없습니다.'}
   },
   journals: {'u1-learn': '아직 헷갈린다.'}
  }
 });
 // demo-4: 이 반에서 아직 아무것도 입력하지 않은 학생 — '아직 제출한 답변이 없습니다' 안내 확인용.
 detailStateCache.set('demo-4', {status: 'empty'});
 paintRosterList();
 paintClassPanel();
}

if (typeof window !== 'undefined') window.aipyAnswersDemo = renderAnswersDemo;

function wireTabs() {
 const studentTab = $('answers-tab-student');
 const classTab = $('answers-tab-class');
 if (studentTab) studentTab.addEventListener('click', () => setTab('student'));
 if (classTab) classTab.addEventListener('click', () => setTab('class'));
 const loadBtn = $('answers-class-load');
 if (loadBtn) loadBtn.addEventListener('click', loadClassOverview);
 const csvSummaryBtn = $('answers-class-csv-summary');
 if (csvSummaryBtn) csvSummaryBtn.addEventListener('click', exportSummaryCsv);
 const csvLongBtn = $('answers-class-csv-long');
 if (csvLongBtn) csvLongBtn.addEventListener('click', exportLongCsv);
}

async function startTeacherAnswers() {
 if (!$('answers-roster-list')) return;
 wireTabs();
 if (!ready && !isDemo()) note('answers-roster-note', '로그인 설정이 없어 답변을 불러올 수 없습니다.');
 try {
  const catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  titles = titlesFromCatalog(catalog);
  tasks = tasksFromCatalog(catalog);
  exampleIndex = exampleIndexFromCatalog(catalog);
  topics = topicListFromCatalog(catalog);
  questions = Array.isArray(catalog.questions) ? catalog.questions : [];
 } catch (error) {
  console.warn('[teacher-answers] catalog', error);
 }
 paintRosterList();
 if (isDemo()) {
  renderAnswersDemo();
  return;
 }
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
}

startTeacherAnswers();
