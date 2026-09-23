/* 교사 현황 보드. M3 이해도·도움 요청을 유지하고, M4 카드·히트맵·문항·CSV를 붙입니다.
   선택한 반의 progress·presence·help·roster를 실시간 구독합니다.
   학생 상세 패널을 열 때만 students/{uid}/state/current를 1회 조회해 답안·저널을 보여 줍니다(#104). */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {inClass} from './class-picker.js';
import {
 titlesFromCatalog, topicTitle, studentLabel, countUnderstanding, groupHardByTopic
} from './understanding-model.js';
import {sortOpenHelp} from './help-model.js';
import {
 topicListFromCatalog, buildStudentCards, sortStudentCards, filterStuck,
 questionStats, classQuestionTotals, classCsv, cardAccuracyLabel, formatRate,
 heatmapTone, historyItems, answerRows, filterAnswerRows, groupAnswerRowsByUnit,
 unitAnswerTotals, journalRows, formatAnswerValue, answerStatusLabel, UNIT_ROMAN
} from './board-model.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let classIdValue = '';
let titles = {};
let topics = [];
let questions = [];
let progressUnsub = null;
let helpUnsub = null;
let presenceUnsub = null;
let rosterUnsub = null;
let progressRows = [];
let helpRows = [];
let presenceRows = [];
let rosterRows = [];
let paintedCards = [];
let filterTopic = '';
let selectedKey = '';
// uid -> {status: 'loading'|'ready'|'empty'|'error', data?}. students/{uid}/state/current를 학생당 1회만 조회.
let detailStateCache = new Map();
let detailFilter = 'all';

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

let feedbackRows = [];
let feedbackUnsub = null;

// 주제별 '다 했어요' 집계(#87): progress.counts.done 기준, 현재 반 학생 카드로 계산
function paintDone() {
 const host = $('heatmap-wrap');
 if (!host) return;
 let box = document.getElementById('board-done');
 if (!box) {
  box = node('div', 'board-done');
  box.id = 'board-done';
  host.before(box);
 }
 const cards = liveCards();
 if (!classIdValue || !cards.length || !topics.length) { box.replaceChildren(); return; }
 const rows = topics.map((topic) => {
  const n = cards.filter((card) => (card.done instanceof Set ? card.done.has(topic.id) : (card.done || []).includes(topic.id))).length;
  return {topic, n};
 });
 const wrap = node('div', 'done-list');
 wrap.append(node('p', 'small visual-label', `주제별 다 했어요 (학생 ${cards.length}명)`));
 for (const {topic, n} of rows) {
  const row = node('div', 'done-row');
  row.title = topic.title;
  const rate = cards.length ? n / cards.length : 0;
  const bar = node('div', 'card-rate');
  bar.dataset.tone = rate >= 0.7 ? 'good' : rate >= 0.4 ? 'mid' : 'low';
  const fill = node('span');
  fill.style.width = `${Math.round(rate * 100)}%`;
  bar.append(fill);
  row.append(node('span', 'done-topic', topic.short), bar, node('b', 'done-count', `${n}/${cards.length}`));
  wrap.append(row);
 }
 box.replaceChildren(wrap);
}

function paintFeedback(list) {
 const rows = feedbackRows.filter((row) => row.text);
 if (!rows.length) return;
 const byTopic = new Map();
 for (const row of rows) {
  if (!byTopic.has(row.topicId)) byTopic.set(row.topicId, []);
  byTopic.get(row.topicId).push(row);
 }
 const wrap = node('div', 'admin-rows');
 wrap.append(node('h3', '', `학생 의견 ${rows.length}건`));
 for (const [topicId, items] of [...byTopic.entries()].sort((a, b) => b[1].length - a[1].length)) {
  const card = node('article', 'admin-row feedback-topic-row');
  const head = node('div');
  head.append(node('strong', '', topicTitle(topicId, titles)), node('span', 'small', `${items.length}건`));
  card.append(head);
  const ul = node('ul', 'feedback-items');
  for (const item of items.sort((a, b) => studentLabel(a).localeCompare(studentLabel(b), 'ko'))) {
   const li = node('li');
   li.append(node('b', '', studentLabel(item) + ' '), node('span', '', item.text));
   ul.append(li);
  }
  card.append(ul);
  wrap.append(card);
 }
 list.append(wrap);
}

