/* 성취수준 참고 지표(#145-B) 순수 함수. Firebase 호출 없이 학생 state(students/{uid}/state/current),
   catalog.json(questions/examples/topics), data/standards.json(13개 성취기준 ↔ 소단원 매핑)을 받아
   성취기준별 이해·적용·성찰·참여 지표와 가중합 점수, A~E 수준을 계산한다.

   이 모듈이 내는 숫자는 "웹 실습 기록"만 근거로 한 참고 지표다 — 수행평가·지필평가 점수가
   아니며, 최종 성취수준은 교사가 판단한다(화면 고정 안내와 같은 전제). 가중치·분할점수·글자 수
   하한은 모두 settings 객체로 받아 교사가 화면에서 바꿀 수 있게 한다(localStorage는 이 파일이
   아니라 호출부가 저장 위치를 넘겨 쓴다 — 여기서는 순수 변환만 한다).

   예제→소단원 인덱스는 board-model.js의 exampleIndexFromCatalog() 결과를 그대로 받는다(중복 금지).
   원본 코드 vs 학생 코드 diff는 code-diff-model.js의 projectDiffSummary()를 그대로 쓴다. */

export const LEVELS = ['A', 'B', 'C', 'D', 'E'];

export function defaultSettings() {
 return {
  weights: {understand: 50, apply: 20, reflect: 20, participate: 10},
  cutoffs: {A: 90, B: 80, C: 70, D: 60},
  advancedWeight: 1.5,
  minReflectLen: 10,
  minEvidence: 1
 };
}

const SETTINGS_STORAGE_KEY = 'aipy-achievement-settings-v1';

function clampNumber(value, fallback, min, max) {
 const n = Number(value);
 if (!Number.isFinite(n)) return fallback;
 if (min != null && n < min) return min;
 if (max != null && n > max) return max;
 return n;
}

// partial은 localStorage에서 막 읽어 온 값일 수 있어 어떤 필드가 빠져도 defaultSettings()로 채운다.
export function mergeSettings(partial) {
 const base = defaultSettings();
 const p = partial && typeof partial === 'object' ? partial : {};
 const weights = {...base.weights, ...(p.weights && typeof p.weights === 'object' ? p.weights : {})};
 const cutoffs = {...base.cutoffs, ...(p.cutoffs && typeof p.cutoffs === 'object' ? p.cutoffs : {})};
 return {
  weights,
  cutoffs,
  advancedWeight: clampNumber(p.advancedWeight, base.advancedWeight, 1, 5),
  minReflectLen: clampNumber(p.minReflectLen, base.minReflectLen, 0, 500),
  minEvidence: clampNumber(p.minEvidence, base.minEvidence, 0, 50)
 };
}

export function loadSettings(storage) {
 try {
  const raw = storage && typeof storage.getItem === 'function' ? storage.getItem(SETTINGS_STORAGE_KEY) : null;
  if (!raw) return defaultSettings();
  return mergeSettings(JSON.parse(raw));
 } catch {
  return defaultSettings();
 }
}

export function saveSettings(storage, settings) {
 try {
  if (storage && typeof storage.setItem === 'function') {
   storage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(mergeSettings(settings)));
  }
 } catch {
  // localStorage가 막혀 있어도(사생활 보호 모드 등) 조용히 무시 — 기본값으로 계속 동작한다.
 }
}

