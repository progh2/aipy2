/* 교사 현황 보드의 이해도·도움 요청 최소 실시간 보기. 선택한 반만 집계합니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {inClass} from './class-picker.js';
import {
 titlesFromCatalog, topicTitle, studentLabel, countUnderstanding, groupHardByTopic
} from './understanding-model.js';
import {sortOpenHelp} from './help-model.js';

const $ = (id) => document.getElementById(id);
const prefix = document.body.dataset.prefix || '';
const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let classIdValue = '';
let titles = {};
let progressUnsub = null;
let helpUnsub = null;
let progressRows = [];
let helpRows = [];

function note(id, text) {
 const el = $(id);
 if (el) el.textContent = text || '';
}

function paintUnderstanding() {
 const {counts, hardRows} = countUnderstanding(progressRows);
 const countsEl = $('understanding-counts');
 if (countsEl) {
  countsEl.textContent = `어려워요 ${counts.hard} · 조금 어려워요 ${counts.somewhat} · 이해했어요 ${counts.understood}`;
 }
 const list = $('understanding-list');
 if (!list) return;
 const groups = groupHardByTopic(hardRows);
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!groups.length) {
  list.replaceChildren(node('p', 'small', '이 반에서 어려워요를 누른 학생이 없습니다.'));
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const [topicId, rows] of groups) {
  const card = node('article', 'admin-row understanding-topic-row');
  const head = node('div');
  head.append(
   node('strong', '', topicTitle(topicId, titles)),
   node('span', 'small', `어려워요 ${rows.length}명`)
  );
  const people = node('p', 'small', rows.map((row) => studentLabel(row)).join(' · '));
  card.append(head, people);
  wrap.append(card);
 }
 list.replaceChildren(wrap);
}

function formatWhen(value) {
 if (!value) return '';
 try {
  if (typeof value.toDate === 'function') return value.toDate().toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
  if (typeof value === 'number') return new Date(value).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'});
 } catch { /* 시각 없음 */ }
 return '';
}

function paintHelp() {
 const open = sortOpenHelp(helpRows);
 const countsEl = $('help-counts');
 if (countsEl) countsEl.textContent = `대기 ${open.length}`;
 const list = $('help-list');
 if (!list) return;
 if (!classIdValue) {
  list.replaceChildren(node('p', 'small', '위에서 수업할 반을 선택하세요.'));
  return;
 }
 if (!open.length) {
  list.replaceChildren(node('p', 'small', '열린 도움 요청이 없습니다.'));
  return;
 }
 const wrap = node('div', 'admin-rows');
 for (const row of open) {
  const card = node('article', 'admin-row help-row');
  const who = node('div');
  who.append(
   node('strong', '', studentLabel(row)),
   node('span', 'small', [formatWhen(row.createdAt), topicTitle(row.topic, titles), row.example || ''].filter(Boolean).join(' · '))
  );
  const detail = node('p', 'small', row.lastError || '오류 메시지 없음');
  const resolve = node('button', '', '해결');
  resolve.type = 'button';
  resolve.dataset.helpId = row.id;
  resolve.addEventListener('click', () => resolveHelp(row.id));
  card.append(who, detail, resolve);
  wrap.append(card);
 }
 list.replaceChildren(wrap);
}

async function resolveHelp(id) {
 if (!id) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'helpRequests', id), {
   status: 'resolved',
   updatedAt: store.serverTimestamp()
  });
 } catch (error) {
  console.error('[teacher-board]', error);
  note('help-note', `해결로 표시하지 못했습니다. (${error.code || error})`);
 }
}

function stop() {
 if (progressUnsub) {
  progressUnsub();
  progressUnsub = null;
 }
 if (helpUnsub) {
  helpUnsub();
  helpUnsub = null;
 }
 progressRows = [];
 helpRows = [];
 paintUnderstanding();
 paintHelp();
}

function listen(id) {
 stop();
 classIdValue = id || '';
 if (!id || !ready) {
  paintUnderstanding();
  paintHelp();
  return;
 }
 load().then(({db, store}) => {
  progressUnsub = store.onSnapshot(store.collection(db, 'progress'), (snap) => {
   progressRows = [];
   snap.forEach((doc) => {
    const data = doc.data();
    if (inClass(data, id)) progressRows.push({id: doc.id, ...data});
   });
   paintUnderstanding();
  }, (error) => {
   console.error('[teacher-board]', error);
   note('understanding-note', '이해도 요약을 읽지 못했습니다.');
  });
  helpUnsub = store.onSnapshot(
   store.query(store.collection(db, 'helpRequests'), store.where('classId', '==', id)),
   (snap) => {
    helpRows = [];
    snap.forEach((doc) => helpRows.push({id: doc.id, ...doc.data()}));
    paintHelp();
   },
   (error) => {
    console.error('[teacher-board]', error);
    note('help-note', '도움 요청을 읽지 못했습니다.');
   }
  );
 }).catch((error) => {
  console.error('[teacher-board]', error);
 });
}

function onClass(detail) {
 listen((detail && detail.classId) || '');
}

async function startTeacherBoard() {
 if (!$('understanding-board')) return;
 if (!ready) {
  note('understanding-note', '로그인 설정이 없어 현황을 불러올 수 없습니다.');
  return;
 }
 try {
  titles = titlesFromCatalog(await (await fetch(`${prefix}data/catalog.json`)).json());
 } catch (error) {
  console.warn('[teacher-board] catalog', error);
 }
 document.addEventListener('aipy:class', (event) => onClass(event.detail));
 if (window.aipyClass) onClass(window.aipyClass);
 paintUnderstanding();
 paintHelp();
}

startTeacherBoard();