function paintUnderstanding() {
 const {counts, hardRows} = countUnderstanding(progressRows);
 const countsEl = $('understanding-counts');
 if (countsEl) {
  countsEl.textContent = `어려워요 ${counts.hard} · 조금 어려워요 ${counts.somewhat} · 이해했어요 ${counts.understood}`;
 }
 const list = $('understanding-list');
 if (!list) return;
 const groups = groupHardByTopic(hardRows);
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!groups.length) {
  list.replaceChildren(node('p', 'small', '이 반에서 어려워요를 누른 학생이 없습니다.'));
  paintFeedback(list);
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const [topicId, rows] of groups) {
  const card = node('article', 'admin-row understanding-topic-row');
  const head = node('div');
  head.append(
   node('strong', '', topicTitle(topicId, titles)),
   node('span', 'small', `어려워요 ${rows.length}명`)
  );
  const people = node('p', 'small', rows.map((row) => studentLabel(row)).join(' · '));
  card.append(head, people);
  wrap.append(card);
 }
 list.replaceChildren(wrap);
 paintFeedback(list);
}

function formatWhen(value) {
 if (!value) return '';
 try {
  if (typeof value.toDate === 'function') return value.toDate().toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
  if (typeof value === 'number') return new Date(value).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
 } catch { /* 시각 없음 */ }
 return '';
}

function paintHelp() {
 const open = sortOpenHelp(helpRows);
 const countsEl = $('help-counts');
 if (countsEl) countsEl.textContent = `대기 ${open.length}`;
 const list = $('help-list');
 if (!list) return;
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!open.length) {
  list.replaceChildren(node('p', 'small', '열린 도움 요청이 없습니다.'));
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const row of open) {
  const card = node('article', 'admin-row help-row');
  const who = node('div');
  who.append(
   node('strong', '', studentLabel(row)),
   node('span', 'small', [formatWhen(row.createdAt), topicTitle(row.topic, titles), row.example || ''].filter(Boolean).join(' · '))
  );
  const detail = node('p', 'small', row.lastError || '오류 메시지 없음');
  const resolve = node('button', '', '해결');
  resolve.type = 'button';
  resolve.dataset.helpId = row.id;
  resolve.addEventListener('click', () => resolveHelp(row.id));
  card.append(who, detail, resolve);
  wrap.append(card);
 }
 list.replaceChildren(wrap);
}

async function resolveHelp(id) {
 if (!id) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'helpRequests', id), {
   status: 'resolved',
   updatedAt: store.serverTimestamp()
  });
 } catch (error) {
  console.error('[teacher-board]', error);
  note('help-note', `해결로 표시하지 못했습니다. (${error.code || error})`);
 }
}

function liveCards() {
 return sortStudentCards(buildStudentCards({
  roster: rosterRows,
  progress: progressRows,
  presence: presenceRows,
  help: helpRows,
  classId: classIdValue,
  topics,
  titles
 }));
}

const UND_KEY = {'어려워요': 'hard', '조금 어려워요': 'somewhat', '이해했어요': 'understood'};
const UND_ORDER = [['hard', '어려워요'], ['somewhat', '조금 어려워요'], ['understood', '이해했어요'], ['none', '미표시']];

