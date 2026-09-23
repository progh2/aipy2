/* 기기 간 편집 잠금 순수 함수 검사. node tools/web/test_editlock_model.mjs */
import {
 LOCK_FRESH_MS, HEARTBEAT_MS, LOCK_NOTE, deviceLabel, isFresh, heldByOther, lockFields, newDeviceId,
 newTabId, combineDeviceId, deviceIdOf, sameDevice, lockOwnerLabel
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

// #121 같은 기기의 두 탭 구분
const tab1 = newTabId(() => 0.111111);
const tab2 = newTabId(() => 0.222222);
eq(tab1.startsWith('tab-'), true, 'tab id prefix');
eq(tab1 !== tab2, true, 'tab ids differ with different rand');

const deviceA = 'dev-aaaaaaaaaaaaaaaa';
const combined1 = combineDeviceId(deviceA, tab1);
const combined2 = combineDeviceId(deviceA, tab2);
eq(combined1, `${deviceA}:${tab1}`, 'combine device+tab id');
eq(combined1.length <= 64, true, 'combined id fits rule length limit');
eq(deviceIdOf(combined1), deviceA, 'deviceIdOf strips tab suffix');
eq(deviceIdOf('no-colon-here'), 'no-colon-here', 'deviceIdOf handles plain id');
eq(sameDevice(combined1, combined2), true, 'same device, different tab');
eq(sameDevice(combined1, combineDeviceId('dev-bbbbbbbbbbbbbbbb', tab1)), false, 'different device, same tab id never happens but still compared correctly');
eq(sameDevice('', combined1), false, 'empty id is never the same device');

// 두 탭이 같은 기기라도 heldByOther는 조합 id 전체로 비교하므로 서로를 "다른 쪽"으로 본다.
const now2 = 2_000_000;
eq(heldByOther({beat: now2 - 1000, deviceId: combined1}, combined2, now2), true, 'other tab of same device still counts as holding the lock');
eq(heldByOther({beat: now2 - 1000, deviceId: combined1}, combined1, now2), false, 'same tab (e.g. after reload) is not held by other');

eq(lockOwnerLabel(null, combined1), '다른 기기', 'no lock label fallback');
eq(lockOwnerLabel({deviceId: combined2, label: 'Windows · Chrome'}, combined1), '이 컴퓨터의 다른 탭', 'same device shows tab label regardless of stored label');
eq(lockOwnerLabel({deviceId: combineDeviceId('dev-bbbbbbbbbbbbbbbb', tab1), label: 'Mac · Safari'}, combined1), '다른 기기(Mac · Safari)', 'different device shows its label');
eq(lockOwnerLabel({deviceId: combineDeviceId('dev-bbbbbbbbbbbbbbbb', tab1), label: ''}, combined1), '다른 기기', 'different device without label falls back');

console.log('editlock model OK');
