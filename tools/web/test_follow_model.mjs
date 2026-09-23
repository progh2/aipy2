/* follow-model 순수 함수 검사. node tools/web/test_follow_model.mjs */
import {
 isSessionLive, timestampMillis, pageFromPath, samePage, shouldNavigate, focusHref,
 focusKey, topicFromHash, visibleTopic, countPresence, nextAttentionNonce, wholeNonce,
 expiresAtMillis, sessionFields, sessionEndFields, existingAttentionNonce, sessionStartChanged,
 focusFields, focusWritePayload, focusFromUnitClick,
 isUnitLessonPage, presenceFields, readPendingFocus, writePendingFocus, readFollowing, writeFollowing,
 catalogTopics, catalogExamples, SESSION_TTL_MS, PRESENCE_STALE_MS, PENDING_FOCUS_KEY,
 DEFAULT_PAGE, isLessonTopic, resolveFocusLocation, pageTopicId, parseAnchor, anchorId
} from '../../web/assets/follow-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const now = 1_700_000_000_000;
eq(timestampMillis({seconds: 10, nanoseconds: 0}), 10000, 'timestamp seconds');
eq(isSessionLive(null, now), false, 'no session');
eq(isSessionLive({active: false, expiresAt: now + 1000}, now), false, 'inactive');
eq(isSessionLive({active: true, expiresAt: now - 1}, now), false, 'expired');
eq(isSessionLive({active: true, expiresAt: now + 1}, now), true, 'live');
eq(isSessionLive({active: true}, now), true, 'live without expiry');

eq(pageFromPath('/aipy2/units/unit01/index.html'), 'units/unit01/index.html', 'pages path');
eq(pageFromPath('/units/unit02/index.html'), 'units/unit02/index.html', 'local unit path');
eq(pageFromPath('/aipy2/'), 'index.html', 'site root');
eq(pageFromPath('/teacher/session.html'), 'teacher/session.html', 'teacher page');
eq(samePage('units/unit01/index.html', '/units/unit01/index.html'), true, 'same page');
eq(shouldNavigate('units/unit01/index.html', {page: 'units/unit02/index.html'}), true, 'other unit');
eq(shouldNavigate('units/unit01/index.html', {page: 'units/unit01/index.html'}), false, 'same unit');
eq(focusHref('../../', {page: 'units/unit03/index.html', topicAnchor: 'ml-overview'}),
 '../../units/unit03/ml-overview.html', 'focus href');
eq(shouldNavigate('units/unit01/overview.html', {page: 'units/unit01/index.html', topicAnchor: 'overview'}),
 false, 'topic page matches unit+anchor');
eq(shouldNavigate('units/unit01/overview.html', {page: 'units/unit01/index.html', topicAnchor: 'define'}),
 true, 'other topic navigates');
eq(topicFromHash('#overview'), 'overview', 'hash topic');
eq(topicFromHash('#bad id'), null, 'invalid hash');
eq(visibleTopic([{id: 'a', top: -20}, {id: 'b', top: 40}, {id: 'c', top: 400}], 120), 'b', 'visible topic');

eq(countPresence([
 {following: true, updatedAt: now - 1000},
 {following: false, updatedAt: now - 2000},
 {following: true, updatedAt: now - PRESENCE_STALE_MS - 1}
], now), {following: 1, browsing: 1}, 'presence counts skip stale');
eq(nextAttentionNonce(3), 4, 'nonce');
eq(wholeNonce(1.9), 1, 'whole nonce truncates');
eq(expiresAtMillis(now) - now, SESSION_TTL_MS, 'ttl');

