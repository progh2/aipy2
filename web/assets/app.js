'use strict';
/* 학습 UI와 localStorage. 클라우드 미러는 assets/sync.js가 붙습니다.
   훅: save(kind), window.aipyLearning.{getState,applyRemote,onLocalChange,key}.
   kind: complete|answer 즉시 동기화, code|journal|draft|nav 는 유휴·이탈. */
(() => {
const prefix=document.body.dataset.prefix||'', unit=Number(document.body.dataset.unit||0), KEY='aipy-lab-v1';
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
 if(kind!=='remote'){
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
 if($('#resume') && typeof state.last==='string' && /^units\/unit0[1-4]\/index\.html#[a-z0-9-]+$/.test(state.last))$('#resume').href=state.last;
 if(typeof window.aipyLearning._refreshUnit==='function') window.aipyLearning._refreshUnit();
}
window.aipyLearning={ready:false,key:KEY,saveLocal(){save('leave');},getState(){return state;},applyRemote,onLocalChange:null,selectExample(){},currentExample(){return null;}};
window.addEventListener('pagehide',()=>{try{window.aipyLearning.saveLocal();}catch{}});
function download(name,content,type='text/plain;charset=utf-8'){const url=URL.createObjectURL(new Blob([content],{type}));const a=node('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);}
async function copy(text){try{await navigator.clipboard.writeText(text);toast('복사했습니다.');}catch{const area=node('textarea');area.value=text;document.body.append(area);area.select();const ok=document.execCommand('copy');area.remove();toast(ok?'복사했습니다.':'복사가 제한되었습니다. 코드를 선택하여 복사하세요.');}}
function updateProgress(){for(const item of $$('[data-unit-progress]')){const u=Number(item.dataset.unitProgress),total=Number(item.dataset.total)||1;const count=Object.entries(state.complete).filter(([k,v])=>k.startsWith(`u${u}-`)&&v).length;const value=Math.min(100,Math.round(count/total*100));item.textContent=`${value}%`;$$(`[data-unit-bar="${u}"]`).forEach(e=>e.value=value);}}
updateProgress();
if(!storageWorks)toast('기록을 불러오지 못했습니다. 이 세션의 기록은 내보내기로 보관하세요.');
if($('#resume') && typeof state.last==='string' && /^units\/unit0[1-4]\/index\.html#[a-z0-9-]+$/.test(state.last))$('#resume').href=state.last;
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
 const tip=box.closest('.lesson')?.querySelector('.pai-note'),originalMood=tip?.dataset.paiMood,originalLabel=tip?.querySelector('.pai-label').textContent;
 function showCompletion(){if(!tip)return;const mood=box.checked?'celebrate':originalMood;tip.dataset.paiMood=mood;const img=tip.querySelector('img');img.src=prefix+`assets/mascot/pai-${mood}-v1.webp?v=girl2`;img.alt='';tip.querySelector('.pai-label').textContent=box.checked?'파이 · 설명까지 완료했어요!':originalLabel;}
 box._paintComplete=showCompletion;
 showCompletion();box.addEventListener('change',()=>{state.complete[box.dataset.complete]=box.checked;save('complete');updateProgress();showCompletion();});
});
$$('[data-journal]').forEach(area=>{area.value=state.journals[area.dataset.journal]||'';area.addEventListener('input',()=>{state.journals[area.dataset.journal]=area.value;save('journal');});});
if($('#download-journal'))$('#download-journal').onclick=()=>{let text=`# ${unit}단원 학습 저널\n\n작성일: ${new Date().toLocaleDateString('ko-KR')}\n`;for(const [key,title]of [['learn','이해한 개념'],['error','오류와 해결 근거'],['next','시험 결과와 다음 도전']])text+=`\n## ${title}\n\n${state.journals[`u${unit}-${key}`]||''}\n`;download(`unit${unit}-journal.md`,text);};
if(!unit){window.aipyLearning.ready=true;document.dispatchEvent(new CustomEvent('aipy:learning-ready'));return;}
let data, currentId, files={},fileName, worker=null,running=false,timer,jobResolve,jobOutput,exampleDirty=false;
function remember(){const id=location.hash.slice(1)||'overview';if(/^[a-z0-9-]+$/.test(id)){state.last=`units/unit0${unit}/index.html#${id}`;save('nav');}}
window.addEventListener('hashchange',remember);remember();
function stop(reason='실행을 중지했습니다.'){
 if(worker)worker.terminate();worker=null;clearTimeout(timer);
 if(jobOutput)jobOutput(reason+'\n');
 paiGuide('thinking','잠시 멈추고 조건을 살펴봐요.','반복이 끝나는 조건을 확인하고, 수정한 뒤 다시 실행하세요.');
 if(jobResolve)jobResolve({ok:false,stopped:true});
 jobResolve=null;jobOutput=null;running=false;$('#stop').disabled=true;
}
function execute(payload,onOutput){
 if(running){toast('현재 실행을 마치거나 중지한 뒤 다시 실행하세요.');return Promise.resolve({ok:false,busy:true});}
 running=true;$('#stop').disabled=false;
 return new Promise(resolve=>{
  jobResolve=resolve;jobOutput=onOutput;
  if(!worker)worker=new Worker(prefix+'assets/python-worker.js?v=science1');
  clearTimeout(timer);timer=setTimeout(()=>stop('실행 엔진 준비 시간이 초과되었습니다. 네트워크를 확인하고 다시 실행하세요.'),180000);
  worker.onmessage=({data:m})=>{
   if(m.type==='loading')onOutput(m.text+'\n');
   if(m.type==='ready'){clearTimeout(timer);timer=setTimeout(()=>stop('30초 실행 제한에 도달했습니다. 반복 조건을 확인하세요.'),30000);}
   if(m.type==='stdout')onOutput(m.text);
   if(m.type==='done'){clearTimeout(timer);running=false;$('#stop').disabled=true;if(m.error)onOutput(m.error+'\n');jobResolve=null;jobOutput=null;resolve(m);}
  };
  worker.onerror=e=>{onOutput('실행 오류: '+e.message+'\n');stop('실행 엔진을 다시 준비합니다.');};
  worker.postMessage(payload);
 });
}
$('#stop').onclick=()=>stop();
function validName(name){return typeof name==='string' && /^[\w.-]+(?:\/[\w.-]+)*$/.test(name) && !name.split('/').some(p=>p==='.'||p==='..') && name.length<150;}
function stash(){if(!currentId)return;files[fileName]=$('#code-editor').value;state.projects[currentId]={files,entry:$('#entry-file').value,stdin:$('#stdin').value,args:$('#argv').value};save('code');}
function renderFiles(){
 const tree=$('#file-tree');tree.replaceChildren();
 Object.keys(files).sort().forEach(name=>{const b=node('button',name===fileName?'active':'',name);b.setAttribute('aria-pressed',String(name===fileName));b.onclick=()=>{stash();fileName=name;$('#code-editor').value=files[name];$('#file-name').textContent=name;renderFiles();};tree.append(b);});
 const entry=$('#entry-file'),old=entry.value;entry.replaceChildren();Object.keys(files).filter(n=>n.endsWith('.py')).forEach(n=>{const opt=node('option','',n);opt.value=n;entry.append(opt);});if(files[old]!==undefined)entry.value=old;
 $('#file-name').textContent=fileName;
}
function selectExample(id,scroll=false,workspace=null){
 if(running){$('#example-select').value=currentId;toast('현재 실행을 마치거나 중지한 뒤 예제를 바꾸세요.');return;}
 if(!data.examples[id])return;
 const lab=$('#lab'),active=lab.closest('[data-workspace]');
 const owner=workspace || (active && data.lessons.find(l=>l.id===active.dataset.workspace)?.examples.includes(id) ? active : $$('[data-workspace]').find(el=>data.lessons.find(l=>l.id===el.dataset.workspace)?.examples.includes(id)));
 if(owner){owner.querySelector('.editor-mount').append(lab);$('#lab h2').textContent='바로 실습 · '+data.lessons.find(l=>l.id===owner.dataset.workspace).title;}
 $$('[data-example]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.example===id&&b.closest('[data-workspace]')===owner)));
if(currentId)stash();currentId=id;const ex=data.examples[id],saved=state.projects[id];
 files=JSON.parse(JSON.stringify(ex.files));
 if(saved && saved.files && typeof saved.files==='object' && Object.entries(saved.files).every(([n,s])=>validName(n)&&typeof s==='string') && Object.keys(saved.files).some(n=>n.endsWith('.py')))files={...saved.files};
 fileName=files[ex.entry]!==undefined?ex.entry:Object.keys(files)[0];
 $('#example-select').value=id;$('#code-editor').value=files[fileName];renderFiles();
 $('#entry-file').value=saved?.entry&&files[saved.entry]!==undefined?saved.entry:ex.entry;
 $('#stdin').value=saved?.stdin??ex.stdin??'';$('#argv').value=saved?.args??ex.args??'[]';if(!$('#argv').value)$('#argv').value='[]';
 $('#run-mode').textContent=ex.mode==='web'?'브라우저 Python 실행':'PC Python 실습';
 $('#run').textContent=ex.mode==='web'?'▶ Python 실행':'Python 문법 확인';
 $('#check-example').disabled=!ex.checks;
 $('#check-example').textContent=ex.checks?'입력·조건 검사':'PC 실행으로 동작 점검';
 $('#example-note').textContent=(ex.note||'')+(ex.mode==='pc'?' 이 코드는 PC에서 실행하세요. 웹에서는 Python 문법만 확인합니다. ZIP 다운로드 후 예제 폴더를 VS Code로 열고 python main.py를 실행하세요. 필요한 라이브러리는 requirements.txt로 설치합니다.':' 파일을 오가며 편집한 뒤 실행 파일을 선택하세요. 각 실행은 새 가상 프로젝트에서 시작합니다.');
 $('#plot-output').replaceChildren();
 $('#output').textContent=`${ex.title}\n${ex.mode==='web'?'실행 결과가 여기에 표시됩니다.':'문법 검사는 패키지 설치·데이터·장치·실제 프로그램 동작까지 검사하지 않습니다.'}`;
 paiGuide('thinking',ex.mode==='web'?'실행 전에 결과를 먼저 예상해 볼까요?':'웹에서 확인한 뒤, PC에서도 시험해요.',ex.mode==='web'?'어떤 파일을 실행하나요? 입력값을 바꾸면 어떤 결과가 나올지 먼저 적어 보세요.':'문법 확인은 첫 단계예요. 다운로드한 예제를 실행하고 입력·결과·오류 처리를 확인하세요.');
 if(scroll)$('#lab').scrollIntoView({behavior:'smooth'});
}
$('#code-editor').addEventListener('input',stash);
$('#code-editor').addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();const a=e.target,s=a.selectionStart,end=a.selectionEnd;a.setRangeText('    ',s,end,'end');stash();}});
for(const id of ['stdin','argv','entry-file'])$('#'+id).addEventListener('change',stash);
$('#example-select').onchange=e=>selectExample(e.target.value,true);
$('#add-file').onclick=()=>{const name=prompt('파일 경로를 입력하세요. 예: utils.py 또는 nature/bird.py');if(name===null)return;if(!validName(name)||Object.hasOwn(files,name))return toast('중복되지 않는 상대 경로를 입력하세요.');stash();files[name]=name.endsWith('.py')?'# 새 기능을 작성하세요.\n':'';fileName=name;$('#code-editor').value=files[name];renderFiles();stash();};
$('#delete-file').onclick=()=>{if(Object.keys(files).length===1 || (fileName.endsWith('.py')&&Object.keys(files).filter(n=>n.endsWith('.py')).length===1))return toast('Python 파일 하나는 남겨 두세요.');if(!confirm(fileName+' 파일을 지울까요?'))return;delete files[fileName];fileName=Object.keys(files)[0];$('#code-editor').value=files[fileName];renderFiles();stash();};
$('#copy-code').onclick=()=>copy($('#code-editor').value);
$('#download-file').onclick=()=>download(fileName.split('/').pop(),$('#code-editor').value);
$('#reset-code').onclick=()=>{if(running)return toast('실행을 마치거나 중지한 뒤 원본으로 복원하세요.');if(confirm('이 예제의 수정 내용을 원본으로 되돌릴까요?')){const id=currentId;currentId=null;delete state.projects[id];save('code');selectExample(id);}};
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
 if(result.ok){
  if(ex.mode!=='web')paiGuide('idea','문법 확인을 통과했어요. 다음은 실제 동작!', 'PC에서 예제를 실행하고 입력·출력·오류 처리를 직접 확인하세요.');
  else if(check)paiGuide('celebrate','준비된 조건을 통과했어요!', '입력값을 하나 더 바꾸어 보고, 왜 이 결과가 나오는지 내 말로 설명하세요.');
  else paiGuide('idea','예상했던 결과가 나왔나요?', '출력의 이유를 설명한 다음 숫자나 조건을 하나 바꾸어 다시 실험해 보세요.');
 }else if(!result.stopped && !result.busy)paiGuide('debug','오류는 원인을 찾을 단서예요.', '마지막 오류 줄 → 파일명과 줄 번호 → 사용한 이름과 값을 순서대로 확인하세요.');
}
$('#run').onclick=()=>runExample(false);$('#check-example').onclick=()=>runExample(true);
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
$('#download-project').onclick=()=>{stash();const ex=data.examples[currentId],all={...files};let dep=currentId.includes('pyside')?'PySide6':currentId.includes('pyqt')?'PyQt6':currentId.includes('-wx')?'wxPython':currentId.includes('kivy')?'Kivy':currentId==='thirdparty'?'numpy':'';if(dep&&!all['requirements.txt'])all['requirements.txt']=dep+'\n';all['실행안내.md']=`# ${ex.title}\n\n이 폴더를 VS Code로 열고 python ${$('#entry-file').value}로 실행하세요.\n${dep?'가상환경에서 python -m pip install -r requirements.txt를 먼저 실행하세요.':''}\n\n${ex.note||''}\n`;download(currentId+'.zip',zipFiles(all),'application/zip');};
// Question bank: keep attempts, answers and self-assessment separately.
let page=0,filtered=[];
const PAGE_SIZE=8;
function norm(s){return String(s??'').trim().replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/\s+/g,'').replace(/'/g,'"');}
function answerRecord(q){return state.answers[q.id]||{};}
function storeAnswer(q,patch){state.answers[q.id]={...answerRecord(q),...patch};save(patch.status!==undefined||patch.attempts!==undefined?'answer':'draft');}
function questionCard(q){
 const card=node('article','question');card.id=q.id;
 card.append(node('div','question-meta',`${q.id} · ${q.kind} · ${q.ref}`),node('h3','',q.prompt));
 const record=answerRecord(q);let input,order,answer=()=>'';
 if(q.kind==='선택'){
  const options=node('div','options');for(const [i,text]of q.options.entries()){const label=node('label'),radio=node('input');radio.type='radio';radio.name=q.id;radio.value=text;radio.checked=record.value===text;radio.addEventListener('change',()=>storeAnswer(q,{value:text}));label.append(radio,node('span','',text));options.append(label);}card.append(options);answer=()=>card.querySelector('input:checked')?.value||'';
 }else if(q.kind==='순서'){
  order=Array.isArray(record.value)&&record.value.length===q.answer.length&&q.answer.every(x=>record.value.includes(x))?[...record.value]:[...q.answer.slice(1),q.answer[0]];
  const list=node('ol','order-list');
  function draw(){list.replaceChildren();order.forEach((text,i)=>{const li=node('li');li.append(node('span','',text));for(const [label,diff]of [['↑',-1],['↓',1]]){const b=node('button','',label);b.setAttribute('aria-label',text+(diff<0?' 위로':' 아래로'));b.disabled=i+diff<0||i+diff>=order.length;b.onclick=()=>{[order[i],order[i+diff]]=[order[i+diff],order[i]];storeAnswer(q,{value:order});draw();};li.append(b);}list.append(li);});}draw();card.append(list);answer=()=>order;
 }else{
  const label=node('label','',q.starter?'Python 코드':q.kind==='서술'?'내 설명':'내 답안');input=node('textarea',q.starter?'code-answer':'');input.rows=q.starter?6:q.kind==='서술'?4:2;input.spellcheck=false;input.value=typeof record.value==='string'?record.value:q.starter||'';input.addEventListener('input',()=>storeAnswer(q,{value:input.value}));label.append(input);card.append(label);answer=()=>input.value;
 }
 const actions=node('div','actions'),check=node('button','primary',q.kind==='서술'?'설명 저장':q.starter?'실행하고 검사':'답 확인');
 const retry=node('button','','다시 풀기');actions.append(check,retry);card.append(actions);
 const feedback=node('div','feedback'+(record.status==='done'?' success':record.status==='retry'?' retry':''),record.feedback||'먼저 스스로 풀어 보세요.');feedback.setAttribute('role','status');paiFeedback(feedback,record.feedback||'실행하기 전에 결과를 예상하세요. 막히면 힌트를 하나씩 열어 보세요.',record.status==='done'?'celebrate':record.status==='retry'?'debug':'thinking');card.append(feedback);
 function detail(title,text){const d=node('details'),s=node('summary','',title);d.append(s,node('pre','',text));card.append(d);}
 detail('힌트 1 · 방향 잡기',q.hint);detail('힌트 2 · 점검할 원리',q.explain);detail('정답 예시와 해설',(Array.isArray(q.answer)?q.answer.join('\n'):q.answer)+'\n\n'+q.explain);
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
  storeAnswer(q,{value,status:ok?'done':'retry',attempts:(record.attempts||0)+1,feedback:text});check.disabled=false;
 };
 retry.onclick=()=>{if(confirm('이 문제의 답안을 초기화하고 다시 풀까요?')){delete state.answers[q.id];save('answer');renderQuestions(false);}};
 if(q.starter){const copyButton=node('button','','코드 복사');copyButton.onclick=()=>copy(answer());actions.append(copyButton);const stopButton=node('button','','실행 중지');stopButton.onclick=()=>{if(running)stop();};actions.append(stopButton);}
 return card;
}
function renderQuestions(reset=true){
 if(reset)page=0;const kind=$('#question-kind').value,status=$('#question-status').value,search=$('#question-search').value.trim().toLowerCase();
 filtered=data.questions.filter(q=>(!kind||q.kind===kind)&&(!search||`${q.prompt} ${q.topic} ${q.ref}`.toLowerCase().includes(search))&&(!status||(status==='todo'?!['done','retry'].includes(answerRecord(q).status):answerRecord(q).status===status)));
 const pages=Math.max(1,Math.ceil(filtered.length/PAGE_SIZE));page=Math.min(page,pages-1);
 $('#questions').replaceChildren(...filtered.slice(page*PAGE_SIZE,(page+1)*PAGE_SIZE).map(questionCard));
 const done=data.questions.filter(q=>answerRecord(q).status==='done').length;
 $('#question-summary').textContent=`전체 ${data.questions.length}문제 중 ${done}문제 점검 완료 · 현재 조건 ${filtered.length}문제`;
 $('#question-page').textContent=`${page+1} / ${pages}`;$('#previous-questions').disabled=page===0;$('#next-questions').disabled=page===pages-1;
}
for(const id of ['question-kind','question-status'])$('#'+id).onchange=()=>renderQuestions();$('#question-search').oninput=()=>renderQuestions();
$('#previous-questions').onclick=()=>{page--;renderQuestions(false);$('#practice').scrollIntoView();};$('#next-questions').onclick=()=>{page++;renderQuestions(false);$('#practice').scrollIntoView();};
function initGUI(){
 if(unit!==2)return;
 $('#demo-greet').onclick=()=>{const name=$('#demo-name').value.trim()||'여러분';$('#demo-result').textContent=`${name}님, 안녕하세요!`;$('#event-log').textContent='클릭 발생 → greet 호출 → 입력값 읽기 → 라벨 변경';};
 $('#demo-reset').onclick=()=>{$('#demo-name').value='';$('#demo-result').textContent='이름을 입력하세요.';$('#event-log').textContent='클릭 발생 → reset 호출 → 입력과 출력 초기화';};
 $('#demo-layout').onchange=e=>$('#layout-preview').className=e.target.value;
 function stats(){const text=$('#demo-memo').value;$('#demo-stats').textContent=`${text.length}자 · ${text?text.split('\n').length:0}줄`;}$('#demo-memo').oninput=stats;
 $('#demo-open').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>2000000)throw Error('2MB 이하 텍스트를 선택하세요.');$('#demo-memo').value=await f.text();stats();}catch(error){toast(error.message);}finally{e.target.value='';}};
 $('#demo-save').onclick=()=>download('memo.txt',$('#demo-memo').value);
 $('#demo-new').onclick=()=>{if(!$('#demo-memo').value||confirm('현재 메모 내용을 지우고 새 문서를 시작할까요?')){$('#demo-memo').value='';stats();}};
 function compare(){const [tk,qt]=data.pairs[Number($('#compare-select').value)];$('#compare-tk').textContent=data.examples[tk].files['main.py'];$('#compare-qt').textContent=data.examples[qt].files['main.py'];}
 $('#compare-select').onchange=compare;compare();
 $$('[data-view]').forEach(b=>b.onclick=()=>{$$('[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));const v=b.dataset.view;$$('[data-side]').forEach(x=>x.hidden=v!=='both'&&x.dataset.side!==v);$('#compare').classList.toggle('single',v!=='both');});
}
fetch(prefix+`data/unit${unit}.json`).then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(d=>{
 data=d;
 for(const ex of Object.values(data.examples)){const opt=node('option','',ex.title);opt.value=ex.id;$('#example-select').append(opt);}
 for(const kind of new Set(data.questions.map(q=>q.kind))){const opt=node('option','',kind);opt.value=kind;$('#question-kind').append(opt);}
 $$('[data-example]').forEach(b=>b.onclick=()=>selectExample(b.dataset.example,true,b.closest('[data-workspace]')));
 selectExample(Object.keys(data.examples)[0]);renderQuestions();initGUI();
 window.aipyLearning.saveLocal=()=>{stash();};
 window.aipyLearning.selectExample=(id)=>{if(data.examples[id])selectExample(id,false);};
 window.aipyLearning.currentExample=()=>currentId||null;
 window.aipyLearning._refreshUnit=()=>{
  if(!data || !currentId)return;
  const id=currentId;currentId=null;selectExample(id,false);renderQuestions(false);
 };
 window.aipyLearning.ready=true;
 document.dispatchEvent(new CustomEvent('aipy:learning-ready'));
}).catch(error=>{$('#output').textContent='학습 데이터를 불러오지 못했습니다. 웹서버 또는 GitHub Pages 주소로 접속하고 새로고침하세요. '+error.message;toast('학습 데이터 로딩 실패');window.aipyLearning.ready=true;document.dispatchEvent(new CustomEvent('aipy:learning-ready'));});
})();
