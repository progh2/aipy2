/* '이어서 학습하기' 링크 변환 검사(#7). node tools/web/test_resume_model.mjs */
import {resumeHref, LESSON_SLUGS} from '../../web/assets/resume-model.js';

function eq(actual, expected, label) {
 const left = JSON.stringify(actual), right = JSON.stringify(expected);
 if (left !== right) throw new Error(`${label}: ${left} !== ${right}`);
}

// 현재 형식은 그대로 유지한다.
eq(resumeHref('units/unit01/overview.html'), 'units/unit01/overview.html', 'modern page unchanged');
eq(resumeHref('units/unit02/memo.html#lab'), 'units/unit02/memo.html#lab', 'modern page with anchor unchanged');

// 구형 소단원 앵커 → 그 소단원의 독립 페이지.
eq(resumeHref('units/unit01/index.html#overview'), 'units/unit01/overview.html', 'legacy lesson anchor to page');
eq(resumeHref('units/unit03/index.html#ml-cluster'), 'units/unit03/ml-cluster.html', 'unit3 lesson slug');

// 저널은 지금도 유효한 앵커다.
eq(resumeHref('units/unit01/index.html#journal'), 'units/unit01/index.html#journal', 'journal anchor kept');

// 옛 #practice는 단원 전체 문제집으로.
eq(resumeHref('units/unit02/index.html#practice'), 'units/unit02/practice.html', 'practice anchor to practice.html');

// #lab은 예제별 페이지로 흩어져 특정할 수 없다 → 단원 안내.
eq(resumeHref('units/unit01/index.html#lab'), 'units/unit01/index.html', 'lab anchor falls back to unit index');

// #gallery·#simulator는 2단원 index.html에만 실존한다.
eq(resumeHref('units/unit02/index.html#gallery'), 'units/unit02/index.html#gallery', 'unit2 gallery kept');
eq(resumeHref('units/unit02/index.html#simulator'), 'units/unit02/index.html#simulator', 'unit2 simulator kept');
eq(resumeHref('units/unit01/index.html#gallery'), 'units/unit01/index.html', 'unit1 gallery has no target, falls back');
eq(resumeHref('units/unit04/index.html#simulator'), 'units/unit04/index.html', 'unit4 simulator has no target, falls back');

// 완료 체크·저널 키와 같은 표기(u{N}-{slug})는 그 소단원 페이지로.
eq(resumeHref('units/unit01/index.html#u1-overview'), 'units/unit01/overview.html', 'topic-id anchor to its page');
eq(resumeHref('units/unit04/index.html#u4-cv-yolo'), 'units/unit04/cv-yolo.html', 'unit4 topic-id anchor');

// 문항 id(u{N}-q###)는 어느 소단원인지 알 수 없어 단원 안내로.
eq(resumeHref('units/unit01/index.html#u1-q001'), 'units/unit01/index.html', 'question id falls back to unit index');

// 알 수 없는 anchor도 단원 안내로(임의 문자열을 소단원 페이지로 잘못 추측하지 않는다).
eq(resumeHref('units/unit01/index.html#trace-mode'), 'units/unit01/index.html', 'unknown anchor falls back');

// 형식을 벗어난 값은 빈 문자열(caller가 기존 href를 그대로 둔다).
eq(resumeHref(''), '', 'empty string');
eq(resumeHref(null), '', 'non-string null');
eq(resumeHref('https://example.com'), '', 'unrelated url');

for (const [unit, slugs] of Object.entries(LESSON_SLUGS)) {
 eq(Array.isArray(slugs) && slugs.length > 0, true, `unit ${unit} has lesson slugs`);
}

console.log('PASS: resume-model helpers');
