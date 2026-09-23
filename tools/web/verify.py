"""Content, Python, archive and local-link validation; scientific examples require their libraries.

Local / CI / Pages path and the teacher I–IV smoke list:
  docs/teacher-smoke-checklist.md
  python3 tools/web/build.py && python3 tools/web/verify.py
  .github/workflows/verify.yml (pull requests)
  .github/workflows/pages.yml (main → GitHub Pages)
"""
from pathlib import Path
import sys,subprocess,tempfile,ast,json,zipfile,io,contextlib,re
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
sys.path.insert(0,str(Path(__file__).parent))
from content import examples,questions,units,QUESTION_HINTS
import questions as bank
import later_units
import slots as content_slots
import unit1_pre_api
import unit1_tips
import unit2_pre_api
import unit2_tips
import unit3_pre_api
import unit3_tips
import unit4_pre_api
import unit4_tips
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLBACKEND='Agg')
ROOT=Path(__file__).resolve().parents[2];WEB=ROOT/'web'
assert [sum(q['unit']==u for q in questions) for u in [1,2]]==[60,70]
assert len({q['id'] for q in questions})==len(questions)
assert set(units)=={1,2,3,4}
assert {u:sum(q['unit']==u for q in questions) for u in units} == {1:60,2:70,3:44,4:39}
assert set(QUESTION_HINTS) == {q['id'] for q in questions}, '문항과 힌트 목록 불일치'
for q in questions:
 assert QUESTION_HINTS[q['id']]['prompt'] == q['prompt'], q['id']
 for field in ('hint', 'hint2'):
  hint = q[field]
  assert isinstance(hint,str) and hint.strip(), (q['id'],field)
  assert hint != q['explain'], (q['id'],'해설을 힌트로 재사용')
  assert not re.search(r'(도감|개념 표|패키지 목록|예제의 함수 이름).*(확인|비교)하세요',hint), (q['id'],'참조 지시')
  if q['kind'] in ('빈칸','예측'):
   answer = str(q['answer']).strip()
   # 숫자 부분 일치(-3와 -3.5 등)는 정답 노출로 잘못 판정하지 않습니다.
   assert not re.search(r'(?<![\w.])'+re.escape(answer)+r'(?![\w.])',hint), (q['id'],field,'정답 직접 노출')
 assert q['hint'] != q['hint2'], (q['id'],'두 단계가 동일')
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
  # 404 페이지는 어떤 깊이에서도 열리므로 사이트 절대경로(/aipy2/...)를 쓴다.
  if u.path.startswith('/'):
   assert u.path.startswith('/aipy2/'),('absolute link must start with /aipy2/',p,link)
   target=(WEB/unquote(u.path)[len('/aipy2/'):]).resolve()
  else:
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
sync=subprocess.run(['node',str(Path(__file__).parent/'test_sync_model.mjs')],capture_output=True,text=True)
assert sync.returncode==0, sync.stdout+sync.stderr
board_model=subprocess.run(['node',str(Path(__file__).parent/'test_board_model.mjs')],capture_output=True,text=True)
assert board_model.returncode==0, board_model.stdout+board_model.stderr
ops_model=subprocess.run(['node',str(Path(__file__).parent/'test_ops_model.mjs')],capture_output=True,text=True)
assert ops_model.returncode==0, ops_model.stdout+ops_model.stderr
ops_boot=subprocess.run(['node',str(Path(__file__).parent/'test_ops_boot.mjs')],capture_output=True,text=True)
assert ops_boot.returncode==0, ops_boot.stdout+ops_boot.stderr
for name in ['admin.html','ops.html','board.html','session.html','assignments.html']:
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
assert 'id="together-panel"' in session
assert 'id="together-question"' in session
assert 'id="together-bars"' in session
assert '함께 풀기' in session
assert '이름 없이' in session
assert 'id="lesson-report"' in session
assert 'id="report-summary"' in session
assert '수업 리포트' in session
teacher_session=(WEB/'assets/teacher-session.js').read_text()
assert '세션이 없어요. 시작하면 약 2시간 동안 유지돼요.' in teacher_session
assert '시선을 모았어요. 학생 쪽에 안내만 뜨고, 화면은 안 옮겨요.' in teacher_session
assert 'lesson-report-model.js' in teacher_session
assert 'together-send' in teacher_session
assert 'report-refresh' in teacher_session
assert '이름 없이' in teacher_session
assert 'aipySessionDemo' in teacher_session
assert 'existingAttentionNonce' in teacher_session
assert 'sessionEndFields' in teacher_session
assert 'getDoc' in teacher_session
follow_js=(WEB/'assets/follow.js').read_text()
assert '잠깐 혼자 보는 중' in follow_js
assert '선생님이 여기를 보고 있어요' in follow_js
assert '선생님 화면을 따라가는 중' in follow_js
assert '선생님 화면으로' in follow_js
assert 'sessionStartChanged' in follow_js
unit=(WEB/'units/unit01/index.html').read_text()
assert 'assets/follow.js' in unit
assert 'assets/sync.js' in unit
assert 'assets/sync.js' in (WEB/'index.html').read_text()
assert 'assets/teacher-focus.js' in unit
assert 'assets/teacher-focus.js' not in (WEB/'index.html').read_text()
assert 'assets/teacher-focus.js' not in (WEB/'teacher/session.html').read_text()
teacher_shell=(WEB/'assets/teacher-shell.js').read_text()
assert 'teacherPickerEmpty' in teacher_shell
assert 'readTeacherFlag' in teacher_shell
ops_js=(WEB/'assets/ops.js').read_text()
assert 'teacherAccessMessage' in ops_js
assert 'dataFailureNote' in ops_js
admin_js=(WEB/'assets/admin.js').read_text()
assert 'teacherAccessMessage' in admin_js
teacher_focus=(WEB/'assets/teacher-focus.js').read_text()
assert 'resolveTeacherClassId' in teacher_focus
assert 'focusFromUnitClick' in teacher_focus
assert 'focusWritePayload' in teacher_focus
assert '초점을 보냈습니다.' in teacher_focus
assert '에 초점을 보내요' in teacher_focus
assert 'admins' in teacher_focus
catalog=json.loads((WEB/'data/catalog.json').read_text())
example_unit={eid:u for u,ls in units.items() for l in ls for eid in l['examples']}
_ex_html_cache={}
def ex_html(eid):
 if eid not in _ex_html_cache:
  _ex_html_cache[eid]=(WEB/f'units/unit0{example_unit[eid]}/ex-{eid}.html').read_text()
 return _ex_html_cache[eid]
assert [p['id'] for p in catalog['pages']]==['units/unit01/index.html','units/unit02/index.html','units/unit03/index.html','units/unit04/index.html']
assert catalog['topics']['units/unit01/index.html'][0]['id']=='overview'
assert catalog['topics']['units/unit01/index.html'][0]['href']=='units/unit01/overview.html'
assert catalog['topics']['units/unit02/index.html'][2]['href']=='units/unit02/widgets.html'
for u, lessons in units.items():
 for lesson in lessons:
  topic_page=WEB/f'units/unit0{u}/{lesson["id"]}.html'
  assert topic_page.exists(), ('missing topic page', topic_page)
  html=topic_page.read_text()
  assert f'data-complete="u{u}-{lesson["id"]}"' in html
  assert f'data-topic="{lesson["id"]}"' in html
  assert 'class="lesson-prose"' in html
  assert 'assets/follow.js' in html
  assert lesson['lead'] in html
  if lesson['examples']:
   assert f'id="{lesson["id"]}-lab"' in html
   assert all(eid in html for eid in lesson['examples'])
   for eid in lesson['examples']:
    ex_page=WEB/f'units/unit0{u}/ex-{eid}.html'
    assert ex_page.exists(), ('missing example page', ex_page)
    ex_page_html=ex_page.read_text()
    assert 'id="lab"' in ex_page_html
    assert f'data-example="{eid}"' in ex_page_html
    assert f'data-topic="{lesson["id"]}"' in ex_page_html
