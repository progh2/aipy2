/* 주제 끝 이해도 버튼. 완료 체크 옆에 붙이고, 로컬을 먼저 저장한 뒤 progress.understanding 을 맞춥니다.
   로그인·네트워크 실패는 학습을 막지 않습니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {progressFields} from './sync-model.js';
import {
 UNDERSTANDING_KEY, UNDERSTANDING_WRITE_MS, COMMENT_MAX, UNDERSTANDING_VALUES,
 UNDERSTANDING_LABELS, HARD_PROMPT, NOT_GRADED_NOTE, normalizeStore, mergeStores,
 setUnderstanding, setComment, historyItems, topicHref, titlesFromCatalog,
 titlesFromLessons, topicTitle, feedbackId, feedbackFields
} from './understanding-model.js';

const prefix = document.body.dataset.prefix || '';
const unit = Number(document.body.dataset.unit || 0);
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let store = normalizeStore(readLocal());
let user = null;
let profile = null;
let writeTimer = 0;
let writing = false;
let titles = {};

function readLocal() {
 try { return JSON.parse(localStorage.getItem(UNDERSTANDING_KEY) || 'null'); }
 catch { return null; }
}

function persistLocal() {
 try { localStorage.setItem(UNDERSTANDING_KEY, JSON.stringify(store)); } catch { /* 사생활 모드 등 */ }
}

function liveState() {
 if (window.aipyLearning && typeof window.aipyLearning.getState === 'function') {
  return window.aipyLearning.getState();
 }
 return {complete: {}, answers: {}};
}

function snapshot() {
 return store.values;
}

function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text || '';
}

function paintChoices() {
 document.querySelectorAll('.topic-signals').forEach((root) => {
  const topicId = root.dataset.topic;
  const current = store.values[topicId] || '';
  root.querySelectorAll('[data-understanding]').forEach((button) => {
   button.setAttribute('aria-pressed', String(button.dataset.understanding === current));
  });
  const comment = root.querySelector('.hard-comment');
  if (comment) {
   comment.hidden = current !== 'hard';
   const input = comment.querySelector('input');
   if (input && document.activeElement !== input) input.value = store.comments[topicId] || '';
  }
 });
 paintHistory();
}

function paintHistory() {
 const items = historyItems(store.values);
 let root = document.getElementById('understanding-history');
 if (!root) {
  const host = document.querySelector('section.record')
   || (document.querySelector('section.lesson') && document.getElementById('main'));
  if (!host) return;
  root = node('section', 'understanding-history');
  root.id = 'understanding-history';
  if (host.id === 'main') host.prepend(root);
  else host.prepend(root);
 }
 if (!items.length) {
  root.hidden = true;
  root.replaceChildren();
  return;
 }
 root.hidden = false;
 const list = node('ul', 'understanding-history-list');
 for (const item of items) {
  const li = node('li');
  const link = node('a', '', topicTitle(item.topicId, titles));
  link.href = topicHref(prefix, item.topicId);
  li.append(link, node('span', 'understanding-history-tag', item.label));
  list.append(li);
 }
 root.replaceChildren(
  node('h2', '', '다시 보면 좋은 주제'),
  node('p', 'small understanding-note', NOT_GRADED_NOTE),
  list
 );
}

function mountSignals() {
 document.querySelectorAll('label.completion [data-complete]').forEach((box) => {
  const topicId = box.dataset.complete;
  const label = box.closest('label.completion');
  if (!topicId || !label || label.nextElementSibling?.classList.contains('topic-signals')) return;
  const root = node('div', 'topic-signals');
  root.dataset.topic = topicId;
  const note = node('p', 'small understanding-note', NOT_GRADED_NOTE);
  const group = node('div', 'understanding-choices');
  group.setAttribute('role', 'group');
  group.setAttribute('aria-label', '이 주제 이해도');
  for (const value of UNDERSTANDING_VALUES) {
   const button = node('button', '', UNDERSTANDING_LABELS[value]);
   button.type = 'button';
   button.dataset.understanding = value;
   button.setAttribute('aria-pressed', 'false');
   button.addEventListener('click', () => choose(topicId, value));
   group.append(button);
  }
  const comment = node('div', 'hard-comment');
  comment.hidden = true;
  const field = node('label', '', HARD_PROMPT);
  const input = node('input');
  input.type = 'text';
  input.maxLength = COMMENT_MAX;
  input.autocomplete = 'off';
  input.setAttribute('aria-label', HARD_PROMPT);
  input.placeholder = '한 줄로 적어도 되고, 비워도 돼요';
  const save = node('button', '', '남기기');
  save.type = 'button';
  save.addEventListener('click', () => submitComment(topicId, input.value));
  input.addEventListener('keydown', (event) => {
   if (event.key === 'Enter') {
    event.preventDefault();
    submitComment(topicId, input.value);
   }
  });
  field.append(input);
  comment.append(field, save);
  root.append(note, group, comment);
  label.after(root);
 });
}

