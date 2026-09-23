/* 기기 간 편집 잠금. 한 학생이 두 기기(학교 PC·집 PC)에서 같은 코드 예제를 동시에 열면
   sync.js의 "어느 코드를 남길까요?" 충돌 대화상자가 뜬다. 이를 막기 위해 한 번에 한 기기만
   편집을 허용하고, 다른 기기가 이미 쥐고 있으면 이 기기는 읽기 전용으로 시작한다.
   Firestore editLocks/{uid} 문서 하나로 판단하며, 실패해도 학습(코드 실행·읽기)은 막지 않는다.
   #121: 같은 브라우저의 두 탭도 서로 다른 잠금 소유자로 구분한다(탭id는 sessionStorage). */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {
 LOCK_FRESH_MS, HEARTBEAT_MS, LOCK_NOTE, deviceLabel, isFresh, heldByOther, lockFields, newDeviceId,
 newTabId, combineDeviceId, lockOwnerLabel
} from './editlock-model.js';

const DEVICE_KEY = 'aipy-device-id';
const TAB_KEY = 'aipy-tab-id';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

function readDeviceId() {
 try {
  const existing = localStorage.getItem(DEVICE_KEY);
  if (existing) return existing;
  const created = newDeviceId();
  localStorage.setItem(DEVICE_KEY, created);
  return created;
 } catch {
  // localStorage를 못 쓰면 탭마다 새 기기로 취급한다(잠금은 보조 장치이므로 무해하다).
  return newDeviceId();
 }
}

// 탭마다 하나. 새로고침에는 sessionStorage가 남아 있으므로 같은 탭이 계속 같은 id를 쓴다.
function readTabId() {
 try {
  const existing = sessionStorage.getItem(TAB_KEY);
  if (existing) return existing;
  const created = newTabId();
  sessionStorage.setItem(TAB_KEY, created);
  return created;
 } catch {
  return newTabId();
 }
}

const deviceId = readDeviceId();
const tabId = readTabId();
// 잠금 문서에는 이 조합 id를 쓴다 — 같은 기기의 다른 탭과도 구분된다.
const lockOwnerId = combineDeviceId(deviceId, tabId);
const label = deviceLabel(navigator.userAgent);

let user = null;
let profile = null;
let unsub = null;
let heartbeatTimer = null;
let latestLock = null;
let editable = true;
let sawFirstSnapshot = false;
let bar = null;

function editor() { return document.getElementById('code-editor'); }

function lockDocFor(uid) {
 return async () => {
  const {db, store} = await load();
  return {db, store, ref: store.doc(db, 'editLocks', uid)};
 };
}

function ensureBar() {
 if (bar) return bar;
 const editorEl = editor();
 if (!editorEl) return null;
 bar = node('div', 'editlock-bar');
 bar.id = 'editlock-bar';
 bar.hidden = true;
 bar.setAttribute('role', 'status');
 bar.setAttribute('aria-live', 'polite');
 const text = node('span', 'editlock-text', '');
 text.id = 'editlock-text';
 const take = node('button', 'editlock-take', '이 기기에서 편집하기');
 take.type = 'button';
 take.id = 'editlock-take';
 take.title = LOCK_NOTE;
 take.addEventListener('click', takeover);
 bar.append(text, take);
 const wrap = editorEl.closest('.hl-wrap') || editorEl;
 wrap.parentNode.insertBefore(bar, wrap);
 return bar;
}

// mode: 'locked'(다른 기기가 쥐고 있음, 빼앗기기 전부터) | 'taken-over'(방금 다른 기기가 가져감) | null(편집 가능)
function setReadOnly(readOnly, mode, lock) {
 editable = !readOnly;
 const editorEl = editor();
 if (editorEl) editorEl.readOnly = readOnly;
 document.body.classList.toggle('edit-locked', readOnly);
 for (const id of ['add-file', 'delete-file', 'reset-code']) {
  const el = document.getElementById(id);
  if (el) el.disabled = readOnly;
 }
 const b = ensureBar();
 if (!b) return;
 const text = document.getElementById('editlock-text');
 const take = document.getElementById('editlock-take');
 if (!readOnly) {
  b.hidden = true;
  b.classList.remove('editlock-locked');
  return;
 }
 b.hidden = false;
 b.classList.add('editlock-locked');
 if (text) {
  text.textContent = mode === 'taken-over'
   ? '다른 기기가 편집을 가져갔어요. '
   : `${lockOwnerLabel(lock, lockOwnerId)}에서 편집 중이에요. `;
 }
 if (take) take.hidden = false;
}