unit_index=(WEB/'units/unit01/index.html').read_text()
assert 'data-lessons=' in unit_index
assert 'overview.html' in unit_index
assert 'id="topic-index-title"' in unit_index
widgets=(WEB/'units/unit02/widgets.html').read_text()
assert 'id="widgets-lab"' in widgets and 'widgets-tk' in widgets
assert 'data-complete="u2-widgets"' in widgets
for rec in list(examples.values())+[lesson for group in units.values() for lesson in group]:
 assert isinstance(rec.get('pre_api'),list),(rec.get('id'),'pre_api')
 assert isinstance(rec.get('glossary'),list),(rec.get('id'),'glossary')
 assert isinstance(rec.get('tips'),dict) and 'history' in rec['tips'] and 'youtube' in rec['tips'],(rec.get('id'),'tips')
 assert isinstance(rec.get('screenshots'),list),(rec.get('id'),'screenshots')
 for shot in rec['screenshots']:
  src=shot['src']
  if src.startswith(('http://','https://','/')):continue
  path=WEB/(src if src.startswith('assets/') else f'assets/screenshots/{src}')
  assert path.is_file() and path.stat().st_size>1000,('missing screenshot',rec.get('id'),src)
 for video in rec['tips']['youtube']:
  assert video['url'].startswith('https://'),video
  assert 'youtube.com/' in video['url'] or 'youtu.be/' in video['url'],video
hello=examples['hello-tk']
# hello-tk's youtube tip lives on the 'widgets' lesson only (#63 dedup); the
# example itself keeps history/pre_api/screenshots but not its own video.
assert hello['pre_api'] and hello['glossary'] and hello['tips']['history'] and not hello['tips']['youtube'] and hello['screenshots']
assert examples['widgets-tk']['pre_api'] and examples['widgets-tk']['tips']['history']
assert examples['widgets-tk']['screenshots']
assert examples['hello-pyside']['pre_api'] and examples['hello-pyside']['screenshots']
# hello-pyside/hello-kivy's videos live on the 'pyside'/'kivy' lessons only (#63 dedup).
assert examples['hello-pyside']['tips']['history'] and not examples['hello-pyside']['tips']['youtube']
assert examples['hello-kivy']['tips']['history'] and not examples['hello-kivy']['tips']['youtube']
assert examples['hello-wx']['tips']['history'] and not examples['hello-wx']['tips']['youtube']
libraries=(WEB/'units/unit02/libraries.html').read_text()
assert 'id="pre-api"' in ex_html('hello-pyside')
assert 'id="pre-api-hello-tk"' not in libraries
assert '코드 전에 알아 두기' in libraries
assert '역사 한 줄' in libraries
assert '사용자 인터페이스 · CLI, GUI, NUI' in libraries
assert 'id="pre-api"' in ex_html('widgets-tk')
assert 'BooleanVar' in widgets
assert 'widgets-label-entry-tk' in widgets and 'widgets-choice-tk' in widgets
assert 'assets/screenshots/widgets-tk.png' in widgets
assert 'id="screenshots"' in ex_html('widgets-tk')
assert '실행하면 이렇게 보여요' in widgets
ui_page=(WEB/'units/unit02/ui.html').read_text()
assert '코드 전에 알아 두기' in ui_page
assert 'ui-cli' in ui_page
assert content_slots.has_slots(hello) and content_slots.has_slots(examples['hello-pyside'])
unit2={lesson['id']:lesson for lesson in units[2]}
assert len(unit2['widgets']['examples'])>=5
assert len(unit2['layout']['examples'])>=4
assert len(unit2['events']['examples'])>=5
assert len(unit2['memo']['examples'])>=6
assert 'events-command-tk' in unit2['events']['examples']
assert 'memo-window-tk' in unit2['memo']['examples']
assert 'review-scratch-tk' in unit2['review']['examples']
for eid in ['widgets-label-entry-tk','layout-pack-tk','events-command-tk','memo-window-tk','pyside-first','ui-cli']:
 assert examples[eid]['pre_api'], eid
events_page=(WEB/'units/unit02/events.html').read_text()
assert 'id="pre-api"' in ex_html('events-command-tk')
assert 'command=greet()' in events_page or 'command=too_early()' in events_page
memo_page=(WEB/'units/unit02/memo.html').read_text()
assert 'memo-window-tk' in memo_page and 'memo-files-tk' in memo_page
assert 'id="pre-api"' in ex_html('memo-window-tk')
assert 'assets/screenshots/memo-tk.png' in memo_page
assert 'id="screenshots"' in ex_html('memo-tk')
# #80: Text index "1.0" / end-1c must draw as a concept-visual, not only glossary cards.
assert 'text-index-visual' in memo_page
# 소단원 단계(memo.html)와 memo-files-tk 예제 전용 페이지에 각각 하나씩 있어야 한다(#101로 분리 배치).
assert memo_page.count('text-index-visual') + ex_html('memo-files-tk').count('text-index-visual') >= 2
assert 'Text 위치는 줄.칸입니다' in memo_page
assert 'id="pre-api"' in ex_html('memo-files-tk')
assert 'get(&quot;1.0&quot;, &quot;end-1c&quot;)' in memo_page
assert '끝 자동 개행' in memo_page
layout_page=(WEB/'units/unit02/layout.html').read_text()
assert 'assets/screenshots/layout-tk.png' in layout_page
assert 'id="screenshots"' in ex_html('layout-pack-tk')
assert '실행하면 이렇게 보여요' in events_page
assert 'assets/screenshots/events-command-tk.png' in events_page
pc_unit2=[eid for lesson in units[2] for eid in lesson['examples'] if examples[eid]['mode']=='pc']
assert all(examples[eid]['screenshots'] for eid in pc_unit2), [eid for eid in pc_unit2 if not examples[eid]['screenshots']]
assert examples['events-bind-tk']['screenshots'][0]['src']=='events-bind-tk.png'
assert examples['events-pyside-signal']['screenshots'][0]['src']=='events-pyside-signal.png'
# #53: Unit II examples that introduce APIs show pre_api/glossary.
for eid in unit2_pre_api.unit2_pre_coverage():
 assert examples[eid]['pre_api'] or examples[eid]['glossary'], ('unit2 pre_api/glossary', eid)
 assert examples[eid]['pre_api'], ('unit2 pre_api', eid)
for lesson in units[2]:
 page=(WEB/f'units/unit02/{lesson["id"]}.html').read_text()
 assert '코드 전에 알아 두기' in page, lesson['id']
 for eid in lesson['examples']:
  if eid in unit2_pre_api.SKIP_TOOLKIT:
   continue
  assert 'id="pre-api"' in ex_html(eid), (lesson['id'], eid)
