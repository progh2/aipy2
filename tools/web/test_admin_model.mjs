/* 명단 관리(admin.js) 순수 로직 검사. node tools/web/test_admin_model.mjs
   admin.js는 모듈 최상단에서 DOM을 만지므로(#125-6) node에서 import할 수 없다.
   여기서는 분리한 admin-model.js만 검사한다. */
import {
 FIELDS, parseCsv, columnOrder, deriveFromStudentId, readRow, rosterPayload, legacyIdRows, SCHOOL
} from '../../web/assets/admin-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

// --- 학번 범위(#123): 자릿수는 맞아도 범위를 벗어나면 학번이 아니다 ---
eq(deriveFromStudentId('0314'), null, '4자리지만 학년 0 → 거부');
eq(deriveFromStudentId('2314'), {grade: 2, classroom: 3, number: 14}, '4자리 정상 학번 허용');
eq(deriveFromStudentId('40314'), null, '학년 4 → 거부');
eq(deriveFromStudentId('20014'), null, '반 0 → 거부');
eq(deriveFromStudentId('20300'), null, '번호 0 → 거부');
eq(deriveFromStudentId('23140'), {grade: 2, classroom: 31, number: 40}, '5자리는 반이 2자리로 분해된다');
eq(deriveFromStudentId('abcd'), null, '숫자가 아니면 거부');
eq(deriveFromStudentId(''), null, '빈 값 거부');

// --- CSV 직접 입력값과 학번 불일치 오류 ---
{
 const {order} = columnOrder(['email', 'studentId', 'admissionYear', 'name', 'grade', 'classroom', 'number']);
 const {entry, problems} = readRow(['s2314@e-mirim.hs.kr', '2314', '2025', '홍길동', '3', '3', '14'], order);
 eq(entry.grade, 3, '입력한 grade 값을 그대로 담는다(검증은 problems로)');
 eq(problems.some((p) => p.includes('grade가 학번')), true, 'grade가 학번과 다르면 오류');
}
{
 const {order} = columnOrder(['email', 'studentId', 'admissionYear', 'name', 'grade', 'classroom', 'number']);
 const {entry, problems} = readRow(['s2314@e-mirim.hs.kr', '2314', '2025', '홍길동', '', '', ''], order);
 eq(entry.grade, 2, 'grade·classroom·number를 안 적으면 학번에서 유도');
 eq(entry.classroom, 3, '학번에서 유도한 classroom');
 eq(entry.number, 14, '학번에서 유도한 number');
 eq(problems, [], '학번과 일치하면 오류 없음');
}

// --- BOM·CRLF·대문자 이메일 ---
{
 const csv = '﻿email,studentId,admissionYear,name,grade,classroom,number\r\nS2314@E-MIRIM.HS.KR,2314,2025,홍길동,,,\r\n';
 const rows = parseCsv(csv);
 eq(rows.length, 2, 'BOM·CRLF가 있어도 데이터 줄 2개(머리글+본문)로 파싱');
 eq(rows[0][0], 'email', 'BOM이 첫 헤더 셀에서 제거됨');
 const {order, skipHead} = columnOrder(rows[0]);
 eq(skipHead, true, '머리글 인식');
 const {entry, problems} = readRow(rows[1], order);
 eq(entry.email, 's2314@e-mirim.hs.kr', '대문자 이메일을 소문자로 정규화');
 eq(problems, [], '학교 도메인과 일치하면 오류 없음(도메인 비교도 소문자로)');
}
{
 // 헤더 없이(순서만) 준 CSV
 const {order, skipHead} = columnOrder(['s2315@e-mirim.hs.kr', '2315', '2025', '김서연', '', '', '']);
 eq(skipHead, false, '머리글 없는 CSV는 FIELDS 기본 순서를 쓴다');
 eq(order, FIELDS.map((f) => f.key), '기본 열 순서');
}

// --- 다른 학교 도메인 이메일 거부 ---
{
 const {order} = columnOrder(['email', 'studentId', 'admissionYear', 'name', 'grade', 'classroom', 'number']);
 const {problems} = readRow(['s2314@gmail.com', '2314', '2025', '홍길동', '', '', ''], order);
 eq(problems.some((p) => p.includes(`@${SCHOOL}`)), true, '학교 이메일이 아니면 오류');
}

// --- 반영 payload: archived·archivedAt 보존 ---
{
 const entry = {email: 'a@e-mirim.hs.kr', studentId: '2314', admissionYear: 2025, name: '홍길동', grade: 2, classroom: 3, number: 14};
 eq(rosterPayload(entry, null), {
  email: 'a@e-mirim.hs.kr', studentId: '2314', admissionYear: 2025, name: '홍길동',
  grade: 2, classroom: 3, number: 14
 }, '기존 문서가 없으면 archived 없이 그대로');
 const before = {archived: true, archivedAt: 'TS'};
 eq(rosterPayload(entry, before), {
  email: 'a@e-mirim.hs.kr', studentId: '2314', admissionYear: 2025, name: '홍길동',
  grade: 2, classroom: 3, number: 14, archived: true, archivedAt: 'TS'
 }, '보관 학생은 archived·archivedAt을 이어간다');
 eq(rosterPayload(entry, {archived: false}), {
  email: 'a@e-mirim.hs.kr', studentId: '2314', admissionYear: 2025, name: '홍길동',
  grade: 2, classroom: 3, number: 14
 }, 'archived가 false면 payload에 안 넣는다');
 const noNumber = {...entry, number: null};
 eq(rosterPayload(noNumber, null).number, undefined, 'number가 없으면 payload에서 뺀다');
}

// --- 5자리(옛 형식) 정리 대상 선별 ---
{
 const rows = [
  {id: 'a@e-mirim.hs.kr', studentId: '2314', name: '정상'},
  {id: 'b@e-mirim.hs.kr', studentId: '23140', name: '옛5자리'},
  {id: 'c@e-mirim.hs.kr', studentId: 'abcd', name: '비숫자'},
  {id: 'd@e-mirim.hs.kr', studentId: '', name: '학번없음'}
 ];
 eq(legacyIdRows(rows).map((r) => r.name), ['옛5자리', '비숫자', '학번없음'], '4자리가 아닌 학번만 정리 대상');
 eq(legacyIdRows([]), [], '빈 명단은 정리 대상 없음');
}

console.log('PASS: admin-model helpers');
