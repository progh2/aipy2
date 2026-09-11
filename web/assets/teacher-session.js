/* 교사 수업 세션. 헤더에서 고른 반(window.aipyClass)의 sessions/{학년}-{반}을 만들고 초점을 보냅니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {labelClass} from './class-picker.js';
import {
 isSessionLive, timestampMillis, countPresence, catalogPages, catalogTopics,
 catalogExamples, sessionFields, expiresAtMillis, wholeNonce, DEFAULT_PAGE
} from './follow-model.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let catalog = {pages: [], topics: {}, examples: {}};
let classIdValue = '';
let teacherEmail = '';
let current = null;
let sessionUnsub = null;
let presenceUnsub = null;

function fillSelect(select, items, selected) {
 select.replaceChildren();
 for (const item of items) {
  const opt = node('option', '', item.title);
  opt.value = item.id;
  if (item.id === selected) opt.selected = true;
  select.append(opt);
 }
}

function selectedFocus() {
 const page = $('focus-page').value || DEFAULT_PAGE;
 const topic = $('focus-topic').value || null;
 const example = $('focus-example').value || null;
 return {page, topicAnchor: topic, exampleId: example};
}

function refillTopics(keep) {
 const page = $('focus-page').value;
 const topics = catalogTopics(catalog, page).map((t) => ({id: t.id, title: t.title}));
 fillSelect($('focus-topic'), [{id: '', title: '(주제 없음)'}, ...topics], keep || '');
 refillExamples(keep ? $('focus-example').value : '');
}

function refillExamples(keep) {
 const page = $('focus-page').value;
 const topicId = $('focus-topic').value;
 const topic = catalogTopics(catalog, page).find((t) => t.id === topicId);
 const examples = catalogExamples(catalog, topic);
 fillSelect($('focus-example'), [{id: '', title: '(예제 없음)'}, ...examples], keep || '');
}

function paintFocusFromSession(session) {
 const focus = session && session.focus;
 const page = (focus && focus.page) || (catalogPages(catalog)[0] && catalogPages(catalog)[0].id) || DEFAULT_PAGE;
 fillSelect($('focus-page'), catalogPages(catalog).map((p) => ({id: p.id, title: p.label || p.id})), page);
 refillTopics(focus && focus.topicAnchor);
 if (focus && focus.exampleId) $('focus-example').value = focus.exampleId;
}

function formatExpiry(session) {
 const exp = timestampMillis(session && session.expiresAt);
 if (!exp) return '';
 return new Date(exp).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
}

function paintStatus() {
 const status = $('session-status');
 const start = $('session-start');
 const end = $('session-end');
 const send = $('focus-send');
 const attention = $('attention-send');
 const hasClass = Boolean(classIdValue);
 start.disabled = !hasClass || !teacherEmail;
 if (!hasClass) {
  status.textContent = '위에서 수업할 반을 선택하세요.';
  end.disabled = true;
  send.disabled = true;
  attention.disabled = true;
  return;
 }
 if (!current || !isSessionLive(current)) {
  status.textContent = `${labelClass(classIdValue)} 세션이 없습니다. 세션 시작을 누르면 2시간 동안 유지됩니다.`;
  end.disabled = true;
  send.disabled = true;
  attention.disabled = true;
  return;
 }
 status.textContent = `${labelClass(classIdValue)} 진행 중 · 만료 ${formatExpiry(current) || '미정'}`;
 end.disabled = false;
 send.disabled = false;
 attention.disabled = false;
}

function paintCounts(rows) {
 const {following, browsing} = countPresence(rows);
 $('presence-counts').textContent = `따라오는 중 ${following} / 따로 보는 중 ${browsing}`;
}

function note(text) {
 $('focus-note').textContent = text || '';
}

async function startSession() {
 if (!classIdValue || !teacherEmail) return;
 const {page, topicAnchor, exampleId} = selectedFocus();
 try {
  const {db, store} = await load();
  const fields = sessionFields({teacherEmail, page, topicAnchor, exampleId});
  await store.setDoc(store.doc(db, 'sessions', classIdValue), {
   active: fields.active,
   teacherEmail: fields.teacherEmail,
   startedAt: store.serverTimestamp(),
   expiresAt: store.Timestamp.fromMillis(expiresAtMillis()),
   focus: {
    page: fields.focus.page,
    topicAnchor: fields.focus.topicAnchor,
    exampleId: fields.focus.exampleId,
    updatedAt: store.serverTimestamp()
   },
   attention: {nonce: wholeNonce(fields.attention.nonce), at: store.serverTimestamp()}
  });
  note('세션을 시작했습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`세션을 시작하지 못했습니다. (${error.code || error})`);
 }
}

async function endSession() {
 if (!classIdValue || !current) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {active: false});
  note('세션을 종료했습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`세션을 종료하지 못했습니다. (${error.code || error})`);
 }
}

async function sendFocus() {
 if (!classIdValue || !isSessionLive(current)) return;
 const {page, topicAnchor, exampleId} = selectedFocus();
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   'focus.page': page,
   'focus.topicAnchor': topicAnchor || null,
   'focus.exampleId': exampleId || null,
   'focus.updatedAt': store.serverTimestamp()
  });
  note('초점을 보냈습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`초점을 보내지 못했습니다. (${error.code || error})`);
 }
}

async function sendAttention() {
 if (!classIdValue || !isSessionLive(current)) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   'attention.nonce': store.increment(1),
   'attention.at': store.serverTimestamp()
  });
  note('시선을 모았습니다. 학생 화면에는 배너만 표시됩니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`시선 모으기를 보내지 못했습니다. (${error.code || error})`);
 }
}

function listen(id) {
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 if (presenceUnsub) {
  presenceUnsub();
  presenceUnsub = null;
 }
 current = null;
 paintCounts([]);
 paintStatus();
 if (!id || !teacherEmail) return;
 load().then(({db, store}) => {
  sessionUnsub = store.onSnapshot(store.doc(db, 'sessions', id), (snap) => {
   current = snap.exists() ? snap.data() : null;
   if (current && current.focus && !$('focus-page').dataset.dirty) paintFocusFromSession(current);
   paintStatus();
  }, (error) => {
   console.error('[teacher-session]', error);
   note('세션을 읽지 못했습니다.');
  });
  presenceUnsub = store.onSnapshot(
   store.query(store.collection(db, 'presence'), store.where('classroom', '==', id)),
   (snap) => {
    const rows = [];
    snap.forEach((doc) => rows.push(doc.data()));
    paintCounts(rows);
   },
   (error) => {
    console.error('[teacher-session]', error);
    $('presence-counts').textContent = '따라오는 중 — / 따로 보는 중 —';
   }
  );
 }).catch((error) => {
  console.error('[teacher-session]', error);
  note('세션 기능을 불러오지 못했습니다.');
 });
}

function onClass(detail) {
 classIdValue = (detail && detail.classId) || '';
 listen(classIdValue);
}

function onAccount(detail) {
 const user = detail && detail.user;
 teacherEmail = (user && user.email) ? user.email.toLowerCase() : '';
 paintStatus();
 if (classIdValue) listen(classIdValue);
}

async function startTeacherSession() {
 if (!$('session-start')) return;
 if (!ready) {
  $('session-status').textContent = '로그인 설정이 없어 세션을 시작할 수 없습니다.';
  return;
 }
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
 } catch (error) {
  console.error('[teacher-session]', error);
  note('단원 목록을 읽지 못했습니다. 생성기를 다시 실행하세요.');
 }
 paintFocusFromSession(null);
 $('focus-page').onchange = () => {
  $('focus-page').dataset.dirty = '1';
  refillTopics('');
 };
 $('focus-topic').onchange = () => {
  $('focus-page').dataset.dirty = '1';
  refillExamples('');
 };
 $('focus-example').onchange = () => { $('focus-page').dataset.dirty = '1'; };
 $('session-start').onclick = startSession;
 $('session-end').onclick = endSession;
 $('focus-send').onclick = sendFocus;
 $('attention-send').onclick = sendAttention;
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
 if (window.aipyAccount) onAccount(window.aipyAccount);
 paintStatus();
}

startTeacherSession();
