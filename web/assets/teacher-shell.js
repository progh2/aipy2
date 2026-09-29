/* 교사 관리 화면의 공통 뼈대. 헤더 아래 반 선택과 명단/보드/세션/과제/답변 내역 내비게이션을 붙입니다.
   이 스크립트는 관리 페이지에만 넣습니다. 로그인·설정 실패는 학습을 막지 않습니다. */
import {ready} from './firebase-config.js';
import {load, readTeacherFlag} from './auth.js';
import {teacherPickerEmpty} from './auth-model.js';
import {
 classesFromRoster, resolveSelectedClass, writeSelectedClass, publishClass,
 mountClassPicker, paintClassContext
} from './class-picker.js';

const PAGES = [
 {id: 'roster', href: 'admin.html', label: '명단'},
 {id: 'ops', href: 'ops.html', label: '운영'},
 {id: 'board', href: 'board.html', label: '현황 보드'},
 {id: 'session', href: 'session.html', label: '수업 세션'},
 {id: 'assignments', href: 'assignments.html', label: '과제'},
 {id: 'answers', href: 'answers.html', label: '답변 내역'}
];

const host = document.getElementById('teacher-shell');
let teacherEmail = '';
let pickerHost = null;

function node(tag, cls, text) {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
}

// (#141) 교사 권한이 확인되기 전에는 관리 화면 본문을 숨기고, 교사가 아니면 '교사 전용' 안내만 보인다.
// 학생 데이터는 원래 firestore.rules가 막지만(비교사 목록 조회 거부), 보드·세션 화면 틀이 학생에게
// 보이던 문제를 막는다. ?demo=1(가짜 데이터 미리보기)은 잠그지 않는다. 네트워크 오류로 권한을
// 확인하지 못한 경우엔 교사가 수업 중 잠기지 않도록 본문을 연다(데이터는 규칙이 계속 보호).
const DEMO = new URLSearchParams(location.search).get('demo') === '1';
let pendingTimer = 0;
function lockNote() { return document.getElementById('teacher-lock-note'); }
function settleGate() {
 clearTimeout(pendingTimer);
 document.body.classList.remove('teacher-pending');
}
function lockTeacherPage(message) {
 settleGate();
 document.body.classList.add('teacher-locked');
 let note = lockNote();
 if (!note) {
  note = node('section', 'teacher-lock-note admin-card');
  note.id = 'teacher-lock-note';
  const main = document.querySelector('main');
  if (main) main.prepend(note); else document.body.append(note);
 }
 note.replaceChildren(node('h2', '', '교사 전용 페이지입니다'), node('p', '', message));
}
function unlockTeacherPage() {
 settleGate();
 document.body.classList.remove('teacher-locked');
 const note = lockNote();
 if (note) note.remove();
}

function currentPage() {
 return (host && host.dataset.teacherPage) || document.body.dataset.teacherPage || 'roster';
}

function renderChrome() {
 if (!host) return;
 const page = currentPage();
 const bar = node('div', 'teacher-shell-bar');
 const brand = node('p', 'teacher-shell-title', '수업 관리');
 const nav = node('nav', 'teacher-shell-nav');
 nav.setAttribute('aria-label', '교사 관리 메뉴');
 for (const item of PAGES) {
  const link = node('a', '', item.label);
  link.href = item.href;
  if (item.id === page) link.setAttribute('aria-current', 'page');
  nav.append(link);
 }
 const row = node('div', 'teacher-shell-row');
 row.append(brand, nav);
 pickerHost = node('div', 'class-picker');
 pickerHost.id = 'class-picker';
 bar.append(row, pickerHost);
 host.classList.add('teacher-shell');
 host.replaceChildren(bar);
 mountClassPicker(pickerHost, {classes: [], disabled: true, emptyText: '로그인하면 반을 선택할 수 있습니다'});
 paintClassContext({classId: '', label: '반 미선택'});
}

function setPicker(options) {
 if (!pickerHost) return;
 mountClassPicker(pickerHost, {
  ...options,
  onChange: (id) => {
   writeSelectedClass(teacherEmail, id);
   publishClass(id);
  }
 });
}

async function fetchRosterRows() {
 const {db, store} = await load();
 const snapshot = await store.getDocs(store.collection(db, 'roster'));
 const rows = [];
 snapshot.forEach((doc) => rows.push(doc.data()));
 return rows;
}

export async function refreshTeacherClasses() {
 if (!teacherEmail) return;
 try {
  const classes = classesFromRoster(await fetchRosterRows());
  const selected = resolveSelectedClass(teacherEmail, classes);
  if (selected) writeSelectedClass(teacherEmail, selected);
  setPicker({
   classes,
   selected,
   disabled: classes.length === 0,
   emptyText: '명단에 등록된 반이 없습니다'
  });
  publishClass(selected);
 } catch (error) {
  console.error('[teacher-shell]', error);
  setPicker({
   classes: [],
   disabled: true,
   emptyText: teacherPickerEmpty({ready: true, user: {email: teacherEmail}, teacher: true, error})
  });
 }
}

async function review(user) {
 if (!ready) {
  setPicker({classes: [], disabled: true, emptyText: teacherPickerEmpty({ready: false})});
  publishClass('');
  if (!DEMO) lockTeacherPage('로그인 기능을 불러오지 못했습니다. 교사 계정으로 다시 접속하세요.');
  return;
 }
 if (!user) {
  teacherEmail = '';
  setPicker({classes: [], disabled: true, emptyText: teacherPickerEmpty({ready: true, user: null})});
  publishClass('');
  if (!DEMO) lockTeacherPage('학교 교사 계정으로 로그인해야 볼 수 있습니다.');
  return;
 }
 const email = (user.email || '').toLowerCase();
 teacherEmail = email;
 const {teacher, error} = await readTeacherFlag(email);
 if (!teacher) {
  setPicker({
   classes: [],
   disabled: true,
   emptyText: teacherPickerEmpty({ready: true, user, teacher: false, error})
  });
  publishClass('');
  if (DEMO) settleGate();
  else if (error) unlockTeacherPage();
  else lockTeacherPage('이 계정에는 교사 권한이 없습니다.');
  return;
 }
 unlockTeacherPage();
 await refreshTeacherClasses();
}

function startTeacherShell() {
 if (!host) {
  console.info('[teacher-shell] 관리 뼈대가 없는 페이지입니다.');
  return;
 }
 renderChrome();
 if (!DEMO) {
  document.body.classList.add('teacher-pending');
  // 로그인 확인 이벤트가 끝내 오지 않으면(스크립트 로드 실패 등) 화면을 영구히 가리지 않는다.
  pendingTimer = setTimeout(settleGate, 10000);
 }
 document.addEventListener('aipy:account', (event) => review(event.detail.user));
 document.addEventListener('aipy:roster-changed', () => refreshTeacherClasses());
 if (window.aipyAccount) review(window.aipyAccount.user);
}

startTeacherShell();