// 반 전체를 한눈에: 평균 완료율, 완료율 분포(4구간), 이해도 분포 스택 막대
function paintVisual(all) {
 const list = $('roster-list');
 if (!list) return;
 let vis = document.getElementById('board-visual');
 if (!vis) {
  vis = node('div', 'board-visual');
  vis.id = 'board-visual';
  list.parentNode.insertBefore(vis, list);
 }
 if (!classIdValue || !all.length) { vis.replaceChildren(); return; }
 const rates = all.map((c) => (Number.isFinite(c.completeRate) ? c.completeRate : 0));
 const avg = rates.reduce((a, b) => a + b, 0) / rates.length;

 const tile = node('div', 'visual-tile');
 tile.append(node('b', '', `${Math.round(avg * 100)}%`), node('span', 'small', '평균 완료율'));

 const buckets = [0, 0, 0, 0];
 rates.forEach((r) => { buckets[Math.min(3, Math.floor(r * 4))] += 1; });
 const histo = node('div', 'visual-panel');
 histo.append(node('span', 'small visual-label', '완료율 분포 (학생 수)'));
 const bars = node('div', 'visual-histogram');
 const max = Math.max(...buckets, 1);
 ['0~25%', '25~50%', '50~75%', '75~100%'].forEach((label, i) => {
  const col = node('div', 'histo-col');
  const bar = node('div', 'histo-bar');
  bar.style.height = `${Math.round((buckets[i] / max) * 100)}%`;
  bar.dataset.tone = i >= 3 ? 'good' : i >= 2 ? 'mid' : 'low';
  col.append(node('span', 'histo-count', String(buckets[i])), bar, node('span', 'small', label));
  bars.append(col);
 });
 histo.append(bars);

 const und = {hard: 0, somewhat: 0, understood: 0, none: 0};
 all.forEach((c) => { und[UND_KEY[c.understandingLabel] || 'none'] += 1; });
 const undPanel = node('div', 'visual-panel');
 undPanel.append(node('span', 'small visual-label', '이해도 분포'));
 const stack = node('div', 'visual-stack');
 const legend = node('div', 'visual-legend');
 UND_ORDER.forEach(([key, label]) => {
  if (und[key] > 0) {
   const seg = node('span', 'stack-seg');
   seg.dataset.und = key;
   seg.style.flexGrow = String(und[key]);
   seg.title = `${label} ${und[key]}명`;
   stack.append(seg);
  }
  const item = node('span', 'legend-item');
  item.dataset.und = key;
  item.textContent = `${label} ${und[key]}`;
  legend.append(item);
 });
 undPanel.append(stack, legend);
 vis.replaceChildren(tile, histo, undPanel);
}

