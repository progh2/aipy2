/* 답변 내역 페이지(#128, #145) 순수 헬퍼. Firebase 없이 검사할 수 있는 부분만 모은다.
   학생 목록·상세 그룹핑은 board-model.js의 answerRows/journalRows/buildStudentCards를 그대로 쓰고,
   여기서는 그 결과를 반별→학생별 화면에 맞게 다듬는 함수만 추가한다(중복 구현 금지). */
import {topicTitle} from './understanding-model.js';
import {projectDiffSummary} from './code-diff-model.js?v=q135d';
import {answerRows, journalRows, csvCell, formatAnswerValue, formatRate} from './board-model.js?v=q135b';

// answerRows()가 만든 목록을 단원 → 소단원(topic anchor) 순으로 더 세분화해서 묶는다.
// board.html 학생 상세는 단원 단위로만 접지만, 답변 내역 페이지는 소단원별로 봐야 한다.
export function groupAnswerRowsBySubunit(rows, titles = {}) {
 const map = new Map();
 for (const row of rows || []) {
  const unit = row && row.unit != null ? Number(row.unit) : 0;
  const topic = (row && row.topic) || '';
  const key = `${unit}::${topic}`;
  if (!map.has(key)) {
   map.set(key, {
    unit,
    topic,
    topicTitle: topic ? topicTitle(`u${unit}-${topic}`, titles) : '',
    rows: []
   });
  }
  map.get(key).rows.push(row);
 }
 return [...map.values()].sort((a, b) => a.unit - b.unit || a.topic.localeCompare(b.topic));
}

// 학생 목록 카드 한 줄 요약. board-model.js buildStudentCards()가 만든 카드를 받는다.
export function studentSummaryLabel(card) {
 if (!card) return '';
 const attempted = Number(card.attempted) || 0;
 const correct = Number(card.correct) || 0;
 const doneCount = Number(card.doneCount) || 0;
 const topicTotal = Number(card.topicTotal) || 0;
 return `답변 ${attempted} · 정답 ${correct} · 완료 ${doneCount}/${topicTotal}`;
}

// state(students/{uid}/state/current)에 답안·저널·예제 프로젝트 기록이 하나라도 있는지 — 없으면
// "아직 제출한 답변이 없습니다" 안내로 대체한다.
export function hasAnswerRecord(state) {
 const answers = state && state.answers;
 if (answers && typeof answers === 'object') {
  for (const rec of Object.values(answers)) {
   if (!rec || typeof rec !== 'object') continue;
   const value = rec.value;
   const hasValue = Array.isArray(value) ? value.length > 0 : value != null && String(value).trim() !== '';
   if (hasValue || Number(rec.attempts) > 0) return true;
  }
 }
 const journals = state && state.journals;
 if (journals && typeof journals === 'object') {
  for (const text of Object.values(journals)) {
   if (typeof text === 'string' && text.trim()) return true;
  }
 }
 const projects = state && state.projects;
 if (projects && typeof projects === 'object' && Object.keys(projects).length) return true;
 return false;
}

// 학생이 저장한 예제 프로젝트(state.projects)를 소단원별로 묶어 원본과의 diff를 붙인다(#135-4).
// exampleIndex는 board-model.js의 exampleIndexFromCatalog() 결과(eid -> {unit, topicId, title}).
// originalFilesById는 화면 쪽이 unit{n}.json에서 이미 읽어 온 eid -> files 맵이다 — 아직 못 읽었거나
// 원본을 찾을 수 없는 예제는 조용히 건너뛴다(원본을 확인하지 못한 채 "수정함/동일"을 단정하지 않는다).
export function groupProjectRowsBySubunit(projects, exampleIndex, originalFilesById, titles = {}) {
 const map = new Map();
 for (const [eid, proj] of Object.entries(projects || {})) {
  const meta = exampleIndex && exampleIndex[eid];
  if (!meta) continue;
  const origFiles = originalFilesById && originalFilesById[eid];
  if (!origFiles) continue;
  const studentFiles = (proj && typeof proj === 'object' && proj.files) || {};
  const diff = projectDiffSummary(origFiles, studentFiles);
  const unit = Number(meta.unit) || 0;
  const topic = meta.topicId || '';
  const key = `${unit}::${topic}`;
  if (!map.has(key)) {
   map.set(key, {
    unit,
    topic,
    topicTitle: topic ? topicTitle(`u${unit}-${topic}`, titles) : '',
    items: []
   });
  }
  map.get(key).items.push({id: eid, title: meta.title || eid, diff});
 }
 return [...map.values()]
  .map((group) => ({...group, items: group.items.sort((a, b) => a.title.localeCompare(b.title))}))
  .sort((a, b) => a.unit - b.unit || a.topic.localeCompare(b.topic));
}

