/* #145 A 답변 내역 페이지 확장 순수 함수 검사. node tools/web/test_teacher_answers_sections.mjs */
import {
 buildStudentDetailSections, mergeProjectGroupsIntoSections, summarizeStudentActivity,
 classOverviewColumns, buildClassOverviewRow, classOverviewCellLabel,
 classSummaryCsvRows, classSummaryCsv, classLongCsvRows, anchorForJournalItem
} from '../../web/assets/teacher-answers-model.js';
import {loadStatesForUids, snapshotToEntry} from '../../web/assets/class-state-loader.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const topics = [
 {id: 'u1-overview', unit: 1, anchor: 'overview', title: '모듈이 필요한 이유', short: '1.1'},
 {id: 'u1-define', unit: 1, anchor: 'define', title: '모듈 정의', short: '1.2'},
 {id: 'u2-ui', unit: 2, anchor: 'ui', title: 'GUI 시작', short: '2.1'}
];
const titles = {'u1-overview': '모듈이 필요한 이유', 'u1-define': '모듈 정의', 'u2-ui': 'GUI 시작'};
const tasks = {'u1-define-1': '모듈을 하나 만들어 import 해 보세요.'};
const exampleIndex = {'copy-twice': {unit: 1, topicId: 'define', title: '복사 두 번', keyLines: [], missions: [{level: '기본'}]}};
const questions = [
 {id: 'u1-q001', unit: 1, topic: 'overview', kind: '선택', prompt: '문제1', options: ['a', 'b'], answer: 'a'},
 {id: 'u1-q003', unit: 1, topic: 'define', kind: '선택', prompt: '문제3', options: ['a', 'b'], answer: 'b'}
];

const state = {
 answers: {
  'u1-q001': {status: 'done', attempts: 1, value: 'a'}
 },
 journals: {
  'u1-learn': '모듈 개념을 배웠다',
  'j-u1-define': '모듈 정의가 헷갈렸다',
  'd-u1-define-1': 'answer.py를 import했다',
  'd-u1-define-submitted': '2026-09-29T01:00:00.000Z',
  'm-copy-twice-1': '2026-09-30T02:00:00.000Z'
 }
};

// 1) buildStudentDetailSections — 카탈로그 순서대로 단원→소단원, 입력 없는 소단원도 포함.
const sections = buildStudentDetailSections(state, {titles, tasks, exampleIndex, questions, topics});
eq(sections.map((u) => u.unit), [1, 2], 'units present in order');
const u1 = sections.find((u) => u.unit === 1);
eq(u1.subunits.map((s) => s.topic), ['overview', 'define'], 'unit1 subunits follow catalog order');
eq(u1.unitJournal, [{key: 'learn', label: '이해한 개념', text: '모듈 개념을 배웠다'}], 'unit-level journal captured separately');
const overviewSub = u1.subunits.find((s) => s.topic === 'overview');
eq(overviewSub.hasContent, true, 'overview has an answer so hasContent is true');
eq(overviewSub.answers.length, 1, 'overview has one answer row');
const defineSub = u1.subunits.find((s) => s.topic === 'define');
eq(defineSub.hasContent, true, 'define has journal/task content');
eq(defineSub.journalItems.length >= 2, true, 'define collects topic journal + task + mission items');
const u2 = sections.find((u) => u.unit === 2);
eq(u2.subunits.map((s) => s.topic), ['ui'], 'unit2 ui subunit included even with no input');
eq(u2.subunits[0].hasContent, false, 'ui subunit with no input is marked empty for collapsing');

// 2) mergeProjectGroupsIntoSections — 예제 코드 섹션을 올바른 소단원에 붙인다.
const projectGroups = [{unit: 1, topic: 'define', topicTitle: '모듈 정의', items: [{id: 'copy-twice', title: '복사 두 번', diff: {added: 1, removed: 0, same: false}}]}];
const merged = mergeProjectGroupsIntoSections(sections, projectGroups);
const mergedDefine = merged.find((u) => u.unit === 1).subunits.find((s) => s.topic === 'define');
eq(mergedDefine.projectItems.length, 1, 'project items merged into matching subunit');
// unrelated subunit untouched
const mergedOverview = merged.find((u) => u.unit === 1).subunits.find((s) => s.topic === 'overview');
eq(mergedOverview.projectItems, [], 'subunit without project items stays empty array');

// 3) anchorForJournalItem — 접두 섞인 topicId에서 anchor를 복원한다.
eq(anchorForJournalItem({topicId: 'u1-define'}, 1, ['overview', 'define']), 'define', 'plain topic journal anchor');
eq(anchorForJournalItem({topicId: 'define-task1'}, 1, ['overview', 'define']), 'define', 'task item anchor without unit prefix');
eq(anchorForJournalItem({topicId: 'define-mission-copy-twice-1'}, 1, ['overview', 'define']), 'define', 'mission item anchor');

