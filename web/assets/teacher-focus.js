/* 교사 단원 페이지 초점. 로그인·admins 확인 + 선택한 반의 활성 세션이 있을 때만
   주제 앵커·예제 클릭으로 sessions/{반}.focus를 갱신합니다. 아니면 기존 학습만 합니다.
   반은 window.aipyClass, 없으면 aipy-teacher-class:{email} localStorage에서 읽습니다. */
import {ready} from './firebase-config.js';
import {load, readTeacherFlag} from './auth.js';
import {dataFailureNote} from './auth-model.js';
import {publishClass, resolveTeacherClassId, labelClass} from './class-picker.js';
import {
 isSessionLive, pageFromPath, focusFromUnitClick, focusWritePayload, focusHref,
 sessionFields, expiresAtMillis, existingAttentionNonce, wholeNonce, blockAnchor, blockOnlyAllowed,
 focusFields
} from './follow-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

const prefix = document.body.dataset.prefix || '';
let teacherEmail = '';
let classIdValue = '';
let current = null;
let sessionUnsub = null;
let toastTimer = 0;
let cueTimer = 0;
let lastCueState = '';
let lastTracked = '';
let trackTimer = 0;

// ── 교사가 실제로 보고 있는 위치 추적(#126): 화면 상단 근처의 소단원/문항 컨테이너(id)를 먼저 찾고,
//    그 안에서 다시 build.py가 매긴 [data-fb] 블록(화면 한 장 단위)을 찾아 훨씬 촘촘한 위치를 기록한다.
//    'id@비율'(옛 형식) 또는 'id~b{n}@비율'(블록) — 규칙의 focus.topicAnchor(문자열 80자 이내)를
//    그대로 쓰므로 규칙 변경이 없다. 학생의 '선생님 화면으로 이동'이 이 지점으로 간다.
//    컨테이너 탐색은 절대 건드리지 않는다 — 보조 섹션(pre-api 등)을 잡으면 학생이 없는 페이지로 이동한
//    사고(#105/#106)가 있었다. querySelectorAll을 컨테이너로 스코프해 블록도 그 밖으로 새지 않는다.
function viewAnchor() {
 const z = parseFloat(document.body.style.zoom) || 1;
 const viewTop = 110 / z; // 헤더 아래
 let best = null, bestTop = -Infinity;
 // 소단원과 문항만 추적한다. 보조 섹션(pre-api 등)을 잡으면 학생이 없는 페이지로 이동한다.
 for (const el of document.querySelectorAll('main section.lesson[id], main .question[id]')) {
  const r = el.getBoundingClientRect();
  const top = r.top / z, height = r.height / z;
  if (height < 40 || !el.id) continue;
  if (top <= viewTop && top > bestTop) { best = el; bestTop = top; }
 }
 if (!best) {
  // (#126) 컨테이너가 없는 페이지(예제·연습문제 목록·단원 인덱스 등)는 id 없는 블록 전용
  // 앵커('~b{n}@비율')로만 추적한다. blockOnlyAllowed가 그 페이지가 안전한지 검사하는 단일
  // 출처다 — q-*.html처럼 pageTopicId가 소단원 id를 반환하는 페이지에서는 절대 false라서
  // 여기로 오지 않는다(빈 id 앵커가 오면 resolveFocusLocation이 다른 페이지로 잘못 판단한다).
  if (!blockOnlyAllowed(currentPage())) return '';
  const main = document.querySelector('main');
  if (!main) return '';
  let mainBlock = null, mainBlockTop = -Infinity;
  for (const el of main.querySelectorAll('[data-fb]')) {
   const r = el.getBoundingClientRect();
   const top = r.top / z, height = r.height / z;
   if (height < 10 || !el.dataset.fb) continue;
   if (top <= viewTop && top > mainBlockTop) { mainBlock = el; mainBlockTop = top; }
  }
  if (!mainBlock) return '';
  const mainHeight = mainBlock.getBoundingClientRect().height / z;
  const mainFrac = mainHeight > 0 ? (viewTop - mainBlockTop) / mainHeight : 0;
  return blockAnchor('', mainBlock.dataset.fb, mainFrac);
 }
 let block = null, blockTop = -Infinity;
 for (const el of best.querySelectorAll('[data-fb]')) {
  const r = el.getBoundingClientRect();
  const top = r.top / z, height = r.height / z;
  if (height < 10 || !el.dataset.fb) continue;
  if (top <= viewTop && top > blockTop) { block = el; blockTop = top; }
 }
 if (block) {
  const height = block.getBoundingClientRect().height / z;
  const frac = height > 0 ? (viewTop - blockTop) / height : 0;
  return blockAnchor(best.id, block.dataset.fb, frac);
 }
 const height = best.getBoundingClientRect().height / z;
 const frac = height > 0 ? (viewTop - bestTop) / height : 0;
 return blockAnchor(best.id, null, frac);
}

