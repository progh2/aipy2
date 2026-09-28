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
import unit4_pre_api
import unit4_tips
# (#131) unit2_pre_api/unit2_tips/unit3_pre_api/unit3_tips는 pre-api/tips 슬롯을
# 더는 렌더링하지 않는 2·3단원과 무관해져 여기서는 더 쓰지 않는다(1·4단원은 그대로).
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLBACKEND='Agg')
ROOT=Path(__file__).resolve().parents[2];WEB=ROOT/'web'
assert [sum(q['unit']==u for q in questions) for u in [1,2]]==[60,40]
assert len({q['id'] for q in questions})==len(questions)
assert set(units)=={1,2,3,4}
assert {u:sum(q['unit']==u for q in questions) for u in units} == {1:60,2:40,3:50,4:39}
assert set(QUESTION_HINTS) == {q['id'] for q in questions}, '문항과 힌트 목록 불일치'
# (#116) 문항 topic은 반드시 그 단원의 실제 소단원 id여야 q-{topic}.html로 연결된다.
# review처럼 문제를 일부러 만들지 않은 소단원만 허용 목록으로 예외를 둔다.
LESSON_IDS={u:{l['id'] for l in units[u]} for u in units}
EMPTY_TOPIC_ALLOWED={(2,'review'),(2,'project')}
# (#131) 2단원 개편으로 'pyside' 소단원 페이지를 삭제했다. questions.py·question_topics.py의
# 문항 정의(topic='pyside' 12개)는 D/E가 별도로 정리 중이므로 여기서는 고치지 않고, 이제
# 어떤 소단원도 가리키지 않는 topic만 허용 목록으로 봐 준다 — 렌더링은 build.py가 이미
# 소단원별 페이지에서 건너뛰고, 단원 전체 문제 목록(practice.html)에는 그대로 남는다.
ORPHANED_TOPICS_ALLOWED=set()
# (#131) 2·3단원은 PPT 슬라이드 기반 소단원 페이지(deck_u2/deck_u3)를 쓴다 —
# pre-api/tips/screenshots/density 문단은 더 이상 렌더링하지 않는다. 'project'(2단원)는
# 교과서 슬라이드가 없는 확장 페이지라 deck-slide 0개를 허용한다.
import deck_u2, deck_u3
DECKS={2:deck_u2.LESSONS,3:deck_u3.LESSONS}
EMPTY_SLIDES_ALLOWED={(2,'project')}
BANNED_LIBS=('PySide','PyQt','wxPython','Kivy')
def lesson_practice_ids(u,lesson):
 if u in DECKS: return [it for it in (DECKS[u].get(lesson['id'],{}).get('practice') or []) if isinstance(it,str)]
 return lesson['examples']
for q in questions:
 assert q['topic'] in LESSON_IDS[q['unit']] or (q['unit'],q['topic']) in ORPHANED_TOPICS_ALLOWED, (q['id'],'topic이 소단원 id가 아니며 허용되지 않음',q['topic'])
for u in units:
 for l in units[u]:
  has_q=any(q['unit']==u and q['topic']==l['id'] for q in questions)
  if not has_q:
   assert (u,l['id']) in EMPTY_TOPIC_ALLOWED, (u,l['id'],'문항이 없는 소단원이 허용 목록에 없음')
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
 assert len(lessons)>=(7 if u==2 else 9)  # (#131) 2단원 8개 소단원(pyside/wx/kivy 삭제)
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
teacher_answers_model=subprocess.run(['node',str(Path(__file__).parent/'test_teacher_answers_model.mjs')],capture_output=True,text=True)
assert teacher_answers_model.returncode==0, teacher_answers_model.stdout+teacher_answers_model.stderr
for name in ['admin.html','ops.html','board.html','session.html','assignments.html','answers.html']:
 html=(WEB/'teacher'/name).read_text()
 assert 'id="teacher-shell"' in html, name
 assert 'teacher-shell.js' in html, name
