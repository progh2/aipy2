/* 상단 진도 막대(#137). 소단원 및 그에 딸린 페이지(ex-, q-, tut- 등, 모두 layout()이
   topic=소단원id를 넘겨 <div id="progress-bar"> 컨테이너를 낸 페이지)에서만 동작한다.
   데이터는 data/catalog.json의 'progress'를 fetch해서 쓴다 — 오프라인·실패 시 막대는 숨긴 채로
   둔다(화면이 깨지지 않는 것이 우선). 순수 계산은 progress-model.js에 있다. */
import {
 lessonIndex, counterText, segmentStates, regionAt, regionLabel, endMessage, clampFraction,
} from './progress-model.js';

// (#142) 헤더·진도 막대 실제 높이를 --header-h·--progress-h로 게시한다. 이 값은 따라가기 UI
// (follow.js/account.css)·헤더 밑 sticky 요소들이 겹치지 않게 쓰는 공용 좌표다. 진도 막대가
// 없는 페이지(단원 목차·홈 등)에서도 --header-h는 필요하므로, 아래 topic 가드보다 먼저,
// 항상 실행한다.
(() => {
 const body = document.body;
 const header = document.querySelector('header.top');
 function sync() {
  const bar = document.getElementById('progress-bar');
  const headerH = header && header.offsetHeight && !body.classList.contains('hide-header') && !body.classList.contains('presenting')
   ? header.offsetHeight : 0;
  const barH = bar && !bar.hidden ? bar.offsetHeight : 0;
  document.documentElement.style.setProperty('--header-h', `${headerH}px`);
  document.documentElement.style.setProperty('--progress-h', `${barH}px`);
  document.documentElement.style.scrollPaddingTop = `${headerH + barH + 12}px`;
  document.documentElement.style.setProperty('--rail-top', `${headerH + barH + 12}px`);
 }
 sync();
 window.addEventListener('resize', sync);
 window.addEventListener('load', sync);
 const classObserver = new MutationObserver(sync);
 classObserver.observe(body, {attributes: true, attributeFilter: ['class']});
 const bar = document.getElementById('progress-bar');
 if (bar) {
  const barObserver = new MutationObserver(sync);
  barObserver.observe(bar, {attributes: true, attributeFilter: ['hidden'], childList: true, subtree: true});
 }
 window.aipyOffsets = {sync};
})();

