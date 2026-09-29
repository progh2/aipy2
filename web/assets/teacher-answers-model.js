/* 답변 내역 페이지(#128) 순수 헬퍼. Firebase 없이 검사할 수 있는 부분만 모은다.
   학생 목록·상세 그룹핑은 board-model.js의 answerRows/journalRows/buildStudentCards를 그대로 쓰고,
   여기서는 그 결과를 반별→학생별 화면에 맞게 다듬는 함수만 추가한다(중복 구현 금지). */
import {topicTitle} from './understanding-model.js';
import {projectDiffSummary} from './code-diff-model.js?v=q135d';

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