answers=(WEB/'teacher/answers.html').read_text()
assert 'teacher-answers.js' in answers
assert 'id="answers-roster-list"' in answers and '학번순입니다' in answers
assert 'id="answers-detail-body"' in answers
teacher_shell_js=(WEB/'assets/teacher-shell.js').read_text()
assert "href: 'answers.html'" in teacher_shell_js and "label: '답변 내역'" in teacher_shell_js
teacher_answers_js=(WEB/'assets/teacher-answers.js').read_text()
assert 'getDoc' in teacher_answers_js
assert 'aipyAnswersDemo' in teacher_answers_js
assert '아직 제출한 답변이 없습니다' in teacher_answers_js
board_js=(WEB/'assets/teacher-board.js').read_text()
assert 'renderAnswerUnitGroup' in board_js and 'answer-view.js' in board_js
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
example_unit={eid:u for u,ls in units.items() for l in ls for eid in lesson_practice_ids(u,l)}
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
  assert 'assets/follow.js' in html
  assert lesson['lead'] in html
  # (#130) 소단원 설명·실습·문제 페이지는 저널 칸 하나를 data-journal="j-u{u}-{소단원id}"로 공유한다.
  journal_key=f'j-u{u}-{lesson["id"]}'
  assert html.count(f'data-journal="{journal_key}"')==1, ('missing/duplicate lesson journal', topic_page)
  if u in DECKS:
   if (u,lesson['id']) not in EMPTY_SLIDES_ALLOWED:
    assert html.count('class="deck-slide"')>=1, ('missing deck slide', topic_page)
   if lesson['id']!='libraries':
    for banned in BANNED_LIBS:
     assert banned not in html, (banned,'off-curriculum library mentioned on deck page',topic_page)
   # (#131) 2단원(및 DECKS 기반 소단원)은 슬라이드마다 설명이 있어야 하고, 실습에 넣은
   # 튜토리얼은 최소 1단계 이상이어야 한다. 빈 explain·steps로 남겨 두는 회귀를 막는다.
   if u==2:
    deck_lesson=DECKS[u].get(lesson['id'],{})
    slides=deck_lesson.get('slides') or []
    for sl in slides:
     assert sl.get('explain'), ('slide missing explain text',lesson['id'],sl.get('n'))
    for it in (deck_lesson.get('practice') or []):
     if isinstance(it,dict):
      assert it.get('kind')=='tutorial', ('unknown practice item kind',lesson['id'],it)
      assert it.get('steps') and len(it['steps'])>=1, ('tutorial with no steps',lesson['id'],it.get('id'))
      for st in it['steps']:
       assert (st.get('text') or '').strip(), ('tutorial step missing text',lesson['id'],it.get('id'))
  else:
   assert 'class="lesson-prose"' in html
  practice_ids=lesson_practice_ids(u,lesson)
  if practice_ids:
   assert f'id="{lesson["id"]}-lab"' in html
   assert all(eid in html for eid in practice_ids)
   for eid in practice_ids:
    ex_page=WEB/f'units/unit0{u}/ex-{eid}.html'
    assert ex_page.exists(), ('missing example page', ex_page)
    ex_page_html=ex_page.read_text()
    assert 'id="lab"' in ex_page_html
    assert f'data-example="{eid}"' in ex_page_html
    assert f'data-topic="{lesson["id"]}"' in ex_page_html
    assert ex_page_html.count(f'data-journal="{journal_key}"')==1, ('missing/duplicate lesson journal', ex_page)
  # (#116) 소단원 전용 문제 페이지의 문항 수가 데이터와 일치하는지 확인한다.
  q_page=WEB/f'units/unit0{u}/q-{lesson["id"]}.html'
  assert q_page.exists(), ('missing question page', q_page)
  q_html=q_page.read_text()
  assert q_html.count(f'data-journal="{journal_key}"')==1, ('missing/duplicate lesson journal', q_page)
  lesson_qcount=sum(q['unit']==u and q['topic']==lesson['id'] for q in questions)
  if lesson_qcount:
   assert f'문항 {lesson_qcount}개' in q_html, (lesson['id'],lesson_qcount)
   assert f'data-topic-filter="{lesson["id"]}"' in q_html
  else:
   assert (u,lesson['id']) in EMPTY_TOPIC_ALLOWED, (u,lesson['id'],'문항 0개인데 허용 목록에 없음')
   assert '이 소단원 전용 문제는 없습니다' in q_html
   assert 'practice.html' in q_html
# (#131 C) 3단원 slide/explain/practice 데이터 자체의 무결성 — 렌더링된 HTML이
# 아니라 tools/web/deck_u3.LESSONS를 직접 검사한다.
U3_THEORY_ONLY={'ml-overview','ml-use','ml-process','ml-terms','ml-methods'}
for lid, ldata in deck_u3.LESSONS.items():
 for sl in ldata.get('slides', ()):
  assert sl.get('explain'), ('u3 슬라이드에 explain 없음', lid, sl['n'])
 practice_items=ldata.get('practice') or []
 if lid in U3_THEORY_ONLY:
  assert not practice_items, ('이론 소단원인데 practice가 있음', lid)
 for it in practice_items:
  if isinstance(it, str):
   assert it in examples, ('u3 practice가 참조하는 예제 없음', lid, it)
  else:
   assert it.get('kind')=='tutorial', ('u3 practice dict는 튜토리얼이어야 함', lid, it)
   assert it.get('id') and it.get('title'), ('u3 튜토리얼에 id/title 없음', lid, it)
   assert len(it.get('steps') or ())>=1, ('u3 튜토리얼 steps가 비어 있음', lid, it.get('id'))
   for st in it['steps']:
    assert st.get('text'), ('u3 튜토리얼 step에 text 없음', lid, it['id'])
