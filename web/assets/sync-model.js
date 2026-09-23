/* 학습 기록 동기화(M2) 순수 헬퍼. Firebase 없이 병합·요약·쓰기 억제를 검사합니다.
   화면이 읽는 complete/answers/journals/projects 모양은 그대로 두고,
   항목별 시각은 times 맵에만 둡니다. 문항·주제가 늘어도 키를 나열하지 않습니다.
   understanding은 progress 요약에만 두고, 값 모양은 understanding-model이 맞춥니다.
   삭제(#119): 항목이 사라지면 times.tombstones[bucket][key]에 삭제 시각을 남긴다.
   병합 때 상대(로컬/클라우드)에 그 항목이 남아 있어도 삭제 시각이 그 항목 시각보다
   늦거나 같으면 삭제를 유지한다(그래야 되돌리기 후 병합해도 부활하지 않는다). 반대로
   삭제 이후 어느 기기에서 더 늦게 다시 만들었다면 그 항목 시각이 더 늦으므로 살아남는다.
   툼스톤은 TOMBSTONE_TTL_MS가 지나면 무시되어 다음 병합에서 자연히 사라진다(무한 누적 방지). */
import {normalizeUnderstanding} from './understanding-model.js';

export const LEARNING_KEY = 'aipy-lab-v1';
export const CODE_IDLE_MS = 25000;
export const BUCKETS = ['complete', 'answers', 'journals', 'projects'];
export const IMMEDIATE_KINDS = ['complete', 'answer', 'import'];
export const TOMBSTONE_TTL_MS = 30 * 24 * 60 * 60 * 1000;

export function emptyTombstones() {
 return {complete: {}, answers: {}, journals: {}, projects: {}};
}

export function emptyTimes() {
 return {complete: {}, answers: {}, journals: {}, projects: {}, last: 0, tombstones: emptyTombstones()};
}

export function emptyState() {
 return {version: 1, complete: {}, answers: {}, journals: {}, projects: {}, last: '', times: emptyTimes()};
}

export function asMap(value) {
 return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function normalizeTombstoneMap(raw) {
 const map = asMap(raw);
 const out = {};
 for (const [key, value] of Object.entries(map)) {
  const n = Number(value);
  if (Number.isFinite(n) && n > 0) out[key] = n;
 }
 return out;
}

// now 시각 기준으로 아직 유효한(TTL 안의) 삭제 시각을 돌려준다. 지났으면 0(무시).
export function freshTombstone(map, key, now) {
 const t = Number(asMap(map)[key]);
 if (!Number.isFinite(t) || t <= 0) return 0;
 return (now - t) < TOMBSTONE_TTL_MS ? t : 0;
}

export function normalizeState(raw) {
 const state = emptyState();
 if (!raw || typeof raw !== 'object') return state;
 for (const key of BUCKETS) state[key] = {...asMap(raw[key])};
 state.last = typeof raw.last === 'string' ? raw.last : '';
 const times = asMap(raw.times);
 for (const key of BUCKETS) state.times[key] = {...asMap(times[key])};
 const tombstones = asMap(times.tombstones);
 for (const key of BUCKETS) state.times.tombstones[key] = normalizeTombstoneMap(tombstones[key]);
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

export function projectCode(project) {
 const raw = project && typeof project === 'object' && !Array.isArray(project) ? project : {};
 const files = asMap(raw.files);
 const names = Object.keys(files).sort();
 const out = {};
 for (const name of names) out[name] = typeof files[name] === 'string' ? files[name] : String(files[name] ?? '');
 return {
  files: out,
  entry: typeof raw.entry === 'string' ? raw.entry : '',
  stdin: typeof raw.stdin === 'string' ? raw.stdin : '',
  args: typeof raw.args === 'string' ? raw.args : '[]'
 };
}

export function projectCodeEqual(a, b) {
 return deepEqual(projectCode(a), projectCode(b));
}

export function projectMetaScore(project) {
 const raw = project && typeof project === 'object' ? project : {};
 return (Number(raw.attempts) || 0) + (raw.lastOk != null || raw.lastOutput != null ? 1 : 0);
}

export function keepProjectRecord(a, b) {
 return projectMetaScore(b) > projectMetaScore(a) ? b : a;
}

export function projectConflictSignature(id, local, cloud) {
 return `${id}:${JSON.stringify(projectCode(local))}:${JSON.stringify(projectCode(cloud))}`;
}

export const CHOICE_KEY = 'aipy-sync-choices-v1';

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
  last: from.times.last || 0,
  tombstones: {
   complete: {...from.times.tombstones.complete},
   answers: {...from.times.tombstones.answers},
   journals: {...from.times.tombstones.journals},
   projects: {...from.times.tombstones.projects}
  }
 };
 for (const bucket of BUCKETS) {
  const keys = new Set([...Object.keys(from[bucket]), ...Object.keys(to[bucket])]);
  for (const key of keys) {
   const had = Object.hasOwn(from[bucket], key);
   const has = Object.hasOwn(to[bucket], key);
   if (!has) {
    delete to.times[bucket][key];
    // 방금 사라졌다(원본으로 되돌리기 등). 되살아나지 않도록 삭제 시각을 남긴다.
    if (had) to.times.tombstones[bucket][key] = now;
    continue;
   }
   // 항목이 있다 = 삭제가 아니다(다시 만들었거나 원래부터 있었다). 낡은 툼스톤은 지운다.
   delete to.times.tombstones[bucket][key];
   if (!had || !deepEqual(from[bucket][key], to[bucket][key])) {
    if (bucket === 'projects' && had && projectCodeEqual(from[bucket][key], to[bucket][key])) {
     to[bucket][key] = keepProjectRecord(from[bucket][key], to[bucket][key]);
     to.times[bucket][key] = itemTime(from.times, bucket, key) || now;
    } else to.times[bucket][key] = now;
   }
   else if (!itemTime(to.times, bucket, key)) to.times[bucket][key] = itemTime(from.times, bucket, key) || now;
  }
 }
 if (to.last !== from.last) to.times.last = to.last ? now : 0;
 else if (to.last && !to.times.last) to.times.last = now;
 return to;
}