project_page=(WEB/'units/unit02/project.html').read_text()
# core's pre_api now lives only on the 1단원 project page (#63 dedup).
assert 'id="pre-api-core"' not in project_page
assert 'id="pre-api"' in ex_html('project-tk') and 'messagebox.showwarning' in ex_html('project-tk')
assert 'id="pre-api"' in ex_html('project-pyside') and 'QComboBox' in ex_html('project-pyside')
assert 'widgets-tk' in unit2['widgets']['examples'] and 'widgets-pyside' in unit2['widgets']['examples']
assert 'memo-tk' in unit2['memo']['examples'] and 'memo-pyside' in unit2['memo']['examples']
assert 'wx' in unit2 and unit2['wx']['extra']
assert unit2['wx']['examples'] == [
    'first-wx', 'widgets-label-entry-wx', 'widgets-choice-wx', 'widgets-wx',
    'layout-wx', 'events-wx', 'memo-window-wx', 'memo-wx', 'project-wx',
]
assert 'widgets-wx' not in unit2['widgets']['examples']
assert 'memo-wx' not in unit2['memo']['examples']
wx_page = (WEB / 'units/unit02/wx.html').read_text()
assert 'id="wx-lab"' in wx_page and 'first-wx' in wx_page and 'memo-wx' in wx_page
assert 'id="pre-api"' in ex_html('first-wx') and 'wx.App' in wx_page
assert 'id="pre-api"' in ex_html('memo-wx') and 'FileDialog' in wx_page
assert 'Pyodide' in wx_page and '본편 tkinter/PySide6' in wx_page
assert 'assets/screenshots/widgets-wx.png' in wx_page
assert 'id="screenshots"' in ex_html('widgets-wx')
assert '코드 전에 알아 두기' in wx_page
assert examples['first-wx']['pre_api'] and examples['memo-wx']['pre_api']
assert examples['widgets-wx']['screenshots'][0]['src'] == 'widgets-wx.png'
assert '브라우저(Pyodide)' in examples['first-wx']['note']
assert 'kivy' in unit2 and unit2['kivy']['extra']
assert unit2['kivy']['examples'] == [
    'first-kivy', 'widgets-label-entry-kivy', 'widgets-choice-kivy', 'widgets-kivy',
    'layout-kivy', 'events-kivy', 'memo-window-kivy', 'memo-kivy', 'project-kivy',
]
assert 'widgets-kivy' not in unit2['widgets']['examples']
assert 'memo-kivy' not in unit2['memo']['examples']
assert 'first-kivy' not in unit2['wx']['examples']
kivy_page = (WEB / 'units/unit02/kivy.html').read_text()
assert 'id="kivy-lab"' in kivy_page and 'first-kivy' in kivy_page and 'memo-kivy' in kivy_page
assert 'id="pre-api"' in ex_html('first-kivy') and 'App / build' in ex_html('first-kivy')
assert 'id="pre-api"' in ex_html('memo-kivy') and 'memo.txt' in kivy_page
assert 'Pyodide' in kivy_page and '본편 tkinter/PySide6' in kivy_page
assert 'pip install kivy' in kivy_page
assert 'assets/screenshots/widgets-kivy.png' in kivy_page
assert 'id="screenshots"' in ex_html('widgets-kivy')
assert '코드 전에 알아 두기' in kivy_page
assert examples['first-kivy']['pre_api'] and examples['memo-kivy']['pre_api']
assert examples['widgets-kivy']['screenshots'][0]['src'] == 'widgets-kivy.png'
assert '브라우저(Pyodide)' in examples['first-kivy']['note']
assert 'pip install kivy' in examples['first-kivy']['note']
assert 'kivy.html' in (WEB / 'units/unit02/review.html').read_text()
assert 'kivy.html' in (WEB / 'units/unit02/index.html').read_text()
# #58: Unit II history/youtube seeds (empty youtube is OK where no solid public video).
for lid in unit2_tips.unit2_history_lessons():
 assert unit2[lid]['tips']['history'], ('unit2 history', lid)
for lid in unit2_tips.unit2_youtube_lessons():
 assert unit2[lid]['tips']['youtube'], ('unit2 youtube', lid)
assert not unit2['wx']['tips']['youtube']
assert not unit2['project']['tips']['youtube']
assert not unit2['review']['tips']['youtube']
assert not unit2['libraries']['tips']['youtube']
ui_page=(WEB/'units/unit02/ui.html').read_text()
assert 'id="content-tips"' in ui_page
assert '더 알아보는 팁' in ui_page
assert 'https://www.youtube.com/watch?v=XIGSJshYb90' in ui_page
assert 'Xerox Alto' in ui_page
assert 'id="pre-api"' in ex_html('hello-tk')
assert 'tk.Button' in ex_html('hello-tk') and 'command=함수()' in ex_html('hello-tk')
assert 'assets/screenshots/tk.png' in ui_page
pyside_page=(WEB/'units/unit02/pyside.html').read_text()
assert 'https://www.youtube.com/watch?v=Z1N9JzNax2k' in pyside_page
assert 'id="content-tips"' in pyside_page
kivy_page_tips=(WEB/'units/unit02/kivy.html').read_text()
assert 'https://www.youtube.com/watch?v=l8Imtec4ReQ' in kivy_page_tips
assert 'id="content-tips"' in kivy_page_tips
wx_page_tips=(WEB/'units/unit02/wx.html').read_text()
assert '역사 한 줄' in wx_page_tips and 'Julian Smart' in wx_page_tips
assert 'id="content-tips"' in wx_page_tips
widgets_tips=(WEB/'units/unit02/widgets.html').read_text()
assert 'id="content-tips"' in widgets_tips
assert 'https://www.youtube.com/watch?v=YXPyB4XeYLA' in widgets_tips
assert '역사 한 줄' in (WEB/'units/unit02/layout.html').read_text()
assert '역사 한 줄' in (WEB/'units/unit02/events.html').read_text()
assert '역사 한 줄' in (WEB/'units/unit02/memo.html').read_text()
assert '역사 한 줄' in (WEB/'units/unit02/project.html').read_text()
assert '역사 한 줄' in (WEB/'units/unit02/review.html').read_text()
# #59: Unit I density · pre_api · history/youtube (CLI screenshots stay empty).
unit1={lesson['id']:lesson for lesson in units[1]}
assert len(unit1['overview']['examples'])>=3
assert len(unit1['imports']['examples'])>=6
assert len(unit1['os-sys']['examples'])>=4
assert len(unit1['math']['examples'])>=3
assert len(unit1['random']['examples'])>=4
assert len(unit1['datetime']['examples'])>=3
assert len(unit1['thirdparty']['examples'])>=3
assert len(unit1['project']['examples'])>=2
assert len(unit1['review']['examples'])>=2
assert 'copy-twice' in unit1['overview']['examples'] and 'two-adds' in unit1['overview']['examples']
assert 'import-clash' in unit1['imports']['examples']
assert 'sys-modules' in unit1['os-sys']['examples']
assert 'math-circle' in unit1['math']['examples'] and 'math-signed' in unit1['math']['examples']
assert 'random-seed' in unit1['random']['examples'] and 'random-sample' in unit1['random']['examples']
assert 'weekday-fixed' in unit1['datetime']['examples']
assert 'pypi-names' in unit1['thirdparty']['examples'] and 'stdlib-json' in unit1['thirdparty']['examples']
assert 'project-roll' in unit1['project']['examples']
assert 'review-two-files' in unit1['review']['examples']
for eid in unit1_pre_api.unit1_pre_coverage():
 assert examples[eid]['pre_api'] or examples[eid]['glossary'], ('unit1 pre_api/glossary', eid)
 assert examples[eid]['pre_api'], ('unit1 pre_api', eid)
for lesson in units[1]:
 page=(WEB/f'units/unit01/{lesson["id"]}.html').read_text()
 assert '코드 전에 알아 두기' in page, lesson['id']
 for eid in lesson['examples']:
  assert 'id="pre-api"' in ex_html(eid), (lesson['id'], eid)
for lid in unit1_tips.unit1_history_lessons():
 assert unit1[lid]['tips']['history'], ('unit1 history', lid)
