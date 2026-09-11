/* 학생 따라가기. 활성 세션이 있을 때만 UI를 붙이고, 실패하면 기존 학습만 남깁니다.
   M2 학습 기록 미러에 의존하지 않습니다. 코드는 localStorage(app.js)에 저장한 뒤 이동합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classId} from './class-picker.js';
import {
 isSessionLive, pageFromPath, shouldNavigate, focusHref, focusKey, topicFromHash,
 visibleTopic, presenceFields, readPendingFocus, writePendingFocus, readFollowing,
 writeFollowing, sessionStartChanged, PRESENCE_HEARTBEAT_MS
} from './follow-model.js';

const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let classroom = '';
let uid = '';
let following = true;
let sessionUnsub = null;
let heartbeatTimer = null;
let liveSession = null;
let lastFocusKey = '';
let seenNonce = null;
let ignoreScrollUntil = 0;
let attentionTimer = 0;

function currentPage() {
 return pageFromPath(location.pathname);
}

function currentTopic() {
 const fromHash = topicFromHash(location.hash);
 if (fromHash && document.getElementById(fromHash)) return fromHash;
 const lessons = [...document.querySelectorAll('section.lesson[id]')].map((el) => ({
  id: el.id,
  top: el.getBoundingClientRect().top
 }));
 return visibleTopic(lessons, 130) || fromHash;
}

function prefersSmooth() {
 return !matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function saveLocal() {
 try {
  if (window.aipyLearning && typeof window.aipyLearning.saveLocal === 'function') {
   window.aipyLearning.saveLocal();
  }
 } catch (error) {
  console.warn('[follow] 로컬 저장 실패', error);
 }
}

function whenLearningReady(done) {
 if (window.aipyLearning && window.aipyLearning.ready) {
  done();
  return;
 }
 const finish = () => done();
 document.addEventListener('aipy:learning-ready', finish, {once: true});
 setTimeout(finish, 4000);
}

function ensureUi() {
 let root = document.getElementById('follow-ui');
 if (root) return root;
 root = node('div', 'follow-ui');
 root.id = 'follow-ui';
 root.hidden = true;
 const bar = node('div', 'follow-bar');
 const status = node('p', 'follow-status', '');
 status.id = 'follow-status';
 const rejoin = node('button', 'follow-rejoin', '선생님 화면으로');
 rejoin.id = 'follow-rejoin';
 rejoin.type = 'button';
 rejoin.hidden = true;
 rejoin.addEventListener('click', rejoinFocus);
 bar.append(status, rejoin);
 const attention = node('p', 'follow-attention', '선생님이 여기를 보고 있어요');
 attention.id = 'follow-attention';
 attention.hidden = true;
 attention.setAttribute('role', 'status');
 root.append(bar, attention);
 const header = document.querySelector('header.top');
 if (header) header.after(root);
 else document.body.prepend(root);
 return root;
}

function hideUi() {
 const root = document.getElementById('follow-ui');
 if (root) root.hidden = true;
 document.body.classList.remove('follow-active');
 const attention = document.getElementById('follow-attention');
 if (attention) attention.hidden = true;
}

function paintUi() {
 if (!liveSession) {
  hideUi();
  return;
 }
 const root = ensureUi();
 root.hidden = false;
 document.body.classList.add('follow-active');
 const status = document.getElementById('follow-status');
 const rejoin = document.getElementById('follow-rejoin');
 if (following) {
  status.textContent = '선생님 화면을 따라가는 중';
  rejoin.hidden = true;
 } else {
  status.textContent = '잠깐 혼자 보는 중';
  rejoin.hidden = false;
 }
}

function showAttention() {
 const banner = document.getElementById('follow-attention');
 if (!banner) return;
 banner.hidden = false;
 clearTimeout(attentionTimer);
 attentionTimer = setTimeout(() => { banner.hidden = true; }, 6000);
}

function scrollToId(id) {
 const el = document.getElementById(id);
 if (!el) return false;
 ignoreScrollUntil = Date.now() + 1400;
 el.scrollIntoView({behavior: prefersSmooth() ? 'smooth' : 'auto', block: 'start'});
 return true;
}

function applyExample(id) {
 if (!id || !window.aipyLearning || typeof window.aipyLearning.selectExample !== 'function') return;
 window.aipyLearning.selectExample(id);
}

function applyFocus(focus, force) {
 if (!focus || (!following && !force)) return;
 const key = focusKey(focus);
 if (!force && key && key === lastFocusKey) return;
 lastFocusKey = key || lastFocusKey;
 if (shouldNavigate(currentPage(), focus)) {
  saveLocal();
  writePendingFocus(sessionStorage, focus);
  location.href = focusHref(prefix, focus);
  return;
 }
 whenLearningReady(() => {
  if (focus.topicAnchor) scrollToId(focus.topicAnchor);
  if (focus.exampleId) {
   applyExample(focus.exampleId);
   if (!focus.topicAnchor) scrollToId('lab');
  }
 });
}

function persistFollowing() {
 writeFollowing(sessionStorage, classroom, liveSession, following);
}

function rejoinFocus() {
 following = true;
 persistFollowing();
 paintUi();
 if (liveSession && liveSession.focus) applyFocus(liveSession.focus, true);
 writePresence();
}

function markIndependent() {
 if (!following || !liveSession) return;
 if (Date.now() < ignoreScrollUntil) return;
 following = false;
 persistFollowing();
 paintUi();
 writePresence();
}

function onUserScrollIntent() {
 markIndependent();
}

async function writePresence() {
 if (!uid || !classroom || !liveSession) return;
 try {
  const {db, store} = await load();
  await store.setDoc(
   store.doc(db, 'presence', uid),
   {
    ...presenceFields({
     classroom,
     page: currentPage(),
     topicAnchor: currentTopic(),
     following
    }),
    updatedAt: store.serverTimestamp()
   }
  );
 } catch (error) {
  console.warn('[follow] 접속 상태를 쓰지 못했습니다.', error);
 }
}

async function clearPresence() {
 if (!uid) return;
 try {
  const {db, store} = await load();
  await store.deleteDoc(store.doc(db, 'presence', uid));
 } catch { /* 규칙·네트워크 실패는 학습을 막지 않습니다. */ }
}

