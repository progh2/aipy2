/* 교사용 반별 입력 현황 집계 검사. node tools/web/test_teacher_progress.mjs */
import {buildClassProgress, cellLevel, subunitStats, missingStudents, progressCsv, missingCsv, countable} from '../../web/assets/teacher-progress-model.js';

function eq(actual, expected, label) {
 const l = JSON.stringify(actual), r = JSON.stringify(expected);
 if (l !== r) throw new Error(`${label}: ${l} !== ${r}`);
}
const catalog = {
 topics: {
  'units/unit01/index.html': [
   {id: 'overview', title: '개요', href: 'units/unit01/overview.html', practiceHref: 'x', tasks: [], examples: []},
   {id: 'define', title: '정의', href: 'units/unit01/define.html', practiceHref: 'y', tasks: [], examples: []}
  ],
  'units/unit02/index.html': [{id: 'ui', title: 'UI', href: 'units/unit02/ui.html', practiceHref: 'z', tasks: [], examples: []}]
 },
 examples: {},
 questions: [
  {id: 'u1-q1', unit: 1, topic: 'overview', kind: '선택', prompt: 'a', options: ['x', 'y'], answer: 'x'},
  {id: 'u1-q2', unit: 1, topic: 'overview', kind: '서술', prompt: 'b'}
 ]
};
// 1) 학생 0명
const none = buildClassProgress([], new Map(), catalog);
eq(none.students.length, 0, '학생 0명');
eq(none.units.map((u) => u.unit), [1, 2], '학생 0명이어도 단원 구조');
eq(subunitStats(none, 'u1-overview'), {n: 0, done: 0, journal: 0, donePct: 0, journalPct: 0}, '0명 통계');
eq(missingStudents(none, 'u1-overview'), [], '0명 명단');

// 2) 일부 저널
const cards = [{key: 'a', uid: 'a', label: '20301 가'}, {key: 'b', uid: 'b', label: '20302 나, "다"'}, {key: 'c', uid: 'c', label: '20303 다'}, {key: 'd', label: '20304 라'}];
const entries = new Map([
 ['a', {status: 'ready', data: {complete: {'u1-overview': true}, journals: {'j-u1-overview': '정리함'}, answers: {'u1-q1': {value: 'x', status: 'done', attempts: 1}, 'u1-q2': {value: '답', attempts: 1}}}}],
 ['b', {status: 'ready', data: {complete: {'u1-overview': true}}}],
 ['c', {status: 'error'}]
]);
const m = buildClassProgress(cards, entries, catalog);
eq(m.students.map((s) => s.status), ['ready', 'ready', 'error', 'nouid'], '상태');
eq(cellLevel(m.students[0].cells['u1-overview']), 'full', '다 함');
eq(cellLevel(m.students[1].cells['u1-overview']), 'part', '일부');
eq(cellLevel(m.students[1].cells['u1-define']), 'none', '안 함');
eq(cellLevel(m.students[1].cells['u1-overview'], 'journal'), 'none', '저널만 보기');
eq(cellLevel(m.students[1].cells['u1-overview'], 'done'), 'full', '완료만 보기');
eq(countable(m.students[2]), false, '오류는 집계 제외');
eq(subunitStats(m, 'u1-overview'), {n: 3, done: 2, journal: 1, donePct: 67, journalPct: 33}, '소단원 통계');
eq(missingStudents(m, 'u1-overview'), ['20302 나, "다"', '20304 라'], '저널 미작성');
eq(missingStudents(m, 'u1-overview', 'done'), ['20304 라'], '완료 미체크');

// 3) 단원 필터 CSV
const csv = progressCsv(m, 2).split('\r\n');
eq(csv[0], '학생,UI 완료,UI 문제,UI 저널,UI 직접'.replace(/UI/g, m.units[1].subunits[0].short || 'UI'), 'CSV 머리');
eq(csv.length, 5, 'CSV 행 수(머리+4명)');
eq(csv[2], '"20302 나, ""다""",X,0/0,X,-', 'CSV 쉼표·따옴표 이스케이프');
eq(progressCsv(m, 9), '', '없는 단원');
eq(missingCsv(m, 'u1-overview').split('\r\n').length, 3, '미작성 CSV');
console.log('test_teacher_progress OK');
