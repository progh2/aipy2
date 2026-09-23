'use strict';
/* 학습 UI와 localStorage. 클라우드 미러는 assets/sync.js가 붙습니다.
   훅: save(kind), window.aipyLearning.{getState,applyRemote,onLocalChange,key}.
   kind: complete|answer 즉시 동기화, code|journal|draft|nav 는 유휴·이탈. */
(() => {
const prefix=document.body.dataset.prefix||'', unit=Number(document.body.dataset.unit||0), KEY='aipy-lab-v1';
const pageTopic=document.body.dataset.topic||'';
const pageExample=document.body.dataset.example||'';
const pageLessons=(document.body.dataset.lessons||'').split(/\s+/).filter(Boolean);
if(unit && !pageTopic){
 const hash=location.hash.slice(1);
 if(hash && pageLessons.includes(hash)) location.replace(hash+'.html');
}
function resumeHref(raw){
 if(typeof raw!=='string') return '';
 const legacy=/^units\/unit0([1-4])\/index\.html#([a-z0-9-]+)$/.exec(raw);
 if(legacy){
  if(['lab','practice','gallery','simulator','journal'].includes(legacy[2]) || legacy[2].startsWith('u')) return raw;
  return `units/unit0${legacy[1]}/${legacy[2]}.html`;
 }
 if(/^units\/unit0[1-4]\/[a-z0-9-]+\.html(?:#[a-z0-9-]+)?$/.test(raw)) return raw;
 return '';
}
let state={version:1,complete:{},answers:{},journals:{},projects:{},last:''};
let storageWorks=true;
try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved && saved.version===1) state={...state,...saved};}catch{storageWorks=false;}
for(const key of ['complete','answers','journals','projects']) if(!state[key] || typeof state[key]!=='object' || Array.isArray(state[key])) state[key]={};
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el;};
// Five expressions have distinct learning roles; guidance remains readable as text.
const paiLabels={welcome:'반가워요',thinking:'생각 중',idea:'아하!',debug:'오류 탐정',celebrate:'해냈어요'};
function paiImage(mood,cls='pai-feedback-image'){
 const img=node('img',cls);img.src=prefix+`assets/mascot/pai-${mood}-v1.webp?v=girl2`;img.alt='';img.width=62;img.height=62;img.decoding='async';return img;
}
function paiFeedback(el,text,mood){
 const copy=node('div','pai-feedback-copy');copy.append(node('b','',`파이 · ${paiLabels[mood]}`),node('p','',text));
 el.replaceChildren(paiImage(mood),copy);el.classList.add('pai-feedback');el.dataset.paiMood=mood;
}
function paiGuide(mood,title,text){
 const box=$('#pai-run-guide');if(!box)return;
 box.dataset.paiMood=mood;const img=box.querySelector('img');img.src=prefix+`assets/mascot/pai-${mood}-v1.webp?v=girl2`;img.alt='';
 box.querySelector('.pai-label').textContent=`파이의 실습 안내 · ${paiLabels[mood]}`;
 box.querySelector('strong').textContent=title;box.querySelector('p').textContent=text;
}
const moodButtons=$$('[data-pai-preview]');
if(moodButtons.length){
 const hero=$('.pai-hero'),toggle=$('#pai-auto'),motion=matchMedia('(prefers-reduced-motion: reduce)');
 let index=0,automatic=!motion.matches,moodTimer;
 function showMood(next){
  index=next;const button=moodButtons[index],mood=button.dataset.paiPreview,img=$('.pai-hero-image');
  img.src=prefix+`assets/mascot/pai-${mood}-v1.webp?v=girl2`;img.alt=button.dataset.paiAlt;
  $('#pai-mood-title').textContent=paiLabels[mood];$('#pai-mood-description').textContent=button.dataset.paiDescription;
  moodButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 }
 function scheduleMood(){
  clearTimeout(moodTimer);toggle.setAttribute('aria-pressed',String(automatic));
  toggle.textContent=automatic?'자동 전환 일시정지':'자동 전환 시작';
  if(automatic&&!document.hidden&&!hero.matches(':hover')&&!hero.contains(document.activeElement))
   moodTimer=setTimeout(()=>{showMood((index+1)%moodButtons.length);scheduleMood();},6000);
 }
 moodButtons.forEach((button,i)=>button.onclick=()=>{showMood(i);scheduleMood();});
 toggle.onclick=()=>{automatic=!automatic;scheduleMood();};
 for(const event of ['mouseenter','mouseleave','focusin'])hero.addEventListener(event,scheduleMood);
 hero.addEventListener('focusout',()=>setTimeout(scheduleMood,0));
 document.addEventListener('visibilitychange',scheduleMood);
 motion.addEventListener('change',()=>{automatic=!motion.matches;scheduleMood();});
 scheduleMood();
}
let toastTimer;
function toast(text){$('#toast').textContent=text;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').textContent='',4200);}
function save(kind){
 try{localStorage.setItem(KEY,JSON.stringify(state));}
 catch{if(storageWorks){toast('저장 공간에 접근할 수 없습니다. 기록을 내보내세요.');storageWorks=false;}}
 if(kind!=='remote'&&kind!=='quiet'){
  try{if(typeof window.aipyLearning.onLocalChange==='function')window.aipyLearning.onLocalChange(kind||'save');}catch{}
 }
}
function applyRemote(next){
 if(!next || typeof next!=='object')return;
 for(const key of ['complete','answers','journals','projects']){
  if(next[key] && typeof next[key]==='object' && !Array.isArray(next[key])) state[key]=next[key];
 }
 if(typeof next.last==='string') state.last=next.last;
 if(next.times && typeof next.times==='object') state.times=next.times;
 save('remote');
 updateProgress();
 $$('[data-complete]').forEach(box=>{
  box.checked=!!state.complete[box.dataset.complete];
  if(typeof box._paintComplete==='function') box._paintComplete();
 });
 $$('[data-journal]').forEach(area=>{area.value=state.journals[area.dataset.journal]||'';});
 if($('#resume')){const href=resumeHref(state.last);if(href)$('#resume').href=href;}
 renderRailTodo();
 if(typeof window.aipyLearning._refreshUnit==='function') window.aipyLearning._refreshUnit();
}
let lastError='';
function rememberError(text){lastError=typeof text==='string'?text.replace(/\s+/g,' ').trim().slice(0,300):'';}
window.aipyLearning={ready:false,key:KEY,saveLocal(){save('leave');},saveLocalQuiet(){save('quiet');},getState(){return state;},applyRemote,onLocalChange:null,selectExample(){},currentExample(){return null;},lastError(){return lastError;},lastCheck:null};
window.addEventListener('pagehide',()=>{try{window.aipyLearning.saveLocal();}catch{}});
function download(name,content,type='text/plain;charset=utf-8'){const url=URL.createObjectURL(new Blob([content],{type}));const a=node('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);}
async function copy(text){try{await navigator.clipboard.writeText(text);toast('복사했습니다.');}catch{const area=node('textarea');area.value=text;document.body.append(area);area.select();const ok=document.execCommand('copy');area.remove();toast(ok?'복사했습니다.':'복사가 제한되었습니다. 코드를 선택하여 복사하세요.');}}
function updateProgress(){for(const item of $$('[data-unit-progress]')){const u=Number(item.dataset.unitProgress),total=Number(item.dataset.total)||1;const count=Object.entries(state.complete).filter(([k,v])=>k.startsWith(`u${u}-`)&&v).length;const value=Math.min(100,Math.round(count/total*100));item.textContent=`${value}%`;$$(`[data-unit-bar="${u}"]`).forEach(e=>e.value=value);}}
updateProgress();
if(!storageWorks)toast('기록을 불러오지 못했습니다. 이 세션의 기록은 내보내기로 보관하세요.');
if($('#resume')){const href=resumeHref(state.last);if(href)$('#resume').href=href;}
$$('[data-export]').forEach(b=>b.addEventListener('click',()=>download('aipy-learning-record.json',JSON.stringify(state,null,2),'application/json')));
$$('[data-import]').forEach(input=>input.addEventListener('change',async()=>{
 try{
  const f=input.files[0];if(!f)return;if(f.size>6000000)throw Error('6MB 이하 기록 파일을 선택하세요.');
  const data=JSON.parse(await f.text());if(data.version!==1 || !['complete','answers','journals','projects'].every(k=>data[k]&&typeof data[k]==='object'&&!Array.isArray(data[k])))throw Error('올바른 학습 기록 파일이 아닙니다.');
  if(!confirm('현재 브라우저 기록을 이 파일의 기록으로 바꿀까요?'))return;
  state={version:1,complete:data.complete,answers:data.answers,journals:data.journals,projects:data.projects,last:typeof data.last==='string'?data.last:''};save('import');location.reload();
 }catch(error){toast('불러오기 실패: '+error.message);}finally{input.value='';}
}));
$$('[data-clear]').forEach(b=>b.addEventListener('click',()=>{if(confirm('이 실습실의 코드·풀이·저널 기록을 지울까요? 먼저 내보내기를 권장합니다.')){try{localStorage.removeItem(KEY);}catch{}location.reload();}}));
 $$('[data-complete]').forEach(box=>{
 box.checked=!!state.complete[box.dataset.complete];
 // 체크 시 멀리 있는 마스코트 팁을 바꿔치기하던 동작이 '이상한 표시'로 보고되어(#88)
 // 라벨 옆 인라인 배지로 교체했다. 화면의 다른 곳은 건드리지 않는다.
 const label=box.closest('label.completion');
 const badge=node('span','completion-badge','✔ 완료로 표시했어요');
 if(label)label.append(badge);
 function showCompletion(){badge.hidden=!box.checked;}
 box._paintComplete=showCompletion;
 showCompletion();box.addEventListener('change',()=>{state.complete[box.dataset.complete]=box.checked;save('complete');updateProgress();showCompletion();renderRailTodo();});
});
$$('[data-journal]').forEach(area=>{area.value=state.journals[area.dataset.journal]||'';area.addEventListener('input',()=>{state.journals[area.dataset.journal]=area.value;save('journal');});});
if($('#download-journal'))$('#download-journal').onclick=()=>{let text=`# ${unit}단원 학습 저널\n\n작성일: ${new Date().toLocaleDateString('ko-KR')}\n`;for(const [key,title]of [['learn','이해한 개념'],['error','오류와 해결 근거'],['next','시험 결과와 다음 도전']])text+=`\n## ${title}\n\n${state.journals[`u${unit}-${key}`]||''}\n`;download(`unit${unit}-journal.md`,text);};
if(!unit){window.aipyLearning.ready=true;document.dispatchEvent(new CustomEvent('aipy:learning-ready'));return;}
const hasLab=Boolean($('#lab')), hasPractice=Boolean($('#practice')), hasRail=Boolean($('aside.rail'));
let data, currentId, files={},fileName, worker=null,running=false,timer,jobResolve,jobOutput,exampleDirty=false;
function markCode(){exampleDirty=true;stash();}
function remember(){
 if(pageTopic){state.last=`units/unit0${unit}/${pageTopic}.html`;save('nav');return;}
 const id=location.hash.slice(1);
 if(id && pageLessons.includes(id)){location.replace(id+'.html');return;}
 if(id && /^[a-z0-9-]+$/.test(id)) state.last=`units/unit0${unit}/index.html#${id}`;
 else state.last=`units/unit0${unit}/index.html`;
 save('nav');
}
window.addEventListener('hashchange',remember);remember();
function setStopDisabled(v){const b=$('#stop');if(b)b.disabled=v;}
function stop(reason='실행을 중지했습니다.'){
 if(worker)worker.terminate();worker=null;clearTimeout(timer);
 if(jobOutput)jobOutput(reason+'\n');
 paiGuide('thinking','잠시 멈추고 조건을 살펴봐요.','반복이 끝나는 조건을 확인하고, 수정한 뒤 다시 실행하세요.');
 if(jobResolve)jobResolve({ok:false,stopped:true});
 jobResolve=null;jobOutput=null;running=false;setStopDisabled(true);
}
function execute(payload,onOutput){
 if(running){toast('현재 실행을 마치거나 중지한 뒤 다시 실행하세요.');return Promise.resolve({ok:false,busy:true});}
 running=true;setStopDisabled(false);
 return new Promise(resolve=>{
  jobResolve=resolve;jobOutput=onOutput;
  if(!worker)worker=new Worker(prefix+'assets/python-worker.js?v=science1');
  clearTimeout(timer);timer=setTimeout(()=>stop('실행 엔진 준비 시간이 초과되었습니다. 네트워크를 확인하고 다시 실행하세요.'),180000);
  worker.onmessage=({data:m})=>{
   if(m.type==='loading')onOutput(m.text+'\n');
   if(m.type==='ready'){clearTimeout(timer);timer=setTimeout(()=>stop('30초 실행 제한에 도달했습니다. 반복 조건을 확인하세요.'),30000);}
   if(m.type==='stdout')onOutput(m.text);
   if(m.type==='done'){clearTimeout(timer);running=false;setStopDisabled(true);if(m.error){onOutput(m.error+'\n');rememberError(m.error);}else if(m.ok)rememberError('');jobResolve=null;jobOutput=null;resolve(m);}
  };
  worker.onerror=e=>{onOutput('실행 오류: '+e.message+'\n');stop('실행 엔진을 다시 준비합니다.');};
  worker.postMessage(payload);
 });
}
if($('#stop'))$('#stop').onclick=()=>stop();
function validName(name){return typeof name==='string' && /^[\w.-]+(?:\/[\w.-]+)*$/.test(name) && !name.split('/').some(p=>p==='.'||p==='..') && name.length<150;}
function stash(){if(!currentId||!exampleDirty)return;files[fileName]=$('#code-editor').value;const prev=state.projects[currentId]&&typeof state.projects[currentId]==='object'?state.projects[currentId]:{};state.projects[currentId]={...prev,files,entry:$('#entry-file').value,stdin:$('#stdin').value,args:$('#argv').value};save('code');}
function renderFiles(){
 const tree=$('#file-tree');tree.replaceChildren();
 Object.keys(files).sort().forEach(name=>{const b=node('button',name===fileName?'active':'',name);b.setAttribute('aria-pressed',String(name===fileName));b.type='button';b.onclick=()=>{try{stash();fileName=name;const ed=$('#code-editor');ed.value=files[name];ed.dispatchEvent(new Event('input',{bubbles:true}));$('#file-name').textContent=name;renderFiles();}catch(error){console.error('[lab] 파일 전환 실패',name,error);toast('파일을 여는 중 문제가 생겼습니다: '+error.message);}};tree.append(b);});
 const entry=$('#entry-file'),old=entry.value;entry.replaceChildren();Object.keys(files).filter(n=>n.endsWith('.py')).forEach(n=>{const opt=node('option','',n);opt.value=n;entry.append(opt);});if(files[old]!==undefined)entry.value=old;
 $('#file-name').textContent=fileName;
}
function selectExample(id,scroll=false,workspace=null){
 if(!hasLab)return;
 const select=$('#example-select');
 if(running){if(select)select.value=currentId;toast('현재 실행을 마치거나 중지한 뒤 예제를 바꾸세요.');return;}
 if(!data.examples[id])return;
 const lab=$('#lab'),active=lab.closest('[data-workspace]');
 // 예제 전용 페이지에는 .lesson-workspace가 없으므로 owner를 찾지 못하면 #lab은 제자리에 둔다.
 const owner=workspace || (active && data.lessons.find(l=>l.id===active.dataset.workspace)?.examples.includes(id) ? active : $$('[data-workspace]').find(el=>data.lessons.find(l=>l.id===el.dataset.workspace)?.examples.includes(id)));
 if(owner){const mount=owner.querySelector('.editor-mount');if(mount)mount.append(lab);const h2=$('#lab h2');if(h2)h2.textContent='바로 실습 · '+data.lessons.find(l=>l.id===owner.dataset.workspace).title;}
 $$('[data-example]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.example===id&&b.closest('[data-workspace]')===owner)));
if(currentId)stash();currentId=id;exampleDirty=false;const ex=data.examples[id],saved=state.projects[id];
 files=JSON.parse(JSON.stringify(ex.files));
 if(saved && saved.files && typeof saved.files==='object' && Object.entries(saved.files).every(([n,s])=>validName(n)&&typeof s==='string') && Object.keys(saved.files).some(n=>n.endsWith('.py')))files={...saved.files};
 fileName=files[ex.entry]!==undefined?ex.entry:Object.keys(files)[0];
 if(select)select.value=id;$('#code-editor').value=files[fileName];renderFiles();
 $('#entry-file').value=saved?.entry&&files[saved.entry]!==undefined?saved.entry:ex.entry;
 $('#stdin').value=saved?.stdin??ex.stdin??'';$('#argv').value=saved?.args??ex.args??'[]';if(!$('#argv').value)$('#argv').value='[]';
 $('#run-mode').textContent=ex.mode==='web'?'브라우저 Python 실행':'PC Python 실습';
 $('#run').textContent=ex.mode==='web'?'▶ Python 실행':'Python 문법 확인';
 $('#check-example').disabled=!ex.checks;
 $('#check-example').textContent=ex.checks?'입력·조건 검사':'PC 실행으로 동작 점검';
 const deps=(ex.files['requirements.txt']||'').split(/\s+/).filter(Boolean).join(' ')||(id.includes('pyside')?'PySide6':id.includes('pyqt')?'PyQt6':/(^|-)wx(-|$)/.test(id)||id.endsWith('-wx')?'wxPython':id.includes('kivy')?'Kivy':'');
 const installNote=deps?` 이 예제는 외부 라이브러리가 필요해 설치 없이는 동작하지 않습니다. 먼저 python -m pip install ${deps} 를 실행하세요.`:(id.includes('tk')?' tkinter는 파이썬에 기본 포함되어 별도 설치가 필요 없습니다. 창이 안 뜨면 파이썬 설치 시 tcl/tk 옵션을 확인하세요.':' 표준 라이브러리만 사용하므로 별도 설치가 필요 없습니다.');
 $('#example-note').textContent=(ex.note||'')+(ex.mode==='pc'?' 이 코드는 PC에서 실행하세요. 웹에서는 Python 문법만 확인합니다. ZIP 다운로드 후 예제 폴더를 VS Code로 열고 python main.py를 실행하세요.'+installNote:' 파일을 오가며 편집한 뒤 실행 파일을 선택하세요. 각 실행은 새 가상 프로젝트에서 시작합니다.');
 $('#plot-output').replaceChildren();
 $('#output').textContent=`${ex.title}\n${ex.mode==='web'?'실행 결과가 여기에 표시됩니다.':'문법 검사는 패키지 설치·데이터·장치·실제 프로그램 동작까지 검사하지 않습니다.'}`;
 paiGuide('thinking',ex.mode==='web'?'실행 전에 결과를 먼저 예상해 볼까요?':'웹에서 확인한 뒤, PC에서도 시험해요.',ex.mode==='web'?'어떤 파일을 실행하나요? 입력값을 바꾸면 어떤 결과가 나올지 먼저 적어 보세요.':'문법 확인은 첫 단계예요. 다운로드한 예제를 실행하고 입력·결과·오류 처리를 확인하세요.');
 if(scroll)$('#lab').scrollIntoView({behavior:'smooth'});
}
if(hasLab){
$('#code-editor').addEventListener('input',markCode);
$('#code-editor').addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();const a=e.target,s=a.selectionStart,end=a.selectionEnd;a.setRangeText('    ',s,end,'end');markCode();}});
for(const id of ['stdin','argv','entry-file'])$('#'+id).addEventListener('change',markCode);
if($('#example-select'))$('#example-select').onchange=e=>selectExample(e.target.value,true);
$('#add-file').onclick=()=>{const name=prompt('파일 경로를 입력하세요. 예: utils.py 또는 nature/bird.py');if(name===null)return;if(!validName(name)||Object.hasOwn(files,name))return toast('중복되지 않는 상대 경로를 입력하세요.');markCode();files[name]=name.endsWith('.py')?'# 새 기능을 작성하세요.\n':'';fileName=name;$('#code-editor').value=files[name];renderFiles();markCode();};
$('#delete-file').onclick=()=>{if(Object.keys(files).length===1 || (fileName.endsWith('.py')&&Object.keys(files).filter(n=>n.endsWith('.py')).length===1))return toast('Python 파일 하나는 남겨 두세요.');if(!confirm(fileName+' 파일을 지울까요?'))return;delete files[fileName];fileName=Object.keys(files)[0];$('#code-editor').value=files[fileName];renderFiles();markCode();};
$('#copy-code').onclick=()=>copy($('#code-editor').value);
$('#download-file').onclick=()=>download(fileName.split('/').pop(),$('#code-editor').value);
$('#reset-code').onclick=()=>{if(running)return toast('실행을 마치거나 중지한 뒤 원본으로 복원하세요.');if(confirm('이 예제의 수정 내용을 원본으로 되돌릴까요?')){const id=currentId;currentId=null;delete state.projects[id];save('code');selectExample(id);}};
}
async function runExample(check=false){
 if(running)return toast('현재 실행을 마치거나 중지하세요.');stash();let args;
 try{args=JSON.parse($('#argv').value||'[]');if(!Array.isArray(args)||!args.every(x=>typeof x==='string'))throw Error();}catch{return toast('실행 인자는 ["값1", "값2"] 형식으로 입력하세요.');}
 const ex=data.examples[currentId],entry=$('#entry-file').value;
 if(!entry || !files[entry])return toast('실행할 Python 파일을 선택하세요.');
 const out=$('#output');out.textContent='';$('#plot-output').replaceChildren();
 paiGuide('thinking','예상한 결과와 실제 출력을 비교할 준비!','실행이 끝나면 출력값뿐 아니라 실행 순서도 확인해 보세요.');
 const result=await execute({files,entry,stdin:$('#stdin').value,args,checks:check?ex.checks:'',syntax:ex.mode!=='web'},s=>out.textContent+=s);
 if(result.images)for(const picture of result.images){const fig=node('figure'),img=node('img');img.src='data:image/png;base64,'+picture.data;img.alt='Python 실행 결과: '+picture.name;const caption=node('figcaption','',picture.name+' · 실제 실행 결과');const link=node('a','','PNG 저장');link.href=img.src;link.download=picture.name;fig.append(img,caption,link);$('#plot-output').append(fig);}
 if(result.ok)out.textContent+='\n실행 완료'+(check?' · 준비된 검사 통과':'')+'\n';
 const saved=state.projects[currentId]||{};
 const checkInfo={type:'example',id:currentId,ok:!!result.ok,checked:!!check,output:out.textContent,attempts:(Number(saved.attempts)||0)+(check?1:0)};
 if(check){state.projects[currentId]={...saved,files,entry,stdin:$('#stdin').value,args:$('#argv').value,lastOk:!!result.ok,lastOutput:out.textContent,attempts:checkInfo.attempts};save('answer');}
 window.aipyLearning.lastCheck=checkInfo;document.dispatchEvent(new CustomEvent('aipy:checked',{detail:checkInfo}));
 if(result.ok){
  if(ex.mode!=='web')paiGuide('idea','문법 확인을 통과했어요. 다음은 실제 동작!', 'PC에서 예제를 실행하고 입력·출력·오류 처리를 직접 확인하세요.');
  else if(check)paiGuide('celebrate','준비된 조건을 통과했어요!', '입력값을 하나 더 바꾸어 보고, 왜 이 결과가 나오는지 내 말로 설명하세요.');
  else paiGuide('idea','예상했던 결과가 나왔나요?', '출력의 이유를 설명한 다음 숫자나 조건을 하나 바꾸어 다시 실험해 보세요.');
 }else if(!result.stopped && !result.busy){if(!lastError)rememberError((out.textContent||'').trim().split('\n').filter(Boolean).slice(-1)[0]||'');paiGuide('debug','오류는 원인을 찾을 단서예요.', '마지막 오류 줄 → 파일명과 줄 번호 → 사용한 이름과 값을 순서대로 확인하세요.');}
}
if(hasLab){$('#run').onclick=()=>runExample(false);$('#check-example').onclick=()=>runExample(true);}
// Dependency-free ZIP writer (stored entries, UTF-8 names, CRC32).
function zipFiles(items){
 const encoder=new TextEncoder(),table=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
 const chunks=[],central=[];let offset=0;
 function block(length,fields){const b=new Uint8Array(length),v=new DataView(b.buffer);for(const [at,val,size]of fields)size===2?v.setUint16(at,val,true):v.setUint32(at,val>>>0,true);return b;}
 for(const [path,text]of Object.entries(items)){
  const name=encoder.encode(path),bytes=encoder.encode(text);let crc=0xffffffff;for(const b of bytes)crc=table[(crc^b)&255]^(crc>>>8);crc=(crc^0xffffffff)>>>0;
  const local=block(30,[[0,0x04034b50,4],[4,20,2],[6,0x800,2],[14,crc,4],[18,bytes.length,4],[22,bytes.length,4],[26,name.length,2]]);
  chunks.push(local,name,bytes);
  const directory=block(46,[[0,0x02014b50,4],[4,20,2],[6,20,2],[8,0x800,2],[16,crc,4],[20,bytes.length,4],[24,bytes.length,4],[28,name.length,2],[42,offset,4]]);
  central.push(directory,name);offset+=local.length+name.length+bytes.length;
 }
 const size=central.reduce((s,b)=>s+b.length,0),count=Object.keys(items).length;
 return new Blob([...chunks,...central,block(22,[[0,0x06054b50,4],[8,count,2],[10,count,2],[12,size,4],[16,offset,4]])],{type:'application/zip'});
}
if(hasLab)$('#download-project').onclick=()=>{stash();const ex=data.examples[currentId],all={...files};let dep=currentId.includes('pyside')?'PySide6':currentId.includes('pyqt')?'PyQt6':currentId.includes('-wx')?'wxPython':currentId.includes('kivy')?'Kivy':currentId==='thirdparty'?'numpy':'';if(dep&&!all['requirements.txt'])all['requirements.txt']=dep+'\n';all['실행안내.md']=`# ${ex.title}\n\n이 폴더를 VS Code로 열고 python ${$('#entry-file').value}로 실행하세요.\n${dep?'가상환경에서 python -m pip install -r requirements.txt를 먼저 실행하세요.':''}\n\n${ex.note||''}\n`;download(currentId+'.zip',zipFiles(all),'application/zip');};
// Question bank: keep attempts, answers and self-assessment separately.
let filtered=[];
// 문항은 전부 한 번에 보여 준다 — 페이지로 나누면 1쪽만 풀고 끝난 줄 아는 학생이 있었다(#90).
function norm(s){return String(s??'').trim().replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/\s+/g,'').replace(/'/g,'"');}
function answerRecord(q){return state.answers[q.id]||{};}
function storeAnswer(q,patch){state.answers[q.id]={...answerRecord(q),...patch};save(patch.status!==undefined||patch.attempts!==undefined?'answer':'draft');updateQuestionSummary();renderRailTodo();}
function questionCard(q){
 const card=node('article','question');card.id=q.id;
 card.append(node('div','question-meta',`${q.id} · ${q.kind} · ${q.ref}`),node('h3','',q.prompt));
 const record=answerRecord(q);let input,order,answer=()=>'';
 if(q.kind==='선택'){
  const options=node('div','options');for(const [i,text]of q.options.entries()){const label=node('label'),radio=node('input');radio.type='radio';radio.name=q.id;radio.value=text;radio.checked=record.value===text;radio.addEventListener('change',()=>storeAnswer(q,{value:text}));label.append(radio,node('span','',text));options.append(label);}card.append(options);answer=()=>card.querySelector('input:checked')?.value||'';
 }else if(q.kind==='순서'){
  order=Array.isArray(record.value)&&record.value.length===q.answer.length&&q.answer.every(x=>record.value.includes(x))?[...record.value]:[...q.answer.slice(1),q.answer[0]];
  const list=node('ol','order-list');
  // 드래그 앤 드롭(마우스: HTML5 DnD, 터치·펜: pointer 이벤트)으로도 순서를 바꾼다(#94). ▲▼ 버튼은 키보드 접근용으로 유지.
  let dragFrom=-1,dropAt=null;// dropAt: {index, before}
  function move(from,to){if(from<0||to<0||from===to)return;const [item]=order.splice(from,1);order.splice(to,0,item);storeAnswer(q,{value:order});draw();}
  function clearMarks(){for(const el of list.querySelectorAll('.drop-before,.drop-after,.dragging'))el.classList.remove('drop-before','drop-after','dragging');}
  function markTarget(li,clientY){const rect=li.getBoundingClientRect(),before=clientY<rect.top+rect.height/2,index=Number(li.dataset.index);for(const el of list.querySelectorAll('.drop-before,.drop-after'))el.classList.remove('drop-before','drop-after');if(index===dragFrom){dropAt=null;return;}li.classList.add(before?'drop-before':'drop-after');dropAt={index,before};}
  function finishDrop(){const from=dragFrom;let to=dropAt?dropAt.index+(dropAt.before?0:1):-1;if(to>from)to--;dragFrom=-1;dropAt=null;clearMarks();move(from,to);}
  function draw(){list.replaceChildren();order.forEach((text,i)=>{
   const li=node('li');li.dataset.index=i;li.draggable=true;
   const handle=node('span','order-handle','⋮⋮');handle.setAttribute('aria-hidden','true');handle.title='끌어서 순서 바꾸기';
   li.append(handle,node('span','',text));
   for(const [label,diff]of [['↑',-1],['↓',1]]){const b=node('button','',label);b.setAttribute('aria-label',text+(diff<0?' 위로':' 아래로'));b.disabled=i+diff<0||i+diff>=order.length;b.onclick=()=>{[order[i],order[i+diff]]=[order[i+diff],order[i]];storeAnswer(q,{value:order});draw();};li.append(b);}
   // 마우스: HTML5 drag & drop
   li.addEventListener('dragstart',e=>{if(e.target.tagName==='BUTTON'){e.preventDefault();return;}dragFrom=i;dropAt=null;li.classList.add('dragging');e.dataTransfer.effectAllowed='move';try{e.dataTransfer.setData('text/plain',String(i));}catch(_){}});
   li.addEventListener('dragover',e=>{if(dragFrom<0)return;e.preventDefault();e.dataTransfer.dropEffect='move';markTarget(li,e.clientY);});
   li.addEventListener('dragleave',e=>{if(!li.contains(e.relatedTarget))li.classList.remove('drop-before','drop-after');});
   li.addEventListener('drop',e=>{if(dragFrom<0)return;e.preventDefault();markTarget(li,e.clientY);finishDrop();});
   li.addEventListener('dragend',()=>{dragFrom=-1;dropAt=null;clearMarks();});
   // 터치·펜: 핸들에서 pointer 이벤트로 처리(HTML5 DnD가 모바일에서 잘 안 되므로)
   handle.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;e.preventDefault();dragFrom=i;dropAt=null;li.classList.add('dragging');try{handle.setPointerCapture(e.pointerId);}catch(_){}});
   handle.addEventListener('pointermove',e=>{if(dragFrom<0||e.pointerType==='mouse')return;e.preventDefault();const target=document.elementFromPoint(e.clientX,e.clientY)?.closest('li');if(target&&target.parentElement===list)markTarget(target,e.clientY);});
   handle.addEventListener('pointerup',e=>{if(dragFrom<0||e.pointerType==='mouse')return;e.preventDefault();finishDrop();});
   handle.addEventListener('pointercancel',()=>{if(dragFrom<0)return;dragFrom=-1;dropAt=null;clearMarks();});
   list.append(li);});}
  draw();card.append(list);answer=()=>order;
 }else{
  const label=node('label','',q.starter?'Python 코드':q.kind==='서술'?'내 설명':'내 답안');input=node('textarea',q.starter?'code-answer':'');input.rows=q.starter?6:q.kind==='서술'?4:2;input.spellcheck=false;input.value=typeof record.value==='string'?record.value:q.starter||'';input.addEventListener('input',()=>storeAnswer(q,{value:input.value}));label.append(input);card.append(label);answer=()=>input.value;
 }
 const actions=node('div','actions'),check=node('button','primary',q.kind==='서술'?'설명 저장':q.starter?'실행하고 검사':'답 확인');
 actions.append(check);card.append(actions);
 const feedback=node('div','feedback'+(record.status==='done'?' success':record.status==='retry'?' retry':''),record.feedback||'먼저 스스로 풀어 보세요.');feedback.setAttribute('role','status');paiFeedback(feedback,record.feedback||'실행하기 전에 결과를 예상하세요. 막히면 힌트를 하나씩 열어 보세요.',record.status==='done'?'celebrate':record.status==='retry'?'debug':'thinking');card.append(feedback);
 function detail(title,text){const d=node('details'),s=node('summary','',title);d.append(s,node('pre','',text));card.append(d);}
 detail('힌트 1 · 방향 잡기',q.hint);detail('힌트 2 · 구체적 단서',q.hint2);detail('정답 예시와 해설',(Array.isArray(q.answer)?q.answer.join('\n'):q.answer)+'\n\n'+q.explain);
 if(q.kind==='서술'){
  const self=node('label','completion'),box=node('input');box.type='checkbox';box.checked=record.status==='done';self.append(box,node('span','','해설과 비교하고 근거를 포함했는지 스스로 점검했습니다.'));box.onchange=()=>{storeAnswer(q,{value:answer(),status:box.checked?'done':'todo',feedback:box.checked?'자기 점검 완료 · 자동 채점 점수가 아닙니다.':'자기 점검을 진행하세요.'});paiFeedback(feedback,box.checked?'설명과 근거를 스스로 확인했어요. 다른 예에도 적용해 보세요.':'해설과 내 설명을 비교하며 빠진 근거를 채워 보세요.',box.checked?'celebrate':'thinking');};card.append(self);
 }
 check.onclick=async()=>{
  const value=answer();if(!value || (typeof value==='string'&&!value.trim()))return toast('답안을 먼저 입력하세요.');
  if(running&&q.starter)return toast('다른 실행을 마치거나 중지하세요.');
  if(q.kind==='서술'){storeAnswer(q,{value,feedback:'설명을 저장했습니다. 해설과 비교한 뒤 자기 점검하세요.'});paiFeedback(feedback,'설명을 저장했습니다. 해설과 비교하며 근거가 충분한지 확인하세요.','idea');return;}
  check.disabled=true;let ok=false,trace='';
  if(q.starter){feedback.textContent='';const result=await execute({files:{'main.py':value},entry:'main.py',args:[],stdin:'',checks:q.checks},s=>{trace+=s;feedback.textContent=trace;});if(result.busy){check.disabled=false;return;}ok=!!(result.ok&&result.checked);}
  else ok=q.kind==='순서'?JSON.stringify(value)===JSON.stringify(q.answer):norm(value)===norm(q.answer);
  const text=ok?'확인 완료! '+q.explain:'다시 살펴보세요. '+q.hint+(q.starter?'\n'+trace:'\n다른 올바른 표현일 수 있으니 정답 예시와 비교하세요.');
  feedback.className='feedback '+(ok?'success':'retry');paiFeedback(feedback,text,ok?'celebrate':'debug');
  if(ok)rememberError('');else rememberError(q.starter?(trace.trim().split('\n').filter(Boolean).slice(-1)[0]||text):text);
  const attempts=(answerRecord(q).attempts||0)+1;
  storeAnswer(q,{value,status:ok?'done':'retry',attempts,feedback:text});check.disabled=false;
  const checkInfo={type:'question',id:q.id,ok,checked:true,output:text,attempts};
  window.aipyLearning.lastCheck=checkInfo;document.dispatchEvent(new CustomEvent('aipy:checked',{detail:checkInfo}));
 };
 if(q.starter){const copyButton=node('button','','코드 복사');copyButton.onclick=()=>copy(answer());actions.append(copyButton);const stopButton=node('button','','실행 중지');stopButton.onclick=()=>{if(running)stop();};actions.append(stopButton);}
 return card;
}
function topicQuestions(){
 const filter=$('#practice') && $('#practice').dataset.topicFilter;
 return data.questions.filter(q=>!filter || q.topic===filter);
}
function updateQuestionSummary(){
 if(!hasPractice||!data)return;
 const pool=topicQuestions(),done=pool.filter(q=>answerRecord(q).status==='done').length;
 $('#question-summary').textContent=`${pool.length===data.questions.length?'전체':'이 주제'} ${pool.length}문제 · 완료 ${done} · 남은 ${pool.length-done} · 현재 표시 ${filtered.length}문제`;
 const progress=$('#question-progress');progress.max=pool.length||1;progress.value=done;
}
function renderQuestions(){
 if(!hasPractice)return;
 const kind=$('#question-kind').value,status=$('#question-status').value,search=$('#question-search').value.trim().toLowerCase();
 const pool=topicQuestions();
 filtered=pool.filter(q=>(!kind||q.kind===kind)&&(!search||`${q.prompt} ${q.topic} ${q.ref}`.toLowerCase().includes(search))&&(!status||(status==='todo'?!['done','retry'].includes(answerRecord(q).status):answerRecord(q).status===status)));
 $('#questions').replaceChildren(...filtered.map(questionCard));
 if(!filtered.length)$('#questions').append(node('p','note','조건에 맞는 문제가 없습니다. 유형·상태·검색 조건을 바꿔 보세요.'));
 updateQuestionSummary();
}
if(hasPractice){
 for(const id of ['question-kind','question-status'])$('#'+id).onchange=()=>renderQuestions();$('#question-search').oninput=()=>renderQuestions();
}
function initGUI(){
 if($('#demo-greet')){
  $('#demo-greet').onclick=()=>{const name=$('#demo-name').value.trim()||'여러분';$('#demo-result').textContent=`${name}님, 안녕하세요!`;$('#event-log').textContent='클릭 발생 → greet 호출 → 입력값 읽기 → 라벨 변경';};
  $('#demo-reset').onclick=()=>{$('#demo-name').value='';$('#demo-result').textContent='이름을 입력하세요.';$('#event-log').textContent='클릭 발생 → reset 호출 → 입력과 출력 초기화';};
 }
 if($('#demo-layout')) $('#demo-layout').onchange=e=>$('#layout-preview').className=e.target.value;
 if($('#demo-memo')){
  function stats(){const text=$('#demo-memo').value;$('#demo-stats').textContent=`${text.length}자 · ${text?text.split('\n').length:0}줄`;}$('#demo-memo').oninput=stats;
  $('#demo-open').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>2000000)throw Error('2MB 이하 텍스트를 선택하세요.');$('#demo-memo').value=await f.text();stats();}catch(error){toast(error.message);}finally{e.target.value='';}};
  $('#demo-save').onclick=()=>download('memo.txt',$('#demo-memo').value);
  $('#demo-new').onclick=()=>{if(!$('#demo-memo').value||confirm('현재 메모 내용을 지우고 새 문서를 시작할까요?')){$('#demo-memo').value='';stats();}};
 }
 if($('#compare-select') && data.pairs){
  function compare(){const [tk,qt]=data.pairs[Number($('#compare-select').value)];$('#compare-tk').textContent=data.examples[tk].files['main.py'];$('#compare-qt').textContent=data.examples[qt].files['main.py'];}
  $('#compare-select').onchange=compare;compare();
  $$('[data-view]').forEach(b=>b.onclick=()=>{$$('[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));const v=b.dataset.view;$$('[data-side]').forEach(x=>x.hidden=v!=='both'&&x.dataset.side!==v);$('#compare').classList.toggle('single',v!=='both');});
 }
}
if(!hasLab && !hasPractice && !hasRail){
 window.aipyLearning.ready=true;
 document.dispatchEvent(new CustomEvent('aipy:learning-ready'));
}else fetch(prefix+`data/unit${unit}.json`).then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(d=>{
 data=d;
 renderRailTodo();
 const lesson=pageTopic && data.lessons.find(l=>l.id===pageTopic);
 const exampleIds=(lesson && lesson.examples.length)?lesson.examples:Object.keys(data.examples);
 if(hasLab){
  const select=$('#example-select');
  if(select)for(const id of exampleIds){const ex=data.examples[id];if(!ex)continue;const opt=node('option','',ex.title);opt.value=ex.id;select.append(opt);}
  $$('[data-example]').forEach(b=>b.onclick=()=>selectExample(b.dataset.example,true,b.closest('[data-workspace]')));
  // 예제 전용 페이지는 data-example으로 어느 예제인지 이미 정해져 있으므로 선택 UI 없이 바로 불러온다.
  if(pageExample && data.examples[pageExample]) selectExample(pageExample);
  else if(exampleIds[0]) selectExample(exampleIds[0]);
 }
 if(hasPractice){
  for(const kind of new Set(topicQuestions().map(q=>q.kind))){const opt=node('option','',kind);opt.value=kind;$('#question-kind').append(opt);}
  renderQuestions();
 }
 initGUI();
 window.aipyLearning.saveLocal=()=>{stash();};
 window.aipyLearning.selectExample=(id)=>{if(data.examples[id])selectExample(id,false);};
 window.aipyLearning.currentExample=()=>currentId||null;
 window.aipyLearning._refreshUnit=()=>{
  if(!data)return;
  if(currentId){const id=currentId;currentId=null;selectExample(id,false);}
  renderQuestions(false);
  renderRailTodo();
 };
 window.aipyLearning.ready=true;
 document.dispatchEvent(new CustomEvent('aipy:learning-ready'));
}).catch(error=>{const out=$('#output');if(out)out.textContent='학습 데이터를 불러오지 못했습니다. 웹서버 또는 GitHub Pages 주소로 접속하고 새로고침하세요. '+error.message;toast('학습 데이터 로딩 실패');window.aipyLearning.ready=true;document.dispatchEvent(new CustomEvent('aipy:learning-ready'));});

/* 왼쪽 목차 맨 위 '아직 남은 것' — 완료 체크·문제 풀이 중 놓친 항목을 한눈에 보여 준다(#102).
   소단원 페이지는 '{id}.html', 문제 페이지는 'q-{id}.html'로 그 소단원과 같은 폴더에 있으므로
   상대 경로만으로 링크할 수 있다. 체크·풀이·원격 병합 지점에서 다시 부른다. */
function renderRailTodo(){
 const rail=$('aside.rail');
 if(!rail || !unit || !data || !Array.isArray(data.lessons)) return;
 let box=rail.querySelector('.rail-todo');
 if(!box){box=node('section','rail-todo');rail.prepend(box);}
 box.replaceChildren(node('p','eyebrow','아직 남은 것'));
 const rows=data.lessons.map(l=>{
  const done=!!state.complete[`u${unit}-${l.id}`];
  const left=(data.questions||[]).filter(q=>q.topic===l.id && answerRecord(q).status!=='done').length;
  return {lesson:l,done,left};
 });
 if(rows.every(r=>r.done && r.left===0)){
  box.append(node('p','rail-todo-clear','이 단원에서 남은 것이 없어요 🎉'));
  return;
 }
 const list=node('ul','rail-todo-list');
 for(const r of rows){
  const li=node('li','rail-todo-item');
  if(r.done && r.left===0){
   li.classList.add('rail-todo-ok');
   li.append(node('span','rail-todo-check','✔'),node('span','rail-todo-title',r.lesson.title));
   list.append(li);continue;
  }
  const link=node('a','rail-todo-link');
  link.href=!r.done?`${r.lesson.id}.html#${r.lesson.id}`:`q-${r.lesson.id}.html`;
  link.append(node('span','rail-todo-title',r.lesson.title));
  const badges=node('span','rail-todo-badges');
  if(!r.done)badges.append(node('span','rail-todo-badge warn','완료 체크 안 함'));
  if(r.left>0)badges.append(node('span','rail-todo-badge','문제 '+r.left+'개 남음'));
  link.append(badges);li.append(link);list.append(li);
 }
 box.append(list);
}
})();

