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
  await open(`/units/unit0${unit}/index.html`);
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
 assert.equal(await page.evaluate(()=>{
  const lab=document.querySelector('#lab'),check=document.querySelector('label.completion');
  return !!(lab.compareDocumentPosition(check)&Node.DOCUMENT_POSITION_FOLLOWING);
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
 const total=await page.locator('#questions .question').count();
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
 page.once('dialog',dialog=>dialog.accept());
 await page.locator(`#${q.id} button`).filter({hasText:'다시 풀기'}).click();
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'0');
 // 원격 병합도 기존 체크와 진행 표시를 갱신해야 합니다.
 await page.evaluate(id=>{
  const state=window.aipyLearning.getState();
  window.aipyLearning.applyRemote({...state,complete:{'u2-widgets':true},answers:{[id]:{status:'done'}}});
 },q.id);
 assert.equal(await badge.isVisible(),true);
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 await page.reload();await page.waitForFunction(()=>window.aipyLearning?.ready);
 assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 console.log('PASS progress on answer/retry/filter/remote/reload and repeated attempts');
 await open('/units/unit02/ui.html');
 const self=page.locator('#questions .question label.completion input').first();
 await self.check();assert.equal(await page.locator('#question-progress').getAttribute('value'),'1');
 await self.uncheck();assert.equal(await page.locator('#question-progress').getAttribute('value'),'0');
 console.log('PASS written self-assessment progress');
 for(const [path,label] of [['/units/unit01/overview.html','Python 실행'],['/units/unit02/layout.html','문법 확인']]){
  await open(path);
  assert.match(await page.locator('#run').textContent(),new RegExp(label));
  assert.match(await page.locator('.run-mode-guide').textContent(),/Python 실행.*문법 확인.*PC/);
  await page.setViewportSize({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 }
 assert.deepEqual(errors,[]);
 console.log('PASS run modes, explanatory guide and 390px mobile layout');
} finally {await browser.close();}