unit_index=(WEB/'units/unit01/index.html').read_text()
assert 'data-lessons=' in unit_index
assert 'overview.html' in unit_index
assert 'id="topic-index-title"' in unit_index
# (#131) 2단원 GUI 비교 갤러리·부록(pyside/wx/kivy) 관련 옛 검증 블록을 통째로
# 제거했다 — 위 새 for 루프의 deck-slide·banned-library 검사로 대체됐다.
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
# (#131) 3단원 ml-* density/pre_api/tips/screenshots 옛 검증 블록을 제거했다 —
# 위 새 for 루프의 deck-slide·banned-library 검사로 대체됐다.
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
# (#131) 2단원 'libraries' 갤러리 페이지(pyqt/ttk/wx/kivy pre-api) 검증은 갤러리
# 삭제와 함께 뺐다 — 위 새 for 루프의 deck-slide·banned-library 검사로 대체됐다.
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
assert "collection(db, name)" in teacher_board
assert "byGrade('progress')" in teacher_board
assert "byGrade('roster')" in teacher_board
assert "byGrade('feedback')" in teacher_board
assert "where('grade', '==', parsed.grade)" in teacher_board
assert "collection(db, 'helpRequests')" in teacher_board
assert "collection(db, 'presence')" in teacher_board
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

# (#126) 화면 단위 따라가기 블록 표식: 학생 페이지(teacher/ 아래는 교사 관리 화면이라 제외)의
# data-fb 값은 페이지 안에서 유일해야 하고 항상 'b{정수}' 형식이어야 한다. follow-model.js의
# 블록 앵커('{id}~b{n}@{비율}')가 이 값을 그대로 참조하므로 형식이 깨지면 스크롤 위치가 틀어진다.
FB_RE=re.compile(r'data-fb="([^"]*)"')
FB_VALUE_RE=re.compile(r'^b\d+$')
fb_pages_checked=0
fb_blocks_total=0
for p in WEB.rglob('*.html'):
 if 'teacher' in p.relative_to(WEB).parts:continue
 values=FB_RE.findall(p.read_text())
 if not values:continue
 fb_pages_checked+=1
 fb_blocks_total+=len(values)
 for v in values:
  assert FB_VALUE_RE.match(v),(p,'data-fb 형식이 아님',v)
 assert len(values)==len(set(values)),(p,'data-fb 중복',values)
assert fb_pages_checked>0,'data-fb가 매겨진 학생 페이지가 없음'

# (#132) 실행 결과 매니페스트(tools/web/render_results.py 산출물): id가 실제
# 예제·튜토리얼을 가리키는지, img 경로가 web/ 아래에 실제로 존재하는지 확인한다.
# 매니페스트가 없으면(아직 한 번도 안 돌렸으면) 전체를 건너뛴다 — build.py도 같은
# 방식으로 조용히 생략하므로 이 스크립트가 필수 전제 조건이 되지 않게 한다.
results_path=Path(__file__).parent/'results.json'
if results_path.is_file():
 results=json.loads(results_path.read_text())
 tutorial_ids=set()
 import deck_u2,deck_u3
 for deck in (deck_u2.LESSONS, deck_u3.LESSONS):
  for lesson in deck.values():
   for it in (lesson.get('practice') or []):
    if isinstance(it,dict) and it.get('kind')=='tutorial':
     tutorial_ids.add(it['id'])
 assert results,'results.json이 비어 있음(생성 실패 의심)'
 for rid,entry in results.items():
  assert rid in examples or rid in tutorial_ids,(rid,'results.json의 id가 예제·튜토리얼 어디에도 없음')
  assert set(entry)<={'img','text'},(rid,'알 수 없는 키',entry)
  if 'text' in entry:
   assert isinstance(entry['text'],str) and entry['text'].strip(),(rid,'text가 비어 있음')
  for img in entry.get('img') or []:
   assert img.startswith('assets/results/'),(rid,img)
   assert (WEB/img).is_file(),(rid,img,'파일 없음')
   assert (WEB/img).stat().st_size>200,(rid,img,'파일이 너무 작음')
 print(f'PASS: results.json {len(results)} entries checked ({sum(len(v.get("img") or []) for v in results.values())} images).')

print(f'PASS: {len(examples)} example syntax checks; all browser Python examples; {len(questions)} question records and executable answers; internal links and ZIP archives; {fb_blocks_total} focus blocks across {fb_pages_checked} student pages.')
