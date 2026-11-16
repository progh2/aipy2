/* 학생용 '내 학습 기록' 순수 집계 함수. DOM·Firebase 없이 node로 검사한다.
   입력은 학생 한 명의 학습 상태(localStorage 'aipy-lab-v1' 또는 students/{uid}/state/current와
   같은 모양)와 data/catalog.json이다. 답안·저널 가공은 교사 화면과 같은 함수를 재사용한다. */
import {answerRows} from './board-model.js?v=q135b';
import {titlesFromCatalog, tasksFromCatalog} from './understanding-model.js';
import {exampleIndexFromCatalog, topicListFromCatalog} from './board-model.js?v=q135b';
import {buildStudentDetailSections} from './teacher-answers-model.js?v=q145a';

export const FILTERS = [
 {id: 'all', label: '전체'},
 {id: 'todo', label: '안 한 것만'},
 {id: 'nojournal', label: '저널 안 쓴 곳'},
 {id: 'wrong', label: '틀린 문제 다시 보기'}
];

function map(value) {
 return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function hasValue(value) {
 return Array.isArray(value) ? value.length > 0 : value != null && String(value).trim() !== '';
}

// 문항 하나를 푼 것으로 보는 기준: 답이 비어 있지 않거나 시도 기록이 있다(board-model unitAnswerTotals와 같음).
export function isAnswered(rec) {
 return Boolean(rec && typeof rec === 'object' && (hasValue(rec.value) || Number(rec.attempts) > 0));
}

export function buildMyRecord(state, catalog) {
 const st = state && typeof state === 'object' ? state : {};
 const complete = map(st.complete);
 const answers = map(st.answers);
 const journals = map(st.journals);
 const titles = titlesFromCatalog(catalog);
 const tasks = tasksFromCatalog(catalog);
 const exampleIndex = exampleIndexFromCatalog(catalog);
 const topics = topicListFromCatalog(catalog);
 const questions = Array.isArray(catalog && catalog.questions) ? catalog.questions : [];
 const rowTopics = new Map();
 for (const [page, rows] of Object.entries((catalog && catalog.topics) || {})) {
  for (const row of rows || []) if (row && row.id) rowTopics.set(`${page}::${row.id}`, row);
 }
 const sections = buildStudentDetailSections(st, {titles, tasks, exampleIndex, questions, topics});
 const sectionByKey = new Map();
 for (const u of sections) for (const s of u.subunits) sectionByKey.set(`${u.unit}::${s.topic}`, s);
 const allRows = answerRows(st, questions);

 const units = [];
 for (const t of topics) {
  let unit = units.find((u) => u.unit === t.unit);
  if (!unit) {
   unit = {unit: t.unit, subunits: [], totals: {topics: 0, done: 0, questions: 0, answered: 0, correct: 0, journals: 0}};
   units.push(unit);
  }
  const meta = rowTopics.get(`${t.page}::${t.anchor}`) || {};
  const qs = questions.filter((q) => q && q.unit === t.unit && q.topic === t.anchor);
  const qIds = new Set(qs.map((q) => q.id));
  const answered = qs.filter((q) => isAnswered(answers[q.id]));
  const correct = answered.filter((q) => answers[q.id].status === 'done');
  const rows = allRows.filter((r) => qIds.has(r.id));
  const wrongRows = rows.filter((r) => r.status !== 'done');
  const journalText = typeof journals[`j-u${t.unit}-${t.anchor}`] === 'string' ? journals[`j-u${t.unit}-${t.anchor}`].trim() : '';
  const section = sectionByKey.get(`${t.unit}::${t.anchor}`);
  const ownKey = `u${t.unit}-${t.anchor}`;
  const extraItems = section ? section.journalItems.filter((it) => it.topicId !== ownKey) : [];
  const taskItems = extraItems.filter((it) => /-task\d+$/.test(it.topicId || ''));
  const otherItems = extraItems.filter((it) => !/-task\d+$/.test(it.topicId || ''));
  const done = Boolean(complete[ownKey]);
  const sub = {
   unit: t.unit,
   anchor: t.anchor,
   key: ownKey,
   title: t.title,
   short: t.short,
   href: meta.href || `units/unit0${t.unit}/${t.anchor}.html`,
   practiceHref: meta.practiceHref || `units/unit0${t.unit}/q-${t.anchor}.html`,
   done,
   qTotal: qs.length,
   qAnswered: answered.length,
   qCorrect: correct.length,
   qUnanswered: qs.length - answered.length,
   rows,
   wrongRows,
   journal: journalText,
   hasJournal: journalText !== '',
   taskTotal: Array.isArray(meta.tasks) ? meta.tasks.length : 0,
   taskItems,
   otherItems
  };
  sub.needsWork = !sub.done || sub.qUnanswered > 0;
  unit.subunits.push(sub);
  const tot = unit.totals;
  tot.topics += 1;
  if (done) tot.done += 1;
  tot.questions += qs.length;
  tot.answered += answered.length;
  tot.correct += correct.length;
  if (sub.hasJournal) tot.journals += 1;
 }
 units.sort((a, b) => a.unit - b.unit);
 const overall = {topics: 0, done: 0, questions: 0, answered: 0, correct: 0, journals: 0};
 for (const u of units) for (const k of Object.keys(overall)) overall[k] += u.totals[k];
 overall.rate = overall.topics ? Math.round((overall.done / overall.topics) * 100) : 0;
 return {units, overall, todo: nextTodo(units), empty: overall.done === 0 && overall.answered === 0 && overall.journals === 0 &&
  !units.some((u) => u.subunits.some((s) => s.taskItems.length || s.otherItems.length))};
}

// 안 한 소단원(완료 체크 안 함 또는 안 푼 문제 있음)을 교과서 순서대로 모은다.
export function nextTodo(units) {
 const list = [];
 for (const u of units || []) {
  for (const s of u.subunits) {
   if (!s.needsWork) continue;
   const reasons = [];
   if (!s.done) reasons.push('완료 체크 안 함');
   if (s.qUnanswered > 0) reasons.push(`안 푼 문제 ${s.qUnanswered}개`);
   list.push({unit: s.unit, anchor: s.anchor, title: s.title, href: s.href, practiceHref: s.practiceHref, done: s.done, reasons});
  }
 }
 return list;
}

export function subunitMatches(sub, mode) {
 if (mode === 'todo') return sub.needsWork;
 if (mode === 'nojournal') return !sub.hasJournal;
 if (mode === 'wrong') return sub.wrongRows.length > 0;
 return true;
}

// 필터에 맞는 소단원만 남긴 새 목록. 소단원이 하나도 없는 단원은 뺀다.
export function filterRecord(record, mode) {
 const units = [];
 for (const u of record.units) {
  const subunits = u.subunits.filter((s) => subunitMatches(s, mode));
  if (subunits.length) units.push({...u, subunits});
 }
 return units;
}

export function percent(part, whole) {
 return whole > 0 ? Math.round((part / whole) * 100) : 0;
}

// 인쇄·화면 공용 상태 배지 문구.
export function statusBadges(sub) {
 const out = [{tone: sub.done ? 'good' : 'warn', text: sub.done ? '완료' : '완료 안 함'}];
 if (sub.qTotal > 0) out.push({tone: sub.qUnanswered === 0 ? 'good' : 'muted', text: `문제 ${sub.qAnswered}/${sub.qTotal}`});
 out.push({tone: sub.hasJournal ? 'good' : 'muted', text: sub.hasJournal ? '저널 있음' : '저널 없음'});
 return out;
}
