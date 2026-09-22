/* 기기 간 편집 잠금(editLocks) 순수 헬퍼. Firebase 없이 신선도·소유권·필드 모양만 다룹니다.
   한 학생이 두 기기에서 동시에 코드 편집기를 열면 sync.js의 코드 충돌 대화상자가 뜨는 것을
   막기 위해, 한 번에 한 기기만 편집을 허용한다. 잠금은 학습을 막지 않는 보조 장치이므로
   신선도(beat)가 끊기면 자동으로 풀린다. */

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

// 다른 기기가 신선한 잠금을 쥐고 있으면 true. 잠금이 없거나, 만료됐거나, 내 기기면 false.
export function heldByOther(lock, deviceId, now) {
 if (!lock || !isFresh(lock, now)) return false;
 return lock.deviceId !== deviceId;
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