// 4) summarizeStudentActivity
const card = {doneCount: 1, topicTotal: 3, completeRate: 1 / 3, correct: 1, attempted: 1, accuracy: 1, lastActivityLabel: '10/1 09:00'};
const summary = summarizeStudentActivity(state, card, {titles, tasks, exampleIndex});
eq(summary.doneCount, 1, 'summary carries card doneCount');
eq(summary.missionPassCount, 1, 'summary counts mission pass entries');
eq(summary.journalCount >= 3, true, 'summary counts all journal/task/mission entries');

// 5) class overview row/columns/cell label
const cols = classOverviewColumns(topics);
eq(cols.map((c) => c.key), ['1::overview', '1::define', '2::ui'], 'overview columns follow catalog order');
const entryReady = {status: 'ready', data: state};
const row = buildClassOverviewRow({key: 'r:1', uid: 'u1', label: '20301 김가', studentId: '20301'}, entryReady, {titles, tasks, exampleIndex, questions, topics});
eq(row.cells['1::overview'], {correct: 1, attempted: 1, journal: 0}, 'overview cell counts the correct answer');
eq(classOverviewCellLabel(row.cells['1::overview']), '1/1', 'cell label shows correct/attempted');
eq(classOverviewCellLabel(row.cells['1::define']).includes('✎'), true, 'define cell shows journal mark');
const pendingRow = buildClassOverviewRow({key: 'r:2', uid: 'u2', label: '20302 이나', studentId: '20302'}, {status: 'loading'}, {topics});
eq(pendingRow.cells, {}, 'pending entry has no cells yet');

// 6) CSV
const summaries = new Map([['u1', summary]]);
const csvRows = classSummaryCsvRows([{uid: 'u1', studentId: '20301', name: '김가', label: '20301 김가'}], summaries);
eq(csvRows[0][0], '학번', 'summary csv header first column');
eq(csvRows[1][0], '20301', 'summary csv row has student id');
const csvText = classSummaryCsv([{uid: 'u1', studentId: '20301', name: '김가', label: '20301 김가'}], summaries);
eq(csvText.startsWith('﻿'), true, 'summary csv has BOM for excel');

const longRows = classLongCsvRows(
 [{uid: 'u1', studentId: '20301', name: '김가', label: '20301 김가'}],
 new Map([['u1', entryReady]]),
 {titles, tasks, exampleIndex, questions}
);
eq(longRows[0], ['학번', '이름', '단원', '소단원', '항목종류', '키', '내용', '정답여부', '시각'], 'long csv header');
eq(longRows.length > 1, true, 'long csv has data rows');
eq(longRows.some((r) => r[4] === '문항' && r[7] === '정답'), true, 'long csv marks correct answer row');
eq(longRows.some((r) => r[4] === '저널·과제'), true, 'long csv includes journal rows');

// 7) class-state-loader — concurrency-limited bulk fetch, pure except for injected fetchOne.
eq(snapshotToEntry(null), {status: 'empty'}, 'null snapshot is empty');
eq(snapshotToEntry({exists: () => true, data: () => ({a: 1})}), {status: 'ready', data: {a: 1}}, 'modular snapshot shape');
eq(snapshotToEntry({exists: false}), {status: 'empty'}, 'plain object shape not existing');

async function runLoaderTest() {
 const uids = ['a', 'b', 'c', 'd'];
 let inFlight = 0;
 let maxInFlight = 0;
 const calls = [];
 const fetchOne = async (uid) => {
  inFlight += 1;
  maxInFlight = Math.max(maxInFlight, inFlight);
  calls.push(uid);
  await new Promise((resolve) => setTimeout(resolve, 5));
  inFlight -= 1;
  if (uid === 'c') throw new Error('boom');
  return {exists: () => uid !== 'd', data: () => ({uid})};
 };
 const progressSeen = [];
 const result = await loadStatesForUids(uids, fetchOne, {concurrency: 2, onProgress: (p) => progressSeen.push(p.done)});
 eq(maxInFlight <= 2, true, 'loader respects concurrency limit');
 eq(result.get('a'), {status: 'ready', data: {uid: 'a'}}, 'loader resolves ready student');
 eq(result.get('c').status, 'error', 'loader captures per-student fetch error without failing others');
 eq(result.get('d'), {status: 'empty'}, 'loader resolves empty (no state doc) student');
 eq(progressSeen.length, 4, 'onProgress fired once per uid');
 console.log('PASS: teacher-answers-model sections/overview/csv + class-state-loader');
}

runLoaderTest();
