/* 교사용 답변 내역(#128). 반을 고르면 학번순 학생 목록이 나오고, 학생을 누르면 그 학생의
   문항 답·저널을 단원→소단원 순으로 본다. roster·progress는 board.js와 같은 방식으로
   학년 단위로 구독하고 화면에서 이 반(classIdValue)만 골라 보여 준다(#125-4 패턴 재사용).
   학생 상세는 board.js 학생 상세 패널(#104)과 같은 규칙으로 students/{uid}/state/current를
   학생당 1회만 읽고 캐시한다 — 반 전체 state를 한꺼번에 읽지 않는다. 답안 줄·저널 렌더링은
   board.js와 answer-view.js를 공유해 중복 구현하지 않는다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {parseClassId} from './class-picker.js';
import {titlesFromCatalog, tasksFromCatalog} from './understanding-model.js';
import {
 topicListFromCatalog, buildStudentCards, sortStudentCards, formatRate,
 cardAccuracyLabel, answerRows, unitAnswerTotals, journalRows, UNIT_ROMAN
} from './board-model.js';
import {renderAnswerRow, renderJournalUnitGroup} from './answer-view.js';
import {groupAnswerRowsBySubunit, studentSummaryLabel, hasAnswerRecord} from './teacher-answers-model.js';

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
let topics = [];
let questions = [];
let rosterUnsub = null;
let progressUnsub = null;
let rosterRows = [];
let progressRows = [];
let selectedKey = '';
// uid -> {status: 'loading'|'ready'|'empty'|'error', data?}. students/{uid}/state/current를 학생당 1회만 조회(#104와 동일 규칙).
let detailStateCache = new Map();

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

function liveCards() {
 return sortStudentCards(buildStudentCards({roster: rosterRows, progress: progressRows, classId: classIdValue, topics, titles}));
}

function paintRosterList() {
 const list = $('answers-roster-list');
 if (!list) return;
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  paintDetail(null);
  return;
 }
 const cards = liveCards();
 if (!cards.length) {
  list.replaceChildren(node('p', 'small', '이 반 명단·진행 기록이 없습니다.'));
  paintDetail(null);
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
 const card = liveCards().find((item) => item.key === key);
 paintRosterList();
 if (changed) scrollDetailToTop();
 if (card && card.uid) ensureStudentState(card.uid);
}

// students/{uid}/state/current를 학생당 1회만 읽는다. 실패·미존재는 캐시에 남겨 재요청하지 않는다.
async function ensureStudentState(uid) {
 if (!uid || detailStateCache.has(uid)) return;
 detailStateCache.set(uid, {status: 'loading'});
 refreshDetailIfSelected(uid);
 try {
  const {db, store} = await load();
  const snap = await store.getDoc(store.doc(db, 'students', uid, 'state', 'current'));
  detailStateCache.set(uid, snap.exists() ? {status: 'ready', data: snap.data()} : {status: 'empty'});
 } catch (error) {
  console.error('[teacher-answers]', error);
  detailStateCache.set(uid, {status: 'error', error});
 }
 refreshDetailIfSelected(uid);
}

function refreshDetailIfSelected(uid) {
 if (!selectedKey) return;
 const card = liveCards().find((item) => item.key === selectedKey);
 if (card && card.uid === uid) paintDetail(card);
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

function paintDetail(card) {
 const body = $('answers-detail-body');
 if (!body) return;
 if (!card) {
  body.replaceChildren(node('p', 'small', '학생을 선택하면 답변과 저널을 봅니다.'));
  return;
 }
 const wrap = node('div', 'student-detail-answers');
 wrap.append(
  node('h3', '', card.label),
  node('p', '', `완료 ${formatRate(card.completeRate)} (${card.doneCount}/${card.topicTotal || 0}) · 정답 ${cardAccuracyLabel(card)}`),
  reloadButton(card)
 );
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
 const rows = answerRows(state, questions);
 const totalsByUnit = new Map(unitAnswerTotals(state, questions).map((t) => [t.unit, t]));
 const groups = groupAnswerRowsBySubunit(rows, titles);
 let currentUnit = null;
 let unitHost = null;
 for (const group of groups) {
  if (group.unit !== currentUnit) {
   currentUnit = group.unit;
   const totalInfo = totalsByUnit.get(group.unit);
   unitHost = node('details', 'answer-unit-group');
   unitHost.open = groups.length <= 3;
   unitHost.append(node('summary', '', `${UNIT_ROMAN[group.unit] || group.unit} 단원 · 푼 문항 ${totalInfo ? totalInfo.answered : ''} / 전체 ${totalInfo ? totalInfo.total : ''}`));
   wrap.append(unitHost);
  }
  const topicBox = node('div', 'answer-subunit');
  topicBox.append(node('h4', '', group.topicTitle || group.topic || '(주제 없음)'));
  const ul = node('ul', 'answer-row-list');
  for (const row of group.rows) ul.append(renderAnswerRow(row, titles));
  topicBox.append(ul);
  unitHost.append(topicBox);
 }
 const journals = journalRows(state, titles, tasks);
 if (journals.length) {
  wrap.append(node('h3', '', '학습 저널'));
  for (const jr of journals) wrap.append(renderJournalUnitGroup(jr));
 }
 body.replaceChildren(wrap);
}

function stop() {
 if (rosterUnsub) { rosterUnsub(); rosterUnsub = null; }
 if (progressUnsub) { progressUnsub(); progressUnsub = null; }
 rosterRows = [];
 progressRows = [];
 selectedKey = '';
 detailStateCache = new Map();
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
function renderAnswersDemo() {
 classIdValue = '2-3';
 rosterRows = [
  {email: '20301@e-mirim.hs.kr', name: '김가', studentId: '20301', grade: 2, classroom: 3},
  {email: '20302@e-mirim.hs.kr', name: '이나', studentId: '20302', grade: 2, classroom: 3}
 ];
 progressRows = [
  {email: '20301@e-mirim.hs.kr', uid: 'demo-1', grade: 2, classroom: 3, counts: {done: ['u1-overview'], answers: {'u1-q001': {attempts: 1, correct: 1}}}},
  {email: '20302@e-mirim.hs.kr', uid: 'demo-2', grade: 2, classroom: 3, counts: {done: [], answers: {}}}
 ];
 detailStateCache.set('demo-1', {
  status: 'ready',
  data: {
   answers: {
    'u1-q001': {status: 'done', attempts: 1, value: '저장한 Python 파일은 모듈이 될 수 없습니다.'}
   },
   journals: {'u1-learn': '모듈을 나눠 쓰는 이유를 배웠다.'}
  }
 });
 detailStateCache.set('demo-2', {status: 'empty'});
 paintRosterList();
}

if (typeof window !== 'undefined') window.aipyAnswersDemo = renderAnswersDemo;

async function startTeacherAnswers() {
 if (!$('answers-roster-list')) return;
 if (!ready && !isDemo()) note('answers-roster-note', '로그인 설정이 없어 답변을 불러올 수 없습니다.');
 try {
  const catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  titles = titlesFromCatalog(catalog);
  tasks = tasksFromCatalog(catalog);
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
