/* 함께 풀기·수업 리포트(M7/F9) 순수 헬퍼. 막대에는 이름을 넣지 않습니다. */
import {inClass, labelClass} from './class-picker.js';
import {completedTopicIds, completeRate, topicListFromCatalog} from './board-model.js';
import {countUnderstanding, groupHardByTopic, topicTitle, titlesFromCatalog, studentLabel} from './understanding-model.js';
import {sortOpenHelp} from './help-model.js';
import {timestampMillis, focusFields, DEFAULT_PAGE} from './follow-model.js';

export const TOGETHER_TITLE = '함께 풀기';
export const TOGETHER_NOTE = '선택형 문제 하나를 초점으로 보내면, 반 응답 분포를 이름 없이 막대로 봅니다.';
export const TOGETHER_SEND = '이 문제로 함께 풀기';
export const TOGETHER_REFRESH = '응답 새로고침';
export const REPORT_TITLE = '수업 리포트';
export const REPORT_NOTE = '선택한 반과 최근 세션을 기준으로 다음 차시 도입에 쓸 요약을 만듭니다.';
export const BASELINE_KEY_PREFIX = 'aipy-report-baseline:';
export const TRAIL_KEY_PREFIX = 'aipy-focus-trail:';
export const TRAIL_MAX = 24;
export const QUESTION_ANCHOR_RE = /^u[1-4]-q\d+$/;

export function isQuestionAnchor(id) {
 return typeof id === 'string' && QUESTION_ANCHOR_RE.test(id);
}

export function choiceQuestions(catalog, {unit, search} = {}) {
 const q = String(search || '').trim().toLowerCase();
 const unitNum = unit === '' || unit == null ? null : Number(unit);
 return ((catalog && catalog.questions) || []).filter((item) => {
  if (!item || item.kind !== '선택' || !Array.isArray(item.options) || !item.options.length) return false;
  if (unitNum != null && Number.isFinite(unitNum) && Number(item.unit) !== unitNum) return false;
  if (!q) return true;
  return `${item.id} ${item.prompt} ${item.topic}`.toLowerCase().includes(q);
 });
}

export function questionPage(question) {
 const unit = question && Number(question.unit);
 if (!Number.isInteger(unit) || unit < 1 || unit > 4) return DEFAULT_PAGE;
 return `units/unit0${unit}/index.html`;
}

export function focusFromQuestion(question) {
 if (!question || !question.id) return null;
 return focusFields({
  page: questionPage(question),
  topicAnchor: question.id,
  exampleId: null
 });
}

export function choiceValue(record) {
 if (!record || typeof record !== 'object') return '';
 if (typeof record.choice === 'string') return record.choice.trim();
 if (typeof record.value === 'string') return record.value.trim();
 return '';
}

export function collectChoices(progressRows, questionId) {
 const values = [];
 if (!questionId) return values;
 for (const row of progressRows || []) {
  const answers = row && row.counts && row.counts.answers;
  if (!answers || typeof answers !== 'object') continue;
  values.push(choiceValue(answers[questionId]));
 }
 return values;
}

export function collectChoicesFromStates(states, questionId) {
 const values = [];
 if (!questionId) return values;
 for (const state of states || []) {
  const answers = state && state.answers;
  const record = answers && typeof answers === 'object' ? answers[questionId] : null;
  values.push(choiceValue(record));
 }
 return values;
}

export function choiceBars(question, choices) {
 const options = (question && Array.isArray(question.options)) ? question.options : [];
 const counts = new Map(options.map((label) => [label, 0]));
 let other = 0;
 let blank = 0;
 for (const raw of choices || []) {
  const value = typeof raw === 'string' ? raw.trim() : '';
  if (!value) {
   blank += 1;
   continue;
  }
  if (counts.has(value)) counts.set(value, counts.get(value) + 1);
  else other += 1;
 }
 const total = (choices || []).length;
 const answered = total - blank;
 const bars = options.map((label) => ({
  label,
  count: counts.get(label) || 0,
  share: answered ? (counts.get(label) || 0) / answered : 0,
  correct: question && question.answer != null && String(label) === String(question.answer)
 }));
 let crowd = -1;
 let crowdCount = 0;
 bars.forEach((bar, index) => {
  if (!bar.correct && bar.count > crowdCount) {
   crowd = index;
   crowdCount = bar.count;
  }
 });
 if (crowd >= 0 && crowdCount > 0) bars[crowd].crowd = true;
 return {bars, other, blank, answered, total};
}

export function trailStorageKey(classId) {
 return `${TRAIL_KEY_PREFIX}${classId || ''}`;
}

export function baselineStorageKey(classId, startedAt) {
 return `${BASELINE_KEY_PREFIX}${classId || ''}:${timestampMillis(startedAt) || 0}`;
}

export function readJson(storage, key, fallback) {
 if (!storage) return fallback;
 try {
  const raw = storage.getItem(key);
  if (!raw) return fallback;
  const data = JSON.parse(raw);
  return data == null ? fallback : data;
 } catch {
  return fallback;
 }
}

export function writeJson(storage, key, value) {
 if (!storage) return;
 try { storage.setItem(key, JSON.stringify(value)); } catch { /* 사생활 모드 등 */ }
}

export function readTrail(storage, classId) {
 const rows = readJson(storage, trailStorageKey(classId), []);
 return Array.isArray(rows) ? rows : [];
}

