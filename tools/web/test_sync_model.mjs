/* 학습 기록 병합·요약 검사. node tools/web/test_sync_model.mjs */
import {
 LEARNING_KEY, CODE_IDLE_MS, shouldFlushNow, stampChanged, mergeStates, mapsChanged,
 summarizeProgress, progressFields, statePayload, cloudToState, projectNeedsChoice,
 projectPreview, emptyState, normalizeState, projectCodeEqual, keepProjectRecord,
 projectConflictSignature, CHOICE_KEY
} from '../../web/assets/sync-model.js';

function code(text, extra = {}) {
 return {files: {'main.py': text}, entry: 'main.py', stdin: '', args: '[]', ...extra};
}

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(LEARNING_KEY, 'aipy-lab-v1', 'storage key');
eq(CODE_IDLE_MS >= 20000 && CODE_IDLE_MS <= 30000, true, 'idle window');
eq(shouldFlushNow('complete'), true, 'complete immediate');
eq(shouldFlushNow('answer'), true, 'answer immediate');
eq(shouldFlushNow('code'), false, 'code idle');
eq(shouldFlushNow('journal'), false, 'journal idle');

const now = 1_700_000_100_000;
const local = normalizeState({
 complete: {'u1-overview': true, 'u2-hello': true},
 answers: {'q1-1': {value: 'A', status: 'done', attempts: 2}},
 journals: {'u1-learn': '로컬 저널'},
 projects: {
  reuse: {files: {'main.py': 'print(1)'}, entry: 'main.py', stdin: '', args: '[]'},
  math: {files: {'main.py': 'print("local")'}, entry: 'main.py', stdin: '', args: '[]'}
 },
 last: 'units/unit01/index.html#overview',
 times: {
  complete: {'u1-overview': now - 5000, 'u2-hello': now - 1000},
  answers: {'q1-1': now - 2000},
  journals: {'u1-learn': now - 8000},
  projects: {reuse: now - 1000, math: now - 3000},
  last: now - 1000
 }
});
const cloud = normalizeState({
 complete: {'u1-overview': false, 'u1-define': true},
 answers: {'q1-1': {value: 'B', status: 'retry', attempts: 1}, 'q1-2': {value: 'C', status: 'done', attempts: 1}},
 journals: {'u1-learn': '클라우드 저널', 'u1-error': '클라우드 오류'},
 projects: {
  reuse: {files: {'main.py': 'print(1)'}, entry: 'main.py', stdin: '', args: '[]'},
  math: {files: {'main.py': 'print("cloud")'}, entry: 'main.py', stdin: '', args: '[]'},
  extra: {files: {'main.py': 'print(9)'}, entry: 'main.py', stdin: '', args: '[]'}
 },
 last: 'units/unit02/index.html#hello',
 times: {
  complete: {'u1-overview': now - 1000, 'u1-define': now - 2000},
  answers: {'q1-1': now - 9000, 'q1-2': now - 1000},
  journals: {'u1-learn': now - 1000, 'u1-error': now - 1000},
  projects: {reuse: now - 4000, math: now - 2000, extra: now - 500},
  last: now - 500
 }
});

const merged = mergeStates(local, cloud, {}, now);
eq(merged.state.complete['u1-overview'], false, 'complete newer cloud uncheck');
eq(merged.state.complete['u2-hello'], true, 'complete local-only kept');
eq(merged.state.complete['u1-define'], true, 'complete cloud-only kept');
eq(merged.state.answers['q1-1'].value, 'A', 'answer newer local');
eq(merged.state.answers['q1-2'].status, 'done', 'answer cloud-only');
eq(merged.state.journals['u1-learn'], '클라우드 저널', 'journal newer cloud');
eq(merged.state.journals['u1-error'], '클라우드 오류', 'journal cloud-only');
eq(merged.state.last, 'units/unit02/index.html#hello', 'last newer cloud');
eq(merged.state.projects.reuse.files['main.py'], 'print(1)', 'same project no conflict');
eq(merged.state.projects.extra.files['main.py'], 'print(9)', 'project cloud-only');
eq(merged.unresolved, [], 'newer cloud project auto-picked');
eq(merged.state.projects.math.files['main.py'], 'print("cloud")', 'newer cloud project wins');

const sameTimeLocal = normalizeState({
 projects: {math: code('print("local")')},
 times: {projects: {math: now}}
});
const sameTimeCloud = normalizeState({
 projects: {math: code('print("cloud")')},
 times: {projects: {math: now}}
});
const tied = mergeStates(sameTimeLocal, sameTimeCloud, {}, now);
eq(tied.unresolved.map((item) => item.id), ['math'], 'same-time project asks once');
eq(tied.state.projects.math.files['main.py'], 'print("local")', 'unresolved keeps local');

const pickedCloud = mergeStates(sameTimeLocal, sameTimeCloud, {math: 'cloud'}, now);
eq(pickedCloud.unresolved, [], 'choice resolves');
eq(pickedCloud.state.projects.math.files['main.py'], 'print("cloud")', 'keep cloud project');
const pickedLocal = mergeStates(sameTimeLocal, sameTimeCloud, {math: 'local'}, now);
eq(pickedLocal.state.projects.math.files['main.py'], 'print("local")', 'keep local project');
eq(pickedLocal.unresolved, [], 'same choice stays resolved');