for lid in unit1_tips.unit1_youtube_lessons():
 assert unit1[lid]['tips']['youtube'], ('unit1 youtube', lid)
assert not unit1['math']['tips']['youtube']
assert not unit1['project']['tips']['youtube']
assert not unit1['review']['tips']['youtube']
overview_page=(WEB/'units/unit01/overview.html').read_text()
assert 'id="pre-api"' in ex_html('reuse')
assert 'id="pre-api"' in ex_html('copy-twice')
assert 'id="content-tips"' in overview_page
assert '더 알아보는 팁' in overview_page
# The modules video now lives on 'imports' only (#63 dedup).
assert 'https://www.youtube.com/watch?v=CqvZ3vGoGs0' not in overview_page
assert 'Python 1.5' in overview_page
imports_page=(WEB/'units/unit01/imports.html').read_text()
assert 'https://www.youtube.com/watch?v=CqvZ3vGoGs0' in imports_page
math_page=(WEB/'units/unit01/math.html').read_text()
assert 'id="pre-api"' in ex_html('math-signed')
assert 'math-circle' in math_page and 'math-signed' in math_page
assert '역사 한 줄' in math_page
assert 'https://www.youtube.com/' not in math_page
entrypoint_page=(WEB/'units/unit01/entrypoint.html').read_text()
assert 'https://www.youtube.com/watch?v=sugvnHA7ElY' in entrypoint_page
thirdparty_page=(WEB/'units/unit01/thirdparty.html').read_text()
assert 'pypi-names' in thirdparty_page and 'stdlib-json' in thirdparty_page
assert 'https://www.youtube.com/watch?v=U2ZN104hIcc' in thirdparty_page
assert 'id="pre-api"' in ex_html('pypi-names')
packages_page=(WEB/'units/unit01/packages.html').read_text()
assert 'https://www.youtube.com/watch?v=HGOBQPFzWKo' in packages_page
random_page=(WEB/'units/unit01/random.html').read_text()
assert 'https://www.youtube.com/watch?v=KzqSDvzOFNA' in random_page
assert 'random-seed' in random_page
datetime_page=(WEB/'units/unit01/datetime.html').read_text()
assert 'https://www.youtube.com/watch?v=eirjjyP2qcQ' in datetime_page
assert 'weekday-fixed' in datetime_page
os_page=(WEB/'units/unit01/os-sys.html').read_text()
assert 'https://www.youtube.com/watch?v=tJxcKyFMTGo' in os_page
assert 'sys-modules' in os_page
project1=(WEB/'units/unit01/project.html').read_text()
assert 'project-roll' in project1 and 'id="pre-api"' in ex_html('project-roll')
assert 'id="pre-api"' in ex_html('core')
review1=(WEB/'units/unit01/review.html').read_text()
assert 'review-two-files' in review1
assert '역사 한 줄' in review1
assert '실행하면 이렇게 보여요' not in overview_page
assert '실행하면 이렇게 보여요' not in math_page
# #60: Unit III density · pre_api · history/youtube (console shots stay empty unless a real science render exists).
unit3={lesson['id']:lesson for lesson in units[3]}
assert len(unit3['ml-overview']['examples'])>=3
assert len(unit3['ml-use']['examples'])>=3
assert len(unit3['ml-process']['examples'])>=2
assert len(unit3['ml-terms']['examples'])>=3
assert len(unit3['ml-methods']['examples'])>=3
assert len(unit3['ml-classification']['examples'])>=3
assert len(unit3['ml-project']['examples'])>=1  # 교차검증 예제는 ml-selection 소단원에만 배치
assert 'ml-rule-vs-learn' in unit3['ml-overview']['examples'] and 'ml-nesting' in unit3['ml-overview']['examples']
assert 'ml-when-not' in unit3['ml-use']['examples'] and 'ml-loan-data' in unit3['ml-use']['examples']
assert 'ml-success-mae' in unit3['ml-process']['examples']
assert 'ml-xy-table' in unit3['ml-terms']['examples'] and 'ml-leakage' in unit3['ml-terms']['examples']
assert 'ml-classify-vs-regress' in unit3['ml-methods']['examples'] and 'ml-rl-reward' in unit3['ml-methods']['examples']
assert 'ml-logistic-name' in unit3['ml-classification']['examples']
assert 'ml-report-card' in unit3['ml-project']['examples']
for eid in unit3_pre_api.unit3_pre_coverage():
 assert examples[eid]['pre_api'] or examples[eid]['glossary'], ('unit3 pre_api/glossary', eid)
 assert examples[eid]['pre_api'], ('unit3 pre_api', eid)
for lesson in units[3]:
 page=(WEB/f'units/unit03/{lesson["id"]}.html').read_text()
 assert '코드 전에 알아 두기' in page, lesson['id']
 for eid in lesson['examples']:
  assert 'id="pre-api"' in ex_html(eid), (lesson['id'], eid)
for lid in unit3_tips.unit3_history_lessons():
 assert unit3[lid]['tips']['history'], ('unit3 history', lid)
for lid in unit3_tips.unit3_youtube_lessons():
 assert unit3[lid]['tips']['youtube'], ('unit3 youtube', lid)
