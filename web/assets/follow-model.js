/* 수업 따라가기(M5) 순수 헬퍼. Firebase 없이 검사할 수 있게 상태·경로·집계만 다룹니다. */

export const SESSION_TTL_MS = 2 * 60 * 60 * 1000;
export const PRESENCE_HEARTBEAT_MS = 90 * 1000;
export const PRESENCE_STALE_MS = 3 * 60 * 1000;
export const PENDING_FOCUS_KEY = 'aipy-follow-pending';
export const FOLLOWING_KEY_PREFIX = 'aipy-following:';
export const DEFAULT_PAGE = 'units/unit01/index.html';

export function timestampMillis(value) {
 if (value == null) return 0;
 if (typeof value === 'number' && Number.isFinite(value)) return value;
 if (typeof value.toMillis === 'function') return value.toMillis();
 if (typeof value.toDate === 'function') return value.toDate().getTime();
 if (value instanceof Date) return value.getTime();
 if (typeof value.seconds === 'number') {
  return value.seconds * 1000 + Math.floor((value.nanoseconds || 0) / 1e6);
 }
 return 0;
}

export function isSessionLive(session, now = Date.now()) {
 if (!session || session.active !== true) return false;
 const exp = timestampMillis(session.expiresAt);
 return !exp || exp >= now;
}