// 아직 원본을 못 읽었거나(fetch 대기) exampleIndex가 없는 항목이 있는지 — 있으면 화면이 unit{n}.json을
// 더 받아 와야 한다. 단원 번호 집합을 돌려준다.
export function pendingProjectUnits(projects, exampleIndex, originalFilesById) {
 const units = new Set();
 for (const eid of Object.keys(projects || {})) {
  const meta = exampleIndex && exampleIndex[eid];
  if (!meta) continue;
  if (originalFilesById && originalFilesById[eid]) continue;
  units.add(Number(meta.unit) || 0);
 }
 return [...units].filter(Boolean);
}

// ---------------------------------------------------------------------------
// #145 A: 학생 상세 정리 개선 — 단원 → 소단원(교과서 목차 순) 섹션 구성, 반 전체 표, CSV.
// ---------------------------------------------------------------------------

const UNIT_LEVEL_KEYS = ['learn', 'error', 'next'];

// journalRows()가 돌려주는 topic-level 항목의 topicId는 형태가 섞여 있다 — 소단원 저널(j-u{n}-{anchor})은
// 'u{unit}-{anchor}' 그대로지만, 직접 해 보세요/예측/코드 읽기/미션 항목은 유닛 접두 없이
// '{anchor}-task1' 'anchor-predict-eid' 식이다(matchExampleId와 같은 '제일 긴 후보부터' 접두 비교가 필요).
// anchors(그 단원의 소단원 anchor 목록)와 대조해 실제 소단원 anchor를 복원한다.
export function anchorForJournalItem(item, unit, anchors) {
 const topicId = (item && item.topicId) || '';
 const prefix = `u${unit}-`;
 const rest = topicId.startsWith(prefix) ? topicId.slice(prefix.length) : topicId;
 const sorted = (anchors || []).slice().sort((a, b) => b.length - a.length);
 for (const anchor of sorted) {
  if (rest === anchor || rest.startsWith(`${anchor}-`)) return anchor;
 }
 return rest;
}

// 단원 → 소단원(교과서 목차 순, topics는 topicListFromCatalog() 결과) 섹션 뼈대를 만든다.
// 카탈로그에 있는 소단원은 입력이 전혀 없어도 포함한다(화면에서 '입력 없음'으로 접어서 보여 줄 수 있게).
// 예제 코드(projects) 섹션은 원본 코드를 async로 받아야 해서 여기 포함하지 않는다 —
// mergeProjectGroupsIntoSections()로 화면 쪽에서 나중에 합친다.
export function buildStudentDetailSections(state, {titles = {}, tasks = {}, exampleIndex = {}, questions = [], topics = []} = {}) {
 const rows = answerRows(state, questions);
 const answerGroups = new Map(groupAnswerRowsBySubunit(rows, titles).map((g) => [`${g.unit}::${g.topic}`, g]));
 const jr = journalRows(state, titles, tasks, exampleIndex);

 const anchorsByUnit = new Map();
 for (const t of topics || []) {
  if (!t || t.unit == null || !t.anchor) continue;
  if (!anchorsByUnit.has(t.unit)) anchorsByUnit.set(t.unit, []);
  anchorsByUnit.get(t.unit).push(t.anchor);
 }

 const unitJournalByUnit = new Map();
 const topicJournalByKey = new Map();
 for (const group of jr) {
  const unitLevel = group.items.filter((it) => UNIT_LEVEL_KEYS.includes(it.key));
  if (unitLevel.length) unitJournalByUnit.set(group.unit, unitLevel);
  const anchors = anchorsByUnit.get(group.unit) || [];
  for (const item of group.items) {
   if (UNIT_LEVEL_KEYS.includes(item.key)) continue;
   const anchor = anchorForJournalItem(item, group.unit, anchors);
   const key = `${group.unit}::${anchor}`;
   if (!topicJournalByKey.has(key)) topicJournalByKey.set(key, []);
   topicJournalByKey.get(key).push(item);
  }
 }

 const catalogKeys = new Set();
 const orderedKeys = [];
 for (const t of topics || []) {
  const key = `${t.unit}::${t.anchor}`;
  if (catalogKeys.has(key)) continue;
  catalogKeys.add(key);
  orderedKeys.push(key);
 }
 for (const key of answerGroups.keys()) {
  if (!catalogKeys.has(key) && !orderedKeys.includes(key)) orderedKeys.push(key);
 }
 for (const key of topicJournalByKey.keys()) {
  if (!catalogKeys.has(key) && !orderedKeys.includes(key)) orderedKeys.push(key);
 }

 const byUnit = new Map();
 for (const key of orderedKeys) {
  const sep = key.indexOf('::');
  const unit = Number(key.slice(0, sep));
  const anchor = key.slice(sep + 2);
  const answerGroup = answerGroups.get(key);
  const journalItems = topicJournalByKey.get(key) || [];
  const catalogTopic = (topics || []).find((t) => t.unit === unit && t.anchor === anchor);
  const sub = {
   topic: anchor,
   topicTitle: (catalogTopic && catalogTopic.title) || (answerGroup && answerGroup.topicTitle) || topicTitle(`u${unit}-${anchor}`, titles),
   answers: answerGroup ? answerGroup.rows : [],
   journalItems,
   projectItems: [],
   hasContent: Boolean((answerGroup && answerGroup.rows.length) || journalItems.length)
  };
  if (!byUnit.has(unit)) byUnit.set(unit, []);
  byUnit.get(unit).push(sub);
 }

 const units = [...new Set([...byUnit.keys(), ...unitJournalByUnit.keys()])].sort((a, b) => a - b);
 return units.map((unit) => ({
  unit,
  subunits: byUnit.get(unit) || [],
  unitJournal: unitJournalByUnit.get(unit) || []
 }));
}

