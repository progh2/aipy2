/* 교사용 과제 정의·제출 확인. 헤더에서 고른 반(window.aipyClass)을 기본으로 씁니다.
   문항·예제 목록은 data/catalog.json이며 항목을 코드에 적지 않습니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classesFromRoster, inClass, labelClass} from './class-picker.js';
import {
 assignmentFields, assignmentReady, catalogTargets, filterCatalogTargets, targetTitle,
 targetHref, statusLabel, reviewLabel, teacherReviewFields, formatWhen, toDatetimeLocal,
 fromDatetimeLocal, studentLabel, REGRADE_NOTE, BROWSER_GRADE_NOTE, COMMENT_MAX,
 COMMENT_PLACEHOLDER
} from './assignment-model.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let teacherEmail = '';
let catalog = {questions: [], examples: {}, topics: {}};
let catalogItems = [];
let classRows = [];
let rosterRows = [];
let assignments = [];
let submissions = [];
let editingId = '';
let selectedAssignmentId = '';
let detailUid = '';
let writing = false;

function toast(text) {
 const box = document.getElementById('toast');
 if (box) box.textContent = text || '';
}

function selectedClassId() {
 return (window.aipyClass && window.aipyClass.classId) || '';
}

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

function status(text) {
 const gate = $('assign-gate');
 if (gate) gate.replaceChildren(node('p', '', text));
}

async function isTeacher(email) {
 const {db, store} = await load();
 try {
  return (await store.getDoc(store.doc(db, 'admins', email))).exists();
 } catch (error) {
  console.error('[teacher-assignments]', error);
  return false;
 }
}

function formTargets() {
 const box = $('target-picker');
 if (!box) return [];
 return [...box.querySelectorAll('input[type="checkbox"]:checked')].map((input) => ({
  type: input.dataset.targetType,
  id: input.value
 }));
}

function formClassrooms() {
 const box = $('assign-classes');
 if (!box) return [];
 const checked = [...box.querySelectorAll('input[type="checkbox"]:checked')].map((input) => input.value);
 if (checked.length) return checked;
 const current = selectedClassId();
 return current ? [current] : [];
}

function readForm() {
 return assignmentFields({
  title: $('assign-title') ? $('assign-title').value : '',
  description: $('assign-desc') ? $('assign-desc').value : '',
  targets: formTargets(),
  classrooms: formClassrooms(),
  openAt: fromDatetimeLocal($('assign-open-at') && $('assign-open-at').value),
  dueAt: fromDatetimeLocal($('assign-due-at') && $('assign-due-at').value),
  open: $('assign-open') ? $('assign-open').checked : true,
  createdBy: teacherEmail
 });
}

function paintClasses() {
 const host = $('assign-classes');
 if (!host) return;
 const selected = new Set(formClassrooms());
 if (!selected.size && selectedClassId()) selected.add(selectedClassId());
 host.replaceChildren();
 if (!classRows.length) {
  host.append(node('p', 'small', '명단에 등록된 반이 없습니다.'));
  return;
 }
 for (const row of classRows) {
  const label = node('label', 'assign-check');
  const box = node('input');
  box.type = 'checkbox';
  box.value = row.id;
  box.checked = selected.has(row.id);
  label.append(box, node('span', '', `${labelClass(row.id)}${row.count != null ? ` · ${row.count}명` : ''}`));
  host.append(label);
 }
}

function paintPicker() {
 const host = $('target-picker');
 if (!host) return;
 const unit = $('target-unit') ? $('target-unit').value : '';
 const type = $('target-type') ? $('target-type').value : '';
 const search = $('target-search') ? $('target-search').value : '';
 const selected = new Set(formTargets().map((t) => `${t.type}:${t.id}`));
 const rows = filterCatalogTargets(catalogItems, {unit, type, search});
 host.replaceChildren();
 if (!rows.length) {
  host.append(node('p', 'small', '조건에 맞는 문제·예제가 없습니다.'));
  return;
 }
 for (const item of rows) {
  const key = `${item.type}:${item.id}`;
  const label = node('label', 'assign-check');
  const box = node('input');
  box.type = 'checkbox';
  box.value = item.id;
  box.dataset.targetType = item.type;
  box.checked = selected.has(key);
  const kind = item.type === 'question' ? (item.kind || '문제') : '예제';
  const unitText = item.unit ? `${item.unit}단원` : '';
  label.append(box, node('span', '', `${item.id} · ${kind}${unitText ? ` · ${unitText}` : ''} · ${item.title}`));
  host.append(label);
 }
 const count = $('target-count');
 if (count) count.textContent = `고른 항목 ${selected.size}개 · 목록 ${rows.length}개`;
}

function fillForm(assignment, id) {
 editingId = id || '';
 if ($('assign-title')) $('assign-title').value = (assignment && assignment.title) || '';
 if ($('assign-desc')) $('assign-desc').value = (assignment && assignment.description) || '';
 if ($('assign-open-at')) $('assign-open-at').value = toDatetimeLocal(assignment && assignment.openAt);
 if ($('assign-due-at')) $('assign-due-at').value = toDatetimeLocal(assignment && assignment.dueAt);
 if ($('assign-open')) $('assign-open').checked = !assignment || assignment.open !== false;
 const want = new Set((assignment && assignment.classrooms) || []);
 document.querySelectorAll('#assign-classes input[type="checkbox"]').forEach((box) => {
  box.checked = want.size ? want.has(box.value) : box.value === selectedClassId();
 });
 const targets = new Set((assignment && assignment.targets || []).map((t) => `${t.type}:${t.id}`));
 document.querySelectorAll('#target-picker input[type="checkbox"]').forEach((box) => {
  box.checked = targets.has(`${box.dataset.targetType}:${box.value}`);
 });
 paintPicker();
 note('assign-form-note', editingId ? `수정 중 · ${assignment.title || editingId}` : '새 과제를 만듭니다.');
}

function assignmentForClass(row, classId) {
 if (!classId) return true;
 return Array.isArray(row.classrooms) && row.classrooms.includes(classId);
}

function paintAssignmentList() {
 const host = $('assign-list');
 if (!host) return;
 const classId = selectedClassId();
 const rows = assignments.filter((row) => assignmentForClass(row, classId));
 if (!classId) {
  host.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!rows.length) {
  host.replaceChildren(node('p', 'small', '이 반에 만든 과제가 없습니다.'));
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const row of rows) {
  const card = node('article', 'admin-row assign-row');
  const head = node('div');
  const openLabel = row.open ? '공개' : '비공개';
  head.append(
   node('strong', '', row.title || row.id),
   node('span', 'small', `${openLabel} · 대상 ${Array.isArray(row.targets) ? row.targets.length : 0}개`)
  );
  const meta = node('p', 'small', `마감 ${formatWhen(row.dueAt) || '없음'} · ${row.classrooms.map(labelClass).join(', ')}`);
  const actions = node('div', 'actions');
  const edit = node('button', '', '수정');
  edit.type = 'button';
  edit.onclick = () => fillForm(row, row.id);
  const review = node('button', 'primary', '제출 보기');
  review.type = 'button';
  review.onclick = () => {
   selectedAssignmentId = row.id;
   paintReviewSelect();
   loadSubmissions();
   const panel = $('review-panel');
   if (panel) panel.scrollIntoView({behavior: 'smooth', block: 'start'});
  };
  actions.append(edit, review);
  card.append(head, meta, actions);
  wrap.append(card);
 }
 host.replaceChildren(wrap);
}

function paintReviewSelect() {
 const select = $('review-assignment');
 if (!select) return;
 const classId = selectedClassId();
 const rows = assignments.filter((row) => assignmentForClass(row, classId));
 const keep = selectedAssignmentId;
 select.replaceChildren();
 select.append(Object.assign(node('option', '', '과제를 선택하세요'), {value: ''}));
 for (const row of rows) {
  const opt = node('option', '', row.title || row.id);
  opt.value = row.id;
  select.append(opt);
 }
 if (keep && rows.some((row) => row.id === keep)) select.value = keep;
 else {
  selectedAssignmentId = rows[0] ? rows[0].id : '';
  select.value = selectedAssignmentId;
 }
}

function currentAssignment() {
 return assignments.find((row) => row.id === selectedAssignmentId) || null;
}

function paintSubmissions() {
 const host = $('submission-list');
 if (!host) return;
 const assignment = currentAssignment();
 if (!selectedClassId()) {
  host.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!assignment) {
  host.replaceChildren(node('p', 'small', '확인할 과제를 고르세요.'));
  return;
 }
 if (!submissions.length) {
  host.replaceChildren(node('p', 'small', '이 반에서 아직 제출한 학생이 없습니다.'));
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const row of submissions) {
  const card = node('button', 'admin-row assign-row assign-sub-btn', '');
  card.type = 'button';
  const head = node('div');
  head.append(
   node('strong', '', studentLabel(row)),
   node('span', 'small', statusLabel(row))
  );
  const meta = node('p', 'small', `${formatWhen(row.submittedAt) || ''} · ${reviewLabel(row.reviewStatus)} · ${row.attemptCount || 1}회`);
  card.append(head, meta);
  card.onclick = () => {
   detailUid = row.uid;
   paintDetail();
  };
  wrap.append(card);
 }
 host.replaceChildren(wrap);
 note('review-note', `${labelClass(selectedClassId())} · 제출 ${submissions.length}명`);
}

function paintDetail() {
 const host = $('submission-detail');
 if (!host) return;
 const row = submissions.find((item) => item.uid === detailUid);
 if (!row) {
  host.replaceChildren(node('p', 'small', '목록에서 제출물을 고르면 소스와 출력을 봅니다.'));
  return;
 }
 const head = node('div');
 head.append(node('h3', '', studentLabel(row)), node('p', 'small', `${statusLabel(row)} · ${reviewLabel(row.reviewStatus)} · ${row.attemptCount || 1}회`));
 const gradeNote = node('p', 'small', BROWSER_GRADE_NOTE);
 const targets = node('div', 'assign-sources');
 for (const [key, target] of Object.entries(row.targets || {})) {
  const card = node('article', 'assign-source');
  const title = targetTitle({type: target.type, id: target.id}, catalog) || key;
  card.append(node('h4', '', `${target.type === 'example' ? '예제' : '문제'} · ${target.id}`));
  card.append(node('p', 'small', `${title} · ${target.grade && target.grade.ok ? '통과' : '미통과'} · 시도 ${target.attempts || 0}`));
  const href = targetHref(prefix, {type: target.type, id: target.id, unit: target.unit}, catalog);
  if (href) {
   const link = node('a', '', '실습 화면으로');
   link.href = href;
   card.append(link);
  }
  if (target.stdin) card.append(node('p', 'small', `표준 입력: ${target.stdin}`));
  if (target.args && target.args !== '[]') card.append(node('p', 'small', `실행 인자: ${target.args}`));
  for (const [name, source] of Object.entries(target.files || {})) {
   card.append(node('p', 'small', name));
   card.append(node('pre', '', source || '(비어 있음)'));
  }
  if (target.output) {
   card.append(node('p', 'small', '출력'));
   card.append(node('pre', '', target.output));
  }
  targets.append(card);
 }
 const review = node('div', 'assign-review-form');
 review.append(node('label', '', '한 줄 코멘트'));
 const input = node('input');
 input.id = 'review-comment';
 input.maxLength = COMMENT_MAX;
 input.value = row.reviewComment || '';
 input.placeholder = COMMENT_PLACEHOLDER;
 const save = node('button', 'primary', '확인함');
 save.type = 'button';
 save.onclick = () => saveReview(row, input.value);
 const stub = node('p', 'small', REGRADE_NOTE);
 review.append(input, save, stub);
 if (Array.isArray(row.history) && row.history.length) {
  const hist = node('details', 'assign-history');
  hist.append(node('summary', '', `이전 제출 ${row.history.length}회`));
  for (const item of row.history) {
   hist.append(node('p', 'small', `${formatWhen(item.submittedAt) || ''} · ${statusLabel(item)} · ${item.attemptCount || ''}회`));
  }
  host.replaceChildren(head, gradeNote, targets, review, hist);
  return;
 }
 host.replaceChildren(head, gradeNote, targets, review);
}

async function saveAssignment() {
 if (writing) return;
 const fields = readForm();
 if (!assignmentReady(fields)) {
  toast('제목, 반, 문제·예제를 모두 넣어 주세요.');
  return;
 }
 writing = true;
 try {
  const {db, store} = await load();
  const payload = {
   ...fields,
   openAt: fields.openAt || null,
   dueAt: fields.dueAt || null,
   updatedAt: store.serverTimestamp()
  };
  if (editingId) {
   const prev = assignments.find((row) => row.id === editingId);
   payload.createdBy = (prev && prev.createdBy) || teacherEmail;
   payload.createdAt = prev && prev.createdAt ? prev.createdAt : store.serverTimestamp();
   await store.setDoc(store.doc(db, 'assignments', editingId), payload);
   toast('과제를 고쳤습니다.');
  } else {
   payload.createdAt = store.serverTimestamp();
   const ref = await store.addDoc(store.collection(db, 'assignments'), payload);
   editingId = ref.id;
   toast('과제를 만들었습니다.');
  }
  await loadAssignments();
 } catch (error) {
  console.error('[teacher-assignments]', error);
  toast('과제를 저장하지 못했습니다. 권한과 네트워크를 확인하세요.');
 } finally {
  writing = false;
 }
}

let deleteArmed = false;
async function deleteAssignment() {
 if (!editingId || writing) return;
 const button = $('assign-delete');
 if (!deleteArmed) {
  deleteArmed = true;
  if (button) button.textContent = '정말 지울까요?';
  setTimeout(() => {
   deleteArmed = false;
   if (button) button.textContent = '과제 삭제';
  }, 4000);
  return;
 }
 deleteArmed = false;
 if (button) button.textContent = '과제 삭제';
 writing = true;
 try {
  const {db, store} = await load();
  await store.deleteDoc(store.doc(db, 'assignments', editingId));
  toast('과제를 지웠습니다.');
  editingId = '';
  fillForm(null, '');
  await loadAssignments();
 } catch (error) {
  console.error('[teacher-assignments]', error);
  toast('과제를 지우지 못했습니다.');
 } finally {
  writing = false;
 }
}

async function saveReview(row, comment) {
 if (!row || writing) return;
 writing = true;
 try {
  const {db, store} = await load();
  const patch = teacherReviewFields({comment, email: teacherEmail});
  patch.reviewedAt = store.serverTimestamp();
  await store.updateDoc(store.doc(db, 'students', row.uid, 'submissions', row.assignmentId), patch);
  toast('확인을 남겼습니다.');
  await loadSubmissions();
 } catch (error) {
  console.error('[teacher-assignments]', error);
  toast('확인을 저장하지 못했습니다.');
 } finally {
  writing = false;
 }
}

async function loadAssignments() {
 const {db, store} = await load();
 const snap = await store.getDocs(store.collection(db, 'assignments'));
 assignments = [];
 snap.forEach((doc) => assignments.push({id: doc.id, ...doc.data()}));
 assignments.sort((a, b) => String(a.title || '').localeCompare(String(b.title || ''), 'ko'));
 paintAssignmentList();
 paintReviewSelect();
}

async function loadRoster() {
 const {db, store} = await load();
 const snap = await store.getDocs(store.collection(db, 'roster'));
 rosterRows = [];
 snap.forEach((doc) => rosterRows.push({id: doc.id, ...doc.data()}));
 classRows = classesFromRoster(rosterRows);
 paintClasses();
}

async function loadSubmissions() {
 const assignment = currentAssignment();
 const classId = selectedClassId();
 submissions = [];
 paintSubmissions();
 paintDetail();
 if (!assignment || !classId) return;
 try {
  const {db, store} = await load();
  const students = rosterRows.filter((row) => inClass(row, classId));
  const progressSnap = await store.getDocs(store.collection(db, 'progress'));
  const byEmail = new Map();
  progressSnap.forEach((doc) => {
   const data = doc.data();
   if (data && data.email) byEmail.set(String(data.email).toLowerCase(), {uid: data.uid || doc.id, ...data});
  });
  const reads = students.map(async (row) => {
   const email = String(row.email || row.id || '').toLowerCase();
   const person = byEmail.get(email);
   if (!person || !person.uid) return null;
   const snap = await store.getDoc(store.doc(db, 'students', person.uid, 'submissions', assignment.id));
   if (!snap.exists()) return null;
   return {id: snap.id, uid: person.uid, ...snap.data(), name: person.name || row.name, studentId: person.studentId || row.studentId};
  });
  submissions = (await Promise.all(reads)).filter(Boolean);
  submissions.sort((a, b) => studentLabel(a).localeCompare(studentLabel(b), 'ko'));
  paintSubmissions();
  paintDetail();
 } catch (error) {
  console.error('[teacher-assignments]', error);
  note('review-note', '제출물을 읽지 못했습니다.');
 }
}

function bind() {
 const save = $('assign-save');
 if (save) save.onclick = saveAssignment;
 const clear = $('assign-new');
 if (clear) clear.onclick = () => fillForm(null, '');
 const remove = $('assign-delete');
 if (remove) remove.onclick = deleteAssignment;
 for (const id of ['target-unit', 'target-type']) {
  if ($(id)) $(id).onchange = paintPicker;
 }
 if ($('target-search')) $('target-search').oninput = paintPicker;
 if ($('target-picker')) $('target-picker').addEventListener('change', paintPicker);
 if ($('review-assignment')) {
  $('review-assignment').onchange = () => {
   selectedAssignmentId = $('review-assignment').value;
   loadSubmissions();
  };
 }
}

async function review(user) {
 const tools = $('assign-tools');
 if (!tools) return;
 if (!ready) {
  tools.hidden = true;
  status('로그인 설정이 없어 과제를 만들 수 없습니다.');
  return;
 }
 if (!user) {
  teacherEmail = '';
  tools.hidden = true;
  status('헤더의 “학교 계정으로 로그인”으로 먼저 로그인하세요.');
  return;
 }
 const email = (user.email || '').toLowerCase();
 if (!(await isTeacher(email))) {
  tools.hidden = true;
  status('이 계정에는 교사 권한이 없습니다.');
  return;
 }
 teacherEmail = email;
 status(`교사 권한 확인됨 · ${email}`);
 tools.hidden = false;
 bind();
 await loadRoster();
 if (!editingId) fillForm(null, '');
 await loadAssignments();
 await loadSubmissions();
}

async function start() {
 if (!$('assign-gate')) return;
 catalogItems = [];
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  catalogItems = catalogTargets(catalog);
 } catch (error) {
  console.warn('[teacher-assignments] catalog', error);
 }
 const unit = $('target-unit');
 if (unit && !unit.options.length) {
  unit.append(Object.assign(node('option', '', '모든 단원'), {value: ''}));
  for (const n of [1, 2, 3, 4]) {
   const opt = node('option', '', `${n}단원`);
   opt.value = String(n);
   unit.append(opt);
  }
 }
 paintPicker();
 document.addEventListener('aipy:account', (event) => review(event.detail.user));
 document.addEventListener('aipy:class', () => {
  paintClasses();
  paintAssignmentList();
  paintReviewSelect();
  loadSubmissions();
 });
 document.addEventListener('aipy:roster-changed', () => loadRoster());
 if (window.aipyAccount) review(window.aipyAccount.user);
}

start();