function paintRoster() {
 const list = $('roster-list');
 const countsEl = $('roster-counts');
 const exportBtn = $('board-export');
 const clearBtn = $('heatmap-clear');
 if (exportBtn) exportBtn.disabled = !classIdValue;
 if (!classIdValue) {
  paintedCards = [];
  if (countsEl) countsEl.textContent = '학생 0 · 접속 0 · 도움 0';
  paintVisual([]);
  if (list) list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  if (clearBtn) clearBtn.hidden = true;
  paintDetail(null);
  return;
 }
 const all = liveCards();
 paintVisual(all);
 const cards = filterStuck(all, filterTopic);
 paintedCards = cards;
 const online = all.filter((card) => card.online).length;
 const help = all.filter((card) => card.openHelp > 0).length;
 if (countsEl) countsEl.textContent = `학생 ${all.length} · 접속 ${online} · 도움 ${help}`;
 if (clearBtn) {
  clearBtn.hidden = !filterTopic;
  clearBtn.textContent = filterTopic ? `${topicTitle(filterTopic, titles)} 필터 해제` : '주제 필터 해제';
 }
 if (!list) return;
 if (!all.length) {
  list.replaceChildren(node('p', 'small', '이 반 명단·진행 기록이 없습니다.'));
  return;
 }
 if (!cards.length) {
  list.replaceChildren(node('p', 'small', '이 주제에 막힌 학생이 없습니다.'));
  return;
 }
 const wrap = node('div', 'student-card-grid');
 for (const card of cards) {
  const btn = node('button', 'student-card');
  btn.type = 'button';
  btn.dataset.studentKey = card.key;
  if (card.openHelp) btn.dataset.help = '1';
  if (card.key === selectedKey) btn.classList.add('is-selected');
  btn.setAttribute('aria-label', `${card.label} 상세. 접속 ${card.presenceLabel}. 완료 ${formatRate(card.completeRate)}. 도움 ${card.openHelp}`);
  const head = node('div', 'student-card-head');
  const who = node('div', 'student-card-who');
  const dot = node('span', `presence-dot${card.online ? ' is-online' : ''}`);
  dot.setAttribute('aria-hidden', 'true');
  who.append(dot, node('strong', '', card.label));
  head.append(who, node('span', 'small', card.presenceLabel));
  const place = node('p', 'small', card.place || '위치 없음');
  const stats = node('p', 'small', `완료 ${formatRate(card.completeRate)} · 정답 ${cardAccuracyLabel(card)}`);
  const rate = Number.isFinite(card.completeRate) ? card.completeRate : 0;
  const bar = node('div', 'card-rate');
  bar.dataset.tone = rate >= 0.7 ? 'good' : rate >= 0.4 ? 'mid' : 'low';
  const fill = node('span');
  fill.style.width = `${Math.round(rate * 100)}%`;
  bar.append(fill);
  btn.dataset.und = UND_KEY[card.understandingLabel] || 'none';
  // 이해도는 전체 주제 중 '가장 나쁜 값' 하나가 아니라 집계(어려워요 1 · 이해했어요 3)로 보여 준다(#96).
  const flags = node('p', 'small', [card.openHelp ? `도움 ${card.openHelp}` : '', card.understandingSummary || '', card.lastActivityLabel].filter(Boolean).join(' · '));
  if (card.understandingLabel !== '—') btn.title = `테두리 색 = 가장 어려워한 주제 기준(${card.understandingLabel})`;
  btn.append(head, place, stats, bar, flags);
  btn.addEventListener('click', () => openDetail(card.key));
  wrap.append(btn);
 }
 list.replaceChildren(wrap);
}

