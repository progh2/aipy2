/* 참여 현황 보드 순수 함수 검사. node tools/web/test_board_model.mjs */
import {
 topicListFromCatalog, completedTopicIds, completeRate, studentAccuracy, formatRate,
 presenceFreshness, currentPlace, worstUnderstanding, understandingSummary,
 heatmapTone, isStuckOnTopic, filterStuck, buildStudentCards, sortStudentCards,
 classQuestionTotals, questionStats, csvCell, classCsv, cardAccuracyLabel,
 answerRows, filterAnswerRows, groupAnswerRowsByUnit, unitAnswerTotals, journalRows,
 formatAnswerValue, answerStatusLabel, isSubjectiveKind,
 PRESENCE_FRESH_MS, PRESENCE_RECENT_MS, CSV_HEADER
} from '../../web/assets/board-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const catalog = {
 topics: {
  'units/unit01/index.html': [
   {id: 'overview', title: '모듈이 필요한 이유'},
   {id: 'define', title: '모듈 정의'}
  ],
  'units/unit02/index.html': [{id: 'ui', title: 'GUI 시작'}]
 }
};
const topics = topicListFromCatalog(catalog);
eq(topics.map((t) => t.id), ['u1-overview', 'u1-define', 'u2-ui'], 'topic ids');
eq(topics[0].short, '1.1', 'topic short');
eq(topics[0].title, '모듈이 필요한 이유', 'topic title');

eq(completedTopicIds({done: ['u1-overview', 'skip', 'u2-ui']}), ['u1-overview', 'u2-ui'], 'done filter');
eq(completedTopicIds({}), [], 'done missing');
eq(completeRate(1, 4), 0.25, 'complete rate');
eq(completeRate(9, 4), 1, 'complete rate cap');
eq(completeRate(0, 0), 0, 'complete rate empty');

eq(studentAccuracy({
 answers: {'u1-q001': {attempts: 2, correct: 1}, 'u1-q002': {attempts: 3, correct: 0}}
}), {correct: 1, attempted: 2, attempts: 5, rate: 0.5}, 'accuracy from answers');
eq(studentAccuracy({questions: {attempts: 5, correct: 2}}), {correct: 2, attempted: 0, attempts: 5, rate: null}, 'accuracy fallback');
eq(formatRate(0.5), '50%', 'format rate');
eq(formatRate(null), '—', 'format rate empty');

const now = 1_700_000_000_000;
eq(presenceFreshness(now - 10_000, now).label, '1분 이내', 'fresh 1 min');
eq(presenceFreshness(now - 10_000, now).online, true, 'fresh online');
eq(presenceFreshness(now - PRESENCE_FRESH_MS - 1, now).label, '3분 이내', 'fresh 3 min');
eq(presenceFreshness(now - PRESENCE_RECENT_MS - 1, now).online, false, 'stale offline');
eq(presenceFreshness(null, now).label, '오프라인', 'no presence');
eq(PRESENCE_FRESH_MS >= 60_000 && PRESENCE_RECENT_MS >= 120_000, true, 'freshness windows');

eq(currentPlace({page: 'units/unit01/index.html', topicAnchor: 'overview'}, {'u1-overview': '모듈이 필요한 이유'}),
 'Ⅰ · 모듈이 필요한 이유', 'current place');
eq(worstUnderstanding({'u1-overview': 'understood', 'u1-define': 'hard'}), 'hard', 'worst hard');
eq(understandingSummary({'u1-overview': 'hard', 'u1-define': 'somewhat'}), '어려워요 1 · 조금 어려워요 1', 'summary');
eq(heatmapTone(true, 'hard'), 'hard', 'tone hard wins');
eq(heatmapTone(true, ''), 'done', 'tone done');
eq(heatmapTone(false, ''), 'empty', 'tone empty');
eq(heatmapTone(true, 'understood'), 'understood', 'tone understood');

