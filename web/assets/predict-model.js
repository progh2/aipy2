/* #135 항목1·2 순수 로직 — 실행 전 예측·코드 읽기(핵심 줄 설명).
   저장은 기존 저널 버킷([data-journal], app.js)을 그대로 쓴다. 여기서는
   그 키를 만들고, 실행 버튼 활성 조건과 "자기 말로 다시 써 보세요" 유사도 판정만 다룬다.
   node tools/web/test_predict_model.mjs 로 검사한다. */

// 예측 p-{예제id} / 비교 p-{예제id}-match·-why / 웹 실행·PC 자가 보고 결과 p-{예제id}-actual.
export function predictKey(id) { return `p-${id}`; }
export function predictMatchKey(id) { return `p-${id}-match`; }
export function predictWhyKey(id) { return `p-${id}-why`; }
export function predictActualKey(id) { return `p-${id}-actual`; }

// 코드 읽기 c-{예제id}-{줄번호 또는 파일_줄번호}. ref는 key_lines.resolve()가 만든
// 'main.py_12' 또는 '12' 형태 문자열이다(콜론 없음 — 저널 키에 콜론을 안 쓰려고 이미 치환됨).
export function codeReadKey(id, ref) { return `c-${id}-${ref}`; }

// 예측을 적어야 [실행]이 켜진다.
export function hasPrediction(text) {
 return typeof text === 'string' && text.trim().length > 0;
}

export function isSameValue(value) { return value === 'same'; }
export function isDiffValue(value) { return value === 'diff'; }

// 공백 제거 후 두 문자열의 가장 긴 공통 부분 문자열 길이 / 짧은 쪽 길이.
function normalize(s) {
 return String(s ?? '').replace(/\s+/g, '');
}

export function longestCommonSubstringLength(a, b) {
 const s1 = normalize(a), s2 = normalize(b);
 if (!s1 || !s2) return 0;
 const m = s1.length, n = s2.length;
 let prev = new Array(n + 1).fill(0);
 let best = 0;
 for (let i = 1; i <= m; i++) {
  const cur = new Array(n + 1).fill(0);
  for (let j = 1; j <= n; j++) {
   if (s1[i - 1] === s2[j - 1]) {
    cur[j] = prev[j - 1] + 1;
    if (cur[j] > best) best = cur[j];
   }
  }
  prev = cur;
 }
 return best;
}

export function commonSubstringRatio(a, b) {
 const s1 = normalize(a), s2 = normalize(b);
 const shorter = Math.min(s1.length, s2.length);
 if (shorter === 0) return 0;
 return longestCommonSubstringLength(a, b) / shorter;
}

// explanation이 references(예제·슬라이드 설명 문장들) 중 하나와 거의 같으면(공통 부분
// 문자열 비율이 높으면) true. 너무 짧은 설명(공백 제거 8자 미만)은 판단하지 않는다 —
// 짧은 문장은 우연히도 참조 문장의 일부와 겹치기 쉽다.
export function looksCopied(explanation, references, threshold = 0.6) {
 const text = normalize(explanation);
 if (text.length < 8) return false;
 const list = Array.isArray(references) ? references : [references];
 for (const ref of list) {
  const refText = normalize(ref);
  if (refText.length < 8) continue;
  if (commonSubstringRatio(explanation, ref) >= threshold) return true;
 }
 return false;
}