export function appendTrail(storage, classId, item, now = Date.now()) {
 const prev = readTrail(storage, classId);
 const entry = {
  page: (item && item.page) || '',
  topicAnchor: (item && item.topicAnchor) || null,
  exampleId: (item && item.exampleId) || null,
  at: now
 };
 const last = prev[prev.length - 1];
 if (last && last.page === entry.page && last.topicAnchor === entry.topicAnchor && last.exampleId === entry.exampleId) {
  return prev;
 }
 const next = [...prev, entry].slice(-TRAIL_MAX);
 writeJson(storage, trailStorageKey(classId), next);
 return next;
}

export function classCompletion({roster = [], progress = [], classId, topicTotal} = {}) {
 const students = (roster || []).filter((row) => inClass(row, classId));
 const rows = students.length ? students : (progress || []).filter((row) => inClass(row, classId));
 const byEmail = new Map();
 for (const row of progress || []) {
  const email = row && row.email ? String(row.email).toLowerCase() : '';
  if (email) byEmail.set(email, row);
 }
 let done = 0;
 for (const person of rows) {
  const email = person && person.email ? String(person.email).toLowerCase() : '';
  const matched = (email && byEmail.get(email)) || person;
  done += completedTopicIds(matched && matched.counts).length;
 }
 const n = rows.length;
 const total = Number(topicTotal) || 0;
 return {
  done,
  students: n,
  topicTotal: total,
  rate: n && total ? completeRate(done, n * total) : 0
 };
}

export function snapshotBaseline(completion, now = Date.now()) {
 return {
  at: now,
  done: completion && completion.done || 0,
  students: completion && completion.students || 0,
  topicTotal: completion && completion.topicTotal || 0,
  rate: completion && completion.rate || 0
 };
}

export function readBaseline(storage, classId, startedAt) {
 return readJson(storage, baselineStorageKey(classId, startedAt), null);
}

export function writeBaseline(storage, classId, startedAt, baseline) {
 writeJson(storage, baselineStorageKey(classId, startedAt), baseline);
}

export function formatRateDelta(before, after) {
 const left = before == null || !Number.isFinite(before) ? null : before;
 const right = after == null || !Number.isFinite(after) ? null : after;
 if (left == null && right == null) return '완료율 —';
 if (left == null) return `지금 ${Math.round(right * 100)}%`;
 if (right == null) return `시작 ${Math.round(left * 100)}%`;
 const delta = right - left;
 const sign = delta > 0 ? '+' : '';
 return `시작 ${Math.round(left * 100)}% → 지금 ${Math.round(right * 100)}% (${sign}${Math.round(delta * 100)}%p)`;
}

export function topicsCovered({trail = [], focus, presence = [], titles = {}} = {}) {
 const seen = new Set();
 const rows = [];
 function add(anchor, page) {
  if (!anchor || isQuestionAnchor(anchor) || seen.has(anchor)) return;
  const unit = page && /unit0([1-4])/.exec(page);
  const topicId = /^u[1-4]-/.test(anchor) ? anchor : (unit ? `u${unit[1]}-${anchor}` : anchor);
  if (seen.has(topicId)) return;
  seen.add(topicId);
  seen.add(anchor);
  rows.push({id: topicId, title: topicTitle(topicId, titles), page: page || ''});
 }
 if (focus && focus.topicAnchor) add(focus.topicAnchor, focus.page);
 for (const item of trail || []) add(item && item.topicAnchor, item && item.page);
 for (const row of presence || []) add(row && row.topicAnchor, row && row.page);
 return rows;
}

export function topHardTopics(progressRows, titles, limit = 3) {
 const {hardRows} = countUnderstanding(progressRows);
 return groupHardByTopic(hardRows).slice(0, limit).map(([topicId, rows]) => ({
  topicId,
  title: topicTitle(topicId, titles),
  count: rows.length
 }));
}

export function missingSubmitters({roster = [], classId, submissions = []} = {}) {
 const submitted = new Set();
 for (const row of submissions || []) {
  const email = row && row.email ? String(row.email).toLowerCase() : '';
  if (email) submitted.add(email);
  if (row && row.uid) submitted.add(row.uid);
 }
 return (roster || []).filter((row) => {
  if (!inClass(row, classId)) return false;
  const email = row.email ? String(row.email).toLowerCase() : String(row.id || '').toLowerCase();
  return !submitted.has(email);
 }).map((row) => ({
  email: row.email || row.id || '',
  name: row.name || '',
  studentId: row.studentId ?? '',
  label: studentLabel(row)
 }));
}

export function sessionWindowLabel(session, now = Date.now()) {
 const start = timestampMillis(session && session.startedAt);
 if (!start) return '최근 수업';
 try {
  const from = new Date(start).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
  const to = new Date(now).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
  return `${from}–${to}`;
 } catch {
  return '최근 수업';
 }
}

export function buildLessonReport({
 classId, session, roster, progress, help, presence, trail, titles, topicTotal,
 assignment, submissions, now = Date.now()
} = {}) {
 const completion = classCompletion({roster, progress, classId, topicTotal});
 const baseline = session && session.baseline ? session.baseline : null;
 const topics = topicsCovered({trail, focus: session && session.focus, presence, titles});
 const hardTop = topHardTopics(progress, titles, 3);
 const openHelp = sortOpenHelp(help);
 const missing = assignment ? missingSubmitters({roster, classId, submissions}) : [];
 return {
  classId: classId || '',
  classLabel: labelClass(classId) || '반 미선택',
  windowLabel: sessionWindowLabel(session, now),
  topics,
  completion,
  baseline,
  completionLabel: formatRateDelta(baseline && baseline.rate, completion.rate),
  hardTop,
  openHelpCount: openHelp.length,
  openHelp,
  assignmentTitle: assignment ? (assignment.title || assignment.id) : '',
  missing,
  missingCount: missing.length
 };
}

export {topicListFromCatalog, titlesFromCatalog, labelClass, studentLabel};
