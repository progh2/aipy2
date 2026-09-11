/* 이해도 신호 순수 함수 검사. node tools/web/test_understanding_model.mjs */
import {
 UNDERSTANDING_KEY, UNDERSTANDING_WRITE_MS, COMMENT_MAX, UNDERSTANDING_LABELS,
 HARD_PROMPT, NOT_GRADED, STUDENT_NOTE, TEACHER_NOTE, normalizeUnderstanding, normalizeStore, mergeUnderstanding,
 mergeStores, setUnderstanding, setComment, clipComment, historyItems, topicHref,
 titlesFromCatalog, titlesFromLessons, topicTitle, studentLabel, countUnderstanding,
 groupHardByTopic, shouldWriteAfter, feedbackId, feedbackFields, isTopicId
} from '../../web/assets/understanding-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(UNDERSTANDING_KEY, 'aipy-understanding-v1', 'storage key');
eq(UNDERSTANDING_WRITE_MS >= 500 && UNDERSTANDING_WRITE_MS <= 2000, true, 'write debounce');
eq(UNDERSTANDING_LABELS.understood, '이해했어요', 'label ok');
eq(UNDERSTANDING_LABELS.somewhat, '조금 어려워요', 'label mid');
eq(UNDERSTANDING_LABELS.hard, '어려워요', 'label hard');
eq(HARD_PROMPT, '어디가 막혔나요?', 'hard prompt');
eq(STUDENT_NOTE, '이해도·도움 요청은 성적에 안 들어가요. 수업 중에만 쓰는 신호예요.', 'student note');
eq(TEACHER_NOTE, '학생이 보내는 신호예요. 점수·출결에는 안 반영돼요.', 'teacher note');
eq(NOT_GRADED, STUDENT_NOTE, 'not graded alias');
eq(isTopicId('u1-overview'), true, 'topic id');
eq(isTopicId('overview'), false, 'bare topic rejected');
eq(normalizeUnderstanding({
 'u1-overview': 'hard',
 'u2-hello': 'ok',
 skip: 'hard',
 'u3-ml': 'somewhat'
}), {'u1-overview': 'hard', 'u3-ml': 'somewhat'}, 'normalize drops invalid');

eq(clipComment('  어디가   막혔나요  '), '어디가 막혔나요', 'comment trim');
eq(clipComment('가'.repeat(COMMENT_MAX + 20)).length, COMMENT_MAX, 'comment max');

const store = setComment(setUnderstanding({}, 'u1-overview', 'hard'), 'u1-overview', 'import가 헷갈려요');
eq(store.values['u1-overview'], 'hard', 'set value');
eq(store.comments['u1-overview'], 'import가 헷갈려요', 'set comment');

eq(mergeUnderstanding({'u1-overview': 'hard'}, {'u1-overview': 'understood', 'u1-define': 'somewhat'}),
 {'u1-overview': 'hard', 'u1-define': 'somewhat'}, 'local wins merge');
const merged = mergeStores(
 {values: {'u1-overview': 'hard'}, comments: {'u1-overview': '로컬'}},
 {values: {'u1-overview': 'understood', 'u2-hello': 'somewhat'}, comments: {'u2-hello': '클라우드'}}
);
eq(merged.values['u1-overview'], 'hard', 'store local value');
eq(merged.values['u2-hello'], 'somewhat', 'store cloud fill');
eq(merged.comments['u1-overview'], '로컬', 'store local comment');
eq(merged.comments['u2-hello'], '클라우드', 'store cloud comment');

eq(historyItems({'u1-overview': 'hard', 'u1-define': 'understood', 'u2-hello': 'somewhat'}).map((i) => i.topicId),
 ['u1-overview', 'u2-hello'], 'history skips understood');
eq(topicHref('../../', 'u2-hello'), '../../units/unit02/index.html#hello', 'topic href');

const catalog = {topics: {'units/unit01/index.html': [{id: 'overview', title: '모듈이 필요한 이유'}]}};
eq(titlesFromCatalog(catalog)['u1-overview'], '모듈이 필요한 이유', 'catalog title');
eq(titlesFromLessons([{id: 'overview', title: '개요'}], 1)['u1-overview'], '개요', 'lesson title');
eq(topicTitle('u1-overview', {'u1-overview': '개요'}), '개요', 'title lookup');
eq(studentLabel({studentId: '20314', name: '홍길동'}), '20314 홍길동', 'student label');

const counted = countUnderstanding([
 {uid: 'a', studentId: '20314', name: '홍길동', understanding: {'u1-overview': 'hard', 'u1-define': 'understood'}},
 {uid: 'b', studentId: '20315', name: '김서연', understanding: {'u1-overview': 'hard'}}
]);
eq(counted.counts, {understood: 1, somewhat: 0, hard: 2}, 'counts');
eq(counted.hardRows.length, 2, 'hard rows');
eq(groupHardByTopic(counted.hardRows)[0][0], 'u1-overview', 'group hard topic');
eq(groupHardByTopic(counted.hardRows)[0][1].length, 2, 'group hard count');

eq(shouldWriteAfter(0, 1000), true, 'first write');
eq(shouldWriteAfter(1000, 1000 + UNDERSTANDING_WRITE_MS - 1), false, 'inside debounce');
eq(shouldWriteAfter(1000, 1000 + UNDERSTANDING_WRITE_MS), true, 'after debounce');
eq(feedbackId('uid1', 'u1-overview'), 'uid1_u1-overview', 'feedback id');
eq(feedbackFields({profile: {uid: 'u', email: 'a@e-mirim.hs.kr', name: '홍'}, topicId: 'u1-overview', text: '막힘'}).text, '막힘', 'feedback text');
eq(normalizeStore(null).values, {}, 'empty store');

console.log('PASS: understanding-model helpers');
