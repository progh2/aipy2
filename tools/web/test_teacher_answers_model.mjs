/* 답변 내역 페이지(#128) 순수 함수 검사. node tools/web/test_teacher_answers_model.mjs */
import {groupAnswerRowsBySubunit, studentSummaryLabel, hasAnswerRecord} from '../../web/assets/teacher-answers-model.js';
import {answerRows} from '../../web/assets/board-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const questions = [
 {id: 'u1-q001', unit: 1, topic: 'overview', kind: '선택', prompt: '문제1', options: ['a', 'b'], answer: 'a'},
 {id: 'u1-q002', unit: 1, topic: 'overview', kind: '서술', prompt: '문제2'},
 {id: 'u1-q003', unit: 1, topic: 'define', kind: '선택', prompt: '문제3', options: ['a', 'b'], answer: 'b'},
 {id: 'u2-q010', unit: 2, topic: 'ui', kind: '구현', prompt: '문제4'}
];
const state = {
 answers: {
  'u1-q001': {status: 'done', attempts: 1, value: 'a'},
  'u1-q002': {status: 'retry', attempts: 2, value: '내 답'},
  'u1-q003': {status: 'done', attempts: 1, value: 'b'},
  'u2-q010': {status: 'retry', attempts: 3, value: 'code'}
 }
};
const titles = {'u1-overview': '모듈이 필요한 이유', 'u1-define': '모듈 정의', 'u2-ui': 'GUI 시작'};

const rows = answerRows(state, questions);
const grouped = groupAnswerRowsBySubunit(rows, titles);
eq(grouped.map((g) => `${g.unit}::${g.topic}`), ['1::define', '1::overview', '2::ui'], 'grouped by unit+topic sorted');
const overviewGroup = grouped.find((g) => g.topic === 'overview');
eq(overviewGroup.rows.length, 2, 'overview subgroup has both questions');
eq(overviewGroup.topicTitle, '모듈이 필요한 이유', 'subgroup carries topic title');
const uiGroup = grouped.find((g) => g.topic === 'ui');
eq(uiGroup.topicTitle, 'GUI 시작', 'unit2 topic title resolved');

eq(groupAnswerRowsBySubunit([], titles), [], 'empty rows produce no groups');
eq(groupAnswerRowsBySubunit(rows, {}).find((g) => g.topic === 'overview').topicTitle, 'u1-overview', 'missing titles fall back to full topic id via topicTitle');

eq(studentSummaryLabel(null), '', 'no card no label');
eq(studentSummaryLabel({attempted: 4, correct: 3, doneCount: 5, topicTotal: 40}), '답변 4 · 정답 3 · 완료 5/40', 'summary label formats counts');
eq(studentSummaryLabel({}), '답변 0 · 정답 0 · 완료 0/0', 'summary label defaults missing fields to 0');

eq(hasAnswerRecord({}), false, 'empty state has no record');
eq(hasAnswerRecord({answers: {'u1-q001': {attempts: 0, value: ''}}}), false, 'blank value and zero attempts is not a record');
eq(hasAnswerRecord({answers: {'u1-q001': {attempts: 1, value: ''}}}), true, 'attempt without value still counts as a record');
eq(hasAnswerRecord({journals: {'u1-learn': '  '}}), false, 'blank journal text is not a record');
eq(hasAnswerRecord({journals: {'u1-learn': '개념 이해함'}}), true, 'non-blank journal text counts as a record');

console.log('PASS: teacher-answers-model helpers');