const started = sessionFields({teacherEmail: 't@e-mirim.hs.kr', page: 'units/unit01/index.html', topicAnchor: 'overview'});
eq(started.active, true, 'session active');
eq(started.focus.page, 'units/unit01/index.html', 'session page');
eq(started.focus.topicAnchor, 'overview', 'session topic');
eq(started.focus.exampleId, null, 'session example default');
eq(Object.keys(started.focus).sort(), ['exampleId', 'page', 'topicAnchor'], 'focus keys always present');
eq(started.attention.nonce, 0, 'nonce whole');
eq(existingAttentionNonce(null), 0, 'missing session nonce');
eq(existingAttentionNonce({attention: {nonce: 4}}), 4, 'existing nonce');
eq(existingAttentionNonce({attention: {nonce: 4.8}}), 4, 'existing nonce trunc');
eq(sessionFields({teacherEmail: 't@e-mirim.hs.kr', attentionNonce: 7}).attention.nonce, 7, 'restart keeps nonce');
eq(sessionStartChanged({startedAt: 10}, {startedAt: 20}), true, 'startedAt changed');
eq(sessionStartChanged({startedAt: 10}, {startedAt: 10}), false, 'startedAt same');
eq(sessionStartChanged(null, {startedAt: 10}), true, 'first start has startedAt');
const ended = sessionEndFields({
 teacherEmail: 't@e-mirim.hs.kr',
 attention: {nonce: 3},
 focus: {page: 'units/unit01/index.html', topicAnchor: 'overview'}
});
eq(ended.active, false, 'end inactive');
eq(ended.attention.nonce, 3, 'end keeps nonce');
eq(ended.teacherEmail, 't@e-mirim.hs.kr', 'end keeps teacher');
eq(ended.focus.page, 'units/unit01/index.html', 'end keeps page');
eq(Object.keys(ended.focus).sort(), ['exampleId', 'page', 'topicAnchor'], 'end focus keys');
const bare = sessionFields({teacherEmail: 't@e-mirim.hs.kr'});
eq(bare.focus.topicAnchor, null, 'topic default null');
eq(bare.focus.exampleId, null, 'example default null');
eq('topicAnchor' in bare.focus && 'exampleId' in bare.focus, true, 'optional focus keys present');
eq(presenceFields({classroom: '2-3', following: false}).following, false, 'presence following');
eq(presenceFields({classroom: '2-3'}).following, true, 'presence default following');

const store = new Map();
const storage = {
 getItem: (key) => (store.has(key) ? store.get(key) : null),
 setItem: (key, value) => { store.set(key, String(value)); },
 removeItem: (key) => { store.delete(key); }
};
writePendingFocus(storage, {page: DEFAULT_PAGE, topicAnchor: 'define', exampleId: 'reuse'});
eq(storage.getItem(PENDING_FOCUS_KEY) != null, true, 'pending written');
eq(readPendingFocus(storage), {page: DEFAULT_PAGE, topicAnchor: 'define', exampleId: 'reuse'}, 'pending read');
eq(readPendingFocus(storage), null, 'pending consumed');
eq(readFollowing(storage, '2-3', {startedAt: now}), true, 'following default');
writeFollowing(storage, '2-3', {startedAt: now}, false);
eq(readFollowing(storage, '2-3', {startedAt: now}), false, 'following persisted');
eq(readFollowing(storage, '2-3', {startedAt: now + 1}), true, 'new session resets follow');

const catalog = {
 pages: [{id: 'units/unit01/index.html', label: 'Ⅰ 모듈'}],
 topics: {'units/unit01/index.html': [{id: 'overview', title: '개요', examples: ['reuse']}]},
 examples: {reuse: {title: '재사용'}}
};
eq(catalogTopics(catalog, 'units/unit01/index.html')[0].id, 'overview', 'catalog topics');
eq(catalogExamples(catalog, catalog.topics['units/unit01/index.html'][0])[0],
 {id: 'reuse', title: '재사용'}, 'catalog examples');
eq(focusKey({page: 'units/unit01/index.html', topicAnchor: 'a', exampleId: null, updatedAt: 9}),
 'units/unit01/index.html|a||9', 'focus key');

eq(isUnitLessonPage('units/unit01/index.html'), true, 'unit lesson page');
eq(isUnitLessonPage('units/unit01/overview.html'), true, 'topic lesson page');
eq(isUnitLessonPage('units/unit01/summary.html'), false, 'unit summary is not lesson');
eq(focusFields({page: 'units/unit02/index.html', topicAnchor: 'events'}),
 {page: 'units/unit02/index.html', topicAnchor: 'events', exampleId: null}, 'focus fields');
eq(focusWritePayload({page: 'units/unit01/index.html', topicAnchor: 'overview', exampleId: 'reuse'}),
 {'focus.page': 'units/unit01/index.html', 'focus.topicAnchor': 'overview', 'focus.exampleId': 'reuse'},
 'focus write payload');