async function writeLock(reason) {
 if (!user || !profile) return;
 try {
  const {store, ref} = await lockDocFor(user.uid)();
  await store.setDoc(ref, {
   ...lockFields({profile, deviceId: lockOwnerId, label, now: Date.now()}),
   updatedAt: store.serverTimestamp()
  });
 } catch (error) {
  console.warn('[editlock] 잠금을 쓰지 못했습니다.', reason, error);
 }
}

function stopHeartbeat() {
 clearInterval(heartbeatTimer);
 heartbeatTimer = null;
}

function startHeartbeat() {
 stopHeartbeat();
 heartbeatTimer = setInterval(() => {
  if (document.hidden) return;
  writeLock('heartbeat');
 }, HEARTBEAT_MS);
}

async function takeover() {
 await writeLock('takeover');
 setReadOnly(false, null);
 startHeartbeat();
}

function wasMine(lock) {
 return Boolean(lock && lock.deviceId === lockOwnerId);
}

function onLockSnap(snapshot) {
 const now = Date.now();
 const data = snapshot.exists() ? snapshot.data() : null;
 // 스냅샷 직전에 내가 편집 가능한 상태였는데, 이번에 다른 탭(다른 기기 포함)이 신선한
 // 잠금으로 나타났다면 "가져간" 것이다(원래부터 다른 쪽이 쥐고 있던 것과 구분해 배너 문구를
 // 다르게 보여 준다).
 const justLost = sawFirstSnapshot && editable && heldByOther(data, lockOwnerId, now);
 sawFirstSnapshot = true;
 latestLock = data;
 if (heldByOther(data, lockOwnerId, now)) {
  stopHeartbeat();
  setReadOnly(true, justLost ? 'taken-over' : 'locked', data);
  return;
 }
 // 잠금이 없거나(첫 사용), 만료됐거나, 이미 이 탭 것이면 이 탭이 편집을 갖는다.
 setReadOnly(false, null);
 if (!wasMine(data) || !isFresh(data, now)) writeLock('claim');
 startHeartbeat();
}

function listen() {
 if (unsub) { unsub(); unsub = null; }
 sawFirstSnapshot = false;
 if (!user) return;
 load().then(({db, store}) => {
  unsub = store.onSnapshot(
   store.doc(db, 'editLocks', user.uid),
   onLockSnap,
   (error) => {
    console.warn('[editlock] 잠금 구독 실패', error);
    setReadOnly(false, null);
   }
  );
 }).catch((error) => {
  console.warn('[editlock] 시작하지 못했습니다.', error);
  setReadOnly(false, null);
 });
}

async function releaseIfMine() {
 if (!user || !wasMine(latestLock)) return;
 try {
  const {store, ref} = await lockDocFor(user.uid)();
  await store.deleteDoc(ref);
 } catch { /* 실패해도 됨 — 만료(beat 끊김)가 나중에 처리한다 */ }
}

function onAccount(detail) {
 const nextUser = detail && detail.user;
 const nextProfile = detail && detail.profile;
 if (!nextUser || !nextProfile) {
  if (unsub) { unsub(); unsub = null; }
  stopHeartbeat();
  user = null;
  profile = null;
  latestLock = null;
  setReadOnly(false, null);
  return;
 }
 user = nextUser;
 profile = nextProfile;
 listen();
}

function start() {
 if (!editor()) return;
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!ready) return;
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.addEventListener('pagehide', () => { releaseIfMine(); });
 document.addEventListener('visibilitychange', () => {
  if (document.hidden) stopHeartbeat();
  else if (user && editable) startHeartbeat();
 });
}

start();
