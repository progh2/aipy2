/* 학생 답안·저널 한 줄을 문항 지문·정답과 함께 그리는 공유 렌더링 함수(#128).
   board.html 학생 상세 패널(#104)과 answers.html 답변 내역 페이지가 이 모듈을 함께 쓴다.
   중복 구현을 피하려고 DOM 생성만 여기 모으고, 데이터 가공은 board-model.js의 순수 함수에 맡긴다. */
import {answerStatusLabel, formatAnswerValue, UNIT_ROMAN} from './board-model.js?v=q135b';
import {topicTitle} from './understanding-model.js';
import {classOverviewCellLabel} from './teacher-answers-model.js?v=q145a';

function node(tag, cls, text) {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
}

function statusTone(status) {
 if (status === 'done') return 'good';
 if (status === 'retry') return 'warn';
 return 'muted';
}

// row는 board-model.js의 answerRows()가 만든 모양. titles가 있으면 소단원 anchor 대신
// 실제 소단원 제목을 보여 준다(topicTitle은 'u{unit}-{anchor}' 전체 id를 받는다).
function rowTopicLabel(row, titles) {
 if (!row) return '';
 if (row.unit && row.topic && titles) {
  const full = topicTitle(`u${row.unit}-${row.topic}`, titles);
  if (full) return full;
 }
 return row.topic || '';
}

export function renderAnswerRow(row, titles) {
 const li = node('li', 'answer-row');
 const head = node('div', 'answer-row-head');
 const info = node('span', 'answer-row-info');
 info.append(node('b', '', row.kind || '문항'), node('span', 'small', ` · ${UNIT_ROMAN[row.unit] || ''} ${rowTopicLabel(row, titles)}`.trim()));
 head.append(info, node('span', `answer-status answer-status--${statusTone(row.status)}`, answerStatusLabel(row)));
 const prompt = node('p', 'answer-prompt', row.prompt.length > 60 ? `${row.prompt.slice(0, 60)}…` : row.prompt);
 prompt.title = row.prompt;
 const meta = node('p', 'small', `시도 ${row.attempts}회`);
 const valueBox = node('pre', 'answer-value', formatAnswerValue(row.value) || '(빈 답안)');
 li.append(head, prompt, meta, valueBox);
 if (row.correctAnswer != null && row.correctAnswer !== '') {
  const det = node('details', 'answer-key');
  det.append(node('summary', '', '정답 보기'), node('pre', '', formatAnswerValue(row.correctAnswer)));
  li.append(det);
 }
 return li;
}

// unit 문항 그룹 1개(details.answer-unit-group). totalInfo는 unitAnswerTotals() 항목.
export function renderAnswerUnitGroup(unit, unitRows, totalInfo, {open = false, titles} = {}) {
 const details = node('details', 'answer-unit-group');
 details.open = open;
 details.append(node('summary', '', `${UNIT_ROMAN[unit] || unit} 단원 · 푼 문항 ${totalInfo ? totalInfo.answered : unitRows.length} / 전체 ${totalInfo ? totalInfo.total : unitRows.length}`));
 const ul = node('ul', 'answer-row-list');
 for (const row of unitRows) ul.append(renderAnswerRow(row, titles));
 details.append(ul);
 return details;
}

// 예제 코드 수정 배지 하나. diff는 code-diff-model.js의 projectDiffSummary() 결과.
function projectDiffBadge(diff) {
 if (diff.same) return node('span', 'answer-status answer-status--muted', '원본과 동일');
 return node('span', 'answer-status answer-status--good', `+${diff.added} −${diff.removed}줄 수정`);
}

// 예제 코드 그룹 1개(teacher-answers-model.js groupProjectRowsBySubunit()의 한 항목).
export function renderProjectUnitGroup(group) {
 const details = node('details', 'answer-unit-group');
 details.append(node('summary', '', `${UNIT_ROMAN[group.unit] || group.unit} 단원 · ${group.topicTitle || group.topic || '(주제 없음)'}`));
 const ul = node('ul', 'answer-row-list');
 for (const item of group.items) {
  const li = node('li', 'answer-row');
  const head = node('div', 'answer-row-head');
  head.append(node('span', 'answer-row-info', item.title), projectDiffBadge(item.diff));
  li.append(head);
  ul.append(li);
 }
 details.append(ul);
 return details;
}

// 저널 항목 배열 → <dl>. renderJournalUnitGroup()과 renderSubunitSection() 둘 다 쓴다.
function renderJournalList(items) {
 const dl = node('dl', 'journal-list');
 for (const item of items || []) {
  // #132 '직접 해 보세요' 항목은 제출 여부·시각을 라벨 옆에 붙인다.
  let label = item.label;
  if (item.submittedAt) {
   let when = item.submittedAt;
   try { when = new Date(item.submittedAt).toLocaleString('ko-KR'); } catch { /* 그대로 둠 */ }
   label += ` · 제출함 ${when}`;
  } else if (item.submitted === false) {
   label += ' · 미제출';
  }
  dl.append(node('dt', '', label));
  dl.append(node('dd', '', item.text));
 }
 return dl;
}

// 저널 그룹 1개(journalRows()의 한 항목 → details.answer-unit-group).
export function renderJournalUnitGroup(jr) {
 const details = node('details', 'answer-unit-group');
 details.append(node('summary', '', `${UNIT_ROMAN[jr.unit] || jr.unit} 단원 저널`));
 details.append(renderJournalList(jr.items));
 return details;
}