assert not unit3['ml-preprocess']['tips']['youtube']
assert not unit3['ml-project']['tips']['youtube']
overview3=(WEB/'units/unit03/ml-overview.html').read_text()
assert 'id="pre-api"' in ex_html('ml-rule-vs-learn')
assert 'id="pre-api"' in ex_html('ml-nesting')
assert 'id="content-tips"' in overview3
assert '더 알아보는 팁' in overview3
assert 'https://www.youtube.com/watch?v=z-EtmaFJieY' in overview3
assert '다트머스' in overview3
assert '실행하면 이렇게 보여요' not in overview3
use3=(WEB/'units/unit03/ml-use.html').read_text()
assert 'ml-when-not' in use3 and 'ml-loan-data' in use3
assert 'id="pre-api"' in ex_html('ml-loan-data')
# The Crash Course ML video now lives on 'ml-overview' only (#63 dedup).
assert 'https://www.youtube.com/watch?v=z-EtmaFJieY' not in use3
terms3=(WEB/'units/unit03/ml-terms.html').read_text()
assert 'ml-leakage' in terms3 and 'id="pre-api"' in ex_html('ml-leakage')
assert 'https://www.youtube.com/watch?v=Gv9_4yMHFhI' in terms3
methods3=(WEB/'units/unit03/ml-methods.html').read_text()
assert 'ml-rl-reward' in methods3
assert '역사 한 줄' in methods3
preprocess3=(WEB/'units/unit03/ml-preprocess.html').read_text()
assert '역사 한 줄' in preprocess3
assert 'https://www.youtube.com/' not in preprocess3
classify3=(WEB/'units/unit03/ml-classification.html').read_text()
assert 'ml-logistic-name' in classify3
assert 'https://www.youtube.com/watch?v=cKxRvEZd3Mw' in classify3
cluster3=(WEB/'units/unit03/ml-cluster.html').read_text()
assert 'https://www.youtube.com/watch?v=4b5d3muPQmA' in cluster3
assert 'assets/science/ml-cluster.png' in cluster3
assert 'id="screenshots"' in ex_html('ml-cluster')
metrics3=(WEB/'units/unit03/ml-metrics.html').read_text()
assert 'https://www.youtube.com/watch?v=Kdsp6soqA7o' in metrics3
selection3=(WEB/'units/unit03/ml-selection.html').read_text()
assert 'https://www.youtube.com/watch?v=fSytzGwwBVw' in selection3
assert 'assets/science/ml-learning-curve.png' in selection3
libraries3=(WEB/'units/unit03/ml-libraries.html').read_text()
assert 'https://www.youtube.com/watch?v=ZyhVh-qRZPA' in libraries3
assert 'assets/science/ml-chart.png' in libraries3
assert 'id="screenshots"' in ex_html('ml-chart')
project3=(WEB/'units/unit03/ml-project.html').read_text()
assert 'ml-report-card' in project3 and 'id="pre-api"' in ex_html('ml-report-card')
assert '역사 한 줄' in project3
assert 'https://www.youtube.com/' not in project3
assert examples['ml-chart']['screenshots'] and examples['ml-cluster']['screenshots']
assert examples['ml-learning-curve']['screenshots']
assert not examples['ml-rule-vs-learn']['screenshots']
assert not examples['ml-report-card']['screenshots']
assert not unit3['ml-overview']['screenshots']
# #61: Unit IV density · pre_api · history/youtube (console shots stay empty unless a real science render exists).
unit4={lesson['id']:lesson for lesson in units[4]}
assert len(unit4['cv-overview']['examples'])>=3
assert len(unit4['cv-pixels']['examples'])>=3
assert len(unit4['cv-pipeline']['examples'])>=3
assert len(unit4['cv-filters']['examples'])>=2
assert len(unit4['cv-features']['examples'])>=2
assert len(unit4['cv-haar']['examples'])>=3
assert len(unit4['cv-yolo']['examples'])>=3
assert len(unit4['cv-project']['examples'])>=1  # 원근 변환 예제는 cv-transform 소단원에만 배치
assert 'cv-process-vs-vision' in unit4['cv-overview']['examples'] and 'cv-use-fields' in unit4['cv-overview']['examples']
assert 'cv-shape-size' in unit4['cv-pixels']['examples'] and 'cv-bgr-rgb' in unit4['cv-pixels']['examples']
assert 'cv-pipeline-steps' in unit4['cv-pipeline']['examples'] and 'cv-plate-stages' in unit4['cv-pipeline']['examples']
assert 'cv-threshold-kinds' in unit4['cv-filters']['examples']
assert 'cv-feature-kinds' in unit4['cv-features']['examples']
assert 'cv-haar-vs-id' in unit4['cv-haar']['examples']
assert 'cv-scan-card' in unit4['cv-project']['examples']
for eid in unit4_pre_api.unit4_pre_coverage():
 assert examples[eid]['pre_api'] or examples[eid]['glossary'], ('unit4 pre_api/glossary', eid)
 assert examples[eid]['pre_api'], ('unit4 pre_api', eid)
for lesson in units[4]:
 page=(WEB/f'units/unit04/{lesson["id"]}.html').read_text()
 assert '코드 전에 알아 두기' in page, lesson['id']
 for eid in lesson['examples']:
  assert 'id="pre-api"' in ex_html(eid), (lesson['id'], eid)
for lid in unit4_tips.unit4_history_lessons():
 assert unit4[lid]['tips']['history'], ('unit4 history', lid)
for lid in unit4_tips.unit4_youtube_lessons():
 assert unit4[lid]['tips']['youtube'], ('unit4 youtube', lid)
