/* 과제·제출(M6/F7) 순수 헬퍼. 카탈로그 고르기·제출 상태·이력·쓰로틀을 Firebase 없이 검사합니다.
   과제는 코드가 아니라 데이터입니다. 문항·예제는 생성기 catalog.json에서 가져옵니다. */
import {classId as rosterClassId} from './class-picker.js';
import {timestampMillis} from './follow-model.js';
import {studentLabel} from './understanding-model.js';

export const SUBMIT_COOLDOWN_MS = 4000;
export const OUTPUT_MAX = 4000;
export const FILE_MAX = 40000;
export const FILES_MAX = 12;
export const HISTORY_MAX = 8;
export const TITLE_MAX = 80;
export const DESC_MAX = 500;
export const COMMENT_MAX = 80;
export const TARGETS_MAX = 40;
export const CLASSROOMS_MAX = 20;

export const TARGET_TYPES = ['question', 'example'];
export const SUBMIT_PASSED = 'passed';
export const SUBMIT_FAILED = 'failed';
export const REVIEW_PENDING = 'pending';
export const REVIEW_DONE = 'reviewed';

export const LABEL_PASSED = '통과';
export const LABEL_FAILED = '미통과 제출';
export const LABEL_LATE = '지연';
export const LABEL_REVIEWED = '확인됨';
export const LABEL_PENDING = '확인 대기';
export const BROWSER_GRADE_NOTE = '브라우저 채점 결과예요. 성적으로 바로 쓰이지 않아요.';
export const LATE_NOTE = '마감 후에도 제출할 수 있어요. 지연으로 표시돼요.';
export const FAIL_OK_NOTE = '검사를 한 뒤 제출할 수 있어요. 통과하지 않아도 제출할 수 있어요.';
export const REGRADE_NOTE = '브라우저에서 다시 채점하는 기능은 다음 단계에서 붙습니다.';
export const SUBMIT_LABEL = '제출';
export const RESUBMIT_LABEL = '다시 제출';

export function clipText(value, max) {
 if (value == null) return '';
 return String(value).replace(/\s+/g, ' ').trim().slice(0, max);
}

export function clipOutput(text) {
 if (text == null) return '';
 return String(text).trim().slice(0, OUTPUT_MAX);
}

export function clipComment(text) {
 return clipText(text, COMMENT_MAX);
}

export function clipFiles(files) {
 const out = {};
 if (!files || typeof files !== 'object' || Array.isArray(files)) return out;
 const names = Object.keys(files).filter((name) => typeof name === 'string' && name && typeof files[name] === 'string');
 for (const name of names.slice(0, FILES_MAX)) {
  out[name] = String(files[name]).slice(0, FILE_MAX);
 }
 return out;
}

export function targetKey(target) {
 if (!target || !TARGET_TYPES.includes(target.type) || !target.id) return '';
 return `${target.type}:${target.id}`;
}

export function parseTargetKey(key) {
 if (typeof key !== 'string') return null;
 const match = /^(question|example):(.+)$/.exec(key);
 if (!match) return null;
 return {type: match[1], id: match[2]};
}

export function normalizeTarget(raw) {
 if (!raw || typeof raw !== 'object') return null;
 const type = raw.type === 'example' ? 'example' : raw.type === 'question' ? 'question' : '';
 const id = typeof raw.id === 'string' ? raw.id.trim() : '';
 if (!type || !id || id.length > 80) return null;
 return {type, id};
}

export function normalizeTargets(list) {
 const out = [];
 const seen = new Set();
 for (const raw of list || []) {
  const target = normalizeTarget(raw);
  if (!target) continue;
  const key = targetKey(target);
  if (seen.has(key)) continue;
  seen.add(key);
  out.push(target);
  if (out.length >= TARGETS_MAX) break;
 }
 return out;
}

export function normalizeClassrooms(list) {
 const out = [];
 const seen = new Set();
 for (const raw of list || []) {
  const id = typeof raw === 'string' ? raw.trim() : '';
  if (!/^\d+-\d+$/.test(id) || seen.has(id)) continue;
  seen.add(id);
  out.push(id);
  if (out.length >= CLASSROOMS_MAX) break;
 }
 return out;
}

export function catalogTargets(catalog) {
 const items = [];
 for (const q of (catalog && catalog.questions) || []) {
  if (!q || !q.id) continue;
  items.push({
   type: 'question',
   id: q.id,
   unit: q.unit ?? null,
   kind: q.kind || '',
   topic: q.topic || '',
   title: q.prompt || q.id,
   prompt: q.prompt || ''
  });
 }
 const examples = catalog && catalog.examples;
 if (examples && typeof examples === 'object' && !Array.isArray(examples)) {
  for (const [id, meta] of Object.entries(examples)) {
   const row = meta && typeof meta === 'object' ? meta : {};
   items.push({
    type: 'example',
    id,
    unit: row.unit ?? null,
    kind: row.mode || '',
    topic: '',
    title: row.title || id,
    prompt: row.title || id
   });
  }
 }
 return items;
}