export function mergeBucket(localMap, cloudMap, localTimes, cloudTimes, bucket, now, localTombstones, cloudTombstones) {
 const local = asMap(localMap);
 const cloud = asMap(cloudMap);
 const localTomb = asMap(localTombstones);
 const cloudTomb = asMap(cloudTombstones);
 const keys = new Set([...Object.keys(local), ...Object.keys(cloud), ...Object.keys(localTomb), ...Object.keys(cloudTomb)]);
 const map = {};
 const times = {};
 const tombstones = {};
 for (const key of keys) {
  const hasL = Object.hasOwn(local, key);
  const hasC = Object.hasOwn(cloud, key);
  const lt = itemTime(localTimes, bucket, key);
  const ct = itemTime(cloudTimes, bucket, key);
  const tombTime = Math.max(freshTombstone(localTomb, key, now), freshTombstone(cloudTomb, key, now));
  if (hasL && hasC) {
   if (deepEqual(local[key], cloud[key])) {
    map[key] = local[key];
    times[key] = Math.max(lt, ct);
   } else if (lt >= ct) {
    map[key] = local[key];
    times[key] = lt || now;
   } else {
    map[key] = cloud[key];
    times[key] = ct;
   }
   continue;
  }
  if (hasL && !hasC) {
   // 클라우드에는 없고(다른 기기에서 지웠거나 원래 없었음) 삭제 시각이 이 항목 시각보다
   // 늦거나 같으면 삭제를 유지한다. 그렇지 않으면 이 기기가 더 늦게 만든 것이므로 살린다.
   if (tombTime && tombTime >= lt) { tombstones[key] = tombTime; continue; }
   map[key] = local[key];
   times[key] = lt || now;
   continue;
  }
  if (!hasL && hasC) {
   if (tombTime && tombTime >= ct) { tombstones[key] = tombTime; continue; }
   map[key] = cloud[key];
   times[key] = ct;
   continue;
  }
  // 둘 다 없다 — 삭제 시각만 있으면 TTL 안에서 들고 있는다(뒤늦게 도착하는 기기를 대비).
  if (tombTime) tombstones[key] = tombTime;
 }
 return {map, times, tombstones};
}

export function projectNeedsChoice(localValue, cloudValue, localTime, cloudTime) {
 if (projectCodeEqual(localValue, cloudValue)) return false;
 // 소스(파일·진입점·입력)만 비교합니다. 검사 횟수·출력 같은 부가 정보는 충돌이 아닙니다.
 // 시각이 다르면 늦은 쪽을 따릅니다(기기 전환). 같은 시각에만 학생에게 묻습니다.
 return localTime === cloudTime;
}

export function mergeProjects(localProjects, cloudProjects, localTimes, cloudTimes, choices, now, localTombstones, cloudTombstones) {
 const local = asMap(localProjects);
 const cloud = asMap(cloudProjects);
 const localTomb = asMap(localTombstones);
 const cloudTomb = asMap(cloudTombstones);
 const keys = new Set([...Object.keys(local), ...Object.keys(cloud), ...Object.keys(localTomb), ...Object.keys(cloudTomb)]);
 const map = {};
 const times = {};
 const tombstones = {};
 const unresolved = [];
 for (const key of keys) {
  const hasL = Object.hasOwn(local, key);
  const hasC = Object.hasOwn(cloud, key);
  const lt = itemTime(localTimes, 'projects', key);
  const ct = itemTime(cloudTimes, 'projects', key);
  const tombTime = Math.max(freshTombstone(localTomb, key, now), freshTombstone(cloudTomb, key, now));
  if (hasL && !hasC) {
   if (tombTime && tombTime >= lt) { tombstones[key] = tombTime; continue; }
   map[key] = local[key];
   times[key] = lt || now;
   continue;
  }
  if (!hasL && hasC) {
   if (tombTime && tombTime >= ct) { tombstones[key] = tombTime; continue; }
   map[key] = cloud[key];
   times[key] = ct;
   continue;
  }
  if (!hasL && !hasC) {
   if (tombTime) tombstones[key] = tombTime;
   continue;
  }
  if (projectCodeEqual(local[key], cloud[key])) {
   map[key] = keepProjectRecord(local[key], cloud[key]);
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
 return {map, times, tombstones, unresolved};
}

export function mergeStates(localRaw, cloudRaw, choices, now) {
 const local = normalizeState(localRaw);
 const cloud = normalizeState(cloudRaw);
 const lt = local.times.tombstones, ct = cloud.times.tombstones;
 const complete = mergeBucket(local.complete, cloud.complete, local.times, cloud.times, 'complete', now, lt.complete, ct.complete);
 const answers = mergeBucket(local.answers, cloud.answers, local.times, cloud.times, 'answers', now, lt.answers, ct.answers);
 const journals = mergeBucket(local.journals, cloud.journals, local.times, cloud.times, 'journals', now, lt.journals, ct.journals);
 const projects = mergeProjects(local.projects, cloud.projects, local.times, cloud.times, choices, now, lt.projects, ct.projects);
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
    last: lastTime,
    tombstones: {
     complete: complete.tombstones,
     answers: answers.tombstones,
     journals: journals.tombstones,
     projects: projects.tombstones
    }
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
