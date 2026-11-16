/* 교사용 반별 입력 현황판. 반을 고르고 [불러오기]를 누르면 그 학년의 roster·progress를 1회 읽고
   (getDocs, 실시간 구독 아님 — answers.html과 같은 조회 범위) 반 학생의 students/{uid}/state/current를
   class-state-loader로 1회씩 읽는다. 집계는 teacher-progress-model.js(= 학생용 내 학습 기록과 같은
   buildMyRecord)이고 답안 줄 렌더링은 answer-view.js를 쓴다. ?demo=1은 가짜 학생 6명으로 미리보기한다. */
import {ready} from './firebase-config.js?v=a144';
import {load} from './auth.js?v=a144';
import {parseClassId} from './class-picker.js';
import {buildStudentCards, sortStudentCards, UNIT_ROMAN} from './board-model.js?v=q135b';
import {renderAnswerRow} from './answer-view.js?v=q145a';
import {loadStatesForUids} from './class-state-loader.js';
import {
 MODES, LEVEL_TEXT, buildClassProgress, cellLevel, cellParts, subunitStats, missingStudents,
 progressCsv, missingCsv, withBom, countable
} from './teacher-progress-model.js?v=q149';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const DEMO = new URLSearchParams(location.search).get('demo') === '1';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let catalog = null;
let titles = {};
let classIdValue = '';
let rosterRows = [];
let progressRows = [];
let entries = new Map();
let model = null;
let loading = false;
let mode = 'all';
let activeUnit = 1;
let selSub = '';
let selStudent = '';

function note(text) { const el = $('tprog-note'); if (el) el.textContent = text || ''; }

function cards() {
 return sortStudentCards(buildStudentCards({roster: rosterRows, progress: progressRows, classId: classIdValue, topics: [], titles}));
}

function recompute() {
 model = catalog ? buildClassProgress(cards(), entries, catalog) : null;
 if (model && !model.units.some((u) => u.unit === activeUnit) && model.units.length) activeUnit = model.units[0].unit;
 paint();
}

function currentUnit() { return model && model.units.find((u) => u.unit === activeUnit); }

function paintTabs() {
 const host = $('tprog-tabs');
 host.replaceChildren();
 if (!model) return;
 for (const u of model.units) {
  const b = node('button', `tprog-tab${u.unit === activeUnit ? ' is-active' : ''}`, `${UNIT_ROMAN[u.unit] || u.unit} 단원`);
  b.type = 'button';
  b.setAttribute('aria-pressed', String(u.unit === activeUnit));
  b.addEventListener('click', () => { activeUnit = u.unit; selSub = ''; selStudent = ''; paint(); });
  host.append(b);
 }
}

function paintModes() {
 const host = $('tprog-modes');
 host.replaceChildren();
 for (const m of MODES) {
  const b = node('button', `tprog-mode${m.id === mode ? ' is-active' : ''}`, m.label);
  b.type = 'button';
  b.setAttribute('aria-pressed', String(m.id === mode));
  b.addEventListener('click', () => { mode = m.id; paint(); });
  host.append(b);
 }
}

function bar(label, pct, text) {
 const wrap = node('div', 'tprog-bar');
 wrap.append(node('span', 'tprog-bar-label', label));
 const track = node('span', 'tprog-bar-track');
 const fill = node('span', 'tprog-bar-fill');
 fill.style.width = `${pct}%`;
 track.append(fill);
 wrap.append(track, node('b', '', text));
 return wrap;
}

