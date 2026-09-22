/* 실제 브라우저 회귀 검사 (#88, #89, #90, #98).
   빌드 후 python3 -m http.server 8767 --directory web 실행.
   PLAYWRIGHT_MODULE=/path/to/playwright/index.mjs node tools/web/test_classroom_ui.mjs
   기본 의존성 이름은 playwright, CLASSROOM_URL로 테스트 서버를 바꿀 수 있습니다. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const {chromium} = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.CLASSROOM_URL || 'http://127.0.0.1:8767';
const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
try {
 const page = await browser.newPage({viewport:{width:1280,height:900}});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 // 계정 서버가 없어도 동작해야 하는 로컬 학습 UI를 검사합니다.
 await page.route('https://**',route=>route.abort());
 async function open(path){
  await page.goto(base+path);
  await page.waitForFunction(()=>window.aipyLearning?.ready);
 }
 for(const unit of [1,2,3,4]){
  const data=JSON.parse(await readFile(new URL(`../../web/data/unit${unit}.json`,import.meta.url)));
  // 문제는 독립 페이지로 분리됐다(#106) — 단원 전체 문제는 이제 practice.html에 있다.
  await open(`/units/unit0${unit}/practice.html`);
  assert.equal(await page.locator('#questions .question').count(),data.questions.length);
  assert.equal(await page.locator('#question-page, #previous-questions, #next-questions').count(),0);
  for(const q of data.questions){
   const hints=page.locator(`#${q.id} > details pre`);
   assert.equal(await hints.nth(0).textContent(),q.hint);
   assert.equal(await hints.nth(1).textContent(),q.hint2);
   assert.notEqual(q.hint2,q.explain);
  }
  console.log(`PASS unit ${unit}: all ${data.questions.length} questions and separate hints`);
 }
 await open('/units/unit02/widgets.html');
 await page.waitForFunction(()=>!!window.aipyUnderstanding);
 const originalTip=await page.locator('.lesson > .pai-note').textContent();
 const box=page.locator('[data-complete="u2-widgets"]');
 const badge=page.locator('.completion-badge');
 assert.equal(await badge.isVisible(),false);
 // 편집기는 소단원 페이지에서 예제 전용 페이지로 옮겨졌다(#101) — 여기서는 실습 카드 다음에 체크박스가 온다.
 assert.equal(await page.evaluate(()=>{
  const workspace=document.querySelector('#widgets-lab'),check=document.querySelector('label.completion');
  return !!(workspace.compareDocumentPosition(check)&Node.DOCUMENT_POSITION_FOLLOWING);
 }),true);
 await box.check();assert.equal(await badge.isVisible(),true);
 assert.equal(await page.locator('.lesson > .pai-note').textContent(),originalTip);
 await page.reload();await page.waitForFunction(()=>!!window.aipyUnderstanding);
 assert.equal(await box.isChecked(),true);assert.equal(await badge.isVisible(),true);
 await box.uncheck();assert.equal(await badge.isVisible(),false);
 const hard=page.locator('[data-understanding="hard"]');
 // 의견란은 항상 보이고(#97), '어려워요'일 때만 막힌 곳을 묻는 문구로 바뀐다.
 await hard.click();assert.equal(await page.locator('.hard-comment').isVisible(),true);
 assert.equal(await page.locator('.hard-comment-field').textContent(),'어디가 막혔나요?');
 await page.locator('[data-understanding="understood"]').click();
 assert.equal(await page.locator('.hard-comment').isVisible(),true);
 assert.notEqual(await page.locator('.hard-comment-field').textContent(),'어디가 막혔나요?');
 assert.equal(await page.locator('[data-understanding="understood"]').getAttribute('aria-pressed'),'true');
 await page.reload();await page.waitForFunction(()=>!!window.aipyUnderstanding);
 assert.equal(await page.locator('[data-understanding="understood"]').getAttribute('aria-pressed'),'true');
 assert.notEqual(await page.locator('.hard-comment-field').textContent(),'어디가 막혔나요?');
 console.log('PASS completion position, badge, understanding switches and reload');
 const q=JSON.parse(await readFile(new URL('../../web/data/unit2.json',import.meta.url))).questions.find(q=>q.id==='u2-q009');
 // 소단원 문제는 독립 페이지(q-{소단원id}.html)로 옮겨졌다(#106) — 여기서 문항이 뜨는지 확인한다.
 await open('/units/unit02/q-widgets.html');
 const topicTotal=JSON.parse(await readFile(new URL('../../web/data/unit2.json',import.meta.url))).questions.filter(x=>x.topic==='widgets').length;
 const total=await page.locator('#questions .question').count();
 assert.equal(total,topicTotal,'q-widgets.html shows exactly this topic\'s questions');
 await page.locator(`#${q.id} textarea`).fill(q.answer);
 await page.locator(`#${q.id} .primary`).click();
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 assert.match(await page.locator('#question-summary').textContent(),new RegExp(`남은 ${total-1}`));
 await page.locator(`#${q.id} .primary`).click();
 assert.equal(await page.evaluate(id=>window.aipyLearning.getState().answers[id].attempts,q.id),2);
 await page.selectOption('#question-status','done');
 assert.equal(await page.locator('#questions .question').count(),1);
 await page.selectOption('#question-status','todo');
 assert.equal(await page.locator('#questions .question').count(),total-1);
 await page.selectOption('#question-status','');
 await page.fill('#question-search','존재하지않는검색어');
 assert.equal(await page.locator('#questions .question').count(),0);
 assert.match(await page.locator('#questions').textContent(),/조건에 맞는 문제가 없습니다/);
 await page.fill('#question-search','');
 // '다시 풀기' 버튼은 제거됨(답안을 다시 제출하면 됨) — 원격 병합 검사로 이어간다.
 // 원격 병합도 기존 체크와 진행 표시를 갱신해야 합니다.
 await page.evaluate(id=>{
  const state=window.aipyLearning.getState();
  window.aipyLearning.applyRemote({...state,complete:{'u2-widgets':true},answers:{[id]:{status:'done'}}});
 },q.id);
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 await page.reload();await page.waitForFunction(()=>window.aipyLearning?.ready);
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 console.log('PASS progress on answer/filter/remote/reload and repeated attempts');
 // 완료 체크는 소단원 설명 페이지에 있다 — 원격 병합이 그 페이지에도 반영됐는지 확인한다.
 await open('/units/unit02/widgets.html');
 assert.equal(await badge.isVisible(),true);
 console.log('PASS remote-merged completion reflected on the lesson page');
 await open('/units/unit02/q-ui.html');
 const self=page.locator('#questions .question label.completion input').first();
 await self.check();assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 await self.uncheck();assert.equal(await page.locator('#question-progress').getAttribute('value'),'0');
 console.log('PASS written self-assessment progress');
 // 편집기가 있는 곳은 이제 예제 전용 페이지뿐이다(#101). 페이지를 열자마자 선택 UI 없이 코드가 채워져 있어야 한다.
 for(const [path,label] of [['/units/unit01/ex-reuse.html','Python 실행'],['/units/unit02/ex-layout-pack-tk.html','문법 확인']]){
  await open(path);
  assert.match(await page.locator('#run').textContent(),new RegExp(label));
  assert.match(await page.locator('.run-mode-guide').textContent(),/Python 실행.*문법 확인.*PC/);
  assert.equal(await page.locator('#example-select').count(),0);
  const code=await page.locator('#code-editor').inputValue();
  assert.ok(code && code.trim().length>0, `#code-editor should be pre-filled on ${path}`);
  await page.setViewportSize({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 }
 assert.deepEqual(errors,[]);
 console.log('PASS run modes, auto-filled editor, no selection UI and 390px mobile layout');
} finally {await browser.close();}