export function normalizePage(page) {
 if (!page || typeof page !== 'string') return '';
 return page.replace(/\\/g, '/').replace(/^\/+/, '').replace(/^\.\//, '');
}

export function pageFromPath(pathname) {
 const raw = decodeURIComponent(String(pathname || '')).replace(/\\/g, '/');
 const parts = raw.split('/').filter(Boolean);
 if (parts[0] === 'aipy2') parts.shift();
 if (!parts.length) return 'index.html';
 const last = parts[parts.length - 1];
 if (!last.includes('.')) {
  if (parts.includes('units')) {
   const i = parts.indexOf('units');
   return parts.slice(i).concat('index.html').join('/');
  }
  if (parts.includes('teacher')) {
   const i = parts.indexOf('teacher');
   return parts.slice(i).concat('index.html').join('/');
  }
  return 'index.html';
 }
 if (parts.includes('units')) {
  const i = parts.indexOf('units');
  return parts.slice(i).join('/');
 }
 if (parts.includes('teacher')) {
  const i = parts.indexOf('teacher');
  return parts.slice(i).join('/');
 }
 return last;
}

export function samePage(a, b) {
 return normalizePage(a) === normalizePage(b) && Boolean(normalizePage(a));
}

const CHROME_TOPICS = new Set(['main', 'account', 'toast', 'lab', 'practice', 'gallery', 'simulator', 'journal',
 // 본문 안의 보조 섹션들 — 소단원 이름이 아니다(pre-api를 소단원으로 오인해 없는 페이지로 보내던 사고).
 'pre-api', 'content-tips', 'screenshots', 'example-guides', 'questions', 'question-page',
 'notes-layer', 'student-detail', 'follow-ui', 'teacher-focus-ui', 'toc', 'rail-todo']);

export function unitFromPage(page) {
 const match = /^units\/unit0([1-4])\//.exec(normalizePage(page));
 return match ? Number(match[1]) : 0;
}

// ex-*.html은 예제 전용 페이지이며 소단원(lesson) id로 오인하면 안 된다 — 별도 정규식으로 걸러낸다.
export function pageTopicId(page) {
 const match = /^units\/unit0[1-4]\/(?!ex-)([a-z0-9-]+)\.html$/.exec(normalizePage(page));
 if (!match || match[1] === 'index' || match[1] === 'summary' || match[1] === 'practice') return null;
 // 문제 페이지(q-widgets.html)의 주제는 그 소단원(widgets)이다.
 return match[1].startsWith('q-') ? match[1].slice(2) : match[1];
}

export function pageExampleId(page) {
 const match = /^units\/unit0[1-4]\/ex-([a-z0-9-]+)\.html$/.exec(normalizePage(page));
 return match ? match[1] : null;
}

// 문항 앵커(u1-q041)는 소단원 이름이 아니다. 예전에는 이것을 소단원으로 오인해
// units/unit01/u1-q041.html 같은 없는 페이지로 보냈다(교사가 문항에 초점을 보낼 때 이동 실패).
const QUESTION_ANCHOR_RE = /^u[1-4]-q\d+$/;

// 앵커 정규화를 한 곳에 모은다. topicAnchor는 세 형식을 받는다.
//  - '요소id' (버튼 클릭 등, 비율 없음)
//  - '요소id@비율' (교사 스크롤 추적, 옛 형식 — 컨테이너 전체 안에서의 비율)
//  - '요소id~b{n}@비율' (#126, 블록 추적 — build.py가 매긴 data-fb="b{n}" 블록 안에서의 비율)
// 비율·블록은 스크롤 위치 계산에만 쓴다 — 페이지·소단원·문항 여부를 판단할 때는 반드시 이 함수로
// 비율·블록을 먼저 뗀 id만 본다. (예: 'u1-q042@0.3'을 그대로 문항 판정 정규식에 넣으면 매치에 실패해
// q-math.html이 math.html로 바뀌는 사고가 났다. 블록 부분도 같은 이유로 절대 경로 판정에 넣지 않는다.)
// '~b{n}' 형식이 잘못된 값(경로 조각, 빈 값, 너무 긴 값 등)이면 조용히 버리고 id는 그대로 살린다 —
// 악의적이거나 이상한 블록 값이 와도 앵커 해석 자체가 깨지지 않게 하기 위해서다.
const BLOCK_TOKEN_RE = /^b\d{1,6}$/;

export function parseAnchor(anchor) {
 const raw = String(anchor || '');
 const m = /^([^@]+)(?:@([0-9.]+))?$/.exec(raw);
 if (!m) return {id: '', block: null, frac: null};
 const frac = m[2] === undefined ? null : Math.min(0.99, Math.max(0, parseFloat(m[2]) || 0));
 const idPart = m[1];
 const tilde = idPart.indexOf('~');
 if (tilde === -1) return {id: idPart, block: null, frac};
 const id = idPart.slice(0, tilde);
 const token = idPart.slice(tilde + 1);
 return {id, block: BLOCK_TOKEN_RE.test(token) ? token : null, frac};
}

export function anchorId(anchor) {
 return parseAnchor(anchor).id;
}

// 교사 쪽에서 앵커 문자열을 만드는 단일 출처(#126). block이 형식에 안 맞으면 조용히 빼고
// 옛 '요소id@비율' 형식으로 내려간다 — parseAnchor의 검증 규칙과 항상 짝을 이룬다.
// id를 비워 두면(''), 소단원/문항 컨테이너가 없는 페이지(예제·연습문제 목록·단원 인덱스 등)에서
// 쓰는 '~b{n}@비율'(id 없는 블록 전용 앵커, #126) 형식이 된다 — 반드시 blockOnlyAllowed(page)가
// true인 페이지에서만 이 형태로 호출해야 한다(teacher-focus.js에서 그렇게 쓴다).
export function blockAnchor(id, block, frac) {
 const safeId = String(id || '');
 const validBlock = Boolean(block) && BLOCK_TOKEN_RE.test(String(block));
 if (!safeId && !validBlock) return '';
 const f = Math.min(0.99, Math.max(0, Number.isFinite(frac) ? frac : 0));
 let base;
 if (validBlock) base = safeId ? `${safeId}~${block}` : `~${block}`;
 else base = safeId;
 if (!base) return '';
 return `${base}@${f.toFixed(2)}`;
}

// 컨테이너(section.lesson[id]·.question[id])가 없는 페이지에서만 id 없는 블록 전용 앵커
// ('~b{n}@비율')를 써도 되는지 판단하는 단일 출처(#126). resolveFocusLocation에서
// topicId가 ''일 때 pageTopicId(page)가 null이 아니면 fromPage로 다른 페이지(예: q-math.html
// → math.html)로 잘못 넘어간다 — 그래서 pageTopicId(page)===null인 페이지(ex-*.html·
// practice.html·index.html·summary.html)에서만 허용한다. q-*.html은 pageTopicId가 그
// 소단원 id를 반환하므로 여기서 반드시 false다 — 절대 이 규칙을 약화하지 말 것.
export function blockOnlyAllowed(page) {
 const p = normalizePage(page);
 return pageTopicId(p) === null && unitFromPage(p) > 0;
}

export function isLessonTopic(id) {
 return Boolean(id) && /^[a-z][a-z0-9-]*$/.test(id) && !CHROME_TOPICS.has(id) && !QUESTION_ANCHOR_RE.test(id);
}

export function topicPage(unit, topicId) {
 if (!unit || !isLessonTopic(topicId)) return '';
 return `units/unit0${unit}/${topicId}.html`;
}

export function examplePage(unit, exampleId) {
 if (!unit || !exampleId) return '';
 return `units/unit0${unit}/ex-${exampleId}.html`;
}

export function resolveFocusLocation(focus) {
 const page = normalizePage(focus && focus.page);
 // 페이지·소단원·문항 판정은 언제나 비율을 뗀 id로 한다(스크롤용 비율은 여기서 버린다).
 const topicId = anchorId(focus && focus.topicAnchor);
 const unit = unitFromPage(page);
 const fromPage = pageTopicId(page);
 const exampleId = focus && focus.exampleId;
 // 예제가 지정되면 그 예제의 독립 페이지가 목적지다 — 소단원 페이지에는 더 이상 편집기가 없다.
 if (unit && exampleId) return {page: examplePage(unit, exampleId), topicAnchor: null};
 // 문항 앵커는 보낸 페이지(문제 페이지)를 그대로 두고 그 문항으로만 스크롤한다.
 if (QUESTION_ANCHOR_RE.test(topicId)) return {page: page || DEFAULT_PAGE, topicAnchor: topicId};
 const lesson = isLessonTopic(topicId) ? topicId : fromPage;
 if (unit && lesson) return {page: topicPage(unit, lesson), topicAnchor: lesson};
 return {page, topicAnchor: topicId || fromPage || null};
}

export function shouldNavigate(currentPage, focus) {
 if (!focus || !focus.page) return false;
 // currentPage는 이미 실제로 열려 있는 페이지(정규화된 최종 경로)이므로 그대로 비교한다.
 // 예전에는 이 자리에서도 resolveFocusLocation을 한 번 더 거쳤는데, q-math.html처럼
 // 문제 페이지에 있을 때 그 page를 다시 fromPage 경유로 math.html(소단원 페이지)로
 // 바꿔 버려 "이미 있는 페이지인데도 이동해야 한다"고 잘못 판단하는 문제가 있었다.
 const there = resolveFocusLocation(focus);
 return Boolean(there.page) && !samePage(currentPage, there.page);
}

export function focusHref(prefix, focus) {
 const loc = resolveFocusLocation(focus);
 if (!loc.page) return '';
 const pageTopic = pageTopicId(loc.page);
 const hash = loc.topicAnchor && loc.topicAnchor !== pageTopic ? `#${loc.topicAnchor}` : '';
 return `${prefix || ''}${loc.page}${hash}`;
}

export function focusKey(focus) {
 if (!focus) return '';
 return [
  normalizePage(focus.page),
  anchorId(focus.topicAnchor) || '',
  focus.exampleId || '',
  timestampMillis(focus.updatedAt)
 ].join('|');
}

export function topicFromHash(hash) {
 const id = String(hash || '').replace(/^#/, '');
 return /^[a-z0-9-]+$/.test(id) ? id : null;
}

export function visibleTopic(lessons, viewportTop = 120) {
 let current = null;
 for (const lesson of lessons || []) {
  if (!lesson || !lesson.id) continue;
  if (Number(lesson.top) <= viewportTop) current = lesson.id;
 }
 return current;
}

export function countPresence(rows, now = Date.now(), staleMs = PRESENCE_STALE_MS) {
 let following = 0, browsing = 0;
 for (const row of rows || []) {
  const at = timestampMillis(row && row.updatedAt);
  if (!at || now - at > staleMs) continue;
  if (row.following) following += 1;
  else browsing += 1;
 }
 return {following, browsing};
}

export function wholeNonce(value) {
 const n = Number(value);
 return Number.isFinite(n) && n >= 0 ? Math.trunc(n) : 0;
}

export function nextAttentionNonce(current) {
 return wholeNonce(current) + 1;
}

export function expiresAtMillis(now = Date.now()) {
 return now + SESSION_TTL_MS;
}

export function focusFields({page, topicAnchor, exampleId} = {}) {
 return {
  page: normalizePage(page) || DEFAULT_PAGE,
  topicAnchor: topicAnchor || null,
  exampleId: exampleId || null
 };
}

export function focusWritePayload(focus) {
 const fields = focusFields(focus || {});
 return {
  'focus.page': fields.page,
  'focus.topicAnchor': fields.topicAnchor,
  'focus.exampleId': fields.exampleId
 };
}

export function existingAttentionNonce(session) {
 return wholeNonce(session && session.attention && session.attention.nonce);
}

export function sessionStartChanged(prev, next) {
 const from = timestampMillis(prev && prev.startedAt);
 const to = timestampMillis(next && next.startedAt);
 return Boolean(to) && from !== to;
}

export function sessionFields({teacherEmail, page, topicAnchor, exampleId, attentionNonce} = {}) {
 return {
  active: true,
  teacherEmail: teacherEmail || '',
  focus: focusFields({page, topicAnchor, exampleId}),
  attention: {nonce: wholeNonce(attentionNonce)}
 };
}

export function sessionEndFields(existing, {teacherEmail} = {}) {
 const focus = (existing && existing.focus) || {};
 return {
  active: false,
  teacherEmail: (existing && existing.teacherEmail) || teacherEmail || '',
  focus: focusFields(focus),
  attention: {nonce: existingAttentionNonce(existing)}
 };
}

// topicAnchor를 함께 넘기면 practice.html에서도 문항 앵커일 때만 그 페이지를 초점 대상으로 허용한다
// (practice.html 자체는 소단원이 아니지만, 문항으로 스크롤하는 초점은 그 페이지에 머물러야 한다).
export function isUnitLessonPage(page, topicAnchor) {
 const path = normalizePage(page);
 if (/^units\/unit0[1-4]\/index\.html$/.test(path) || pageTopicId(path) || pageExampleId(path)) return true;
 if (/^units\/unit0[1-4]\/practice\.html$/.test(path) && QUESTION_ANCHOR_RE.test(anchorId(topicAnchor))) return true;
 return false;
}

const SKIP_FOCUS_TOPICS = new Set(['main', 'account', 'toast']);

export function resolveHref(href, currentPage) {
 if (href == null || typeof href !== 'string') return null;
 const raw = href.trim();
 if (!raw || raw === '#') return null;
 if (/^(mailto:|javascript:|tel:)/i.test(raw)) return null;
 try {
  const basePage = normalizePage(currentPage) || 'index.html';
  const url = new URL(raw, `https://progh2.github.io/aipy2/${basePage}`);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return null;
  return {page: pageFromPath(url.pathname), topicAnchor: topicFromHash(url.hash)};
 } catch {
  return null;
 }
}

export function focusFromUnitClick({href, exampleId, lessonId, currentPage} = {}) {
 const page = normalizePage(currentPage);
 if (exampleId && typeof exampleId === 'string' && exampleId.trim()) {
  return focusFields({
   page: page || DEFAULT_PAGE,
   topicAnchor: lessonId || pageTopicId(page) || null,
   exampleId: exampleId.trim()
  });
 }
 const resolved = resolveHref(href, page);
 if (!resolved || !isUnitLessonPage(resolved.page, resolved.topicAnchor)) return null;
 const topic = resolved.topicAnchor || pageTopicId(resolved.page);
 if (topic && SKIP_FOCUS_TOPICS.has(topic)) return null;
 if (!topic && samePage(resolved.page, page)) return null;
 return focusFields({
  page: resolved.page,
  topicAnchor: topic || null,
  exampleId: null
 });
}

export function presenceFields({classroom, page, topicAnchor, following}) {
 return {
  classroom: classroom || '',
  page: page || null,
  topicAnchor: topicAnchor || null,
  following: following !== false
 };
}

export function readPendingFocus(storage) {
 if (!storage) return null;
 try {
  const raw = storage.getItem(PENDING_FOCUS_KEY);
  if (!raw) return null;
  storage.removeItem(PENDING_FOCUS_KEY);
  const data = JSON.parse(raw);
  return data && typeof data === 'object' ? data : null;
 } catch {
  return null;
 }
}

export function followingStorageKey(classroom, session) {
 return `${FOLLOWING_KEY_PREFIX}${classroom || ''}:${timestampMillis(session && session.startedAt)}`;
}

export function readFollowing(storage, classroom, session) {
 if (!storage) return true;
 try {
  const raw = storage.getItem(followingStorageKey(classroom, session));
  if (raw === '0') return false;
  if (raw === '1') return true;
 } catch { /* 사생활 모드 등 */ }
 return true;
}

export function writeFollowing(storage, classroom, session, value) {
 if (!storage) return;
 try {
  storage.setItem(followingStorageKey(classroom, session), value ? '1' : '0');
 } catch { /* 사생활 모드 등 */ }
}

export function writePendingFocus(storage, focus) {
 if (!storage || !focus) return;
 try {
  storage.setItem(PENDING_FOCUS_KEY, JSON.stringify({
   page: focus.page || '',
   topicAnchor: focus.topicAnchor || null,
   exampleId: focus.exampleId || null
  }));
 } catch { /* 사생활 모드 등 */ }
}

export function catalogPages(catalog) {
 return (catalog && Array.isArray(catalog.pages)) ? catalog.pages : [];
}

export function catalogTopics(catalog, page) {
 const topics = catalog && catalog.topics;
 if (!topics || typeof topics !== 'object') return [];
 const key = normalizePage(page);
 if (topics[key]) return topics[key];
 const unit = unitFromPage(key);
 if (unit) return topics[`units/unit0${unit}/index.html`] || [];
 return [];
}

export function catalogExamples(catalog, topic) {
 if (!topic || !Array.isArray(topic.examples)) return [];
 const titles = (catalog && catalog.examples) || {};
 return topic.examples.map((id) => ({id, title: (titles[id] && titles[id].title) || id}));
}

export function emptyOption(label) {
 return {id: '', title: label};
}

// (#132) 학생이 새 창(연습문제 q-*·practice.html, 예제 ex-*, 튜토리얼 tut-*, 보강 자료
// extra-*)으로 연 탭은 수업 흐름의 "원래 탭"이 아니다. 교사 초점이 다른 페이지를 가리켜도
// 그 탭을 이동시키면 학생이 풀던 문제·읽던 자료가 사라진다 — 그래서 이동하지 않는다.
export function isPoppedPage(page) {
 const p = normalizePage(page);
 return /^units\/unit0[1-4]\/(q-[a-z0-9-]+\.html|practice\.html|ex-[a-z0-9-]+\.html|tut-[a-z0-9-]+\.html|extra-[a-z0-9-]+\.html)$/.test(p);
}

// 새 창(팝업) 여부는 window.opener 유무나 링크에 붙인 ?w=1 같은 쿼리 표식으로 판단한다.
// 이 함수는 그 판단 결과(isPopped)를 받아, popped 탭이면 순수하게 "이동할지/스크롤만 할지/
// 안내만 할지"를 결정한다 — DOM·location에는 손대지 않아 노드에서 표로 검증할 수 있다.
export function poppedFocusDecision(currentPage, focus, isPopped) {
 if (!isPopped) return {action: 'follow'};
 if (!focus || !focus.page) return {action: 'none'};
 const there = resolveFocusLocation(focus);
 if (!there.page) return {action: 'none'};
 if (samePage(currentPage, there.page)) return {action: 'scroll', topicAnchor: there.topicAnchor};
 return {action: 'notice'};
}

export function isPoppedTabMarker(search) {
 try {
  return new URLSearchParams(search || '').get('w') === '1';
 } catch {
  return false;
 }
}

// (#143) '의도적으로 다른 곳을 본다'의 판정. wheel·touchmove가 편집기·textarea·pre 같은
// 내부 스크롤 영역 안에서 일어나면 창(window)은 실제로 움직이지 않는다 — 그래서 창이 실제로
// 스크롤된 거리로만 판정한다. 프로그램(따라가기)이 스크롤을 거는 동안(ignoreUntil)에는 사용자
// 입력 때문이 아니므로 무시한다. lastFollowY가 아직 없으면(따라간 적이 없으면) 거리를 0으로 본다
// — 페이지를 막 열었을 때 바로 독립으로 튕기는 것을 막는다.
export function shouldMarkIndependent({lastFollowY, currentY, viewportH, ignoreUntil, now} = {}) {
 if ((now || 0) < (ignoreUntil || 0)) return false;
 if (!viewportH) return false;
 const base = lastFollowY == null ? currentY : lastFollowY;
 const dist = Math.abs((currentY || 0) - (base || 0));
 return dist >= viewportH * 0.6;
}

// (#143) '입력 중'을 활성 요소가 편집 가능하고, 최근(기본 6초) 안에 그 요소에서 input·keydown이
// 있었을 때로만 한정한다. 포커스가 남아 있기만 해서는(예: 저널 작성 후 그대로 둔 경우) '입력 중'이
// 아니다 — 그래야 이후 스크롤 초점을 계속 건너뛰는 문제가 없다.
export function isRecentlyEditing({focused, lastActivityAt, now, thresholdMs = 6000} = {}) {
 if (!focused || !lastActivityAt) return false;
 return (now || 0) - lastActivityAt < thresholdMs;
}
