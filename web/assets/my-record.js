/* 학생용 '내 학습 기록' 화면. 로그인하지 않았으면 이 브라우저의 localStorage 기록, 로그인했으면
   sync.js가 계정 기록과 합쳐 둔 같은 상태를 보여 준다(Firestore를 따로 읽지 않으므로 규칙 변경이
   필요 없고, 다른 학생의 데이터에는 접근할 수 없다). 집계는 my-record-model.js, 답안 줄 렌더링은
   교사 답변 내역과 같은 answer-view.js를 쓴다. */
import {buildMyRecord, filterRecord, statusBadges, percent, FILTERS} from './my-record-model.js?v=q148';
import {renderAnswerRow} from './answer-view.js?v=q145a';
import {titlesFromCatalog} from './understanding-model.js';
import {UNIT_ROMAN} from './board-model.js?v=q135b';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const STORAGE_KEY = 'aipy-lab-v1';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let catalog = null;
let titles = {};
let filter = 'all';
let lastSig = '';
let openKeys = new Set();

function readState() {
 if (window.aipyLearning && typeof window.aipyLearning.getState === 'function') {
  const live = window.aipyLearning.getState();
  if (live && typeof live === 'object') return live;
 }
 try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  if (saved && typeof saved === 'object') return saved;
 } catch { /* 저장소를 못 읽으면 빈 기록으로 본다 */ }
 return {};
}

function signedIn() {
 return Boolean(window.aipyAccount && window.aipyAccount.user);
}

function bar(value, total, label) {
 const wrap = node('div', 'myrec-meter');
 const head = node('div', 'myrec-meter-head');
 head.append(node('span', '', label), node('b', '', `${value}/${total}`));
 const track = node('div', 'myrec-track');
 const fill = node('span', 'myrec-fill');
 fill.style.width = `${percent(value, total)}%`;
 track.append(fill);
 track.setAttribute('role', 'img');
 track.setAttribute('aria-label', `${label} ${value}/${total}`);
 wrap.append(head, track);
 return wrap;
}

function paintNotice() {
 const box = $('myrec-notice');
 if (!box) return;
 if (signedIn()) {
  box.textContent = '로그인한 계정에 동기화된 기록을 기준으로 보여 줍니다. 방금 한 내용이 안 보이면 잠시 뒤 새로 고침하세요.';
 } else {
  box.textContent = '로그인하지 않아 이 브라우저에 저장된 기록만 보입니다. 학교 계정으로 로그인하면 다른 기기에서 한 내용도 함께 봅니다.';
 }
}

function paintSummary(record) {
 const host = $('myrec-summary');
 host.replaceChildren();
 const o = record.overall;
 const top = node('div', 'myrec-overall');
 top.append(node('p', 'myrec-rate', `${o.rate}%`), node('p', 'myrec-rate-label', `전체 진행률 (완료 체크한 소단원 ${o.done}/${o.topics})`));
 host.append(top);
 const grid = node('div', 'myrec-unit-grid');
 for (const u of record.units) {
  const card = node('section', 'myrec-unit-card');
  card.append(node('h3', '', `${UNIT_ROMAN[u.unit] || u.unit} 단원`));
  card.append(bar(u.totals.done, u.totals.topics, '완료 체크'), bar(u.totals.answered, u.totals.questions, '푼 문제'), bar(u.totals.journals, u.totals.topics, '저널 쓴 소단원'));
  grid.append(card);
 }
 host.append(grid);
}

function paintTodo(record) {
 const host = $('myrec-todo');
 host.replaceChildren();
 host.append(node('h2', '', '다음에 할 것'));
 if (!record.todo.length) {
  host.append(node('p', 'myrec-empty', '남은 소단원이 없습니다. 모두 완료했습니다.'));
  return;
 }
 host.append(node('p', 'small', `완료 체크를 안 했거나 안 푼 문제가 있는 소단원 ${record.todo.length}개입니다. 교과서 순서대로 보여 줍니다.`));
 const make = (items) => {
  const ul = node('ul', 'myrec-todo-list');
  for (const t of items) {
   const li = node('li');
   const a = node('a', 'myrec-todo-link', `${UNIT_ROMAN[t.unit] || t.unit} ${t.title}`);
   a.href = prefix + t.href;
   li.append(a, node('span', 'myrec-todo-why', t.reasons.join(' · ')));
   if (t.reasons.some((r) => r.startsWith('안 푼'))) {
    const q = node('a', 'myrec-todo-q', '문제 풀기');
    q.href = prefix + t.practiceHref;
    li.append(q);
   }
   ul.append(li);
  }
  return ul;
 };
 const head = record.todo.slice(0, 6);
 host.append(make(head));
 if (record.todo.length > head.length) {
  const more = node('details', 'myrec-more');
  more.append(node('summary', '', `나머지 ${record.todo.length - head.length}개 더 보기`), make(record.todo.slice(head.length)));
  host.append(more);
 }
}

function paintFilters(record) {
 const host = $('myrec-filters');
 host.replaceChildren();
 for (const f of FILTERS) {
  const count = filterRecord(record, f.id).reduce((n, u) => n + u.subunits.length, 0);
  const btn = node('button', 'myrec-filter', `${f.label} ${count}`);
  btn.type = 'button';
  btn.setAttribute('aria-pressed', String(filter === f.id));
  btn.addEventListener('click', () => {
   filter = f.id;
   render(true);
  });
  host.append(btn);
 }
}

