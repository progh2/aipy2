/* Python execution is isolated from the page. A stopped worker is replaced. */
let pyodide;
self.onmessage = async ({data}) => {
  try {
    if (!pyodide) {
      self.postMessage({type:'loading',text:'Python 실행 엔진을 준비합니다. 첫 실행은 시간이 걸릴 수 있습니다…'});
      importScripts('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js');
      pyodide = await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'});
    }
    if(!data.syntax){
      self.postMessage({type:'loading',text:'실습에 필요한 Python 패키지를 확인합니다…'});
      const source=Object.entries(data.files).filter(([name])=>name.endsWith('.py')).map(([,value])=>value).join('\n');
      if (/\b(?:from|import)\s+(?:sklearn|scipy|cv2|ultralytics)\b/.test(source)) {
        throw new Error('이 라이브러리의 전체 예제는 PC 실습 경로입니다. 프로젝트 ZIP을 내려받아 실행하거나, 연결된 웹 원리 예제를 선택하세요.');
      }
      await pyodide.loadPackagesFromImports(source);
    }
    self.postMessage({type:'ready'});
    let emitted=0;
    const output = (text) => { if(emitted < 30000) {emitted+=text.length;self.postMessage({type:'stdout',text:text.slice(0,Math.max(0,30000-emitted+text.length))+'\n'});} };
    pyodide.setStdout({batched:output});
    pyodide.setStderr({batched:output});
    pyodide.globals.set('__lab_payload',JSON.stringify(data));
    const result = await pyodide.runPythonAsync(`
import json, os, sys, io, shutil, runpy, traceback, importlib, ast, base64
_lab = json.loads(__lab_payload)
_base = '/home/pyodide/student_project'
# Remove learning modules before replacing files; module caching is taught separately.
for _key, _module in list(sys.modules.items()):
    if str(getattr(_module, '__file__', '')).startswith(_base + '/'):
        del sys.modules[_key]
os.chdir('/home/pyodide')
if os.path.exists(_base):
    shutil.rmtree(_base)
os.makedirs(_base)
for _name, _source in _lab['files'].items():
    if _name.startswith('/') or '..' in _name.split('/') or '\\\\' in _name:
        raise ValueError('프로젝트 안의 상대 파일 경로만 사용하세요.')
    _path = os.path.join(_base, _name)
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    with open(_path, 'w', encoding='utf-8') as _file:
        _file.write(_source)
os.chdir(_base)
if _base not in sys.path:
    sys.path.insert(0, _base)
importlib.invalidate_caches()
sys.argv = [_lab['entry']] + _lab.get('args', [])
_old_stdin = sys.stdin
sys.stdin = io.StringIO(_lab.get('stdin', '') + '\\n')
_result = {'ok': True, 'checked': False, 'images': []}
if 'matplotlib.pyplot' in sys.modules:
    sys.modules['matplotlib.pyplot'].close('all')
try:
    if _lab.get('syntax'):
        for _name, _source in _lab['files'].items():
            if _name.endswith('.py'):
                ast.parse(_source, filename=_name)
        print('문법 확인 통과 · 실제 동작은 PC에서 실행하여 확인하세요.')
    else:
        _namespace = runpy.run_path(os.path.join(_base, _lab['entry']), run_name='__main__')
        if _lab.get('checks'):
            exec(compile(_lab['checks'], '<학습 검사>', 'exec'), _namespace)
            _result['checked'] = True
            print('✓ 준비된 입력·조건 검사를 통과했습니다.')
except SystemExit as _exit:
    if _exit.code not in (None, 0):
        _result['ok'] = False
    print('프로그램 종료:', _exit.code)
except BaseException:
    _result['ok'] = False
    traceback.print_exc()
finally:
    sys.stdin = _old_stdin
# Render only PNG files produced by this run, with bounded output size.
if _result['ok'] and not _lab.get('syntax'):
    for _folder, _, _names in os.walk(_base):
        for _name in sorted(_names):
            _path = os.path.join(_folder, _name)
            if _name.endswith('.png') and os.path.getsize(_path) < 1500000 and len(_result['images']) < 6:
                with open(_path, 'rb') as _image:
                    _bytes = _image.read()
                if _bytes.startswith(bytes([137,80,78,71,13,10,26,10])):
                    _result['images'].append({'name': _name, 'data': base64.b64encode(_bytes).decode('ascii')})
json.dumps(_result)
`);
    self.postMessage({type:'done',...JSON.parse(result)});
  } catch(error) {
    self.postMessage({type:'done',ok:false,checked:false,error:String(error)});
  }
};
