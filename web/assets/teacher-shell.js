/* 교사 관리 화면의 공통 뼈대. 헤더 아래 반 선택과 명단/보드/세션/과제 내비게이션을 붙입니다.
   이 스크립트는 관리 페이지에만 넣습니다. 로그인·설정 실패는 학습을 막지 않습니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {
 classesFromRoster, resolveSelectedClass, writeSelectedClass, publishClass,
 mountClassPicker, paintClassContext
} from './class-picker.js';

const PAGES = [
 {id: 'roster', href: 'admin.html', label: '명단'},
 {id: 'board', href: 'board.html', label: '현황 보드'},
 {id: 'session', href: 'session.html', label: '수업 세션'},
 {id: 'assignments', href: 'assignments.html', label: '과제'}
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

async function isTeacher(email) {
 const {db, store} = await load();
 try {
  return (await store.getDoc(store.doc(db, 'admins', email))).exists();
 } catch (error) {
  console.error('[teacher-shell]', error);
  return false;
 }
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
  setPicker({classes: [], disabled: true, emptyText: '명단을 읽지 못했습니다'});
 }
}

async function review(user) {
 if (!ready) {
  setPicker({classes: [], disabled: true, emptyText: '로그인 설정이 없어 반을 고를 수 없습니다'});
  publishClass('');
  return;
 }
 if (!user) {
  teacherEmail = '';
  setPicker({classes: [], disabled: true, emptyText: '로그인하면 반을 선택할 수 있습니다'});
  publishClass('');
  return;
 }
 const email = (user.email || '').toLowerCase();
 teacherEmail = email;
 if (!(await isTeacher(email))) {
  setPicker({classes: [], disabled: true, emptyText: '교사 권한이 확인되면 반을 고를 수 있습니다'});
  publishClass('');
  return;
 }
 await refreshTeacherClasses();
}

function startTeacherShell() {
 if (!host) {
  console.info('[teacher-shell] 관리 뼈대가 없는 페이지입니다.');
  return;
 }
 renderChrome();
 document.addEventListener('aipy:account', (event) => review(event.detail.user));
 document.addEventListener('aipy:roster-changed', () => refreshTeacherClasses());
 if (window.aipyAccount) review(window.aipyAccount.user);
}

startTeacherShell();
