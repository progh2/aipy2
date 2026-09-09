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
print(f'PASS: {len(examples)} example syntax checks; all browser Python examples; {len(questions)} question records and executable answers; internal links and ZIP archives.')
