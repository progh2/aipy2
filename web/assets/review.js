/* 기말 총정리: 점검표 저장·진행률, 단원 펼침, 인쇄 */
(function () {
  var KEY = 'review-check-v1';
  var boxes = [].slice.call(document.querySelectorAll('input[data-review]'));
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { state = {}; }

  var bar = document.getElementById('review-progress');
  var text = document.getElementById('review-progress-text');

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* 저장 불가 환경은 무시 */ }
  }
  function update() {
    var lessons = boxes.filter(function (b) { return b.hasAttribute('data-review-lesson'); });
    var done = lessons.filter(function (b) { return b.checked; }).length;
    if (bar) bar.value = done;
    if (text) text.textContent = done + ' / ' + lessons.length;
  }
  boxes.forEach(function (b) {
    b.checked = !!state[b.getAttribute('data-review')];
    b.addEventListener('change', function () {
      var k = b.getAttribute('data-review');
      if (b.checked) state[k] = 1; else delete state[k];
      save();
      update();
    });
  });
  update();

  var reset = document.querySelector('[data-review-reset]');
  if (reset) reset.addEventListener('click', function () {
    if (!window.confirm('점검 표시를 모두 지울까요?')) return;
    state = {};
    boxes.forEach(function (b) { b.checked = false; });
    save();
    update();
  });

  var units = [].slice.call(document.querySelectorAll('details.review-unit'));
  function openFor(hash) {
    if (!hash || hash.length < 2) return;
    var el;
    try { el = document.querySelector(hash); } catch (e) { return; }
    for (var n = el; n; n = n.parentElement) {
      if (n.tagName === 'DETAILS') n.open = true;
    }
    if (el) el.scrollIntoView();
  }
  window.addEventListener('hashchange', function () { openFor(location.hash); });
  openFor(location.hash);

  [].slice.call(document.querySelectorAll('[data-review-toggle]')).forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('data-review-toggle') === 'open';
      units.forEach(function (d) { d.open = open; });
    });
  });
  var print = document.querySelector('[data-review-print]');
  if (print) print.addEventListener('click', function () { window.print(); });

  var saved = null;
  window.addEventListener('beforeprint', function () {
    var all = [].slice.call(document.querySelectorAll('.review-page details'));
    saved = all.map(function (d) { return [d, d.open]; });
    all.forEach(function (d) { d.open = true; });
  });
  window.addEventListener('afterprint', function () {
    if (saved) saved.forEach(function (p) { p[0].open = p[1]; });
    saved = null;
  });
})();
