/* 참여 현황 보드(M4/F3) 순수 헬퍼. Firebase 없이 카드·히트맵·문항·CSV를 검사합니다.
   교사 화면은 progress·presence·help·roster를 실시간 구독하고, students/{uid}/state는
   학생 상세 패널을 열 때만 1회 조회합니다(#104 답안 보기). 여기 함수들은 그 문서를
   받아 답안·저널 목록으로 바꾸는 순수 변환만 맡습니다. */
import {inClass} from './class-picker.js';
import {
 asMap, isTopicId, studentLabel, normalizeUnderstanding, UNDERSTANDING_LABELS,
 historyItems, topicTitle, topicParts
} from './understanding-model.js';
import {sortOpenHelp} from './help-model.js';
import {timestampMillis, PRESENCE_HEARTBEAT_MS, PRESENCE_STALE_MS} from './follow-model.js';

// (#135) 예측·코드 읽기 답변을 소단원 아래로 붙이려면 예제id → {unit, topicId, title, keyLines}가
// 필요하다. catalog.topics[...][].examples가 이미 예제→소단원 대응을 담고 있으므로(#132),
// catalog.examples(제목·keyLines)와 합쳐 인덱스를 만든다.
export function exampleIndexFromCatalog(catalog) {
 const index = {};
 const topics = catalog && catalog.topics;
 const exampleMeta = asMap(catalog && catalog.examples);
 if (topics && typeof topics === 'object') {
  for (const [page, rows] of Object.entries(topics)) {
   const unitMatch = /unit0([1-4])/.exec(page);
   if (!unitMatch || !Array.isArray(rows)) continue;
   const unit = Number(unitMatch[1]);
   for (const row of rows) {
    if (!row || !row.id || !Array.isArray(row.examples)) continue;
    for (const eid of row.examples) {
     if (typeof eid !== 'string' || !eid) continue;
     const meta = exampleMeta[eid] || {};
     index[eid] = {unit, topicId: row.id, title: meta.title || eid, keyLines: Array.isArray(meta.keyLines) ? meta.keyLines : [], missions: Array.isArray(meta.missions) ? meta.missions : []};
    }
   }
  }
 }
 return index;
}

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
 const fileTopic = /unit0[1-4]\/([a-z0-9-]+)\.html$/.exec(page);
 const fromFile = fileTopic && fileTopic[1] !== 'index' && fileTopic[1] !== 'summary' ? fileTopic[1] : '';
 const anchor = presence.topicAnchor || fromFile;
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
 // progress는 반 필터 없이 전부 이메일로 먼저 색인한다(#123). 반 판정은 명단(roster)의 현재 반으로
 // 하고, progress 자체의 classroom 필드로 거르지 않는다 — 명단에서 반을 옮긴 학생의 progress 문서는
 // 다음 활동(코드 실행·저널 저장 등)까지 예전 반 값을 그대로 갖고 있어서, progress 기준으로 먼저
 // 거르면 옮긴 반에는 진행률 없는 카드만 남고 이전 반에는 유령 카드가 남는다.
 const rosterEmails = new Set();
 for (const row of roster || []) {
  if (row && row.archived === true) continue;
  const email = emailKey(row);
  if (email) rosterEmails.add(email);
 }
 const progressByEmail = new Map();
 for (const row of progress || []) {
  const email = emailKey(row);
  if (email) progressByEmail.set(email, row);
 }
 const usedProgress = new Set();
 const cards = [];
 // key 유일화용 순번. 이메일·uid가 모두 없는 비정상 데이터라도 이름만으로 충돌하지 않도록,
 // 다른 식별자가 하나도 없을 때만 이름#순번을 최후 수단으로 쓴다(#125-5).
 let fallbackIndex = 0;
 const nextFallback = () => { fallbackIndex += 1; return fallbackIndex; };
 for (const row of roster || []) {
  if (row && row.archived === true) continue;
  if (!inClass(row, classId)) continue;
  const email = emailKey(row);
  const matched = (email && progressByEmail.get(email)) || null;
  if (matched) usedProgress.add(matched);
  cards.push(makeCard({roster: row, progress: matched, presenceByUid, helpByUid, topicTotal, titles, now, nextFallback}));
 }
 // 명단에 없는 progress만 progress 자체의 반으로 판단한다(예: 퇴학·전출 등으로 명단에서 빠졌지만
 // 기록은 남아 있는 경우). 명단에 있지만 이번 반이 아닌 학생은 이미 자기 반 카드로 나왔으므로 제외.
 for (const row of progress || []) {
  if (usedProgress.has(row)) continue;
  const email = emailKey(row);
  if (email && rosterEmails.has(email)) continue;
  if (!inClass(row, classId)) continue;
  cards.push(makeCard({roster: null, progress: row, presenceByUid, helpByUid, topicTotal, titles, now, nextFallback}));
 }
 return cards;
}

