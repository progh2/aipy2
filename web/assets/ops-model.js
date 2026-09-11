/* 입학년도(코호트) 운영. 진급은 grade·classroom만 바꾸고 admissionYear는 유지합니다.
   졸업 정리는 roster에 보관 표시하거나 명단 한 줄만 지웁니다. 학습 기록은 지우지 않습니다. */
import {isArchived} from './class-picker.js';

export {isArchived};

export const COHORT_CSV_HEADER = ['email', 'studentId', 'admissionYear', 'name', 'grade', 'classroom', 'number', 'archived'];
export const PROMOTE_NOTE = '입학년도는 그대로 둡니다. 학년·반만 바뀌고 이전 학습 기록이 이어집니다.';
export const ARCHIVE_NOTE = '보관하면 수업 반 목록에서만 빠집니다. 학습 기록·제출물은 지우지 않습니다.';
export const REMOVE_NOTE = '명단에서 제거하면 roster 한 줄만 지웁니다. 학습 기록은 남습니다.';
export const LEARNING_KEEP_NOTE = '학습 기록·제출물·이해도 신호는 일괄 삭제하지 않습니다.';
export const CONFIRM_ARCHIVE_PREFIX = '졸업';
export const CONFIRM_REMOVE_PREFIX = '명단삭제';
export const BATCH_LIMIT = 400;

export function asInt(value) {
 if (value == null || value === '') return null;
 const parsed = Number(value);
 return Number.isInteger(parsed) ? parsed : null;
}

export function emailKey(row) {
 return String((row && (row.email || row.id)) || '').trim().toLowerCase();
}

export function isActiveRoster(row) {
 return Boolean(row) && !isArchived(row);
}

export function admissionYearOf(row) {
 return asInt(row && row.admissionYear);
}

export function cohortYears(rows) {
 const years = new Set();
 for (const row of rows || []) {
  const year = admissionYearOf(row);
  if (year != null) years.add(year);
 }
 return [...years].sort((a, b) => b - a);
}

export function filterCohort(rows, year, {includeArchived = true, classId = ''} = {}) {
 const want = asInt(year);
 if (want == null) return [];
 return (rows || []).filter((row) => {
  if (admissionYearOf(row) !== want) return false;
  if (!includeArchived && isArchived(row)) return false;
  if (classId) {
   const id = `${row.grade}-${row.classroom}`;
   if (id !== classId) return false;
  }
  return true;
 });
}

export function sortCohort(rows) {
 return (rows || []).slice().sort((a, b) =>
  (Number(a.grade) - Number(b.grade)) ||
  (Number(a.classroom) - Number(b.classroom)) ||
  String(a.studentId || '').localeCompare(String(b.studentId || ''), 'ko') ||
  emailKey(a).localeCompare(emailKey(b)));
}

export function parsePromoteTarget({grade, classroom} = {}) {
 const nextGrade = asInt(grade);
 const nextClass = asInt(classroom);
 const problems = [];
 if (nextGrade == null) problems.push('학년은 정수여야 함');
 else if (nextGrade < 1 || nextGrade > 3) problems.push('학년은 1–3이어야 함');
 if (nextClass == null) problems.push('반은 정수여야 함');
 else if (nextClass < 1 || nextClass > 20) problems.push('반은 1–20이어야 함');
 return {grade: nextGrade, classroom: nextClass, problems};
}

export function promotePreview(rows, target) {
 const parsed = parsePromoteTarget(target);
 const list = sortCohort(rows);
 return {
  ...parsed,
  rows: list.map((row) => ({
   email: emailKey(row),
   studentId: row.studentId || '',
   name: row.name || '',
   admissionYear: admissionYearOf(row),
   fromGrade: asInt(row.grade),
   fromClassroom: asInt(row.classroom),
   toGrade: parsed.grade,
   toClassroom: parsed.classroom,
   unchangedYear: admissionYearOf(row),
   same: asInt(row.grade) === parsed.grade && asInt(row.classroom) === parsed.classroom,
   archived: isArchived(row)
  }))
 };
}

export function rosterWriteFields(row, patch = {}) {
 const email = emailKey(row);
 const payload = {
  email,
  studentId: String(row.studentId ?? ''),
  admissionYear: admissionYearOf(row),
  name: row.name || '',
  grade: patch.grade != null ? patch.grade : asInt(row.grade),
  classroom: patch.classroom != null ? patch.classroom : asInt(row.classroom)
 };
 if ((patch.number != null ? patch.number : row.number) != null) {
  payload.number = patch.number != null ? patch.number : row.number;
 }
 if (isArchived(row) || patch.archived === true) payload.archived = true;
 if (row.archivedAt) payload.archivedAt = row.archivedAt;
 if (patch.archived === false) {
  delete payload.archived;
  delete payload.archivedAt;
 }
 return payload;
}

export function identityPatch(target) {
 const parsed = parsePromoteTarget(target);
 return {grade: parsed.grade, classroom: parsed.classroom};
}

export function archivePhrase(year) {
 return `${CONFIRM_ARCHIVE_PREFIX} ${asInt(year)}`;
}

export function removePhrase(year) {
 return `${CONFIRM_REMOVE_PREFIX} ${asInt(year)}`;
}

export function phraseMatches(typed, expected) {
 return String(typed || '').trim() === String(expected || '').trim();
}

export function csvCell(value) {
 const text = value == null ? '' : String(value);
 if (/[",\n]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
 return text;
}

export function cohortCsv(rows) {
 const body = sortCohort(rows).map((row) => [
  emailKey(row),
  row.studentId ?? '',
  admissionYearOf(row) ?? '',
  row.name || '',
  row.grade ?? '',
  row.classroom ?? '',
  row.number ?? '',
  isArchived(row) ? '1' : ''
 ].map(csvCell).join(','));
 return ['\ufeff' + COHORT_CSV_HEADER.join(','), ...body].join('\n') + '\n';
}

export function matchByEmail(docs, email) {
 const key = String(email || '').toLowerCase();
 if (!key) return null;
 return (docs || []).find((doc) => emailKey(doc) === key) || null;
}

export function chunkWrites(items, limit = BATCH_LIMIT) {
 const size = Math.max(1, Number(limit) || BATCH_LIMIT);
 const chunks = [];
 for (let i = 0; i < (items || []).length; i += size) chunks.push(items.slice(i, i + size));
 return chunks;
}

export function countPromoteWrites(preview, students = [], progress = []) {
 let n = 0;
 for (const row of preview.rows || []) {
  if (row.archived || row.same) continue;
  n += 1;
  if (matchByEmail(students, row.email)) n += 1;
  if (matchByEmail(progress, row.email)) n += 1;
 }
 return n;
}
