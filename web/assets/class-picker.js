/* 수업 반 식별·선택. 반은 roster의 grade + classroom이며, 이후 보드·세션의 기준 단위입니다.
   문서 ID는 `{학년}-{반}` (예: 2-3). Firestore sessions/{반}에도 그대로 씁니다. */

export const CLASS_STORAGE_PREFIX = 'aipy-teacher-class:';

export function isArchived(entry) {
 return Boolean(entry && entry.archived === true);
}

export function classId(entry) {
 if (!entry || entry.grade == null || entry.classroom == null) return '';
 const grade = Number(entry.grade), classroom = Number(entry.classroom);
 if (!Number.isInteger(grade) || !Number.isInteger(classroom)) return '';
 return `${grade}-${classroom}`;
}

export function parseClassId(id) {
 if (!id || typeof id !== 'string') return null;
 const match = /^(\d+)-(\d+)$/.exec(id.trim());
 if (!match) return null;
 return {grade: Number(match[1]), classroom: Number(match[2])};
}

export function labelClass(id) {
 const parsed = typeof id === 'object' && id ? id : parseClassId(id);
 if (!parsed) return '';
 return `${parsed.grade}학년 ${parsed.classroom}반`;
}

export function inClass(entry, id) {
 return Boolean(id) && classId(entry) === id;
}

export function classesFromRoster(rows) {
 const map = new Map();
 for (const row of rows || []) {
  if (isArchived(row)) continue;
  const id = classId(row);
  if (!id) continue;
  const prev = map.get(id);
  map.set(id, {
   id,
   grade: Number(row.grade),
   classroom: Number(row.classroom),
   count: (prev ? prev.count : 0) + 1
  });
 }
 return [...map.values()].sort((a, b) => a.grade - b.grade || a.classroom - b.classroom);
}

export function storageKey(email) {
 return CLASS_STORAGE_PREFIX + String(email || '').toLowerCase();
}

export function readSelectedClass(email) {
 if (!email) return '';
 try {
  return (globalThis.localStorage && localStorage.getItem(storageKey(email))) || '';
 } catch {
  return '';
 }
}

export function writeSelectedClass(email, id) {
 if (!email) return;
 try {
  if (!globalThis.localStorage) return;
  if (!id) localStorage.removeItem(storageKey(email));
  else localStorage.setItem(storageKey(email), id);
 } catch { /* 사생활 모드 등 */ }
}

export function resolveSelectedClass(email, classes) {
 const saved = readSelectedClass(email);
 if (saved && classes.some((item) => item.id === saved)) return saved;
 return classes[0] ? classes[0].id : '';
}

// 단원 페이지에는 반 선택 UI가 없습니다. 헤더에서 고른 값(window.aipyClass)이
// 있으면 그걸 쓰고, 없으면 교사 이메일별 localStorage를 읽습니다.
export function resolveTeacherClassId(email, published) {
 const live = published && published.classId;
 if (live && parseClassId(live)) return live;
 const saved = readSelectedClass(email);
 return parseClassId(saved) ? saved : '';
}

export function classDetail(id) {
 const parsed = parseClassId(id);
 if (!parsed) return {classId: '', grade: null, classroom: null, label: ''};
 return {classId: id, grade: parsed.grade, classroom: parsed.classroom, label: labelClass(id)};
}

export function paintClassContext(detail) {
 const label = (detail && detail.label) || '반 미선택';
 const id = (detail && detail.classId) || '';
 document.querySelectorAll('[data-class-label]').forEach((el) => { el.textContent = label; });
 // body에도 data-class-id를 두므로, 표시용 노드만 고친다. body.textContent를 바꾸면 페이지가 비워진다.
 document.querySelectorAll('[data-class-id]').forEach((el) => {
  if (el === document.body) return;
  el.textContent = id;
 });
 if (document.body) document.body.dataset.classId = id;
}

export function publishClass(id) {
 const detail = classDetail(id);
 if (typeof window !== 'undefined') window.aipyClass = detail;
 if (typeof document !== 'undefined') {
  paintClassContext(detail);
  document.dispatchEvent(new CustomEvent('aipy:class', {detail}));
 }
 return detail;
}

function node(tag, cls, text) {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
}

export function mountClassPicker(host, options = {}) {
 if (!host) return null;
 const {classes = [], selected = '', disabled = false, emptyText = '선택할 반이 없습니다', onChange} = options;
 host.classList.add('class-picker');
 let select = host.querySelector('#class-picker-select');
 if (!select) {
  const label = node('label', 'class-picker-label', '지금 수업하는 반');
  label.setAttribute('for', 'class-picker-select');
  select = node('select');
  select.id = 'class-picker-select';
  select.setAttribute('aria-label', '지금 수업하는 반');
  const current = node('span', 'class-picker-current');
  current.dataset.classLabel = '';
  current.textContent = selected ? labelClass(selected) : '반 미선택';
  host.replaceChildren(label, select, current);
 }
 select.disabled = Boolean(disabled) || classes.length === 0;
 select.replaceChildren();
 if (!classes.length) {
  const opt = node('option', '', emptyText);
  opt.value = '';
  select.append(opt);
 } else {
  for (const item of classes) {
   const opt = node('option', '', `${labelClass(item.id)}${item.count != null ? ` · ${item.count}명` : ''}`);
   opt.value = item.id;
   if (item.id === selected) opt.selected = true;
   select.append(opt);
  }
 }
 select.onchange = () => { if (onChange) onChange(select.value); };
 return select;
}