async function trackScroll() {
 if (!canSend() || !isSessionLive(current)) return;
 const anchor = viewAnchor();
 if (!anchor || anchor === lastTracked) return;
 lastTracked = anchor;
 try {
  const {db, store} = await load();
  // 추적 갱신은 예제 선택을 담지 않는다 — 남겨 두면 학생 편집기가 갱신마다 예제를 다시 열어 초기화된다.
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   'focus.page': currentPage(),
   'focus.topicAnchor': anchor,
   'focus.exampleId': null,
   'focus.updatedAt': store.serverTimestamp()
  });
 } catch (error) {
  console.warn('[teacher-focus] track', error);
 }
}

// (#126) 1.2초 스로틀 + 트레일링: 스크롤이 시작되면 스로틀 창이 비어 있으면 바로 보내고, 창 안에서
// 또 스크롤하면 창이 끝나는 시점에 마지막 위치로 한 번 더 보낸다(스크롤이 멈춘 뒤의 최종 위치를 반드시
// 반영). 예전의 '3초 후 1회'보다 훨씬 촘촘하다.
const TRACK_THROTTLE_MS = 1200;
let lastTrackAt = 0;

function scheduleTrack() {
 const cue = document.getElementById('teacher-focus-ui');
 if (cue && !cue.hidden) cue.hidden = true; // 스크롤을 시작하면 안내는 접는다
 const now = Date.now();
 const elapsed = now - lastTrackAt;
 clearTimeout(trackTimer);
 if (elapsed >= TRACK_THROTTLE_MS) {
  lastTrackAt = now;
  trackTimer = 0;
  trackScroll();
 } else {
  trackTimer = setTimeout(() => {
   trackTimer = 0;
   lastTrackAt = Date.now();
   trackScroll();
  }, TRACK_THROTTLE_MS - elapsed);
 }
}

function currentPage() {
 return pageFromPath(location.pathname);
}

// 세션을 먼저 켜지 않아도 버튼이 보인다. 첫 전송 때 세션을 자동으로 시작한다.
function canSend() {
 return Boolean(teacherEmail && classIdValue);
}

function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text || '';
 clearTimeout(toastTimer);
 toastTimer = setTimeout(() => { box.textContent = ''; }, 4200);
}

function paintCue() {
 let root = document.getElementById('teacher-focus-ui');
 if (!canSend()) {
  if (root) root.hidden = true;
  lastCueState = '';
  document.body.classList.remove('teacher-focus-live');
  removeFocusButtons();
  return;
 }
 injectFocusButtons();
 injectDetailFocusButtons();
 if (!root) {
  root = node('div', 'teacher-focus-ui');
  root.id = 'teacher-focus-ui';
  const status = node('p', 'teacher-focus-status', '');
  status.id = 'teacher-focus-status';
  const toggleLabel = node('label', 'teacher-focus-detail-toggle', '');
  const toggle = node('input', '', '');
  toggle.type = 'checkbox';
  toggle.checked = detailChipsEnabled();
  toggle.addEventListener('change', () => {
   setDetailChipsEnabled(toggle.checked);
   if (toggle.checked) injectDetailFocusButtons();
  });
  toggleLabel.append(toggle, document.createTextNode(' 📍 세부 초점 버튼 보이기'));
  const close = node('button', 'teacher-focus-close', '✕');
  close.type = 'button';
  close.title = '안내 닫기';
  close.addEventListener('click', () => { root.hidden = true; });
  root.append(status, toggleLabel, close);
  const header = document.querySelector('header.top');
  if (header) header.after(root);
  else document.body.prepend(root);
 }
 setDetailChipsEnabled(detailChipsEnabled());
 document.body.classList.add('teacher-focus-live');
 // 스크롤 추적으로 세션 문서가 2초마다 갱신되므로, 반·세션 상태가 실제로 바뀔 때만 띠를 다시 펼친다(깜빡임 방지).
 const cueState = `${classIdValue}|${isSessionLive(current) ? 'live' : 'idle'}`;
 if (cueState !== lastCueState) {
  lastCueState = cueState;
  root.hidden = false;
  clearTimeout(cueTimer);
  cueTimer = setTimeout(() => { root.hidden = true; }, 6000);
 }
 document.getElementById('teacher-focus-status').textContent =
  `${labelClass(classIdValue)}에 초점을 보내요. 📍 버튼을 누르면 학생 화면 우하단에 이동 안내가 떠요.` +
  (isSessionLive(current) ? '' : ' (첫 전송 때 수업 세션이 자동으로 시작돼요)');
}

