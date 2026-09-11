/* 교사용 명단 관리. 콘솔에서 문서를 손으로 만들지 않도록 CSV로 일괄 등록합니다.
   쓰기 권한은 admins/{교사이메일} 문서가 있을 때만 규칙이 허용합니다.
   목록·내보내기는 헤더에서 고른 반(grade-classroom)만 보여 줍니다. */
import {load, SCHOOL} from './auth.js';
import {inClass, labelClass, isArchived} from './class-picker.js';

const $ = (id) => document.getElementById(id);
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};
function headRow(titles) {
 const thead = node('thead'), tr = node('tr');
 titles.forEach((t) => tr.append(node('th', '', t)));
 thead.append(tr);
 return thead;
}
const gate = $('admin-gate');
if (gate) startAdmin();

const FIELDS = [
 {key: 'email', labels: ['email', '이메일', '메일'], type: 'text'},
 {key: 'studentId', labels: ['studentid', 'student_id', '학번'], type: 'text'},
 {key: 'admissionYear', labels: ['admissionyear', 'admission_year', '입학년도', '입학연도'], type: 'int'},
 {key: 'name', labels: ['name', '이름', '성명'], type: 'text'},
 {key: 'grade', labels: ['grade', '학년'], type: 'int'},
 {key: 'classroom', labels: ['classroom', 'class', '반'], type: 'int'},
 {key: 'number', labels: ['number', '번호', '출석번호'], type: 'int', optional: true}
];
const NEWLINE = String.fromCharCode(10);
const HEADER = 'email,studentId,admissionYear,name,grade,classroom,number';
const SAMPLE = [HEADER,
 `20314@${SCHOOL},20314,2025,홍길동,2,3,14`,
 `20315@${SCHOOL},20315,2025,김서연,2,3,15`].join(NEWLINE);

let planned = [];
let teacherEmail = '';
let cachedRoster = null;
let dbRef = null;
let storeRef = null;

function status(text) {
 gate.replaceChildren(node('p', '', text));
}

async function startAdmin() {
 status('로그인과 권한을 확인합니다…');
 document.addEventListener('aipy:account', (event) => review(event.detail.user));
 if (window.aipyAccount) review(window.aipyAccount.user);
}

async function review(user) {
 const tools = $('admin-tools');
 if (!tools) return;
 if (!user) {
  tools.hidden = true;
  status('헤더의 “학교 계정으로 로그인”으로 먼저 로그인하세요.');
  return;
 }
 const email = (user.email || '').toLowerCase();
 const {db, store} = await load();
 let teacher = false;
 try {
  teacher = (await store.getDoc(store.doc(db, 'admins', email))).exists();
 } catch (error) {
  console.error('[admin]', error);
 }
 if (!teacher) {
  tools.hidden = true;
  gate.replaceChildren(
   node('p', '', '이 계정에는 교사 권한이 없습니다.'),
   node('p', 'small', 'Firebase 콘솔 → Firestore → 컬렉션 admins → 문서 ID를 아래 값으로 만들고 필드 role(문자열) = teacher 를 넣으세요.'),
   node('code', 'admin-code', email),
   node('p', 'small', '보안을 위해 이 문서는 웹에서 만들 수 없습니다. 웹에서 가능하다면 학생도 스스로 교사가 될 수 있기 때문입니다.')
  );
  return;
 }
 teacherEmail = email;
 gate.replaceChildren(node('p', '', `교사 권한 확인됨 · ${email}`));
 tools.hidden = false;
 bind(db, store);
 listRoster(db, store);
}

function selectedClassId() {
 return (window.aipyClass && window.aipyClass.classId) || '';
}

function existingFromCache(email) {
 if (!cachedRoster) return null;
 return cachedRoster.find((row) => (row.id || row.email) === email) || null;
}

function scopedRoster(rows) {
 const id = selectedClassId();
 const active = (rows || []).filter((row) => !isArchived(row));
 if (!id) return active;
 return active.filter((row) => inClass(row, id));
}

let bound = false;
function bind(db, store) {
 if (bound) return;
 bound = true;
 dbRef = db;
 storeRef = store;
 $('roster-sample').onclick = () => { $('roster-text').value = SAMPLE; };
 $('roster-file').onchange = async (event) => {
  const file = event.target.files[0];
  if (file) $('roster-text').value = await file.text();
  event.target.value = '';
 };
 $('roster-check').onclick = () => check(db, store);
 $('roster-apply').onclick = () => apply(db, store);
 $('roster-load').onclick = () => listRoster(db, store);
 $('roster-export').onclick = () => exportRoster(db, store);
 $('unassigned-load').onclick = () => listUnassigned(db, store);
}

