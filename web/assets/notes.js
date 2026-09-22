/* 포스트잇 메모(#99). 로그인한 학생·교사가 페이지 오른쪽에 메모를 붙입니다.
   위치(y)는 문서 기준 px, 공개 범위는 비공개(기본)/학생에게 공개/모두 공개.
   저장은 Firestore notes 컬렉션(규칙이 공개 범위별 읽기를 제한). 실패해도 학습을 막지 않습니다. */
import {ready} from './firebase-config.js';
import {load, readTeacherFlag} from './auth.js';
import {pageFromPath} from './follow-model.js';
import {
 NOTE_COLORS, NOTE_VISIBILITY, NOTE_VISIBILITY_LABELS, NOTE_TEXT_MAX, NOTE_WRITE_MS,
 randomColor, linkify, extractLinks, noteFields, normalizeNote, classIdOf, sortNotes, authorLabel
} from './notes-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};
const zoom = () => parseFloat(document.body.style.zoom) || 1;
const page = pageFromPath(location.pathname);

// 문서 좌표(레이아웃 px). body zoom이 걸려 있어도 일관되게 쓴다.
function layoutRect(el) {
 const r = el.getBoundingClientRect();
 const z = zoom();
 return {top: (r.top + window.scrollY) / z, height: r.height / z};
}
// 메모를 붙일 앵커: 본문 안 id가 있는 큰 요소 중 y 바로 위에서 시작하는 것
function anchorFor(y) {
 let best = null, bestTop = -1;
 for (const el of document.querySelectorAll('main [id]')) {
  if (!el.id || /^(toast|account|notes-layer)$/.test(el.id)) continue;
  const {top, height} = layoutRect(el);
  if (height < 40) continue;
  if (top <= y && top > bestTop) { best = el; bestTop = top; }
 }
 return best;
}
function placeFromY(note, y) {
 note.y = Math.max(0, y);
 const el = anchorFor(note.y);
 if (el) {
  const {top, height} = layoutRect(el);
  note.anchor = el.id;
  note.offset = height > 0 ? Math.max(0, (note.y - top) / height) : 0;
 } else {
  note.anchor = '';
  note.offset = 0;
 }
}
function topFor(note) {
 if (note.anchor) {
  const el = document.getElementById(note.anchor);
  if (el) {
   const {top, height} = layoutRect(el);
   return top + Math.min(10, note.offset || 0) * height;
  }
 }
 return note.y;
}
function reposition() {
 if (!layer) return;
 for (const card of layer.querySelectorAll('.note-card')) {
  if (card.classList.contains('dragging')) continue;
  const note = allNotes().find((n) => n.id === card.dataset.id);
  if (note) card.style.top = `${topFor(note)}px`;
 }
 sizeLayer();
}

let user = null, profile = null, teacher = false, classId = '';
let db = null, fs = null;
let unsubs = [];
const buckets = {own: new Map(), all: new Map(), cls: new Map()};
const timers = new Map();
let layer = null, addBtn = null;

function toast(text) {
 const box = document.getElementById('toast');
 if (!box) return;
 box.textContent = text || '';
 setTimeout(() => { if (box.textContent === text) box.textContent = ''; }, 4000);
}

function allNotes() {
 const map = new Map();
 for (const bucket of Object.values(buckets)) for (const [id, n] of bucket) map.set(id, n);
 return sortNotes([...map.values()]);
}

function ensureLayer() {
 if (layer) return layer;
 layer = node('div', 'notes-layer');
 layer.id = 'notes-layer';
 document.body.append(layer);
 addBtn = node('button', 'notes-add', '🗒 메모');
 addBtn.type = 'button';
 addBtn.title = '지금 보는 위치 옆에 포스트잇을 붙입니다';
 addBtn.hidden = true;
 addBtn.addEventListener('click', createNote);
 document.body.append(addBtn);
 window.addEventListener('resize', reposition);
 // 본문 높이가 바뀌면(문항 렌더·이미지 로드·글자 크기) 앵커 기준으로 다시 놓는다.
 if (window.ResizeObserver) new ResizeObserver(() => reposition()).observe(document.body);
 return layer;
}

function sizeLayer() {
 if (!layer) return;
 layer.style.height = `${document.documentElement.scrollHeight}px`;
}