/* ── 수업 프로젝터용 글자 크기 조절: −/현재%/＋. %버튼을 누르면 주요 배율 목록에서 바로 선택. */
(function(){
 const header=document.querySelector('header.top');if(!header)return;
 const KEY='aipy-zoom',MIN=0.8,MAX=1.8,STEP=0.1,PRESETS=[0.8,0.9,1,1.1,1.25,1.5,1.8];
 let z=parseFloat(localStorage.getItem(KEY));if(!(z>=MIN&&z<=MAX))z=1;
 const wrap=document.createElement('div');wrap.className='fontsize';wrap.setAttribute('role','group');wrap.setAttribute('aria-label','화면 글자 크기 조절');
 const btn=(label,title)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.title=title;b.setAttribute('aria-label',title);return b;};
 const minus=btn('−','글자 작게'),pct=btn('100%','배율 목록 열기'),plus=btn('＋','글자 크게');
 const menu=document.createElement('div');menu.className='zoom-menu';menu.hidden=true;
 PRESETS.forEach(v=>{const b=btn(Math.round(v*100)+'%','배율 '+Math.round(v*100)+'%로');b.onclick=()=>{z=v;apply();menu.hidden=true;};menu.append(b);});
 const apply=()=>{z=Math.round(z*20)/20;document.body.style.zoom=z===1?'':String(z);document.dispatchEvent(new CustomEvent('aipy:zoom'));pct.textContent=Math.round(z*100)+'%';localStorage.setItem(KEY,String(z));minus.disabled=z<=MIN;plus.disabled=z>=MAX;
  [...menu.children].forEach(b=>b.setAttribute('aria-pressed',String(b.textContent===Math.round(z*100)+'%')));};
 minus.onclick=()=>{z-=STEP;apply();};plus.onclick=()=>{z+=STEP;apply();};
 pct.onclick=(e)=>{e.stopPropagation();menu.hidden=!menu.hidden;};
 document.addEventListener('click',e=>{if(!menu.hidden&&!wrap.contains(e.target))menu.hidden=true;});
 wrap.append(minus,pct,plus,menu);
 const account=header.querySelector('.account');
 if(account)header.insertBefore(wrap,account);else header.append(wrap);
 apply();
})();