// 교사에게만 보이는 '초점 보내기' 버튼을 소단원 제목·실습 워크스페이스·문항 카드에 붙인다(#84).
// 앵커 클릭으로도 초점이 가지만, 눈에 보이는 버튼이 있어야 수업 중 바로 누를 수 있다.
let questionObserver = null;
function focusButton(anchorId, exampleId, label) {
 const b = node('button', 'focus-send', label || '📍 초점 보내기');
 b.type = 'button';
 b.title = '따라오는 학생 화면을 이 위치로 옮깁니다';
 b.addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  if (!canSend()) return;
  const focus = exampleId
   ? focusFromUnitClick({exampleId, lessonId: anchorId, currentPage: currentPage()})
   : focusFromUnitClick({href: '#' + anchorId, currentPage: currentPage()});
  if (focus) sendFocus(focus);
 });
 return b;
}
function injectFocusButtons() {
 if (!canSend()) return;
 document.querySelectorAll('section.lesson[id]').forEach((lesson) => {
  const h2 = lesson.querySelector('h2');
  if (!h2 || h2.querySelector('.focus-send')) return;
  h2.append(focusButton(lesson.id, null));
  const ws = lesson.querySelector('.lesson-workspace');
  const first = ws && ws.querySelector('[data-example]');
  const h3 = ws && ws.querySelector('h3');
  if (h3 && first && !h3.querySelector('.focus-send')) h3.append(focusButton(lesson.id, first.dataset.example, '📍 실습으로 초점'));
 });
 document.querySelectorAll('#questions .question[id]').forEach((card) => {
  const meta = card.querySelector('.question-meta') || card;
  if (meta.querySelector('.focus-send')) return;
  meta.append(focusButton(card.id, null, '📍 이 문제로 초점'));
 });
 const host = document.getElementById('questions');
 if (host && !questionObserver) {
  questionObserver = new MutationObserver(() => injectFocusButtons());
  questionObserver.observe(host, {childList: true});
 }
}
function removeFocusButtons() {
 document.querySelectorAll('.focus-send').forEach((el) => el.remove());
 removeDetailFocusButtons();
}

// ── 세부 초점 버튼(#140): 소단원 화면 안의 슬라이드·설명·과제·실습 카드 등 각 요소에 작은
//    📍 칩을 붙인다. 클릭하면 그 요소의 블록 앵커(blockAnchor, follow-model.js)로 초점을 보낸다.
//    본문 레이아웃을 밀지 않도록 절대 위치 오버레이로만 붙이고, 기본은 hover(또는 focus-within)
//    할 때만 보인다 — 버튼이 항상 다 보이면 화면이 산만해진다.
const DETAIL_CHIPS_KEY = 'aipy-focus-detail-chips';

function detailChipsEnabled() {
 try {
  return localStorage.getItem(DETAIL_CHIPS_KEY) !== '0';
 } catch { return true; }
}

function setDetailChipsEnabled(on) {
 try { localStorage.setItem(DETAIL_CHIPS_KEY, on ? '1' : '0'); } catch { /* 사생활 모드 */ }
 document.body.classList.toggle('teacher-focus-detail-off', !on);
}

// 요소 자신이 data-fb를 가지고 있으면 그것을, 없으면 안(첫 자손)에서, 그래도 없으면 밖(조상)에서
// 가장 가까운 [data-fb]를 찾는다. 동적으로 만들어지는 요소(코드 읽기 줄 등)는 대개 조상에서 찾는다.
function fbBlockFor(el) {
 if (!el) return null;
 if (el.dataset && el.dataset.fb) return el.dataset.fb;
 const desc = el.querySelector && el.querySelector('[data-fb]');
 if (desc) return desc.dataset.fb;
 const anc = el.closest && el.closest('[data-fb]');
 return anc ? anc.dataset.fb : null;
}