const cards = buildStudentCards({
 classId: '2-3',
 topics,
 titles: {'u1-overview': '모듈이 필요한 이유'},
 now,
 roster: [
  {email: 'a@e-mirim.hs.kr', studentId: '20314', name: '홍길동', grade: 2, classroom: 3, number: 14},
  {email: 'b@e-mirim.hs.kr', studentId: '20301', name: '김서연', grade: 2, classroom: 3, number: 1},
  {email: 'c@e-mirim.hs.kr', studentId: '20401', name: '다른반', grade: 2, classroom: 4, number: 1}
 ],
 progress: [
  {
   id: 'uid-a', uid: 'uid-a', email: 'a@e-mirim.hs.kr', studentId: '20314', name: '홍길동',
   grade: 2, classroom: 3, number: 14,
   counts: {done: ['u1-overview'], questions: {attempts: 2, correct: 1}, answers: {'u1-q001': {attempts: 2, correct: 1}}, lastActivity: now - 1000},
   understanding: {'u1-overview': 'hard'}
  },
  {
   id: 'uid-d', uid: 'uid-d', email: 'd@e-mirim.hs.kr', studentId: '20320', name: '박민수',
   grade: 2, classroom: 3, number: 20,
   counts: {done: ['u1-overview', 'u1-define', 'u2-ui'], questions: {attempts: 0, correct: 0}, lastActivity: now}
  }
 ],
 presence: [
  {id: 'uid-a', uid: 'uid-a', classroom: '2-3', page: 'units/unit01/index.html', topicAnchor: 'overview', updatedAt: now - 5000}
 ],
 help: [
  {id: 'h1', uid: 'uid-a', studentId: '20314', name: '홍길동', status: 'open', createdAt: now - 8000, topic: 'u1-overview'}
 ]
});
eq(cards.length, 3, 'class cards only');
eq(buildStudentCards({
 classId: '2-3', topics, now,
 roster: [
  {email: 'a@e-mirim.hs.kr', studentId: '20314', name: '홍길동', grade: 2, classroom: 3},
  {email: 'z@e-mirim.hs.kr', studentId: '20399', name: '보관', grade: 2, classroom: 3, archived: true}
 ]
}).map((c) => c.name), ['홍길동'], 'archived roster omitted');
const byName = Object.fromEntries(cards.map((c) => [c.name, c]));
eq(byName['홍길동'].openHelp, 1, 'help on card');
eq(byName['홍길동'].online, true, 'presence online');
eq(byName['홍길동'].place, 'Ⅰ · 모듈이 필요한 이유', 'card place');
eq(byName['홍길동'].understandingLabel, '어려워요', 'card understanding');
eq(byName['김서연'].online, false, 'roster only offline');
eq(byName['박민수'].doneCount, 3, 'progress-only card');
eq(byName['홍길동'].completeRate, completeRate(1, 3), 'hong complete rate');

// 명단에서 2-3 → 2-4로 반을 옮긴 학생(#123). progress 문서의 classroom 필드는 다음 활동 전까지
// 옛 반(3)을 그대로 갖고 있을 수 있다 — 반 판정은 명단(roster)의 현재 반으로 해야
// 새 반에 진행률과 함께 나오고, 옛 반에는 유령 카드로 남지 않는다.
const movedRoster = [
 {email: 'e@e-mirim.hs.kr', studentId: '20415', name: '이동학생', grade: 2, classroom: 4, number: 5}
];
const movedProgress = [
 {
  id: 'uid-e', uid: 'uid-e', email: 'e@e-mirim.hs.kr', studentId: '20415', name: '이동학생',
  grade: 2, classroom: 3, number: 15,
  counts: {done: ['u1-overview'], lastActivity: now}
 }
];
const movedNewClassCards = buildStudentCards({classId: '2-4', topics, now, roster: movedRoster, progress: movedProgress});
eq(movedNewClassCards.length, 1, 'moved student appears in new class');
eq(movedNewClassCards[0].doneCount, 1, 'moved student progress carried over to new class');
const movedOldClassCards = buildStudentCards({classId: '2-3', topics, now, roster: movedRoster, progress: movedProgress});
eq(movedOldClassCards.length, 0, 'moved student does not ghost in old class');

const sorted = sortStudentCards(cards);
eq(sorted.map((c) => c.name), ['김서연', '홍길동', '박민수'], 'student id order');

const noHelp = sortStudentCards(cards.map((c) => ({...c, openHelp: 0})));
eq(noHelp.map((c) => c.name), ['김서연', '홍길동', '박민수'], 'student id order regardless of help');

eq(isStuckOnTopic(byName['홍길동'], 'u1-overview'), true, 'hard is stuck');
eq(isStuckOnTopic(byName['박민수'], 'u1-overview'), false, 'done not stuck');
eq(filterStuck(cards, 'u1-define').map((c) => c.name).sort(), ['김서연', '홍길동'], 'filter stuck define');

const totals = classQuestionTotals(cards.map((c) => ({counts: c.name === '홍길동' ? {questions: {attempts: 2, correct: 1}} : {questions: {attempts: 0, correct: 0}}})));
eq(totals.attempts, 2, 'class attempts');
eq(totals.correct, 1, 'class correct');