assert not unit4['cv-transform']['tips']['youtube']
assert not unit4['cv-project']['tips']['youtube']
overview4=(WEB/'units/unit04/cv-overview.html').read_text()
assert 'id="pre-api"' in ex_html('cv-process-vs-vision')
assert 'id="pre-api"' in ex_html('cv-use-fields')
assert 'id="content-tips"' in overview4
assert '더 알아보는 팁' in overview4
assert 'https://www.youtube.com/watch?v=-4E2-0sxVUM' in overview4
assert 'MIT' in overview4 or '여름' in overview4
assert '실행하면 이렇게 보여요' not in overview4
pixels4=(WEB/'units/unit04/cv-pixels.html').read_text()
assert 'cv-shape-size' in pixels4 and 'cv-bgr-rgb' in pixels4
assert 'id="pre-api"' in ex_html('cv-shape-size')
# The Crash Course CV video now lives on 'cv-overview' only (#63 dedup).
assert 'https://www.youtube.com/watch?v=-4E2-0sxVUM' not in pixels4
pipeline4=(WEB/'units/unit04/cv-pipeline.html').read_text()
assert 'cv-plate-stages' in pipeline4 and 'cv-eval-criteria' in pipeline4
assert '역사 한 줄' in pipeline4
assert 'https://www.youtube.com/watch?v=-4E2-0sxVUM' not in pipeline4
transform4=(WEB/'units/unit04/cv-transform.html').read_text()
assert '역사 한 줄' in transform4
assert 'https://www.youtube.com/' not in transform4
assert 'assets/science/cv-perspective.png' in transform4
assert 'id="screenshots"' in ex_html('cv-perspective')
filters4=(WEB/'units/unit04/cv-filters.html').read_text()
assert 'cv-threshold-kinds' in filters4
assert 'https://www.youtube.com/watch?v=C_zFhWdM4ic' in filters4
assert 'assets/science/cv-filters.png' in filters4
assert 'id="screenshots"' in ex_html('cv-filters')
features4=(WEB/'units/unit04/cv-features.html').read_text()
assert 'cv-feature-kinds' in features4
assert 'https://www.youtube.com/watch?v=uihBwtPIBxM' in features4
assert 'assets/science/cv-features.png' in features4
libraries4=(WEB/'units/unit04/cv-libraries.html').read_text()
assert 'https://www.youtube.com/watch?v=oXlwWbU8l2o' in libraries4
assert 'assets/science/cv-sobel.png' in libraries4
assert 'id="screenshots"' in ex_html('cv-skimage')
io4=(WEB/'units/unit04/cv-io.html').read_text()
# The OpenCV course video now lives on 'cv-libraries' only (#63 dedup).
assert 'https://www.youtube.com/watch?v=oXlwWbU8l2o' not in io4
assert 'assets/science/cv-io.png' in io4
haar4=(WEB/'units/unit04/cv-haar.html').read_text()
assert 'cv-haar-vs-id' in haar4 and 'id="pre-api"' in ex_html('cv-haar-vs-id')
assert 'https://www.youtube.com/watch?v=uEJ71VlUmMQ' in haar4
yolo4=(WEB/'units/unit04/cv-yolo.html').read_text()
assert 'cv-count' in yolo4
assert 'https://www.youtube.com/watch?v=Cgxsv1riJhI' in yolo4
project4=(WEB/'units/unit04/cv-project.html').read_text()
assert 'cv-scan-card' in project4 and 'id="pre-api"' in ex_html('cv-scan-card')
assert '역사 한 줄' in project4
assert 'https://www.youtube.com/' not in project4
assert examples['cv-io']['screenshots'] and examples['cv-filters']['screenshots']
assert examples['cv-features']['screenshots'] and examples['cv-perspective']['screenshots']
assert examples['cv-skimage']['screenshots']
assert not examples['cv-process-vs-vision']['screenshots']
assert not examples['cv-scan-card']['screenshots']
assert not unit4['cv-overview']['screenshots']
assert 'id="pre-api"' in libraries
assert 'id="pre-api"' in ex_html('hello-pyqt') and 'from PyQt6.QtWidgets' in ex_html('hello-pyqt')
assert 'id="pre-api"' in ex_html('hello-ttk')
assert 'id="pre-api"' in ex_html('hello-wx')
assert 'id="pre-api"' in ex_html('hello-kivy')
assert '바인딩' in libraries
assert examples['hello-wx']['pre_api'] and 'Bind' in ''.join(item['name'] + item['signature'] for item in examples['hello-wx']['pre_api'])
assert examples['hello-kivy']['pre_api'] and 'bind' in ''.join(item['name'] + item['signature'] for item in examples['hello-kivy']['pre_api'])
assert len(catalog['questions'])==len(questions)
assert len(catalog['examples'])==len(examples)
assert catalog['questions'][0]['id'].startswith('u')
assert 'kind' in catalog['questions'][0] and 'prompt' in catalog['questions'][0]
choice_q=next((q for q in catalog['questions'] if q.get('kind')=='선택'), None)
assert choice_q and choice_q.get('options'), 'catalog choice options'
assert catalog['examples']['reuse']['title']
assert 'unit' in catalog['examples']['reuse']
rules=(ROOT/'firebase/firestore.rules').read_text()
assert 'match /sessions/{classroom}' in rules
assert 'match /presence/{uid}' in rules
assert 'wholeNumber(request.resource.data.attention.nonce)' in rules
assert 'request.resource.data.attention.nonce is int' not in rules
assert 'function sessionPayloadOk()' in rules
assert 'function sessionNonceMonotonic()' in rules
assert 'function sessionRestart()' in rules
assert 'allow create: if isTeacher() && classIdOk(classroom) && sessionPayloadOk()' in rules
assert 'allow update: if isTeacher() && classIdOk(classroom) && sessionPayloadOk()' in rules
assert 'sessionNonceMonotonic() || sessionRestart()' in rules
assert 'request.resource.data.focus is map' in rules
assert 'request.resource.data.attention is map' in rules
assert 'match /students/{uid}' in rules
assert 'match /state/{docId}' in rules
assert 'match /progress/{uid}' in rules
assert "keys().hasOnly(['uid', 'email', 'studentId', 'admissionYear', 'name', 'grade', 'classroom', 'number', 'counts', 'understanding', 'updatedAt'])" in rules
assert 'function understandingOk(value)' in rules
assert 'understandingOk(request.resource.data.understanding)' in rules
assert 'match /helpRequests/{id}' in rules
assert 'match /feedback/{id}' in rules
assert "helpStatusPatch('cancelled')" in rules
assert "helpStatusPatch('resolved')" in rules
assert 'function helpCreateOk()' in rules
assert 'function feedbackPayloadOk()' in rules
assert "id == request.auth.uid + '_' + request.resource.data.topicId" in rules
assert 'request.resource.data.topicId == resource.data.topicId' in rules
assert 'optionalTopic(request.resource.data.get(\'topic\', null))' in rules
assert 'resource == null' not in rules
assert 'match /assignments/{id}' in rules
assert 'function assignmentWriteOk()' in rules
assert 'function submissionCreateOk(taskId)' in rules
assert 'function submissionUpdateOk(taskId)' in rules
assert 'function teacherReviewPatch()' in rules
assert "request.resource.data.status in ['passed', 'failed']" in rules
assert "resource.data.classrooms.hasAny([rosterClassId()])" in rules
assert "reviewStatus == 'reviewed'" in rules
assignment_model=subprocess.run(['node',str(Path(__file__).parent/'test_assignment_model.mjs')],capture_output=True,text=True)
assert assignment_model.returncode==0, assignment_model.stdout+assignment_model.stderr
regrade_model_test=subprocess.run(['node',str(Path(__file__).parent/'test_regrade_model.mjs')],capture_output=True,text=True)
assert regrade_model_test.returncode==0, regrade_model_test.stdout+regrade_model_test.stderr
lesson_report_test=subprocess.run(['node',str(Path(__file__).parent/'test_lesson_report_model.mjs')],capture_output=True,text=True)
assert lesson_report_test.returncode==0, lesson_report_test.stdout+lesson_report_test.stderr
understanding=subprocess.run(['node',str(Path(__file__).parent/'test_understanding_model.mjs')],capture_output=True,text=True)
assert understanding.returncode==0, understanding.stdout+understanding.stderr
help_model=subprocess.run(['node',str(Path(__file__).parent/'test_help_model.mjs')],capture_output=True,text=True)
assert help_model.returncode==0, help_model.stdout+help_model.stderr
auth_model=subprocess.run(['node',str(Path(__file__).parent/'test_auth_model.mjs')],capture_output=True,text=True)
assert auth_model.returncode==0, auth_model.stdout+auth_model.stderr
understanding_model=(WEB/'assets/understanding-model.js').read_text()
assert '이해했어요' in understanding_model and '조금 어려워요' in understanding_model and '어려워요' in understanding_model
assert '어디가 막혔나요?' in understanding_model
assert '이해도·도움 요청은 성적에 안 들어가요. 수업 중에만 쓰는 신호예요.' in understanding_model
assert '학생이 보내는 신호예요. 점수·출결에는 안 반영돼요.' in understanding_model
understanding_js=(WEB/'assets/understanding.js').read_text()
assert "doc(db, 'progress', user.uid)" in understanding_js
assert "doc(db, 'feedback', id)" in understanding_js
assert "label.completion [data-complete]" in understanding_js
assert 'understanding-history' in understanding_js
assert 'aside.rail' in understanding_js
assert 'section.record' in understanding_js
assert 'NOT_GRADED_NOTE' in understanding_js
help_model=(WEB/'assets/help-model.js').read_text()
assert '도움 요청' in help_model
assert '요청 취소' in help_model
assert '선생님께 보냈어요.' in help_model
help_js=(WEB/'assets/help.js').read_text()
assert 'HELP_SENT' in help_js or '선생님께 보냈어요.' in help_js
assert "collection(db, 'helpRequests')" in help_js
assert "where('uid', '==', user.uid)" in help_js
assert 'status: \'cancelled\'' in help_js or "status: 'cancelled'" in help_js
assert '#lab' in help_js and '#practice' in help_js
teacher_board=(WEB/'assets/teacher-board.js').read_text()
assert "collection(db, 'progress')" in teacher_board
assert "collection(db, 'helpRequests')" in teacher_board
assert "collection(db, 'presence')" in teacher_board
assert "collection(db, 'roster')" in teacher_board
assert "where('classId', '==', id)" in teacher_board
assert "where('classroom', '==', id)" in teacher_board
assert "status: 'resolved'" in teacher_board
assert 'studentLabel' in teacher_board
assert 'board-model.js' in teacher_board
assert 'board-export' in teacher_board
assert 'student-detail' in teacher_board
assert 'aipyBoardRender' in teacher_board
assert 'renderFixture' in teacher_board
assert "doc(db, 'students', " in teacher_board and "'state', 'current')" in teacher_board
assert 'ensureStudentState' in teacher_board
assert '학습 기록 미러가 아직 없습니다' in teacher_board
assert 'answerRows' in teacher_board and 'journalRows' in teacher_board
board_model=(WEB/'assets/board-model.js').read_text()
assert 'CSV 내보내기' not in board_model
assert '학번' in board_model
assert '1분 이내' in board_model and '3분 이내' in board_model
assert 'export function answerRows' in board_model
assert 'export function journalRows' in board_model
assert 'export function unitAnswerTotals' in board_model
assert 'export function filterAnswerRows' in board_model
assert "'서술'" in board_model and "SUBJECTIVE_KINDS" in board_model
assert "collection(db, 'students'" not in board_model
assert "collection(db, 'students'" not in teacher_board
board=(WEB/'teacher/board.html').read_text()
assert 'teacher-board.js' in board
assert 'id="understanding-board"' in board
assert 'id="help-board"' in board
assert 'id="understanding-counts"' in board
assert 'id="help-list"' in board
assert 'id="roster-board"' in board
assert 'id="heatmap-board"' in board
assert 'id="question-board"' in board
assert 'id="student-detail"' in board
assert 'id="board-export"' in board
assert 'id="roster-list"' in board
assert 'id="heatmap-wrap"' in board
assert 'id="question-list"' in board
assert '학생이 보내는 신호예요. 점수·출결에는 안 반영돼요.' in board
assert '어려워요' in board
assert 'CSV 내보내기' in board
assert '이 반 학생의 접속·완료·막힌 곳·도움 요청을 한눈에 봐요.' in board
assert '여러 반이 동시에 수업해도 이 반만 보여요.' in board
assert '학번·완료·정답·도움만 내려받아요. 성적용은 아니에요.' in board
assert '>히트맵<' in board
assert '주제별로 완료·이해도 색을 봐요.' in board
assert '조회·집계는 이 반만 대상으로 합니다' not in board
assert '주제 × 학생' not in board
assert '준비 중' not in board
catalog_questions=json.loads((WEB/'data/catalog.json').read_text()).get('questions') or []
assert catalog_questions and catalog_questions[0]['id'].startswith('u'), 'catalog questions'
unit=(WEB/'units/unit01/index.html').read_text()
assert 'assets/understanding.js' in unit
assert 'assets/help.js' in unit
assert 'class="completion"' in (WEB/'units/unit01/overview.html').read_text()
assert 'data-complete="u1-overview"' in (WEB/'units/unit01/overview.html').read_text()
assert 'assets/understanding.js' in (WEB/'index.html').read_text()
assert 'assets/assignments.js' in unit
assert 'assets/assignments.js' in (WEB/'index.html').read_text()
assignments_html=(WEB/'teacher/assignments.html').read_text()
assert 'teacher-assignments.js' in assignments_html
assert 'id="assign-form"' in assignments_html
assert 'id="target-picker"' in assignments_html
assert 'id="review-panel"' in assignments_html
assert 'id="submission-list"' in assignments_html
assert '기존 문제·예제로 과제를 만들고, 반별 제출 소스·출력을 확인해요.' in assignments_html
assert 'id="reverify-class"' in assignments_html
assert 'id="reverify-note"' in assignments_html
assert '이 반 다시 채점' in assignments_html
assert '이 브라우저에서 다시 실행해 저장된 채점과 비교해요. 제출 기록은 바꾸지 않아요.' in assignments_html
assert '이 반 제출 다시 채점' not in assignments_html
assert '브라우저에서 다시 채점하는 기능은 다음 단계에서 붙습니다.' not in assignments_html
assert '다시 채점은 다음 단계' not in assignments_html
assert '문제·예제 고르기' in assignments_html
teacher_assign=(WEB/'assets/teacher-assignments.js').read_text()
assert "collection(db, 'assignments')" in teacher_assign
assert "doc(db, 'students'" in teacher_assign
assert 'submissions' in teacher_assign
assert 'catalog.json' in teacher_assign
assert '확인함' in teacher_assign
assert '짧게 남겨 주세요' in teacher_assign or 'COMMENT_PLACEHOLDER' in teacher_assign
assert 'python-run.js' in teacher_assign
assert 'regrade-model.js' in teacher_assign
assert 'REVERIFY_LABEL' in teacher_assign
assert '같음' in teacher_assign and '다름' in teacher_assign and '건너뜀' in teacher_assign
assert 'aipyAssignDemo' in teacher_assign
assert '브라우저에서 다시 채점하는 기능은 다음 단계에서 붙습니다.' not in teacher_assign
python_run=(WEB/'assets/python-run.js').read_text()
assert 'createPythonRunner' in python_run
assert 'new Worker' in python_run
regrade_model=(WEB/'assets/regrade-model.js').read_text()
assert '이 브라우저에서 다시 실행해 저장된 채점과 비교해요. 제출 기록은 바꾸지 않아요.' in regrade_model
assert '이 제출 다시 채점' in regrade_model
assert '이 반 다시 채점' in regrade_model
assert '저장된 결과와 같아요' in regrade_model
assert '저장된 결과와 달라요' in regrade_model
assert '다시 채점 안 함' in regrade_model
assert '다시 채점하지 못했어요' in regrade_model
assert '서술형은 자동 재검증하지 않아요.' in regrade_model
assert '다시 채점하지 않음' not in regrade_model
assert '다음 단계' not in regrade_model
assign_js=(WEB/'assets/assignments.js').read_text()
assert "collection(db, 'assignments')" in assign_js
assert "where('open', '==', true)" in assign_js
assert "array-contains" in assign_js
assert 'submitButtonLabel' in assign_js
assert 'statusChips' in assign_js
assert 'submitToast' in assign_js
assert 'aipy:checked' in assign_js
assert 'teacher-shell' in assign_js
assert 'location.pathname' in assign_js
assign_model=(WEB/'assets/assignment-model.js').read_text()
assert "LABEL_FAILED = '미통과'" in assign_model
assert "LABEL_PASSED = '통과'" in assign_model
assert "LABEL_LATE = '지연'" in assign_model
assert "SUBMIT_LABEL = '제출'" in assign_model
assert "RESUBMIT_LABEL = '다시 제출'" in assign_model
assert '통과하지 않아도 제출할 수 있어요.' in assign_model
assert '마감 후에도 제출할 수 있어요. 지연으로 표시돼요.' in assign_model
assert '브라우저 채점이에요. 성적·출결에는 안 들어가요.' in assign_model
assert '다시 채점은 다음 단계에서 붙어요.' not in assign_model
assert '이 브라우저에서 다시 실행해 저장된 채점과 비교해요. 제출 기록은 바꾸지 않아요.' in assign_model
assert '제출했어요.' in assign_model
assert '지연으로 제출했어요.' in assign_model
assert '미통과로 제출했어요.' in assign_model
assert '짧게 남겨 주세요' in assign_model
teacher_index=(WEB/'teacher/index.html').read_text()
assert 'assignments.html' in teacher_index
shell=(WEB/'assets/teacher-shell.js').read_text()
assert 'assignments.html' in shell
assert 'ops.html' in shell
assert "{id: 'ops'" in shell or "id: 'ops'" in shell
ops_html=(WEB/'teacher/ops.html').read_text()
assert 'ops.js' in ops_html
assert 'ops.js?v=3' in ops_html
assert 'id="ops-year"' in ops_html
assert 'id="ops-promote"' not in ops_html  # 일괄 진급 제거
assert 'id="ops-archive"' in ops_html
assert 'id="ops-remove"' in ops_html
assert 'id="ops-export"' in ops_html
assert '입학년도' in ops_html
assert '입학년도로 학생을 모아 졸업·보관을 정리해요.' in ops_html
assert '진급 반영' not in ops_html  # 일괄 진급 제거(2026-09)
assert '요약 CSV 내보내기' in ops_html
assert '코호트 보관' in ops_html
assert '명단에서만 제거' in ops_html
assert '나래 스모크' in ops_html
assert '보관하면 수업 반 목록에서만 빠져요. 학습 기록·제출물은 지우지 않아요.' in ops_html
assert '명단 한 줄만 지워요. 학습 기록은 남아요.' in ops_html
assert '학습 기록·제출물·이해도 신호는 한꺼번에 지우지 않아요.' in ops_html
ops_js=(WEB/'assets/ops.js').read_text()
assert 'ops-model.js' in ops_js
assert 'admissionYear' in ops_js
assert 'archived' in ops_js
assert "collection(db, 'roster')" in ops_js
assert "collection(db, 'students')" in ops_js
assert "collection(db, 'progress')" in ops_js
assert 'aipyOpsDemo' in ops_js
assert 'function bindUi()' in ops_js
assert 'archivePhrase' in ops_js
assert 'removePhrase' in ops_js
assert 'showBootError' in ops_js
assert '운영 화면을 시작하지 못했습니다. 새로고침하세요.' in ops_js
assert 'teacherAccessMessage' in ops_js
assert '권한을 확인하지 못했습니다. 네트워크를 확인하고 새로고침하세요.' in (WEB/'assets/auth-model.js').read_text()
assert "from './firebase-config.js'" in ops_js
assert ops_js.rfind("if ($('ops-gate')) startOps();") > ops_js.find('let uiBound')
ops_model_js=(WEB/'assets/ops-model.js').read_text()
assert '입학년도는 그대로예요. 학년·반만 바뀌고 이전 학습 기록이 이어져요.' in ops_model_js
assert '보관하면 수업 반 목록에서만 빠져요. 학습 기록·제출물은 지우지 않아요.' in ops_model_js
assert '명단 한 줄만 지워요. 학습 기록은 남아요.' in ops_model_js
assert '학습 기록·제출물·이해도 신호는 한꺼번에 지우지 않아요.' in ops_model_js
assert "CONFIRM_ARCHIVE_PREFIX = '졸업'" in ops_model_js
assert "CONFIRM_REMOVE_PREFIX = '명단삭제'" in ops_model_js
privacy_model=(WEB/'assets/privacy-model.js').read_text()
assert "PRIVACY_TITLE = '무엇이 저장되나요?'" in privacy_model
assert "PRIVACY_LEAD = '수업 운영에 필요한 최소 항목만 저장해요.'" in privacy_model
assert '학교 이메일' in privacy_model
assert '학번과 입학년도' in privacy_model
assert '학습 기록(완료·답안·저널·코드)' in privacy_model
assert '과제 제출물' in privacy_model
assert '이해도 신호' in privacy_model
assert '선생님이 보는 것' in privacy_model
assert '성적·출결에는 들어가지 않아요.' not in privacy_model  # 문구 삭제(2026-09-21 교사 요청)
assert '본인 학습 기록은 JSON으로 내보낼 수 있어요.' in privacy_model
assert '실제 보관·동의는 학교 규정을 따릅니다.' in privacy_model
auth_js=(WEB/'assets/auth.js').read_text()
assert 'privacy-model.js' in auth_js
assert 'privacyButton' in auth_js
assert 'mountPrivacyNotice' in auth_js
home=(WEB/'index.html').read_text()
assert 'id="privacy-notice"' in home
assert 'data-export' in home
assert '학습 기록 내보내기' in home
unit_home=(WEB/'units/unit01/index.html').read_text()
assert 'id="privacy-notice"' in unit_home
assert 'data-export' in unit_home
teacher_index=(WEB/'teacher/index.html').read_text()
assert 'ops.html' in teacher_index
assert 'function teacherIdentityPatch()' in rules
assert 'archived' in rules
assert 'archivedAt' in rules
assert 'allow update: if isTeacher() && teacherIdentityPatch()' in rules
app_js=(WEB/'assets/app.js').read_text()
assert 'aipy:checked' in app_js
account_css=(WEB/'assets/account.css').read_text()
assert '.topic-signals' in account_css
assert '.understanding-choices' in account_css
assert '.help-request' in account_css
assert '.assignment-panel' in account_css
assert '.assignment-chip' in account_css
assert '.target-picker' in account_css
assert '.together-bar' in account_css
assert '.report-grid' in account_css
assert '.reverify-badge' in account_css
assert '.privacy-notice' in account_css
assert '.account-privacy' in account_css
assert '.ops-filters' in account_css
assert '.answer-filter-bar' in account_css
assert '.answer-row' in account_css
assert '.answer-value' in account_css
assert '.journal-list' in account_css
assert '#student-detail-body{overflow-y:auto' in account_css
sync_js=(WEB/'assets/sync.js').read_text()
assert 'aipyUnderstanding' in sync_js
app_js=(WEB/'assets/app.js').read_text()
assert 'lastError' in app_js
assert 'rememberError' in app_js
auth_js=(WEB/'assets/auth.js').read_text()
assert 'UNDERSTANDING_KEY' in auth_js
sync_js=(WEB/'assets/sync.js').read_text()
assert "doc(db, 'students', user.uid, 'state', 'current')" in sync_js
assert "doc(db, 'progress', user.uid)" in sync_js
assert 'confirmClearLocal' in sync_js
assert '이 브라우저의 학습 기록을 지울까요?' in sync_js
assert '어느 코드를 남길까요?' in sync_js
assert 'rememberedChoice' in sync_js
assert 'projectCodeEqual' in (WEB/'assets/sync-model.js').read_text()
assert 'aipy-sync-choices-v1' in (WEB/'assets/sync-model.js').read_text()
assert "exampleDirty" in app_js
assert 'markCode' in app_js
app_js=(WEB/'assets/app.js').read_text()
assert 'onLocalChange' in app_js
assert "save('complete')" in app_js
assert "save('code')" in app_js
assert 'applyRemote' in app_js
auth_js=(WEB/'assets/auth.js').read_text()
assert 'auth-model.js' in auth_js
assert 'initializeAuth' in auth_js
assert 'indexedDBLocalPersistence' in auth_js
assert 'browserSessionPersistence' in auth_js
assert 'authStateReady' in auth_js
assert 'readTeacherFlag' in auth_js
assert 'googleCustomParameters' in auth_js
assert 'account-switch' in auth_js
assert 'shouldWriteStudentProfile' in auth_js
assert 'missingRosterWarning' in auth_js
assert "prompt: 'select_account'" not in auth_js
assert 'setPersistence' not in auth_js
auth_model_js=(WEB/'assets/auth-model.js').read_text()
assert "params.prompt = 'select_account'" in auth_model_js
assert 'forceChooser' in auth_model_js
assert 'shouldSignOutForeignAccount' in auth_model_js
assert 'isPermissionDenied' in auth_model_js
assert 'shouldWriteStudentProfile' in auth_model_js
assert 'missingRosterWarning' in auth_model_js
assert '다시 로그인할 필요는 없습니다' in auth_model_js
account_css=(WEB/'assets/account.css').read_text()
assert '.account-switch' in account_css
# 로그아웃 로컬 지우기는 화면 안 모달 (네이티브 확인창은 교실 PC에서 막힐 수 있음)
assert 'logout-clear-overlay' in auth_js
assert 'askClearLocalOnLogout' in auth_js
assert '이 브라우저의 학습 기록을 지울까요?' in auth_js
assert "window.confirm(" not in auth_js
assert 'aipySync.flush' in auth_js
assert 'focus.get(\'topicAnchor\', null)' in rules
assert 'focus.get(\'exampleId\', null)' in rules
assert '>= resource.data.attention.nonce' in rules
assert 'resource == null' not in rules
assert '!resource.exists' not in rules
# #62: teacher smoke checklist stays next to the build/verify/Pages path.
assert (ROOT/'.github'/'workflows'/'verify.yml').is_file()
smoke=(ROOT/'docs'/'teacher-smoke-checklist.md').read_text()
assert 'python3 tools/web/build.py' in smoke
assert 'python3 tools/web/verify.py' in smoke
assert 'verify.yml' in smoke and 'pages.yml' in smoke
assert 'units/unit01/' in smoke and 'units/unit02/' in smoke
assert 'units/unit03/' in smoke and 'units/unit04/' in smoke
assert '#lab' in smoke
assert '더 알아보는 팁' in smoke
assert '코드 전에 알아 두기' in smoke
print(f'PASS: {len(examples)} example syntax checks; all browser Python examples; {len(questions)} question records and executable answers; internal links and ZIP archives.')
