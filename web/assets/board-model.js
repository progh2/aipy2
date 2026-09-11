/* 참여 현황 보드(M4/F3) 순수 헬퍼. Firebase 없이 카드·히트맵·문항·CSV를 검사합니다.
   교사 화면은 progress·presence·help·roster만 읽고, students/{uid}/state는 읽지 않습니다. */
import {inClass} from './class-picker.js';
import {
 asMap, isTopicId, studentLabel, normalizeUnderstanding, UNDERSTANDING_LABELS,
 historyItems, topicTitle, topicParts
} from './understanding-model.js';
import {sortOpenHelp} from './help-model.js';
import {timestampMillis, PRESENCE_HEARTBEAT_MS, PRESENCE_STALE_MS} from './follow-model.js';

export const PRESENCE_FRESH_MS = PRESENCE_HEARTBEAT_MS;
export const PRESENCE_RECENT_MS = PRESENCE_STALE_MS;
export const CSV_HEADER = ['학번', '이름', '번호', '접속', '현재 위치', '완료율', '정답률', '도움', '이해도', '마지막 활동'];

export function topicListFromCatalog(catalog) {
 const list = [];
 const topics = catalog && catalog.topics;
 if (!topics || typeof topics !== 'object') return list;
 for (const [page, rows] of Object.entries(topics)) {
  const unit = /unit0([1-4])/.exec(page);
  if (!unit || !Array.isArray(rows)) continue;
  let index = 0;
  for (const row of rows) {
   if (!row || !row.id) continue;
   index += 1;
   list.push({
    id: `u${unit[1]}-${row.id}`,
    unit: Number(unit[1]),
    anchor: row.id,
    title: row.title || row.id,
    short: `${unit[1]}.${index}`,
    page
   });
  }
 }
 return list;
}

export function completedTopicIds(counts) {
 const done = counts && counts.done;
 if (!Array.isArray(done)) return [];
 return done.filter((id) => isTopicId(id));
}

export function completeRate(doneCount, topicTotal) {
 const total = Number(topicTotal) || 0;
 if (!total) return 0;
 const n = Number(doneCount) || 0;
 return Math.min(1, Math.max(0, n / total));
}

export function studentAccuracy(counts) {
 const answers = asMap(counts && counts.answers);
 const ids = Object.keys(answers);
 if (ids.length) {
  const correct = ids.filter((id) => Number(answers[id] && answers[id].correct) > 0).length;
  return {correct, attempted: ids.length, attempts: ids.reduce((sum, id) => sum + (Number(answers[id] && answers[id].attempts) || 0), 0), rate: correct / ids.length};
 }
 const questions = counts && counts.questions;
 const correct = Number(questions && questions.correct) || 0;
 const attempts = Number(questions && questions.attempts) || 0;
 if (!correct && !attempts) return {correct: 0, attempted: 0, attempts: 0, rate: null};
 return {correct, attempted: 0, attempts, rate: null};
}

export function formatRate(rate) {
 if (rate == null || !Number.isFinite(rate)) return '—';
 return `${Math.round(rate * 100)}%`;
}

export function presenceFreshness(updatedAt, now = Date.now()) {
 const at = timestampMillis(updatedAt);
 if (!at) return {online: false, label: '오프라인', ageMs: Infinity};
 const age = Math.max(0, now - at);
 if (age <= PRESENCE_FRESH_MS) return {online: true, label: '1분 이내', ageMs: age};
 if (age <= PRESENCE_RECENT_MS) return {online: true, label: '3분 이내', ageMs: age};
 return {online: false, label: '오프라인', ageMs: age};
}

