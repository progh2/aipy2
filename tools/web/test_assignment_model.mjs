/* 과제·제출 순수 함수 검사. node tools/web/test_assignment_model.mjs */
import {
 SUBMIT_COOLDOWN_MS, OUTPUT_MAX, LABEL_FAILED, LABEL_LATE, LABEL_PASSED, LABEL_REVIEWED,
 BROWSER_GRADE_NOTE, LATE_NOTE, FAIL_OK_NOTE, REGRADE_NOTE, SUBMIT_LABEL, RESUBMIT_LABEL,
 COMMENT_PLACEHOLDER, TOAST_OK, TOAST_LATE, TOAST_FAILED,
 targetKey, parseTargetKey, normalizeTargets, normalizeClassrooms, catalogTargets,
 filterCatalogTargets, assignmentVisible, isLate, statusLabel, reviewLabel, submitButtonLabel,
 statusChips, submitToast,
 assignmentFields, assignmentReady, targetSnapshot, targetsFromState, submissionStatus,
 submissionFields, teacherReviewFields, canSubmit, clipOutput, clipComment, clipFiles,
 appendHistory, targetHref
} from '../../web/assets/assignment-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(LABEL_FAILED, '미통과', 'failed label');
eq(LABEL_LATE, '지연', 'late label');
eq(LABEL_PASSED, '통과', 'passed label');
eq(LABEL_REVIEWED, '확인됨', 'reviewed label');
eq(BROWSER_GRADE_NOTE, '브라우저 채점이에요. 성적·출결에는 안 들어가요.', 'browser grade');
eq(LATE_NOTE, '마감 후에도 제출할 수 있어요. 지연으로 표시돼요.', 'late note');
eq(FAIL_OK_NOTE, '통과하지 않아도 제출할 수 있어요.', 'fail ok');
eq(REGRADE_NOTE, '이 브라우저에서 다시 실행해 저장된 채점과 비교해요. 제출 기록은 바꾸지 않아요.', 'regrade note');
eq(REGRADE_NOTE.includes('다음 단계'), false, 'no regrade stub');
eq(SUBMIT_LABEL, '제출', 'submit');
eq(RESUBMIT_LABEL, '다시 제출', 'resubmit');
eq(COMMENT_PLACEHOLDER, '짧게 남겨 주세요', 'comment placeholder');
eq(TOAST_OK, '제출했어요.', 'toast ok');
eq(TOAST_LATE, '지연으로 제출했어요.', 'toast late');
eq(TOAST_FAILED, '미통과로 제출했어요.', 'toast failed');
eq(SUBMIT_COOLDOWN_MS >= 3000 && SUBMIT_COOLDOWN_MS <= 10000, true, 'cooldown');

eq(targetKey({type: 'question', id: 'u1-q041'}), 'question:u1-q041', 'target key');
eq(parseTargetKey('example:reuse'), {type: 'example', id: 'reuse'}, 'parse key');
eq(normalizeTargets([
 {type: 'question', id: 'u1-q001'},
 {type: 'example', id: 'reuse'},
 {type: 'question', id: 'u1-q001'},
 {type: 'other', id: 'x'},
 {id: 'no-type'}
]), [{type: 'question', id: 'u1-q001'}, {type: 'example', id: 'reuse'}], 'normalize targets');
eq(normalizeClassrooms(['2-3', '2-3', 'bad', '1-2']), ['2-3', '1-2'], 'classrooms');

const catalog = {
 pages: [{id: 'units/unit01/index.html', label: 'Ⅰ', unit: 1}],
 topics: {'units/unit01/index.html': [{id: 'overview', title: '모듈', examples: ['reuse']}]},
 examples: {reuse: {title: '재사용', unit: 1, mode: 'web'}},
 questions: [{id: 'u1-q041', unit: 1, topic: 'define', kind: '구현', prompt: 'add 함수를 완성하세요.'}]
};
const items = catalogTargets(catalog);
eq(items.some((row) => row.type === 'question' && row.id === 'u1-q041' && row.title.includes('add')), true, 'catalog question');
eq(items.some((row) => row.type === 'example' && row.id === 'reuse' && row.unit === 1), true, 'catalog example');
eq(filterCatalogTargets(items, {unit: 1, type: 'question', search: 'add'}).map((r) => r.id), ['u1-q041'], 'filter');
eq(targetHref('../', {type: 'question', id: 'u1-q041', unit: 1}, catalog), '../units/unit01/index.html#u1-q041', 'q href');
eq(targetHref('../', {type: 'example', id: 'reuse'}, catalog), '../units/unit01/index.html#overview', 'ex href');

const assignment = {
 title: '모듈 과제',
 open: true,
 classrooms: ['2-3'],
 targets: [{type: 'question', id: 'u1-q041'}, {type: 'example', id: 'reuse'}],
 openAt: Date.parse('2026-09-01T00:00:00+09:00'),
 dueAt: Date.parse('2026-09-10T18:00:00+09:00')
};
eq(assignmentVisible(assignment, '2-3', Date.parse('2026-09-05T12:00:00+09:00')), true, 'visible');
eq(assignmentVisible({...assignment, open: false}, '2-3', Date.parse('2026-09-05T12:00:00+09:00')), false, 'closed');
eq(assignmentVisible(assignment, '2-4', Date.parse('2026-09-05T12:00:00+09:00')), false, 'other class');
eq(assignmentVisible(assignment, '2-3', Date.parse('2026-08-01T12:00:00+09:00')), false, 'before open');
eq(isLate(assignment, Date.parse('2026-09-11T12:00:00+09:00')), true, 'late');
eq(isLate(assignment, Date.parse('2026-09-09T12:00:00+09:00')), false, 'on time');

