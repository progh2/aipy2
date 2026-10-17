/* 반 전체 학생의 students/{uid}/state/current를 한 번에 조회하는 공용 로더(#145 A/B 공유).
   Firestore 접근 자체는 호출 쪽이 넘기는 fetchOne(uid)에 맡기고(answers.html도 achievement.html도
   자기 db/store 인스턴스를 쓰므로 여기서 import하지 않는다), 이 모듈은 동시성 제한과 진행률
   콜백만 담당하는 얇은 오케스트레이션이다. Firebase 전용 타입에 의존하지 않아 테스트가 쉽다.

   export:
   - DEFAULT_CONCURRENCY: number
   - loadStatesForUids(uids, fetchOne, {concurrency, onProgress}) -> Promise<Map<uid, Entry>>
     Entry는 {status:'ready', data} | {status:'empty'} | {status:'error', error} 중 하나.
     fetchOne(uid)이 던지는 값은 Firestore DocumentSnapshot(또는 exists/data를 가진 비슷한 객체)이거나
     그냥 일반 객체({exists:boolean, data:object})여도 된다 — exists가 함수면 호출하고, 아니면 값으로 본다.
   - snapshotToEntry(snap) -> Entry  (낱개 변환이 필요할 때 재사용) */

export const DEFAULT_CONCURRENCY = 5;

export function snapshotToEntry(snap) {
 if (!snap) return {status: 'empty'};
 const exists = typeof snap.exists === 'function' ? snap.exists() : Boolean(snap.exists);
 if (!exists) return {status: 'empty'};
 const data = typeof snap.data === 'function' ? snap.data() : snap.data;
 return {status: 'ready', data: data || {}};
}

// uids 순서대로 fetchOne을 호출하되, 동시에 최대 concurrency개까지만 진행한다.
// onProgress({done, total, uid})는 각 학생 조회가 끝날 때마다(성공/실패 모두) 호출된다.
export async function loadStatesForUids(uids, fetchOne, {concurrency = DEFAULT_CONCURRENCY, onProgress} = {}) {
 const list = (uids || []).filter(Boolean);
 const result = new Map();
 if (!list.length) return result;
 let nextIndex = 0;
 let doneCount = 0;
 const limit = Math.max(1, Math.min(Number(concurrency) || DEFAULT_CONCURRENCY, list.length));

 async function worker() {
  while (nextIndex < list.length) {
   const i = nextIndex;
   nextIndex += 1;
   const uid = list[i];
   let entry;
   try {
    const snap = await fetchOne(uid);
    entry = snapshotToEntry(snap);
   } catch (error) {
    entry = {status: 'error', error};
   }
   result.set(uid, entry);
   doneCount += 1;
   if (onProgress) onProgress({done: doneCount, total: list.length, uid, entry});
  }
 }

 await Promise.all(Array.from({length: limit}, worker));
 return result;
}

// --- (#145-B) 성취수준 화면용 단순 시그니처. 위 loadStatesForUids와 같은 일을 db/store를 받아 수행한다.
export async function loadClassStates({db, store, students, concurrency = 5, onProgress} = {}) {
 const results = new Map();
 const list = Array.isArray(students) ? students.filter((s) => s && s.uid) : [];
 if (!db || !store || !list.length) return results;
 let cursor = 0;
 let done = 0;
 const report = () => { if (typeof onProgress === 'function') onProgress(done, list.length); };
 report();
 async function worker() {
  while (cursor < list.length) {
   const i = cursor;
   cursor += 1;
   const uid = list[i].uid;
   try {
    const snap = await store.getDoc(store.doc(db, 'students', uid, 'state', 'current'));
    results.set(uid, snap.exists() ? snap.data() : null);
   } catch (error) {
    console.error('[class-state-loader]', uid, error);
    results.set(uid, null);
   }
   done += 1;
   report();
  }
 }
 const workerCount = Math.max(1, Math.min(Number(concurrency) || 5, list.length));
 await Promise.all(Array.from({length: workerCount}, () => worker()));
 return results;
}