const unit01 = 'units/unit01/index.html';
eq(focusFromUnitClick({href: '#overview', currentPage: unit01}),
 {page: unit01, topicAnchor: 'overview', exampleId: null}, 'toc topic click');
eq(focusFromUnitClick({href: '#lab', currentPage: unit01}),
 {page: unit01, topicAnchor: 'lab', exampleId: null}, 'lab anchor click');
eq(focusFromUnitClick({href: '#main', currentPage: unit01}), null, 'skip chrome hash');
eq(focusFromUnitClick({href: '../../units/unit01/index.html', currentPage: unit01}),
 null, 'same unit nav without topic');
eq(focusFromUnitClick({href: '../unit02/index.html', currentPage: unit01}),
 {page: 'units/unit02/index.html', topicAnchor: null, exampleId: null}, 'next unit page');
eq(focusFromUnitClick({href: '../unit02/index.html#define', currentPage: unit01}),
 {page: 'units/unit02/index.html', topicAnchor: 'define', exampleId: null}, 'other unit topic');
eq(focusFromUnitClick({href: 'widgets.html', currentPage: 'units/unit02/index.html'}),
 {page: 'units/unit02/widgets.html', topicAnchor: 'widgets', exampleId: null}, 'topic file click');
eq(focusFromUnitClick({href: 'summary.html', currentPage: unit01}), null, 'skip summary');
eq(focusFromUnitClick({href: '../../downloads/unit1-examples.zip', currentPage: unit01}),
 null, 'skip download');
eq(focusFromUnitClick({exampleId: 'reuse', lessonId: 'overview', currentPage: unit01}),
 {page: unit01, topicAnchor: 'overview', exampleId: 'reuse'}, 'example button');
eq(focusFromUnitClick({href: 'https://www.mtrschool.co.kr/post/3095', currentPage: unit01}),
 null, 'skip external');

// 문항 앵커는 소단원으로 오인되면 안 된다(없는 페이지로 이동하던 버그).
eq(isLessonTopic('u1-q041'), false, 'question anchor is not a lesson');
eq(isLessonTopic('widgets'), true, 'lesson id still ok');
eq(resolveFocusLocation({page: 'units/unit01/q-overview.html', topicAnchor: 'u1-q041'}),
 {page: 'units/unit01/q-overview.html', topicAnchor: 'u1-q041'}, 'question focus keeps its page');
eq(pageTopicId('units/unit01/q-overview.html'), 'overview', 'question page maps to its lesson');
eq(pageTopicId('units/unit01/practice.html'), null, 'unit practice page has no lesson topic');

// ── (#124) 앵커 정규화: '@비율'은 스크롤에만 쓴다. parseAnchor/anchorId가 그 규칙의 단일 출처다. ──
eq(parseAnchor('widgets@0.42'), {id: 'widgets', frac: 0.42}, 'parseAnchor splits id/ratio');
eq(parseAnchor('widgets'), {id: 'widgets', frac: null}, 'parseAnchor without ratio');
eq(parseAnchor(''), {id: '', frac: null}, 'parseAnchor empty');
eq(parseAnchor('u1-q041@1.5'), {id: 'u1-q041', frac: 0.99}, 'parseAnchor clamps ratio to 0.99');
eq(anchorId('u1-q041@0.3'), 'u1-q041', 'anchorId strips ratio');
eq(anchorId('u1-q041'), 'u1-q041', 'anchorId passthrough without ratio');
eq(anchorId(null), '', 'anchorId handles null');

// 회귀: 'u1-q042@0.3'(교사 스크롤 추적)이 문항 앵커로 인식되지 않아 q-math.html이 math.html로
// 바뀌던 사고(#124). 비율을 뗀 뒤에 문항인지 판정해야 한다.
eq(resolveFocusLocation({page: 'units/unit01/q-math.html', topicAnchor: 'u1-q042@0.3'}),
 {page: 'units/unit01/q-math.html', topicAnchor: 'u1-q042'}, 'question anchor with ratio keeps its question page');
eq(shouldNavigate('units/unit01/q-math.html', {page: 'units/unit01/q-math.html', topicAnchor: 'u1-q042@0.3'}),
 false, 'question anchor with ratio does not trigger navigation away');