eq(statusLabel({status: 'failed', late: false}), '미통과', 'fail label');
eq(statusLabel({status: 'failed', late: true}), '미통과 · 지연', 'fail late');
eq(statusLabel({status: 'passed', late: true}), '지연', 'pass late');
eq(statusLabel({status: 'passed', late: false}), '통과', 'pass');
eq(reviewLabel('reviewed'), '확인됨', 'review');
eq(submitButtonLabel({status: 'failed', hasSubmission: false}), '제출', 'fail submit');
eq(submitButtonLabel({status: 'passed', hasSubmission: true}), '다시 제출', 'resubmit pass');
eq(submitButtonLabel({status: 'failed', hasSubmission: true}), '다시 제출', 'resubmit fail');
eq(statusChips({status: 'failed', late: false}), ['미통과'], 'chips fail');
eq(statusChips({status: 'failed', late: true}), ['미통과', '지연'], 'chips fail late');
eq(statusChips({status: 'passed', late: true}), ['통과', '지연'], 'chips pass late');
eq(statusChips({status: 'passed', late: false}), ['통과'], 'chips pass');
eq(submitToast({status: 'passed', late: false}), '제출했어요.', 'toast pass');
eq(submitToast({status: 'passed', late: true}), '지연으로 제출했어요.', 'toast late pass');
eq(submitToast({status: 'failed', late: true}), '미통과로 제출했어요.', 'toast fail late');

const fields = assignmentFields({
 title: '  모듈 과제  ',
 description: '기존 문제와 예제를 고릅니다.',
 targets: [{type: 'question', id: 'u1-q041'}],
 classrooms: ['2-3'],
 open: true,
 createdBy: 'teacher@e-mirim.hs.kr'
});
eq(fields.title, '모듈 과제', 'title trim');
eq(assignmentReady(fields), true, 'ready');
eq(assignmentReady({...fields, targets: []}), false, 'no targets');

eq(clipOutput('x'.repeat(OUTPUT_MAX + 50)).length, OUTPUT_MAX, 'output max');
eq(clipComment('  한 줄   코멘트  '), '한 줄 코멘트', 'comment');
eq(Object.keys(clipFiles({a: '1', b: '2'})).length, 2, 'files');

const snap = targetSnapshot({
 type: 'example', id: 'reuse', files: {'main.py': 'print(1)'}, stdin: '6', args: '[]',
 grade: {ok: false, checked: true}, output: 'Error', attempts: 2
});
eq(snap.grade.ok, false, 'snap fail');
eq(snap.grade.kind, 'browser', 'browser kind');
eq(snap.files['main.py'], 'print(1)', 'source kept');

const collected = targetsFromState({
 assignment,
 state: {
  answers: {'u1-q041': {value: 'def add(a,b): return a+b', status: 'done', attempts: 1, feedback: '확인 완료'}},
  projects: {reuse: {files: {'main.py': 'print(2)'}, stdin: '', args: '[]', lastOk: false, lastOutput: 'boom', attempts: 3}}
 },
 catalog
});
eq(submissionStatus(collected), 'failed', 'mixed status');
eq(collected['question:u1-q041'].grade.ok, true, 'q passed');
eq(collected['example:reuse'].grade.ok, false, 'ex failed');
eq(collected['example:reuse'].attempts, 3, 'ex attempts');

const profile = {
 uid: 'u1', email: '20314@e-mirim.hs.kr', studentId: '20314', admissionYear: 2025,
 name: '홍길동', grade: 2, classroom: 3, number: 14
};
const first = submissionFields({profile, assignmentId: 'a1', classId: '2-3', targets: collected, late: true});
eq(first.status, 'failed', 'sub status');
eq(first.late, true, 'sub late');
eq(first.attemptCount, 1, 'first attempt');
eq(first.reviewStatus, 'pending', 'pending');
eq(first.classId, '2-3', 'class');
eq(first.studentId, '20314', 'sid');

const again = submissionFields({
 profile, assignmentId: 'a1', classId: '2-3', targets: collected, late: true,
 previous: {...first, submittedAt: 100, reviewComment: '한 줄', reviewStatus: 'reviewed'}
});
eq(again.attemptCount, 2, 'resubmit count');
eq(again.history.length, 1, 'history');
eq(again.history[0].status, 'failed', 'hist status');
eq(again.reviewStatus, 'pending', 'reset review');
eq(again.reviewComment, '한 줄', 'keep comment');

const review = teacherReviewFields({comment: '  입력값을 바꿔 보세요  ', email: 'Teacher@e-mirim.hs.kr'});
eq(review.reviewStatus, 'reviewed', 'review status');
eq(review.reviewComment, '입력값을 바꿔 보세요', 'review comment');
eq(review.reviewedBy, 'teacher@e-mirim.hs.kr', 'reviewer');

eq(canSubmit({lastAt: 10, now: 12}).ok, false, 'cooldown block');
eq(canSubmit({lastAt: 10, now: 10 + SUBMIT_COOLDOWN_MS}).ok, true, 'cooldown ok');
eq(appendHistory(null).length, 0, 'empty history');

console.log('PASS: assignment-model helpers');