/* ── 코드 편집기 파이썬 문법 하이라이팅: textarea 아래에 색칠한 미러(pre)를 겹칩니다. */
(function(){
 const ta=document.getElementById('code-editor');if(!ta)return;
 const wrap=document.createElement('div');wrap.className='hl-wrap';
 ta.parentNode.insertBefore(wrap,ta);
 const view=document.createElement('pre');view.className='hl-view';view.setAttribute('aria-hidden','true');
 const code=document.createElement('code');view.append(code);
 wrap.append(view,ta);
 const escHtml=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;');
 const RX=new RegExp([
  '(#[^\\n]*)',                                                    // 1 주석
  '([rbfuRBFU]{0,2}(?:\'\'\'[\\s\\S]*?\'\'\'|"""[\\s\\S]*?"""))',  // 2 삼중 문자열
  '([rbfuRBFU]{0,2}(?:\'(?:\\\\.|[^\'\\\\\\n])*\'|"(?:\\\\.|[^"\\\\\\n])*"))', // 3 문자열
  '(@[A-Za-z_][\\w.]*)',                                           // 4 데코레이터
  '\\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\\b', // 5 키워드
  '\\b(self|cls|print|input|len|range|int|float|str|bool|list|tuple|dict|set|open|type|enumerate|zip|map|filter|sorted|reversed|sum|min|max|abs|round|super|isinstance|hasattr|getattr|Exception|ValueError|TypeError|KeyError|IndexError|OSError|ZeroDivisionError)\\b', // 6 내장·자주 쓰는 이름
  '\\b(\\d[\\d_]*(?:\\.[\\d_]+)?(?:[eE][+-]?\\d+)?[jJ]?)\\b'      // 7 숫자
 ].join('|'),'g');
 const CLS=['','hl-com','hl-str','hl-str','hl-dec','hl-kw','hl-bi','hl-num'];
 function paint(){
  const src=ta.value;let out='',last=0,m;RX.lastIndex=0;
  while((m=RX.exec(src))){
   out+=escHtml(src.slice(last,m.index));
   for(let g=1;g<CLS.length;g++)if(m[g]!==undefined){out+='<span class="'+CLS[g]+'">'+escHtml(m[g])+'</span>';break;}
   last=m.index+m[0].length;
   if(m[0].length===0)RX.lastIndex++;
  }
  out+=escHtml(src.slice(last));
  code.innerHTML=out+'\n';
  sync();
 }
 function sync(){view.scrollTop=ta.scrollTop;view.scrollLeft=ta.scrollLeft;}
 ta.addEventListener('input',paint);
 ta.addEventListener('scroll',sync);
 // 예제 전환 등 코드가 스크립트로 바뀌는 경우를 잡는 저비용 감시
 let lastValue=null;
 setInterval(()=>{if(ta.value!==lastValue){lastValue=ta.value;paint();}},250);
 paint();
})();

