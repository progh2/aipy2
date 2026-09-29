/* 학생 따라가기. 활성 세션이 있을 때만 UI를 붙이고, 실패하면 기존 학습만 남깁니다.
   M2 학습 기록 미러에 의존하지 않습니다. 코드는 localStorage(app.js)에 저장한 뒤 이동합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classId} from './class-picker.js';
import {
 isSessionLive, pageFromPath, shouldNavigate, focusHref, focusKey, topicFromHash,
 visibleTopic, presenceFields, readPendingFocus, writePendingFocus, readFollowing,
 writeFollowing, sessionStartChanged, PRESENCE_HEARTBEAT_MS, samePage, unitFromPage,
 parseAnchor, isPoppedTabMarker, poppedFocusDecision
} from './follow-model.js';

// (#132) 연습문제·예제·튜토리얼·보강 자료는 새 창(target=_blank rel=noopener)으로 연다.
// rel=noopener 탓에 window.opener는 항상 비어 있으므로, 그 링크들이 붙이는 ?w=1 쿼리
// 표식으로 "이 탭은 수업 원래 탭이 아니라 학생이 따로 연 탭"임을 판별한다. window.opener가
// 남아 있는 경우(다른 경로로 새 창이 열린 경우)도 함께 판별에 넣는다.
const isPoppedTab = Boolean(window.opener) || isPoppedTabMarker(location.search);
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
let lastAppliedExample = '';
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

// (#132) 새 창(따로 연 탭)에서, 교사 초점이 이 탭과 다른 페이지를 가리킬 때만 쓰는 작은 안내.
// showNotice(focus)와 달리 이동 버튼을 주지 않는다 — 이 탭은 옮기지 않기로 한 탭이기 때문이다.
function showPoppedNotice() {
 const box = ensureNotice();
 box.replaceChildren();
 box.append(node('p', 'follow-notice-text', '선생님이 다른 곳을 보고 있어요 — 원래 수업 창을 확인하세요.'));
 box.hidden = false;
 clearTimeout(noticeTimer);
 noticeTimer = setTimeout(hideNotice, 8000);
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
  // 이동 직전에는 로컬 저장만 한다. 동기화 flush를 부르면 코드 충돌 대화상자가 떠 이동을 가로막는다.
  if (window.aipyLearning && typeof window.aipyLearning.saveLocalQuiet === 'function') {
   window.aipyLearning.saveLocalQuiet();
  } else if (window.aipyLearning && typeof window.aipyLearning.saveLocal === 'function') {
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
 // (#142) 진도 막대(#progress-bar)가 있는 페이지는 그 바로 아래에 둔다 — 헤더 바로 다음에
 // 꽂으면 진도 막대와 같은 자리를 다투게 된다(둘 다 sticky). 진도 막대가 없는 페이지는
 // 헤더 바로 아래.
 const progressBar = document.getElementById('progress-bar');
 const header = document.querySelector('header.top');
 const anchor = progressBar || header;
 if (anchor) anchor.after(root);
 else document.body.prepend(root);
 if (window.aipyOffsets) window.aipyOffsets.sync();
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

// 'libraries@0.42' 또는 'libraries~b12@0.37' → {id, block, frac}. 블록이 있으면 그 블록(화면 한 장
// 단위, #126)을, 없으면(옛 형식·블록을 못 찾음) 컨테이너 전체 비율로 그 지점(선생님이 보던 높이)으로 간다.
// 앵커 파싱은 follow-model.js의 parseAnchor로 모아 두었다(페이지 판정과 같은 규칙을 쓴다).

// 자동 따라가기 중의 추적 갱신은 선생님 위치가 화면 높이의 이 비율 이상 멀어졌을 때만 옮긴다(잔 흔들림
// 방지). 블록 단위 추적(#126)으로 훨씬 촘촘해졌으므로 예전 0.4(화면 40%)보다 낮춘다.
const FOLLOW_MOVE_THRESHOLD = 0.15;

function scrollToId(anchor, force) {
 const {id, block, frac} = parseAnchor(anchor);
 // 블록을 먼저 찾는다. 옛 클라이언트가 보낸 앵커·블록이 사라진 경우엔 컨테이너 id로 폴백한다.
 const el = (block && document.querySelector(`[data-fb="${block}"]`)) || document.getElementById(id);
 if (!el) return false;
 if (frac == null) {
  ignoreScrollUntil = Date.now() + 1400;
  el.scrollIntoView({behavior: prefersSmooth() ? 'smooth' : 'auto', block: 'start'});
  flash(el);
 } else {
  const z = parseFloat(document.body.style.zoom) || 1;
  const r = el.getBoundingClientRect();
  const target = Math.max(0, window.scrollY + r.top + frac * r.height - 110 * z);
  const delta = Math.abs(target - window.scrollY);
  if (!force && delta < window.innerHeight * FOLLOW_MOVE_THRESHOLD) return true;
  ignoreScrollUntil = Date.now() + 1400;
  // 짧은 거리는 즉시 이동한다 — 연속 갱신이 smooth 애니메이션과 겹쳐 흔들리는 것을 줄인다.
  // 긴 거리는 그대로 smooth. scrollTo를 다시 호출하면 진행 중인 스크롤의 목표만 갈아탄다.
  const behavior = (!prefersSmooth() || delta < window.innerHeight * 0.05) ? 'auto' : 'smooth';
  window.scrollTo({top: target, behavior});
 }
 return true;
}

function applyExample(id) {
 if (!id || !window.aipyLearning || typeof window.aipyLearning.selectExample !== 'function') return;
 window.aipyLearning.selectExample(id);
}

// (#126, #130) 예제 페이지에서 교사가 편집기(#lab, data-fb 붙어 있음)를 보고 있으면 학생도 그
// 위치로 스크롤될 수 있다 — 학생이 코드나 저널을 입력하는 중이면 자동 스크롤로 입력 포커스를
// 빼앗지 않는다. 따라가기 상태 자체는 그대로 두고(안내·페이지 이동은 계속) 스크롤 이동만 건너뛴다.
function isEditingCode() {
 const el = document.activeElement;
 if (!el) return false;
 if (el.id === 'code-editor') return true;
 return el.tagName === 'TEXTAREA' && el.hasAttribute('data-journal');
}

function applyFocus(focus, force) {
 if (!focus || (!following && !force)) return;
 const key = focusKey(focus);
 if (!force && key && key === lastFocusKey) return;
 if (isPoppedTab) {
  // 새 창(따로 연 탭)은 교사 초점 때문에 다른 페이지로 이동하지 않는다(#132). 같은 페이지
  // 안의 다른 위치를 가리키면 스크롤만 하고, 다른 페이지를 가리키면 작은 안내만 띄운다.
  const decision = poppedFocusDecision(currentPage(), focus, true);
  lastFocusKey = key || lastFocusKey;
  if (decision.action === 'scroll') {
   whenLearningReady(() => { if (decision.topicAnchor && !isEditingCode()) scrollToId(decision.topicAnchor, force); });
  } else if (decision.action === 'notice') {
   showPoppedNotice();
  }
  return;
 }
 if (shouldNavigate(currentPage(), focus)) {
  // resolveFocusLocation(follow-model.js)이 앵커의 비율을 알아서 떼고 목적지를 판정한다.
  const href = focusHref(prefix, focus);
  // 목적지가 실제로 있는지 먼저 확인한다. 없는 주소로 보내면 학생 화면이 404로 튕긴다(2026-09-23 수업 사고).
  fetch(href, {method: 'HEAD'}).then((res) => {
   if (!res.ok) { console.warn('[follow] 없는 페이지라 이동하지 않습니다', href); return; }
   // HEAD 확인이 끝나 실제로 이동할 때만 키를 갱신한다. 실패 시 갱신을 건너뛰어야
   // 같은 초점이 나중에(재시도·재연결) 다시 와도 "이미 처리한 것"으로 무시되지 않는다.
   lastFocusKey = key || lastFocusKey;
   saveLocal();
   writePendingFocus(sessionStorage, focus);
   location.href = href;
  }).catch((error) => { console.warn('[follow] 이동 확인 실패', error); });
  return;
 }
 lastFocusKey = key || lastFocusKey;
 whenLearningReady(() => {
  if (focus.topicAnchor && !isEditingCode()) scrollToId(focus.topicAnchor, force);
  // 같은 예제를 다시 적용하면 편집기가 초기화되므로, 예제가 바뀌었을 때만 연다.
  if (focus.exampleId && (force || focus.exampleId !== lastAppliedExample)) {
   lastAppliedExample = focus.exampleId;
   applyExample(focus.exampleId);
   if (!focus.topicAnchor && !isEditingCode()) scrollToId('lab', force);
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

// 세션 구독 세대 번호. load()가 비동기라 그 사이 반이 다시 바뀌면(oldClass→newClass→oldClass 등)
// 먼저 시작한 load()가 나중에 끝나 옛 반을 구독해 버릴 수 있다 — 최신 호출만 구독을 등록한다.
let sessionGen = 0;

function listenSession() {
 const gen = ++sessionGen;
 const cls = classroom;
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 dropSession();
 if (!cls) return;
 load().then(({db, store}) => {
  const unsub = store.onSnapshot(
   store.doc(db, 'sessions', cls),
   (snapshot) => { if (gen === sessionGen) onSessionSnap(snapshot); },
   (error) => {
    if (gen !== sessionGen) return;
    console.warn('[follow] 세션을 구독하지 못했습니다.', error);
    dropSession();
   }
  );
  if (gen !== sessionGen) { unsub(); return; } // 오래된 호출 — 등록하지 않고 바로 해지
  sessionUnsub = unsub;
 }).catch((error) => {
  if (gen !== sessionGen) return;
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
 // 계정·반이 그대로면 재구독하지 않는다(불필요한 구독 해지·재생성으로 인한 경합 방지).
 if (uid === nextUid && classroom === nextClass && sessionUnsub) return;
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