const stats = questionStats([
 {counts: {answers: {'u1-q001': {attempts: 2, correct: 1}}}},
 {counts: {answers: {'u1-q001': {attempts: 4, correct: 0}, 'u1-q002': {attempts: 1, correct: 1}}}}
], [{id: 'u1-q001', unit: 1, topic: 'overview'}, {id: 'u1-q002', unit: 1, topic: 'overview'}]);
eq(stats[0].id, 'u1-q001', 'low rate first');
eq(stats[0].attempts, 6, 'q1 attempts');
eq(stats[0].correct, 1, 'q1 correct');
eq(stats[0].students, 2, 'q1 students');
eq(stats[0].correctRate, 0.5, 'q1 rate');
eq(stats[0].avgAttempts, 3, 'q1 avg');

eq(csvCell('a,b'), '"a,b"', 'csv quote');
eq(CSV_HEADER.includes('완료율'), true, 'csv header');
const csv = classCsv(sorted);
eq(csv.split('\n')[0], CSV_HEADER.join(','), 'csv first line');
eq(csv.includes('홍길동'), true, 'csv name');
eq(csv.includes('어려워요 1'), true, 'csv understanding');
eq(cardAccuracyLabel(byName['홍길동']), '100%', 'card accuracy label');

// 학생 상세 패널 — 답안 보기(#101)
const questions = [
 {id: 'u1-q001', unit: 1, topic: '기초 개념', kind: '선택', prompt: '모듈에 대한 설명으로 틀린 것을 고르세요.', options: ['a', 'b'], answer: 'b'},
 {id: 'u1-q002', unit: 1, topic: '기초 개념', kind: '빈칸', prompt: '함수·변수·클래스 등을 담은 Python 파일은?', answer: '모듈'},
 {id: 'u2-q010', unit: 2, topic: 'GUI', kind: '서술', prompt: 'tkinter로 창을 띄우는 과정을 서술하세요.'}
];
const detailState = {
 answers: {
  'u1-q001': {value: 'a', status: 'retry', attempts: 2},
  'u1-q002': {value: '모듈', status: 'done', attempts: 1},
  'u2-q010': {value: ['a', 'b', 'c'], status: 'retry', attempts: 1}
 },
 journals: {'u1-learn': ' 모듈 개념을 배웠다 ', 'u1-error': '', 'u2-next': 'GUI 이벤트 처리 도전'}
};
const rows = answerRows(detailState, questions);
eq(rows.length, 3, 'answer rows count');
eq(rows.map((r) => r.id), ['u1-q001', 'u1-q002', 'u2-q010'], 'answer rows sorted by unit');
eq(rows[0].topic, '기초 개념', 'answer row topic from catalog');
eq(rows[0].correctAnswer, 'b', 'answer row correct answer');

eq(formatAnswerValue(['a', 'b', 'c']), 'a → b → c', 'format array answer');
eq(formatAnswerValue('모듈'), '모듈', 'format string answer');
eq(formatAnswerValue(null), '', 'format empty answer');

eq(answerStatusLabel({status: 'done'}), '정답', 'answer status done');
eq(answerStatusLabel({status: 'retry'}), '다시 풀기', 'answer status retry');
eq(answerStatusLabel({value: '모듈'}), '제출', 'answer status submitted unknown');
eq(answerStatusLabel({value: ''}), '미제출', 'answer status empty');

eq(isSubjectiveKind('서술'), true, 'subjective kind narrative');
eq(isSubjectiveKind('선택'), false, 'objective kind choice');

eq(filterAnswerRows(rows, 'retry').map((r) => r.id), ['u1-q001', 'u2-q010'], 'filter retry only');
eq(filterAnswerRows(rows, 'subjective').map((r) => r.id), ['u1-q002', 'u2-q010'], 'filter subjective only');
eq(filterAnswerRows(rows, 'all').length, 3, 'filter all');

const grouped = groupAnswerRowsByUnit(rows);
eq(grouped.map(([unit]) => unit), [1, 2], 'grouped by unit');
eq(grouped[0][1].length, 2, 'unit1 group size');

const unitTotals = unitAnswerTotals(detailState, questions);
eq(unitTotals, [{unit: 1, total: 2, answered: 2, correct: 1}, {unit: 2, total: 1, answered: 1, correct: 0}], 'unit answer totals');

const journals = journalRows(detailState);
eq(journals.length, 2, 'journal rows by unit');
eq(journals[0], {unit: 1, items: [{key: 'learn', label: '이해한 개념', text: '모듈 개념을 배웠다'}]}, 'journal unit1 trims and skips empty');
eq(journals[1].items[0].label, '다음 도전', 'journal unit2 label');

eq(answerRows({}, questions), [], 'answer rows empty state');
eq(unitAnswerTotals({}, questions), [{unit: 1, total: 2, answered: 0, correct: 0}, {unit: 2, total: 1, answered: 0, correct: 0}], 'unit totals no answers');
eq(journalRows({}), [], 'journal rows empty state');

console.log('PASS: board-model helpers');
