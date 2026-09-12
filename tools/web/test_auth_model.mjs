/* 로그인 유지·계정 선택·권한 거부 구분 검사. node tools/web/test_auth_model.mjs */
import {
 userEmail, isSchoolEmail, shouldSignOutForeignAccount, googleCustomParameters,
 markChooserNext, consumeChooserFlag, isPermissionDenied, needsReauth,
 teacherAccessMessage, teacherPickerEmpty, dataFailureNote,
 AUTH_CHOOSER_KEY, SIGNED_OUT_GATE, PERMISSION_GATE, PERMISSION_ACTION
} from '../../web/assets/auth-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(userEmail({email: 'A@E-Mirim.hs.kr'}), 'a@e-mirim.hs.kr', 'userEmail direct');
eq(userEmail({email: '', providerData: [{email: '20314@e-mirim.hs.kr'}]}), '20314@e-mirim.hs.kr', 'userEmail provider');
eq(userEmail({uid: 'x'}), '', 'userEmail empty');
eq(isSchoolEmail('teacher@e-mirim.hs.kr', 'e-mirim.hs.kr'), true, 'school email');
eq(isSchoolEmail('someone@gmail.com', 'e-mirim.hs.kr'), false, 'personal email');

eq(shouldSignOutForeignAccount({email: 'me@gmail.com'}, 'e-mirim.hs.kr'), true, 'sign out personal');
eq(shouldSignOutForeignAccount({email: 't@e-mirim.hs.kr'}, 'e-mirim.hs.kr'), false, 'keep school');
eq(shouldSignOutForeignAccount({uid: 'restore'}, 'e-mirim.hs.kr'), false, 'empty email not foreign');
eq(shouldSignOutForeignAccount(null, 'e-mirim.hs.kr'), false, 'null user');

eq(googleCustomParameters('e-mirim.hs.kr'), {hd: 'e-mirim.hs.kr'}, 'no chooser by default');
eq(googleCustomParameters('e-mirim.hs.kr', {forceChooser: true}), {
 hd: 'e-mirim.hs.kr',
 prompt: 'select_account'
}, 'chooser after logout');

const store = new Map();
const storage = {
 getItem: (key) => (store.has(key) ? store.get(key) : null),
 setItem: (key, value) => store.set(key, value),
 removeItem: (key) => store.delete(key)
};
markChooserNext(storage);
eq(store.get(AUTH_CHOOSER_KEY), '1', 'mark chooser');
eq(consumeChooserFlag(storage), true, 'consume chooser');
eq(consumeChooserFlag(storage), false, 'chooser once');

eq(isPermissionDenied({code: 'permission-denied'}), true, 'firestore denied');
eq(isPermissionDenied({message: 'PERMISSION_DENIED: missing'}), true, 'denied message');
eq(isPermissionDenied({code: 'unavailable'}), false, 'network not denied');
eq(needsReauth({code: 'auth/user-token-expired'}), true, 'expired token');
eq(needsReauth({code: 'permission-denied'}), false, 'denied is not auth loss');

eq(teacherAccessMessage({user: null}).kind, 'signed-out', 'gate signed out');
eq(teacherAccessMessage({user: null}).text, SIGNED_OUT_GATE, 'gate asks login only when signed out');
eq(teacherAccessMessage({user: {email: 't@e-mirim.hs.kr'}, error: {code: 'permission-denied'}}).kind, 'permission', 'gate permission');
eq(teacherAccessMessage({user: {email: 't@e-mirim.hs.kr'}, error: {code: 'permission-denied'}}).text, PERMISSION_GATE, 'gate keeps session');
eq(teacherAccessMessage({user: {email: 't@e-mirim.hs.kr'}, error: {code: 'auth/user-token-expired'}}).kind, 'signed-out', 'gate reauth');
eq(teacherAccessMessage({user: {email: 't@e-mirim.hs.kr'}, teacher: false}).kind, 'not-teacher', 'gate not teacher');
eq(teacherAccessMessage({user: {email: 't@e-mirim.hs.kr'}, teacher: true}).kind, 'ok', 'gate ok');
eq(teacherAccessMessage({ready: false}).kind, 'config', 'gate config');

eq(teacherPickerEmpty({user: null}), '로그인하면 반을 선택할 수 있습니다', 'picker signed out');
eq(teacherPickerEmpty({user: {}, error: {code: 'permission-denied'}}).includes('다시 로그인'), false, 'picker no relogin');
eq(dataFailureNote({code: 'permission-denied'}), PERMISSION_ACTION, 'action denied');
eq(dataFailureNote({code: 'auth/invalid-user-token'}), SIGNED_OUT_GATE, 'action reauth');

console.log('PASS auth-model');
