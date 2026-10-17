/* 성취수준 참고 지표(#145-B) 순수 로직 검사. node tools/web/test_achievement_model.mjs */
import assert from 'node:assert/strict';
import {
 defaultSettings, mergeSettings, subunitTopicIds, exampleIdsForStandard,
 understandingScore, applyScore, applyScoreWithDiff, reflectScore, participateScore,
 levelFromScore, standardScore, studentStandardScores, unitAverage, overallAverage,
 classDistribution, strengthsWeaknesses, achievementCsvHeader, achievementCsvRow,
 INSUFFICIENT
} from '../../web/assets/achievement-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const STANDARD = {
 code: '12파실01-01',
 area: '모듈과 패키지 활용',
 statement: '모듈과 패키지의 개념을 이해하고 설명할 수 있다.',
 subunits: [{unit: 1, id: 'overview'}, {unit: 1, id: 'define'}]
};

const QUESTIONS = [
 {id: 'u1-q001', unit: 1, topic: 'overview', level: '기본'},
 {id: 'u1-q002', unit: 1, topic: 'overview', level: '심화'},
 {id: 'u1-q003', unit: 1, topic: 'define', level: '기본'},
 {id: 'u1-q999', unit: 1, topic: 'packages', level: '기본'} // 다른 소단원 — 포함되지 않아야 함
];

// --- subunitTopicIds / exampleIdsForStandard ---
eq(subunitTopicIds(STANDARD), ['u1-overview', 'u1-define'], 'topicIds 변환');

const EXAMPLE_INDEX = {
 'copy-twice': {unit: 1, topicId: 'overview', title: '복사본', missions: [], keyLines: [{ref: '1'}]},
 'reuse': {unit: 1, topicId: 'overview', title: '재사용', missions: [{level: 1, text: 'm'}], keyLines: []},
 'sum-input': {unit: 1, topicId: 'define', title: '합', missions: [], keyLines: []},
 'os': {unit: 1, topicId: 'os-sys', title: '다른 소단원', missions: [], keyLines: []}
};
eq(
 exampleIdsForStandard(STANDARD, EXAMPLE_INDEX).sort(),
 ['copy-twice', 'reuse', 'sum-input'],
 '표준 소단원에 속한 예제만 추림'
);

// --- understandingScore ---
{
 const state = {answers: {
  'u1-q001': {status: 'done', attempts: 1},
  'u1-q002': {status: 'retry', attempts: 2}
 }};
 const result = understandingScore(STANDARD, state, QUESTIONS);
 // q001(가중1, 정답) + q002(가중1.5, 오답) → 1/(1+1.5)=40%
 eq(result, {score: 40, attempted: 2, totalQuestions: 3}, '심화 가중 반영한 이해도 점수');
}
{
 const result = understandingScore(STANDARD, {answers: {}}, QUESTIONS);
 eq(result.score, null, '시도 기록이 없으면 score는 null');
 eq(result.attempted, 0, '시도 수 0');
}
{
 // 모두 정답
 const state = {answers: {'u1-q001': {status: 'done', attempts: 1}, 'u1-q002': {status: 'done', attempts: 1}, 'u1-q003': {status: 'done', attempts: 1}}};
 eq(understandingScore(STANDARD, state, QUESTIONS).score, 100, '전부 정답이면 100');
}

// --- applyScore ---
{
 // 미션 통과(reuse), 코드 수정 없음, 예측 없음
 const state = {journals: {'m-reuse-1': '2026-01-01'}, projects: {}};
 const result = applyScore(STANDARD, state, EXAMPLE_INDEX, null);
 // 미션 적용 대상은 reuse 하나뿐이라 100%, 예측은 0/3 → 평균 50
 eq(result.score, 50, '미션 통과만 있을 때 적용 점수');
}
{
 const state = {journals: {}, projects: {}};
 const result = applyScore(STANDARD, state, EXAMPLE_INDEX, null);
 // 미션 1/1 실패(0%) + 예측 0/3(0%) → 0
 eq(result.score, 0, '아무 신호도 없으면 0');
}
{
 const emptyStandard = {code: 'x', subunits: [{unit: 9, id: 'nope'}]};
 eq(applyScore(emptyStandard, {}, EXAMPLE_INDEX, null).score, null, '해당 예제가 없으면 null');
}

// --- applyScoreWithDiff ---
{
 const state = {journals: {}, projects: {'copy-twice': {files: {'main.py': 'x'}}}};
 const modified = new Set(['copy-twice']);
 const result = applyScoreWithDiff(STANDARD, state, EXAMPLE_INDEX, modified);
 // 미션 0/1, 코드수정 1/1(touched), 예측 0/3 → (0+1+0)/3 = 33%
 eq(result.score, 33, 'diff 기반 코드 수정 신호 반영');
}

// --- reflectScore ---
{
 const tasks = {'u1-overview-1': '과제문장', 'u1-overview-2': '과제문장2'};
 const state = {journals: {
  'j-u1-overview': '충분히 긴 저널입니다',
  'd-u1-overview-1': '충분히 긴 답변입니다',
  'd-u1-overview-2': '짧음'
 }};
 const result = reflectScore(STANDARD, state, tasks, EXAMPLE_INDEX, mergeSettings({minReflectLen: 5}));
 // 저널: u1-overview만 작성(1/2개 소단원) = 0.5
 // 과제: 2개 중 1개 충족 = 0.5
 // 코드읽기: copy-twice에 keyLines 1개 있지만 미작성 = 0/1 = 0
 // 평균 (0.5+0.5+0)/3 = 0.333 → 33
 eq(result.score, 33, '저널·과제·코드읽기 평균');
}
{
 eq(reflectScore({subunits: []}, {}, {}, {}).score, null, '소단원이 없으면 null');
}

