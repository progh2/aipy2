/* 교사 브라우저 재검증(M7/F8.3) 순수 헬퍼. Pyodide 호출은 하지 않습니다. */
import {targetKey} from './assignment-model.js';

export const REVERIFY_NOTE = '제출 소스를 이 브라우저에서 다시 실행해 저장된 채점과 비교합니다. 브라우저 채점이에요.';
export const REVERIFY_LABEL = '브라우저 채점 다시 하기';
export const REVERIFY_CLASS_LABEL = '이 반 제출 다시 채점';
export const REVERIFY_SKIP_ESSAY = '서술형은 자동 재검증하지 않아요.';
export const REVERIFY_SKIP_MISSING = '검사에 필요한 문제·예제 데이터를 찾지 못했어요.';
export const MATCH_LABEL = '저장된 결과와 같아요';
export const MISMATCH_LABEL = '저장된 결과와 달라요';
export const SKIP_LABEL = '다시 채점하지 않음';
export const ERROR_LABEL = '다시 채점하지 못했어요';

export function normAnswer(value) {
 if (Array.isArray(value)) return JSON.stringify(value);
 return String(value ?? '').trim().replace(/[“”]/g, '"').replace(/[‘’]/g, "'").replace(/\s+/g, '').replace(/'/g, '"');
}

export function submittedSource(target) {
 const files = target && target.files && typeof target.files === 'object' ? target.files : {};
 if (typeof files['main.py'] === 'string') return files['main.py'];
 if (typeof files['answer.txt'] === 'string') return files['answer.txt'];
 const name = Object.keys(files).find((key) => typeof files[key] === 'string');
 return name ? files[name] : '';
}

export function storedOk(target) {
 return Boolean(target && target.grade && target.grade.ok);
}

export function unitFromTarget(target, catalog) {
 if (!target) return null;
 if (target.unit != null && Number.isFinite(Number(target.unit))) return Number(target.unit);
 if (target.type === 'question') {
  const match = /^u([1-4])-/.exec(target.id || '');
  return match ? Number(match[1]) : null;
 }
 const meta = catalog && catalog.examples && catalog.examples[target.id];
 if (meta && meta.unit != null) return Number(meta.unit);
 return null;
}

export function localRegrade(spec, target) {
 if (!target) return {ok: false, checked: false, skip: true, reason: REVERIFY_SKIP_MISSING, method: 'none'};
 if (spec && spec.kind === '서술') {
  return {ok: false, checked: false, skip: true, reason: REVERIFY_SKIP_ESSAY, method: 'essay'};
 }
 const source = submittedSource(target);
 if (spec && spec.kind === '순서') {
  let value = source;
  try { value = JSON.parse(source); } catch { /* 제출이 줄글이면 문자열 비교 */ }
  const ok = normAnswer(value) === normAnswer(spec.answer);
  return {ok, checked: true, skip: false, reason: '', method: 'order'};
 }
 if (spec && spec.kind && spec.kind !== '구현' && spec.kind !== '오류 수정' && !spec.starter && !spec.checks) {
  const ok = normAnswer(source) === normAnswer(spec.answer);
  return {ok, checked: true, skip: false, reason: '', method: 'text'};
 }
 return {ok: false, checked: false, skip: false, reason: '', method: 'pyodide'};
}

export function pyodidePayload(spec, target) {
 const files = target && target.files && typeof target.files === 'object' ? target.files : {};
 const names = Object.keys(files).filter((name) => typeof files[name] === 'string');
 if (!names.length) return null;
 const entry = (spec && spec.entry && files[spec.entry] !== undefined)
  ? spec.entry
  : (files['main.py'] !== undefined ? 'main.py' : names.find((name) => name.endsWith('.py')) || names[0]);
 let args = [];
 try {
  const parsed = JSON.parse((target && target.args) || (spec && spec.args) || '[]');
  if (Array.isArray(parsed) && parsed.every((item) => typeof item === 'string')) args = parsed;
 } catch { args = []; }
 const syntax = Boolean(spec && spec.mode && spec.mode !== 'web');
 return {
  files,
  entry,
  stdin: typeof (target && target.stdin) === 'string' ? target.stdin : ((spec && spec.stdin) || ''),
  args,
  checks: spec && spec.checks ? spec.checks : '',
  syntax
 };
}

export function compareTargetGrade(stored, live) {
 const storedValue = Boolean(stored);
 if (!live || live.skip) {
  return {status: 'skip', match: null, storedOk: storedValue, liveOk: null, label: SKIP_LABEL};
 }
 if (live.error && !live.checked && live.method === 'pyodide') {
  return {status: 'error', match: false, storedOk: storedValue, liveOk: Boolean(live.ok), label: ERROR_LABEL};
 }
 const liveOk = Boolean(live.ok);
 const match = storedValue === liveOk;
 return {
  status: match ? 'match' : 'mismatch',
  match,
  storedOk: storedValue,
  liveOk,
  label: match ? MATCH_LABEL : MISMATCH_LABEL
 };
}

export function summarizeReverify(rows) {
 const out = {total: 0, match: 0, mismatch: 0, skip: 0, error: 0};
 for (const row of rows || []) {
  if (!row) continue;
  out.total += 1;
  if (row.status === 'match') out.match += 1;
  else if (row.status === 'mismatch') out.mismatch += 1;
  else if (row.status === 'error') out.error += 1;
  else out.skip += 1;
 }
 return out;
}

export function reverifyResultRow({uid, target, live, output} = {}) {
 const key = targetKey(target) || `${(target && target.type) || ''}:${(target && target.id) || ''}`;
 const compared = compareTargetGrade(storedOk(target), live);
 return {
  uid: uid || '',
  key,
  type: target && target.type,
  id: target && target.id,
  storedOk: compared.storedOk,
  liveOk: compared.liveOk,
  status: compared.status,
  match: compared.match,
  label: compared.label,
  reason: (live && live.reason) || '',
  output: output || (live && live.output) || ''
 };
}

export function submissionMismatchCount(results, uid) {
 return (results || []).filter((row) => row && row.uid === uid && row.status === 'mismatch').length;
}
