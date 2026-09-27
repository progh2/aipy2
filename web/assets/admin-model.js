/* 명단 관리(admin.js)용 순수 로직. DOM·Firebase 없이 CSV 파싱·학번 검증·반영 payload를
   검사할 수 있게 admin.js에서 분리했다(#125-6). admin.js는 이 파일을 import해서 쓴다. */
import {SCHOOL_DOMAIN} from './firebase-config.js';

export const SCHOOL = SCHOOL_DOMAIN;

export const FIELDS = [
 {key: 'email', labels: ['email', '이메일', '메일'], type: 'text'},
 {key: 'studentId', labels: ['studentid', 'student_id', '학번'], type: 'text'},
 {key: 'admissionYear', labels: ['admissionyear', 'admission_year', '입학년도', '입학연도'], type: 'int'},
 {key: 'name', labels: ['name', '이름', '성명'], type: 'text'},
 {key: 'grade', labels: ['grade', '학년'], type: 'int', optional: true},
 {key: 'classroom', labels: ['classroom', 'class', '반'], type: 'int', optional: true},
 {key: 'number', labels: ['number', '번호', '출석번호'], type: 'int', optional: true}
];

export function parseCsv(text) {
 const rows = [];
 let row = [], field = '', quoted = false;
 text = text.replace(/^﻿/, '');
 for (let i = 0; i < text.length; i++) {
  const c = text[i];
  if (quoted) {
   if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
   else if (c === '"') quoted = false;
   else field += c;
  } else if (c === '"') quoted = true;
  else if (c === ',' || c === '\t') { row.push(field); field = ''; }
  else if (c === '\n') { row.push(field); field = ''; rows.push(row); row = []; }
  else if (c !== '\r') field += c;
 }
 if (field !== '' || row.length) { row.push(field); rows.push(row); }
 return rows.filter((r) => r.some((v) => v.trim() !== ''));
}

// 머리글이 있으면 이름으로, 없으면 정해진 순서로 열을 맞춥니다. 한글 머리글도 받습니다.
export function columnOrder(head) {
 const cells = head.map((c) => c.trim().toLowerCase());
 const isHeader = cells.some((c) => FIELDS.some((f) => f.labels.includes(c)));
 if (!isHeader) return {order: FIELDS.map((f) => f.key), skipHead: false};
 const order = cells.map((c) => {
  const field = FIELDS.find((f) => f.labels.includes(c));
  return field ? field.key : null;
 });
 return {order, skipHead: true};
}

// 학번 규칙: 4자리 = 학년(1)·반(1)·번호(2), 5자리 = 학년(1)·반(2)·번호(2). 예: 2314 → 2학년 3반 14번.
// 학년이 바뀌면 학번이 새로 부여되므로 코호트 구분은 입학년도로 한다.
// 범위를 벗어난 값(학년 0/4 이상, 반 0, 번호 0 등)은 자릿수는 맞아도 학번이 아니다(#123) — null로
// 돌려 readRow가 오류로 표시하게 한다.
function validParts(grade, classroom, number) {
 if (!(grade >= 1 && grade <= 3)) return null;
 if (!(classroom >= 1)) return null;
 if (!(number >= 1)) return null;
 return {grade, classroom, number};
}
export function deriveFromStudentId(studentId) {
 const id = String(studentId || '');
 if (/^\d{4}$/.test(id)) return validParts(+id[0], +id[1], +id.slice(2));
 if (/^\d{5}$/.test(id)) return validParts(+id[0], +id.slice(1, 3), +id.slice(3));
 return null;
}

export function readRow(cells, order, schoolDomain = SCHOOL) {
 const raw = {};
 order.forEach((key, i) => { if (key) raw[key] = (cells[i] || '').trim(); });
 const problems = [];
 const entry = {};
 for (const field of FIELDS) {
  const value = raw[field.key] || '';
  if (!value) {
   if (field.optional) { entry[field.key] = null; continue; }
   problems.push(`${field.key} 없음`);
   continue;
  }
  if (field.type === 'int') {
   const parsed = Number(value);
   if (!Number.isInteger(parsed)) { problems.push(`${field.key}는 정수여야 함`); continue; }
   entry[field.key] = parsed;
  } else {
   entry[field.key] = value;
  }
 }
 // 학년·반·번호가 비면 학번에서 유도한다. CSV에 직접 적은 값이 학번에서 유도한 값과 다르면
 // 오타·전입 전 학번 재사용 등 데이터 불일치이므로 오류로 본다(#123).
 const derived = deriveFromStudentId(entry.studentId);
 for (const key of ['grade', 'classroom', 'number']) {
  if (entry[key] == null) { if (derived) entry[key] = derived[key]; }
  else if (derived && entry[key] !== derived[key]) {
   problems.push(`${key}가 학번(${entry.studentId})과 다름: 입력값 ${entry[key]} ≠ 학번 기준 ${derived[key]}`);
  }
 }
 if (entry.studentId && !derived) problems.push('학번이 4~5자리 숫자 형식(학년·반·번호)이 아님');
 if (entry.grade == null) problems.push('grade 없음(학번이 4~5자리 숫자가 아니면 직접 입력)');
 if (entry.classroom == null) problems.push('classroom 없음(학번이 4~5자리 숫자가 아니면 직접 입력)');
 if (entry.email) {
  entry.email = entry.email.toLowerCase();
  if (!entry.email.endsWith(`@${schoolDomain}`)) problems.push(`학교 이메일(@${schoolDomain})이 아님`);
 }
 return {entry, problems};
}

// apply()가 Firestore에 쓸 payload. archived·archivedAt은 CSV에 없는 필드라서 기존 문서 값을
// 그대로 이어가야 한다(#123) — 안 하면 CSV 반영 때마다 보관 학생이 되살아난다.
// updatedAt(서버 타임스탬프)은 Firebase가 있어야 만들 수 있으므로 호출부(admin.js)에서 붙인다.
export function rosterPayload(entry, before) {
 const payload = {
  email: entry.email,
  studentId: entry.studentId,
  admissionYear: entry.admissionYear,
  name: entry.name,
  grade: entry.grade,
  classroom: entry.classroom
 };
 if (entry.number != null) payload.number = entry.number;
 if (before && before.archived === true) {
  payload.archived = true;
  if (before.archivedAt) payload.archivedAt = before.archivedAt;
 }
 return payload;
}

// 학번이 4자리 숫자가 아닌 학생(옛 5자리 형식 등) 선별. 명단에서만 지우고 학습 기록은 남긴다.
export function legacyIdRows(rows) {
 return (rows || []).filter((r) => !/^\d{4}$/.test(String(r.studentId || '')));
}
