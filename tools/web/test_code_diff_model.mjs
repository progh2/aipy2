/* 예제 코드 수정 여부 표시(#135-4) 순수 로직 검사. node tools/web/test_code_diff_model.mjs */
import {lineDiffCounts, projectDiffSummary} from '../../web/assets/code-diff-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

// --- lineDiffCounts ---
eq(lineDiffCounts('a\nb\nc\n', 'a\nb\nc\n'), {added: 0, removed: 0}, '동일한 내용은 0/0');
eq(lineDiffCounts('a\nb\n', 'a\nb\n\n'), {added: 0, removed: 0}, '끝 빈 줄 차이는 무시');
eq(lineDiffCounts('a\nb  \n', 'a\nb\n'), {added: 0, removed: 0}, '줄 끝 공백 차이는 무시');
eq(lineDiffCounts('a\nb\nc\n', 'a\nb\nc\nd\n'), {added: 1, removed: 0}, '한 줄 추가는 +1/0');
eq(lineDiffCounts('a\nb\nc\n', 'a\nB\nc\n'), {added: 1, removed: 1}, '한 줄 수정은 +1/-1');
eq(lineDiffCounts('', ''), {added: 0, removed: 0}, '빈 입력 둘 다면 0/0');
eq(lineDiffCounts('a\nb\n', ''), {added: 0, removed: 2}, '학생 파일이 비면 전부 removed');
eq(lineDiffCounts('', 'a\nb\n'), {added: 2, removed: 0}, '원본이 비면 전부 added');

// --- projectDiffSummary ---
eq(
 projectDiffSummary({'main.py': 'a\nb\n'}, {'main.py': 'a\nb\n'}),
 {added: 0, removed: 0, same: true},
 '동일한 프로젝트는 same:true'
);
eq(
 projectDiffSummary({'main.py': 'a\nb\n'}, {'main.py': 'a\nb\nc\n'}),
 {added: 1, removed: 0, same: false},
 '한 줄 추가된 프로젝트'
);
eq(
 projectDiffSummary({'main.py': 'a\nb\nc\n'}, {'main.py': 'a\nB\nc\n'}),
 {added: 1, removed: 1, same: false},
 '한 줄 수정된 프로젝트는 +1/-1'
);
eq(
 projectDiffSummary({'main.py': 'a\n'}, {'main.py': 'a\n', 'extra.py': 'x\n'}),
 {added: 1, removed: 0, same: false},
 '파일이 추가되면 그 파일 줄만큼 added'
);
eq(projectDiffSummary({}, {}), {added: 0, removed: 0, same: true}, '빈 입력끼리는 same:true');
eq(projectDiffSummary(null, undefined), {added: 0, removed: 0, same: true}, 'null/undefined도 빈 것으로 취급');

console.log('PASS test_code_diff_model.mjs');