const untimedLocal = normalizeState({
 projects: {math: {files: {'main.py': 'print("old")'}, entry: 'main.py', stdin: '', args: '[]'}}
});
const timedCloud = normalizeState({
 projects: {math: {files: {'main.py': 'print("new")'}, entry: 'main.py', stdin: '', args: '[]'}},
 times: {projects: {math: now}}
});
const auto = mergeStates(untimedLocal, timedCloud, {}, now);
eq(auto.unresolved, [], 'untimed local loses to timed cloud without prompt');
eq(auto.state.projects.math.files['main.py'], 'print("new")', 'timed cloud project wins');

eq(projectNeedsChoice(code('a'), code('a'), 1, 2), false, 'equal values no choice');
eq(projectNeedsChoice(code('a'), code('b'), 0, 5), false, 'one-sided time no choice');
eq(projectNeedsChoice(code('a'), code('b'), 5, 6), false, 'newer cloud no prompt');
eq(projectNeedsChoice(code('a'), code('b'), 6, 5), false, 'newer local no prompt');
eq(projectNeedsChoice(code('a'), code('b'), 0, 0), true, 'both untimed differ');
eq(projectNeedsChoice(code('a'), code('b'), 5, 5), true, 'same time differ asks');
eq(projectNeedsChoice(code('print(1)'), code('print(1)', {lastOk: true, attempts: 2}), 5, 6), false, 'check metadata is not a source conflict');
eq(projectCodeEqual(code('print(1)'), {files: {'main.py': 'print(1)'}, entry: 'main.py', stdin: '', args: '[]', lastOutput: 'ok'}), true, 'code equal ignores extra fields');
eq(keepProjectRecord(code('print(1)'), code('print(1)', {attempts: 3, lastOk: true})).attempts, 3, 'keep richer project record');
eq(projectConflictSignature('math', code('a'), code('b')), projectConflictSignature('math', code('a'), code('b')), 'conflict signature stable');
eq(CHOICE_KEY, 'aipy-sync-choices-v1', 'choice store key');

const stamped = stampChanged(
 {complete: {'u1-overview': true}, times: {complete: {'u1-overview': 10}}},
 {complete: {'u1-overview': true, 'u1-define': true}},
 now
);
eq(stamped.times.complete['u1-overview'], 10, 'unchanged keeps time');
eq(stamped.times.complete['u1-define'], now, 'new item stamped');

const stampedProject = stampChanged(
 {projects: {math: code('print(1)', {attempts: 2, lastOk: true})}, times: {projects: {math: 10}}},
 {projects: {math: code('print(1)')}},
 now
);
eq(stampedProject.times.projects.math, 10, 'same source does not restamp');
eq(stampedProject.projects.math.attempts, 2, 'stash without check fields keeps richer record');

const counts = summarizeProgress({
 complete: {'u1-overview': true, 'u1-define': false, 'u3-ml': true, 'skip': true},
 answers: {
  a: {status: 'done', attempts: 3, value: '모듈은 파일입니다.'},
  b: {status: 'retry', attempts: 2},
  c: {status: 'done'}
 }
}, now);
eq(counts.complete, {1: 1, 2: 0, 3: 1, 4: 0}, 'unit complete counts');
eq(counts.questions, {attempts: 5, correct: 2}, 'question attempts and correct');
eq(counts.done, ['u1-overview', 'u3-ml'], 'done topic ids');
eq(counts.answers.a, {attempts: 3, correct: 1, choice: '모듈은 파일입니다.'}, 'answer summary done');
eq(counts.answers.b, {attempts: 2, correct: 0}, 'answer summary retry');
eq(counts.lastActivity, now, 'last activity');

const profile = {
 uid: 'u1', email: '20314@e-mirim.hs.kr', studentId: '20314', admissionYear: 2025,
 name: '홍길동', grade: 2, classroom: 3, number: 14
};
const progress = progressFields(profile, {complete: {'u1-overview': true}, answers: {}}, now, {'u1-overview': 'hard', skip: 'nope'});
eq(Object.keys(progress).sort(), ['admissionYear', 'classroom', 'counts', 'email', 'grade', 'name', 'number', 'studentId', 'uid', 'understanding'], 'progress keys');
eq(progress.understanding, {'u1-overview': 'hard'}, 'normalize understanding');
eq(progress.counts.complete[1], 1, 'progress unit count');

const payload = statePayload(local);
eq(payload.version, 1, 'payload version');
eq('updatedAt' in payload, false, 'payload leaves updatedAt to caller');
eq(cloudToState({...payload, updatedAt: {seconds: 1}}).projects.reuse.files['main.py'], 'print(1)', 'strip extra cloud fields');
eq(mapsChanged(local, merged.state), true, 'maps changed after merge');
eq(mapsChanged(local, local), false, 'same maps');
eq(projectPreview(local.projects.reuse).entry, 'main.py', 'preview entry');
eq(emptyState().version, 1, 'empty version');

console.log('PASS: sync-model helpers');