function paintSummary() {
 const host = $('tprog-summary');
 host.replaceChildren();
 const u = currentUnit();
 if (!u || !model.students.length) return;
 const list = node('div', 'tprog-sum-list');
 for (const s of u.subunits) {
  const st = subunitStats(model, s.key);
  const b = node('button', `tprog-sum-item${selSub === s.key ? ' is-active' : ''}`);
  b.type = 'button';
  b.append(node('span', 'tprog-sum-title', s.short || s.title),
   bar('저널', st.journalPct, `${st.journal}/${st.n} (${st.journalPct}%)`),
   bar('완료', st.donePct, `${st.done}/${st.n} (${st.donePct}%)`));
  b.addEventListener('click', () => { selSub = selSub === s.key ? '' : s.key; paint(); });
  list.append(b);
 }
 host.append(list);
 if (selSub) {
  const sub = u.subunits.find((s) => s.key === selSub);
  const box = node('div', 'tprog-missing');
  const kind = mode === 'done' ? 'done' : 'journal';
  const names = missingStudents(model, selSub, kind);
  box.append(node('h3', '', `${sub ? sub.title : selSub} — ${kind === 'done' ? '완료 체크 안 한' : '저널 미작성'} ${names.length}명`));
  box.append(node('p', 'tprog-missing-names', names.length ? names.join(', ') : '모두 했습니다.'));
  const row = node('div', 'tprog-actions');
  const copy = node('button', 'tprog-btn', '명단 복사');
  copy.type = 'button';
  copy.addEventListener('click', async () => {
   try { await navigator.clipboard.writeText(names.join('\n')); note('미작성 명단을 복사했습니다.'); } catch { note('복사하지 못했습니다. 명단을 직접 선택해 복사하세요.'); }
  });
  const csv = node('button', 'tprog-btn', '명단 CSV');
  csv.type = 'button';
  csv.addEventListener('click', () => download(`미작성_${selSub}.csv`, withBom(missingCsv(model, selSub, kind))));
  row.append(copy, csv);
  box.append(row);
  host.append(box);
 }
}

function paintGrid() {
 const host = $('tprog-grid');
 host.replaceChildren();
 const u = currentUnit();
 if (!model) { host.append(node('p', 'small', '불러오는 중입니다…')); return; }
 if (!model.students.length) { host.append(node('p', 'small', classIdValue ? '이 반 명단이 없습니다.' : '위에서 반을 먼저 선택하세요.')); return; }
 if (!u) return;
 const table = node('table', 'tprog-table');
 const thead = node('thead');
 const hr = node('tr');
 hr.append(node('th', 'tprog-name', '학생'));
 for (const s of u.subunits) { const th = node('th', '', s.short || s.title); th.title = s.title; hr.append(th); }
 thead.append(hr);
 const tbody = node('tbody');
 for (const st of model.students) {
  const tr = node('tr');
  const th = node('th', 'tprog-name', st.label);
  if (st.status === 'error') th.append(node('span', 'tprog-flag', ' 오류'));
  else if (st.status === 'nouid') th.append(node('span', 'tprog-flag', ' 미접속'));
  else if (st.status === 'empty') th.append(node('span', 'tprog-flag', ' 기록 없음'));
  tr.append(th);
  for (const s of u.subunits) {
   const cell = st.cells[s.key];
   const td = node('td');
   if (!countable(st) || !cell) { td.append(node('span', 'tprog-cell tprog-na', st.status === 'error' ? '오류' : '…')); tr.append(td); continue; }
   const level = cellLevel(cell, mode);
   const p = cellParts(cell);
   const hl = mode === 'missing' ? (cell.hasJournal ? ' tprog-dim' : ' tprog-hl') : '';
   const b = node('button', `tprog-cell tprog-${level}${hl}${selStudent === st.key && selSub === s.key ? ' is-selected' : ''}`);
   b.type = 'button';
   b.dataset.level = level;
   b.title = `${st.label} · ${s.title} — ${LEVEL_TEXT[level]}`;
   b.append(node('span', 'tprog-lv', LEVEL_TEXT[level]));
   if (mode !== 'journal') b.append(node('span', '', p.done));
   if (mode === 'all' || mode === 'missing') b.append(node('span', '', p.q));
   if (mode !== 'done') b.append(node('span', '', p.journal));
   if (mode === 'all' && p.task) b.append(node('span', '', p.task));
   b.addEventListener('click', () => { selStudent = st.key; selSub = s.key; paint(); $('tprog-detail')?.scrollIntoView({block: 'nearest'}); });
   td.append(b);
   tr.append(td);
  }
  tbody.append(tr);
 }
 table.append(thead, tbody);
 host.append(table);
}

