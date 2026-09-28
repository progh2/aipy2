/* 실행 전 예측·코드 읽기 순수 로직 검사. node tools/web/test_predict_model.mjs */
import {
 predictKey, predictMatchKey, predictWhyKey, predictActualKey, codeReadKey,
 hasPrediction, isSameValue, isDiffValue, longestCommonSubstringLength, commonSubstringRatio, looksCopied
} from '../../web/assets/predict-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(predictKey('hello-tk'), 'p-hello-tk', 'predict key');
eq(predictMatchKey('hello-tk'), 'p-hello-tk-match', 'predict match key');
eq(predictWhyKey('hello-tk'), 'p-hello-tk-why', 'predict why key');
eq(predictActualKey('hello-tk'), 'p-hello-tk-actual', 'predict actual key');
eq(codeReadKey('hello-tk', '11'), 'c-hello-tk-11', 'code read key single file');
eq(codeReadKey('all', 'main.py_1'), 'c-all-main.py_1', 'code read key multi file');

eq(hasPrediction(''), false, 'empty prediction');
eq(hasPrediction('   '), false, 'whitespace prediction');
eq(hasPrediction('안녕하세요가 출력된다'), true, 'real prediction');
eq(hasPrediction(null), false, 'null prediction');
eq(hasPrediction(undefined), false, 'undefined prediction');

eq(isSameValue('same'), true, 'same value');
eq(isSameValue('diff'), false, 'same value negative');
eq(isDiffValue('diff'), true, 'diff value');
eq(isDiffValue(''), false, 'diff value empty');

eq(longestCommonSubstringLength('abcdef', 'xxabcdyy'), 4, 'lcs substring length');
eq(longestCommonSubstringLength('', 'abc'), 0, 'lcs empty a');
eq(longestCommonSubstringLength('abc', ''), 0, 'lcs empty b');

eq(commonSubstringRatio('hello world', 'hello world'), 1, 'identical ratio 1');
eq(commonSubstringRatio('', 'abc'), 0, 'ratio empty');
eq(Math.round(commonSubstringRatio('name = entry.get()', 'get()') * 100) / 100, 1, 'short string fully contained ratio 1');

// 참조 문장을 거의 그대로 베끼면(공백 제거 후 대부분 겹침) 안내가 뜬다.
const ref = '이름을 입력받아 인사 문구를 만들고 라벨에 표시합니다';
eq(looksCopied('이름을 입력받아 인사 문구를 만들고 라벨에 표시합니다', [ref]), true, 'exact copy flagged');
eq(looksCopied('  이름을   입력받아 인사 문구를 만들고 라벨에 표시합니다  ', [ref]), true, 'copy with extra spaces flagged');
eq(looksCopied('버튼을 누르면 이름을 읽어서 인사말을 만든다', [ref]), false, 'own words not flagged');
eq(looksCopied('짧음', [ref]), false, 'too short to judge');
eq(looksCopied('버튼을 누르면 이름을 읽어서 인사말을 만든다', []), false, 'no references never flagged');
eq(looksCopied('버튼을 누르면 이름을 읽어서 인사말을 만든다', null), false, 'null references never flagged');

console.log('PASS test_predict_model.mjs');
