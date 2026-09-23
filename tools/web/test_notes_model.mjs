/* 포스트잇 메모 순수 함수 검사. node tools/web/test_notes_model.mjs */
import {
 NOTE_COLORS, NOTE_VISIBILITY, NOTE_TEXT_MAX, randomColor, isNoteColor, isVisibility, clipNoteText,
 clampY, clampOffset, linkify, extractLinks, noteFields, normalizeNote, canSee, sortNotes, authorLabel, classIdOf,
 currentTeacherClassId, resolveNoteClassId, noteVisibilityBlocked
} from '../../web/assets/notes-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(NOTE_COLORS.length, 12, '12 colors');
eq(NOTE_COLORS.every((c) => /^#[0-9a-f]{6}$/.test(c)), true, 'hex colors');
eq(NOTE_VISIBILITY, ['private', 'students', 'all'], 'visibility values');
eq(isNoteColor(randomColor(() => 0.999)), true, 'random color valid');
eq(randomColor(() => 0), NOTE_COLORS[0], 'random first');
eq(isNoteColor('#FFF59D'), true, 'color case-insensitive');
eq(isNoteColor('#123456'), false, 'unknown color');
eq(isVisibility('all') && !isVisibility('public'), true, 'visibility check');
eq(clipNoteText('a'.repeat(NOTE_TEXT_MAX + 50)).length, NOTE_TEXT_MAX, 'clip text');
eq(clampY(-10), 0, 'clamp y low');
eq(clampY(12.6), 13, 'clamp y round');
eq(clampY('abc'), 0, 'clamp y nan');

eq(linkify('참고 https://example.com/a?b=1. 끝'), '참고 <a href="https://example.com/a?b=1" target="_blank" rel="noopener noreferrer">https://example.com/a?b=1</a>. 끝', 'linkify trailing dot');
eq(linkify('<b>x</b>'), '&lt;b&gt;x&lt;/b&gt;', 'escape html');
eq(linkify('줄1\n줄2'), '줄1<br>줄2', 'line breaks');
eq(extractLinks('a http://x.io/p) b https://y.kr'), ['http://x.io/p', 'https://y.kr'], 'extract links');

const profile = {uid: 'u1', email: 's1@e-mirim.hs.kr', studentId: '2314', name: '홍길동', grade: 2, classroom: 3};
eq(classIdOf(profile), '2-3', 'class id');
const fields = noteFields({profile, page: 'units/unit02/index.html', y: 340.4, color: 'bad', visibility: 'nope', text: 'hi'});
eq(fields, {uid: 'u1', email: 's1@e-mirim.hs.kr', studentId: '2314', name: '홍길동', classId: '2-3', page: 'units/unit02/index.html', y: 340, anchor: '', offset: 0, color: NOTE_COLORS[0], visibility: 'private', text: 'hi'}, 'note fields defaults');
eq(Object.keys(fields).sort(), ['anchor', 'classId', 'color', 'email', 'name', 'offset', 'page', 'studentId', 'text', 'uid', 'visibility', 'y'], 'field keys match rules');
eq(noteFields({profile, page: 'p', y: 1, anchor: 'lesson-overview', offset: 0.33333333}).offset, 0.3333, 'offset rounded');
eq(clampOffset(-1), 0, 'offset low'); eq(clampOffset(99), 10, 'offset high');
eq(normalizeNote('n9', {anchor: 'x', offset: '0.5'}).offset, 0.5, 'normalize offset');

const mine = normalizeNote('n1', {uid: 'u1', classId: '2-3', y: 50, visibility: 'private', color: '#b3e5fc', text: 't'});
const cls = normalizeNote('n2', {uid: 'u2', classId: '2-3', y: 10, visibility: 'students', text: 't'});
const other = normalizeNote('n3', {uid: 'u3', classId: '2-4', y: 30, visibility: 'students', text: 't'});
const pub = normalizeNote('n4', {uid: 'u3', classId: '2-4', y: 20, visibility: 'all', text: 't'});
eq(canSee(mine, {uid: 'u1', classId: '2-3'}), true, 'own private visible');
eq(canSee(mine, {uid: 'u2', classId: '2-3'}), false, 'other private hidden');
eq(canSee(cls, {uid: 'u1', classId: '2-3'}), true, 'same class students visible');
eq(canSee(other, {uid: 'u1', classId: '2-3'}), false, 'other class hidden');
eq(canSee(pub, {uid: 'u1', classId: '2-3'}), true, 'all visible');
eq(canSee(other, {uid: 't', classId: '', teacher: true}), true, 'teacher sees all');
eq(sortNotes([mine, cls, other, pub]).map((n) => n.id), ['n2', 'n4', 'n3', 'n1'], 'sort by y');
eq(authorLabel({studentId: '2314', name: '홍길동'}), '2314 홍길동', 'author label');
eq(authorLabel({}), '익명', 'author fallback');

// #120 교사 메모 classId 해석
eq(currentTeacherClassId({classId: '2-3', grade: 2, classroom: 3}), '2-3', 'teacher class id from aipyClass');
eq(currentTeacherClassId(null), '', 'no aipyClass yields empty classId');
eq(currentTeacherClassId({grade: 2}), '', 'aipyClass without classId string yields empty');

eq(resolveNoteClassId({profile: {grade: 2, classroom: 5}, teacher: false}), '2-5', 'student uses own class');
eq(resolveNoteClassId({profile: {}, teacher: true, teacherClassId: '2-3'}), '2-3', 'teacher uses selected class');
eq(resolveNoteClassId({profile: {}, teacher: true, teacherClassId: ''}), '', 'teacher with no class selected yields empty');
eq(resolveNoteClassId({profile: {}, teacher: true, teacherClassId: '3-1', existingClassId: '2-3'}), '2-3', 'existing classId is kept even if teacher switched class');

eq(noteVisibilityBlocked({teacher: true, visibility: 'students', classId: ''}), true, 'teacher without class blocked for students visibility');
eq(noteVisibilityBlocked({teacher: true, visibility: 'students', classId: '2-3'}), false, 'teacher with class not blocked');
eq(noteVisibilityBlocked({teacher: true, visibility: 'all', classId: ''}), false, 'all visibility never blocked');
eq(noteVisibilityBlocked({teacher: false, visibility: 'students', classId: ''}), false, 'student cannot set students visibility anyway, not blocked here');

const teacherFields = noteFields({
 profile: {uid: 't1', email: 't@e-mirim.hs.kr', name: '교사'},
 page: 'p', y: 1, visibility: 'students',
 classId: resolveNoteClassId({profile: {}, teacher: true, teacherClassId: '2-3'})
});
eq(teacherFields.classId, '2-3', 'teacher note stores selected classId');

console.log('notes model OK');