function detailChipButton(label) {
 const b = node('button', 'focus-chip', '');
 b.type = 'button';
 b.title = '학생 화면을 이 위치로 옮깁니다';
 const icon = node('span', 'focus-chip-icon', '📍');
 icon.setAttribute('aria-hidden', 'true');
 const text = node('span', 'focus-chip-label', label);
 b.append(icon, text);
 return b;
}

// el에 칩을 하나 붙인다(이미 자기 칩이 있으면 건너뛴다). buildAnchor()는 anchorId(소단원/문항
// 컨테이너 id, 없으면 '')를 받아 최종 앵커 문자열을 돌려준다 — 페이지 종류마다 컨테이너 규칙이
// 달라서 호출부에서 결정한다.
function attachDetailChip(el, label, containerId) {
 if (!el || !el.appendChild) return;
 if ([...el.children].some((c) => c.classList && c.classList.contains('focus-chip'))) return;
 el.classList.add('focus-chip-host');
 const chip = detailChipButton(label);
 chip.addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  if (!canSend()) return;
  const block = fbBlockFor(el);
  const anchor = blockAnchor(containerId || '', block, 0);
  if (!anchor) return;
  sendFocus(focusFields({page: currentPage(), topicAnchor: anchor, exampleId: null}));
 });
 el.appendChild(chip);
}

// 소단원 컨테이너(section.lesson[id]) 안에서만 쓰는 세밀한 규칙. task-box는 상자 전체 칩 +
// 항목(li)마다 칩을 둘 다 붙인다(교사가 "이 항목만" 짚을 수 있게).
const LESSON_DETAIL_RULES = [
 {sel: 'figure.deck-slide', label: '📍 이 슬라이드'},
 {sel: '.slide-explain', label: '📍 이 설명'},
 {sel: 'details.slide-reveal', label: '📍 답 보기'},
 {sel: '.task-box', label: '📍 과제'},
 {sel: '.task-box li', label: '📍 과제 항목'},
 {sel: '.lesson-workspace', label: '📍 실습 카드'}
];
// 위 규칙에 안 걸리는 나머지 h3·pre·table(1·4단원처럼 슬라이드가 없는 페이지)은 일반 규칙으로
// 잡되, 위 상자들 안에 있는 것은 중복이라 건너뛴다.
const LESSON_GENERIC_EXCLUDE = '.task-box, .lesson-workspace, .code-read, .slide-explain, details.slide-reveal, figure.deck-slide';
const LESSON_GENERIC_RULES = [
 {sel: 'h3', label: '📍 이 설명'},
 {sel: 'pre', label: '📍 이 코드'},
 {sel: 'table', label: '📍 이 표'}
];
const PAGE_EXTRA_RULES = [
 {sel: '.exercise-section .example-card', label: '📍 연습문제'},
 {sel: '#journal', label: '📍 저널'}
];
// 예제 페이지(ex-*)용 규칙. 이 페이지들은 소단원 컨테이너가 없어(blockOnlyAllowed) id 없는
// 블록 전용 앵커('~b{n}@0')를 쓴다.
const EX_DETAIL_RULES = [
 {sel: '#predict-box', label: '📍 예측'},
 {sel: '#lab', label: '📍 편집기'},
 {sel: '.run-result', label: '📍 실행 결과'},
 // 변형 미션 섹션(다른 작업에서 추가 중) — 있을 때만 처리한다.
 {sel: '.mission, [data-mission]', label: '📍 미션'}
];

let codeReadObserver = null;

function attachCodeReadChips() {
 const list = document.getElementById('code-read-list');
 if (!list) return;
 [...list.children].forEach((item, idx) => {
  attachDetailChip(item, `📍 코드 줄 ${idx + 1}`, '');
 });
}

function injectDetailFocusButtons() {
 try { injectDetailFocusButtonsUnsafe(); } catch (error) { console.warn('[teacher-focus] 세부 초점 버튼', error); }
}