// 예제 코드 그룹(groupProjectRowsBySubunit() 결과)을 buildStudentDetailSections() 결과에 합친다.
// 카탈로그에 이미 있는 소단원이면 그 subunit.projectItems를 채우고, 없으면(드문 경우) 그 단원
// 끝에 새 소단원을 덧붙인다. 입력 전용 객체를 변형하지 않고 새 배열/객체를 돌려준다.
export function mergeProjectGroupsIntoSections(sections, projectGroups) {
 const result = (sections || []).map((u) => ({...u, subunits: u.subunits.map((s) => ({...s, projectItems: s.projectItems || []}))}));
 const byKey = new Map();
 for (const u of result) for (const s of u.subunits) byKey.set(`${u.unit}::${s.topic}`, s);
 for (const g of projectGroups || []) {
  const key = `${g.unit}::${g.topic}`;
  const existing = byKey.get(key);
  if (existing) {
   existing.projectItems = g.items;
   existing.hasContent = true;
   continue;
  }
  let unitRow = result.find((u) => u.unit === g.unit);
  if (!unitRow) {
   unitRow = {unit: g.unit, subunits: [], unitJournal: []};
   result.push(unitRow);
  }
  const sub = {topic: g.topic, topicTitle: g.topicTitle, answers: [], journalItems: [], projectItems: g.items, hasContent: true};
  unitRow.subunits.push(sub);
  byKey.set(key, sub);
 }
 result.sort((a, b) => a.unit - b.unit);
 return result;
}

// 학생 상세 상단 요약 줄. card는 board-model.js buildStudentCards() 결과 한 개(완료율·정답률은 거기서),
// 저널·과제·미션 수는 journalRows()를 다시 훑어 센다(화면이 answerRows/journalRows를 또 만들지 않게).
export function summarizeStudentActivity(state, card, {titles = {}, tasks = {}, exampleIndex = {}} = {}) {
 const jr = journalRows(state, titles, tasks, exampleIndex);
 let journalCount = 0;
 let taskSubmittedCount = 0;
 let missionPassCount = 0;
 for (const group of jr) {
  for (const item of group.items) {
   journalCount += 1;
   if (typeof item.topicId === 'string' && item.topicId.includes('-mission-')) missionPassCount += 1;
   if (item.submitted === true) taskSubmittedCount += 1;
  }
 }
 return {
  doneCount: (card && card.doneCount) || 0,
  topicTotal: (card && card.topicTotal) || 0,
  completeRate: card ? card.completeRate : null,
  correct: (card && card.correct) || 0,
  attempted: (card && card.attempted) || 0,
  accuracy: card ? card.accuracy : null,
  journalCount,
  taskSubmittedCount,
  missionPassCount,
  lastActivityLabel: (card && card.lastActivityLabel) || '—'
 };
}

// 반 전체 한눈 표의 열(소단원) 정의. topics는 topicListFromCatalog() 결과.
export function classOverviewColumns(topics) {
 return (topics || []).map((t) => ({unit: t.unit, topic: t.anchor, topicTitle: t.title, short: t.short, key: `${t.unit}::${t.anchor}`}));
}

