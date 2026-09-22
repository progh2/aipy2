/* 학생 따라가기. 활성 세션이 있을 때만 UI를 붙이고, 실패하면 기존 학습만 남깁니다.
   M2 학습 기록 미러에 의존하지 않습니다. 코드는 localStorage(app.js)에 저장한 뒤 이동합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classId} from './class-picker.js';
import {
 isSessionLive, pageFromPath, shouldNavigate, focusHref, focusKey, topicFromHash,
 visibleTopic, presenceFields, readPendingFocus, writePendingFocus, readFollowing,
 writeFollowing, sessionStartChanged, PRESENCE_HEARTBEAT_MS, samePage, unitFromPage
} from './follow-model.js';
import {titlesFromCatalog} from './understanding-model.js';

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
let lastNoticeKey = '';
let noticeTimer = 0;
let titles = {};
fetch(`${prefix}data/catalog.json`).then((r) => r.json()).then((c) => { titles = titlesFromCatalog(c); }).catch(() => {});

// 초점 위치를 사람이 읽을 이름으로
function describeFocus(focus) {
 const unit = unitFromPage(focus.page);
 const anchor = parseAnchor(focus.topicAnchor).id;
 const q = /^u\d-q(\d+)$/.exec(anchor);
 let label = '';
 if (q) label = `문제 ${Number(q[1])}번`;
 else if (anchor && titles[`u${unit}-${anchor}`]) label = titles[`u${unit}-${anchor}`];
 else if (anchor && document.getElementById(anchor)) label = (document.getElementById(anchor).querySelector('h2, h3') || {}).textContent || anchor;
 else if (focus.exampleId) label = `예제 ${focus.exampleId}`;
 else label = unit ? `${unit}단원` : '학습 페이지';
 const here = samePage(currentPage(), focus.page);
 return here ? `이 페이지의 「${label.trim()}」` : `${unit ? unit + '단원 ' : ''}「${label.trim()}」`;
}

// 우하단 안내: 입력을 막지 않고, 새 안내가 오면 이전 안내를 교체한다.
function ensureNotice() {
 let box = document.getElementById('follow-notice');
 if (box) return box;
 box = node('div', 'follow-notice');
 box.id = 'follow-notice';
 box.hidden = true;
 box.setAttribute('role', 'status');
 box.setAttribute('aria-live', 'polite');
 document.body.append(box);
 return box;
}

function hideNotice() {
 const box = document.getElementById('follow-notice');
 if (box) { box.hidden = true; box.replaceChildren(); }
 clearTimeout(noticeTimer);
}

function showNotice(focus) {
 const box = ensureNotice();
 box.replaceChildren();
 const text = node('p', 'follow-notice-text', `선생님이 ${describeFocus(focus)}(으)로 이동했어요.`);
 const actions = node('div', 'follow-notice-actions');
 const go = node('button', 'primary', '이동하기');
 go.type = 'button';
 go.addEventListener('click', () => { hideNotice(); applyFocus(focus, true); });
 const close = node('button', '', '닫기');
 close.type = 'button';
 close.addEventListener('click', hideNotice);
 actions.append(go, close);
 box.append(text, actions);
 box.hidden = false;
 clearTimeout(noticeTimer);
 noticeTimer = setTimeout(hideNotice, 3 * 60 * 1000);
}

function currentPage() {
 return pageFromPath(location.pathname);
}

function currentTopic() {
 if (document.body.dataset.topic) return document.body.dataset.topic;
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
 // 버튼은 세션 중 항상 보인다(#86): 따라가는 중이어도 '지금 선생님 위치로' 한 번 이동할 수 있다.
 rejoin.hidden = false;
 if (following) {
  status.textContent = '선생님 화면을 따라가는 중';
  rejoin.textContent = '선생님 화면으로 이동';
 } else {
  status.textContent = '잠깐 혼자 보는 중';
  rejoin.textContent = '선생님 화면으로 돌아가기';
 }
}

function showAttention() {
 const banner = document.getElementById('follow-attention');
 if (!banner) return;
 banner.hidden = false;
 clearTimeout(attentionTimer);
 attentionTimer = setTimeout(() => { banner.hidden = true; }, 6000);
}

function flash(el) {
 el.classList.remove('focus-flash');
 void el.offsetWidth; // 애니메이션 재시작
 el.classList.add('focus-flash');
 setTimeout(() => el.classList.remove('focus-flash'), 2600);
}

// 'libraries@0.42' → {id, frac}. 비율이 있으면 요소 안 그 지점(선생님이 보던 높이)으로 간다.
function parseAnchor(anchor) {
 const m = /^([^@]+)(?:@([0-9.]+))?$/.exec(String(anchor || ''));
 if (!m) return {id: '', frac: 0};
 const frac = m[2] === undefined ? null : Math.min(0.99, Math.max(0, parseFloat(m[2]) || 0));
 return {id: m[1], frac};
}

function scrollToId(anchor) {
 const {id, frac} = parseAnchor(anchor);
 const el = document.getElementById(id);
 if (!el) return false;
 ignoreScrollUntil = Date.now() + 1400;
 if (frac == null) {
  el.scrollIntoView({behavior: prefersSmooth() ? 'smooth' : 'auto', block: 'start'});
  flash(el);
 } else {
  const z = parseFloat(document.body.style.zoom) || 1;
  const r = el.getBoundingClientRect();
  const target = window.scrollY + r.top + frac * r.height - 110 * z;
  window.scrollTo({top: Math.max(0, target), behavior: prefersSmooth() ? 'smooth' : 'auto'});
 }
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
  location.href = focusHref(prefix, {...focus, topicAnchor: parseAnchor(focus.topicAnchor).id});
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
 if (liveSession && liveSession.focus && liveSession.focus.page) applyFocus(liveSession.focus, true);
 else {
  const box = document.getElementById('toast');
  if (box) { box.textContent = '아직 선생님이 보낸 위치가 없어요. 잠시 후 다시 눌러 보세요.'; setTimeout(() => { box.textContent = ''; }, 4000); }
 }
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
 lastNoticeKey = '';
 hideNotice();
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
  const key = focusKey(data.focus);
  // 따라가는 중이든 아니든 새 초점은 우하단 안내로 알린다(따라가는 중이면 아래에서 자동 이동도 한다).
  // 교사 스크롤 추적('id@비율')은 조용히 따라가고, 📍로 보낸 초점(비율 없음)만 안내를 띄운다.
  const passive = parseAnchor(data.focus && data.focus.topicAnchor).frac != null;
  if (key && key !== lastNoticeKey) { lastNoticeKey = key; if (!passive) showNotice(data.focus); }
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
