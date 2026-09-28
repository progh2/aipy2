/* 학생 답안·저널 한 줄을 문항 지문·정답과 함께 그리는 공유 렌더링 함수(#128).
   board.html 학생 상세 패널(#104)과 answers.html 답변 내역 페이지가 이 모듈을 함께 쓴다.
   중복 구현을 피하려고 DOM 생성만 여기 모으고, 데이터 가공은 board-model.js의 순수 함수에 맡긴다. */
import {answerStatusLabel, formatAnswerValue, UNIT_ROMAN} from './board-model.js';
import {topicTitle} from './understanding-model.js';

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

// 저널 그룹 1개(journalRows()의 한 항목 → details.answer-unit-group).
export function renderJournalUnitGroup(jr) {
 const details = node('details', 'answer-unit-group');
 details.append(node('summary', '', `${UNIT_ROMAN[jr.unit] || jr.unit} 단원 저널`));
 const dl = node('dl', 'journal-list');
 for (const item of jr.items) {
  dl.append(node('dt', '', item.label));
  dl.append(node('dd', '', item.text));
 }
 details.append(dl);
 return details;
}