// --- CSV ---

export function parseCsv(text) {
 const rows = [];
 let row = [], field = '', quoted = false;
 text = text.replace(/^﻿/, '');
 for (let i = 0; i < text.length; i++) {
  const c = text[i];
  if (quoted) {
   if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
   else if (c === '"') quoted = false;
   else field += c;
  } else if (c === '"') quoted = true;
  else if (c === ',' || c === '\t') { row.push(field); field = ''; }
  else if (c === '\n') { row.push(field); field = ''; rows.push(row); row = []; }
  else if (c !== '\r') field += c;
 }
 if (field !== '' || row.length) { row.push(field); rows.push(row); }
 return rows.filter((r) => r.some((v) => v.trim() !== ''));
}

// 머리글이 있으면 이름으로, 없으면 정해진 순서로 열을 맞춥니다. 한글 머리글도 받습니다.
export function columnOrder(head) {
 const cells = head.map((c) => c.trim().toLowerCase());
 const isHeader = cells.some((c) => FIELDS.some((f) => f.labels.includes(c)));
 if (!isHeader) return {order: FIELDS.map((f) => f.key), skipHead: false};
 const order = cells.map((c) => {
  const field = FIELDS.find((f) => f.labels.includes(c));
  return field ? field.key : null;
 });
 return {order, skipHead: true};
}

export function readRow(cells, order) {
 const raw = {};
 order.forEach((key, i) => { if (key) raw[key] = (cells[i] || '').trim(); });
 const problems = [];
 const entry = {};
 for (const field of FIELDS) {
  const value = raw[field.key] || '';
  if (!value) {
   if (field.optional) { entry[field.key] = null; continue; }
   problems.push(`${field.key} 없음`);
   continue;
  }
  if (field.type === 'int') {
   const parsed = Number(value);
   if (!Number.isInteger(parsed)) { problems.push(`${field.key}는 정수여야 함`); continue; }
   entry[field.key] = parsed;
  } else {
   entry[field.key] = value;
  }
 }
 if (entry.email) {
  entry.email = entry.email.toLowerCase();
  if (!entry.email.endsWith(`@${SCHOOL}`)) problems.push(`학교 이메일(@${SCHOOL})이 아님`);
 }
 return {entry, problems};
}

async function check(db, store) {
 const text = $('roster-text').value;
 if (!text.trim()) { $('roster-summary').textContent = 'CSV 내용을 붙여넣거나 파일을 선택하세요.'; return; }
 $('roster-summary').textContent = '현재 명단과 비교합니다…';
 const rows = parseCsv(text);
 const {order, skipHead} = columnOrder(rows[0] || []);
 const body = skipHead ? rows.slice(1) : rows;

 let existing = new Map();
 try {
  const snapshot = await store.getDocs(store.collection(db, 'roster'));
  snapshot.forEach((d) => existing.set(d.id, d.data()));
 } catch (error) {
  console.error('[admin]', error);
  $('roster-summary').textContent = '현재 명단을 읽지 못했습니다. 권한과 네트워크를 확인하세요.';
  return;
 }

 const seenEmail = new Map(), seenId = new Map();
 const results = body.map((cells, i) => {
  const {entry, problems} = readRow(cells, order);
  const line = i + 1 + (skipHead ? 1 : 0);
  if (entry.email) {
   if (seenEmail.has(entry.email)) problems.push(`파일 안에서 이메일 중복 (${seenEmail.get(entry.email)}번째 줄)`);
   else seenEmail.set(entry.email, line);
  }
  // 학번은 입학년도가 다르면 겹칠 수 있습니다. 같은 입학년도 안에서만 중복으로 봅니다.
  if (entry.studentId && entry.admissionYear != null) {
   const key = `${entry.admissionYear}/${entry.studentId}`;
   if (seenId.has(key)) problems.push(`같은 입학년도에 학번 중복 (${seenId.get(key)}번째 줄)`);
   else seenId.set(key, line);
  }
  let state = 'new';
  if (problems.length) state = 'error';
  else {
   const before = existing.get(entry.email);
   if (before) {
    const same = FIELDS.every((f) => (before[f.key] ?? null) === (entry[f.key] ?? null));
    state = same ? 'same' : 'update';
   }
  }
  return {line, entry, problems, state};
 });

 planned = results.filter((r) => r.state === 'new' || r.state === 'update');
 const count = (state) => results.filter((r) => r.state === state).length;
 $('roster-summary').textContent =
  `총 ${results.length}줄 · 신규 ${count('new')} · 변경 ${count('update')} · 동일 ${count('same')} · 오류 ${count('error')}`;
 $('roster-apply').disabled = planned.length === 0;
 renderPreview(results);
}

