/* 답변 내역 페이지(#128) 순수 헬퍼. Firebase 없이 검사할 수 있는 부분만 모은다.
   학생 목록·상세 그룹핑은 board-model.js의 answerRows/journalRows/buildStudentCards를 그대로 쓰고,
   여기서는 그 결과를 반별→학생별 화면에 맞게 다듬는 함수만 추가한다(중복 구현 금지). */
import {topicTitle} from './understanding-model.js';

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

// state(students/{uid}/state/current)에 답안·저널 기록이 하나라도 있는지 — 없으면
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
 return false;
}