async function writeProgress() {
 if (!user || !profile || !ready || writing) return;
 writing = true;
 try {
  const {db, store: fs} = await load();
  const payload = progressFields(profile, liveState(), Date.now(), snapshot());
  payload.updatedAt = fs.serverTimestamp();
  await fs.setDoc(fs.doc(db, 'progress', user.uid), payload);
 } catch (error) {
  console.warn('[understanding]', error);
 } finally {
  writing = false;
 }
}

function scheduleWrite() {
 persistLocal();
 paintChoices();
 if (!user || !profile || !ready) return;
 clearTimeout(writeTimer);
 writeTimer = setTimeout(() => { writeProgress(); }, UNDERSTANDING_WRITE_MS);
}

function choose(topicId, value) {
 store = setUnderstanding(store, topicId, value);
 scheduleWrite();
 toast(value === 'hard' ? `${UNDERSTANDING_LABELS[value]} · ${HARD_PROMPT}` : UNDERSTANDING_LABELS[value]);
}

async function writeFeedback(topicId, text) {
 if (!user || !profile || !ready) return;
 const id = feedbackId(user.uid, topicId);
 if (!id) return;
 try {
  const {db, store: fs} = await load();
  const payload = feedbackFields({profile, topicId, text});
  payload.updatedAt = fs.serverTimestamp();
  const ref = fs.doc(db, 'feedback', id);
  const prev = await fs.getDoc(ref);
  if (!prev.exists()) payload.createdAt = fs.serverTimestamp();
  await fs.setDoc(ref, payload, {merge: true});
 } catch (error) {
  console.warn('[understanding] feedback', error);
 }
}

function submitComment(topicId, text) {
 store = setComment(store, topicId, text);
 persistLocal();
 paintChoices();
 writeFeedback(topicId, text);
 toast('남겼어요. 평가에 반영되지 않습니다.');
}

async function pullCloud() {
 if (!user || !ready) return;
 try {
  const {db, store: fs} = await load();
  const snap = await fs.getDoc(fs.doc(db, 'progress', user.uid));
  const cloudValues = snap.exists() ? snap.data().understanding : {};
  store = mergeStores(store, {values: cloudValues, comments: store.comments});
  persistLocal();
  paintChoices();
 } catch (error) {
  console.warn('[understanding] pull', error);
 }
}

function onAccount(detail) {
 user = detail && detail.user;
 profile = detail && detail.profile;
 if (!user || !profile) {
  user = null;
  profile = null;
  return;
 }
 pullCloud();
}

async function loadTitles() {
 try {
  titles = {...titles, ...titlesFromCatalog(await (await fetch(`${prefix}data/catalog.json`)).json())};
 } catch { /* 생성기 산출물이 없어도 주제 id로 보여 줍니다. */ }
 if (unit && window.aipyLearning && typeof window.aipyLearning.getState === 'function') {
  /* 단원 페이지는 레슨 제목을 DOM에서 보강합니다. */
 }
 document.querySelectorAll('section.lesson[id]').forEach((section) => {
  const heading = section.querySelector('h2');
  if (heading && unit) titles[`u${unit}-${section.id}`] = heading.textContent;
 });
 titles = {...titles, ...titlesFromLessons(
  [...document.querySelectorAll('section.lesson[id]')].map((el) => ({id: el.id, title: el.querySelector('h2')?.textContent || el.id})),
  unit
 )};
}

function start() {
 if (document.getElementById('teacher-shell')) return;
 mountSignals();
 loadTitles().then(paintHistory);
 paintChoices();
 window.aipyUnderstanding = {
  snapshot,
  store: () => store,
  key: UNDERSTANDING_KEY,
  flush: writeProgress
 };
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.addEventListener('pagehide', () => {
  persistLocal();
  if (user) writeProgress();
 });
}

start();
