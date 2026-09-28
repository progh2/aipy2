/* 상단 진도 막대(#137) 순수 함수. DOM·fetch에 닿지 않는다 — progress-bar.js가 여기 함수들에
   숫자·배열만 건네고 결과를 DOM에 반영한다. 데이터는 build.py가 낸 catalog.json의 'progress'
   (대단원별 {roman,title,groups,lessons}) 형태를 그대로 받는다. 순수해서 test_progress_model.mjs로
   Node에서 바로 검사한다. */

export function lessonIndex(lessons, id) {
 if (!Array.isArray(lessons)) return -1;
 return lessons.findIndex((l) => l.id === id);
}

export function midTotal(lessons) {
 if (!Array.isArray(lessons) || lessons.length === 0) return 0;
 return new Set(lessons.map((l) => l.mid)).size;
}

// index까지(포함) 등장한 서로 다른 mid 개수 = 지금 중단원의 1-based 순번.
export function midOrdinal(lessons, index) {
 if (!Array.isArray(lessons) || index < 0 || index >= lessons.length) return 0;
 const seen = new Set();
 for (let i = 0; i <= index; i += 1) seen.add(lessons[i].mid);
 return seen.size;
}

export function counterText(lessons, index) {
 if (!Array.isArray(lessons) || index < 0 || index >= lessons.length) return '';
 return `소단원 ${index + 1}/${lessons.length} · 중단원 ${midOrdinal(lessons, index)}/${midTotal(lessons)}`;
}

// 칸(segment) 목록: done(지나옴) / current(지금) / upcoming(아직). mid가 이전과 다르면 중단원
// 경계(boundary)로 표시한다. completedIds는 이 단원에서 학생이 완료 체크한 소단원 id의
// Set/배열이다(호출 쪽에서 `u{unit}-` 접두어를 이미 떼어낸 값을 건넨다).
export function segmentStates(lessons, index, completedIds) {
 if (!Array.isArray(lessons)) return [];
 const done = completedIds instanceof Set ? completedIds : new Set(completedIds || []);
 return lessons.map((l, i) => ({
  id: l.id,
  title: l.title,
  mid: l.mid,
  boundary: i > 0 && lessons[i - 1].mid !== l.mid,
  state: i < index ? 'done' : i === index ? 'current' : 'upcoming',
  completed: done.has(l.id),
 }));
}

export function clampFraction(x) {
 if (!Number.isFinite(x)) return 0;
 return Math.max(0, Math.min(1, x));
}

// 화면 안의 영역(슬라이드/실습/문제/저널) 경계. regions=[{id,label,top}]는 DOM 등장 순서로
// 정렬돼 있다고 가정하고, y(스크롤 기준점)가 몇 번째 영역의 몇 %인지를 낸다.
export function regionAt(regions, y) {
 if (!Array.isArray(regions) || regions.length === 0) return {index: -1, fraction: 0};
 let idx = 0;
 for (let i = 0; i < regions.length; i += 1) {
  if (y >= regions[i].top) idx = i;
 }
 const top = regions[idx].top;
 const bottom = idx + 1 < regions.length ? regions[idx + 1].top : top + 1;
 const fraction = bottom > top ? clampFraction((y - top) / (bottom - top)) : (y >= top ? 1 : 0);
 return {index: idx, fraction};
}

export function regionLabel(kind, count) {
 if (kind === 'slides') return count ? `슬라이드 ${count}장` : '설명';
 if (kind === 'lab') return '실습';
 if (kind === 'practice') return '문제';
 if (kind === 'journal') return '저널';
 return '';
}

// 소단원 끝 예고 문구. nearEnd가 아니면 null(표시 안 함).
export function endMessage(unit, lessons, index, nearEnd) {
 if (!nearEnd || !Array.isArray(lessons) || index < 0 || index >= lessons.length) return null;
 if (index === lessons.length - 1) return `${unit && unit.roman ? unit.roman : ''}단원 마지막 소단원입니다`;
 return `이 소단원 끝 · 다음: ${lessons[index + 1].title}`;
}

export function prevNextLesson(lessons, index) {
 if (!Array.isArray(lessons) || index < 0 || index >= lessons.length) return {prev: null, next: null};
 return {
  prev: index > 0 ? lessons[index - 1] : null,
  next: index + 1 < lessons.length ? lessons[index + 1] : null,
 };
}

export function breadcrumbText(unitProgress, index) {
 if (!unitProgress || !Array.isArray(unitProgress.lessons)) return '';
 const l = unitProgress.lessons[index];
 return l ? l.breadcrumb || '' : '';
}
