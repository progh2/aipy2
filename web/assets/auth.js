/* 학교 Google 계정 로그인. 정적 호스팅(GitHub Pages)에서 그대로 동작하며,
   학교 도메인 확인과 반·번호 위조 방지는 Firestore 규칙이 최종 판단합니다.
   설정이 비어 있으면 아무 UI도 만들지 않고 조용히 종료합니다. */
import {firebaseConfig, SCHOOL_DOMAIN, SDK, ready} from './firebase-config.js';

const slot = document.getElementById('account');
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};
let toastTimer;
function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text;
 clearTimeout(toastTimer);
 toastTimer = setTimeout(() => { box.textContent = ''; }, 6000);
}

export const SCHOOL = SCHOOL_DOMAIN;

let fb = null;
export async function load() {
 if (fb) return fb;
 const [app, authMod, store] = await Promise.all([
  import(`${SDK}/firebase-app.js`),
  import(`${SDK}/firebase-auth.js`),
  import(`${SDK}/firebase-firestore.js`)
 ]);
 const instance = app.initializeApp(firebaseConfig);
 fb = {authMod, store, auth: authMod.getAuth(instance), db: store.getFirestore(instance)};
 return fb;
}

function publish(user, profile) {
 window.aipyAccount = {user, profile, signIn, signOut};
 document.body.dataset.account = user ? 'signed-in' : 'signed-out';
 // 학습 기록 동기화는 이 이벤트를 듣고 붙입니다.
 document.dispatchEvent(new CustomEvent('aipy:account', {detail: {user, profile}}));
}

function renderSignedOut() {
 const button = node('button', 'account-signin', `학교 계정으로 로그인`);
 button.type = 'button';
 button.addEventListener('click', signIn);
 const note = node('span', 'account-note', `@${SCHOOL_DOMAIN} 계정만 사용합니다.`);
 slot.replaceChildren(button, note);
}

function renderBusy(text) {
 slot.replaceChildren(node('span', 'account-note', text));
}

// 학번과 이름을 함께 보여 주고, 학년·반은 아래 줄에 둡니다.
export function describe(profile) {
 const identity = [profile.studentId, profile.name].filter(Boolean).join(' ');
 const place = profile.classroom ? `${profile.grade}학년 ${profile.classroom}반` : '';
 return {identity: identity || profile.email, place};
}

function renderSignedIn(profile) {
 const chip = node('span', 'account-chip');
 const {identity, place} = describe(profile);
 chip.append(node('b', '', identity), node('small', '', place || profile.email));
 const out = node('button', 'account-signout', '로그아웃');
 out.type = 'button';
 out.addEventListener('click', signOut);
 slot.replaceChildren(chip, out);
 if (!profile.classroom) {
  slot.append(node('span', 'account-warn', '명단에 없는 계정입니다. 선생님께 알려 주세요.'));
 }
}

async function start() {
 renderBusy('로그인 상태를 확인합니다…');
 try {
  const {auth, authMod} = await load();
  await authMod.setPersistence(auth, authMod.browserLocalPersistence).catch(() => {});
  authMod.onAuthStateChanged(auth, handleUser);
 } catch (error) {
  console.error('[auth]', error);
  renderBusy('로그인 기능을 불러오지 못했습니다. 네트워크를 확인하세요.');
 }
}

async function signIn() {
 renderBusy('로그인 창을 확인하세요…');
 try {
  const {auth, authMod} = await load();
  const provider = new authMod.GoogleAuthProvider();
  // hd는 학교 계정을 먼저 보여 주는 힌트일 뿐이며, 실제 차단은 규칙이 담당합니다.
  provider.setCustomParameters({hd: SCHOOL_DOMAIN, prompt: 'select_account'});
  await authMod.signInWithPopup(auth, provider);
 } catch (error) {
  const code = error && error.code;
  if (code === 'auth/popup-closed-by-user' || code === 'auth/cancelled-popup-request') {
   renderSignedOut();
   return;
  }
  const messages = {
   'auth/popup-blocked': '브라우저가 팝업을 막았습니다. 주소창의 팝업 허용을 켜고 다시 시도하세요.',
   'auth/unauthorized-domain': '이 주소가 Firebase 승인된 도메인에 없습니다. 선생님께 알려 주세요.',
   'auth/network-request-failed': '네트워크에 연결되지 않았습니다. 연결을 확인하고 다시 시도하세요.',
   'auth/operation-not-allowed': 'Google 로그인이 아직 사용 설정되지 않았습니다. 선생님께 알려 주세요.',
   'auth/configuration-not-found': 'Firebase 로그인 설정이 아직 완료되지 않았습니다. 선생님께 알려 주세요.',
   'auth/admin-restricted-operation': '이 계정은 로그인이 허용되지 않았습니다. 선생님께 알려 주세요.'
  };
  console.error('[auth]', error);
  toast(messages[code] || `로그인에 실패했습니다. (${code || error})`);
  renderSignedOut();
 }
}