// 카드 key는 명단 문서 id → progress 문서 id → 이메일 → uid 순으로 고른다. 넷 다 없는
// 비정상 데이터에서만 이름#순번으로 유일화한다(이름만 쓰면 동명이인 카드가 서로 덮어쓴다).
function cardKey(roster, progress, person, nextFallback) {
 if (roster && roster.id) return `r:${roster.id}`;
 if (progress && progress.id) return `p:${progress.id}`;
 const email = emailKey(person);
 if (email) return email;
 if (person && person.uid) return person.uid;
 return `${studentLabel(person) || '학생'}#${nextFallback ? nextFallback() : ''}`;
}

function makeCard({roster, progress, presenceByUid, helpByUid, topicTotal, titles, now, nextFallback}) {
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
  key: cardKey(roster, progress, person, nextFallback),
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

// 학생 카드는 학번순으로 고정한다(2026-09 수업 요청). 학번이 없는 카드는 뒤로.
export function sortStudentCards(cards) {
 return (cards || []).slice().sort((a, b) => {
  const idA = a && a.studentId ? String(a.studentId) : '';
  const idB = b && b.studentId ? String(b.studentId) : '';
  if (idA && idB && idA !== idB) return idA.localeCompare(idB, 'ko', {numeric: true});
  if (idA !== idB) return idA ? -1 : 1;
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

// 학생 상세 패널(#104) — students/{uid}/state/current 문서(sync-model.js의 statePayload 모양:
// {answers, journals, ...})와 catalog.questions를 합쳐 답안 목록을 만든다.
export const UNIT_ROMAN = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ'];

// '선택'(5지선다)만 정답을 고르는 객관식이고, 나머지는 직접 입력하는 주관식으로 본다.
export const SUBJECTIVE_KINDS = ['서술', '구현', '오류 수정', '예측', '빈칸'];

export function isSubjectiveKind(kind) {
 return SUBJECTIVE_KINDS.includes(kind);
}

export const ANSWER_STATUS_LABELS = {done: '정답', retry: '다시 풀기'};

export function answerStatusLabel(row) {
 const status = row && row.status;
 if (status && ANSWER_STATUS_LABELS[status]) return ANSWER_STATUS_LABELS[status];
 const value = row && row.value;
 const hasValue = Array.isArray(value) ? value.length > 0 : value != null && String(value).trim() !== '';
 return hasValue ? '제출' : '미제출';
}

export function formatAnswerValue(value) {
 if (Array.isArray(value)) return value.map((item) => String(item)).join(' → ');
 if (value == null) return '';
 return String(value);
}

// 문항별 답안 한 줄. state.answers에 기록이 있는 문항만 돌려준다(#104).
export function answerRows(state, questions = []) {
 const answers = asMap(state && state.answers);
 const index = new Map();
 for (const q of questions || []) {
  if (q && q.id) index.set(q.id, q);
 }
 const rows = [];
 for (const [id, rec] of Object.entries(answers)) {
  if (!rec || typeof rec !== 'object') continue;
  const q = index.get(id) || {};
  rows.push({
   id,
   unit: q.unit ?? (topicParts(id) ? topicParts(id).unit : null),
   topic: q.topic || '',
   prompt: q.prompt || id,
   kind: q.kind || '',
   options: Array.isArray(q.options) ? q.options : null,
   correctAnswer: q.answer != null ? q.answer : null,
   status: rec.status || '',
   attempts: Number(rec.attempts) || 0,
   value: rec.value,
   feedback: rec.feedback || ''
  });
 }
 rows.sort((a, b) => (Number(a.unit) || 0) - (Number(b.unit) || 0) || a.id.localeCompare(b.id));
 return rows;
}

export function filterAnswerRows(rows, mode) {
 const list = rows || [];
 if (mode === 'retry') return list.filter((row) => row.status === 'retry');
 if (mode === 'subjective') return list.filter((row) => isSubjectiveKind(row.kind));
 return list;
}

export function groupAnswerRowsByUnit(rows) {
 const map = new Map();
 for (const row of rows || []) {
  const unit = row && row.unit != null ? Number(row.unit) : 0;
  if (!map.has(unit)) map.set(unit, []);
  map.get(unit).push(row);
 }
 return [...map.entries()].sort((a, b) => a[0] - b[0]);
}

// 단원별 '푼 문항/전체 문항/정답 수' — catalog 전체 문항 기준이라 필터와 무관하게 고정된 값이다.
export function unitAnswerTotals(state, questions = []) {
 const answers = asMap(state && state.answers);
 const totals = new Map();
 for (const q of questions || []) {
  if (!q || q.id == null || q.unit == null) continue;
  const unit = Number(q.unit);
  if (!totals.has(unit)) totals.set(unit, {unit, total: 0, answered: 0, correct: 0});
  const bucket = totals.get(unit);
  bucket.total += 1;
  const rec = answers[q.id];
  if (!rec || typeof rec !== 'object') continue;
  const value = rec.value;
  const hasValue = Array.isArray(value) ? value.length > 0 : value != null && String(value).trim() !== '';
  if (hasValue || Number(rec.attempts) > 0) {
   bucket.answered += 1;
   if (rec.status === 'done') bucket.correct += 1;
  }
 }
 return [...totals.values()].sort((a, b) => a.unit - b.unit);
}

// 학습 저널 3칸(u{n}-learn/error/next)을 단원별로 묶는다. 빈 칸은 건너뛴다.
// #130: 소단원 저널(j-u{n}-{anchor})도 같은 단원 그룹에 topic 항목으로 합친다.
export const JOURNAL_LABELS = {learn: '이해한 개념', error: '오류와 해결', next: '다음 도전'};
const JOURNAL_ORDER = ['learn', 'error', 'next'];
const TOPIC_JOURNAL_RE = /^j-(u([1-4])-.+)$/;
// #132 '직접 해 보세요' 항목 답변과 제출 표시. d-u{단원}-{소단원id}-{번호} / -submitted.
const TASK_ITEM_RE = /^d-u([1-4])-(.+)-(\d+)$/;
const TASK_SUBMIT_RE = /^d-u([1-4])-(.+)-submitted$/;

// (#135) 예측 p-{예제id}[-match|-why|-actual] / 코드 읽기 c-{예제id}-{ref}. 예제id 자체에
// 하이픈이 들어 있어(예: 'cv-yolo-count') 정규식만으로는 못 나누므로, exampleIndex가 아는
// id 중 가장 긴 것부터 접두로 시도한다.
function matchExampleId(rest, exampleIds) {
 for (const id of exampleIds) {
  if (rest === id) return {id, suffix: ''};
  if (rest.startsWith(`${id}-`)) return {id, suffix: rest.slice(id.length + 1)};
 }
 return null;
}

export function journalRows(state, titles, tasks, exampleIndex) {
 const journals = asMap(state && state.journals);
 const taskLabels = asMap(tasks);
 const examples = asMap(exampleIndex);
 const exampleIds = Object.keys(examples).sort((a, b) => b.length - a.length);
 const byUnit = new Map();
 const topicItems = new Map();
 const taskEntries = new Map(); // `${unit}::${topicId}::${i}` -> {unit, topicId, i, text}
 const taskSubmitted = new Map(); // `${unit}::${topicId}` -> ISO 시각 문자열
 const predictEntries = new Map(); // exampleId -> {predict, match, why, actual}
 const codeReadEntries = new Map(); // exampleId -> [{ref, text}]
 const missionEntries = new Map(); // exampleId -> [{n, at}]
 for (const [key, text] of Object.entries(journals)) {
  const value = typeof text === 'string' ? text.trim() : '';
  const submitMatch = TASK_SUBMIT_RE.exec(key);
  if (submitMatch && value) {
   taskSubmitted.set(`${submitMatch[1]}::${submitMatch[2]}`, value);
   continue;
  }
  if (exampleIds.length && key.startsWith('p-') && value) {
   const found = matchExampleId(key.slice(2), exampleIds);
   if (found) {
    const rec = predictEntries.get(found.id) || {};
    if (found.suffix === '') rec.predict = value;
    else if (found.suffix === 'match') rec.match = value;
    else if (found.suffix === 'why') rec.why = value;
    else if (found.suffix === 'actual') rec.actual = value;
    predictEntries.set(found.id, rec);
    continue;
   }
  }
  if (exampleIds.length && key.startsWith('c-') && value) {
   const found = matchExampleId(key.slice(2), exampleIds);
   if (found && found.suffix) {
    if (!codeReadEntries.has(found.id)) codeReadEntries.set(found.id, []);
    codeReadEntries.get(found.id).push({ref: found.suffix, text: value});
    continue;
   }
  }
  // (#135-3) 변형 미션 통과 시각. m-{예제id}-{번호} = ISO 시각 문자열.
  if (exampleIds.length && key.startsWith('m-') && value) {
   const found = matchExampleId(key.slice(2), exampleIds);
   if (found && /^\d+$/.test(found.suffix)) {
    if (!missionEntries.has(found.id)) missionEntries.set(found.id, []);
    missionEntries.get(found.id).push({n: Number(found.suffix), at: value});
    continue;
   }
  }
  if (!value) continue;
  const unitMatch = /^u([1-4])-(learn|error|next)$/.exec(key);
  if (unitMatch) {
   const unit = Number(unitMatch[1]);
   if (!byUnit.has(unit)) byUnit.set(unit, {});
   byUnit.get(unit)[unitMatch[2]] = value;
   continue;
  }
  const taskMatch = TASK_ITEM_RE.exec(key);
  if (taskMatch) {
   const [, unitStr, topicId, iStr] = taskMatch;
   taskEntries.set(`${unitStr}::${topicId}::${iStr}`, {unit: Number(unitStr), topicId, i: Number(iStr), text: value});
   continue;
  }
  const topicMatch = TOPIC_JOURNAL_RE.exec(key);
  if (topicMatch) {
   const topicId = topicMatch[1];
   const unit = Number(topicMatch[2]);
   if (!topicItems.has(unit)) topicItems.set(unit, []);
   topicItems.get(unit).push({key: topicId, label: topicTitle(topicId, titles), text: value, topicId});
  }
 }
 for (const entry of taskEntries.values()) {
  const {unit, topicId, i, text} = entry;
  const taskLabel = taskLabels[`u${unit}-${topicId}-${i}`] || '';
  const label = `직접 해 보세요 ${i}${taskLabel ? `: ${taskLabel}` : ''}`;
  const submittedAt = taskSubmitted.get(`${unit}::${topicId}`) || '';
  if (!topicItems.has(unit)) topicItems.set(unit, []);
  topicItems.get(unit).push({
   key: `${topicId}-task${i}`,
   label: `${topicTitle(`u${unit}-${topicId}`, titles)} · ${label}`,
   text,
   topicId: `${topicId}-task${i}`,
   submitted: Boolean(submittedAt),
   submittedAt
  });
 }
 for (const [eid, rec] of predictEntries.entries()) {
  const meta = examples[eid];
  if (!meta || !rec.predict) continue;
  const matchWord = rec.match === 'same' ? '같았어요' : rec.match === 'diff' ? '달랐어요' : '';
  let text = rec.predict;
  if (rec.actual) text += `\n실제/PC 결과: ${rec.actual}`;
  if (rec.why) text += `\n왜 달랐나요: ${rec.why}`;
  if (!topicItems.has(meta.unit)) topicItems.set(meta.unit, []);
  topicItems.get(meta.unit).push({
   key: `${meta.topicId}-predict-${eid}`,
   label: `${topicTitle(`u${meta.unit}-${meta.topicId}`, titles)} · 예제 ${meta.title} · 예측${matchWord ? ` (${matchWord})` : ''}`,
   text,
   topicId: `${meta.topicId}-predict-${eid}`
  });
 }
 for (const [eid, lines] of codeReadEntries.entries()) {
  const meta = examples[eid];
  if (!meta) continue;
  const codeByRef = new Map((meta.keyLines || []).map((kl) => [kl.ref, kl.code]));
  for (const {ref, text} of lines) {
   const code = codeByRef.get(ref) || '';
   if (!topicItems.has(meta.unit)) topicItems.set(meta.unit, []);
   topicItems.get(meta.unit).push({
    key: `${meta.topicId}-code-${eid}-${ref}`,
    label: `${topicTitle(`u${meta.unit}-${meta.topicId}`, titles)} · 예제 ${meta.title} · 줄 ${ref}${code ? ` \`${code}\`` : ''} 설명`,
    text,
    topicId: `${meta.topicId}-code-${eid}-${ref}`
   });
  }
 }
 for (const [eid, entries] of missionEntries.entries()) {
  const meta = examples[eid];
  if (!meta) continue;
  for (const {n, at} of entries) {
   const level = (meta.missions && meta.missions[n - 1] && meta.missions[n - 1].level) || '';
   const when = at ? new Date(at).toLocaleString('ko-KR') : '';
   if (!topicItems.has(meta.unit)) topicItems.set(meta.unit, []);
   topicItems.get(meta.unit).push({
    key: `${meta.topicId}-mission-${eid}-${n}`,
    label: `${topicTitle(`u${meta.unit}-${meta.topicId}`, titles)} · 예제 ${meta.title} · 미션 ${n}${level ? `(${level})` : ''} 통과 ${when}`,
    text: '통과',
    topicId: `${meta.topicId}-mission-${eid}-${n}`
   });
  }
 }
 const units = new Set([...byUnit.keys(), ...topicItems.keys()]);
 return [...units]
  .sort((a, b) => a - b)
  .map((unit) => {
   const entries = byUnit.get(unit) || {};
   const unitLevelItems = JOURNAL_ORDER.filter((key) => entries[key]).map((key) => ({key, label: JOURNAL_LABELS[key], text: entries[key]}));
   const topicLevelItems = (topicItems.get(unit) || []).sort((a, b) => a.topicId.localeCompare(b.topicId));
   return {unit, items: [...unitLevelItems, ...topicLevelItems]};
  })
  .filter((row) => row.items.length > 0);
}

export {studentLabel, historyItems, UNDERSTANDING_LABELS};
