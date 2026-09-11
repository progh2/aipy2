/* class-picker 순수 함수 검사. node tools/web/test_class_picker.mjs */
import {
 classId, parseClassId, labelClass, inClass, classesFromRoster,
 storageKey, readSelectedClass, writeSelectedClass, resolveSelectedClass, classDetail,
 resolveTeacherClassId
} from '../../web/assets/class-picker.js';

const store = new Map();
globalThis.localStorage = {
 getItem: (key) => (store.has(key) ? store.get(key) : null),
 setItem: (key, value) => { store.set(key, String(value)); },
 removeItem: (key) => { store.delete(key); }
};

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(classId({grade: 2, classroom: 3}), '2-3', 'classId');
eq(classId({grade: '2', classroom: '3'}), '2-3', 'classId string numbers');
eq(classId({grade: 2}), '', 'classId missing classroom');
eq(parseClassId('2-3'), {grade: 2, classroom: 3}, 'parseClassId');
eq(parseClassId('nope'), null, 'parseClassId invalid');
eq(labelClass('2-3'), '2학년 3반', 'labelClass');
eq(inClass({grade: 2, classroom: 3}, '2-3'), true, 'inClass match');
eq(inClass({grade: 2, classroom: 4}, '2-3'), false, 'inClass other class');

const classes = classesFromRoster([
 {grade: 2, classroom: 4, name: 'B'},
 {grade: 2, classroom: 3, name: 'A'},
 {grade: 2, classroom: 3, name: 'C'},
 {name: 'no class'}
]);
eq(classes.map((c) => [c.id, c.count]), [['2-3', 2], ['2-4', 1]], 'classesFromRoster');

eq(storageKey('Teacher@e-mirim.hs.kr'), 'aipy-teacher-class:teacher@e-mirim.hs.kr', 'storageKey');
eq(readSelectedClass('t@e-mirim.hs.kr'), '', 'read empty');
writeSelectedClass('t@e-mirim.hs.kr', '2-3');
eq(readSelectedClass('t@e-mirim.hs.kr'), '2-3', 'write then read');
eq(resolveSelectedClass('t@e-mirim.hs.kr', classes), '2-3', 'resolve saved');
eq(resolveSelectedClass('other@e-mirim.hs.kr', classes), '2-3', 'resolve first available');
eq(resolveSelectedClass('t@e-mirim.hs.kr', [{id: '1-1', grade: 1, classroom: 1}]), '1-1', 'resolve stale');
eq(classDetail('2-3'), {classId: '2-3', grade: 2, classroom: 3, label: '2학년 3반'}, 'classDetail');
eq(resolveTeacherClassId('t@e-mirim.hs.kr', {classId: '2-4'}), '2-4', 'resolve published class');
eq(resolveTeacherClassId('t@e-mirim.hs.kr', null), '2-3', 'resolve saved teacher class');
eq(resolveTeacherClassId('nobody@e-mirim.hs.kr', {classId: ''}), '', 'resolve empty class');
eq(resolveTeacherClassId('t@e-mirim.hs.kr', {classId: 'nope'}), '2-3', 'resolve invalid published falls back');

console.log('PASS: class-picker helpers');
