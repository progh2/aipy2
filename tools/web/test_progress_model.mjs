/* progress-model 순수 함수 검사(#137). node tools/web/test_progress_model.mjs */
import {
 lessonIndex, midTotal, midOrdinal, counterText, segmentStates, clampFraction, regionAt,
 regionLabel, endMessage, prevNextLesson, breadcrumbText,
} from '../../web/assets/progress-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

const lessons = [
 {id: 'ml-libraries', title: '파이썬 머신러닝 라이브러리 소개', mid: 1, breadcrumb: 'Ⅲ 파이썬과 머신러닝 › 02 머신러닝 라이브러리 활용 › 01 파이썬 머신러닝 라이브러리 소개'},
 {id: 'ml-preprocess', title: '데이터 준비와 전처리', mid: 1, breadcrumb: 'Ⅲ 파이썬과 머신러닝 › 02 머신러닝 라이브러리 활용 › 02 데이터 준비와 전처리'},
 {id: 'ml-classification', title: '주요 머신러닝 알고리즘 활용', mid: 1, breadcrumb: 'Ⅲ 파이썬과 머신러닝 › 02 머신러닝 라이브러리 활용 › 03 주요 머신러닝 알고리즘 활용'},
 {id: 'ml-metrics', title: '모델 평가와 선택', mid: 1, breadcrumb: 'Ⅲ 파이썬과 머신러닝 › 02 머신러닝 라이브러리 활용 › 04 모델 평가와 선택'},
];
const unit = {roman: 'Ⅲ', title: '파이썬과 머신러닝', lessons};

eq(lessonIndex(lessons, 'ml-classification'), 2, 'lessonIndex finds by id');
eq(lessonIndex(lessons, 'nope'), -1, 'lessonIndex missing');
eq(lessonIndex(null, 'x'), -1, 'lessonIndex handles non-array');

eq(midTotal(lessons), 1, 'midTotal all same group');
eq(midTotal([]), 0, 'midTotal empty');
const mixed = [{mid: 0}, {mid: 0}, {mid: 1}, {mid: 2}, {mid: 2}];
eq(midTotal(mixed), 3, 'midTotal counts distinct groups');
eq(midOrdinal(mixed, 0), 1, 'midOrdinal first item is group 1');
eq(midOrdinal(mixed, 2), 2, 'midOrdinal at group boundary');
eq(midOrdinal(mixed, 4), 3, 'midOrdinal last item is last group');
eq(midOrdinal(mixed, -1), 0, 'midOrdinal out of range');

eq(counterText(lessons, 2), '소단원 3/4 · 중단원 1/1', 'counterText format');
eq(counterText([], 0), '', 'counterText empty lessons');

const segs = segmentStates(lessons, 2, ['ml-libraries']);
eq(segs.length, 4, 'segmentStates length');
eq(segs[0].state, 'done', 'segment before current is done');
eq(segs[2].state, 'current', 'segment at index is current');
eq(segs[3].state, 'upcoming', 'segment after current is upcoming');
eq(segs[0].completed, true, 'segment completion flag true');
eq(segs[1].completed, false, 'segment completion flag false');
eq(segs[0].boundary, false, 'first segment never a boundary');
const withGroups = segmentStates(
 [{id: 'a', title: 'A', mid: 0}, {id: 'b', title: 'B', mid: 0}, {id: 'c', title: 'C', mid: 1}],
 1, [],
);
eq(withGroups[1].boundary, false, 'same mid is not a boundary');
eq(withGroups[2].boundary, true, 'mid change marks a boundary');

eq(clampFraction(-0.2), 0, 'clampFraction floors at 0');
eq(clampFraction(1.4), 1, 'clampFraction caps at 1');
eq(clampFraction(0.5), 0.5, 'clampFraction passthrough');
eq(clampFraction(NaN), 0, 'clampFraction NaN -> 0');

const regions = [{id: 'explain', label: '슬라이드 3장', top: 100}, {id: 'lab', label: '실습', top: 500}, {id: 'journal', label: '저널', top: 700}];
eq(regionAt(regions, 50), {index: 0, fraction: 0}, 'regionAt before first region clamps to start');
eq(regionAt(regions, 300), {index: 0, fraction: 0.5}, 'regionAt midway through first region');
eq(regionAt(regions, 500), {index: 1, fraction: 0}, 'regionAt exactly at a boundary starts that region');
eq(regionAt(regions, 750), {index: 2, fraction: 1}, 'regionAt past the last region caps at 1');
eq(regionAt([], 10), {index: -1, fraction: 0}, 'regionAt empty regions');

eq(regionLabel('slides', 5), '슬라이드 5장', 'regionLabel slides with count');
eq(regionLabel('slides', 0), '설명', 'regionLabel slides falls back without count');
eq(regionLabel('lab'), '실습', 'regionLabel lab');
eq(regionLabel('practice'), '문제', 'regionLabel practice');
eq(regionLabel('journal'), '저널', 'regionLabel journal');
eq(regionLabel('other'), '', 'regionLabel unknown kind');

eq(endMessage(unit, lessons, 1, false), null, 'endMessage hidden when not near end');
eq(endMessage(unit, lessons, 1, true), '이 소단원 끝 · 다음: 주요 머신러닝 알고리즘 활용', 'endMessage previews next lesson');
eq(endMessage(unit, lessons, 3, true), 'Ⅲ단원 마지막 소단원입니다', 'endMessage marks unit end at last lesson');

eq(prevNextLesson(lessons, 0).prev, null, 'prevNextLesson no prev at start');
eq(prevNextLesson(lessons, 0).next.id, 'ml-preprocess', 'prevNextLesson next at start');
eq(prevNextLesson(lessons, 3).next, null, 'prevNextLesson no next at end');
eq(prevNextLesson(lessons, 3).prev.id, 'ml-classification', 'prevNextLesson prev at end');

eq(breadcrumbText(unit, 2), 'Ⅲ 파이썬과 머신러닝 › 02 머신러닝 라이브러리 활용 › 03 주요 머신러닝 알고리즘 활용', 'breadcrumbText reads the lesson breadcrumb');
eq(breadcrumbText(null, 0), '', 'breadcrumbText handles missing unit');

console.log('PASS: progress-model helpers');
