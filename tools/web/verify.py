"""Content, Python, archive and local-link validation; scientific examples require their libraries."""
from pathlib import Path
import sys,subprocess,tempfile,ast,json,zipfile,io,contextlib
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
sys.path.insert(0,str(Path(__file__).parent))
from content import examples,questions,units
import questions as bank
import later_units
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLBACKEND='Agg')
ROOT=Path(__file__).resolve().parents[2];WEB=ROOT/'web'
assert [sum(q['unit']==u for q in questions) for u in [1,2]]==[60,70]
assert len({q['id'] for q in questions})==len(questions)
assert set(units)=={1,2,3,4}
assert {u:sum(q['unit']==u for q in questions) for u in units} == {1:60,2:70,3:44,4:39}
for u, lessons in units.items():
 assert len(lessons)>=9
 for l in lessons:
  for id in l['examples']:assert id in examples
for ex in examples.values():
 for name,src in ex['files'].items():
  if name.endswith('.py'):ast.parse(src,filename=name)
 if ex['mode']=='web':
  with tempfile.TemporaryDirectory(prefix='aipy-verify-') as d:
   for name,src in ex['files'].items():
    p=Path(d)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(src)
   # Run exactly as a fresh script; stdout is retained on failure only.
   p=subprocess.run([sys.executable,ex['entry'],*json.loads(ex['args'] or '[]')],cwd=d,input=ex['stdin']+'\n',text=True,capture_output=True,timeout=40)
   assert p.returncode==0,(ex['id'],p.stderr)
   if ex['checks']:
    script='import runpy\nns=runpy.run_path('+repr(ex['entry'])+',run_name="__main__")\nexec('+repr(ex['checks'])+',ns)'
    p=subprocess.run([sys.executable,'-c',script],cwd=d,input=ex['stdin']+'\n',text=True,capture_output=True,timeout=40)
    assert p.returncode==0,(ex['id'],p.stderr)
for q in questions:
 if q['options']:assert q['answer'] in q['options']
 if q['starter']:
  ns={};exec(q['answer'],ns);exec(q['checks'],ns)
  try:
   with contextlib.redirect_stdout(io.StringIO()):
    ns={};exec(q['starter'],ns);exec(q['checks'],ns)
  except Exception:pass
  else:raise AssertionError(('starter unexpectedly passes',q['id']))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
parsers={}
for p in WEB.rglob('*.html'):
 parser=Links();parser.feed(p.read_text());assert len(parser.ids)==len(set(parser.ids)),('duplicate id',p);parsers[p.resolve()]=parser
for p,parser in parsers.items():
 for link in parser.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),('missing link',p,link)
  if u.fragment and target in parsers:assert unquote(u.fragment) in parsers[target].ids,('missing anchor',p,link)
for p in WEB.rglob('*.zip'):
 with zipfile.ZipFile(p) as z:
  assert len(z.namelist())==len(set(z.namelist())),('duplicate zip entry',p)
  assert z.testzip() is None
for name in ['tk','ttk','pyside','pyqt','wx','kivy']:assert (WEB/f'assets/screenshots/{name}.png').stat().st_size>1000
picker=subprocess.run(['node',str(Path(__file__).parent/'test_class_picker.mjs')],capture_output=True,text=True)
assert picker.returncode==0, picker.stdout+picker.stderr
follow=subprocess.run(['node',str(Path(__file__).parent/'test_follow_model.mjs')],capture_output=True,text=True)
assert follow.returncode==0, follow.stdout+follow.stderr
for name in ['admin.html','board.html','session.html']:
 html=(WEB/'teacher'/name).read_text()
 assert 'id="teacher-shell"' in html, name
 assert 'teacher-shell.js' in html, name
session=(WEB/'teacher/session.html').read_text()
assert 'teacher-session.js' in session
assert 'id="session-start"' in session and '세션 시작' in session
assert 'id="attention-send"' in session and '시선 모으기' in session
assert '따라오는 중' in session
assert '이 반 학생 화면을 같이 따라가게 할 수 있어요' in session
assert '세션 키' not in session and 'Firestore' not in session
teacher_session=(WEB/'assets/teacher-session.js').read_text()
assert '세션이 없어요. 시작하면 약 2시간 동안 유지돼요.' in teacher_session
assert '시선을 모았어요. 학생 쪽에 안내만 뜨고, 화면은 안 옮겨요.' in teacher_session
follow_js=(WEB/'assets/follow.js').read_text()
assert '잠깐 혼자 보는 중' in follow_js
assert '선생님이 여기를 보고 있어요' in follow_js
assert '선생님 화면을 따라가는 중' in follow_js
assert '선생님 화면으로' in follow_js
unit=(WEB/'units/unit01/index.html').read_text()
assert 'assets/follow.js' in unit
assert 'assets/teacher-focus.js' in unit
assert 'assets/teacher-focus.js' not in (WEB/'index.html').read_text()
assert 'assets/teacher-focus.js' not in (WEB/'teacher/session.html').read_text()
teacher_focus=(WEB/'assets/teacher-focus.js').read_text()
assert 'resolveTeacherClassId' in teacher_focus
assert 'focusFromUnitClick' in teacher_focus
assert 'focusWritePayload' in teacher_focus
assert '초점을 보냈습니다.' in teacher_focus
assert '에 초점을 보내요' in teacher_focus
assert 'admins' in teacher_focus
catalog=json.loads((WEB/'data/catalog.json').read_text())
assert [p['id'] for p in catalog['pages']]==['units/unit01/index.html','units/unit02/index.html','units/unit03/index.html','units/unit04/index.html']
assert catalog['topics']['units/unit01/index.html'][0]['id']=='overview'
rules=(ROOT/'firebase/firestore.rules').read_text()
assert 'match /sessions/{classroom}' in rules
assert 'match /presence/{uid}' in rules
assert 'wholeNumber(request.resource.data.attention.nonce)' in rules
assert 'request.resource.data.attention.nonce is int' not in rules
assert 'function sessionPayloadOk()' in rules
assert 'function sessionNonceMonotonic()' in rules
assert 'allow create: if isTeacher() && classIdOk(classroom) && sessionPayloadOk()' in rules
assert 'sessionPayloadOk() && sessionNonceMonotonic()' in rules
assert 'request.resource.data.focus is map' in rules
assert 'request.resource.data.attention is map' in rules
assert 'focus.get(\'topicAnchor\', null)' in rules
assert 'focus.get(\'exampleId\', null)' in rules
assert '>= resource.data.attention.nonce' in rules
assert 'resource == null' not in rules
assert '!resource.exists' not in rules
print(f'PASS: {len(examples)} example syntax checks; all browser Python examples; {len(questions)} question records and executable answers; internal links and ZIP archives.')