function injectDetailFocusButtonsUnsafe() {
 if (!canSend()) return;
 const main = document.querySelector('main');
 if (!main) return;
 main.querySelectorAll('section.lesson[id]').forEach((lesson) => {
  const containerId = lesson.id;
  LESSON_DETAIL_RULES.forEach(({sel, label}) => {
   lesson.querySelectorAll(sel).forEach((el) => attachDetailChip(el, label, containerId));
  });
  LESSON_GENERIC_RULES.forEach(({sel, label}) => {
   lesson.querySelectorAll(sel).forEach((el) => {
    if (el.closest(LESSON_GENERIC_EXCLUDE)) return;
    attachDetailChip(el, label, containerId);
   });
  });
 });
 // 이 페이지 자체가 예제·연습문제 목록처럼 소단원 컨테이너가 없는 페이지(blockOnlyAllowed)면
 // #journal 등도 이 페이지에 머무는 id 없는 블록 전용 앵커를 써야 한다 — lessonIdNear가 돌려주는
 // body.dataset.topic(그 소단원 id)을 그대로 쓰면 다른 페이지(소단원 설명 페이지)로 잘못 이동한다.
 const pageIsBlockOnly = blockOnlyAllowed(currentPage());
 PAGE_EXTRA_RULES.forEach(({sel, label}) => {
  main.querySelectorAll(sel).forEach((el) => {
   const containerId = pageIsBlockOnly ? '' : (lessonIdNear(el) || '');
   attachDetailChip(el, label, containerId);
  });
 });
 // 예제 페이지(section.lesson 없음)는 id 없는 블록 전용 앵커만 허용된다(blockOnlyAllowed).
 if (pageIsBlockOnly) {
  EX_DETAIL_RULES.forEach(({sel, label}) => {
   main.querySelectorAll(sel).forEach((el) => attachDetailChip(el, label, ''));
  });
  attachCodeReadChips();
  const list = document.getElementById('code-read-list');
  if (list && !codeReadObserver) {
   codeReadObserver = new MutationObserver(() => attachCodeReadChips());
   codeReadObserver.observe(list, {childList: true});
  }
 }
}

function removeDetailFocusButtons() {
 document.querySelectorAll('.focus-chip').forEach((el) => el.remove());
 document.querySelectorAll('.focus-chip-host').forEach((el) => el.classList.remove('focus-chip-host'));
}

function lessonIdNear(el) {
 const lesson = el && el.closest && el.closest('section.lesson[id]');
 if (lesson) return lesson.id;
 return document.body.dataset.topic || null;
}

function focusFromEvent(event) {
 const example = event.target.closest && event.target.closest('[data-example]');
 if (example && example.dataset.example) {
  return focusFromUnitClick({
   exampleId: example.dataset.example,
   lessonId: lessonIdNear(example),
   currentPage: currentPage()
  });
 }
 const link = event.target.closest && event.target.closest('a[href]');
 if (!link) return null;
 if (link.target === '_blank') return null;
 return focusFromUnitClick({
  href: link.getAttribute('href'),
  currentPage: currentPage()
 });
}

// 목적지가 실제로 있는 페이지인지 확인한다. 없는 주소로 초점을 보내면 학생 화면이 404로 튕긴다
// (2026-09-23 수업 사고 — 학생 쪽은 follow.js에서 이미 확인하지만, 교사 쪽에서도 보내기 전에 막아야
// "보냈는데 학생이 아무 반응이 없다"는 것을 교사가 알 수 있다).
async function destinationExists(focus) {
 const href = focusHref(prefix, focus);
 if (!href) return true;
 try {
  const res = await fetch(href, {method: 'HEAD'});
  return res.ok;
 } catch (error) {
  console.warn('[teacher-focus] 목적지 확인 실패', error);
  return true; // 네트워크 오류로 확인 못 할 때는 전송을 막지 않는다
 }
}