eq(resolveFocusLocation({page: 'units/unit01/index.html', topicAnchor: 'widgets@0.4'}),
 {page: 'units/unit01/widgets.html', topicAnchor: 'widgets'}, 'lesson anchor with ratio resolves to its lesson page');
eq(
 focusKey({page: 'units/unit01/q-widgets.html', topicAnchor: 'u1-q041@0.1', exampleId: null, updatedAt: 5}),
 focusKey({page: 'units/unit01/q-widgets.html', topicAnchor: 'u1-q041@0.9', exampleId: null, updatedAt: 5}),
 'focusKey ignores ratio differences (ratio is scroll-only)'
);

// 표 기반 검사: 페이지 6종 × 앵커 3형식(소단원 id / 문항 id / 요소id@비율)의 모든 조합에서
// resolveFocusLocation이 항상 "실제로 존재할 수 있는 경로 형식"(units/unit0N/{무엇}.html)만 돌려주는지 확인한다.
// 빈 page(목적지 없음)는 애초에 이동하지 않으므로 형식 검사 대상에서 제외한다.
const TABLE_PAGES = [
 'units/unit01/index.html',      // 단원 인덱스
 'units/unit01/widgets.html',    // 소단원
 'units/unit01/ex-loop.html',    // 예제 전용 페이지
 'units/unit01/q-widgets.html',  // 문제 페이지
 'units/unit01/practice.html',   // 종합 문제 페이지
 'units/unit01/summary.html'     // 단원 정리 페이지
];
const TABLE_ANCHORS = [
 'widgets',       // 소단원 id
 'u1-q041',       // 문항 id
 'widgets@0.42',  // 교사 스크롤 추적(소단원 + 비율)
 'u1-q042@0.3'    // 교사 스크롤 추적(문항 + 비율)
];
const VALID_PAGE_SHAPE_RE = /^units\/unit0[1-4]\/[a-z0-9-]+\.html$/;
let tableChecked = 0;
for (const page of TABLE_PAGES) {
 for (const anchor of TABLE_ANCHORS) {
  const loc = resolveFocusLocation({page, topicAnchor: anchor});
  tableChecked += 1;
  if (loc.page && !VALID_PAGE_SHAPE_RE.test(loc.page)) {
   throw new Error(`resolveFocusLocation(${page}, ${anchor}) -> 존재할 수 없는 경로 형식: ${loc.page}`);
  }
  // topicAnchor로 남는 값도 비율이 없어야 한다(비율은 follow.js 쪽 scrollToId에서 원본 focus로 따로 쓴다).
  if (loc.topicAnchor && /@/.test(loc.topicAnchor)) {
   throw new Error(`resolveFocusLocation(${page}, ${anchor}) -> topicAnchor에 비율이 남음: ${loc.topicAnchor}`);
  }
 }
}
eq(tableChecked, TABLE_PAGES.length * TABLE_ANCHORS.length, 'resolveFocusLocation 조합 표 전부 검사함');
console.log(`PASS: resolveFocusLocation ${TABLE_PAGES.length}페이지 × ${TABLE_ANCHORS.length}앵커 조합 모두 유효한 경로 형식`);

// ── (#124) practice.html 초점: 문항 앵커는 페이지를 유지한 채 허용해야 한다. ──
eq(isUnitLessonPage('units/unit01/practice.html'), false, 'practice page alone is not a lesson page');
eq(isUnitLessonPage('units/unit01/practice.html', 'u1-q041'), true, 'practice page + question anchor is allowed');
eq(isUnitLessonPage('units/unit01/practice.html', 'u1-q041@0.3'), true, 'practice page + question anchor(ratio) is allowed');
eq(isUnitLessonPage('units/unit01/practice.html', 'widgets'), false, 'practice page + lesson anchor stays blocked');
eq(focusFromUnitClick({href: '#u1-q041', currentPage: 'units/unit01/practice.html'}),
 {page: 'units/unit01/practice.html', topicAnchor: 'u1-q041', exampleId: null}, 'practice page question anchor focus allowed');
eq(focusFromUnitClick({href: '#lab', currentPage: 'units/unit01/practice.html'}), null,
 'practice page non-question anchor stays blocked');

console.log('PASS: follow-model helpers');
