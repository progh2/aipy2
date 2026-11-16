/* 교사용 반별 입력 현황 순수 집계. DOM·Firebase 없이 node로 검사한다.
   학생 한 명의 집계는 학생용 '내 학습 기록'과 같은 buildMyRecord()를 그대로 써서
   '완료' 기준(완료 체크·푼 문제·저널)이 학생 화면과 같다. */
import {buildMyRecord} from './my-record-model.js?v=q148';
import {withBom} from './teacher-answers-model.js?v=q145a';

export const MODES = [
 {id: 'all', label: '전체'},
 {id: 'journal', label: '저널만'},
 {id: 'done', label: '완료 체크만'},
 {id: 'missing', label: '미작성만 강조'}
];
export const LEVEL_TEXT = {full: '다 함', part: '일부', none: '안 함'};

// cards: [{key, uid, label}] (이미 정렬됨), entries: Map(uid -> {status:'ready'|'empty'|'error', data?})
export function buildClassProgress(cards, entries, catalog) {
 const students = [];
 let units = [];
 for (const card of cards || []) {
  const entry = card.uid && entries ? entries.get(card.uid) : null;
  const status = !card.uid ? 'nouid' : !entry ? 'wait' : entry.status;
  const state = status === 'ready' ? entry.data || {} : {};
  const rec = buildMyRecord(state, catalog);
  if (!units.length) units = rec.units.map((u) => ({unit: u.unit, subunits: u.subunits.map((s) => ({key: s.key, anchor: s.anchor, title: s.title, short: s.short, qTotal: s.qTotal, taskTotal: s.taskTotal}))}));
  const cells = {};
  for (const u of rec.units) {
   for (const s of u.subunits) {
    const tasks = s.taskItems.filter((it) => it && String(it.text || '').trim() !== '').length;
    cells[s.key] = {
     done: s.done, qAnswered: s.qAnswered, qTotal: s.qTotal, qCorrect: s.qCorrect,
     hasJournal: s.hasJournal, journal: s.journal, tasks, taskTotal: s.taskTotal,
     rows: s.rows, taskItems: s.taskItems, otherItems: s.otherItems
    };
   }
  }
  students.push({key: card.key || card.uid || card.label, uid: card.uid || '', label: card.label || '', status, cells, overall: rec.overall});
 }
 if (!units.length) units = buildMyRecord({}, catalog).units.map((u) => ({unit: u.unit, subunits: u.subunits.map((s) => ({key: s.key, anchor: s.anchor, title: s.title, short: s.short, qTotal: s.qTotal, taskTotal: s.taskTotal}))}));
 return {units, students};
}

// 상태가 확정된 학생만(기록 없음·미접속도 포함, 조회 오류·대기는 제외) 비율 계산에 쓴다.
export function countable(student) {
 return student.status === 'ready' || student.status === 'empty' || student.status === 'nouid';
}

// 칸 하나의 3단계. mode가 journal/done이면 그 항목만 본다.
export function cellLevel(cell, mode = 'all') {
 if (!cell) return 'none';
 if (mode === 'journal') return cell.hasJournal ? 'full' : 'none';
 if (mode === 'done') return cell.done ? 'full' : 'none';
 const parts = [cell.done, cell.hasJournal];
 if (cell.qTotal > 0) parts.push(cell.qAnswered >= cell.qTotal);
 const got = parts.filter(Boolean).length;
 if (got === parts.length) return 'full';
 if (got > 0 || cell.qAnswered > 0 || cell.tasks > 0) return 'part';
 return 'none';
}

// 칸에 쓸 짧은 문구들(색 없이도 알 수 있게).
export function cellParts(cell) {
 return {
  done: cell.done ? '● 완료' : '○ 완료',
  q: cell.qTotal > 0 ? `문제 ${cell.qAnswered}/${cell.qTotal}` : '문제 -',
  journal: cell.hasJournal ? '저널 있음' : '저널 없음',
  task: cell.taskTotal > 0 ? (cell.tasks > 0 ? '직접 입력' : '직접 안 함') : ''
 };
}

export function subunitStats(model, subKey) {
 let n = 0, done = 0, journal = 0;
 for (const st of model.students) {
  if (!countable(st)) continue;
  n += 1;
  const c = st.cells[subKey];
  if (c && c.done) done += 1;
  if (c && c.hasJournal) journal += 1;
 }
 const pct = (v) => (n ? Math.round((v / n) * 100) : 0);
 return {n, done, journal, donePct: pct(done), journalPct: pct(journal)};
}

// kind: 'journal' | 'done'. 확정된 학생 중 해당 항목이 없는 학생 이름들.
export function missingStudents(model, subKey, kind = 'journal') {
 return model.students.filter((st) => countable(st) && !(st.cells[subKey] && (kind === 'done' ? st.cells[subKey].done : st.cells[subKey].hasJournal))).map((st) => st.label);
}

function csvCell(v) {
 const s = String(v == null ? '' : v);
 return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}
function csvLine(arr) { return arr.map(csvCell).join(','); }

// 선택한 단원 표 CSV(문자열, BOM 없음). 칸 = 완료/문제/저널/직접.
export function progressCsv(model, unit) {
 const u = model.units.find((x) => x.unit === unit);
 if (!u) return '';
 const head = ['학생'];
 for (const s of u.subunits) head.push(`${s.short || s.title} 완료`, `${s.short || s.title} 문제`, `${s.short || s.title} 저널`, `${s.short || s.title} 직접`);
 const lines = [csvLine(head)];
 for (const st of model.students) {
  const row = [st.label];
  for (const s of u.subunits) {
   const c = st.cells[s.key];
   row.push(c && c.done ? 'O' : 'X', c ? `${c.qAnswered}/${c.qTotal}` : '', c && c.hasJournal ? 'O' : 'X', c && c.taskTotal > 0 ? (c.tasks > 0 ? 'O' : 'X') : '-');
  }
  lines.push(csvLine(row));
 }
 return lines.join('\r\n');
}

export function missingCsv(model, subKey, kind = 'journal') {
 const lines = [csvLine(['학생', kind === 'done' ? '완료 체크 안 함' : '저널 미작성', subKey])];
 for (const name of missingStudents(model, subKey, kind)) lines.push(csvLine([name, kind === 'done' ? '완료 체크 안 함' : '저널 미작성', subKey]));
 return lines.join('\r\n');
}

export {withBom};
