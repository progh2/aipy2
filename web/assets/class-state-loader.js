/* 반 전체 학생의 students/{uid}/state/current를 한 번에 읽는 작은 로더(#145-B, achievement 전용).
   #145-A가 만들 답변 내역용 class-state-loader.js와 역할이 같아질 수 있어, 시그니처를 최대한
   단순하게 맞춰 뒀다: loadClassStates({db, store, students, concurrency}) → Map uid→state.
   나중에 한 파일로 합칠 때 이 함수만 import 경로를 바꾸면 되도록, Firebase 객체(db/store)를
   인자로 받고 내부에서 import하지 않는다(teacher-answers.js의 ensureStudentState()와 같은 전제:
   읽기 실패·미존재는 null로 남기고 다시 던지지 않는다). */

// students: [{uid, ...}] — uid가 없는 항목은 건너뛴다. concurrency는 한 번에 진행할 getDoc 수.
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