/* ── 발표 모드: 헤더·좌측 메뉴·푸터를 숨기고 본문만 크게. ESC 또는 '↩ 종료'로 복귀.
   펜: 획 단위로 저장해 매번 다시 그린다 — 스크롤을 따라 움직이고,
   드래그 중 잠시 멈추면 직선으로 펴진다. 색·굵기·불투명도는 ▾ 설정판에서. 종료 시 전부 삭제. */
(function(){
 const header=document.querySelector('header.top');if(!header)return;
 const KEY='aipy-presenting';
 const mkBtn=(cls,text,title)=>{const b=document.createElement('button');b.type='button';b.className=cls;b.textContent=text;if(title){b.title=title;b.setAttribute('aria-label',title);}return b;};
 const enter=mkBtn('present-enter','발표 모드','메뉴를 숨기고 본문만 크게 봅니다 (ESC로 복귀)');
 const tools=document.createElement('div');tools.className='present-tools';tools.setAttribute('role','toolbar');tools.setAttribute('aria-label','발표 도구');
 const fontSlot=document.createElement('span');fontSlot.className='present-fontslot';

 // 펜 상태
 const COLORS=['#d21f2c','#f28c1e','#f2c21e','#1e8a4c','#1d5bd6','#7a3bd6','#e0489a','#101831'];
 const pen={on:false,color:COLORS[0],width:3.5,alpha:1};
 const penBtn=mkBtn('present-pen',' ','펜 켜기/끄기 — 켜져 있으면 화면에 그립니다');
 const gear=mkBtn('present-gear','▾','펜 설정: 색·굵기·불투명도');
 const wipe=mkBtn('present-wipe','지우기','펜 낙서 모두 지우기');
 const exit=mkBtn('present-exit','↩ 종료','발표 종료 — 메뉴로 되돌아가기 (ESC)');

 // 설정판
 const panel=document.createElement('div');panel.className='pen-panel';panel.hidden=true;
 const swWrap=document.createElement('div');swWrap.className='pen-swatches';
 COLORS.forEach(c=>{const b=mkBtn('pen-swatch',' ','색 '+c);b.style.setProperty('--pen',c);
  b.onclick=()=>{pen.color=c;pen.on=true;syncPen();};swWrap.append(b);});
 const slider=(label,min,max,step,get,set)=>{
  const row=document.createElement('label');row.className='pen-row';
  const span=document.createElement('span');span.textContent=label;
  const input=document.createElement('input');input.type='range';input.min=min;input.max=max;input.step=step;input.value=get();
  input.oninput=()=>{set(parseFloat(input.value));syncPen();};
  row.append(span,input);return row;};
 panel.append(swWrap,
  slider('굵기',1.5,12,0.5,()=>pen.width,v=>{pen.width=v;}),
  slider('불투명도',0.2,1,0.05,()=>pen.alpha,v=>{pen.alpha=v;}));
 tools.append(fontSlot,penBtn,gear,wipe,exit,panel);document.body.append(tools);

 // 캔버스: body 밖(html)에 붙여 글자 크기(zoom)의 영향을 받지 않는다.
 // 획 좌표는 문서 기준(client+scroll)으로 저장하고, 그릴 때 현재 스크롤만큼 이동한다.
 let canvas=null,ctx=null,strokes=[],cur=null,holdTimer=null,holdAnchor=null,rafPending=false;
 function ensureCanvas(){
  if(canvas)return;
  canvas=document.createElement('canvas');canvas.className='present-ink';canvas.setAttribute('aria-hidden','true');
  document.documentElement.append(canvas);ctx=canvas.getContext('2d');sizeCanvas();
  window.addEventListener('resize',()=>{if(canvas.style.display!=='none'){sizeCanvas();redraw();}});
  window.addEventListener('scroll',()=>{if(canvas.style.display!=='none')scheduleRedraw();},{passive:true});
  document.addEventListener('aipy:zoom',()=>{if(canvas&&canvas.style.display!=='none')scheduleRedraw();});
  canvas.addEventListener('pointerdown',e=>{
   if(!pen.on)return;e.preventDefault();canvas.setPointerCapture(e.pointerId);
   cur={color:pen.color,width:pen.width,alpha:pen.alpha,straight:false,z:zoomNow(),pts:[docPt(e)]};
   holdAnchor=null;armHold(e);scheduleRedraw();});
  canvas.addEventListener('pointermove',e=>{
   if(!cur)return;
   const pt=docPt(e);
   if(cur.straight)cur.pts[1]=pt;              // 직선 모드: 끝점만 갱신
   else cur.pts.push(pt);
   armHold(e);scheduleRedraw();});
  const up=()=>{if(!cur)return;clearTimeout(holdTimer);if(cur.pts.length>1)strokes.push(cur);cur=null;scheduleRedraw();};
  canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);
 }
 // 드래그 중 0.5초 이상 거의 제자리면 직선으로 스냅
 function armHold(e){
  const now={x:e.clientX,y:e.clientY};
  if(holdAnchor&&Math.hypot(now.x-holdAnchor.x,now.y-holdAnchor.y)<5)return; // 아직 같은 자리 — 타이머 유지
  holdAnchor=now;clearTimeout(holdTimer);
  holdTimer=setTimeout(()=>{
   if(cur&&!cur.straight&&cur.pts.length>1){cur.pts=[cur.pts[0],cur.pts[cur.pts.length-1]];cur.straight=true;scheduleRedraw();}
  },500);
 }
 function zoomNow(){return parseFloat(document.body.style.zoom)||1;}
 function docPt(e){return [e.clientX+window.scrollX,e.clientY+window.scrollY];}
 function sizeCanvas(){const w=window.innerWidth,h=window.innerHeight;canvas.width=w;canvas.height=h;canvas.style.width=w+'px';canvas.style.height=h+'px';}
 function scheduleRedraw(){if(rafPending)return;rafPending=true;requestAnimationFrame(()=>{rafPending=false;redraw();});}
 function drawStroke(st,ox,oy){
  // 그릴 당시 배율(st.z) 대비 현재 배율만큼 좌표·굵기를 함께 확대/축소한다.
  const f=zoomNow()/(st.z||1);
  ctx.globalAlpha=st.alpha;ctx.strokeStyle=st.color;ctx.lineWidth=st.width*f;ctx.lineCap='round';ctx.lineJoin='round';
  ctx.beginPath();ctx.moveTo(st.pts[0][0]*f-ox,st.pts[0][1]*f-oy);
  for(let i=1;i<st.pts.length;i++)ctx.lineTo(st.pts[i][0]*f-ox,st.pts[i][1]*f-oy);
  ctx.stroke();
 }
 function redraw(){
  if(!ctx)return;ctx.clearRect(0,0,canvas.width,canvas.height);
  const ox=window.scrollX,oy=window.scrollY;
  for(const st of strokes)drawStroke(st,ox,oy);
  if(cur&&cur.pts.length>1)drawStroke(cur,ox,oy);
  ctx.globalAlpha=1;
 }
 function clearInk(){strokes=[];cur=null;if(ctx)redraw();}
 function syncPen(){
  penBtn.style.setProperty('--pen',pen.color);
  penBtn.setAttribute('aria-pressed',String(pen.on));
  if(pen.on){ensureCanvas();canvas.classList.add('inking');}
  else if(canvas)canvas.classList.remove('inking');
 }
 penBtn.onclick=()=>{pen.on=!pen.on;syncPen();};
 gear.onclick=(e)=>{e.stopPropagation();panel.hidden=!panel.hidden;};
 document.addEventListener('click',e=>{if(!panel.hidden&&!tools.contains(e.target))panel.hidden=true;});
 wipe.onclick=clearInk;

 const set=(on)=>{
  document.body.classList.toggle('presenting',on);
  sessionStorage.setItem(KEY,on?'1':'');
  const fs=document.querySelector('.fontsize');
  if(on){if(fs)fontSlot.append(fs);}
  else{
   if(fs){const account=header.querySelector('.account');if(account)header.insertBefore(fs,account);else header.append(fs);}
   pen.on=false;syncPen();clearInk();panel.hidden=true;
  }
  if(canvas)canvas.style.display=on?'':'none';
 };
 enter.onclick=()=>set(true);
 exit.onclick=()=>set(false);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('presenting'))set(false);});
 syncPen();
 const group=header.querySelector('.fontsize');
 if(group)group.append(enter);else header.append(enter);
 if(sessionStorage.getItem(KEY)==='1')set(true);
})();