(async () => {
 const root = document.getElementById('progress-bar');
 if (!root) return;
 const body = document.body;
 const prefix = body.dataset.prefix || '';
 const topicId = body.dataset.topic || '';
 const unitNum = Number(body.dataset.unit || 0);
 if (!topicId || !unitNum) return;

 let catalog;
 try {
  const res = await fetch(`${prefix}data/catalog.json`);
  if (!res.ok) return;
  catalog = await res.json();
 } catch {
  return; // 오프라인 등 — 막대는 hidden 그대로 둔다.
 }
 const unitProgress = catalog && catalog.progress && catalog.progress[unitNum];
 if (!unitProgress || !Array.isArray(unitProgress.lessons)) return;
 const lessons = unitProgress.lessons;
 const index = lessonIndex(lessons, topicId);
 if (index < 0) return;

 // ── DOM 뼈대 ──────────────────────────────────────────────────────────
 root.innerHTML = '';
 const top = document.createElement('div');
 top.className = 'progress-bar-top';
 const pathEl = document.createElement('span');
 pathEl.className = 'progress-bar-path';
 const countEl = document.createElement('span');
 countEl.className = 'progress-bar-count';
 top.append(pathEl, countEl);

 const track = document.createElement('div');
 track.className = 'progress-bar-track';
 track.setAttribute('role', 'list');
 track.setAttribute('aria-label', `${unitProgress.roman}단원 소단원 진행`);

 const endEl = document.createElement('p');
 endEl.className = 'progress-bar-end';
 endEl.setAttribute('aria-live', 'polite');

 root.append(top, track, endEl);
 root.hidden = false;

 // ── 완료 체크(window.aipyLearning, 없으면 생략) ─────────────────────────
 function completedIds() {
  try {
   const learning = window.aipyLearning;
   if (!learning || typeof learning.getState !== 'function') return [];
   const state = learning.getState();
   const complete = state && state.complete;
   if (!complete) return [];
   const prefixKey = `u${unitNum}-`;
   return Object.keys(complete)
    .filter((k) => complete[k] && k.startsWith(prefixKey))
    .map((k) => k.slice(prefixKey.length));
  } catch {
   return [];
  }
 }

 let segEls = [];
 function renderTop() {
  pathEl.textContent = lessons[index].breadcrumb || '';
  pathEl.title = pathEl.textContent;
  countEl.textContent = counterText(lessons, index);
 }

 function renderTrack() {
  track.innerHTML = '';
  segEls = [];
  const states = segmentStates(lessons, index, completedIds());
  states.forEach((seg) => {
   const item = document.createElement('div');
   item.className = 'progress-bar-seg' + (seg.boundary ? ' boundary' : '') + ' ' + seg.state;
   item.setAttribute('role', 'listitem');
   const fill = document.createElement('span');
   fill.className = 'seg-fill';
   item.append(fill);
   if (seg.completed) {
    const check = document.createElement('span');
    check.className = 'seg-check';
    check.textContent = '✓';
    check.setAttribute('aria-hidden', 'true');
    item.append(check);
   }
   const link = document.createElement('a');
   link.href = `${seg.id}.html`;
   link.title = seg.title + (seg.completed ? ' · 완료' : '');
   link.setAttribute('aria-label', `${seg.title}${seg.state === 'current' ? ' · 지금 보는 중' : ''}`);
   if (seg.state === 'current') link.setAttribute('aria-current', 'page');
   item.append(link);
   track.append(item);
   segEls.push(item);
  });
 }

 renderTop();
 renderTrack();
 document.addEventListener('change', (e) => {
  if (e.target && e.target.matches && e.target.matches('[data-complete]')) renderTrack();
 });
 document.addEventListener('aipy:learning-ready', renderTrack);

 // ── 페이지 안 영역(슬라이드/실습/문제/저널) 경계 — DOM에서 직접 찾는다 ─────
 function buildRegions() {
  const candidates = [];
  const explainEl = document.getElementById(topicId);
  if (explainEl) {
   const slideCount = explainEl.querySelectorAll('.deck-slide').length;
   candidates.push({id: 'explain', label: regionLabel(slideCount ? 'slides' : 'explain', slideCount), el: explainEl});
  }
  const labEl = document.getElementById(`${topicId}-lab`) || document.getElementById('lab');
  if (labEl && !candidates.some((c) => c.el === labEl)) {
   candidates.push({id: 'lab', label: regionLabel('lab'), el: labEl});
  }
  const qEl = document.getElementById('practice') || document.getElementById('practice-link');
  if (qEl) candidates.push({id: 'practice', label: regionLabel('practice'), el: qEl});
  const jEl = document.getElementById('journal');
  if (jEl) candidates.push({id: 'journal', label: regionLabel('journal'), el: jEl});
  return candidates
   .map((c) => ({id: c.id, label: c.label, top: c.el.getBoundingClientRect().top + window.scrollY}))
   .sort((a, b) => a.top - b.top);
 }

 let regions = buildRegions();

 function currentSegFill() {
  const seg = segEls[index];
  if (!seg) return null;
  return seg.querySelector('.seg-fill');
 }

 function onScroll() {
  if (regions.length === 0) {
   endEl.textContent = '';
   return;
  }
  const y = window.scrollY + window.innerHeight * 0.35;
  const {fraction} = regionAt(regions, y);
  const fill = currentSegFill();
  if (fill) fill.style.width = `${Math.round(clampFraction(fraction) * 100)}%`;
  const lastRegion = regions.length - 1;
  const atLast = regionAt(regions, y).index === lastRegion;
  const nearBottom = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 80;
  const nearEnd = (atLast && fraction > 0.75) || nearBottom;
  const msg = endMessage(unitProgress, lessons, index, nearEnd);
  endEl.textContent = msg || '';
 }

 window.addEventListener('scroll', () => window.requestAnimationFrame(onScroll), {passive: true});
 window.addEventListener('resize', () => {
  regions = buildRegions();
  onScroll();
 });
 // 슬라이드·이미지가 늦게 로드되며 레이아웃이 밀릴 수 있어 한 번 더 재계산한다.
 window.addEventListener('load', () => {
  regions = buildRegions();
  onScroll();
 });
 onScroll();

 // 헤더 높이·진도 막대 높이·접기 상태에 맞춘 --header-h/--progress-h/scroll-padding-top은
 // 위쪽의 공용 sync()가 담당한다(모든 페이지 공통). 여기서는 막대가 실제로 그려진 뒤
 // 한 번 더 맞춰 준다(막대 트랙 렌더로 높이가 막 잡힌 시점).
 if (window.aipyOffsets) window.aipyOffsets.sync();
})();
