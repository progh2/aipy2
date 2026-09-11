/* 학습 기록 동기화(M2) 순수 헬퍼. Firebase 없이 병합·요약·쓰기 억제를 검사합니다.
   화면이 읽는 complete/answers/journals/projects 모양은 그대로 두고,
   항목별 시각은 times 맵에만 둡니다. 문항·주제가 늘어도 키를 나열하지 않습니다.
   understanding은 progress 요약에만 두고, 값 모양은 understanding-model이 맞춥니다. */
import {normalizeUnderstanding} from './understanding-model.js';

export const LEARNING_KEY = 'aipy-lab-v1';
export const CODE_IDLE_MS = 25000;
export const BUCKETS = ['complete', 'answers', 'journals', 'projects'];
export const IMMEDIATE_KINDS = ['complete', 'answer', 'import'];

export function emptyTimes() {
 return {complete: {}, answers: {}, journals: {}, projects: {}, last: 0};
}

export function emptyState() {
 return {version: 1, complete: {}, answers: {}, journals: {}, projects: {}, last: '', times: emptyTimes()};
}

export function asMap(value) {
 return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

export function normalizeState(raw) {
 const state = emptyState();
 if (!raw || typeof raw !== 'object') return state;
 for (const key of BUCKETS) state[key] = {...asMap(raw[key])};
 state.last = typeof raw.last === 'string' ? raw.last : '';
 const times = asMap(raw.times);
 for (const key of BUCKETS) state.times[key] = {...asMap(times[key])};
 const lastTime = Number(times.last);
 state.times.last = Number.isFinite(lastTime) ? lastTime : 0;
 return state;
}

export function cloneState(state) {
 return JSON.parse(JSON.stringify(normalizeState(state)));
}

export function deepEqual(a, b) {
 return JSON.stringify(a) === JSON.stringify(b);
}

export function itemTime(times, bucket, key) {
 const n = Number(times?.[bucket]?.[key]);
 return Number.isFinite(n) ? n : 0;
}

export function shouldFlushNow(kind) {
 return IMMEDIATE_KINDS.includes(kind);
}

export function stampChanged(prev, next, now) {
 const from = normalizeState(prev);
 const to = normalizeState(next);
 to.times = {
  complete: {...from.times.complete},
  answers: {...from.times.answers},
  journals: {...from.times.journals},
  projects: {...from.times.projects},
  last: from.times.last || 0
 };
 for (const bucket of BUCKETS) {
  const keys = new Set([...Object.keys(from[bucket]), ...Object.keys(to[bucket])]);
  for (const key of keys) {
   const had = Object.hasOwn(from[bucket], key);
   const has = Object.hasOwn(to[bucket], key);
   if (!has) {
    delete to.times[bucket][key];
    continue;
   }
   if (!had || !deepEqual(from[bucket][key], to[bucket][key])) to.times[bucket][key] = now;
   else if (!itemTime(to.times, bucket, key)) to.times[bucket][key] = itemTime(from.times, bucket, key) || now;
  }
 }
 if (to.last !== from.last) to.times.last = to.last ? now : 0;
 else if (to.last && !to.times.last) to.times.last = now;
 return to;
}

export function mergeBucket(localMap, cloudMap, localTimes, cloudTimes, bucket, now) {
 const local = asMap(localMap);
 const cloud = asMap(cloudMap);
 const keys = new Set([...Object.keys(local), ...Object.keys(cloud)]);
 const map = {};
 const times = {};
 for (const key of keys) {
  const hasL = Object.hasOwn(local, key);
  const hasC = Object.hasOwn(cloud, key);
  const lt = itemTime(localTimes, bucket, key);
  const ct = itemTime(cloudTimes, bucket, key);
  if (hasL && !hasC) {
   map[key] = local[key];
   times[key] = lt || now;
  } else if (!hasL && hasC) {
   map[key] = cloud[key];
   times[key] = ct;
  } else if (deepEqual(local[key], cloud[key])) {
   map[key] = local[key];
   times[key] = Math.max(lt, ct);
  } else if (lt >= ct) {
   map[key] = local[key];
   times[key] = lt || now;
  } else {
   map[key] = cloud[key];
   times[key] = ct;
  }
 }
 return {map, times};
}

export function projectNeedsChoice(localValue, cloudValue, localTime, cloudTime) {
 if (deepEqual(localValue, cloudValue)) return false;
 // 시각이 한쪽만 있으면 그쪽으로 정합니다. 둘 다 있거나 둘 다 없으면 학생에게 묻습니다.
 return localTime === cloudTime || (localTime > 0 && cloudTime > 0);
}

export function mergeProjects(localProjects, cloudProjects, localTimes, cloudTimes, choices, now) {
 const local = asMap(localProjects);
 const cloud = asMap(cloudProjects);
 const keys = new Set([...Object.keys(local), ...Object.keys(cloud)]);
 const map = {};
 const times = {};
 const unresolved = [];
 for (const key of keys) {
  const hasL = Object.hasOwn(local, key);
  const hasC = Object.hasOwn(cloud, key);
  const lt = itemTime(localTimes, 'projects', key);
  const ct = itemTime(cloudTimes, 'projects', key);
  if (hasL && !hasC) {
   map[key] = local[key];
   times[key] = lt || now;
   continue;
  }
  if (!hasL && hasC) {
   map[key] = cloud[key];
   times[key] = ct;
   continue;
  }
  if (deepEqual(local[key], cloud[key])) {
   map[key] = local[key];
   times[key] = Math.max(lt, ct);
   continue;
  }
  const choice = choices && choices[key];
  if (choice === 'local') {
   map[key] = local[key];
   times[key] = Math.max(lt, now);
  } else if (choice === 'cloud') {
   map[key] = cloud[key];
   times[key] = Math.max(ct, now);
  } else if (projectNeedsChoice(local[key], cloud[key], lt, ct)) {
   unresolved.push({id: key, local: local[key], cloud: cloud[key], localTime: lt, cloudTime: ct});
   map[key] = local[key];
   times[key] = lt || now;
  } else if (lt >= ct) {
   map[key] = local[key];
   times[key] = lt || now;
  } else {
   map[key] = cloud[key];
   times[key] = ct;
  }
 }
 return {map, times, unresolved};
}

export function mergeStates(localRaw, cloudRaw, choices, now) {
 const local = normalizeState(localRaw);
 const cloud = normalizeState(cloudRaw);
 const complete = mergeBucket(local.complete, cloud.complete, local.times, cloud.times, 'complete', now);
 const answers = mergeBucket(local.answers, cloud.answers, local.times, cloud.times, 'answers', now);
 const journals = mergeBucket(local.journals, cloud.journals, local.times, cloud.times, 'journals', now);
 const projects = mergeProjects(local.projects, cloud.projects, local.times, cloud.times, choices, now);
 let last = local.last;
 let lastTime = local.times.last || 0;
 if (cloud.last && cloud.times.last > lastTime) {
  last = cloud.last;
  lastTime = cloud.times.last;
 } else if (local.last && !lastTime) lastTime = now;
 return {
  state: {
   version: 1,
   complete: complete.map,
   answers: answers.map,
   journals: journals.map,
   projects: projects.map,
   last,
   times: {
    complete: complete.times,
    answers: answers.times,
    journals: journals.times,
    projects: projects.times,
    last: lastTime
   }
  },
  unresolved: projects.unresolved
 };
}

export function mapsChanged(a, b) {
 const left = normalizeState(a);
 const right = normalizeState(b);
 if (left.last !== right.last) return true;
 return BUCKETS.some((key) => !deepEqual(left[key], right[key]));
}

export function summarizeProgress(state, now = Date.now()) {
 const complete = {1: 0, 2: 0, 3: 0, 4: 0};
 const done = [];
 for (const [key, value] of Object.entries(asMap(state && state.complete))) {
  if (!value) continue;
  const match = /^u([1-4])-/.exec(key);
  if (match) {
   complete[Number(match[1])] += 1;
   done.push(key);
  }
 }
 let attempts = 0;
 let correct = 0;
 const answers = {};
 for (const [id, record] of Object.entries(asMap(state && state.answers))) {
  if (!record || typeof record !== 'object') continue;
  const n = Number(record.attempts) || 0;
  attempts += n;
  const ok = record.status === 'done';
  if (ok) correct += 1;
  if (n || ok || record.status === 'retry') {
   const row = {attempts: n, correct: ok ? 1 : 0};
   if (typeof record.value === 'string') {
    const choice = record.value.trim().slice(0, 200);
    if (choice) row.choice = choice;
   }
   answers[id] = row;
  }
 }
 return {complete, questions: {attempts, correct}, done, answers, lastActivity: now};
}

export function progressFields(profile, state, now, understanding) {
 const counts = summarizeProgress(state, now);
 return {
  uid: profile.uid,
  email: profile.email,
  studentId: profile.studentId ?? null,
  admissionYear: profile.admissionYear ?? null,
  name: typeof profile.name === 'string' ? profile.name : '',
  grade: profile.grade ?? null,
  classroom: profile.classroom ?? null,
  number: profile.number ?? null,
  counts,
  understanding: normalizeUnderstanding(understanding)
 };
}

export function statePayload(state) {
 const next = normalizeState(state);
 return {
  version: 1,
  complete: next.complete,
  answers: next.answers,
  journals: next.journals,
  projects: next.projects,
  last: next.last,
  times: next.times
 };
}

export function cloudToState(data) {
 if (!data || typeof data !== 'object') return emptyState();
 return normalizeState(data);
}

export function projectPreview(project) {
 const files = asMap(project && project.files);
 const names = Object.keys(files);
 const entry = typeof project?.entry === 'string' && files[project.entry] !== undefined ? project.entry : names[0] || '';
 const source = typeof files[entry] === 'string' ? files[entry] : '';
 return {files: names.length, entry, snippet: source.slice(0, 160)};
}