export function filterCatalogTargets(items, {unit, type, search} = {}) {
 const q = String(search || '').trim().toLowerCase();
 const unitNum = unit === '' || unit == null ? null : Number(unit);
 return (items || []).filter((item) => {
  if (unitNum != null && Number.isFinite(unitNum) && Number(item.unit) !== unitNum) return false;
  if (type && item.type !== type) return false;
  if (!q) return true;
  return `${item.id} ${item.title} ${item.prompt} ${item.topic} ${item.kind}`.toLowerCase().includes(q);
 });
}

export function targetTitle(target, catalog) {
 const found = catalogTargets(catalog).find((item) => item.type === target.type && item.id === target.id);
 return found ? (found.title || target.id) : (target && target.id) || '';
}

export function targetHref(prefix, target, catalog) {
 if (!target) return '';
 const base = prefix || '';
 if (target.type === 'question') {
  const fromId = /^u([1-4])-/.exec(target.id);
  const unit = target.unit || (fromId ? Number(fromId[1]) : null);
  if (!unit) return '';
  return `${base}units/unit0${unit}/index.html#${target.id}`;
 }
 const topics = catalog && catalog.topics;
 if (topics && typeof topics === 'object') {
  for (const [page, rows] of Object.entries(topics)) {
   for (const row of rows || []) {
    if (row && Array.isArray(row.examples) && row.examples.includes(target.id)) {
     return `${base}${page}#${row.id}`;
    }
   }
  }
 }
 if (target.unit) return `${base}units/unit0${target.unit}/index.html#lab`;
 return `${base}units/unit01/index.html#lab`;
}

export function assignmentVisible(assignment, classId, now = Date.now()) {
 if (!assignment || assignment.open !== true) return false;
 if (!classId || !Array.isArray(assignment.classrooms) || !assignment.classrooms.includes(classId)) return false;
 const openAt = timestampMillis(assignment.openAt);
 if (openAt && now < openAt) return false;
 return true;
}

export function isLate(assignment, now = Date.now()) {
 const due = timestampMillis(assignment && assignment.dueAt);
 return Boolean(due && now > due);
}

export function statusLabel({status, late} = {}) {
 const fail = status === SUBMIT_FAILED;
 const pass = status === SUBMIT_PASSED;
 if (late && fail) return `${LABEL_FAILED} · ${LABEL_LATE}`;
 if (late && pass) return LABEL_LATE;
 if (fail) return LABEL_FAILED;
 if (pass) return LABEL_PASSED;
 return '';
}

export function reviewLabel(reviewStatus) {
 return reviewStatus === REVIEW_DONE ? LABEL_REVIEWED : LABEL_PENDING;
}

export function submitButtonLabel({status, hasSubmission} = {}) {
 if (hasSubmission) return status === SUBMIT_FAILED ? `${LABEL_FAILED} · ${RESUBMIT_LABEL}` : RESUBMIT_LABEL;
 return status === SUBMIT_FAILED ? LABEL_FAILED : SUBMIT_LABEL;
}

export function assignmentFields({title, description, targets, classrooms, openAt, dueAt, open, createdBy} = {}) {
 return {
  title: clipText(title, TITLE_MAX),
  description: typeof description === 'string' ? description.trim().slice(0, DESC_MAX) : '',
  targets: normalizeTargets(targets),
  classrooms: normalizeClassrooms(classrooms),
  openAt: openAt || null,
  dueAt: dueAt || null,
  open: open !== false,
  createdBy: typeof createdBy === 'string' ? createdBy.trim().toLowerCase().slice(0, 80) : ''
 };
}

export function assignmentReady(fields) {
 if (!fields) return false;
 return Boolean(fields.title && fields.targets.length && fields.classrooms.length && fields.createdBy);
}

export function targetSnapshot({type, id, files, stdin, args, grade, output, attempts} = {}) {
 const target = normalizeTarget({type, id});
 if (!target) return null;
 const ok = Boolean(grade && grade.ok);
 return {
  type: target.type,
  id: target.id,
  files: clipFiles(files),
  stdin: typeof stdin === 'string' ? stdin.slice(0, 2000) : '',
  args: typeof args === 'string' ? args.slice(0, 400) : '[]',
  grade: {
   ok,
   checked: Boolean(grade && grade.checked),
   kind: 'browser'
  },
  output: clipOutput(output),
  attempts: Math.max(0, Number(attempts) || 0)
 };
}

