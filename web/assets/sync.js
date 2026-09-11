/* 학습 기록 클라우드 미러. 화면은 app.js의 localStorage를 즉시 읽고 쓰며,
   이 모듈은 로그인된 뒤에만 백그라운드로 students/{uid}/state/current 와 progress/{uid} 를 맞춥니다.
   실패·미로그인·권한 거부는 학습을 막지 않고 로컬만 사용합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {
 LEARNING_KEY, CODE_IDLE_MS, shouldFlushNow, stampChanged, mergeStates, mapsChanged,
 progressFields, statePayload, cloudToState, cloneState, projectPreview, emptyState
} from './sync-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

const STATUS = {
 local: '로컬만',
 pending: '동기화 대기',
 syncing: '동기화 중',
 synced: '다른 기기와 맞춤',
 error: '로컬만 · 동기화 실패',
 conflict: '코드 버전 선택'
};

let user = null;
let profile = null;
let lastLocal = emptyState();
let choices = {};
let statusMode = 'local';
let idleTimer = 0;
let writing = false;
let pendingKind = '';
let started = false;

function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text;
}

function liveState() {
 if (window.aipyLearning && typeof window.aipyLearning.getState === 'function') {
  return window.aipyLearning.getState();
 }
 try {
  return JSON.parse(localStorage.getItem(LEARNING_KEY) || 'null') || emptyState();
 } catch {
  return emptyState();
 }
}

function persist(state) {
 try { localStorage.setItem(LEARNING_KEY, JSON.stringify(state)); } catch {}
 if (window.aipyLearning && window.aipyLearning.getState) {
  const live = window.aipyLearning.getState();
  if (live && live.times) {
   live.times = state.times;
   if (state.last !== undefined) live.last = state.last;
  }
 }
}

function applyToUi(state) {
 if (window.aipyLearning && typeof window.aipyLearning.applyRemote === 'function') {
  window.aipyLearning.applyRemote(state);
 } else persist(state);
}

function ensureStatus() {
 const slot = document.getElementById('account');
 if (!slot) return null;
 let el = document.getElementById('sync-status');
 if (!el) {
  el = node('span', 'account-sync', STATUS[statusMode]);
  el.id = 'sync-status';
 }
 if (el.parentNode !== slot) slot.append(el);
 return el;
}

function setStatus(mode, detail) {
 statusMode = mode;
 const el = ensureStatus();
 if (!el) return;
 el.dataset.sync = mode;
 el.textContent = STATUS[mode] || STATUS.local;
 el.title = detail || STATUS[mode] || '';
}

function stampNow(kind) {
 if (kind === 'remote') return liveState();
 const current = liveState();
 const stamped = stampChanged(lastLocal, current, Date.now());
 persist(stamped);
 lastLocal = cloneState(stamped);
 return stamped;
}

function schedule(kind) {
 if (!user || !profile) return;
 if (kind === 'remote') return;
 pendingKind = kind;
 if (shouldFlushNow(kind)) {
  clearTimeout(idleTimer);
  flush();
  return;
 }
 clearTimeout(idleTimer);
 idleTimer = setTimeout(() => { flush(); }, CODE_IDLE_MS);
 setStatus(statusMode === 'synced' ? 'pending' : statusMode, '코드·저널은 잠시 후 또는 페이지를 나갈 때 동기화합니다.');
}

async function flush() {
 if (!user || !profile || writing) return;
 clearTimeout(idleTimer);
 const local = stampNow(pendingKind || 'save');
 pendingKind = '';
 writing = true;
 setStatus('syncing');
 try {
  const {db, store} = await load();
  const stateRef = store.doc(db, 'students', user.uid, 'state', 'current');
  const progressRef = store.doc(db, 'progress', user.uid);
  const result = await store.runTransaction(db, async (tx) => {
   const snap = await tx.get(stateRef);
   const prev = await tx.get(progressRef);
   const cloud = snap.exists() ? cloudToState(snap.data()) : emptyState();
   const merged = mergeStates(local, cloud, choices, Date.now());
   if (merged.unresolved.length) return {merged, wrote: false};
   const payload = statePayload(merged.state);
   payload.updatedAt = store.serverTimestamp();
   tx.set(stateRef, payload);
   const liveUnderstanding = (window.aipyUnderstanding && typeof window.aipyUnderstanding.snapshot === 'function')
    ? window.aipyUnderstanding.snapshot()
    : (prev.exists() ? prev.data().understanding : {});
   const progress = progressFields(profile, merged.state, Date.now(), liveUnderstanding);
   progress.updatedAt = store.serverTimestamp();
   tx.set(progressRef, progress);
   return {merged, wrote: true};
  });
  if (mapsChanged(local, result.merged.state)) applyToUi(result.merged.state);
  lastLocal = cloneState(result.merged.state);
  if (!result.wrote) {
   writing = false;
   setStatus('conflict', '같은 예제 코드가 기기마다 다릅니다. 남길 버전을 고르세요.');
   await resolveConflicts(result.merged.unresolved, local);
   return;
  }
  setStatus('synced');
 } catch (error) {
  console.warn('[sync]', error);
  const denied = error && (error.code === 'permission-denied' || /permission/i.test(String(error.message || '')));
  setStatus('error', denied ? '저장 권한이 없어 이 브라우저에만 기록합니다.' : '네트워크를 확인하세요. 학습은 이 브라우저에서 이어집니다.');
 } finally {
  writing = false;
 }
}

async function pullAndMerge() {
 if (!user || !profile) return;
 setStatus('syncing');
 try {
  const {db, store} = await load();
  const snap = await store.getDoc(store.doc(db, 'students', user.uid, 'state', 'current'));
  const cloud = snap.exists() ? cloudToState(snap.data()) : emptyState();
  const local = stampNow('save');
  const merged = mergeStates(local, cloud, choices, Date.now());
  if (mapsChanged(local, merged.state)) applyToUi(merged.state);
  lastLocal = cloneState(merged.state);
  if (merged.unresolved.length) {
   setStatus('conflict');
   await resolveConflicts(merged.unresolved, local);
   return;
  }
  await flush();
 } catch (error) {
  console.warn('[sync]', error);
  setStatus('error', '계정에 저장한 기록을 읽지 못했습니다. 이 브라우저 기록으로 학습하세요.');
 }
}

function conflictCard(id, side, project, time) {
 const preview = projectPreview(project);
 const card = node('article', 'sync-choice');
 const when = time ? new Date(time).toLocaleString('ko-KR') : '시각 없음';
 card.append(
  node('h3', '', side === 'local' ? '이 브라우저' : '다른 기기'),
  node('p', 'small', `${preview.entry || '파일 없음'} · 파일 ${preview.files}개 · ${when}`),
  node('pre', '', preview.snippet || '(비어 있음)')
 );
 return card;
}

function askConflict(id, localProject, cloudProject, localTime, cloudTime) {
 return new Promise((resolve) => {
  const overlay = node('div', 'sync-overlay');
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'sync-conflict-title');
  const box = node('div', 'sync-dialog');
  box.append(node('h2', '', '어느 코드를 남길까요?'));
  const title = node('p', '', `예제 “${id}” 코드가 이 브라우저와 다른 기기에서 서로 다릅니다. 고르지 않은 쪽은 이 기록에서 사라집니다.`);
  title.id = 'sync-conflict-title';
  box.append(title);
  const grid = node('div', 'sync-choices');
  grid.append(conflictCard(id, 'local', localProject, localTime), conflictCard(id, 'cloud', cloudProject, cloudTime));
  box.append(grid);
  const actions = node('div', 'actions');
  const keepLocal = node('button', 'primary', '이 브라우저 코드');
  const keepCloud = node('button', '', '다른 기기 코드');
  keepLocal.type = 'button';
  keepCloud.type = 'button';
  keepLocal.onclick = () => { overlay.remove(); resolve('local'); };
  keepCloud.onclick = () => { overlay.remove(); resolve('cloud'); };
  actions.append(keepLocal, keepCloud);
  box.append(actions);
  overlay.append(box);
  document.body.append(overlay);
  keepLocal.focus();
 });
}

async function resolveConflicts(conflicts, local) {
 for (const item of conflicts) {
  if (choices[item.id]) continue;
  choices[item.id] = await askConflict(item.id, item.local, item.cloud, item.localTime, item.cloudTime);
 }
 // 고른 뒤 클라우드 원본을 다시 읽어 같은 선택으로 병합합니다.
 try {
  const {db, store} = await load();
  const snap = await store.getDoc(store.doc(db, 'students', user.uid, 'state', 'current'));
  const cloud = snap.exists() ? cloudToState(snap.data()) : emptyState();
  const again = mergeStates(local, cloud, choices, Date.now());
  applyToUi(again.state);
  lastLocal = cloneState(again.state);
 } catch {
  const again = mergeStates(local, emptyState(), choices, Date.now());
  applyToUi(again.state);
  lastLocal = cloneState(again.state);
 }
 await flush();
}

async function onAccount(detail) {
 const nextUser = detail && detail.user;
 const nextProfile = detail && detail.profile;
 if (!nextUser || !nextProfile) {
  user = null;
  profile = null;
  choices = {};
  clearTimeout(idleTimer);
  setStatus('local', '로그인하면 다른 기기와 학습 기록을 맞춥니다.');
  return;
 }
 user = nextUser;
 profile = nextProfile;
 lastLocal = cloneState(liveState());
 await pullAndMerge();
}

function onLocalChange(kind) {
 try { schedule(kind || 'save'); } catch (error) { console.warn('[sync]', error); }
}

function confirmClearLocal() {
 return confirm('이 브라우저의 학습 기록을 지울까요? 계정에 저장한 기록은 그대로 남아요.\n\n확인: 이 컴퓨터 기록만 지우기\n취소: 이 브라우저에 기록 남기기');
}

function hookLearning() {
 lastLocal = cloneState(liveState());
 if (window.aipyLearning) window.aipyLearning.onLocalChange = onLocalChange;
}

function start() {
 if (started) return;
 started = true;
 window.aipySync = {flush, confirmClearLocal, status: () => statusMode};
 hookLearning();
 if (window.aipyLearning && window.aipyLearning.ready) hookLearning();
 document.addEventListener('aipy:learning-ready', hookLearning);
 document.addEventListener('aipy:account', (event) => {
  onAccount(event.detail);
  requestAnimationFrame(() => setStatus(statusMode));
 });
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.addEventListener('pagehide', () => { try { flush(); } catch {} });
 window.addEventListener('online', () => {
  if (user && (statusMode === 'error' || statusMode === 'pending')) flush();
 });
 setStatus(user ? 'pending' : 'local');
}

if (!document.getElementById('account')) {
 console.info('[sync] 계정 영역이 없는 페이지입니다.');
} else if (!ready) {
 console.info('[sync] Firebase 설정이 없어 로컬 기록만 사용합니다.');
} else {
 start();
}

