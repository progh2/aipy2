/* 교사 단원 페이지 초점. 로그인·admins 확인 + 선택한 반의 활성 세션이 있을 때만
   주제 앵커·예제 클릭으로 sessions/{반}.focus를 갱신합니다. 아니면 기존 학습만 합니다.
   반은 window.aipyClass, 없으면 aipy-teacher-class:{email} localStorage에서 읽습니다. */
import {ready} from './firebase-config.js';
import {load, readTeacherFlag} from './auth.js';
import {dataFailureNote} from './auth-model.js';
import {publishClass, resolveTeacherClassId, labelClass} from './class-picker.js';
import {
 isSessionLive, pageFromPath, focusFromUnitClick, focusWritePayload
} from './follow-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let teacherEmail = '';
let classIdValue = '';
let current = null;
let sessionUnsub = null;
let toastTimer = 0;

function currentPage() {
 return pageFromPath(location.pathname);
}

function canSend() {
 return Boolean(teacherEmail && classIdValue && isSessionLive(current));
}

function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text || '';
 clearTimeout(toastTimer);
 toastTimer = setTimeout(() => { box.textContent = ''; }, 4200);
}

function paintCue() {
 let root = document.getElementById('teacher-focus-ui');
 if (!canSend()) {
  if (root) root.hidden = true;
  document.body.classList.remove('teacher-focus-live');
  removeFocusButtons();
  return;
 }
 injectFocusButtons();
 if (!root) {
  root = node('div', 'teacher-focus-ui');
  root.id = 'teacher-focus-ui';
  const status = node('p', 'teacher-focus-status', '');
  status.id = 'teacher-focus-status';
  root.append(status);
  const header = document.querySelector('header.top');
  if (header) header.after(root);
  else document.body.prepend(root);
 }
 root.hidden = false;
 document.body.classList.add('teacher-focus-live');
 document.getElementById('teacher-focus-status').textContent =
  `${labelClass(classIdValue)}에 초점을 보내요. 📍 버튼이나 주제·예제를 누르면 따라오는 학생이 옮겨요.`;
}

// 교사에게만 보이는 '초점 보내기' 버튼을 소단원 제목·실습 워크스페이스·문항 카드에 붙인다(#84).
// 앵커 클릭으로도 초점이 가지만, 눈에 보이는 버튼이 있어야 수업 중 바로 누를 수 있다.
let questionObserver = null;
function focusButton(anchorId, exampleId, label) {
 const b = node('button', 'focus-send', label || '📍 초점 보내기');
 b.type = 'button';
 b.title = '따라오는 학생 화면을 이 위치로 옮깁니다';
 b.addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  if (!canSend()) return;
  const focus = exampleId
   ? focusFromUnitClick({exampleId, lessonId: anchorId, currentPage: currentPage()})
   : focusFromUnitClick({href: '#' + anchorId, currentPage: currentPage()});
  if (focus) sendFocus(focus);
 });
 return b;
}
function injectFocusButtons() {
 if (!canSend()) return;
 document.querySelectorAll('section.lesson[id]').forEach((lesson) => {
  const h2 = lesson.querySelector('h2');
  if (!h2 || h2.querySelector('.focus-send')) return;
  h2.append(focusButton(lesson.id, null));
  const ws = lesson.querySelector('.lesson-workspace');
  const first = ws && ws.querySelector('[data-example]');
  const h3 = ws && ws.querySelector('h3');
  if (h3 && first && !h3.querySelector('.focus-send')) h3.append(focusButton(lesson.id, first.dataset.example, '📍 실습으로 초점'));
 });
 document.querySelectorAll('#questions .question[id]').forEach((card) => {
  const meta = card.querySelector('.question-meta') || card;
  if (meta.querySelector('.focus-send')) return;
  meta.append(focusButton(card.id, null, '📍 이 문제로 초점'));
 });
 const host = document.getElementById('questions');
 if (host && !questionObserver) {
  questionObserver = new MutationObserver(() => injectFocusButtons());
  questionObserver.observe(host, {childList: true});
 }
}
function removeFocusButtons() {
 document.querySelectorAll('.focus-send').forEach((el) => el.remove());
}

function lessonIdNear(el) {
 const lesson = el && el.closest && el.closest('section.lesson[id]');
 if (lesson) return lesson.id;
 return document.body.dataset.topic || null;
}

function focusFromEvent(event) {
 const example = event.target.closest && event.target.closest('[data-example]');
 if (example && example.dataset.example) {
  return focusFromUnitClick({
   exampleId: example.dataset.example,
   lessonId: lessonIdNear(example),
   currentPage: currentPage()
  });
 }
 const link = event.target.closest && event.target.closest('a[href]');
 if (!link) return null;
 if (link.target === '_blank') return null;
 return focusFromUnitClick({
  href: link.getAttribute('href'),
  currentPage: currentPage()
 });
}

async function sendFocus(focus) {
 if (!canSend() || !focus || !focus.page) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   ...focusWritePayload(focus),
   'focus.updatedAt': store.serverTimestamp()
  });
  toast('초점을 보냈습니다.');
 } catch (error) {
  console.warn('[teacher-focus]', error);
  toast(dataFailureNote(error, `초점을 보내지 못했습니다. (${error.code || error})`));
 }
}

function onClick(event) {
 if (!canSend()) return;
 const focus = focusFromEvent(event);
 if (focus) sendFocus(focus);
}

function onExampleSelect(event) {
 if (!canSend()) return;
 const id = event.target && event.target.value;
 if (!id) return;
 const button = [...document.querySelectorAll('[data-example]')].find((el) => el.dataset.example === id);
 sendFocus(focusFromUnitClick({
  exampleId: id,
  lessonId: lessonIdNear(button),
  currentPage: currentPage()
 }));
}

function listen(id) {
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 current = null;
 paintCue();
 if (!id || !teacherEmail) return;
 load().then(({db, store}) => {
  sessionUnsub = store.onSnapshot(store.doc(db, 'sessions', id), (snap) => {
   current = snap.exists() ? snap.data() : null;
   paintCue();
  }, (error) => {
   console.warn('[teacher-focus]', error);
   current = null;
   paintCue();
  });
 }).catch((error) => {
  console.warn('[teacher-focus]', error);
  current = null;
  paintCue();
 });
}

function applyClass(id) {
 const next = id || '';
 if (next === classIdValue && sessionUnsub) {
  paintCue();
  return;
 }
 classIdValue = next;
 if (classIdValue) publishClass(classIdValue);
 else publishClass('');
 listen(classIdValue);
}

function resolveClass() {
 applyClass(resolveTeacherClassId(teacherEmail, window.aipyClass));
}

async function isTeacher(email) {
 const {teacher} = await readTeacherFlag(email);
 return teacher;
}

async function onAccount(detail) {
 const user = detail && detail.user;
 const email = (user && user.email) ? user.email.toLowerCase() : '';
 if (!email) {
  teacherEmail = '';
  applyClass('');
  return;
 }
 if (!(await isTeacher(email))) {
  teacherEmail = '';
  applyClass('');
  return;
 }
 teacherEmail = email;
 resolveClass();
}

function startTeacherFocus() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!Number(document.body.dataset.unit)) return;
 if (!ready) return;
 document.addEventListener('click', onClick);
 const select = document.getElementById('example-select');
 if (select) select.addEventListener('change', onExampleSelect);
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 document.addEventListener('aipy:class', (event) => {
  if (!teacherEmail) return;
  const id = event.detail && event.detail.classId;
  if (id && id !== classIdValue) applyClass(id);
 });
 if (window.aipyAccount) onAccount(window.aipyAccount);
}

startTeacherFocus();
