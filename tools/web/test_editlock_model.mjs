/* 기기 간 편집 잠금 순수 함수 검사. node tools/web/test_editlock_model.mjs */
import {
 LOCK_FRESH_MS, HEARTBEAT_MS, LOCK_NOTE, deviceLabel, isFresh, heldByOther, lockFields, newDeviceId
} from '../../web/assets/editlock-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(LOCK_FRESH_MS, 120000, 'fresh window');
eq(HEARTBEAT_MS, 30000, 'heartbeat interval');
eq(typeof LOCK_NOTE === 'string' && LOCK_NOTE.length > 0, true, 'lock note text');

eq(deviceLabel('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36'), 'Windows · Chrome', 'windows chrome');
eq(deviceLabel('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15'), 'Mac · Safari', 'mac safari');
eq(deviceLabel('Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/128.0'), 'Android · Chrome', 'android chrome');
eq(deviceLabel(''), '기기 · 브라우저', 'unknown ua fallback');
eq(deviceLabel('x'.repeat(200)), '기기 · 브라우저'.slice(0, 60), 'label length capped');

const now = 1000000;
eq(isFresh(null, now), false, 'null lock not fresh');
eq(isFresh({beat: now - 1000}, now), true, 'recent beat fresh');
eq(isFresh({beat: now - (LOCK_FRESH_MS + 1)}, now), false, 'old beat stale');
eq(isFresh({beat: 'abc'}, now), false, 'non-numeric beat not fresh');

eq(heldByOther({beat: now - 1000, deviceId: 'dev-a'}, 'dev-b', now), true, 'other fresh device holds');
eq(heldByOther({beat: now - 1000, deviceId: 'dev-a'}, 'dev-a', now), false, 'own device does not hold');
eq(heldByOther({beat: now - (LOCK_FRESH_MS + 1), deviceId: 'dev-a'}, 'dev-b', now), false, 'stale lock not held');
eq(heldByOther(null, 'dev-b', now), false, 'no lock not held');

const fields = lockFields({
 profile: {uid: 'u1', email: 's1@e-mirim.hs.kr'},
 deviceId: 'dev-a'.padEnd(80, 'x'),
 label: 'x'.repeat(80),
 now
});
eq(fields.uid, 'u1', 'lock fields uid');
eq(fields.email, 's1@e-mirim.hs.kr', 'lock fields email');
eq(fields.deviceId.length, 64, 'deviceId clamped to 64');
eq(fields.label.length, 60, 'label clamped to 60');
eq(fields.beat, now, 'lock fields beat');
eq(Object.keys(fields).sort(), ['beat', 'deviceId', 'email', 'label', 'uid'], 'lock field keys match rules payload');

eq(lockFields({}).beat > 0, true, 'lockFields defaults now to Date.now()');

const id1 = newDeviceId(() => 0.123456);
const id2 = newDeviceId(() => 0.654321);
eq(id1.startsWith('dev-'), true, 'device id prefix');
eq(id1 !== id2, true, 'device ids differ with different rand');
eq(newDeviceId(() => 0.5) === newDeviceId(() => 0.5), true, 'device id deterministic for same rand');

console.log('editlock model OK');