function asMapSafe(value) {
 return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function hasValue(value) {
 if (Array.isArray(value)) return value.length > 0;
 return value != null && String(value).trim() !== '';
}

// standards.json의 subunits([{unit,id}])를 'u{unit}-{id}' topicId 배열로 편다.
export function subunitTopicIds(standard) {
 const subunits = Array.isArray(standard && standard.subunits) ? standard.subunits : [];
 return subunits
  .filter((s) => s && s.unit != null && s.id)
  .map((s) => `u${Number(s.unit)}-${s.id}`);
}

// exampleIndex(board-model exampleIndexFromCatalog 결과)에서 standard의 소단원에 속한 예제id만 골라낸다.
export function exampleIdsForStandard(standard, exampleIndex) {
 const topicIds = new Set(subunitTopicIds(standard));
 const index = asMapSafe(exampleIndex);
 const ids = [];
 for (const [eid, meta] of Object.entries(index)) {
  if (!meta) continue;
  const tid = `u${Number(meta.unit)}-${meta.topicId}`;
  if (topicIds.has(tid)) ids.push(eid);
 }
 return ids;
}

// (a) 이해 = 해당 소단원 연습문제 정답률. 심화 문항은 settings.advancedWeight로 가중한다.
// 시도(답안 기록)가 하나도 없으면 score:null, attempted:0을 돌려준다 — 이 경우 standardScore()가
// '판단 보류(증거 부족)'로 처리한다.
export function understandingScore(standard, state, questions, settings = defaultSettings()) {
 const topicIds = new Set(subunitTopicIds(standard));
 const answers = asMapSafe(state && state.answers);
 let weightTotal = 0;
 let correctWeighted = 0;
 let attempted = 0;
 let totalQuestions = 0;
 for (const q of questions || []) {
  if (!q || !q.id || q.unit == null) continue;
  const tid = `u${Number(q.unit)}-${q.topic || ''}`;
  if (!topicIds.has(tid)) continue;
  totalQuestions += 1;
  const weight = q.level === '심화' ? settings.advancedWeight : 1;
  const rec = answers[q.id];
  const attemptedThis = !!rec && typeof rec === 'object' && (Number(rec.attempts) > 0 || hasValue(rec.value));
  if (!attemptedThis) continue;
  attempted += 1;
  weightTotal += weight;
  if (rec.status === 'done') correctWeighted += weight;
 }
 if (attempted === 0 || weightTotal === 0) return {score: null, attempted, totalQuestions};
 return {score: Math.round((correctWeighted / weightTotal) * 100), attempted, totalQuestions};
}

// 예제id가 journal 키 접두(m-, p-, c-)에서 어느 예제를 가리키는지 하이픈 때문에 모호할 수 있어
// (예: 'cv-yolo-count') exampleIds를 긴 것부터 접두로 맞춰 본다. board-model.js와 같은 방식.
function matchExampleId(rest, sortedExampleIds) {
 for (const id of sortedExampleIds) {
  if (rest === id) return {id, suffix: ''};
  if (rest.startsWith(`${id}-`)) return {id, suffix: rest.slice(id.length + 1)};
 }
 return null;
}

function journalExampleSets(state, exampleIds) {
 const journals = asMapSafe(state && state.journals);
 const sorted = [...exampleIds].sort((a, b) => b.length - a.length);
 const missionPassed = new Set();
 const predicted = new Set();
 const codeReadRefs = new Map(); // eid -> Set(ref)
 for (const [key, text] of Object.entries(journals)) {
  const value = typeof text === 'string' ? text.trim() : (text != null ? String(text) : '');
  if (key.startsWith('m-')) {
   const found = matchExampleId(key.slice(2), sorted);
   if (found && found.suffix && /^\d+$/.test(found.suffix)) missionPassed.add(found.id);
   continue;
  }
  if (key.startsWith('p-') && value) {
   const found = matchExampleId(key.slice(2), sorted);
   if (found) predicted.add(found.id);
   continue;
  }
  if (key.startsWith('c-')) {
   const found = matchExampleId(key.slice(2), sorted);
   if (found && found.suffix) {
    if (!codeReadRefs.has(found.id)) codeReadRefs.set(found.id, new Map());
    codeReadRefs.get(found.id).set(found.suffix, value);
   }
  }
 }
 return {missionPassed, predicted, codeReadRefs};
}

// (b) 적용 = 미션 통과 · 예제 코드 수정 여부 · 예측(결과 비교) 작성. 세 신호 각각 "해당 소단원
// 안에서 적용 가능한 예제 중 몇 개가 충족됐는지" 비율로 보고, 평균한다. originalFilesById가 없으면
// (원본을 아직 못 받아 왔으면) '코드 수정' 신호는 판단하지 않고 나머지 두 신호로만 평균한다 —
// 모든 신호가 적용 불가능(예제가 없음)하면 score:null.
export function applyScore(standard, state, exampleIndex, originalFilesById, settings = defaultSettings()) {
 const eids = exampleIdsForStandard(standard, exampleIndex);
 if (!eids.length) return {score: null, exampleCount: 0};
 const {missionPassed, predicted} = journalExampleSets(state, eids);
 const projects = asMapSafe(state && state.projects);
 const index = asMapSafe(exampleIndex);
 const rates = [];

 const missionEligible = eids.filter((eid) => Array.isArray(index[eid] && index[eid].missions) && index[eid].missions.length);
 if (missionEligible.length) {
  const passed = missionEligible.filter((eid) => missionPassed.has(eid)).length;
  rates.push(passed / missionEligible.length);
 }

 if (originalFilesById && typeof originalFilesById === 'object') {
  const knownOriginal = eids.filter((eid) => originalFilesById[eid]);
  if (knownOriginal.length) {
   // code-diff-model.js를 쓰지 않고(순환 참조 방지) 여기서는 단순히 "학생이 저장한 파일이 있고,
   // 그 내용이 비지 않았는지"만 본다 — 실제 줄 단위 diff는 화면이 projectDiffSummary로 계산해
   // modifiedExampleIds로 미리 넘겨주면 더 정확하다(아래 applyScoreWithDiff 참고).
   const touched = knownOriginal.filter((eid) => {
    const files = projects[eid] && projects[eid].files;
    return files && typeof files === 'object' && Object.values(files).some(hasValue);
   }).length;
   rates.push(touched / knownOriginal.length);
  }
 }

 const predictedRate = predicted.size ? eids.filter((eid) => predicted.has(eid)).length / eids.length : (eids.length ? 0 : null);
 if (predictedRate != null) rates.push(predictedRate);

 if (!rates.length) return {score: null, exampleCount: eids.length};
 const avg = rates.reduce((sum, r) => sum + r, 0) / rates.length;
 return {score: Math.round(avg * 100), exampleCount: eids.length};
}

// applyScore의 '코드 수정' 신호를 실제 줄 단위 diff(modifiedExampleIds: Set<eid>)로 정확히 계산하고
// 싶을 때 쓰는 버전. 화면(teacher-achievement.js)이 code-diff-model.js의 projectDiffSummary()로
// 미리 계산해 넘긴다. modifiedExampleIds가 없으면 applyScore()와 동일하게 동작한다.
export function applyScoreWithDiff(standard, state, exampleIndex, modifiedExampleIds, settings = defaultSettings()) {
 const eids = exampleIdsForStandard(standard, exampleIndex);
 if (!eids.length) return {score: null, exampleCount: 0};
 const {missionPassed, predicted} = journalExampleSets(state, eids);
 const index = asMapSafe(exampleIndex);
 const projects = asMapSafe(state && state.projects);
 const rates = [];

 const missionEligible = eids.filter((eid) => Array.isArray(index[eid] && index[eid].missions) && index[eid].missions.length);
 if (missionEligible.length) rates.push(missionEligible.filter((eid) => missionPassed.has(eid)).length / missionEligible.length);

 const attempted = eids.filter((eid) => projects[eid]);
 if (attempted.length && modifiedExampleIds instanceof Set) {
  rates.push(attempted.filter((eid) => modifiedExampleIds.has(eid)).length / attempted.length);
 }

 if (eids.length) rates.push(eids.filter((eid) => predicted.has(eid)).length / eids.length);

 if (!rates.length) return {score: null, exampleCount: eids.length};
 const avg = rates.reduce((sum, r) => sum + r, 0) / rates.length;
 return {score: Math.round(avg * 100), exampleCount: eids.length};
}

// (c) 성찰 = 소단원 저널(j-) + '직접 해 보세요' 제출(d-...-submitted, 글자 수 하한) +
// 코드 읽기 설명(c-) 작성률. 세 하위 지표를 구할 수 있는 만큼만 평균한다.
export function reflectScore(standard, state, tasks, exampleIndex, settings = defaultSettings()) {
 const topicIds = subunitTopicIds(standard);
 const journals = asMapSafe(state && state.journals);
 const taskMap = asMapSafe(tasks);
 const minLen = settings.minReflectLen;
 const rates = [];

 if (topicIds.length) {
  const withJournal = topicIds.filter((tid) => {
   const text = journals[`j-${tid}`];
   return typeof text === 'string' && text.trim().length >= minLen;
  }).length;
  rates.push(withJournal / topicIds.length);
 }

 let taskExpected = 0;
 let taskDone = 0;
 for (const tid of topicIds) {
  const prefix = `${tid}-`;
  const indices = Object.keys(taskMap)
   .filter((key) => key.startsWith(prefix) && /^\d+$/.test(key.slice(prefix.length)))
   .map((key) => key.slice(prefix.length));
  for (const idx of indices) {
   taskExpected += 1;
   const text = journals[`d-${tid}-${idx}`];
   if (typeof text === 'string' && text.trim().length >= minLen) taskDone += 1;
  }
 }
 if (taskExpected) rates.push(taskDone / taskExpected);

 const eids = exampleIdsForStandard(standard, exampleIndex);
 const index = asMapSafe(exampleIndex);
 let codeExpected = 0;
 let codeDone = 0;
 for (const eid of eids) {
  const keyLines = Array.isArray(index[eid] && index[eid].keyLines) ? index[eid].keyLines : [];
  for (const kl of keyLines) {
   if (!kl || !kl.ref) continue;
   codeExpected += 1;
   const text = journals[`c-${eid}-${kl.ref}`];
   if (typeof text === 'string' && text.trim().length >= minLen) codeDone += 1;
  }
 }
 if (codeExpected) rates.push(codeDone / codeExpected);

 if (!rates.length) return {score: null};
 const avg = rates.reduce((sum, r) => sum + r, 0) / rates.length;
 return {score: Math.round(avg * 100)};
}

// (d) 참여 = 완료 체크(complete[topicId]===true) 비율.
export function participateScore(standard, state) {
 const topicIds = subunitTopicIds(standard);
 if (!topicIds.length) return {score: null};
 const complete = asMapSafe(state && state.complete);
 const done = topicIds.filter((tid) => complete[tid] === true).length;
 return {score: Math.round((done / topicIds.length) * 100)};
}

export function levelFromScore(score, cutoffs) {
 if (score == null || !Number.isFinite(score)) return null;
 const c = cutoffs || defaultSettings().cutoffs;
 if (score >= c.A) return 'A';
 if (score >= c.B) return 'B';
 if (score >= c.C) return 'C';
 if (score >= c.D) return 'D';
 return 'E';
}

export const INSUFFICIENT = '판단 보류(증거 부족)';

// 성취기준 하나의 종합 점수. ctx = {state, questions, exampleIndex, tasks, originalFilesById?,
// modifiedExampleIds?}. understand 증거(시도한 문항 수)가 settings.minEvidence보다 적으면
// 다른 지표와 무관하게 '판단 보류'로 둔다 — 이해 문항이 성취기준의 1차 근거이기 때문이다.
export function standardScore(standard, ctx, settings = defaultSettings()) {
 const s = mergeSettings(settings);
 const understand = understandingScore(standard, ctx.state, ctx.questions, s);
 if ((understand.attempted || 0) < s.minEvidence) {
  return {
   code: standard.code,
   score: null,
   level: INSUFFICIENT,
   insufficient: true,
   dimensions: {understand, apply: {score: null}, reflect: {score: null}, participate: {score: null}}
  };
 }
 const apply = ctx.modifiedExampleIds
  ? applyScoreWithDiff(standard, ctx.state, ctx.exampleIndex, ctx.modifiedExampleIds, s)
  : applyScore(standard, ctx.state, ctx.exampleIndex, ctx.originalFilesById, s);
 const reflect = reflectScore(standard, ctx.state, ctx.tasks, ctx.exampleIndex, s);
 const participate = participateScore(standard, ctx.state);

 const dims = [
  {key: 'understand', weight: s.weights.understand, value: understand.score},
  {key: 'apply', weight: s.weights.apply, value: apply.score},
  {key: 'reflect', weight: s.weights.reflect, value: reflect.score},
  {key: 'participate', weight: s.weights.participate, value: participate.score}
 ].filter((d) => d.value != null);
 const weightSum = dims.reduce((sum, d) => sum + d.weight, 0);
 const score = weightSum > 0 ? Math.round(dims.reduce((sum, d) => sum + d.weight * d.value, 0) / weightSum) : null;
 const level = score != null ? levelFromScore(score, s.cutoffs) : INSUFFICIENT;
 return {
  code: standard.code,
  score,
  level,
  insufficient: score == null,
  dimensions: {understand, apply, reflect, participate}
 };
}

// 학생 한 명의 13개 성취기준 결과 배열(순서는 standards.json 순서를 따른다).
export function studentStandardScores(standards, ctx, settings = defaultSettings()) {
 return (standards || []).map((standard) => standardScore(standard, ctx, settings));
}

// 단원 평균(해당 단원 소단원을 가진 성취기준들의 평균) — 판단 보류는 제외하고 평균한다.
// 전부 판단 보류면 scoreUnit도 null을 돌려준다.
export function unitAverage(standardResults, standards, unit) {
 const codes = new Set((standards || []).filter((s) => (s.subunits || []).some((su) => Number(su.unit) === Number(unit))).map((s) => s.code));
 const scores = (standardResults || []).filter((r) => codes.has(r.code) && r.score != null).map((r) => r.score);
 if (!scores.length) return {score: null, level: INSUFFICIENT};
 const score = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
 return {score, level: levelFromScore(score, defaultSettings().cutoffs)};
}

export function overallAverage(standardResults, settings = defaultSettings()) {
 const s = mergeSettings(settings);
 const scores = (standardResults || []).filter((r) => r.score != null).map((r) => r.score);
 if (!scores.length) return {score: null, level: INSUFFICIENT};
 const score = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
 return {score, level: levelFromScore(score, s.cutoffs)};
}

// 반 분포표: 성취기준별 A~E·판단보류 인원 수와 평균 점수.
export function classDistribution(allStudentResults, standards) {
 return (standards || []).map((standard) => {
  const counts = {A: 0, B: 0, C: 0, D: 0, E: 0, insufficient: 0};
  const scores = [];
  for (const results of allStudentResults || []) {
   const r = (results || []).find((x) => x.code === standard.code);
   if (!r || r.insufficient || r.score == null) {
    counts.insufficient += 1;
    continue;
   }
   counts[r.level] = (counts[r.level] || 0) + 1;
   scores.push(r.score);
  }
  const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
  return {code: standard.code, area: standard.area, statement: standard.statement, counts, average: avg, n: scores.length};
 });
}

// 과장 없는 1~2문장 강점/보완점. 가장 높은(A/B) 성취기준 1개, 가장 낮은(D/E/판단보류 제외) 1개를
// 수치와 함께 템플릿 문장으로 만든다 — 숫자 없는 주관적 평가 문장은 쓰지 않는다.
export function strengthsWeaknesses(standardResults, standards) {
 const byCode = new Map((standards || []).map((s) => [s.code, s]));
 const scored = (standardResults || []).filter((r) => r.score != null);
 if (!scored.length) return {strengths: [], weaknesses: [], note: '웹 실습 기록이 거의 없어 강점·보완점을 추정할 수 없습니다.'};
 const sorted = [...scored].sort((a, b) => b.score - a.score);
 const strengths = sorted.slice(0, 2).filter((r) => r.score >= 80).map((r) => {
  const std = byCode.get(r.code);
  return `[${r.code}] ${std ? std.area : ''} 영역에서 ${r.level} 수준(점수 ${r.score})으로, 이해 ${fmtDim(r.dimensions.understand.score)} · 적용 ${fmtDim(r.dimensions.apply.score)}의 기록을 보입니다.`;
 });
 const weak = [...scored].sort((a, b) => a.score - b.score).slice(0, 2).filter((r) => r.score < 70).map((r) => {
  const std = byCode.get(r.code);
  return `[${r.code}] ${std ? std.area : ''} 영역은 ${r.level} 수준(점수 ${r.score})으로, 이해 ${fmtDim(r.dimensions.understand.score)} · 참여 ${fmtDim(r.dimensions.participate.score)} 기록이 낮아 보완이 필요합니다.`;
 });
 return {strengths, weaknesses: weak, note: ''};
}

function fmtDim(score) {
 return score == null ? '기록 없음' : `${score}%`;
}

// 학생별 CSV 행(교사 출력용). header는 호출부가 한 번만 만들어 쓴다.
export function achievementCsvHeader(standards) {
 const base = ['학번', '이름'];
 for (const s of standards || []) base.push(`${s.code} 수준`, `${s.code} 점수`);
 base.push('전체 평균 수준', '전체 평균 점수');
 return base;
}

export function achievementCsvRow(student, standardResults, standards) {
 const row = [student.studentId || '', student.name || student.label || ''];
 const byCode = new Map((standardResults || []).map((r) => [r.code, r]));
 for (const s of standards || []) {
  const r = byCode.get(s.code);
  row.push(r ? r.level : INSUFFICIENT, r && r.score != null ? r.score : '');
 }
 const overall = overallAverage(standardResults);
 row.push(overall.level, overall.score != null ? overall.score : '');
 return row;
}
