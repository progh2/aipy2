/* '이어서 학습하기' 링크(#7)를 위한 순수 함수. app.js가 동적 import로 불러 쓴다.
   state.last에는 두 세대의 값이 섞여 있을 수 있다.
   - 구조 개편(2026-09-23) 이전: `units/unit0N/index.html#anchor` (단원 전체가 한 페이지였다)
   - 이후(현재): `units/unit0N/{소단원}.html` 처럼 소단원별 독립 페이지
   구형 anchor 중 #journal은 지금도 유효하고, #practice는 단원 전체 문제집(practice.html)으로,
   #lab(예제 편집기)은 예제별 독립 페이지(ex-*.html)로 흩어져 대상을 하나로 특정할 수 없어
   단원 안내로 보낸다. #gallery·#simulator는 2단원 index.html에만 실제로 남아 있어 그때만 그대로 둔다.
   u{N}-{slug} 형태는 완료 체크·저널 키와 같은 표기이며 slug가 소단원 파일명과 같으므로 그 페이지로,
   u{N}-q### 문항 id는 어느 소단원 문제인지 이 함수만으로는 알 수 없어 단원 안내로 보낸다. */

export const LESSON_SLUGS = {
 1: ['overview', 'define', 'entrypoint', 'imports', 'packages', 'os-sys', 'math', 'random', 'datetime', 'thirdparty', 'review', 'project'],
 2: ['ui', 'libraries', 'widgets', 'layout', 'events', 'memo', 'pyside', 'project', 'review', 'wx', 'kivy'],
 3: ['ml-overview', 'ml-use', 'ml-process', 'ml-terms', 'ml-methods', 'ml-libraries', 'ml-preprocess', 'ml-classification', 'ml-regression', 'ml-cluster', 'ml-metrics', 'ml-selection', 'ml-project'],
 4: ['cv-overview', 'cv-pixels', 'cv-pipeline', 'cv-libraries', 'cv-io', 'cv-filters', 'cv-transform', 'cv-features', 'cv-haar', 'cv-yolo', 'cv-project']
};

const LEGACY_RE = /^units\/unit0([1-4])\/index\.html#([a-z0-9-]+)$/;
const MODERN_RE = /^units\/unit0[1-4]\/[a-z0-9-]+\.html(?:#[a-z0-9-]+)?$/;
const TOPIC_ID_RE = /^u[1-4]-(.+)$/;
const QUESTION_SLUG_RE = /^q\d+$/;

export function resumeHref(raw) {
 if (typeof raw !== 'string') return '';
 const legacy = LEGACY_RE.exec(raw);
 if (legacy) {
  const n = Number(legacy[1]);
  const anchor = legacy[2];
  const base = `units/unit0${n}/`;
  if (anchor === 'journal') return `${base}index.html#journal`;
  if (anchor === 'practice') return `${base}practice.html`;
  // #gallery·#simulator는 2단원 index.html에만 실존한다(단원 전체 라이브러리 비교·시뮬레이션 절).
  if (n === 2 && (anchor === 'gallery' || anchor === 'simulator')) return `${base}index.html#${anchor}`;
  if (anchor === 'lab' || anchor === 'gallery' || anchor === 'simulator') return `${base}index.html`;
  const topicMatch = TOPIC_ID_RE.exec(anchor);
  const slug = topicMatch ? topicMatch[1] : anchor;
  if (QUESTION_SLUG_RE.test(slug)) return `${base}index.html`;
  if ((LESSON_SLUGS[n] || []).includes(slug)) return `${base}${slug}.html`;
  return `${base}index.html`;
 }
 if (MODERN_RE.test(raw)) return raw;
 return '';
}
