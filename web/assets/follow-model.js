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

export function shouldNavigate(currentPage, focus) {
 return Boolean(focus && focus.page && !samePage(currentPage, focus.page));
}

export function focusHref(prefix, focus) {
 const page = normalizePage(focus && focus.page);
 if (!page) return '';
 const hash = focus.topicAnchor ? `#${focus.topicAnchor}` : '';
 return `${prefix || ''}${page}${hash}`;
}

export function focusKey(focus) {
 if (!focus) return '';
 return [
  normalizePage(focus.page),
  focus.topicAnchor || '',
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

export function isUnitLessonPage(page) {
 return /^units\/unit0[1-4]\/index\.html$/.test(normalizePage(page));
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
   topicAnchor: lessonId || null,
   exampleId: exampleId.trim()
  });
 }
 const resolved = resolveHref(href, page);
 if (!resolved || !isUnitLessonPage(resolved.page)) return null;
 if (resolved.topicAnchor && SKIP_FOCUS_TOPICS.has(resolved.topicAnchor)) return null;
 if (!resolved.topicAnchor && samePage(resolved.page, page)) return null;
 return focusFields({
  page: resolved.page,
  topicAnchor: resolved.topicAnchor,
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
 return (topics && topics[normalizePage(page)]) || [];
}

export function catalogExamples(catalog, topic) {
 if (!topic || !Array.isArray(topic.examples)) return [];
 const titles = (catalog && catalog.examples) || {};
 return topic.examples.map((id) => ({id, title: (titles[id] && titles[id].title) || id}));
}

export function emptyOption(label) {
 return {id: '', title: label};
}
