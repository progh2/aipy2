/* 주제별 이해도(M3/F5) 순수 헬퍼. Firebase 없이 값·이력·집계를 검사합니다.
   저장 키는 complete와 같은 u1-overview 형식이고, 값은 짧은 영문 토큰입니다. */

export const UNDERSTANDING_KEY = 'aipy-understanding-v1';
export const UNDERSTANDING_WRITE_MS = 900;
export const COMMENT_MAX = 200;
export const UNDERSTANDING_MAX_KEYS = 80;
export const TOPIC_ID_RE = /^u[1-4]-[a-z0-9-]+$/;
export const UNDERSTANDING_VALUES = ['understood', 'somewhat', 'hard'];
export const UNDERSTANDING_LABELS = {
 understood: '이해했어요',
 somewhat: '조금 어려워요',
 hard: '어려워요'
};
export const HARD_PROMPT = '어디가 막혔나요?';
export const NOT_GRADED = '평가에 반영되지 않습니다';
export const NOT_GRADED_NOTE = '이 신호는 평가에 반영되지 않습니다. 막힌 곳을 찾기 위한 표시예요.';

export function asMap(value) {
 return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

export function isTopicId(id) {
 return typeof id === 'string' && TOPIC_ID_RE.test(id) && id.length <= 40;
}

export function isUnderstandingValue(value) {
 return UNDERSTANDING_VALUES.includes(value);
}

export function clipComment(text) {
 if (text == null) return '';
 return String(text).replace(/\s+/g, ' ').trim().slice(0, COMMENT_MAX);
}

export function normalizeUnderstanding(raw) {
 const out = {};
 for (const [key, value] of Object.entries(asMap(raw))) {
  if (Object.keys(out).length >= UNDERSTANDING_MAX_KEYS) break;
  if (isTopicId(key) && isUnderstandingValue(value)) out[key] = value;
 }
 return out;
}

export function normalizeComments(raw) {
 const out = {};
 for (const [key, value] of Object.entries(asMap(raw))) {
  if (!isTopicId(key)) continue;
  const text = clipComment(value);
  if (text) out[key] = text;
 }
 return out;
}

export function emptyUnderstandingStore() {
 return {version: 1, values: {}, comments: {}};
}

export function normalizeStore(raw) {
 const store = emptyUnderstandingStore();
 if (!raw || typeof raw !== 'object') return store;
 const values = raw.values !== undefined ? raw.values : raw;
 store.values = normalizeUnderstanding(values);
 store.comments = normalizeComments(raw.comments);
 return store;
}

export function mergeUnderstanding(local, cloud) {
 return {...normalizeUnderstanding(cloud), ...normalizeUnderstanding(local)};
}

export function mergeStores(localRaw, cloudRaw) {
 const local = normalizeStore(localRaw);
 const cloud = normalizeStore(cloudRaw);
 return {
  version: 1,
  values: mergeUnderstanding(local.values, cloud.values),
  comments: {...cloud.comments, ...local.comments}
 };
}

export function setUnderstanding(store, topicId, value) {
 const next = normalizeStore(store);
 if (!isTopicId(topicId) || !isUnderstandingValue(value)) return next;
 next.values = {...next.values, [topicId]: value};
 return next;
}

export function setComment(store, topicId, text) {
 const next = normalizeStore(store);
 if (!isTopicId(topicId)) return next;
 const clipped = clipComment(text);
 next.comments = {...next.comments};
 if (clipped) next.comments[topicId] = clipped;
 else delete next.comments[topicId];
 return next;
}

export function historyItems(values) {
 const items = [];
 for (const [topicId, value] of Object.entries(normalizeUnderstanding(values))) {
  if (value === 'understood') continue;
  items.push({topicId, value, label: UNDERSTANDING_LABELS[value]});
 }
 const rank = {hard: 0, somewhat: 1};
 items.sort((a, b) => (rank[a.value] - rank[b.value]) || a.topicId.localeCompare(b.topicId));
 return items;
}

export function topicParts(topicId) {
 const match = /^u([1-4])-(.+)$/.exec(topicId || '');
 if (!match) return null;
 return {unit: Number(match[1]), anchor: match[2]};
}

export function topicHref(prefix, topicId) {
 const parts = topicParts(topicId);
 if (!parts) return '';
 return `${prefix || ''}units/unit0${parts.unit}/index.html#${parts.anchor}`;
}

export function titlesFromCatalog(catalog) {
 const titles = {};
 const topics = catalog && catalog.topics;
 if (!topics || typeof topics !== 'object') return titles;
 for (const [page, rows] of Object.entries(topics)) {
  const unit = /unit0([1-4])/.exec(page);
  if (!unit || !Array.isArray(rows)) continue;
  for (const row of rows) {
   if (!row || !row.id) continue;
   titles[`u${unit[1]}-${row.id}`] = row.title || row.id;
  }
 }
 return titles;
}

export function titlesFromLessons(lessons, unit) {
 const titles = {};
 const n = Number(unit);
 if (!Number.isInteger(n) || n < 1 || n > 4) return titles;
 for (const lesson of lessons || []) {
  if (!lesson || !lesson.id) continue;
  titles[`u${n}-${lesson.id}`] = lesson.title || lesson.id;
 }
 return titles;
}

export function topicTitle(topicId, titles) {
 const map = asMap(titles);
 return map[topicId] || topicId;
}

export function studentLabel(row) {
 if (!row || typeof row !== 'object') return '학생';
 const id = row.studentId != null && String(row.studentId).trim() ? String(row.studentId).trim() : '';
 const name = typeof row.name === 'string' ? row.name.trim() : '';
 return [id, name].filter(Boolean).join(' ') || row.email || '학생';
}

export function countUnderstanding(rows) {
 const counts = {understood: 0, somewhat: 0, hard: 0};
 const hardRows = [];
 for (const row of rows || []) {
  const values = normalizeUnderstanding(row && row.understanding);
  for (const [topicId, value] of Object.entries(values)) {
   counts[value] += 1;
   if (value === 'hard') {
    hardRows.push({
     uid: row.uid || '',
     studentId: row.studentId ?? null,
     name: row.name || '',
     email: row.email || '',
     topicId,
     value
    });
   }
  }
 }
 hardRows.sort((a, b) => a.topicId.localeCompare(b.topicId) || studentLabel(a).localeCompare(studentLabel(b), 'ko'));
 return {counts, hardRows};
}

export function groupHardByTopic(hardRows) {
 const map = new Map();
 for (const row of hardRows || []) {
  const id = row && row.topicId;
  if (!id) continue;
  if (!map.has(id)) map.set(id, []);
  map.get(id).push(row);
 }
 return [...map.entries()].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0]));
}

export function shouldWriteAfter(lastAt, now, gap = UNDERSTANDING_WRITE_MS) {
 if (!lastAt) return true;
 return Number(now) - Number(lastAt) >= gap;
}

export function feedbackId(uid, topicId) {
 if (!uid || !isTopicId(topicId)) return '';
 return `${uid}_${topicId}`;
}

export function feedbackFields({profile, topicId, text} = {}) {
 const person = profile && typeof profile === 'object' ? profile : {};
 return {
  uid: person.uid || '',
  email: person.email || '',
  studentId: person.studentId ?? null,
  admissionYear: person.admissionYear ?? null,
  name: typeof person.name === 'string' ? person.name : '',
  grade: person.grade ?? null,
  classroom: person.classroom ?? null,
  number: person.number ?? null,
  topicId: isTopicId(topicId) ? topicId : '',
  text: clipComment(text)
 };
}