function renderPreview(results) {
 const labels = {new: '신규', update: '변경', same: '동일', error: '오류'};
 const table = node('table');
 table.append(headRow(['줄', '상태', '이메일', '학번', '입학년도', '이름', '학년', '반', '번호', '메모']));
 const tbody = node('tbody');
 for (const r of results) {
  const tr = node('tr', `state-${r.state}`);
  const e = r.entry;
  [r.line, labels[r.state], e.email || '', e.studentId || '', e.admissionYear ?? '', e.name || '',
   e.grade ?? '', e.classroom ?? '', e.number ?? '', r.problems.join(' / ')]
   .forEach((v) => tr.append(node('td', '', String(v))));
  tbody.append(tr);
 }
 table.append(tbody);
 $('roster-preview').replaceChildren(table);
}

async function apply(db, store) {
 if (!planned.length) return;
 if (!confirm(`${planned.length}명을 명단에 반영할까요? 기존 값은 덮어씁니다.`)) return;
 $('roster-apply').disabled = true;
 $('roster-summary').textContent = '반영 중…';
 // 배치당 500개 제한이 있으므로 여유를 두고 나눕니다.
 const chunks = [];
 for (let i = 0; i < planned.length; i += 400) chunks.push(planned.slice(i, i + 400));
 let done = 0;
 try {
  for (const chunk of chunks) {
   const batch = store.writeBatch(db);
   for (const {entry} of chunk) {
    const payload = {
     email: entry.email,
     studentId: entry.studentId,
     admissionYear: entry.admissionYear,
     name: entry.name,
     grade: entry.grade,
     classroom: entry.classroom,
     updatedAt: store.serverTimestamp()
    };
    if (entry.number != null) payload.number = entry.number;
    const before = existingFromCache(entry.email);
    if (before && before.archived === true) {
     payload.archived = true;
     if (before.archivedAt) payload.archivedAt = before.archivedAt;
    }
    batch.set(store.doc(db, 'roster', entry.email), payload);
   }
   await batch.commit();
   done += chunk.length;
   $('roster-summary').textContent = `반영 중… ${done}/${planned.length}`;
  }
  $('roster-summary').textContent = `${done}명을 반영했습니다. 학생이 다시 로그인하거나 새로고침하면 적용됩니다.`;
  planned = [];
  document.dispatchEvent(new CustomEvent('aipy:roster-changed'));
  listRoster(db, store);
 } catch (error) {
  console.error('[admin]', error);
  $('roster-summary').textContent = `반영 중 오류가 발생했습니다: ${error.code || error}. ${done}명까지 반영되었습니다.`;
  $('roster-apply').disabled = false;
 }
}

// --- 현재 명단 ---

async function fetchRoster(db, store) {
 const snapshot = await store.getDocs(store.collection(db, 'roster'));
 const rows = [];
 snapshot.forEach((d) => rows.push({id: d.id, ...d.data()}));
 rows.sort((a, b) =>
  (a.grade - b.grade) || (a.classroom - b.classroom) ||
  String(a.studentId).localeCompare(String(b.studentId)));
 return rows;
}