/* ── 메뉴 접기(발표 모드와 별개): 상단 헤더·왼쪽 목차를 각각 접고 펼 수 있다. 상태는 브라우저에 저장. */
(function(){
 const header=document.querySelector('header.top');if(!header)return;
 const mk=(cls,text,title)=>{const b=document.createElement('button');b.type='button';b.className=cls;b.textContent=text;b.title=title;b.setAttribute('aria-label',title);return b;};
 const apply=()=>{
  const hh=localStorage.getItem('aipy-hide-header')==='1',hr=localStorage.getItem('aipy-hide-rail')==='1';
  document.body.classList.toggle('hide-header',hh);document.body.classList.toggle('hide-rail',hr);
  showHeader.hidden=!hh;showRail.hidden=!hr||!document.querySelector('aside.rail');
 };
 const hideHeader=mk('menu-fold menu-fold-header','▲','상단 메뉴 접기');
 hideHeader.onclick=()=>{localStorage.setItem('aipy-hide-header','1');apply();};
 const showHeader=mk('menu-unfold menu-unfold-header','☰ 메뉴','상단 메뉴 펼치기');
 showHeader.onclick=()=>{localStorage.setItem('aipy-hide-header','');apply();};
 const showRail=mk('menu-unfold menu-unfold-rail','▶ 목차','왼쪽 목차 펼치기');
 showRail.onclick=()=>{localStorage.setItem('aipy-hide-rail','');apply();};
 const group=header.querySelector('.fontsize');
 if(group)group.append(hideHeader);else header.append(hideHeader);
 document.body.append(showHeader,showRail);
 const rail=document.querySelector('aside.rail');
 if(rail){const hideRail=mk('menu-fold menu-fold-rail','◀ 접기','왼쪽 목차 접기');hideRail.onclick=()=>{localStorage.setItem('aipy-hide-rail','1');apply();};rail.prepend(hideRail);}
 apply();
})();