function subunitBlock(sub) {
 const details = node('details', 'myrec-sub');
 details.dataset.key = sub.key;
 details.open = openKeys.has(sub.key);
 const summary = node('summary', 'myrec-sub-sum');
 summary.append(node('span', 'myrec-sub-title', `${sub.short} ${sub.title}`));
 const badges = node('span', 'myrec-badges');
 for (const b of statusBadges(sub)) badges.append(node('span', `answer-status answer-status--${b.tone}`, b.text));
 summary.append(badges);
 details.append(summary);

 const links = node('p', 'myrec-links');
 const a1 = node('a', 'myrec-link', '소단원 페이지');
 a1.href = prefix + sub.href;
 links.append(a1);
 if (sub.qTotal > 0) {
  const a2 = node('a', 'myrec-link', '문제 페이지');
  a2.href = prefix + sub.practiceHref;
  links.append(a2);
 }
 details.append(links);

 const rows = filter === 'wrong' ? sub.wrongRows : sub.rows;
 if (sub.qTotal > 0) {
  details.append(node('h4', 'myrec-h', filter === 'wrong' ? '틀렸거나 다시 풀 문제' : '문제 답안'));
  if (rows.length) {
   const ul = node('ul', 'answer-row-list');
   for (const row of rows) ul.append(renderAnswerRow(row, titles));
   details.append(ul);
  } else {
   details.append(node('p', 'myrec-none', '아직 푼 문제가 없습니다.'));
  }
  if (sub.qUnanswered > 0) details.append(node('p', 'small', `안 푼 문제 ${sub.qUnanswered}개`));
 }

 const items = [...sub.taskItems, ...sub.otherItems];
 if (items.length) {
  details.append(node('h4', 'myrec-h', '직접 해 보세요 · 예제 기록'));
  const dl = node('dl', 'journal-list');
  for (const item of items) {
   let label = item.label;
   if (item.submittedAt) {
    let when = item.submittedAt;
    try { when = new Date(item.submittedAt).toLocaleString('ko-KR'); } catch { /* 원문 유지 */ }
    label += ` · 제출함 ${when}`;
   } else if (item.submitted === false) label += ' · 미제출';
   dl.append(node('dt', '', label), node('dd', '', item.text));
  }
  details.append(dl);
 }

 details.append(node('h4', 'myrec-h', '저널'));
 details.append(sub.hasJournal ? node('p', 'myrec-journal', sub.journal) : node('p', 'myrec-none', '아직 쓰지 않았습니다.'));
 return details;
}

function paintList(record) {
 const host = $('myrec-list');
 host.replaceChildren();
 const units = filterRecord(record, filter);
 if (!units.length) {
  host.append(node('p', 'myrec-empty', '조건에 맞는 소단원이 없습니다.'));
  return;
 }
 for (const u of units) {
  const details = node('details', 'myrec-unit');
  details.dataset.key = `unit-${u.unit}`;
  details.open = !openKeys.has(`closed-unit-${u.unit}`);
  details.append(node('summary', 'myrec-unit-sum', `${UNIT_ROMAN[u.unit] || u.unit} 단원 · 완료 ${u.totals.done}/${u.totals.topics} · 문제 ${u.totals.answered}/${u.totals.questions} · 저널 ${u.totals.journals}/${u.totals.topics}`));
  for (const sub of u.subunits) details.append(subunitBlock(sub));
  details.addEventListener('toggle', () => {
   if (details.open) openKeys.delete(`closed-unit-${u.unit}`); else openKeys.add(`closed-unit-${u.unit}`);
  });
  host.append(details);
 }
}

function collectOpen() {
 for (const d of document.querySelectorAll('#myrec-list details.myrec-sub')) {
  if (d.open) openKeys.add(d.dataset.key); else openKeys.delete(d.dataset.key);
 }
}

function render(force) {
 if (!catalog) return;
 const state = readState();
 const sig = JSON.stringify([state.complete, state.answers, state.journals, signedIn()]);
 if (!force && sig === lastSig) return;
 lastSig = sig;
 collectOpen();
 const record = buildMyRecord(state, catalog);
 paintNotice();
 $('myrec-empty-all').hidden = !record.empty;
 paintSummary(record);
 paintTodo(record);
 paintFilters(record);
 paintList(record);
}

// 인쇄할 때는 접힌 칸을 모두 펼치고, 끝나면 원래대로 되돌린다.
let printed = [];
window.addEventListener('beforeprint', () => {
 printed = [...document.querySelectorAll('#myrec-list details')].filter((d) => !d.open);
 for (const d of printed) d.open = true;
});
window.addEventListener('afterprint', () => {
 for (const d of printed) d.open = false;
 printed = [];
});

async function start() {
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  titles = titlesFromCatalog(catalog);
 } catch (error) {
  console.warn('[my-record] catalog', error);
  $('myrec-list').replaceChildren(node('p', 'myrec-empty', '학습 목록을 불러오지 못했습니다. 새로 고침하세요.'));
  return;
 }
 $('myrec-print').addEventListener('click', () => window.print());
 render(true);
 document.addEventListener('aipy:learning-ready', () => render(true));
 document.addEventListener('aipy:account', () => render(true));
 // 동기화가 늦게 끝나 상태가 바뀌어도 따라가도록 가볍게 확인한다(바뀔 때만 다시 그림).
 setInterval(() => render(false), 1500);
}

start();
