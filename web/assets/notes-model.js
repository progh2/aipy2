/* 포스트잇 메모(#99) 순수 헬퍼. Firebase 없이 색·공개 범위·링크 변환·검증을 다룹니다. */
export const NOTE_COLORS = [
 '#fff59d', '#ffe082', '#ffcc80', '#ffab91', '#f8bbd0', '#e1bee7',
 '#d1c4e9', '#bbdefb', '#b3e5fc', '#b2dfdb', '#c8e6c9', '#f0f4c3'
];
export const NOTE_VISIBILITY = ['private', 'students', 'all'];
export const NOTE_VISIBILITY_LABELS = {private: '비공개', students: '학생에게 공개', all: '모두 공개'};
export const NOTE_TEXT_MAX = 500;
export const NOTE_WRITE_MS = 600;
export const NOTE_Y_MAX = 200000;

export function randomColor(rand = Math.random) {
 return NOTE_COLORS[Math.floor(rand() * NOTE_COLORS.length) % NOTE_COLORS.length];
}

export function isNoteColor(value) {
 return NOTE_COLORS.includes(String(value || '').toLowerCase());
}

export function isVisibility(value) {
 return NOTE_VISIBILITY.includes(value);
}

export function clipNoteText(text) {
 if (text == null) return '';
 return String(text).replace(/\r\n?/g, '\n').slice(0, NOTE_TEXT_MAX);
}

export function clampY(y) {
 const n = Number(y);
 if (!Number.isFinite(n)) return 0;
 return Math.min(NOTE_Y_MAX, Math.max(0, Math.round(n)));
}

export function escapeHtml(text) {
 return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const URL_RE = /(https?:\/\/[^\s<>"']+)/g;

// 본문의 URL을 새 창 링크로 바꾼 HTML을 돌려준다. 나머지 글자는 이스케이프한다.
export function linkify(text) {
 const src = clipNoteText(text);
 let out = '';
 let last = 0;
 for (const match of src.matchAll(URL_RE)) {
  const start = match.index;
  let url = match[0];
  let trail = '';
  // 문장 끝 구두점은 링크에서 뺀다.
  const m = /[.,;:!?)\]]+$/.exec(url);
  if (m) { trail = m[0]; url = url.slice(0, -trail.length); }
  out += escapeHtml(src.slice(last, start));
  out += `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(url)}</a>${escapeHtml(trail)}`;
  last = start + match[0].length;
 }
 out += escapeHtml(src.slice(last));
 return out.replace(/\n/g, '<br>');
}

export function extractLinks(text) {
 return [...clipNoteText(text).matchAll(URL_RE)].map((m) => m[0].replace(/[.,;:!?)\]]+$/, ''));
}

export function classIdOf(profile) {
 const p = profile && typeof profile === 'object' ? profile : {};
 return p.grade != null && p.classroom != null ? `${p.grade}-${p.classroom}` : '';
}

export function noteFields({profile, page, y, color, visibility, text} = {}) {
 const person = profile && typeof profile === 'object' ? profile : {};
 return {
  uid: person.uid || '',
  email: person.email || '',
  studentId: person.studentId ?? null,
  name: typeof person.name === 'string' ? person.name : '',
  classId: classIdOf(person),
  page: String(page || '').slice(0, 200),
  y: clampY(y),
  color: isNoteColor(color) ? String(color).toLowerCase() : NOTE_COLORS[0],
  visibility: isVisibility(visibility) ? visibility : 'private',
  text: clipNoteText(text)
 };
}

export function normalizeNote(id, raw) {
 const data = raw && typeof raw === 'object' ? raw : {};
 return {
  id,
  uid: data.uid || '',
  name: typeof data.name === 'string' ? data.name : '',
  studentId: data.studentId ?? null,
  classId: typeof data.classId === 'string' ? data.classId : '',
  page: typeof data.page === 'string' ? data.page : '',
  y: clampY(data.y),
  color: isNoteColor(data.color) ? String(data.color).toLowerCase() : NOTE_COLORS[0],
  visibility: isVisibility(data.visibility) ? data.visibility : 'private',
  text: clipNoteText(data.text)
 };
}

// 화면에 보여 줄 수 있는 메모인지(규칙과 같은 기준). 교사는 전부 본다.
export function canSee(note, {uid, classId, teacher} = {}) {
 if (!note) return false;
 if (teacher) return true;
 if (uid && note.uid === uid) return true;
 if (note.visibility === 'all') return true;
 if (note.visibility === 'students' && classId && note.classId === classId) return true;
 return false;
}

export function sortNotes(notes) {
 return (notes || []).slice().sort((a, b) => (a.y - b.y) || String(a.id).localeCompare(String(b.id)));
}

export function authorLabel(note) {
 const id = note && note.studentId != null && String(note.studentId).trim() ? String(note.studentId).trim() : '';
 const name = note && typeof note.name === 'string' ? note.name.trim() : '';
 return [id, name].filter(Boolean).join(' ') || '익명';
}
