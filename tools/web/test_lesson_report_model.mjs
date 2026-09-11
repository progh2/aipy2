/* 함께 풀기·수업 리포트 순수 함수 검사. node tools/web/test_lesson_report_model.mjs */
import {
 TOGETHER_TITLE, REPORT_TITLE, isQuestionAnchor, choiceQuestions, questionPage,
 focusFromQuestion, choiceValue, collectChoices, collectChoicesFromStates, choiceBars,
 appendTrail, readTrail, classCompletion, snapshotBaseline, formatRateDelta,
 topicsCovered, topHardTopics, missingSubmitters, buildLessonReport, TRAIL_KEY_PREFIX
} from '../../web/assets/lesson-report-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(TOGETHER_TITLE, '함께 풀기', 'together title');
eq(REPORT_TITLE, '수업 리포트', 'report title');
eq(isQuestionAnchor('u1-q001'), true, 'question anchor');
eq(isQuestionAnchor('overview'), false, 'topic not question');

const catalog = {
 questions: [
  {id: 'u1-q001', unit: 1, kind: '선택', prompt: '모듈?', topic: 'overview', options: ['A', 'B', 'C'], answer: 'B'},
  {id: 'u1-q002', unit: 1, kind: '빈칸', prompt: '파일', options: []},
  {id: 'u2-q001', unit: 2, kind: '선택', prompt: '위젯?', topic: 'ui', options: ['X', 'Y'], answer: 'X'}
 ]
};
eq(choiceQuestions(catalog).map((q) => q.id), ['u1-q001', 'u2-q001'], 'choice filter');
eq(choiceQuestions(catalog, {unit: 1}).map((q) => q.id), ['u1-q001'], 'choice unit');
eq(questionPage(catalog.questions[0]), 'units/unit01/index.html', 'question page');
eq(focusFromQuestion(catalog.questions[0]), {
 page: 'units/unit01/index.html', topicAnchor: 'u1-q001', exampleId: null
}, 'question focus');

eq(choiceValue({choice: 'B'}), 'B', 'choice field');
eq(choiceValue({value: 'C'}), 'C', 'value field');
eq(collectChoices([
 {counts: {answers: {'u1-q001': {choice: 'A'}}}},
 {counts: {answers: {'u1-q001': {choice: 'B'}}}},
 {counts: {answers: {'u1-q001': {}}}}
], 'u1-q001'), ['A', 'B', ''], 'collect progress');
eq(collectChoicesFromStates([
 {answers: {'u1-q001': {value: 'C'}}},
 {answers: {}}
], 'u1-q001'), ['C', ''], 'collect state');

const bars = choiceBars(catalog.questions[0], ['A', 'A', 'B', '', 'Z']);
eq(bars.answered, 4, 'answered');
eq(bars.blank, 1, 'blank');
eq(bars.other, 1, 'other');
eq(bars.bars[0].count, 2, 'A count');
eq(bars.bars[0].crowd, true, 'wrong crowd');
eq(bars.bars[1].correct, true, 'correct B');
eq(bars.bars.find((row) => row.label === 'A').label.includes('홍'), false, 'no names');

const store = new Map();
const storage = {
 getItem: (key) => (store.has(key) ? store.get(key) : null),
 setItem: (key, value) => { store.set(key, String(value)); }
};
appendTrail(storage, '2-3', {page: 'units/unit01/index.html', topicAnchor: 'overview'}, 10);
appendTrail(storage, '2-3', {page: 'units/unit01/index.html', topicAnchor: 'overview'}, 11);
appendTrail(storage, '2-3', {page: 'units/unit01/index.html', topicAnchor: 'define'}, 12);
eq(readTrail(storage, '2-3').map((row) => row.topicAnchor), ['overview', 'define'], 'trail dedupe');
eq(store.get(`${TRAIL_KEY_PREFIX}2-3`) != null, true, 'trail stored');

const roster = [
 {email: 'a@e-mirim.hs.kr', name: '김가', studentId: '20301', grade: 2, classroom: 3},
 {email: 'b@e-mirim.hs.kr', name: '이나', studentId: '20302', grade: 2, classroom: 3}
];
const progress = [
 {email: 'a@e-mirim.hs.kr', grade: 2, classroom: 3, counts: {done: ['u1-overview']}, understanding: {'u1-overview': 'hard', 'u1-define': 'hard'}},
 {email: 'b@e-mirim.hs.kr', grade: 2, classroom: 3, counts: {done: ['u1-overview', 'u1-define']}, understanding: {'u1-overview': 'hard'}}
];
const completion = classCompletion({roster, progress, classId: '2-3', topicTotal: 2});
eq(completion.done, 3, 'done sum');
eq(completion.students, 2, 'students');
eq(completion.rate, 0.75, 'rate');
eq(snapshotBaseline(completion, 99).rate, 0.75, 'baseline');
eq(formatRateDelta(0.5, 0.75).includes('시작 50%'), true, 'delta');
eq(formatRateDelta(null, 0.4), '지금 40%', 'no baseline');

eq(topicsCovered({
 trail: [{topicAnchor: 'overview', page: 'units/unit01/index.html'}],
 focus: {topicAnchor: 'u1-q001', page: 'units/unit01/index.html'},
 presence: [{topicAnchor: 'define', page: 'units/unit01/index.html'}],
 titles: {'u1-overview': '모듈', 'u1-define': '정의'}
}).map((row) => row.id), ['u1-overview', 'u1-define'], 'topics skip question');
eq(topHardTopics(progress, {'u1-overview': '모듈', 'u1-define': '정의'})[0], {topicId: 'u1-overview', title: '모듈', count: 2}, 'hard top');
eq(missingSubmitters({
 roster, classId: '2-3', submissions: [{email: 'a@e-mirim.hs.kr'}]
}).map((row) => row.studentId), ['20302'], 'missing');

const report = buildLessonReport({
 classId: '2-3',
 session: {startedAt: 1, focus: {topicAnchor: 'overview', page: 'units/unit01/index.html'}, baseline: {rate: 0.5}},
 roster,
 progress,
 help: [{status: 'open', name: '이나', studentId: '20302', createdAt: 1}],
 presence: [],
 trail: [{topicAnchor: 'define', page: 'units/unit01/index.html'}],
 titles: {'u1-overview': '모듈', 'u1-define': '정의'},
 topicTotal: 2,
 assignment: {title: '모듈 과제'},
 submissions: [{email: 'a@e-mirim.hs.kr'}]
});
eq(report.classLabel, '2학년 3반', 'class label');
eq(report.hardTop[0].count, 2, 'report hard');
eq(report.openHelpCount, 1, 'open help');
eq(report.missingCount, 1, 'missing count');
eq(report.topics.length >= 1, true, 'topics present');
eq(JSON.stringify(report).includes('이나') && report.missing[0].label.includes('이나'), true, 'names only on missing list');

console.log('PASS: lesson-report-model helpers');
