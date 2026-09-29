/* 학생이 예제 코드를 원본 그대로 실행만 했는지, 실제로 고쳤는지 교사가 보려면
   원본 파일(카탈로그)과 학생이 저장한 프로젝트(students/{uid}/state/current.projects[eid].files)를
   줄 단위로 비교해야 한다(#135-4). Firebase 없이 검사할 수 있는 순수 함수만 여기 모은다 —
   원본을 어디서 읽어 오는지(fetch)는 화면 쪽(teacher-answers.js/teacher-board.js) 책임이다. */

// 끝 공백과 파일 끝의 빈 줄 차이는 "수정"으로 치지 않는다 — 저장할 때 에디터가 붙이는 개행 하나로
// 학생이 손도 안 댄 파일이 "수정됨"으로 표시되면 신뢰를 잃는다.
function normalizeLines(text) {
 if (text == null) return [];
 const lines = String(text).split('\n');
 while (lines.length && lines[lines.length - 1] === '') lines.pop();
 return lines.map((line) => line.replace(/[ \t]+$/, ''));
}

// 줄 단위 LCS로 added/removed를 센다. 한 줄을 고치면 그 줄은 LCS에서 빠지므로 +1 -1로 잡힌다.
export function lineDiffCounts(originalText, studentText) {
 const a = normalizeLines(originalText);
 const b = normalizeLines(studentText);
 const n = a.length;
 const m = b.length;
 if (!n) return {added: m, removed: 0};
 if (!m) return {added: 0, removed: n};
 const dp = new Array(n + 1);
 for (let i = 0; i <= n; i++) dp[i] = new Array(m + 1).fill(0);
 for (let i = n - 1; i >= 0; i--) {
  for (let j = m - 1; j >= 0; j--) {
   dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  }
 }
 const lcs = dp[0][0];
 return {added: m - lcs, removed: n - lcs};
}

// originalFiles/studentFiles는 {파일명: 내용} 맵. 한쪽에만 있는 파일도 다른 쪽을 빈 문자열로 보고 diff한다.
export function projectDiffSummary(originalFiles, studentFiles) {
 const orig = originalFiles && typeof originalFiles === 'object' ? originalFiles : {};
 const stud = studentFiles && typeof studentFiles === 'object' ? studentFiles : {};
 const names = new Set([...Object.keys(orig), ...Object.keys(stud)]);
 let added = 0;
 let removed = 0;
 for (const name of names) {
  const counts = lineDiffCounts(orig[name], stud[name]);
  added += counts.added;
  removed += counts.removed;
 }
 return {added, removed, same: added === 0 && removed === 0};
}