// --- participateScore ---
{
 const state = {complete: {'u1-overview': true}};
 eq(participateScore(STANDARD, state).score, 50, '소단원 2개 중 1개 완료 체크 = 50');
 eq(participateScore(STANDARD, {}).score, 0, '완료 체크 없으면 0');
}

// --- levelFromScore ---
{
 const cutoffs = defaultSettings().cutoffs;
 eq(levelFromScore(95, cutoffs), 'A', '95점은 A');
 eq(levelFromScore(90, cutoffs), 'A', '경계값 90은 A');
 eq(levelFromScore(89, cutoffs), 'B', '89는 B');
 eq(levelFromScore(60, cutoffs), 'D', '60은 D');
 eq(levelFromScore(59, cutoffs), 'E', '59는 E');
 eq(levelFromScore(null, cutoffs), null, 'null 입력은 null');
}

// --- standardScore: 증거 부족이면 판단 보류 ---
{
 const ctx = {state: {}, questions: QUESTIONS, exampleIndex: EXAMPLE_INDEX, tasks: {}};
 const result = standardScore(STANDARD, ctx);
 eq(result.insufficient, true, '시도 기록 없으면 insufficient');
 eq(result.level, INSUFFICIENT, '판단 보류 라벨');
 eq(result.score, null, '점수는 null');
}
{
 const state = {
  answers: {'u1-q001': {status: 'done', attempts: 1}},
  journals: {'j-u1-overview': '충분히 긴 저널입니다'},
  complete: {'u1-overview': true}
 };
 const ctx = {state, questions: QUESTIONS, exampleIndex: EXAMPLE_INDEX, tasks: {}};
 const result = standardScore(STANDARD, ctx);
 assert.ok(result.score > 0, '증거가 있으면 0보다 큰 점수');
 assert.ok(!result.insufficient, '증거가 있으면 insufficient=false');
}

// --- studentStandardScores / unitAverage / overallAverage ---
{
 const standards = [
  STANDARD,
  {code: '12파실01-02', area: '모듈과 패키지 활용', subunits: [{unit: 1, id: 'packages'}]}
 ];
 const state = {
  answers: {'u1-q001': {status: 'done', attempts: 1}, 'u1-q999': {status: 'done', attempts: 1}},
  complete: {'u1-overview': true}
 };
 const q2 = [...QUESTIONS];
 const ctx = {state, questions: q2, exampleIndex: EXAMPLE_INDEX, tasks: {}};
 const results = studentStandardScores(standards, ctx);
 eq(results.length, 2, '성취기준 수만큼 결과');
 const unit1Avg = unitAverage(results, standards, 1);
 assert.ok(unit1Avg.score == null || unit1Avg.score >= 0, '단원 평균 계산됨');
 const overall = overallAverage(results);
 assert.ok(overall.score == null || overall.score >= 0, '전체 평균 계산됨');
}

// --- classDistribution ---
{
 const standards = [STANDARD];
 const resultsA = [{code: STANDARD.code, score: 95, level: 'A', insufficient: false}];
 const resultsB = [{code: STANDARD.code, score: null, level: INSUFFICIENT, insufficient: true}];
 const dist = classDistribution([resultsA, resultsB], standards);
 eq(dist.length, 1, '성취기준 1개');
 eq(dist[0].counts.A, 1, 'A 1명');
 eq(dist[0].counts.insufficient, 1, '판단보류 1명');
 eq(dist[0].average, 95, '평균은 판단보류 제외');
}

// --- strengthsWeaknesses: 과장 없이 숫자 근거 포함 ---
{
 const results = [
  {code: '12파실01-01', score: 95, level: 'A', dimensions: {understand: {score: 90}, apply: {score: 80}, reflect: {score: 70}, participate: {score: 100}}},
  {code: '12파실01-02', score: 50, level: 'D', dimensions: {understand: {score: 40}, apply: {score: null}, reflect: {score: null}, participate: {score: 0}}}
 ];
 const standards = [
  {code: '12파실01-01', area: 'A영역'},
  {code: '12파실01-02', area: 'B영역'}
 ];
 const sw = strengthsWeaknesses(results, standards);
 assert.ok(sw.strengths[0].includes('95'), '강점 문장에 점수 포함');
 assert.ok(sw.weaknesses[0].includes('50'), '보완점 문장에 점수 포함');
}

// --- CSV ---
{
 const standards = [STANDARD];
 const header = achievementCsvHeader(standards);
 eq(header[0], '학번', 'CSV 헤더 학번');
 const row = achievementCsvRow({studentId: '20301', name: '김가'}, [{code: STANDARD.code, score: 80, level: 'B'}], standards);
 eq(row[0], '20301', 'CSV 행 학번');
 eq(row[1], '김가', 'CSV 행 이름');
}

// --- settings ---
{
 const merged = mergeSettings({weights: {understand: 60}});
 eq(merged.weights.understand, 60, '부분 설정이 기본값을 덮어씀');
 eq(merged.weights.apply, defaultSettings().weights.apply, '나머지는 기본값 유지');
}

console.log('PASS achievement-model: understand/apply/reflect/participate, standardScore, distribution, CSV, settings');
