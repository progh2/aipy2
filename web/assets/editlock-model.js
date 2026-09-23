/* 기기 간 편집 잠금(editLocks) 순수 헬퍼. Firebase 없이 신선도·소유권·필드 모양만 다룹니다.
   한 학생이 두 기기에서 동시에 코드 편집기를 열면 sync.js의 코드 충돌 대화상자가 뜨는 것을
   막기 위해, 한 번에 한 기기만 편집을 허용한다. 잠금은 학습을 막지 않는 보조 장치이므로
   신선도(beat)가 끊기면 자동으로 풀린다.
   #121: deviceId(localStorage, 브라우저당 하나)만으로는 같은 브라우저의 두 탭을 구분하지
   못해 서로 "내 잠금"으로 여긴다. 탭마다 sessionStorage에 tabId를 두고, 잠금 문서의
   deviceId 필드에는 `기기id:탭id` 조합을 쓴다(규칙의 deviceId ≤64자 제한은 그대로 지킨다). */

// 잠금 신선도 기준. 이 시간 동안 beat 갱신이 없으면 잠금이 만료된 것으로 본다.
export const LOCK_FRESH_MS = 120000;
// 내 잠금을 유지하기 위해 beat를 다시 쓰는 주기.
export const HEARTBEAT_MS = 30000;

export const LOCK_NOTE = '다른 기기에서 편집하려면 여기서 [이 기기에서 편집하기]를 눌러야 코드 충돌 창이 뜨지 않아요.';

// 브라우저 User-Agent에서 사람이 읽을 "OS · 브라우저" 라벨을 뽑는다. 실패해도 빈 문자열 대신
// 무난한 기본값을 돌려준다(라벨은 안내용일 뿐 판단 로직에 쓰이지 않는다).
export function deviceLabel(userAgent) {
 const ua = String(userAgent || '');
 let os = '기기';
 if (/Windows/i.test(ua)) os = 'Windows';
 else if (/Mac OS X|Macintosh/i.test(ua)) os = 'Mac';
 else if (/Android/i.test(ua)) os = 'Android';
 else if (/iPhone|iPad|iPod/i.test(ua)) os = 'iOS';
 else if (/CrOS/i.test(ua)) os = 'ChromeOS';
 else if (/Linux/i.test(ua)) os = 'Linux';
 let browser = '브라우저';
 if (/Edg\//i.test(ua)) browser = 'Edge';
 else if (/OPR\/|Opera/i.test(ua)) browser = 'Opera';
 else if (/Whale/i.test(ua)) browser = 'Whale';
 else if (/Chrome\//i.test(ua)) browser = 'Chrome';
 else if (/Firefox\//i.test(ua)) browser = 'Firefox';
 else if (/Safari\//i.test(ua)) browser = 'Safari';
 return `${os} · ${browser}`.slice(0, 60);
}

// beat가 now 기준 LOCK_FRESH_MS 안에 있으면 신선(살아 있는 잠금)하다.
export function isFresh(lock, now) {
 if (!lock || typeof lock !== 'object') return false;
 const beat = Number(lock.beat);
 if (!Number.isFinite(beat)) return false;
 return now - beat < LOCK_FRESH_MS && now - beat >= -LOCK_FRESH_MS;
}

// 다른 탭(다른 기기 포함)이 신선한 잠금을 쥐고 있으면 true. deviceId는 `기기id:탭id` 조합.
// 잠금이 없거나, 만료됐거나, 내 탭이면 false.
export function heldByOther(lock, deviceId, now) {
 if (!lock || !isFresh(lock, now)) return false;
 return lock.deviceId !== deviceId;
}

// `기기id:탭id` 조합에서 기기id만 뗀다.
export function deviceIdOf(combined) {
 const s = String(combined || '');
 const i = s.indexOf(':');
 return i === -1 ? s : s.slice(0, i);
}

// 두 조합 id가 같은 기기(탭만 다름)인지.
export function sameDevice(a, b) {
 const da = deviceIdOf(a), db = deviceIdOf(b);
 return Boolean(da) && da === db;
}

// 잠금을 쥔 쪽을 사람이 읽을 문구로. 같은 기기의 다른 탭이면 "이 컴퓨터의 다른 탭",
// 아니면 "다른 기기(라벨)"(라벨이 없으면 "다른 기기").
export function lockOwnerLabel(lock, myDeviceId) {
 if (!lock) return '다른 기기';
 if (sameDevice(lock.deviceId, myDeviceId)) return '이 컴퓨터의 다른 탭';
 return lock.label ? `다른 기기(${lock.label})` : '다른 기기';
}

// setDoc에 그대로 넣을 필드(서버 타임스탬프는 호출부에서 덧붙인다).
export function lockFields({profile, deviceId, label, now} = {}) {
 const person = profile && typeof profile === 'object' ? profile : {};
 return {
  uid: person.uid || '',
  email: person.email || '',
  deviceId: String(deviceId || '').slice(0, 64),
  label: String(label || '').slice(0, 60),
  beat: Number.isFinite(Number(now)) ? Number(now) : Date.now()
 };
}

// localStorage에 저장할 새 기기 ID. rand는 테스트에서 주입할 수 있다.
export function newDeviceId(rand = Math.random) {
 const part = () => Math.floor(rand() * 0xffffffff).toString(36);
 return `dev-${part()}${part()}`;
}

// sessionStorage에 저장할 새 탭 ID(탭을 닫으면 사라지고, 새로고침에는 남는다).
export function newTabId(rand = Math.random) {
 const part = () => Math.floor(rand() * 0xffffffff).toString(36);
 return `tab-${part()}${part()}`;
}

// 잠금 문서에 쓸 조합 id. 규칙의 deviceId.size() <= 64를 지키도록 자른다.
export function combineDeviceId(deviceId, tabId) {
 return `${deviceId || ''}:${tabId || ''}`.slice(0, 64);
}