export function targetsFromState({assignment, state, lastChecks, catalog} = {}) {
 const out = {};
 const answers = state && state.answers && typeof state.answers === 'object' ? state.answers : {};
 const projects = state && state.projects && typeof state.projects === 'object' ? state.projects : {};
 const checks = lastChecks && typeof lastChecks === 'object' ? lastChecks : {};
 const items = catalogTargets(catalog);
 for (const target of normalizeTargets(assignment && assignment.targets)) {
  const key = targetKey(target);
  const live = checks[key] || {};
  if (target.type === 'example') {
   const project = projects[target.id] || {};
   const snap = targetSnapshot({
    type: 'example',
    id: target.id,
    files: project.files,
    stdin: project.stdin,
    args: project.args,
    grade: {ok: live.ok ?? project.lastOk, checked: live.checked ?? Boolean(project.lastOk != null)},
    output: live.output || project.lastOutput || '',
    attempts: live.attempts ?? project.attempts ?? 0
   });
   if (snap) out[key] = snap;
   continue;
  }
  const record = answers[target.id] || {};
  const item = items.find((row) => row.type === 'question' && row.id === target.id);
  const value = record.value;
  const source = typeof value === 'string' ? value : (Array.isArray(value) ? value.join('\n') : (value == null ? '' : JSON.stringify(value)));
  const fileName = record.starter || (item && /구현|오류/.test(item.kind)) ? 'main.py' : 'answer.txt';
  const snap = targetSnapshot({
   type: 'question',
   id: target.id,
   files: {[fileName]: source},
   stdin: '',
   args: '[]',
   grade: {ok: live.ok ?? record.status === 'done', checked: live.checked ?? Boolean(record.status)},
   output: live.output || record.feedback || '',
   attempts: live.attempts ?? record.attempts ?? 0
  });
  if (snap) out[key] = snap;
 }
 return out;
}

export function submissionStatus(targets) {
 const rows = targets && typeof targets === 'object' ? Object.values(targets) : [];
 if (!rows.length) return SUBMIT_FAILED;
 return rows.every((row) => row && row.grade && row.grade.ok) ? SUBMIT_PASSED : SUBMIT_FAILED;
}

function compactTargets(targets) {
 const out = {};
 for (const [key, row] of Object.entries(targets && typeof targets === 'object' ? targets : {})) {
  if (!row) continue;
  out[key] = {
   ok: Boolean(row.grade && row.grade.ok),
   output: clipOutput(row.output).slice(0, 240)
  };
 }
 return out;
}

export function historyEntry(submission) {
 if (!submission) return null;
 return {
  submittedAt: submission.submittedAt || null,
  status: submission.status || SUBMIT_FAILED,
  late: Boolean(submission.late),
  attemptCount: Number(submission.attemptCount) || 0,
  reviewStatus: submission.reviewStatus || REVIEW_PENDING,
  reviewComment: clipComment(submission.reviewComment),
  targets: compactTargets(submission.targets)
 };
}

export function appendHistory(previous, max = HISTORY_MAX) {
 const prev = Array.isArray(previous && previous.history) ? previous.history.slice() : [];
 const entry = historyEntry(previous);
 if (entry && (previous.submittedAt || previous.attemptCount)) prev.push(entry);
 return prev.slice(-max);
}

export function submissionFields({profile, assignmentId, classId, targets, late, previous} = {}) {
 const person = profile && typeof profile === 'object' ? profile : {};
 const classroomId = classId || rosterClassId(person);
 const status = submissionStatus(targets);
 const prevCount = Number(previous && previous.attemptCount) || 0;
 return {
  assignmentId: assignmentId || '',
  uid: person.uid || '',
  email: person.email || '',
  studentId: person.studentId ?? null,
  admissionYear: person.admissionYear ?? null,
  name: typeof person.name === 'string' ? person.name : '',
  grade: person.grade ?? null,
  classroom: person.classroom ?? null,
  number: person.number ?? null,
  classId: classroomId || '',
  status,
  late: Boolean(late),
  attemptCount: prevCount + 1,
  targets: targets && typeof targets === 'object' ? targets : {},
  history: appendHistory(previous),
  reviewStatus: REVIEW_PENDING,
  reviewComment: previous ? clipComment(previous.reviewComment) : '',
  reviewedAt: previous && previous.reviewedAt ? previous.reviewedAt : null,
  reviewedBy: previous && previous.reviewedBy ? previous.reviewedBy : null
 };
}

export function teacherReviewFields({comment, email} = {}) {
 return {
  reviewStatus: REVIEW_DONE,
  reviewComment: clipComment(comment),
  reviewedBy: typeof email === 'string' ? email.trim().toLowerCase().slice(0, 80) : ''
 };
}

export function canSubmit({lastAt, now} = {}) {
 if (!lastAt) return {ok: true, reason: ''};
 if (Number(now) - Number(lastAt) < SUBMIT_COOLDOWN_MS) return {ok: false, reason: 'cooldown'};
 return {ok: true, reason: ''};
}

export function toDatetimeLocal(value) {
 const ms = timestampMillis(value);
 if (!ms) return '';
 const d = new Date(ms);
 const pad = (n) => String(n).padStart(2, '0');
 return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function fromDatetimeLocal(value) {
 if (!value || typeof value !== 'string') return null;
 const ms = Date.parse(value);
 return Number.isFinite(ms) ? new Date(ms) : null;
}

export function formatWhen(value) {
 const ms = timestampMillis(value);
 if (!ms) return '';
 try {
  return new Date(ms).toLocaleString('ko-KR', {month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'});
 } catch {
  return '';
 }
}

export {studentLabel, timestampMillis, rosterClassId};
