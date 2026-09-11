/* 교사 현황 보드. M3 이해도·도움 요청을 유지하고, M4 카드·히트맵·문항·CSV를 붙입니다.
   선택한 반의 progress·presence·help·roster만 구독합니다. */
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
 heatmapTone, historyItems
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

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
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

function paintRoster() {
 const list = $('roster-list');
 const countsEl = $('roster-counts');
 const exportBtn = $('board-export');
 const clearBtn = $('heatmap-clear');
 if (exportBtn) exportBtn.disabled = !classIdValue;
 if (!classIdValue) {
  paintedCards = [];
  if (countsEl) countsEl.textContent = '학생 0 · 접속 0 · 도움 0';
  if (list) list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  if (clearBtn) clearBtn.hidden = true;
  paintDetail(null);
  return;
 }
 const all = liveCards();
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
  const flags = node('p', 'small', [card.openHelp ? `도움 ${card.openHelp}` : '', card.understandingLabel !== '—' ? card.understandingLabel : '', card.lastActivityLabel].filter(Boolean).join(' · '));
  btn.append(head, place, stats, flags);
  btn.addEventListener('click', () => openDetail(card.key));
  wrap.append(btn);
 }
 list.replaceChildren(wrap);
}

function paintHeatmap() {
 const host = $('heatmap-wrap');
 if (!host) return;
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
 const card = liveCards().find((item) => item.key === key);
 paintRoster();
 paintDetail(card || null);
}

function paintDetail(card) {
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
  units.append(node('li', '', `${['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ'][unit]} ${done}/${total}`));
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
 body.replaceChildren(title, meta, progress, units, histTitle, hist, helpTitle, help);
 const close = $('student-detail-close');
 if (close) close.focus();
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
 progressRows = [];
 helpRows = [];
 presenceRows = [];
 rosterRows = [];
 filterTopic = '';
 selectedKey = '';
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