// #145-A 예제 코드 항목 목록(diff 배지 포함) → <ul>. renderProjectUnitGroup()·renderSubunitSection() 공용.
function renderProjectItemList(items) {
 const ul = node('ul', 'answer-row-list');
 for (const item of items || []) {
  const li = node('li', 'answer-row');
  const head = node('div', 'answer-row-head');
  head.append(node('span', 'answer-row-info', item.title), projectDiffBadge(item.diff));
  li.append(head);
  ul.append(li);
 }
 return ul;
}

// #145-A 학생 상세 요약 줄(완료·정답·저널·과제·미션·마지막 활동). summary는
// teacher-answers-model.js summarizeStudentActivity() 결과.
export function renderStudentSummary(summary) {
 const wrap = node('div', 'student-summary');
 const accuracyText = summary.accuracy != null
  ? `${Math.round(summary.accuracy * 100)}%`
  : (summary.attempted ? `${summary.correct}/${summary.attempted}` : '—');
 const items = [
  ['완료 소단원', `${summary.doneCount}/${summary.topicTotal || 0}`],
  ['문항 정답률', accuracyText],
  ['저널·과제 작성', `${summary.journalCount}건`],
  ['미션 통과', `${summary.missionPassCount}건`],
  ['마지막 활동', summary.lastActivityLabel || '—']
 ];
 for (const [label, value] of items) {
  const cell = node('div', 'student-summary-cell');
  cell.append(node('span', 'small', label), node('strong', '', value));
  wrap.append(cell);
 }
 return wrap;
}

// #145-A 소단원 1개 섹션. sub는 teacher-answers-model.js buildStudentDetailSections()/
// mergeProjectGroupsIntoSections()가 만든 {topic, topicTitle, answers, journalItems, projectItems, hasContent}.
// 입력이 전혀 없으면 접은 채로 "입력 없음"만 보이는 <details>를 돌려준다(요구사항: 빈 섹션은 접기).
export function renderSubunitSection(sub, titles) {
 const details = node('details', 'answer-subunit-block');
 details.open = Boolean(sub.hasContent);
 details.append(node('summary', '', sub.topicTitle || sub.topic || '(소단원)'));
 if (!sub.hasContent && !(sub.projectItems && sub.projectItems.length)) {
  details.append(node('p', 'small', '입력 없음'));
  return details;
 }
 if (sub.answers && sub.answers.length) {
  details.append(node('h5', '', '연습문제'));
  const ul = node('ul', 'answer-row-list');
  for (const row of sub.answers) ul.append(renderAnswerRow(row, titles));
  details.append(ul);
 }
 if (sub.journalItems && sub.journalItems.length) {
  details.append(node('h5', '', '저널·직접 해 보세요·예제 기록'));
  details.append(renderJournalList(sub.journalItems));
 }
 if (sub.projectItems && sub.projectItems.length) {
  details.append(node('h5', '', '예제 코드'));
  details.append(renderProjectItemList(sub.projectItems));
 }
 return details;
}

// #145-A 단원 1개(소단원들 + 단원 저널을 끝에). sections는 buildStudentDetailSections() 결과 1개 항목.
export function renderUnitSection(unitEntry, titles, {openByDefault = false} = {}) {
 const details = node('details', 'answer-unit-group');
 details.open = openByDefault;
 const hasAny = unitEntry.subunits.some((s) => s.hasContent || (s.projectItems && s.projectItems.length)) || unitEntry.unitJournal.length > 0;
 details.open = openByDefault || hasAny;
 details.append(node('summary', '', `${UNIT_ROMAN[unitEntry.unit] || unitEntry.unit} 단원`));
 for (const sub of unitEntry.subunits) details.append(renderSubunitSection(sub, titles));
 if (unitEntry.unitJournal.length) {
  const journalBox = node('div', 'answer-subunit');
  journalBox.append(node('h4', '', '단원 저널'));
  journalBox.append(renderJournalList(unitEntry.unitJournal));
  details.append(journalBox);
 }
 return details;
}

// #145-A 반 전체 한눈 표. columns는 classOverviewColumns(), rows는 buildClassOverviewRow() 배열.
// onCellClick(row)은 학생 셀을 눌렀을 때(학생 상세로 이동).
export function renderClassOverviewTable(columns, rows, {onCellClick} = {}) {
 const table = node('table', 'class-overview-table');
 const thead = node('thead');
 const headRow = node('tr');
 headRow.append(node('th', '', '학생'));
 for (const col of columns) headRow.append(node('th', '', col.short || col.topicTitle || col.topic));
 thead.append(headRow);
 const tbody = node('tbody');
 for (const row of rows || []) {
  const tr = node('tr');
  const nameTh = node('th', 'class-overview-name', row.label);
  if (row.status === 'error') nameTh.append(node('span', 'answer-status answer-status--warn', ' 오류'));
  else if (row.status !== 'ready' && row.status !== 'empty') nameTh.append(node('span', 'small', ' (대기)'));
  tr.append(nameTh);
  for (const col of columns) {
   const td = node('td');
   const cell = row.cells && row.cells[col.key];
   const btn = node('button', 'class-overview-cell', classOverviewCellLabel(cell) || '·');
   btn.type = 'button';
   btn.title = col.topicTitle || col.topic;
   btn.addEventListener('click', () => onCellClick && onCellClick(row));
   td.append(btn);
   tr.append(td);
  }
  tbody.append(tr);
 }
 table.append(thead, tbody);
 return table;
}