function askClearLocalOnLogout() {
 return new Promise((resolve) => {
  const existing = document.getElementById('logout-clear-overlay');
  if (existing) existing.remove();
  const overlay = node('div', 'sync-overlay');
  overlay.id = 'logout-clear-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'logout-clear-title');
  const box = node('div', 'sync-dialog');
  box.append(node('h2', '', '로그아웃'));
  const title = node('p', '', '이 브라우저의 학습 기록을 지울까요? 계정에 저장한 기록은 그대로 남아요.');
  title.id = 'logout-clear-title';
  box.append(title);
  const actions = node('div', 'actions');
  const clearBtn = node('button', 'primary', '이 컴퓨터 기록만 지우기');
  const keepBtn = node('button', '', '기록 남기고 로그아웃');
  const cancelBtn = node('button', '', '취소');
  clearBtn.type = 'button';
  keepBtn.type = 'button';
  cancelBtn.type = 'button';
  const finish = (value) => { overlay.remove(); resolve(value); };
  clearBtn.onclick = () => finish('clear');
  keepBtn.onclick = () => finish('keep');
  cancelBtn.onclick = () => finish('abort');
  overlay.addEventListener('click', (event) => { if (event.target === overlay) finish('abort'); });
  actions.append(clearBtn, keepBtn, cancelBtn);
  box.append(actions);
  overlay.append(box);
  document.body.append(overlay);
  clearBtn.focus();
 });
}

async function finishSignOut(clearLocal) {
 try {
  if (window.aipySync && typeof window.aipySync.flush === 'function') await window.aipySync.flush();
 } catch (error) {
  console.warn('[auth] 로그아웃 전 동기화 실패', error);
 }
 const {auth, authMod} = await load();
 await authMod.signOut(auth);
 if (clearLocal) {
  const key = (window.aipyLearning && window.aipyLearning.key) || 'aipy-lab-v1';
  try { localStorage.removeItem(key); } catch {}
  toast('로그아웃했습니다. 이 브라우저의 학습 기록은 지웠습니다.');
  location.reload();
  return;
 }
 toast('로그아웃했습니다. 이 브라우저의 학습 기록은 그대로 남아 있습니다.');
}

async function signOut() {
 // 학교/브라우저가 네이티브 확인창을 막거나 즉시 거절하는 경우가 있어 화면 안 모달을 씁니다.
 const choice = await askClearLocalOnLogout();
 if (choice === 'abort') return;
 await finishSignOut(choice === 'clear');
}

async function handleUser(user) {
 if (!user) {
  publish(null, null);
  renderSignedOut();
  return;
 }
 const email = (user.email || '').toLowerCase();
 if (!email.endsWith(`@${SCHOOL_DOMAIN}`)) {
  // 규칙에서도 막히지만, 안내는 여기서 먼저 합니다.
  const {auth, authMod} = await load();
  await authMod.signOut(auth);
  toast(`학교 계정(@${SCHOOL_DOMAIN})으로 로그인하세요. 개인 계정은 사용할 수 없습니다.`);
  return;
 }
 renderBusy('명단을 확인합니다…');
 const {db, store} = await load();
 let entry = null;
 try {
  const snapshot = await store.getDoc(store.doc(db, 'roster', email));
  if (snapshot.exists()) entry = snapshot.data();
 } catch (error) {
  console.warn('[auth] 명단을 읽지 못했습니다.', error);
 }
 // 명단 값만 사용합니다. 명단에 없으면 학번·학년·반을 비워 둡니다(규칙에서도 그것만 허용).
 const fromRoster = (key) => (entry && entry[key] != null ? entry[key] : null);
 const profile = {
  uid: user.uid,
  email,
  studentId: fromRoster('studentId'),
  // 학번은 입학년도가 다르면 겹칠 수 있으므로 두 값을 함께 보관합니다. 고유 식별자는 이메일입니다.
  admissionYear: fromRoster('admissionYear'),
  name: (entry && entry.name) || user.displayName || email.split('@')[0],
  grade: fromRoster('grade'),
  classroom: fromRoster('classroom'),
  number: fromRoster('number')
 };
 try {
  await store.setDoc(
   store.doc(db, 'students', user.uid),
   {...profile, updatedAt: store.serverTimestamp()},
   {merge: true}
  );
 } catch (error) {
  console.error('[auth] 프로필 저장 실패', error);
  toast('로그인은 되었지만 학습 정보를 저장하지 못했습니다. 선생님께 알려 주세요.');
 }
 publish(user, profile);
 renderSignedIn(profile);
}

// 모든 선언이 평가된 뒤에 시작합니다.
if (!slot) {
 console.info('[auth] 계정 영역이 없는 페이지입니다.');
} else if (!ready) {
 console.info('[auth] web/assets/firebase-config.js가 아직 비어 있어 로그인을 표시하지 않습니다.');
} else {
 start();
}