async function sendFocus(focus) {
 if (!canSend() || !focus || !focus.page) return;
 if (!(await destinationExists(focus))) {
  toast('이 위치로는 초점을 보낼 수 없습니다.');
  return;
 }
 try {
  const {db, store} = await load();
  const ref = store.doc(db, 'sessions', classIdValue);
  // 로컬 캐시(current)가 비어 있거나 오래됐다고 해서 바로 새 세션을 시작하지 않는다 — 다른 기기/탭이
  // 이미 세션을 시작했는데 이 구독이 아직 못 받았을 수 있다. 서버 최신 문서를 확인한 뒤에만 새로 시작한다
  // (teacher-session.js의 readExistingSession과 같은 방식).
  let existing = current;
  if (!isSessionLive(existing)) {
   try {
    const snap = await store.getDoc(ref);
    existing = snap.exists() ? snap.data() : null;
   } catch (error) {
    console.warn('[teacher-focus] 기존 세션 확인 실패', error);
   }
  }
  if (!isSessionLive(existing)) {
   // 세션이 없거나 만료됐으면 새로 시작하면서 초점을 담는다(teacher-session.js와 같은 문서 형식).
   const fields = sessionFields({teacherEmail, ...focus, attentionNonce: existingAttentionNonce(existing)});
   await store.setDoc(ref, {
    active: true,
    teacherEmail: fields.teacherEmail,
    startedAt: store.serverTimestamp(),
    expiresAt: store.Timestamp.fromMillis(expiresAtMillis()),
    focus: {...fields.focus, updatedAt: store.serverTimestamp()},
    attention: {nonce: wholeNonce(fields.attention.nonce), at: store.serverTimestamp()}
   });
   toast('수업 세션을 시작하고 초점을 보냈습니다.');
   return;
  }
  // 살아 있는 세션이면 초점만 갱신한다 — setDoc으로 통째로 덮어쓰면 세션이 다시 시작된 것처럼 보인다.
  await store.updateDoc(ref, {
   ...focusWritePayload(focus),
   'focus.updatedAt': store.serverTimestamp()
  });
  lastTracked = '';
  toast('초점을 보냈습니다.');
 } catch (error) {
  console.warn('[teacher-focus]', error);
  toast(dataFailureNote(error, `초점을 보내지 못했습니다. (${error.code || error})`));
 }
}

function onClick(event) {
 if (!canSend()) return;
 const focus = focusFromEvent(event);
 if (focus) sendFocus(focus);
}

function onExampleSelect(event) {
 if (!canSend()) return;
 const id = event.target && event.target.value;
 if (!id) return;
 const button = [...document.querySelectorAll('[data-example]')].find((el) => el.dataset.example === id);
 sendFocus(focusFromUnitClick({
  exampleId: id,
  lessonId: lessonIdNear(button),
  currentPage: currentPage()
 }));
}

let listenGen = 0;

function listen(id) {
 const gen = ++listenGen;
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 current = null;
 paintCue();
 if (!id || !teacherEmail) return;
 load().then(({db, store}) => {
  const unsub = store.onSnapshot(store.doc(db, 'sessions', id), (snap) => {
   if (gen !== listenGen) return;
   current = snap.exists() ? snap.data() : null;
   paintCue();
  }, (error) => {
   if (gen !== listenGen) return;
   console.warn('[teacher-focus]', error);
   current = null;
   paintCue();
  });
  if (gen !== listenGen) { unsub(); return; } // 오래된 호출 — 등록하지 않고 바로 해지
  sessionUnsub = unsub;
 }).catch((error) => {
  if (gen !== listenGen) return;
  console.warn('[teacher-focus]', error);
  current = null;
  paintCue();
 });
}

function applyClass(id) {
 const next = id || '';
 if (next === classIdValue && sessionUnsub) {
  paintCue();
  return;
 }
 classIdValue = next;
 if (classIdValue) publishClass(classIdValue);
 else publishClass('');
 listen(classIdValue);
}

function resolveClass() {
 applyClass(resolveTeacherClassId(teacherEmail, window.aipyClass));
}

async function isTeacher(email) {
 const {teacher} = await readTeacherFlag(email);
 return teacher;
}

async function onAccount(detail) {
 const user = detail && detail.user;
 const email = (user && user.email) ? user.email.toLowerCase() : '';
 if (!email) {
  teacherEmail = '';
  applyClass('');
  return;
 }
 if (!(await isTeacher(email))) {
  teacherEmail = '';
  applyClass('');
  return;
 }
 teacherEmail = email;
 resolveClass();
}

function startTeacherFocus() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!Number(document.body.dataset.unit)) return;
 if (!ready) return;
 document.addEventListener('click', onClick);
 window.addEventListener('scroll', scheduleTrack, {passive: true});
 const select = document.getElementById('example-select');
 if (select) select.addEventListener('change', onExampleSelect);
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 document.addEventListener('aipy:class', (event) => {
  if (!teacherEmail) return;
  const id = event.detail && event.detail.classId;
  if (id && id !== classIdValue) applyClass(id);
 });
 if (window.aipyAccount) onAccount(window.aipyAccount);
}

startTeacherFocus();
