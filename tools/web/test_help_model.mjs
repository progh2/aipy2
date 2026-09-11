/* 도움 요청 순수 함수 검사. node tools/web/test_help_model.mjs */
import {
 HELP_COOLDOWN_MS, HELP_LABEL, HELP_CANCEL_LABEL, HELP_KEEP_WORKING, helpRequestFields,
 canCreateHelp, openHelpForTopic, sortOpenHelp, clipLastError, helpStatusLabel
} from '../../web/assets/help-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

eq(HELP_LABEL, '도움 요청', 'help label');
eq(HELP_CANCEL_LABEL, '요청 취소', 'cancel label');
eq(HELP_KEEP_WORKING.includes('계속'), true, 'keep working');
eq(HELP_COOLDOWN_MS >= 3000 && HELP_COOLDOWN_MS <= 10000, true, 'cooldown');

const profile = {
 uid: 'u1', email: '20314@e-mirim.hs.kr', studentId: '20314', admissionYear: 2025,
 name: '홍길동', grade: 2, classroom: 3, number: 14
};
const fields = helpRequestFields({
 profile, classId: '2-3', topic: 'u1-overview', example: 'reuse', lastError: 'NameError: x'
});
eq(fields.status, 'open', 'status open');
eq(fields.classId, '2-3', 'class id');
eq(fields.classroom, 3, 'roster classroom int');
eq(fields.topic, 'u1-overview', 'topic');
eq(fields.example, 'reuse', 'example');
eq(fields.lastError, 'NameError: x', 'error');
eq(fields.studentId, '20314', 'student id');
eq(helpRequestFields({profile}).classId, '2-3', 'class id from profile');

eq(clipLastError('  boom\n  ').length > 0, true, 'clip error');
eq(clipLastError('e'.repeat(400)).length, 300, 'error max');

const open = [{id: 'h1', status: 'open', topic: 'u1-overview'}];
eq(canCreateHelp({openRequests: open, topic: 'u1-overview', now: 10}).ok, false, 'duplicate topic');
eq(canCreateHelp({openRequests: open, topic: 'u1-define', now: 10}).ok, true, 'other topic ok');
eq(canCreateHelp({openRequests: [{status: 'open', topic: null}], topic: null, now: 10}).reason, 'duplicate', 'null topic duplicate');
eq(canCreateHelp({openRequests: [], topic: 'u1-overview', now: 20, lastCreateAt: 16}).reason, 'cooldown', 'cooldown');
eq(openHelpForTopic(open, 'u1-overview').id, 'h1', 'open for topic');

const sorted = sortOpenHelp([
 {status: 'open', createdAt: 30, studentId: '2', name: 'B'},
 {status: 'resolved', createdAt: 1, studentId: '3', name: 'C'},
 {status: 'open', createdAt: 10, studentId: '1', name: 'A'}
]);
eq(sorted.map((row) => row.studentId), ['1', '2'], 'open time order');
eq(helpStatusLabel('resolved'), '해결', 'resolved label');
eq(helpStatusLabel('cancelled'), '취소됨', 'cancelled label');

console.log('PASS: help-model helpers');