// 학생 1명의 반 전체 표 행. stateEntry는 class-state-loader.js loadStatesForUids()가 만든
// {status, data?} 항목. 아직 못 불러왔으면(status가 'ready'가 아니면) cells를 빈 채로 둔다.
export function buildClassOverviewRow(card, stateEntry, {titles = {}, tasks = {}, exampleIndex = {}, questions = [], topics = []} = {}) {
 const cells = {};
 const status = stateEntry ? stateEntry.status : 'pending';
 if (stateEntry && stateEntry.status === 'ready') {
  const state = stateEntry.data || {};
  const rows = answerRows(state, questions);
  const answerGroups = groupAnswerRowsBySubunit(rows, titles);
  for (const g of answerGroups) {
   const key = `${g.unit}::${g.topic}`;
   const cell = cells[key] || {correct: 0, attempted: 0, journal: 0};
   for (const row of g.rows) {
    cell.attempted += 1;
    if (row.status === 'done') cell.correct += 1;
   }
   cells[key] = cell;
  }
  const anchorsByUnit = new Map();
  for (const t of topics || []) {
   if (!anchorsByUnit.has(t.unit)) anchorsByUnit.set(t.unit, []);
   anchorsByUnit.get(t.unit).push(t.anchor);
  }
  const jr = journalRows(state, titles, tasks, exampleIndex);
  for (const group of jr) {
   const anchors = anchorsByUnit.get(group.unit) || [];
   for (const item of group.items) {
    if (UNIT_LEVEL_KEYS.includes(item.key)) continue;
    const anchor = anchorForJournalItem(item, group.unit, anchors);
    const key = `${group.unit}::${anchor}`;
    const cell = cells[key] || {correct: 0, attempted: 0, journal: 0};
    cell.journal += 1;
    cells[key] = cell;
   }
  }
 }
 return {key: card.key, uid: card.uid, label: card.label, studentId: card.studentId, status, cells};
}

// 표 셀 한 칸 텍스트. 입력이 전혀 없으면 빈 문자열(화면이 '·'로 대체).
export function classOverviewCellLabel(cell) {
 if (!cell) return '';
 const parts = [];
 if (cell.attempted) parts.push(`${cell.correct}/${cell.attempted}`);
 if (cell.journal) parts.push(`✎${cell.journal}`);
 return parts.join(' ');
}

// ---- CSV 내보내기 --------------------------------------------------------

function toCsvText(rows) {
 return rows.map((row) => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
}

// 엑셀에서 한글이 깨지지 않도록 UTF-8 BOM을 붙인 CSV 문자열을 돌려준다.
export function withBom(csvText) {
 return `﻿${csvText}`;
}

// 반 전체 요약 CSV(학생별 1행). summaries는 uid -> summarizeStudentActivity() 결과 Map.
export function classSummaryCsvRows(cards, summaries) {
 const header = ['학번', '이름', '완료 소단원', '전체 소단원', '정답', '시도', '정답률', '저널·과제 작성', '미션 통과', '마지막 활동'];
 const rows = [header];
 for (const card of cards || []) {
  const s = (summaries && summaries.get(card.uid)) || {};
  rows.push([
   card.studentId ?? '',
   card.name || card.label || '',
   s.doneCount ?? 0,
   s.topicTotal ?? 0,
   s.correct ?? 0,
   s.attempted ?? 0,
   s.accuracy != null ? formatRate(s.accuracy) : '—',
   s.journalCount ?? 0,
   s.missionPassCount ?? 0,
   s.lastActivityLabel || '—'
  ]);
 }
 return rows;
}

export function classSummaryCsv(cards, summaries) {
 return withBom(toCsvText(classSummaryCsvRows(cards, summaries)));
}

// 반 전체 '긴 형식' CSV — 학생 한 명의 문항 답 1건, 저널·과제 1건이 각각 한 행.
// statesByUid는 class-state-loader.js 결과 Map(uid -> {status, data?}).
export function classLongCsvRows(cards, statesByUid, {titles = {}, tasks = {}, exampleIndex = {}, questions = []} = {}) {
 const header = ['학번', '이름', '단원', '소단원', '항목종류', '키', '내용', '정답여부', '시각'];
 const rows = [header];
 for (const card of cards || []) {
  const entry = statesByUid && statesByUid.get(card.uid);
  if (!entry || entry.status !== 'ready') continue;
  const state = entry.data || {};
  const name = card.name || card.label || '';
  for (const row of answerRows(state, questions)) {
   rows.push([
    card.studentId ?? '', name, row.unit ?? '', row.topic || '', '문항', row.id,
    formatAnswerValue(row.value), row.status === 'done' ? '정답' : (row.status === 'retry' ? '다시풀기' : ''), ''
   ]);
  }
  for (const group of journalRows(state, titles, tasks, exampleIndex)) {
   for (const item of group.items) {
    rows.push([
     card.studentId ?? '', name, group.unit, item.topicId || item.key || '', '저널·과제', item.key,
     item.text || '', '', item.submittedAt || ''
    ]);
   }
  }
 }
 return rows;
}

export function classLongCsv(cards, statesByUid, opts) {
 return withBom(toCsvText(classLongCsvRows(cards, statesByUid, opts)));
}
