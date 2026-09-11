/* 교사 운영 도구. 입학년도로 조회하고 진급·졸업 정리를 합니다.
   학습 기록은 일괄 삭제하지 않습니다. 쓰기는 교사 권한이 있을 때만 규칙이 허용합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {labelClass} from './class-picker.js';
import {
 filterCohort, sortCohort, cohortYears, promotePreview, rosterWriteFields,
 identityPatch, archivePhrase, removePhrase, phraseMatches, cohortCsv,
 matchByEmail, chunkWrites, isArchived, emailKey, LEARNING_KEEP_NOTE, PROMOTE_NOTE,
 ARCHIVE_NOTE, REMOVE_NOTE, asInt
} from './ops-model.js';

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

let teacherEmail = '';
let dbRef = null;
let storeRef = null;
let allRoster = [];
let studentDocs = [];
let progressDocs = [];
let uiBound = false;
let storeBound = false;
let demoMode = false;

function status(text) {
 const gate = $('ops-gate');
 if (gate) gate.replaceChildren(node('p', '', text));
}

function showBootError(error) {
 console.error('[ops]', error);
 const tools = $('ops-tools');
 if (tools) tools.hidden = true;
 const detail = error && (error.message || error.code) ? String(error.message || error.code) : '';
 const gate = $('ops-gate');
 if (!gate) return;
 const kids = [node('p', '', '운영 화면을 시작하지 못했습니다. 새로고침하세요.')];
 if (detail) kids.push(node('p', 'small', detail));
 gate.replaceChildren(...kids);
}

function denyTeacher(email) {
 const gate = $('ops-gate');
 if (!gate) return;
 gate.replaceChildren(
  node('p', '', '이 계정에는 교사 권한이 없습니다.'),
  node('p', 'small', 'Firebase 콘솔 → Firestore → 컬렉션 admins → 문서 ID를 아래 값으로 만들고 필드 role(문자열) = teacher 를 넣으세요.'),
  node('code', 'admin-code', email)
 );
}

async function startOps() {
 try {
  status('로그인과 권한을 확인합니다…');
  document.addEventListener('aipy:account', (event) => {
   review(event.detail && event.detail.user).catch(showBootError);
  });
  if (window.aipyAccount) await review(window.aipyAccount.user);
 } catch (error) {
  showBootError(error);
 }
}

async function review(user) {
 const tools = $('ops-tools');
 if (!tools) return;
 if (demoMode) return;
 if (!ready) {
  tools.hidden = true;
  status('로그인 설정이 없어 운영 도구를 열 수 없습니다.');
  return;
 }
 if (!user) {
  tools.hidden = true;
  status('헤더의 “학교 계정으로 로그인”으로 먼저 로그인하세요.');
  return;
 }
 const email = (user.email || '').toLowerCase();
 let db, store, teacher = false;
 try {
  ({db, store} = await load());
  teacher = (await store.getDoc(store.doc(db, 'admins', email))).exists();
 } catch (error) {
  console.error('[ops]', error);
  tools.hidden = true;
  status('권한을 확인하지 못했습니다. 네트워크를 확인하고 새로고침하세요.');
  return;
 }
 if (!teacher) {
  tools.hidden = true;
  denyTeacher(email);
  return;
 }
 teacherEmail = email;
 status(`교사 권한 확인됨 · ${email}`);
 tools.hidden = false;
 bindUi();
 bindStore(db, store);
 loadAll(db, store);
}

function selectedYear() {
 return asInt($('ops-year') && $('ops-year').value);
}

function includeArchived() {
 return Boolean($('ops-include-archived') && $('ops-include-archived').checked);
}

function selectedClassOnly() {
 if (!$('ops-class-only') || !$('ops-class-only').checked) return '';
 return (window.aipyClass && window.aipyClass.classId) || '';
}

function currentRows() {
 return filterCohort(allRoster, selectedYear(), {
  includeArchived: includeArchived(),
  classId: selectedClassOnly()
 });
}

function bindUi() {
 if (uiBound) return;
 uiBound = true;
 if ($('ops-year')) $('ops-year').onchange = paint;
 if ($('ops-include-archived')) $('ops-include-archived').onchange = paint;
 if ($('ops-class-only')) $('ops-class-only').onchange = paint;
 if ($('ops-promote-preview')) $('ops-promote-preview').onclick = showPromotePreview;
 if ($('ops-promote')) $('ops-promote').onclick = () => {
  if (!dbRef || !storeRef) { $('ops-promote-note').textContent = '로그인한 교사만 반영할 수 있습니다.'; return; }
  applyPromote(dbRef, storeRef);
 };
 if ($('ops-export')) $('ops-export').onclick = exportSummary;
 if ($('ops-archive')) $('ops-archive').onclick = () => startArchive(dbRef, storeRef);
 if ($('ops-remove')) $('ops-remove').onclick = () => startRemove(dbRef, storeRef);
 document.addEventListener('aipy:class', paint);
}

function bindStore(db, store) {
 if (storeBound) return;
 storeBound = true;
 dbRef = db;
 storeRef = store;
 if ($('ops-load')) $('ops-load').onclick = () => loadAll(db, store);
 document.addEventListener('aipy:roster-changed', () => loadAll(db, store));
}

async function loadAll(db, store) {
 $('ops-list').replaceChildren(node('p', 'small', '불러오는 중…'));
 try {
  const [rosterSnap, studentSnap, progressSnap] = await Promise.all([
   store.getDocs(store.collection(db, 'roster')),
   store.getDocs(store.collection(db, 'students')),
   store.getDocs(store.collection(db, 'progress'))
  ]);
  allRoster = [];
  rosterSnap.forEach((d) => allRoster.push({id: d.id, email: d.id, ...d.data()}));
  studentDocs = [];
  studentSnap.forEach((d) => studentDocs.push({id: d.id, uid: d.id, ...d.data()}));
  progressDocs = [];
  progressSnap.forEach((d) => progressDocs.push({id: d.id, uid: d.data().uid || d.id, ...d.data()}));
 } catch (error) {
  console.error('[ops]', error);
  $('ops-list').replaceChildren(node('p', 'small', '명단을 읽지 못했습니다. 권한과 네트워크를 확인하세요.'));
  return;
 }
 fillYears();
 paint();
}

function fillYears() {
 const select = $('ops-year');
 if (!select) return;
 const prev = select.value;
 const years = cohortYears(allRoster);
 select.replaceChildren();
 const empty = node('option', '', years.length ? '입학년도 선택' : '명단에 입학년도가 없습니다');
 empty.value = '';
 select.append(empty);
 for (const year of years) {
  const opt = node('option', '', `${year}년 입학`);
  opt.value = String(year);
  select.append(opt);
 }
 if (prev && years.includes(Number(prev))) select.value = prev;
 else if (years.length === 1) select.value = String(years[0]);
}

function paint() {
 const year = selectedYear();
 const rows = sortCohort(currentRows());
 const scope = $('ops-scope');
 const classId = selectedClassOnly();
 if (scope) {
  if (!year) scope.textContent = '입학년도를 고르면 그 코호트만 보여 줍니다. 반 선택과 관계없이 모을 수 있습니다.';
  else if (classId) scope.textContent = `${year}년 입학 · ${labelClass(classId)}만 표시합니다.`;
  else scope.textContent = `${year}년 입학 ${rows.length}명입니다. 진급 때 학년·반만 바꾸고 입학년도는 유지합니다.`;
 }
 $('ops-count').textContent = year ? `${rows.length}명` : '';
 $('ops-promote').disabled = true;
 $('ops-promote-preview-table').replaceChildren();
 if (!year) {
  $('ops-list').replaceChildren(node('p', 'small', '입학년도를 선택하세요.'));
  return;
 }
 if (!rows.length) {
  $('ops-list').replaceChildren(node('p', 'small', '이 조건에 맞는 학생이 없습니다.'));
  return;
 }
 const table = node('table');
 table.append(headRow(['학년', '반', '학번', '이름', '입학년도', '번호', '이메일', '상태']));
 const tbody = node('tbody');
 for (const r of rows) {
  const tr = node('tr', isArchived(r) ? 'state-same' : '');
  [r.grade, r.classroom, r.studentId, r.name, r.admissionYear, r.number ?? '', r.email || r.id,
   isArchived(r) ? '보관' : '재학']
   .forEach((v) => tr.append(node('td', '', String(v ?? ''))));
  tbody.append(tr);
 }
 table.append(tbody);
 $('ops-list').replaceChildren(table);
}

function showPromotePreview() {
 const year = selectedYear();
 if (!year) { $('ops-promote-note').textContent = '입학년도를 먼저 고르세요.'; return; }
 const preview = promotePreview(currentRows().filter((row) => !isArchived(row)), {
  grade: $('ops-next-grade').value,
  classroom: $('ops-next-class').value
 });
 if (preview.problems.length) {
  $('ops-promote-note').textContent = preview.problems.join(' · ');
  $('ops-promote').disabled = true;
  $('ops-promote-preview-table').replaceChildren();
  return;
 }
 const changing = preview.rows.filter((r) => !r.same);
 $('ops-promote-note').textContent =
  `${PROMOTE_NOTE} ${preview.rows.length}명 중 ${changing.length}명의 학년·반이 바뀝니다.`;
 $('ops-promote').disabled = changing.length === 0;
 const table = node('table');
 table.append(headRow(['이름', '학번', '입학년도', '현재', '진급 후']));
 const tbody = node('tbody');
 for (const r of preview.rows) {
  const tr = node('tr', r.same ? 'state-same' : 'state-update');
  [r.name, r.studentId, r.admissionYear,
   `${r.fromGrade}학년 ${r.fromClassroom}반`,
   `${r.toGrade}학년 ${r.toClassroom}반`]
   .forEach((v) => tr.append(node('td', '', String(v ?? ''))));
  tbody.append(tr);
 }
 table.append(tbody);
 $('ops-promote-preview-table').replaceChildren(table);
}

async function applyPromote(db, store) {
 const preview = promotePreview(currentRows().filter((row) => !isArchived(row)), {
  grade: $('ops-next-grade').value,
  classroom: $('ops-next-class').value
 });
 if (preview.problems.length || !preview.rows.some((r) => !r.same)) return;
 const changing = preview.rows.filter((r) => !r.same);
 if (!confirm(`${changing.length}명의 학년·반을 ${preview.grade}학년 ${preview.classroom}반으로 바꿀까요? 입학년도는 그대로입니다.`)) return;
 $('ops-promote').disabled = true;
 $('ops-promote-note').textContent = '반영 중…';
 const patch = identityPatch({grade: preview.grade, classroom: preview.classroom});
 const writes = [];
 for (const row of changing) {
  const source = allRoster.find((r) => emailKey(r) === row.email);
  if (!source) continue;
  writes.push({kind: 'roster', email: row.email, payload: rosterWriteFields(source, patch)});
  const student = matchByEmail(studentDocs, row.email);
  if (student) writes.push({kind: 'student', id: student.id, payload: patch});
  const progress = matchByEmail(progressDocs, row.email);
  if (progress) writes.push({kind: 'progress', id: progress.id, payload: patch});
 }
 let done = 0;
 try {
  for (const chunk of chunkWrites(writes)) {
   const batch = store.writeBatch(db);
   for (const item of chunk) {
    if (item.kind === 'roster') {
     batch.set(store.doc(db, 'roster', item.email), {...item.payload, updatedAt: store.serverTimestamp()});
    } else {
     batch.update(store.doc(db, item.kind === 'student' ? 'students' : 'progress', item.id), {
      ...item.payload, updatedAt: store.serverTimestamp()
     });
    }
   }
   await batch.commit();
   done += chunk.length;
   $('ops-promote-note').textContent = `반영 중… ${done}/${writes.length}`;
  }
  $('ops-promote-note').textContent = `${changing.length}명을 진급 반영했습니다. 입학년도는 그대로입니다.`;
  document.dispatchEvent(new CustomEvent('aipy:roster-changed'));
  await loadAll(db, store);
 } catch (error) {
  console.error('[ops]', error);
  $('ops-promote-note').textContent = `반영 중 오류가 발생했습니다: ${error.code || error}. ${done}건까지 반영되었습니다.`;
  $('ops-promote').disabled = false;
 }
}

function exportSummary() {
 const year = selectedYear();
 if (!year) { $('ops-archive-note').textContent = '입학년도를 먼저 고르세요.'; return; }
 const rows = currentRows();
 const blob = new Blob([cohortCsv(rows)], {type: 'text/csv;charset=utf-8'});
 const url = URL.createObjectURL(blob);
 const a = node('a');
 a.href = url;
 a.download = `cohort-${year}.csv`;
 document.body.append(a);
 a.click();
 a.remove();
 setTimeout(() => URL.revokeObjectURL(url), 5000);
 $('ops-archive-note').textContent = `${rows.length}명 요약을 내려받았습니다. ${LEARNING_KEEP_NOTE}`;
}

function startArchive(db, store) {
 const year = selectedYear();
 const rows = currentRows().filter((row) => !isArchived(row));
 if (!year || !rows.length) {
  $('ops-archive-note').textContent = '보관할 재학 학생이 없습니다.';
  return;
 }
 askPhrase({
  title: '코호트 보관',
  body: `${year}년 입학 ${rows.length}명을 보관할까요? ${ARCHIVE_NOTE} ${LEARNING_KEEP_NOTE}`,
  expected: archivePhrase(year),
  action: '보관'
 }).then((ok) => {
  if (!ok) return;
  if (!db || !store) { $('ops-archive-note').textContent = '미리보기에서는 확인 문구만 검사합니다. 실제 보관은 교사 로그인 후 합니다.'; return; }
  applyArchive(db, store, rows);
 });
}

function startRemove(db, store) {
 const year = selectedYear();
 const rows = currentRows();
 if (!year || !rows.length) {
  $('ops-archive-note').textContent = '제거할 명단이 없습니다.';
  return;
 }
 askPhrase({
  title: '명단에서만 제거',
  body: `${year}년 입학 ${rows.length}명을 명단에서 지울까요? ${REMOVE_NOTE} ${LEARNING_KEEP_NOTE}`,
  expected: removePhrase(year),
  action: '명단에서 제거',
  danger: true
 }).then((ok) => {
  if (!ok) return;
  if (!db || !store) { $('ops-archive-note').textContent = '미리보기에서는 확인 문구만 검사합니다. 실제 제거는 교사 로그인 후 합니다.'; return; }
  applyRemove(db, store, rows);
 });
}

function askPhrase({title, body, expected, action, danger}) {
 return new Promise((resolve) => {
  const existing = document.getElementById('ops-confirm-overlay');
  if (existing) existing.remove();
  const overlay = node('div', 'sync-overlay');
  overlay.id = 'ops-confirm-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'ops-confirm-title');
  const box = node('div', 'sync-dialog');
  const heading = node('h2', '', title);
  heading.id = 'ops-confirm-title';
  box.append(heading, node('p', '', body));
  box.append(node('p', 'small', `확인하려면 아래 문구를 그대로 입력하세요: ${expected}`));
  const field = node('input');
  field.type = 'text';
  field.autocomplete = 'off';
  field.spellcheck = false;
  field.setAttribute('aria-label', '확인 문구');
  box.append(field);
  const actions = node('div', 'actions');
  const ok = node('button', danger ? '' : 'primary', action);
  const cancel = node('button', '', '취소');
  ok.type = 'button';
  cancel.type = 'button';
  ok.disabled = true;
  const finish = (value) => { overlay.remove(); resolve(value); };
  field.oninput = () => { ok.disabled = !phraseMatches(field.value, expected); };
  ok.onclick = () => finish(phraseMatches(field.value, expected));
  cancel.onclick = () => finish(false);
  overlay.addEventListener('click', (event) => { if (event.target === overlay) finish(false); });
  actions.append(ok, cancel);
  box.append(actions);
  overlay.append(box);
  document.body.append(overlay);
  field.focus();
 });
}

async function applyArchive(db, store, rows) {
 $('ops-archive-note').textContent = '보관 중…';
 let done = 0;
 try {
  for (const chunk of chunkWrites(rows)) {
   const batch = store.writeBatch(db);
   for (const row of chunk) {
    batch.update(store.doc(db, 'roster', row.email || row.id), {
     archived: true,
     archivedAt: store.serverTimestamp(),
     updatedAt: store.serverTimestamp()
    });
   }
   await batch.commit();
   done += chunk.length;
  }
  $('ops-archive-note').textContent = `${done}명을 보관했습니다. 학습 기록은 그대로입니다.`;
  document.dispatchEvent(new CustomEvent('aipy:roster-changed'));
  await loadAll(db, store);
 } catch (error) {
  console.error('[ops]', error);
  $('ops-archive-note').textContent = `보관 중 오류가 발생했습니다: ${error.code || error}.`;
 }
}

async function applyRemove(db, store, rows) {
 $('ops-archive-note').textContent = '명단 제거 중…';
 let done = 0;
 try {
  for (const chunk of chunkWrites(rows)) {
   const batch = store.writeBatch(db);
   for (const row of chunk) batch.delete(store.doc(db, 'roster', row.email || row.id));
   await batch.commit();
   done += chunk.length;
  }
  $('ops-archive-note').textContent = `${done}명을 명단에서 지웠습니다. 학습 기록은 남았습니다.`;
  document.dispatchEvent(new CustomEvent('aipy:roster-changed'));
  await loadAll(db, store);
 } catch (error) {
  console.error('[ops]', error);
  $('ops-archive-note').textContent = `제거 중 오류가 발생했습니다: ${error.code || error}.`;
 }
}

export function renderFixture(data = {}) {
 demoMode = true;
 bindUi();
 allRoster = data.roster || [];
 studentDocs = data.students || [];
 progressDocs = data.progress || [];
 status('미리보기 · 로그인 없이 표시');
 if ($('ops-tools')) $('ops-tools').hidden = false;
 fillYears();
 if (data.year && $('ops-year')) $('ops-year').value = String(data.year);
 paint();
}

if (typeof window !== 'undefined') window.aipyOpsDemo = renderFixture;

// startOps는 모든 let 초기화 뒤에 둡니다. 모듈 평가 중 bindUi가 uiBound를 읽으면 TDZ로 전체가 실패하고
// HTML 기본 문구(권한을 확인합니다…)만 남습니다.
if ($('ops-gate')) startOps();