function renderRoster(rows) {
 cachedRoster = rows;
 const id = selectedClassId();
 const shown = scopedRoster(rows);
 const scope = $('roster-scope');
 if (scope) {
  scope.textContent = id
   ? `${labelClass(id)} 명단만 표시합니다. 반을 바꾸면 이 목록도 바뀝니다.`
   : '수업할 반을 위에서 선택하면 그 반 명단만 보입니다.';
 }
 $('roster-count').textContent = id ? `${shown.length}명 · ${labelClass(id)}` : `${shown.length}명`;
 if (!rows.length) {
  $('roster-list').replaceChildren(node('p', 'small', '등록된 명단이 없습니다.'));
  return;
 }
 const archivedCount = rows.filter((row) => isArchived(row)).length;
 if (archivedCount && scope) {
  scope.textContent += ` 보관한 ${archivedCount}명은 운영 화면에서 봅니다.`;
 }
 if (id && !shown.length) {
  $('roster-list').replaceChildren(node('p', 'small', `${labelClass(id)}에 등록된 학생이 없습니다.`));
  return;
 }
 const table = node('table');
 table.append(headRow(['학년', '반', '학번', '이름', '입학년도', '번호', '이메일', '']));
 const tbody = node('tbody');
 for (const r of shown) {
  const tr = node('tr');
  [r.grade, r.classroom, r.studentId, r.name, r.admissionYear, r.number ?? '', r.id]
   .forEach((v) => tr.append(node('td', '', String(v ?? ''))));
  const cell = node('td');
  const remove = node('button', '', '삭제');
  remove.type = 'button';
  remove.onclick = async () => {
   if (!confirm(`${r.name}(${r.id})을 명단에서 지울까요? 학습 기록은 남습니다.`)) return;
   try {
    await storeRef.deleteDoc(storeRef.doc(dbRef, 'roster', r.id));
    document.dispatchEvent(new CustomEvent('aipy:roster-changed'));
    listRoster(dbRef, storeRef);
   } catch (error) {
    console.error('[admin]', error);
    alert('삭제하지 못했습니다.');
   }
  };
  cell.append(remove);
  tr.append(cell);
  tbody.append(tr);
 }
 table.append(tbody);
 $('roster-list').replaceChildren(table);
}

async function listRoster(db, store) {
 $('roster-list').replaceChildren(node('p', 'small', '불러오는 중…'));
 let rows;
 try {
  rows = await fetchRoster(db, store);
 } catch (error) {
  console.error('[admin]', error);
  $('roster-list').replaceChildren(node('p', 'small', '명단을 읽지 못했습니다.'));
  return;
 }
 renderRoster(rows);
}

document.addEventListener('aipy:class', () => {
 if (cachedRoster) renderRoster(cachedRoster);
 else if (bound && dbRef) listRoster(dbRef, storeRef);
});

async function exportRoster(db, store) {
 const rows = scopedRoster(await fetchRoster(db, store));
 const id = selectedClassId();
 const body = rows.map((r) =>
  [r.id, r.studentId, r.admissionYear, r.name, r.grade, r.classroom, r.number ?? ''].join(','));
 const blob = new Blob(['﻿' + [HEADER, ...body].join('\n') + '\n'], {type: 'text/csv;charset=utf-8'});
 const url = URL.createObjectURL(blob);
 const a = node('a');
 a.href = url;
 a.download = id ? `roster-${id}.csv` : 'roster.csv';
 document.body.append(a);
 a.click();
 a.remove();
 setTimeout(() => URL.revokeObjectURL(url), 5000);
}

// --- 미배정 학생 ---

async function listUnassigned(db, store) {
 $('unassigned-list').replaceChildren(node('p', 'small', '확인 중…'));
 let rows = [];
 try {
  const snapshot = await store.getDocs(
   store.query(store.collection(db, 'students'), store.where('classroom', '==', null)));
  // 교사 계정은 명단에 없는 것이 정상이므로 목록에서 제외합니다.
  snapshot.forEach((d) => {
   const data = d.data();
   if ((data.email || '') !== teacherEmail) rows.push(data);
  });
 } catch (error) {
  console.error('[admin]', error);
  $('unassigned-list').replaceChildren(node('p', 'small', '조회하지 못했습니다.'));
  return;
 }
 if (!rows.length) {
  $('unassigned-list').replaceChildren(node('p', 'small', '미배정 학생이 없습니다.'));
  return;
 }
 const list = node('div', 'admin-rows');
 for (const r of rows) {
  const line = node('div', 'admin-row');
  line.append(node('span', '', `${r.email} · ${r.name || '이름 없음'}`));
  const add = node('button', '', 'CSV 입력란에 추가');
  add.type = 'button';
  add.onclick = () => {
   const box = $('roster-text');
   const head = box.value.trim() ? '' : 'email,studentId,admissionYear,name,grade,classroom,number\n';
   box.value = `${box.value.replace(/\n*$/, '\n')}${head}${r.email},,,${r.name || ''},,,`.replace(/^\n/, '');
   box.focus();
  };
  line.append(add);
  list.append(line);
 }
 $('unassigned-list').replaceChildren(
  node('p', 'small', '추가한 뒤 학번·입학년도·학년·반을 채우고 검사하세요.'), list);
}