function paintHeatmap() {
 const host = $('heatmap-wrap');
 if (!host) return;
 paintDone();
 if (!classIdValue) {
  host.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 const cards = liveCards();
 if (!cards.length || !topics.length) {
  host.replaceChildren(node('p', 'small', '주제 목록이나 학생 카드가 아직 없습니다.'));
  return;
 }
 const table = node('table', 'heatmap-table');
 table.setAttribute('aria-label', '주제별 학생 완료·이해도');
 const head = node('thead');
 const headRow = node('tr');
 headRow.append(node('th', '', '학생'));
 for (const topic of topics) {
  const th = node('th');
  const btn = node('button', 'heatmap-topic', topic.short);
  btn.type = 'button';
  btn.title = topic.title;
  btn.setAttribute('aria-label', `${topic.title}에 막힌 학생만 보기`);
  btn.setAttribute('aria-pressed', filterTopic === topic.id ? 'true' : 'false');
  btn.dataset.topic = topic.id;
  btn.addEventListener('click', () => toggleTopicFilter(topic.id));
  th.append(btn);
  if (filterTopic === topic.id) th.classList.add('is-filtered');
  headRow.append(th);
 }
 head.append(headRow);
 const body = node('tbody');
 for (const card of cards) {
  const row = node('tr');
  row.append(node('th', '', card.label));
  const done = new Set(card.done);
  for (const topic of topics) {
   const signal = card.understanding[topic.id] || '';
   const tone = heatmapTone(done.has(topic.id), signal);
   const td = node('td');
   const cell = node('span', 'heatmap-cell');
   cell.dataset.tone = tone;
   const state = done.has(topic.id) ? '완료' : '미완료';
   const extra = signal ? ` · ${card.understanding[topic.id] === signal ? (signal === 'hard' ? '어려워요' : signal === 'somewhat' ? '조금 어려워요' : '이해했어요') : ''}` : '';
   cell.title = `${card.label} · ${topic.title} · ${state}${extra}`;
   cell.setAttribute('aria-label', cell.title);
   td.append(cell);
   row.append(td);
  }
  body.append(row);
 }
 table.append(head, body);
 host.replaceChildren(table);
}

function paintQuestions() {
 const host = $('question-list');
 const totalsEl = $('question-totals');
 if (!classIdValue) {
  if (totalsEl) totalsEl.textContent = '시도 0 · 정답 0';
  if (host) host.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 const inClassProgress = progressRows.filter((row) => inClass(row, classIdValue));
 const totals = classQuestionTotals(inClassProgress);
 if (totalsEl) {
  const avg = totals.avgAttempts == null ? '—' : totals.avgAttempts.toFixed(1);
  totalsEl.textContent = `시도 ${totals.attempts} · 정답 ${totals.correct} · 학생당 평균 시도 ${avg}`;
 }
 if (!host) return;
 const rows = questionStats(inClassProgress, questions);
 if (!rows.length) {
  host.replaceChildren(node('p', 'small', '문항별 요약이 아직 없습니다. 학생이 동기화하면 시도·정답률이 채워집니다.'));
  return;
 }
 const table = node('table');
 const thead = node('thead');
 const head = node('tr');
 for (const label of ['문항', '주제', '시도', '정답률', '평균 시도']) head.append(node('th', '', label));
 thead.append(head);
 const tbody = node('tbody');
 for (const row of rows) {
  const tr = node('tr');
  tr.append(
   node('td', '', row.id),
   node('td', '', row.topic || '—'),
   node('td', '', String(row.attempts)),
   node('td', '', formatRate(row.correctRate)),
   node('td', '', row.avgAttempts == null ? '—' : row.avgAttempts.toFixed(1))
  );
  tbody.append(tr);
 }
 table.append(thead, tbody);
 host.replaceChildren(table);
}

function paintBoard() {
 paintRoster();
 paintHeatmap();
 paintQuestions();
 if (selectedKey) {
  const card = paintedCards.find((item) => item.key === selectedKey) || liveCards().find((item) => item.key === selectedKey);
  if (card) paintDetail(card);
  else paintDetail(null);
 }
}

function toggleTopicFilter(topicId) {
 filterTopic = filterTopic === topicId ? '' : topicId;
 paintRoster();
 paintHeatmap();
}

function openDetail(key) {
 selectedKey = key;
 detailFilter = 'all';
 const card = liveCards().find((item) => item.key === key);
 paintRoster();
 paintDetail(card || null);
 if (card && card.uid) ensureStudentState(card.uid);
}

// students/{uid}/state/current를 학생당 1회만 읽는다(#104). 실패·미존재는 캐시에 남겨 재요청하지 않는다.
async function ensureStudentState(uid) {
 if (!uid || detailStateCache.has(uid)) return;
 detailStateCache.set(uid, {status: 'loading'});
 refreshDetailIfSelected(uid);
 try {
  const {db, store} = await load();
  const snap = await store.getDoc(store.doc(db, 'students', uid, 'state', 'current'));
  detailStateCache.set(uid, snap.exists() ? {status: 'ready', data: snap.data()} : {status: 'empty'});
 } catch (error) {
  console.error('[teacher-board]', error);
  detailStateCache.set(uid, {status: 'error', error});
 }
 refreshDetailIfSelected(uid);
}

function refreshDetailIfSelected(uid) {
 if (!selectedKey) return;
 const card = liveCards().find((item) => item.key === selectedKey);
 if (card && card.uid === uid) paintDetail(card, {keepFocus: true});
}

function statusTone(status) {
 if (status === 'done') return 'good';
 if (status === 'retry') return 'warn';
 return 'muted';
}

function renderAnswerRow(row) {
 const li = node('li', 'answer-row');
 const head = node('div', 'answer-row-head');
 const info = node('span', 'answer-row-info');
 info.append(node('b', '', row.kind || '문항'), node('span', 'small', ` · ${UNIT_ROMAN[row.unit] || ''} ${row.topic || ''}`.trim()));
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

function renderAnswerSection(card) {
 const wrap = node('div', 'student-detail-answers');
 const filterBar = node('div', 'answer-filter-bar');
 for (const [mode, label] of [['all', '전체'], ['retry', '다시 풀기만'], ['subjective', '서술·코드만']]) {
  const btn = node('button', mode === detailFilter ? 'answer-filter-btn is-active' : 'answer-filter-btn', label);
  btn.type = 'button';
  btn.addEventListener('click', () => {
   if (detailFilter === mode) return;
   detailFilter = mode;
   paintDetail(card, {keepFocus: true});
  });
  filterBar.append(btn);
 }
 // 답안은 학생당 1회만 읽으므로, 수업 중 새로 쓴 답안을 보려면 다시 읽을 수 있어야 한다.
 const again = node('button', 'answer-filter-btn answer-reload', '↻ 새로 읽기');
 again.type = 'button';
 again.title = '이 학생의 답안을 다시 읽습니다';
 again.addEventListener('click', () => {
  detailStateCache.delete(card.uid);
  ensureStudentState(card.uid);
  paintDetail(card, {keepFocus: true});
 });
 filterBar.append(again);
 wrap.append(filterBar);
 const entry = detailStateCache.get(card.uid) || {status: 'loading'};
 if (entry.status === 'loading') {
  wrap.append(node('p', 'small', '학습 기록을 불러오는 중입니다…'));
  return wrap;
 }
 if (entry.status === 'error') {
  wrap.append(node('p', 'small', '학습 기록을 불러오지 못했습니다.'));
  return wrap;
 }
 if (entry.status === 'empty') {
  wrap.append(node('p', 'small', '이 학생의 학습 기록 미러가 아직 없습니다(로그인 후 학습하면 생깁니다).'));
  return wrap;
 }
 const state = entry.data || {};
 const rows = answerRows(state, questions);
 const filtered = filterAnswerRows(rows, detailFilter);
 const totalsByUnit = new Map(unitAnswerTotals(state, questions).map((t) => [t.unit, t]));
 if (!filtered.length) {
  wrap.append(node('p', 'small', '표시할 답안이 없습니다.'));
 } else {
  const groups = groupAnswerRowsByUnit(filtered);
  for (const [unit, unitRows] of groups) {
   const totalInfo = totalsByUnit.get(unit);
   const details = node('details', 'answer-unit-group');
   details.open = groups.length <= 1;
   details.append(node('summary', '', `${UNIT_ROMAN[unit] || unit} 단원 · 푼 문항 ${totalInfo ? totalInfo.answered : unitRows.length} / 전체 ${totalInfo ? totalInfo.total : unitRows.length}`));
   const ul = node('ul', 'answer-row-list');
   for (const row of unitRows) ul.append(renderAnswerRow(row));
   details.append(ul);
   wrap.append(details);
  }
 }
 const journals = journalRows(state);
 if (journals.length) {
  wrap.append(node('h3', '', '학습 저널'));
  for (const jr of journals) {
   const details = node('details', 'answer-unit-group');
   details.append(node('summary', '', `${UNIT_ROMAN[jr.unit] || jr.unit} 단원 저널`));
   const dl = node('dl', 'journal-list');
   for (const item of jr.items) {
    dl.append(node('dt', '', item.label));
    dl.append(node('dd', '', item.text));
   }
   details.append(dl);
   wrap.append(details);
  }
 }
 return wrap;
}

function paintDetail(card, opts = {}) {
 const host = $('student-detail');
 const body = $('student-detail-body');
 if (!host || !body) return;
 if (!card) {
  selectedKey = '';
  host.hidden = true;
  host.setAttribute('aria-hidden', 'true');
  body.replaceChildren();
  return;
 }
 host.hidden = false;
 host.setAttribute('aria-hidden', 'false');
 const title = node('h2', '', card.label);
 title.id = 'student-detail-title';
 const meta = node('p', 'small', `${card.presenceLabel} · ${card.place || '위치 없음'} · ${card.lastActivityLabel}`);
 const progress = node('p', '', `완료 ${formatRate(card.completeRate)} (${card.doneCount}/${card.topicTotal || 0}) · 정답 ${cardAccuracyLabel(card)}`);
 const units = node('ul', 'student-detail-units');
 for (const unit of [1, 2, 3, 4]) {
  const total = topics.filter((topic) => topic.unit === unit).length;
  const done = card.done.filter((id) => id.startsWith(`u${unit}-`)).length;
  units.append(node('li', '', `${UNIT_ROMAN[unit]} 주제 ${done}/${total}`));
 }
 const entryForTotals = detailStateCache.get(card.uid);
 if (entryForTotals && entryForTotals.status === 'ready') {
  for (const t of unitAnswerTotals(entryForTotals.data || {}, questions)) {
   units.append(node('li', '', `${UNIT_ROMAN[t.unit] || t.unit} 문항 ${t.answered}/${t.total} · 정답 ${t.correct}`));
  }
 }
 const histTitle = node('h3', '', '이해도');
 const hist = node('ul', 'student-detail-list');
 const items = historyItems(card.understanding);
 if (!items.length) hist.append(node('li', 'small', '어려워요·조금 어려워요 신호가 없습니다.'));
 else {
  for (const item of items) {
   hist.append(node('li', '', `${topicTitle(item.topicId, titles)} · ${item.label}`));
  }
 }
 const helpTitle = node('h3', '', '열린 도움');
 const help = node('ul', 'student-detail-list');
 if (!card.helpRows.length) help.append(node('li', 'small', '열린 도움 요청이 없습니다.'));
 else {
  for (const row of card.helpRows) {
   help.append(node('li', '', [formatWhen(row.createdAt), topicTitle(row.topic, titles), row.lastError || ''].filter(Boolean).join(' · ')));
  }
 }
 const answerTitle = node('h3', '', '답안 보기');
 const answers = renderAnswerSection(card);
 body.replaceChildren(title, meta, progress, units, histTitle, hist, helpTitle, help, answerTitle, answers);
 if (!opts.keepFocus) {
  const close = $('student-detail-close');
  if (close) close.focus();
 }
}

function exportCsv() {
 const cards = liveCards();
 if (!cards.length) return;
 const blob = new Blob(['\uFEFF' + classCsv(cards)], {type: 'text/csv;charset=utf-8'});
 const url = URL.createObjectURL(blob);
 const a = node('a');
 a.href = url;
 a.download = classIdValue ? `board-${classIdValue}.csv` : 'board.csv';
 document.body.append(a);
 a.click();
 a.remove();
 setTimeout(() => URL.revokeObjectURL(url), 5000);
}

function stop() {
 if (progressUnsub) {
  progressUnsub();
  progressUnsub = null;
 }
 if (helpUnsub) {
  helpUnsub();
  helpUnsub = null;
 }
 if (presenceUnsub) {
  presenceUnsub();
  presenceUnsub = null;
 }
 if (rosterUnsub) {
  rosterUnsub();
  rosterUnsub = null;
 }
 if (feedbackUnsub) {
  feedbackUnsub();
  feedbackUnsub = null;
 }
 progressRows = [];
 helpRows = [];
 presenceRows = [];
 rosterRows = [];
 feedbackRows = [];
 filterTopic = '';
 selectedKey = '';
 detailStateCache = new Map();
 detailFilter = 'all';
 paintUnderstanding();
 paintHelp();
 paintBoard();
}

function listen(id) {
 stop();
 classIdValue = id || '';
 if (!id || !ready) {
  paintUnderstanding();
  paintHelp();
  paintBoard();
  return;
 }
 load().then(({db, store}) => {
  rosterUnsub = store.onSnapshot(store.collection(db, 'roster'), (snap) => {
   rosterRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    rosterRows.push({id: doc.id, email: data.email || doc.id, ...data});
   });
   paintBoard();
  }, (error) => {
   console.error('[teacher-board]', error);
   note('roster-note', '명단을 읽지 못했습니다.');
  });
  progressUnsub = store.onSnapshot(store.collection(db, 'progress'), (snap) => {
   progressRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    if (inClass(data, id)) progressRows.push({id: doc.id, uid: data.uid || doc.id, ...data});
   });
   paintUnderstanding();
   paintBoard();
  }, (error) => {
   console.error('[teacher-board]', error);
   note('understanding-note', '이해도 요약을 읽지 못했습니다.');
   note('roster-note', '진행 요약을 읽지 못했습니다.');
  });
  feedbackUnsub = store.onSnapshot(store.collection(db, 'feedback'), (snap) => {
   feedbackRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    if (inClass(data, id)) feedbackRows.push({id: doc.id, ...data});
   });
   paintUnderstanding();
  }, (error) => {
   console.error('[teacher-board]', error);
   note('understanding-note', '학생 의견을 읽지 못했습니다.');
  });
  presenceUnsub = store.onSnapshot(
   store.query(store.collection(db, 'presence'), store.where('classroom', '==', id)),
   (snap) => {
    presenceRows = [];
    snap.forEach((doc) => presenceRows.push({id: doc.id, uid: doc.id, ...doc.data()}));
    paintBoard();
   },
   (error) => {
    console.error('[teacher-board]', error);
    note('roster-note', '접속 상태를 읽지 못했습니다.');
   }
  );
  helpUnsub = store.onSnapshot(
   store.query(store.collection(db, 'helpRequests'), store.where('classId', '==', id)),
   (snap) => {
    helpRows = [];
    snap.forEach((doc) => helpRows.push({id: doc.id, ...doc.data()}));
    paintHelp();
    paintBoard();
   },
   (error) => {
    console.error('[teacher-board]', error);
    note('help-note', '도움 요청을 읽지 못했습니다.');
   }
  );
 }).catch((error) => {
  console.error('[teacher-board]', error);
 });
}