function paintDetail() {
 const host = $('tprog-detail-body');
 host.replaceChildren();
 const st = model && model.students.find((s) => s.key === selStudent);
 const u = currentUnit();
 const sub = u && u.subunits.find((s) => s.key === selSub);
 const cell = st && sub && st.cells[sub.key];
 if (!cell) { host.append(node('p', 'small', '표의 칸을 누르면 그 학생의 답안·직접 해 보세요·저널이 여기에 나옵니다.')); return; }
 host.append(node('h3', '', `${st.label} · ${sub.title}`));
 const p = cellParts(cell);
 host.append(node('p', 'tprog-badges', `${p.done} · ${p.q} · ${p.journal}${p.task ? ` · ${p.task}` : ''}`));
 host.append(node('h4', '', '연습문제 답안'));
 if (cell.rows.length) {
  const ul = node('ul', 'answer-row-list');
  for (const row of cell.rows) ul.append(renderAnswerRow(row, titles));
  host.append(ul);
 } else host.append(node('p', 'small', '푼 문제가 없습니다.'));
 host.append(node('h4', '', '직접 해 보세요·예제 기록'));
 const items = [...cell.taskItems, ...cell.otherItems];
 if (items.length) {
  const dl = node('dl', 'journal-list');
  for (const it of items) {
   dl.append(node('dt', '', `${it.label}${it.submittedAt ? ' · 제출함' : ''}`), node('dd', '', it.text));
  }
  host.append(dl);
 } else host.append(node('p', 'small', '입력이 없습니다.'));
 host.append(node('h4', '', '소단원 저널'));
 host.append(cell.hasJournal ? node('pre', 'answer-value', cell.journal) : node('p', 'small', '저널이 없습니다.'));
}

function paint() {
 $('tprog-demo').hidden = !DEMO;
 paintModes();
 paintTabs();
 const u = currentUnit();
 $('tprog-print-title').textContent = `${DEMO ? '[데모] ' : ''}${classIdValue || ''}반 ${u ? `${UNIT_ROMAN[u.unit] || u.unit} 단원 ` : ''}입력 현황 · ${new Date().toLocaleDateString('ko-KR')}`;
 paintSummary();
 paintGrid();
 paintDetail();
 const on = Boolean(model && model.students.length);
 $('tprog-csv').disabled = !on;
 $('tprog-print').disabled = !on;
 $('tprog-reload').disabled = !classIdValue;
}

function download(name, text) {
 const url = URL.createObjectURL(new Blob([text], {type: 'text/csv;charset=utf-8'}));
 const a = node('a');
 a.href = url; a.download = name;
 document.body.append(a); a.click(); a.remove();
 setTimeout(() => URL.revokeObjectURL(url), 5000);
}

async function loadClass() {
 if (loading || DEMO) return;
 if (!classIdValue) { note('위에서 반을 먼저 선택하세요.'); return; }
 const parsed = parseClassId(classIdValue);
 if (!parsed) { note('반 정보를 읽지 못했습니다.'); return; }
 loading = true;
 note('명단을 불러오는 중…');
 try {
  const {db, store} = await load();
  const read = async (name) => {
   const snap = await store.getDocs(store.query(store.collection(db, name), store.where('grade', '==', parsed.grade)));
   const rows = [];
   snap.forEach((d) => rows.push({id: d.id, ...d.data()}));
   return rows;
  };
  [rosterRows, progressRows] = await Promise.all([read('roster'), read('progress')]);
  const uids = cards().map((c) => c.uid).filter(Boolean);
  entries = new Map();
  const result = await loadStatesForUids(uids, (uid) => store.getDoc(store.doc(db, 'students', uid, 'state', 'current')), {
   concurrency: 5, onProgress: ({done, total}) => note(`${done}/${total}명 불러오는 중…`)
  });
  for (const [uid, e] of result.entries()) entries.set(uid, e);
  const failed = [...result.values()].filter((e) => e.status === 'error').length;
  note(`${new Date().toLocaleTimeString('ko-KR')} 기준 ${uids.length}명${failed ? ` (${failed}명 실패)` : ''}.`);
 } catch (error) {
  console.error('[teacher-progress]', error);
  note('불러오지 못했습니다. 잠시 뒤 [새로 읽기]를 눌러 보세요.');
 } finally {
  loading = false;
  recompute();
 }
}

