/* 입학년도 운영 순수 함수 검사. node tools/web/test_ops_model.mjs */
import {
 cohortYears, filterCohort, sortCohort, promotePreview, parsePromoteTarget,
 rosterWriteFields, identityPatch, archivePhrase, removePhrase, phraseMatches,
 cohortCsv, matchByEmail, chunkWrites, countPromoteWrites, isActiveRoster, emailKey,
 PROMOTE_NOTE, ARCHIVE_NOTE, REMOVE_NOTE, LEARNING_KEEP_NOTE
} from '../../web/assets/ops-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const rows = [
 {email: 'a@e-mirim.hs.kr', studentId: '20314', admissionYear: 2025, name: '홍길동', grade: 2, classroom: 3, number: 14},
 {email: 'b@e-mirim.hs.kr', studentId: '20315', admissionYear: 2025, name: '김서연', grade: 2, classroom: 4},
 {email: 'c@e-mirim.hs.kr', studentId: '19301', admissionYear: 2024, name: '졸업생', grade: 3, classroom: 1, archived: true},
 {email: 'd@e-mirim.hs.kr', studentId: '19302', admissionYear: 2024, name: '재학', grade: 3, classroom: 2}
];

eq(PROMOTE_NOTE, '입학년도는 그대로예요. 학년·반만 바뀌고 이전 학습 기록이 이어져요.', 'promote note');
eq(ARCHIVE_NOTE, '보관하면 수업 반 목록에서만 빠져요. 학습 기록·제출물은 지우지 않아요.', 'archive note');
eq(REMOVE_NOTE, '명단 한 줄만 지워요. 학습 기록은 남아요.', 'remove note');
eq(LEARNING_KEEP_NOTE, '학습 기록·제출물·이해도 신호는 한꺼번에 지우지 않아요.', 'keep note');

eq(cohortYears(rows), [2025, 2024], 'cohortYears desc');
eq(filterCohort(rows, 2025).map(emailKey), ['a@e-mirim.hs.kr', 'b@e-mirim.hs.kr'], 'filter year');
eq(filterCohort(rows, 2024, {includeArchived: false}).map((r) => r.name), ['재학'], 'hide archived');
eq(filterCohort(rows, 2025, {classId: '2-3'}).map((r) => r.name), ['홍길동'], 'filter class');
eq(sortCohort(filterCohort(rows, 2025)).map((r) => r.studentId), ['20314', '20315'], 'sort');
eq(isActiveRoster(rows[2]), false, 'archived not active');
eq(isActiveRoster(rows[0]), true, 'active');

eq(parsePromoteTarget({grade: '3', classroom: '1'}), {grade: 3, classroom: 1, problems: []}, 'parse promote');
eq(parsePromoteTarget({grade: 4, classroom: 1}).problems.length > 0, true, 'grade range');

const preview = promotePreview(filterCohort(rows, 2025), {grade: 3, classroom: 1});
eq(preview.problems, [], 'preview ok');
eq(preview.rows[0].admissionYear, 2025, 'keep admissionYear');
eq(preview.rows[0].unchangedYear, 2025, 'unchanged year field');
eq(preview.rows[0].toGrade, 3, 'new grade');
eq(preview.rows.every((r) => r.admissionYear === 2025), true, 'all years kept');

const payload = rosterWriteFields(rows[0], {grade: 3, classroom: 1});
eq(payload.admissionYear, 2025, 'roster write keeps year');
eq(payload.grade, 3, 'roster write grade');
eq(payload.classroom, 1, 'roster write class');
eq(payload.email, 'a@e-mirim.hs.kr', 'roster write email');
eq('archived' in payload, false, 'active row has no archived flag');

const archivedWrite = rosterWriteFields(rows[2], {grade: 3, classroom: 1});
eq(archivedWrite.archived, true, 'preserve archived');
eq(archivedWrite.admissionYear, 2024, 'archived keep year');

eq(identityPatch({grade: 3, classroom: 2}), {grade: 3, classroom: 2}, 'identity patch');
eq(archivePhrase(2024), '졸업 2024', 'archive phrase');
eq(removePhrase(2024), '명단삭제 2024', 'remove phrase');
eq(phraseMatches('졸업 2024', archivePhrase(2024)), true, 'phrase match');
eq(phraseMatches('졸업2024', archivePhrase(2024)), false, 'phrase reject');

const csv = cohortCsv(filterCohort(rows, 2024));
if (!csv.includes('email,studentId,admissionYear')) throw new Error('csv header');
if (!csv.includes('c@e-mirim.hs.kr')) throw new Error('csv archived row');
if (!csv.includes(',1\n') && !csv.includes(',1\r')) {
 if (!/,1\n/.test(csv) && !csv.split('\n').some((line) => line.endsWith(',1'))) {
  // archived flag column is last; 졸업생 row should mark 1
 }
}
if (!csv.split('\n').some((line) => line.includes('졸업생') && line.endsWith(',1'))) {
 throw new Error(`csv archived flag: ${csv}`);
}

const students = [{id: 'uid-a', email: 'a@e-mirim.hs.kr'}];
const progress = [{id: 'uid-a', email: 'A@e-mirim.hs.kr'}];
eq(matchByEmail(students, 'a@e-mirim.hs.kr').id, 'uid-a', 'match student');
eq(matchByEmail(progress, 'a@e-mirim.hs.kr').id, 'uid-a', 'match progress case');
eq(countPromoteWrites(preview, students, progress), 4, 'writes: 2 roster + 1 student + 1 progress');
eq(chunkWrites([1, 2, 3, 4], 2), [[1, 2], [3, 4]], 'chunk');

console.log('PASS: ops-model helpers');
