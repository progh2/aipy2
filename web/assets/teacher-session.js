/* 교사 수업 세션. 헤더에서 고른 반(window.aipyClass)의 sessions/{학년}-{반}을 만들고 초점을 보냅니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {labelClass} from './class-picker.js';
import {inClass} from './class-picker.js';
import {
 isSessionLive, timestampMillis, countPresence, catalogPages, catalogTopics,
 catalogExamples, sessionFields, focusWritePayload, expiresAtMillis, wholeNonce, DEFAULT_PAGE
} from './follow-model.js';
import {
 choiceQuestions, focusFromQuestion, isQuestionAnchor,
 collectChoices, collectChoicesFromStates, choiceBars, appendTrail, readTrail,
 classCompletion, snapshotBaseline, readBaseline, writeBaseline, buildLessonReport,
 topicListFromCatalog, titlesFromCatalog, studentLabel
} from './lesson-report-model.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let catalog = {pages: [], topics: {}, examples: {}, questions: []};
let titles = {};
let topics = [];
let classIdValue = '';
let teacherEmail = '';
let current = null;
let sessionUnsub = null;
let presenceUnsub = null;
let progressUnsub = null;
let helpUnsub = null;
let rosterUnsub = null;
let rosterRows = [];
let progressRows = [];
let helpRows = [];
let presenceRows = [];
let assignments = [];
let togetherQuestionId = '';

function fillSelect(select, items, selected) {
 select.replaceChildren();
 for (const item of items) {
  const opt = node('option', '', item.title);
  opt.value = item.id;
  if (item.id === selected) opt.selected = true;
  select.append(opt);
 }
}

function selectedFocus() {
 const page = $('focus-page').value || DEFAULT_PAGE;
 const topic = $('focus-topic').value || null;
 const example = $('focus-example').value || null;
 return {page, topicAnchor: topic, exampleId: example};
}

function refillTopics(keep) {
 const page = $('focus-page').value;
 const topics = catalogTopics(catalog, page).map((t) => ({id: t.id, title: t.title}));
 fillSelect($('focus-topic'), [{id: '', title: '(주제 없음)'}, ...topics], keep || '');
 refillExamples(keep ? $('focus-example').value : '');
}

function refillExamples(keep) {
 const page = $('focus-page').value;
 const topicId = $('focus-topic').value;
 const topic = catalogTopics(catalog, page).find((t) => t.id === topicId);
 const examples = catalogExamples(catalog, topic);
 fillSelect($('focus-example'), [{id: '', title: '(예제 없음)'}, ...examples], keep || '');
}

function paintFocusFromSession(session) {
 const focus = session && session.focus;
 const page = (focus && focus.page) || (catalogPages(catalog)[0] && catalogPages(catalog)[0].id) || DEFAULT_PAGE;
 fillSelect($('focus-page'), catalogPages(catalog).map((p) => ({id: p.id, title: p.label || p.id})), page);
 refillTopics(focus && focus.topicAnchor);
 if (focus && focus.exampleId) $('focus-example').value = focus.exampleId;
}

function formatExpiry(session) {
 const exp = timestampMillis(session && session.expiresAt);
 if (!exp) return '';
 return new Date(exp).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
}

function paintStatus() {
 const status = $('session-status');
 const start = $('session-start');
 const end = $('session-end');
 const send = $('focus-send');
 const attention = $('attention-send');
 const together = $('together-send');
 const refresh = $('together-refresh');
 const report = $('report-refresh');
 const hasClass = Boolean(classIdValue);
 start.disabled = !hasClass || !teacherEmail;
 if (report) report.disabled = !hasClass || !teacherEmail;
 if (!hasClass) {
  status.textContent = '위에서 수업할 반을 선택하세요.';
  end.disabled = true;
  send.disabled = true;
  attention.disabled = true;
  if (together) together.disabled = true;
  if (refresh) refresh.disabled = true;
  return;
 }
 if (!current || !isSessionLive(current)) {
  status.textContent = '세션이 없어요. 시작하면 약 2시간 동안 유지돼요.';
  end.disabled = true;
  send.disabled = true;
  attention.disabled = true;
  if (together) together.disabled = true;
  if (refresh) refresh.disabled = !teacherEmail;
  return;
 }
 status.textContent = `${labelClass(classIdValue)} 진행 중 · 만료 ${formatExpiry(current) || '미정'}`;
 end.disabled = false;
 send.disabled = false;
 attention.disabled = false;
 if (together) together.disabled = !togetherQuestionId;
 if (refresh) refresh.disabled = !togetherQuestionId;
 rememberBaseline();
}

function paintCounts(rows) {
 const {following, browsing} = countPresence(rows);
 $('presence-counts').textContent = `따라오는 중 ${following} / 따로 보는 중 ${browsing}`;
}

function note(text) {
 $('focus-note').textContent = text || '';
}

function togetherNote(text) {
 const el = $('together-note');
 if (el) el.textContent = text || '';
}

function currentTogetherQuestion() {
 return choiceQuestions(catalog).find((item) => item.id === togetherQuestionId) || null;
}

function paintTogetherPicker() {
 const unit = $('together-unit');
 const select = $('together-question');
 if (!select) return;
 const unitValue = unit ? unit.value : '';
 const rows = choiceQuestions(catalog, {unit: unitValue});
 const keep = togetherQuestionId;
 select.replaceChildren();
 select.append(Object.assign(node('option', '', '선택형 문제를 고르세요'), {value: ''}));
 for (const item of rows) {
  const opt = node('option', '', `${item.id} · ${item.prompt}`);
  opt.value = item.id;
  select.append(opt);
 }
 if (keep && rows.some((row) => row.id === keep)) select.value = keep;
 else {
  togetherQuestionId = rows[0] ? rows[0].id : '';
  select.value = togetherQuestionId;
 }
 paintStatus();
}

function paintTogetherBars(question, choices) {
 const host = $('together-bars');
 if (!host) return;
 if (!question) {
  host.replaceChildren(node('p', 'small', '선택형 문제를 고르면 반 응답 막대가 나타납니다.'));
  return;
 }
 const stats = choiceBars(question, choices);
 const head = node('p', 'small', `${question.id} · 응답 ${stats.answered}/${stats.total}명 · 이름 없이 표시`);
 const list = node('div', 'together-bars-list');
 if (!stats.bars.length) {
  host.replaceChildren(head, node('p', 'small', '이 문제의 선택지가 없습니다.'));
  return;
 }
 for (const bar of stats.bars) {
  const row = node('div', 'together-bar');
  if (bar.correct) row.dataset.correct = '1';
  if (bar.crowd) row.dataset.crowd = '1';
  const label = node('span', 'together-bar-label', bar.label);
  const track = node('div', 'together-bar-track');
  const fill = node('div', 'together-bar-fill');
  fill.style.width = `${Math.round((bar.share || 0) * 100)}%`;
  track.append(fill);
  const count = node('span', 'together-bar-count', String(bar.count));
  row.append(label, track, count);
  if (bar.correct) row.append(node('span', 'small', '정답'));
  if (bar.crowd) row.append(node('span', 'small', '오답 몰림'));
  list.append(row);
 }
 const extra = [];
 if (stats.blank) extra.push(`아직 안 고름 ${stats.blank}`);
 if (stats.other) extra.push(`목록 밖 ${stats.other}`);
 host.replaceChildren(head, list, node('p', 'small', extra.join(' · ')));
}

function rememberBaseline() {
 if (!classIdValue || !isSessionLive(current)) return;
 const started = current && current.startedAt;
 const existing = readBaseline(sessionStorage, classIdValue, started);
 const topicTotal = topics.length;
 const completion = classCompletion({roster: rosterRows, progress: progressRows, classId: classIdValue, topicTotal});
 if (existing && (existing.students || !completion.students)) return;
 writeBaseline(sessionStorage, classIdValue, started, snapshotBaseline(completion));
}

function recordTrail(focus) {
 if (!classIdValue || !focus) return;
 appendTrail(sessionStorage, classIdValue, focus);
}

async function sendTogether() {
 const question = currentTogetherQuestion();
 const focus = focusFromQuestion(question);
 if (!focus || !classIdValue || !isSessionLive(current)) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   ...focusWritePayload(focus),
   'focus.updatedAt': store.serverTimestamp()
  });
  recordTrail(focus);
  togetherNote('이 문제를 초점으로 보냈어요. 학생 화면이 그 문항으로 이동합니다.');
  note('초점을 보냈습니다.');
  await refreshTogether(false);
 } catch (error) {
  console.error('[teacher-session]', error);
  togetherNote(`함께 풀기를 보내지 못했습니다. (${error.code || error})`);
 }
}

async function refreshTogether(readStates = true) {
 const question = currentTogetherQuestion();
 if (!question || !classIdValue) {
  paintTogetherBars(null, []);
  return;
 }
 let choices = collectChoices(progressRows.filter((row) => inClass(row, classIdValue)), question.id);
 const answered = choices.filter(Boolean).length;
 if (readStates && !answered) {
  try {
   const {db, store} = await load();
   const states = [];
   for (const row of progressRows.filter((item) => inClass(item, classIdValue) && item.uid)) {
    const snap = await store.getDoc(store.doc(db, 'students', row.uid, 'state', 'current'));
    if (snap.exists()) states.push(snap.data());
   }
   const fromState = collectChoicesFromStates(states, question.id);
   if (fromState.some(Boolean)) choices = fromState;
  } catch (error) {
   console.warn('[teacher-session] choices', error);
   togetherNote('저장된 선택만 보여 줍니다. 원본 답안을 읽지 못했어요.');
  }
 }
 paintTogetherBars(question, choices);
 const stats = choiceBars(question, choices);
 togetherNote(stats.answered ? `이름 없이 ${stats.answered}명 응답을 모았어요.` : '아직 고른 학생이 없어요. 답을 확인하면 막대가 늘어납니다.');
}

function paintReport(report) {
 const host = $('report-summary');
 if (!host) return;
 if (!report) {
  host.replaceChildren(node('p', 'small', '반을 고른 뒤 요약을 만들면 다음 차시 도입에 쓸 수 있어요.'));
  return;
 }
 const block = (title, body) => {
  const card = node('article', 'report-block');
  card.append(node('h3', '', title), body);
  return card;
 };
 const topicsBox = node('div');
 if (!report.topics.length) topicsBox.append(node('p', 'small', '이번 세션에서 보낸 주제나 접속 주제가 아직 없어요.'));
 else {
  const ul = node('ul', 'report-list');
  for (const item of report.topics) ul.append(node('li', '', item.title || item.id));
  topicsBox.append(ul);
 }
 const hardBox = node('div');
 if (!report.hardTop.length) hardBox.append(node('p', 'small', '어려워요 신호가 없어요.'));
 else {
  const ul = node('ul', 'report-list');
  for (const item of report.hardTop) ul.append(node('li', '', `${item.title} · ${item.count}명`));
  hardBox.append(ul);
 }
 const helpBox = node('div');
 helpBox.append(node('p', '', `미해결 ${report.openHelpCount}건`));
 if (report.openHelp.length) {
  const ul = node('ul', 'report-list');
  for (const row of report.openHelp.slice(0, 8)) {
   ul.append(node('li', '', `${studentLabel(row)}${row.topic ? ` · ${row.topic}` : ''}`));
  }
  helpBox.append(ul);
 }
 const missBox = node('div');
 if (!report.assignmentTitle) missBox.append(node('p', 'small', '이 반에 열린 과제가 없어요.'));
 else if (!report.missing.length) missBox.append(node('p', '', `${report.assignmentTitle} · 미제출 없음`));
 else {
  missBox.append(node('p', '', `${report.assignmentTitle} · 미제출 ${report.missingCount}명`));
  const ul = node('ul', 'report-list');
  for (const row of report.missing) ul.append(node('li', '', row.label));
  missBox.append(ul);
 }
 const grid = node('div', 'report-grid');
 grid.append(
  block('진행한 주제', topicsBox),
  block('완료율 변화', node('p', '', report.completionLabel)),
  block('어려워요 상위', hardBox),
  block('미해결 도움', helpBox),
  block('미제출자', missBox)
 );
 host.replaceChildren(
  node('p', 'small', `${report.classLabel} · ${report.windowLabel}`),
  grid
 );
}

async function loadReportSubmissions(assignment) {
 if (!assignment || !classIdValue) return [];
 try {
  const {db, store} = await load();
  const students = rosterRows.filter((row) => inClass(row, classIdValue));
  const byEmail = new Map();
  for (const row of progressRows) {
   const email = row && row.email ? String(row.email).toLowerCase() : '';
   if (email && row.uid) byEmail.set(email, row);
  }
  const reads = students.map(async (row) => {
   const email = String(row.email || row.id || '').toLowerCase();
   const person = byEmail.get(email);
   if (!person || !person.uid) return null;
   const snap = await store.getDoc(store.doc(db, 'students', person.uid, 'submissions', assignment.id));
   if (!snap.exists()) return null;
   return {uid: person.uid, email, ...snap.data()};
  });
  return (await Promise.all(reads)).filter(Boolean);
 } catch (error) {
  console.error('[teacher-session] submissions', error);
  return [];
 }
}

async function refreshReport() {
 if (!classIdValue) {
  paintReport(null);
  return;
 }
 rememberBaseline();
 const started = current && current.startedAt;
 const baseline = readBaseline(sessionStorage, classIdValue, started);
 const open = assignments.filter((row) => row && row.open !== false && Array.isArray(row.classrooms) && row.classrooms.includes(classIdValue));
 open.sort((a, b) => timestampMillis(b.updatedAt || b.createdAt) - timestampMillis(a.updatedAt || a.createdAt));
 const assignment = open[0] || null;
 const submissions = assignment ? await loadReportSubmissions(assignment) : [];
 const report = buildLessonReport({
  classId: classIdValue,
  session: current ? {...current, baseline} : {baseline, focus: current && current.focus},
  roster: rosterRows,
  progress: progressRows,
  help: helpRows,
  presence: presenceRows,
  trail: readTrail(sessionStorage, classIdValue),
  titles,
  topicTotal: topics.length,
  assignment,
  submissions
 });
 paintReport(report);
}

async function startSession() {
 if (!classIdValue || !teacherEmail) return;
 const {page, topicAnchor, exampleId} = selectedFocus();
 try {
  const {db, store} = await load();
  const fields = sessionFields({teacherEmail, page, topicAnchor, exampleId});
  await store.setDoc(store.doc(db, 'sessions', classIdValue), {
   active: fields.active,
   teacherEmail: fields.teacherEmail,
   startedAt: store.serverTimestamp(),
   expiresAt: store.Timestamp.fromMillis(expiresAtMillis()),
   focus: {
    page: fields.focus.page,
    topicAnchor: fields.focus.topicAnchor,
    exampleId: fields.focus.exampleId,
    updatedAt: store.serverTimestamp()
   },
   attention: {nonce: wholeNonce(fields.attention.nonce), at: store.serverTimestamp()}
  });
  recordTrail(fields.focus);
  rememberBaseline();
  note('세션을 시작했습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`세션을 시작하지 못했습니다. (${error.code || error})`);
 }
}

async function endSession() {
 if (!classIdValue || !current) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {active: false});
  note('세션을 종료했습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`세션을 종료하지 못했습니다. (${error.code || error})`);
 }
}

async function sendFocus() {
 if (!classIdValue || !isSessionLive(current)) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   ...focusWritePayload(selectedFocus()),
   'focus.updatedAt': store.serverTimestamp()
  });
  recordTrail(selectedFocus());
  note('초점을 보냈습니다.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`초점을 보내지 못했습니다. (${error.code || error})`);
 }
}

async function sendAttention() {
 if (!classIdValue || !isSessionLive(current)) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'sessions', classIdValue), {
   'attention.nonce': store.increment(1),
   'attention.at': store.serverTimestamp()
  });
  note('시선을 모았어요. 학생 쪽에 안내만 뜨고, 화면은 안 옮겨요.');
 } catch (error) {
  console.error('[teacher-session]', error);
  note(`시선 모으기를 보내지 못했습니다. (${error.code || error})`);
 }
}

function stopExtra() {
 if (progressUnsub) {
  progressUnsub();
  progressUnsub = null;
 }
 if (helpUnsub) {
  helpUnsub();
  helpUnsub = null;
 }
 if (rosterUnsub) {
  rosterUnsub();
  rosterUnsub = null;
 }
 rosterRows = [];
 progressRows = [];
 helpRows = [];
 presenceRows = [];
}

function listen(id) {
 if (sessionUnsub) {
  sessionUnsub();
  sessionUnsub = null;
 }
 if (presenceUnsub) {
  presenceUnsub();
  presenceUnsub = null;
 }
 stopExtra();
 current = null;
 paintCounts([]);
 paintStatus();
 if (!id || !teacherEmail) return;
 load().then(({db, store}) => {
  sessionUnsub = store.onSnapshot(store.doc(db, 'sessions', id), (snap) => {
   current = snap.exists() ? snap.data() : null;
   if (current && current.focus && !$('focus-page').dataset.dirty) paintFocusFromSession(current);
   if (current && current.focus && isQuestionAnchor(current.focus.topicAnchor)) {
    togetherQuestionId = current.focus.topicAnchor;
    paintTogetherPicker();
   }
   paintStatus();
   rememberBaseline();
  }, (error) => {
   console.error('[teacher-session]', error);
   note('세션을 읽지 못했습니다.');
  });
  presenceUnsub = store.onSnapshot(
   store.query(store.collection(db, 'presence'), store.where('classroom', '==', id)),
   (snap) => {
    const rows = [];
    snap.forEach((doc) => rows.push({id: doc.id, uid: doc.id, ...doc.data()}));
    presenceRows = rows;
    paintCounts(rows);
   },
   (error) => {
    console.error('[teacher-session]', error);
    $('presence-counts').textContent = '따라오는 중 — / 따로 보는 중 —';
   }
  );
  rosterUnsub = store.onSnapshot(store.collection(db, 'roster'), (snap) => {
   rosterRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    rosterRows.push({id: doc.id, email: data.email || doc.id, ...data});
   });
   rememberBaseline();
  }, (error) => console.error('[teacher-session]', error));
  progressUnsub = store.onSnapshot(store.collection(db, 'progress'), (snap) => {
   progressRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    if (inClass(data, id)) progressRows.push({id: doc.id, uid: data.uid || doc.id, ...data});
   });
   rememberBaseline();
   if (togetherQuestionId) refreshTogether(false);
  }, (error) => console.error('[teacher-session]', error));
  helpUnsub = store.onSnapshot(
   store.query(store.collection(db, 'helpRequests'), store.where('classId', '==', id)),
   (snap) => {
    helpRows = [];
    snap.forEach((doc) => helpRows.push({id: doc.id, ...doc.data()}));
   },
   (error) => console.error('[teacher-session]', error)
  );
  store.getDocs(store.collection(db, 'assignments')).then((snap) => {
   assignments = [];
   snap.forEach((doc) => assignments.push({id: doc.id, ...doc.data()}));
  }).catch((error) => console.error('[teacher-session]', error));
 }).catch((error) => {
  console.error('[teacher-session]', error);
  note('세션 기능을 불러오지 못했습니다.');
 });
}

function isDemo() {
 return new URLSearchParams(location.search).get('demo') === '1';
}

function onClass(detail) {
 if (isDemo()) return;
 classIdValue = (detail && detail.classId) || '';
 listen(classIdValue);
}

function onAccount(detail) {
 if (isDemo()) return;
 const user = detail && detail.user;
 teacherEmail = (user && user.email) ? user.email.toLowerCase() : '';
 paintStatus();
 if (classIdValue) listen(classIdValue);
}

function renderSessionDemo() {
 const question = choiceQuestions(catalog)[0];
 if (question) {
  togetherQuestionId = question.id;
  paintTogetherPicker();
  paintTogetherBars(question, [question.options[0], question.options[0], question.answer, question.options[1] || question.options[0], '']);
 }
 const roster = [
  {email: '20301@e-mirim.hs.kr', name: '김가', studentId: '20301', grade: 2, classroom: 3},
  {email: '20302@e-mirim.hs.kr', name: '이나', studentId: '20302', grade: 2, classroom: 3},
  {email: '20303@e-mirim.hs.kr', name: '박다', studentId: '20303', grade: 2, classroom: 3}
 ];
 const progress = [
  {email: '20301@e-mirim.hs.kr', grade: 2, classroom: 3, counts: {done: ['u1-overview']}, understanding: {'u1-overview': 'hard'}},
  {email: '20302@e-mirim.hs.kr', grade: 2, classroom: 3, counts: {done: ['u1-overview', 'u1-define']}, understanding: {'u1-define': 'hard'}}
 ];
 paintReport(buildLessonReport({
  classId: '2-3',
  session: {
   startedAt: Date.now() - 40 * 60 * 1000,
   focus: {page: 'units/unit01/index.html', topicAnchor: 'overview'},
   baseline: {rate: 0.4}
  },
  roster,
  progress,
  help: [{status: 'open', name: '박다', studentId: '20303', topic: 'u1-define', createdAt: Date.now()}],
  presence: [{topicAnchor: 'define', page: 'units/unit01/index.html'}],
  trail: [{topicAnchor: 'overview', page: 'units/unit01/index.html'}],
  titles,
  topicTotal: 2,
  assignment: {title: '모듈 과제'},
  submissions: [{email: '20301@e-mirim.hs.kr'}, {email: '20302@e-mirim.hs.kr'}]
 }));
}

if (typeof window !== 'undefined') window.aipySessionDemo = renderSessionDemo;

async function startTeacherSession() {
 if (!$('session-start')) return;
 try {
  catalog = await (await fetch(`${prefix}data/catalog.json`)).json();
  titles = titlesFromCatalog(catalog);
  topics = topicListFromCatalog(catalog);
 } catch (error) {
  console.error('[teacher-session]', error);
  note('단원 목록을 읽지 못했습니다. 생성기를 다시 실행하세요.');
 }
 if (!ready) $('session-status').textContent = '로그인 설정이 없어 세션을 시작할 수 없습니다.';
 paintFocusFromSession(null);
 paintTogetherPicker();
 paintTogetherBars(null, []);
 paintReport(null);
 $('focus-page').onchange = () => {
  $('focus-page').dataset.dirty = '1';
  refillTopics('');
 };
 $('focus-topic').onchange = () => {
  $('focus-page').dataset.dirty = '1';
  refillExamples('');
 };
 $('focus-example').onchange = () => { $('focus-page').dataset.dirty = '1'; };
 $('session-start').onclick = startSession;
 $('session-end').onclick = endSession;
 $('focus-send').onclick = sendFocus;
 $('attention-send').onclick = sendAttention;
 if ($('together-unit')) $('together-unit').onchange = paintTogetherPicker;
 if ($('together-question')) {
  $('together-question').onchange = () => {
   togetherQuestionId = $('together-question').value;
   paintStatus();
   refreshTogether(false);
  };
 }
 if ($('together-send')) $('together-send').onclick = sendTogether;
 if ($('together-refresh')) $('together-refresh').onclick = () => refreshTogether(true);
 if ($('report-refresh')) $('report-refresh').onclick = refreshReport;
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
 if (window.aipyAccount) onAccount(window.aipyAccount);
 paintStatus();
 if (new URLSearchParams(location.search).get('demo') === '1') renderSessionDemo();
}

startTeacherSession();