function demoRandom(seed) {
 let x = seed >>> 0 || 1;
 return () => { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return ((x >>> 0) % 10000) / 10000; };
}
function demoState(ability, seed) {
 const rnd = demoRandom(seed);
 const answers = {}, journals = {}, complete = {};
 for (const q of catalog.questions || []) {
  if (!q || !q.id || rnd() > ability) continue;
  answers[q.id] = {status: rnd() < ability ? 'done' : 'retry', attempts: 1, value: '데모 답안'};
 }
 for (const [page, rows] of Object.entries(catalog.topics || {})) {
  const m = /unit0([1-4])/.exec(page);
  if (!m) continue;
  for (const r of rows || []) {
   if (!r || !r.id) continue;
   if (rnd() < ability) complete[`u${m[1]}-${r.id}`] = true;
   if (rnd() < ability - 0.1) journals[`j-u${m[1]}-${r.id}`] = '오늘 배운 내용을 내 말로 정리했다(데모).';
  }
 }
 return {answers, journals, complete};
}
function renderDemo() {
 classIdValue = '2-3';
 const names = ['김가온', '이나래', '박다솜', '최라온', '정마루', '한서율'];
 rosterRows = names.map((name, i) => ({email: `d${i + 1}@demo`, name, studentId: `2030${i + 1}`, grade: 2, classroom: 3}));
 progressRows = rosterRows.map((r, i) => ({email: r.email, uid: i === 5 ? '' : `demo-${i + 1}`, grade: 2, classroom: 3, counts: {}}));
 const abilities = [0.97, 0.85, 0.7, 0.5, 0.3];
 entries = new Map(abilities.map((a, i) => [`demo-${i + 1}`, {status: 'ready', data: demoState(a, 1000 + i * 7919)}]));
 document.querySelector('[data-class-label]')?.replaceChildren('2학년 3반 (데모 데이터)');
 note('데모 데이터입니다. 실제 학생 기록이 아닙니다.');
 recompute();
}

async function start() {
 if (!$('tprog-grid')) return;
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  const {titlesFromCatalog} = await import('./understanding-model.js');
  titles = titlesFromCatalog(catalog);
 } catch (error) { console.warn('[teacher-progress] catalog', error); }
 $('tprog-reload').addEventListener('click', loadClass);
 $('tprog-csv').addEventListener('click', () => {
  if (!model || !window.confirm('학생 개인정보가 포함됩니다. 내려받으시겠습니까?')) return;
  download(`입력현황_${classIdValue}_${activeUnit}단원.csv`, withBom(progressCsv(model, activeUnit)));
 });
 $('tprog-print').addEventListener('click', () => window.print());
 if (DEMO) { renderDemo(); return; }
 if (!ready) note('로그인 설정이 없어 불러올 수 없습니다.');
 const onClass = (detail) => {
  const id = (detail && detail.classId) || '';
  if (id === classIdValue) return;
  classIdValue = id; entries = new Map(); rosterRows = []; progressRows = []; selSub = ''; selStudent = '';
  recompute();
  if (id) note('[불러오기]를 누르면 이 반의 입력 현황을 읽어 옵니다.');
 };
 document.addEventListener('aipy:class', (e) => onClass(e.detail));
 if (window.aipyClass) onClass(window.aipyClass);
 recompute();
}

start();
