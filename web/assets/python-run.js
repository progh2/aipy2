/* 교사·학생 화면이 같이 쓰는 Pyodide 워커 래퍼. DOM(#stop, #lab)에 의존하지 않습니다.
   한 번에 하나만 실행하고, 반 분량은 호출 쪽에서 순차로 넘깁니다. */
const PREPARE_MS = 180000;
const RUN_MS = 30000;

export function parseArgs(raw) {
 try {
  const args = JSON.parse(raw || '[]');
  if (Array.isArray(args) && args.every((item) => typeof item === 'string')) return args;
 } catch { /* 제출 인자가 비어 있거나 깨져 있으면 빈 배열 */ }
 return [];
}

export function createPythonRunner({workerUrl, prepareMs = PREPARE_MS, runMs = RUN_MS} = {}) {
 let worker = null;
 let running = false;
 let timer = 0;
 let job = null;
 let tail = Promise.resolve();

 function clearTimer() {
  clearTimeout(timer);
  timer = 0;
 }

 function dropWorker() {
  if (worker) {
   try { worker.terminate(); } catch { /* 이미 죽은 워커 */ }
  }
  worker = null;
 }

 function fail(reason) {
  const current = job;
  job = null;
  running = false;
  clearTimer();
  dropWorker();
  if (current) current.resolve({ok: false, checked: false, stopped: true, error: reason, output: current.output});
 }

 function handle(message) {
  if (!job) return;
  if (message.type === 'loading') job.onOutput(message.text + '\n');
  if (message.type === 'ready') {
   clearTimer();
   timer = setTimeout(() => fail('30초 실행 제한에 도달했습니다.'), runMs);
  }
  if (message.type === 'stdout') job.onOutput(message.text);
  if (message.type === 'done') {
   clearTimer();
   running = false;
   const current = job;
   job = null;
   if (message.error) current.onOutput(message.error + '\n');
   current.resolve({
    ok: !!message.ok,
    checked: !!message.checked,
    error: message.error || '',
    images: message.images || [],
    output: current.output,
    stopped: false,
    busy: false
   });
  }
 }

 function runNow(payload, onOutput) {
  if (running) return Promise.resolve({ok: false, busy: true, checked: false, output: '', error: 'busy'});
  running = true;
  return new Promise((resolve) => {
   let output = '';
   const write = (text) => {
    output += text;
    if (typeof onOutput === 'function') onOutput(text);
   };
   job = {resolve, onOutput: write, get output() { return output; }};
   if (!worker) {
    worker = new Worker(workerUrl);
    worker.onmessage = (event) => handle(event.data || {});
    worker.onerror = (event) => {
     write(`실행 오류: ${event.message || event}\n`);
     fail('실행 엔진을 다시 준비합니다.');
    };
   }
   clearTimer();
   timer = setTimeout(() => fail('실행 엔진 준비 시간이 초과되었습니다. 네트워크를 확인하고 다시 실행하세요.'), prepareMs);
   worker.postMessage(payload);
  });
 }

 function run(payload, onOutput) {
  const next = tail.then(() => runNow(payload, onOutput), () => runNow(payload, onOutput));
  tail = next.then(() => {}, () => {});
  return next;
 }

 function stop(reason = '실행을 중지했습니다.') {
  if (running) fail(reason);
 }

 function dispose() {
  stop('실행을 닫았습니다.');
  dropWorker();
 }

 return {run, stop, dispose, get running() { return running; }};
}
