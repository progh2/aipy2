/* 내 학습 기록 집계 함수 검사. node tools/web/test_my_record.mjs */
import fs from 'node:fs';
import {buildMyRecord, filterRecord, nextTodo, statusBadges, percent} from '../../web/assets/my-record-model.js';

function eq(actual, expected, label) {
 const l = JSON.stringify(actual), r = JSON.stringify(expected);
 if (l !== r) throw new Error(`${label}: ${l} !== ${r}`);
}

const catalog = {
 topics: {
  'units/unit01/index.html': [
   {id: 'overview', title: '개요', href: 'units/unit01/overview.html', practiceHref: 'units/unit01/q-overview.html', tasks: ['과제1', '과제2'], examples: []},
   {id: 'define', title: '정의', href: 'units/unit01/define.html', practiceHref: 'units/unit01/q-define.html', tasks: [], examples: []}
  ],
  'units/unit02/index.html': [
   {id: 'ui', title: 'UI', href: 'units/unit02/ui.html', practiceHref: 'units/unit02/q-ui.html', tasks: [], examples: []}
  ]
 },
 examples: {},
 questions: [
  {id: 'u1-q1', unit: 1, topic: 'overview', kind: '선택', prompt: 'a', options: ['x', 'y'], answer: 'x'},
  {id: 'u1-q2', unit: 1, topic: 'overview', kind: '서술', prompt: 'b'},
  {id: 'u1-q3', unit: 1, topic: 'define', kind: '선택', prompt: 'c', options: ['x', 'y'], answer: 'y'},
  {id: 'u2-q4', unit: 2, topic: 'ui', kind: '구현', prompt: 'd'}
 ]
};

// 1) 빈 기록
const empty = buildMyRecord({}, catalog);
eq(empty.empty, true, 'empty flag');
eq(empty.overall, {topics: 3, done: 0, questions: 4, answered: 0, correct: 0, journals: 0, rate: 0}, 'empty overall');
eq(empty.todo.length, 3, 'empty todo');
eq(buildMyRecord(null, catalog).units.length, 2, 'null state tolerated');
eq(buildMyRecord({}, {}).units, [], 'empty catalog');

// 2) 일부 완료
const part = buildMyRecord({
 complete: {'u1-overview': true},
 answers: {
  'u1-q1': {status: 'done', attempts: 1, value: 'x'},
  'u1-q2': {status: 'retry', attempts: 2, value: '내 답'}
 }
}, catalog);
const ov = part.units[0].subunits[0];
eq([ov.done, ov.qTotal, ov.qAnswered, ov.qCorrect, ov.qUnanswered, ov.needsWork], [true, 2, 2, 1, 0, false], 'overview counts');
eq(part.overall.rate, 33, 'rate 1/3');
eq(part.todo.map((t) => t.anchor), ['define', 'ui'], 'todo list');
eq(part.todo[0].reasons, ['완료 체크 안 함', '안 푼 문제 1개'], 'todo reasons');
eq(filterRecord(part, 'todo').map((u) => u.subunits.length), [1, 1], 'filter todo');
eq(statusBadges(ov).map((b) => b.text), ['완료', '문제 2/2', '저널 없음'], 'badges');

// 3) 저널만 쓴 경우: 완료·문제 없어도 저널 집계와 필터에 반영
const jr = buildMyRecord({journals: {'j-u2-ui': '배운 점', 'j-u1-define': '   '}}, catalog);
eq(jr.overall.journals, 1, 'journal count ignores blank');
eq(jr.empty, false, 'journal-only is not empty');
eq(filterRecord(jr, 'nojournal').flatMap((u) => u.subunits.map((s) => s.anchor)), ['overview', 'define'], 'nojournal filter');
eq(jr.units[1].subunits[0].journal, '배운 점', 'journal text');

// 4) 틀린 문제 필터
const wrong = buildMyRecord({
 answers: {
  'u1-q1': {status: 'retry', attempts: 3, value: 'y'},
  'u1-q3': {status: 'done', attempts: 1, value: 'y'},
  'u2-q4': {status: 'retry', attempts: 1, value: 'print'}
 }
}, catalog);
const w = filterRecord(wrong, 'wrong');
eq(w.flatMap((u) => u.subunits.map((s) => [s.anchor, s.wrongRows.map((r) => r.id)])), [['overview', ['u1-q1']], ['ui', ['u2-q4']]], 'wrong rows');
eq(filterRecord(buildMyRecord({}, catalog), 'wrong'), [], 'no wrong in empty');

// 5) 직접 해 보세요 입력·제출
const task = buildMyRecord({journals: {'d-u1-overview-1': '내 설명', 'd-u1-overview-submitted': '2026-11-01T00:00:00Z'}}, catalog);
const tov = task.units[0].subunits[0];
eq([tov.taskItems.length, tov.taskItems[0].text, tov.taskItems[0].submitted, tov.taskTotal], [1, '내 설명', true, 2], 'task item');
eq(task.empty, false, 'task-only is not empty');
eq(percent(1, 3), 33, 'percent');
eq(percent(0, 0), 0, 'percent zero');

// 6) 실제 catalog.json과도 맞물려야 한다.
const real = JSON.parse(fs.readFileSync(new URL('../../web/data/catalog.json', import.meta.url), 'utf8'));
const r = buildMyRecord({}, real);
eq(r.units.length, 4, 'real units');
eq(r.overall.questions, real.questions.length, 'real question total');
console.log('PASS test_my_record');