function stopHeartbeat() {
 clearInterval(heartbeatTimer);
 heartbeatTimer = null;
}

function startHeartbeat() {
 stopHeartbeat();
 writePresence();
 heartbeatTimer = setInterval(() => {
  if (document.hidden) return;
  writePresence();
 }, PRESENCE_HEARTBEAT_MS);
}

function dropSession() {
 liveSession = null;
 lastFocusKey = '';
 seenNonce = null;
 stopHeartbeat();
 hideUi();
}

function onSessionSnap(snapshot) {
 if (!snapshot.exists()) {
  dropSession();
  return;
 }
 const data = snapshot.data();
 if (!isSessionLive(data)) {
  dropSession();
  return;
 }
 const first = !liveSession;
 const restarted = sessionStartChanged(liveSession, data);
 liveSession = data;
 const nonce = data.attention && typeof data.attention.nonce === 'number' ? data.attention.nonce : 0;
 if (first || restarted) {
  following = readFollowing(sessionStorage, classroom, data);
  persistFollowing();
  seenNonce = nonce;
  const pending = first ? readPendingFocus(sessionStorage) : null;
  paintUi();
  applyFocus((pending && pending.page) ? pending : data.focus, following);
 } else {
  if (seenNonce != null && nonce > seenNonce) showAttention();
  seenNonce = nonce;
  paintUi();
  applyFocus(data.focus, false);
 }
 if (!document.hidden) startHeartbeat();
}

function listenSession() {
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 dropSession();
 if (!classroom) return;
 load().then(({db, store}) => {
  sessionUnsub = store.onSnapshot(
   store.doc(db, 'sessions', classroom),
   onSessionSnap,
   (error) => {
    console.warn('[follow] 세션을 구독하지 못했습니다.', error);
    dropSession();
   }
  );
 }).catch((error) => {
  console.warn('[follow] 따라가기를 시작하지 못했습니다.', error);
  dropSession();
 });
}

function onAccount(detail) {
 const profile = detail && detail.profile;
 const user = detail && detail.user;
 const nextUid = (user && user.uid) || '';
 const nextClass = classId(profile);
 if (!nextUid || !nextClass) {
  if (sessionUnsub) {
   sessionUnsub();
   sessionUnsub = null;
  }
  stopHeartbeat();
  if (uid) clearPresence();
  uid = nextUid;
  classroom = nextClass;
  dropSession();
  return;
 }
 uid = nextUid;
 classroom = nextClass;
 listenSession();
}

function startFollow() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!ready) return;
 ensureUi();
 hideUi();
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.addEventListener('wheel', onUserScrollIntent, {passive: true});
 window.addEventListener('touchmove', onUserScrollIntent, {passive: true});
 window.addEventListener('keydown', (event) => {
  if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '].includes(event.key)) {
   onUserScrollIntent();
  }
 });
 document.addEventListener('visibilitychange', () => {
  if (document.hidden) stopHeartbeat();
  else if (liveSession) startHeartbeat();
 });
 window.addEventListener('pagehide', saveLocal);
}

startFollow();