export function currentPlace(presence, titles) {
 if (!presence || typeof presence !== 'object') return '';
 const parts = [];
 const page = typeof presence.page === 'string' ? presence.page : '';
 const unit = /unit0([1-4])/.exec(page);
 if (unit) parts.push(`${['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ'][Number(unit[1])]}`);
 const anchor = presence.topicAnchor;
 if (anchor && unit) {
  const id = `u${unit[1]}-${anchor}`;
  parts.push(topicTitle(id, titles));
 } else if (anchor) parts.push(anchor);
 else if (page) parts.push(page.replace(/^units\//, '').replace(/\/index\.html$/, ''));
 return parts.filter(Boolean).join(' · ');
}

export function worstUnderstanding(values) {
 const map = normalizeUnderstanding(values);
 if (map && Object.values(map).includes('hard')) return 'hard';
 if (map && Object.values(map).includes('somewhat')) return 'somewhat';
 if (map && Object.values(map).includes('understood')) return 'understood';
 return '';
}

export function understandingSummary(values) {
 const map = normalizeUnderstanding(values);
 const counts = {hard: 0, somewhat: 0, understood: 0};
 for (const value of Object.values(map)) counts[value] += 1;
 const parts = [];
 if (counts.hard) parts.push(`어려워요 ${counts.hard}`);
 if (counts.somewhat) parts.push(`조금 어려워요 ${counts.somewhat}`);
 if (counts.understood) parts.push(`이해했어요 ${counts.understood}`);
 return parts.join(' · ') || '—';
}

export function formatActivity(value) {
 const ms = timestampMillis(value);
 if (!ms) return '—';
 try {
  return new Date(ms).toLocaleString('ko-KR', {month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'});
 } catch {
  return '—';
 }
}

function emailKey(row) {
 if (!row || typeof row !== 'object') return '';
 const email = row.email != null ? String(row.email).trim().toLowerCase() : '';
 if (email) return email;
 const id = row.id != null ? String(row.id).trim().toLowerCase() : '';
 return id.includes('@') ? id : '';
}

function numberRank(value) {
 const n = Number(value);
 return Number.isInteger(n) ? n : Number.POSITIVE_INFINITY;
}

export function heatmapTone(done, understanding) {
 if (understanding === 'hard') return 'hard';
 if (understanding === 'somewhat') return 'somewhat';
 if (done && understanding === 'understood') return 'understood';
 if (done) return 'done';
 if (understanding === 'understood') return 'understood';
 return 'empty';
}

export function isStuckOnTopic(card, topicId) {
 if (!card || !topicId) return false;
 const done = card.done instanceof Set ? card.done.has(topicId) : (card.done || []).includes(topicId);
 const signal = normalizeUnderstanding(card.understanding)[topicId] || '';
 return !done || signal === 'hard' || signal === 'somewhat';
}

export function filterStuck(cards, topicId) {
 if (!topicId) return cards || [];
 return (cards || []).filter((card) => isStuckOnTopic(card, topicId));
}

export function buildStudentCards({roster = [], progress = [], presence = [], help = [], classId, topics = [], titles = {}, now = Date.now()} = {}) {
 const topicTotal = topics.length;
 const helpByUid = new Map();
 for (const row of sortOpenHelp(help)) {
  const uid = row && row.uid;
  if (!uid) continue;
  if (!helpByUid.has(uid)) helpByUid.set(uid, []);
  helpByUid.get(uid).push(row);
 }
 const presenceByUid = new Map();
 for (const row of presence || []) {
  const uid = (row && (row.uid || row.id)) || '';
  if (uid) presenceByUid.set(uid, row);
 }
 const progressByEmail = new Map();
 const progressByUid = new Map();
 for (const row of progress || []) {
  if (!inClass(row, classId)) continue;
  const email = emailKey(row);
  if (email) progressByEmail.set(email, row);
  const uid = row.uid || row.id || '';
  if (uid) progressByUid.set(uid, row);
 }
 const usedProgress = new Set();
 const cards = [];
 for (const row of roster || []) {
  if (!inClass(row, classId)) continue;
  const email = emailKey(row);
  const matched = (email && progressByEmail.get(email)) || null;
  if (matched) usedProgress.add(matched);
  cards.push(makeCard({roster: row, progress: matched, presenceByUid, helpByUid, topicTotal, titles, now}));
 }
 for (const row of progress || []) {
  if (!inClass(row, classId) || usedProgress.has(row)) continue;
  cards.push(makeCard({roster: null, progress: row, presenceByUid, helpByUid, topicTotal, titles, now}));
 }
 return cards;
}

function makeCard({roster, progress, presenceByUid, helpByUid, topicTotal, titles, now}) {
 const person = progress || roster || {};
 const uid = person.uid || (progress && progress.id) || '';
 const live = uid ? presenceByUid.get(uid) : null;
 const fresh = presenceFreshness(live && live.updatedAt, now);
 const counts = (progress && progress.counts) || {};
 const done = completedTopicIds(counts);
 const accuracy = studentAccuracy(counts);
 const understanding = normalizeUnderstanding(progress && progress.understanding);
 const helpRows = uid ? (helpByUid.get(uid) || []) : [];
 const worst = worstUnderstanding(understanding);
 const lastRaw = (counts && counts.lastActivity) || (progress && progress.updatedAt) || 0;
 return {
  key: emailKey(person) || uid || studentLabel(person),
  uid,
  email: emailKey(person),
  studentId: roster && roster.studentId != null ? roster.studentId : (person.studentId ?? ''),
  name: (roster && roster.name) || person.name || '',
  number: roster && roster.number != null ? roster.number : person.number,
  label: studentLabel({
   studentId: roster && roster.studentId != null ? roster.studentId : person.studentId,
   name: (roster && roster.name) || person.name,
   email: emailKey(person)
  }),
  online: fresh.online,
  presenceLabel: fresh.label,
  page: (live && live.page) || '',
  topicAnchor: (live && live.topicAnchor) || '',
  place: currentPlace(live, titles),
  done,
  doneCount: done.length,
  topicTotal,
  completeRate: completeRate(done.length, topicTotal),
  accuracy: accuracy.rate,
  correct: accuracy.correct,
  attempted: accuracy.attempted,
  attempts: accuracy.attempts,
  openHelp: helpRows.length,
  helpRows,
  understanding,
  understandingLabel: UNDERSTANDING_LABELS[worst] || '—',
  understandingSummary: understandingSummary(understanding),
  lastActivity: lastRaw,
  lastActivityLabel: formatActivity(lastRaw)
 };
}

export function sortStudentCards(cards) {
 return (cards || []).slice().sort((a, b) => {
  const helpA = a && a.openHelp > 0 ? 1 : 0;
  const helpB = b && b.openHelp > 0 ? 1 : 0;
  if (helpA !== helpB) return helpB - helpA;
  const rateA = a && Number.isFinite(a.completeRate) ? a.completeRate : 0;
  const rateB = b && Number.isFinite(b.completeRate) ? b.completeRate : 0;
  if (rateA !== rateB) return rateA - rateB;
  const num = numberRank(a && a.number) - numberRank(b && b.number);
  if (num) return num;
  return studentLabel(a).localeCompare(studentLabel(b), 'ko');
 });
}

export function classQuestionTotals(progressRows) {
 let attempts = 0, correct = 0, students = 0;
 for (const row of progressRows || []) {
  const questions = row && row.counts && row.counts.questions;
  if (!questions) continue;
  const a = Number(questions.attempts) || 0;
  const c = Number(questions.correct) || 0;
  attempts += a;
  correct += c;
  if (a || c) students += 1;
 }
 return {attempts, correct, students, avgAttempts: students ? attempts / students : null};
}

export function questionStats(progressRows, questions = []) {
 const index = new Map();
 for (const item of questions || []) {
  if (!item || !item.id) continue;
  index.set(item.id, {id: item.id, unit: item.unit ?? null, topic: item.topic || '', attempts: 0, correct: 0, students: 0});
 }
 for (const row of progressRows || []) {
  const answers = asMap(row && row.counts && row.counts.answers);
  for (const [id, rec] of Object.entries(answers)) {
   if (!index.has(id)) index.set(id, {id, unit: topicParts(id) ? topicParts(id).unit : null, topic: '', attempts: 0, correct: 0, students: 0});
   const item = index.get(id);
   const attempts = Number(rec && rec.attempts) || 0;
   const correct = Number(rec && rec.correct) || 0;
   item.attempts += attempts;
   item.correct += correct;
   if (attempts || correct) item.students += 1;
  }
 }
 const rows = [...index.values()].filter((row) => row.students > 0 || row.attempts > 0);
 for (const row of rows) {
  row.correctRate = row.students ? row.correct / row.students : null;
  row.avgAttempts = row.students ? row.attempts / row.students : null;
 }
 rows.sort((a, b) => {
  const ra = a.correctRate == null ? 2 : a.correctRate;
  const rb = b.correctRate == null ? 2 : b.correctRate;
  if (ra !== rb) return ra - rb;
  return b.attempts - a.attempts || a.id.localeCompare(b.id);
 });
 return rows;
}

export function csvCell(value) {
 const text = value == null ? '' : String(value);
 if (/[",\n\r]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
 return text;
}

export function classCsv(cards) {
 const lines = [CSV_HEADER.map(csvCell).join(',')];
 for (const card of cards || []) {
  lines.push([
   card.studentId,
   card.name,
   card.number ?? '',
   card.presenceLabel,
   card.place,
   formatRate(card.completeRate),
   card.accuracy == null ? (card.attempts ? `정답 ${card.correct} · 시도 ${card.attempts}` : '—') : formatRate(card.accuracy),
   card.openHelp,
   card.understandingSummary,
   card.lastActivityLabel
  ].map(csvCell).join(','));
 }
 return `${lines.join('\n')}\n`;
}

export function cardAccuracyLabel(card) {
 if (!card) return '—';
 if (card.accuracy != null) return formatRate(card.accuracy);
 if (card.correct || card.attempts) return `정답 ${card.correct} · 시도 ${card.attempts}`;
 return '—';
}

export {studentLabel, historyItems, UNDERSTANDING_LABELS};
