/* 로그인 유지·계정 선택·권한 거부를 구분하는 순수 함수.
   Auth 세션이 풀린 것과 Firestore permission-denied를 같은 “다시 로그인”으로 보지 않습니다. */

export const AUTH_CHOOSER_KEY = 'aipy-auth-chooser';

export const SIGNED_OUT_GATE = '헤더의 “학교 계정으로 로그인”으로 먼저 로그인하세요.';
export const PERMISSION_GATE = '로그인은 유지되어 있습니다. 데이터 권한이 없어 이 화면을 열지 못했습니다. 다시 로그인할 필요는 없습니다.';
export const NETWORK_GATE = '권한을 확인하지 못했습니다. 네트워크를 확인하고 새로고침하세요.';
export const NOT_TEACHER_GATE = '이 계정에는 교사 권한이 없습니다.';
export const CONFIG_GATE = '로그인 설정이 없어 이 화면을 열 수 없습니다.';
export const PERMISSION_ACTION = '로그인은 되어 있습니다. 권한이 없어 이 작업을 하지 못했습니다. 다시 로그인할 필요는 없습니다.';
export const PICKER_SIGNED_OUT = '로그인하면 반을 선택할 수 있습니다';
export const PICKER_PERMISSION = '로그인은 되어 있습니다. 권한을 확인하지 못했습니다';

const REAUTH_CODES = new Set([
 'auth/user-token-expired',
 'auth/invalid-user-token',
 'auth/requires-recent-login',
 'auth/user-disabled'
]);

export function userEmail(user) {
 if (!user) return '';
 const direct = String(user.email || '').trim().toLowerCase();
 if (direct) return direct;
 const providers = Array.isArray(user.providerData) ? user.providerData : [];
 for (const item of providers) {
  const email = String((item && item.email) || '').trim().toLowerCase();
  if (email) return email;
 }
 return '';
}

export function isSchoolEmail(email, domain) {
 const value = String(email || '').trim().toLowerCase();
 const host = String(domain || '').trim().toLowerCase();
 return Boolean(value && host && value.endsWith(`@${host}`));
}

// 이메일이 아직 비어 있으면 개인 계정으로 단정하지 않습니다. 복원 중에 강제 로그아웃하면
// 다음 페이지 이동마다 다시 로그인하게 됩니다.
export function shouldSignOutForeignAccount(user, domain) {
 const email = userEmail(user);
 if (!email) return false;
 return !isSchoolEmail(email, domain);
}

export function googleCustomParameters(domain, {forceChooser = false} = {}) {
 const params = {hd: domain};
 // 일반 로그인에는 prompt를 넣지 않습니다. select_account는 “다른 계정”을
 // 눌렀거나, 방금 개인 계정을 걸러 낸 뒤에만 씁니다.
 if (forceChooser) params.prompt = 'select_account';
 return params;
}

export function shouldWriteStudentProfile(rosterReadOk) {
 return rosterReadOk === true;
}

export function missingRosterWarning({classroom, teacher = false, rosterReadOk = true} = {}) {
 if (teacher || !rosterReadOk || classroom) return '';
 return '명단에 없는 계정입니다. 선생님께 알려 주세요.';
}

export function markChooserNext(storage) {
 if (!storage || typeof storage.setItem !== 'function') return;
 try { storage.setItem(AUTH_CHOOSER_KEY, '1'); } catch {}
}

export function consumeChooserFlag(storage) {
 if (!storage || typeof storage.getItem !== 'function') return false;
 try {
  const value = storage.getItem(AUTH_CHOOSER_KEY);
  if (value) storage.removeItem(AUTH_CHOOSER_KEY);
  return value === '1';
 } catch {
  return false;
 }
}

export function isPermissionDenied(error) {
 if (!error) return false;
 const code = String(error.code || '');
 const message = String(error.message || '');
 return code === 'permission-denied'
  || code === 'firestore/permission-denied'
  || /permission[-_ ]denied/i.test(code)
  || /permission[-_ ]denied/i.test(message);
}

export function needsReauth(error) {
 const code = String((error && error.code) || '');
 return REAUTH_CODES.has(code);
}

export function teacherAccessMessage({ready = true, user = null, teacher = false, error = null} = {}) {
 if (!ready) return {kind: 'config', text: CONFIG_GATE};
 if (!user) return {kind: 'signed-out', text: SIGNED_OUT_GATE};
 if (needsReauth(error)) return {kind: 'signed-out', text: SIGNED_OUT_GATE};
 if (isPermissionDenied(error)) return {kind: 'permission', text: PERMISSION_GATE};
 if (error) return {kind: 'network', text: NETWORK_GATE};
 if (!teacher) return {kind: 'not-teacher', text: NOT_TEACHER_GATE};
 return {kind: 'ok', text: ''};
}

export function teacherPickerEmpty({ready = true, user = null, teacher = false, error = null} = {}) {
 if (!ready) return '로그인 설정이 없어 반을 고를 수 없습니다';
 if (!user) return PICKER_SIGNED_OUT;
 if (needsReauth(error)) return PICKER_SIGNED_OUT;
 if (isPermissionDenied(error) || error) return PICKER_PERMISSION;
 if (!teacher) return '교사 권한이 확인되면 반을 고를 수 있습니다';
 return '명단에 등록된 반이 없습니다';
}

export function dataFailureNote(error, fallback) {
 if (needsReauth(error)) return SIGNED_OUT_GATE;
 if (isPermissionDenied(error)) return PERMISSION_ACTION;
 return fallback || `처리하지 못했습니다. (${(error && (error.code || error.message)) || error || ''})`;
}