async function createNote() {
 if (!user || !profile) { toast('학교 계정으로 로그인하면 메모를 붙일 수 있어요.'); return; }
 const draft = {};
 placeFromY(draft, (window.scrollY + window.innerHeight * 0.35) / zoom());
 const fields = noteFields({profile: {...profile, uid: user.uid}, page, y: draft.y, anchor: draft.anchor, offset: draft.offset, color: randomColor(), visibility: 'private', text: ''});
 try {
  const ref = await fs.addDoc(fs.collection(db, 'notes'), {...fields, createdAt: fs.serverTimestamp(), updatedAt: fs.serverTimestamp()});
  // 구독 반영 전에 바로 편집할 수 있게 낙관적으로 그린다.
  buckets.own.set(ref.id, normalizeNote(ref.id, fields));
  render(ref.id);
 } catch (error) {
  console.warn('[notes]', error);
  toast('메모를 만들지 못했습니다. 규칙 게시·네트워크를 확인하세요.');
 }
}

function scheduleSave(note, patch) {
 Object.assign(note, patch);
 clearTimeout(timers.get(note.id));
 timers.set(note.id, setTimeout(() => saveNote(note), NOTE_WRITE_MS));
}

async function saveNote(note) {
 if (!user || !profile) return;
 try {
  const fields = noteFields({profile: {...profile, uid: user.uid}, page: note.page || page, y: note.y, anchor: note.anchor, offset: note.offset, color: note.color, visibility: note.visibility, text: note.text});
  await fs.setDoc(fs.doc(db, 'notes', note.id), {...fields, updatedAt: fs.serverTimestamp()}, {merge: true});
 } catch (error) {
  console.warn('[notes]', error);
  toast('메모를 저장하지 못했습니다.');
 }
}

async function removeNote(note) {
 if (!confirm('이 메모를 지울까요?')) return;
 try {
  await fs.deleteDoc(fs.doc(db, 'notes', note.id));
  for (const bucket of Object.values(buckets)) bucket.delete(note.id);
  render();
 } catch (error) {
  console.warn('[notes]', error);
  toast('메모를 지우지 못했습니다.');
 }
}

function colorPicker(note, onPick) {
 const pop = node('div', 'note-colors');
 for (const c of NOTE_COLORS) {
  const b = node('button', 'note-swatch', ' ');
  b.type = 'button';
  b.style.background = c;
  b.title = c;
  b.setAttribute('aria-pressed', String(c === note.color));
  b.addEventListener('click', () => { onPick(c); pop.remove(); });
  pop.append(b);
 }
 return pop;
}

function bindDrag(handle, card, note) {
 let startY = 0, startTop = 0, currentTop = 0, dragging = false;
 handle.addEventListener('pointerdown', (e) => {
  if (e.button !== 0) return;
  dragging = true; startY = e.clientY; startTop = topFor(note); currentTop = startTop;
  handle.setPointerCapture(e.pointerId); card.classList.add('dragging'); e.preventDefault();
 });
 handle.addEventListener('pointermove', (e) => {
  if (!dragging) return;
  currentTop = Math.max(0, startTop + (e.clientY - startY) / zoom());
  card.style.top = `${currentTop}px`;
 });
 const end = () => { if (!dragging) return; dragging = false; card.classList.remove('dragging'); placeFromY(note, currentTop); scheduleSave(note, {}); };
 handle.addEventListener('pointerup', end);
 handle.addEventListener('pointercancel', end);
}

