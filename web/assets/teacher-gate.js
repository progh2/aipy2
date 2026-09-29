/* (#141) 교사용 수업 요약(teacher/index.html, unitNN.html)을 교사에게만 보이게 한다.
   정적 페이지라 완전한 비공개는 아니지만(주소를 알면 파일 자체는 받을 수 있음), 화면에서는
   로그인한 교사가 아니면 제목과 '교사 전용' 안내만 보인다. 학생 데이터는 이 페이지에 없다. */
import {ready} from './firebase-config.js';
import {readTeacherFlag} from './auth.js';

const DEMO = new URLSearchParams(location.search).get('demo') === '1';
let timer = 0;

function note(message) {
 let box = document.getElementById('teacher-lock-note');
 if (!box) {
  box = document.createElement('section');
  box.id = 'teacher-lock-note';
  box.className = 'teacher-lock-note admin-card';
  (document.querySelector('main') || document.body).prepend(box);
 }
 const h = document.createElement('h2');
 h.textContent = '교사 전용 페이지입니다';
 const p = document.createElement('p');
 p.textContent = message;
 box.replaceChildren(h, p);
}
function settle() { clearTimeout(timer); document.body.classList.remove('teacher-pending'); }
function lock(message) { settle(); document.body.classList.add('teacher-locked'); note(message); }
function unlock() {
 settle();
 document.body.classList.remove('teacher-locked');
 document.getElementById('teacher-lock-note')?.remove();
}

async function review(user) {
 if (!ready) return lock('로그인 기능을 불러오지 못했습니다. 교사 계정으로 다시 접속하세요.');
 if (!user) return lock('학교 교사 계정으로 로그인해야 볼 수 있습니다.');
 const {teacher, error} = await readTeacherFlag((user.email || '').toLowerCase());
 if (teacher || error) unlock(); // 네트워크 오류로 확인 못 하면 교사가 막히지 않게 연다.
 else lock('이 계정에는 교사 권한이 없습니다.');
}

if (!DEMO) {
 document.body.classList.add('teacher-pending');
 timer = setTimeout(settle, 10000);
 document.addEventListener('aipy:account', (event) => review(event.detail.user));
 if (window.aipyAccount) review(window.aipyAccount.user);
}
