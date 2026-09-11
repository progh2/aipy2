/* 교사 재검증 순수 함수 검사. node tools/web/test_regrade_model.mjs */
import {
 REVERIFY_NOTE, REVERIFY_LABEL, REVERIFY_CLASS_LABEL, REVERIFY_SKIP_ESSAY,
 MATCH_LABEL, MISMATCH_LABEL, SKIP_LABEL, ERROR_LABEL,
 normAnswer, submittedSource, storedOk, unitFromTarget, localRegrade, pyodidePayload,
 compareTargetGrade, summarizeReverify, reverifyResultRow, submissionMismatchCount
} from '../../web/assets/regrade-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(REVERIFY_NOTE, '이 브라우저에서 다시 실행해 저장된 채점과 비교해요. 제출 기록은 바꾸지 않아요.', 'reverify note');
eq(REVERIFY_LABEL, '이 제출 다시 채점', 'reverify button');
eq(REVERIFY_CLASS_LABEL, '이 반 다시 채점', 'class reverify button');
eq(REVERIFY_SKIP_ESSAY, '서술형은 자동 재검증하지 않아요.', 'essay skip');
eq(MATCH_LABEL, '저장된 결과와 같아요', 'match');
eq(MISMATCH_LABEL, '저장된 결과와 달라요', 'mismatch');
eq(SKIP_LABEL, '다시 채점 안 함', 'skip');
eq(ERROR_LABEL, '다시 채점하지 못했어요', 'error');

eq(normAnswer('  Hello  World '), 'HelloWorld', 'norm space');
eq(normAnswer("it's"), 'it"s', 'norm quote');
eq(submittedSource({files: {'answer.txt': '모듈', 'main.py': 'print(1)'}}), 'print(1)', 'prefer main');
eq(submittedSource({files: {'answer.txt': '모듈'}}), '모듈', 'answer file');
eq(storedOk({grade: {ok: true}}), true, 'stored pass');
eq(storedOk({grade: {ok: false}}), false, 'stored fail');
eq(unitFromTarget({type: 'question', id: 'u2-q010'}), 2, 'unit from id');
eq(unitFromTarget({type: 'example', id: 'reuse'}, {examples: {reuse: {unit: 1}}}), 1, 'unit from catalog');

const mc = localRegrade({kind: '선택', answer: '모듈'}, {files: {'answer.txt': '모듈'}, grade: {ok: true}});
eq(mc.method, 'text', 'mc method');
eq(mc.ok, true, 'mc pass');
eq(localRegrade({kind: '서술'}, {files: {'answer.txt': '설명'}}).reason, REVERIFY_SKIP_ESSAY, 'essay skip');
eq(localRegrade({kind: '순서', answer: ['a', 'b']}, {files: {'answer.txt': '["a","b"]'}}).ok, true, 'order');

const code = localRegrade({kind: '구현', starter: 'def add', checks: 'assert add(1,1)==2'}, {files: {'main.py': 'def add(a,b): return a+b'}});
eq(code.method, 'pyodide', 'code needs pyodide');
eq(code.skip, false, 'code not skip');

const payload = pyodidePayload(
 {entry: 'main.py', checks: 'assert True', mode: 'web'},
 {files: {'main.py': 'print(1)', 'util.py': 'x=1'}, stdin: '6', args: '["a"]'}
);
eq(payload.entry, 'main.py', 'payload entry');
eq(payload.args, ['a'], 'payload args');
eq(payload.checks.includes('assert'), true, 'payload checks');
eq(payload.syntax, false, 'web not syntax');
eq(pyodidePayload({mode: 'pc', entry: 'main.py'}, {files: {'main.py': 'print(1)'}}).syntax, true, 'pc syntax');

eq(compareTargetGrade(true, {ok: true, skip: false}).status, 'match', 'compare match');
eq(compareTargetGrade(true, {ok: false, skip: false}).status, 'mismatch', 'compare mismatch');
eq(compareTargetGrade(false, {skip: true}).status, 'skip', 'compare skip');
eq(compareTargetGrade(true, {ok: false, error: 'boom', checked: false, method: 'pyodide'}).status, 'error', 'compare error');

const row = reverifyResultRow({
 uid: 'u1',
 target: {type: 'question', id: 'u1-q001', grade: {ok: true}},
 live: {ok: false, skip: false, method: 'text'}
});
eq(row.status, 'mismatch', 'row mismatch');
eq(row.key, 'question:u1-q001', 'row key');
eq(summarizeReverify([row, {status: 'match'}, {status: 'skip'}]), {total: 3, match: 1, mismatch: 1, skip: 1, error: 0}, 'summary');
eq(submissionMismatchCount([row, {uid: 'u1', status: 'match'}], 'u1'), 1, 'mismatch count');

console.log('PASS: regrade-model helpers');