function noteCard(note) {
 const own = user && note.uid === user.uid;
 const card = node('article', 'note-card');
 card.dataset.id = note.id;
 card.style.background = note.color;
 card.style.top = `${topFor(note)}px`;
 const head = node('div', 'note-head');
 const handle = node('span', 'note-handle', '⋮⋮');
 handle.title = '끌어서 위아래로 옮기기';
 const who = node('span', 'note-who', own ? '내 메모' : authorLabel(note));
 head.append(handle, who);
 if (own) {
  const sel = node('select', 'note-vis');
  sel.title = '공개 범위';
  for (const v of NOTE_VISIBILITY) {
   const opt = node('option', '', NOTE_VISIBILITY_LABELS[v]);
   opt.value = v; opt.selected = v === note.visibility; sel.append(opt);
  }
  sel.addEventListener('change', () => scheduleSave(note, {visibility: sel.value}));
  const colorBtn = node('button', 'note-color-btn', '🎨');
  colorBtn.type = 'button'; colorBtn.title = '배경색';
  colorBtn.addEventListener('click', () => {
   const old = card.querySelector('.note-colors');
   if (old) { old.remove(); return; }
   card.append(colorPicker(note, (c) => { card.style.background = c; scheduleSave(note, {color: c}); }));
  });
  const del = node('button', 'note-del', '✕');
  del.type = 'button'; del.title = '메모 지우기';
  del.addEventListener('click', () => removeNote(note));
  head.append(sel, colorBtn, del);
  bindDrag(handle, card, note);
 } else {
  head.append(node('span', 'note-badge', NOTE_VISIBILITY_LABELS[note.visibility] || ''));
  if (teacher) {
   const del = node('button', 'note-del', '✕');
   del.type = 'button'; del.title = '교사 권한으로 지우기';
   del.addEventListener('click', () => removeNote(note));
   head.append(del);
  }
 }
 card.append(head);
 if (own) {
  const ta = node('textarea', 'note-text');
  ta.value = note.text; ta.maxLength = NOTE_TEXT_MAX; ta.rows = 4; ta.placeholder = '메모를 적어요. 링크를 넣으면 아래에 열기 버튼이 생겨요.';
  const links = node('div', 'note-links');
  const paintLinks = () => {
   links.replaceChildren();
   for (const url of extractLinks(ta.value)) {
    const a = node('a', '', url.replace(/^https?:\/\//, '').slice(0, 40));
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; links.append(a);
   }
  };
  ta.addEventListener('input', () => { scheduleSave(note, {text: ta.value}); paintLinks(); });
  card.append(ta, links);
  paintLinks();
 } else {
  const body = node('div', 'note-body');
  body.innerHTML = linkify(note.text);
  card.append(body);
 }
 return card;
}

function render(focusId) {
 ensureLayer();
 sizeLayer();
 const notes = allNotes().filter((n) => n.page === page);
 const editing = document.activeElement && document.activeElement.closest && document.activeElement.closest('.note-card');
 const editingId = editing ? editing.dataset.id : '';
 const keep = editingId ? layer.querySelector(`.note-card[data-id="${editingId}"]`) : null;
 layer.replaceChildren();
 for (const note of notes) {
  if (note.id === editingId && keep) { layer.append(keep); continue; }
  layer.append(noteCard(note));
 }
 if (focusId) {
  const ta = layer.querySelector(`.note-card[data-id="${focusId}"] textarea`);
  if (ta) ta.focus();
 }
}

function stop() {
 for (const u of unsubs) { try { u(); } catch { /* 무시 */ } }
 unsubs = [];
 for (const b of Object.values(buckets)) b.clear();
 if (addBtn) addBtn.hidden = true;
 render();
}

function subscribe(key, q) {
 unsubs.push(fs.onSnapshot(q, (snap) => {
  buckets[key].clear();
  snap.forEach((d) => buckets[key].set(d.id, normalizeNote(d.id, d.data())));
  render();
 }, (error) => {
  console.warn('[notes]', key, error);
 }));
}

function start() {
 stop();
 if (!user || !profile || !db) return;
 addBtn.hidden = false;
 const col = fs.collection(db, 'notes');
 subscribe('own', fs.query(col, fs.where('uid', '==', user.uid), fs.where('page', '==', page)));
 subscribe('all', fs.query(col, fs.where('visibility', '==', 'all'), fs.where('page', '==', page)));
 const cls = teacher ? (window.aipyClass || '') : classId;
 if (cls) subscribe('cls', fs.query(col, fs.where('visibility', '==', 'students'), fs.where('classId', '==', cls), fs.where('page', '==', page)));
}

async function onAccount(detail) {
 user = detail && detail.user;
 profile = detail && detail.profile;
 if (!user || !profile) { user = null; profile = null; teacher = false; classId = ''; stop(); return; }
 classId = classIdOf(profile);
 try {
  const loaded = await load();
  db = loaded.db; fs = loaded.store;
  teacher = (await readTeacherFlag((user.email || '').toLowerCase())).teacher;
 } catch (error) {
  console.warn('[notes]', error);
  return;
 }
 start();
}

function boot() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 if (!ready) return;
 ensureLayer();
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 document.addEventListener('aipy:class', () => { if (teacher) start(); });
 if (window.aipyAccount) onAccount(window.aipyAccount);
}

boot();
