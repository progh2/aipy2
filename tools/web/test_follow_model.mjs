/* follow-model 순수 함수 검사. node tools/web/test_follow_model.mjs */
import {
 isSessionLive, timestampMillis, pageFromPath, samePage, shouldNavigate, focusHref,
 focusKey, topicFromHash, visibleTopic, countPresence, nextAttentionNonce, wholeNonce,
 expiresAtMillis, sessionFields, focusFields, focusWritePayload, focusFromUnitClick,
 isUnitLessonPage, presenceFields, readPendingFocus, writePendingFocus, readFollowing, writeFollowing,
 catalogTopics, catalogExamples, SESSION_TTL_MS, PRESENCE_STALE_MS, PENDING_FOCUS_KEY,
 DEFAULT_PAGE
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
 '../../units/unit03/index.html#ml-overview', 'focus href');
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
eq(focusFromUnitClick({href: 'summary.html', currentPage: unit01}), null, 'skip summary');
eq(focusFromUnitClick({href: '../../downloads/unit1-examples.zip', currentPage: unit01}),
 null, 'skip download');
eq(focusFromUnitClick({exampleId: 'reuse', lessonId: 'overview', currentPage: unit01}),
 {page: unit01, topicAnchor: 'overview', exampleId: 'reuse'}, 'example button');
eq(focusFromUnitClick({href: 'https://www.mtrschool.co.kr/post/3095', currentPage: unit01}),
 null, 'skip external');

console.log('PASS: follow-model helpers');