function onClass(detail) {
 listen((detail && detail.classId) || '');
}

export function renderFixture(data = {}) {
 if (progressUnsub || helpUnsub || presenceUnsub || rosterUnsub) stop();
 classIdValue = data.classId || '2-3';
 rosterRows = data.roster || [];
 progressRows = data.progress || [];
 presenceRows = data.presence || [];
 helpRows = data.help || [];
 if (data.titles) titles = data.titles;
 if (data.topics) topics = data.topics;
 if (data.questions) questions = data.questions;
 paintUnderstanding();
 paintHelp();
 paintBoard();
}

if (typeof window !== 'undefined') window.aipyBoardRender = renderFixture;

function bindUi() {
 const exportBtn = $('board-export');
 if (exportBtn) exportBtn.onclick = exportCsv;
 const clearBtn = $('heatmap-clear');
 if (clearBtn) clearBtn.onclick = () => toggleTopicFilter('');
 const close = $('student-detail-close');
 if (close) close.onclick = () => paintDetail(null);
 const detail = $('student-detail');
 if (detail) {
  detail.addEventListener('click', (event) => {
   if (event.target === detail) paintDetail(null);
  });
 }
 document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && $('student-detail') && !$('student-detail').hidden) paintDetail(null);
 });
}

async function startTeacherBoard() {
 if (!$('understanding-board') && !$('roster-board')) return;
 if (!ready) {
  note('understanding-note', '로그인 설정이 없어 현황을 불러올 수 없습니다.');
  note('roster-note', '로그인 설정이 없어 현황을 불러올 수 없습니다.');
  return;
 }
 try {
  const catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  titles = titlesFromCatalog(catalog);
  topics = topicListFromCatalog(catalog);
  questions = Array.isArray(catalog.questions) ? catalog.questions : [];
 } catch (error) {
  console.warn('[teacher-board] catalog', error);
 }
 bindUi();
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
 paintUnderstanding();
 paintHelp();
 paintBoard();
}

startTeacherBoard();
