/* 학생 과제 제출. 단원 실습·문제 영역에 붙이며, 생성 HTML을 고치지 않습니다.
   로그인·권한 실패는 학습을 막지 않습니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classId} from './class-picker.js';
import {
 assignmentVisible, isLate, statusLabel, reviewLabel, submitButtonLabel, statusChips,
 submitToast, targetsFromState, submissionFields, submissionStatus, canSubmit,
 targetTitle, targetHref, formatWhen, FAIL_OK_NOTE, LATE_NOTE, BROWSER_GRADE_NOTE
} from './assignment-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

const prefix = document.body.dataset.prefix || '';
let user = null;
let profile = null;
let classroom = '';
let catalog = {questions: [], examples: {}, topics: {}};
let assignments = [];
let mine = {};
let lastChecks = {};
let lastSubmitAt = 0;
let writing = false;
let assignUnsub = null;
let subUnsub = null;

function toast(text) {
 const box = document.getElementById('toast');
 if (box) box.textContent = text || '';
}

function learningState() {
 if (window.aipyLearning && typeof window.aipyLearning.getState === 'function') {
  return window.aipyLearning.getState();
 }
 return {answers: {}, projects: {}};
}

function visibleAssignments(now = Date.now()) {
 return assignments.filter((row) => assignmentVisible(row, classroom, now));
}

function hostParent() {
 return document.getElementById('practice') || document.getElementById('lab') || document.getElementById('main');
}

function ensurePanel() {
 const parent = hostParent();
 if (!parent) return null;
 let panel = document.getElementById('assignment-panel');
 if (panel) return panel;
 panel = node('section', 'assignment-panel section');
 panel.id = 'assignment-panel';
 panel.setAttribute('aria-label', '과제');
 if (parent.id === 'practice' || parent.id === 'lab') parent.insertAdjacentElement('beforebegin', panel);
 else parent.append(panel);
 return panel;
}

function rememberCheck(detail) {
 if (!detail || !detail.type || !detail.id) return;
 lastChecks[`${detail.type}:${detail.id}`] = {
  ok: Boolean(detail.ok),
  checked: detail.checked !== false,
  output: detail.output || '',
  attempts: Number(detail.attempts) || 0
 };
 paint();
}

function normalizeTargetsSafe(list) {
 return (list || []).filter((row) => row && (row.type === 'question' || row.type === 'example') && row.id);
}

function paint() {
 const panel = ensurePanel();
 if (!panel) return;
 const now = Date.now();
 const rows = visibleAssignments(now);
 const head = node('div', 'section-head');
 const titles = node('div');
 titles.append(node('p', 'eyebrow', 'ASSIGNMENT'), node('h2', '', '과제'));
 head.append(titles);
 const note = node('p', 'small', FAIL_OK_NOTE);
 const late = node('p', 'small', LATE_NOTE);
 const grade = node('p', 'small', BROWSER_GRADE_NOTE);
 if (!user || !classroom) {
  panel.replaceChildren(head, node('p', 'small', '명단에 있는 학교 계정으로 로그인하면 과제를 제출할 수 있어요.'));
  return;
 }
 if (!rows.length) {
  panel.replaceChildren(head, note, node('p', 'small', '이 반에 열린 과제가 없어요.'));
  return;
 }
 const list = node('div', 'assignment-list');
 for (const assignment of rows) {
  list.append(paintCard(assignment, now));
 }
 panel.replaceChildren(head, note, late, grade, list);
}

function paintCard(assignment, now) {
 const card = node('article', 'assignment-card');
 const late = isLate(assignment, now);
 const prev = mine[assignment.id];
 const collected = targetsFromState({assignment, state: learningState(), lastChecks, catalog});
 const status = submissionStatus(collected);
 const title = node('h3', '', assignment.title || '과제');
 const due = formatWhen(assignment.dueAt);
 card.append(title);
 card.append(node('p', '', assignment.description || ''));
 card.append(node('p', 'small', `${due ? `마감 ${due}` : '마감 없음'}${late ? ' · 지연' : ''}`));
 const ul = node('ul', 'assignment-targets');
 for (const target of normalizeTargetsSafe(assignment.targets)) {
  const key = `${target.type}:${target.id}`;
  const snap = collected[key];
  const li = node('li');
  const href = targetHref(prefix, target, catalog);
  const label = targetTitle(target, catalog) || target.id;
  if (href) {
   const a = node('a', '', `${target.id} · ${label}`);
   a.href = href;
   li.append(a);
  } else li.append(node('span', '', `${target.id} · ${label}`));
  li.append(node('span', 'small', snap && snap.grade && snap.grade.ok ? '통과' : (snap && snap.grade && snap.grade.checked ? '미통과' : '미검사')));
  ul.append(li);
 }
 card.append(ul);
 if (prev) {
  card.append(node('p', 'small', `이전 제출: ${statusLabel(prev)} · ${prev.attemptCount || 1}회 · ${formatWhen(prev.submittedAt)}`));
  if (prev.reviewComment) {
   card.append(node('p', 'assignment-comment', `선생님: ${reviewLabel(prev.reviewStatus)} · ${prev.reviewComment}`));
  } else if (prev.reviewStatus === 'reviewed') {
   card.append(node('p', 'small', `선생님: ${reviewLabel(prev.reviewStatus)}`));
  }
 }
 const actions = node('div', 'actions');
 const chips = node('span', 'assignment-chips');
 for (const label of statusChips({status, late})) {
  chips.append(node('span', 'assignment-chip', label));
 }
 const button = node('button', status === 'failed' ? '' : 'primary', submitButtonLabel({hasSubmission: Boolean(prev)}));
 button.type = 'button';
 button.disabled = writing;
 button.onclick = () => submit(assignment, collected, late);
 if (chips.childNodes.length) actions.append(chips);
 actions.append(button);
 card.append(actions);
 if (Array.isArray(prev && prev.history) && prev.history.length) {
  const hist = node('details');
  hist.append(node('summary', '', `제출 이력 ${prev.history.length}회`));
  for (const item of prev.history) {
   hist.append(node('p', 'small', `${formatWhen(item.submittedAt) || ''} · ${statusLabel(item)} · ${item.attemptCount || ''}회`));
  }
  card.append(hist);
 }
 return card;
}

async function submit(assignment, collected, late) {
 if (!user || !classroom || writing) return;
 const gate = canSubmit({lastAt: lastSubmitAt, now: Date.now()});
 if (!gate.ok) {
  toast('잠시 뒤에 다시 제출할 수 있어요.');
  return;
 }
 writing = true;
 paint();
 try {
  const {db, store} = await load();
  const payload = submissionFields({
   profile: {uid: user.uid, ...profile},
   assignmentId: assignment.id,
   classId: classroom,
   targets: collected,
   late,
   previous: mine[assignment.id]
  });
  payload.submittedAt = store.serverTimestamp();
  payload.updatedAt = store.serverTimestamp();
  await store.setDoc(store.doc(db, 'students', user.uid, 'submissions', assignment.id), payload);
  lastSubmitAt = Date.now();
  toast(submitToast({status: payload.status, late}));
 } catch (error) {
  console.warn('[assignments]', error);
  const denied = error && (error.code === 'permission-denied' || /permission/i.test(String(error.message || '')));
  toast(denied ? '제출 권한이 없어요. 명단과 공개 과제를 확인하세요.' : '제출하지 못했어요. 네트워크를 확인하세요.');
 } finally {
  writing = false;
  paint();
 }
}

function listen() {
 if (assignUnsub) {
  assignUnsub();
  assignUnsub = null;
 }
 if (subUnsub) {
  subUnsub();
  subUnsub = null;
 }
 assignments = [];
 mine = {};
 paint();
 if (!ready || !user || !classroom) return;
 load().then(({db, store}) => {
  assignUnsub = store.onSnapshot(
   store.query(
    store.collection(db, 'assignments'),
    store.where('open', '==', true),
    store.where('classrooms', 'array-contains', classroom)
   ),
   (snap) => {
    assignments = [];
    snap.forEach((doc) => assignments.push({id: doc.id, ...doc.data()}));
    paint();
   },
   (error) => {
    console.warn('[assignments] list', error);
    paint();
   }
  );
  subUnsub = store.onSnapshot(
   store.collection(db, 'students', user.uid, 'submissions'),
   (snap) => {
    mine = {};
    snap.forEach((doc) => { mine[doc.id] = {id: doc.id, ...doc.data()}; });
    paint();
   },
   (error) => console.warn('[assignments] mine', error)
  );
 }).catch((error) => console.warn('[assignments]', error));
}

function onAccount(detail) {
 user = detail && detail.user;
 profile = detail && detail.profile;
 classroom = classId(profile);
 listen();
}

async function start() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!hostParent()) return;
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
 } catch (error) {
  console.warn('[assignments] catalog', error);
 }
 paint();
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 document.addEventListener('aipy:learning-ready', paint);
 document.addEventListener('aipy:checked', (event) => rememberCheck(event.detail));
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.aipyAssignments = {list: () => visibleAssignments(), mine: () => mine};
}

start();
