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
board_model=(WEB/'assets/board-model.js').read_text()
assert 'CSV 내보내기' not in board_model
assert '학번' in board_model
assert '1분 이내' in board_model and '3분 이내' in board_model
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
assert 'data-complete="u1-overview"' in unit
assert 'class="completion"' in unit
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
assert 'ops.js?v=2' in ops_html
assert 'id="ops-year"' in ops_html
assert 'id="ops-promote"' in ops_html
assert 'id="ops-archive"' in ops_html
assert 'id="ops-remove"' in ops_html
assert 'id="ops-export"' in ops_html
assert '입학년도' in ops_html
assert '입학년도로 학생을 모아요. 진급 때는 학년·반만 바꾸고, 입학년도와 학습 기록은 그대로 이어져요.' in ops_html
assert '진급 반영' in ops_html
assert '요약 CSV 내보내기' in ops_html
assert '코호트 보관' in ops_html
assert '명단에서만 제거' in ops_html
assert '나래 스모크' in ops_html
assert '입학년도는 그대로예요. 학년·반만 바뀌고 이전 학습 기록이 이어져요.' in ops_html
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
assert '권한을 확인하지 못했습니다. 네트워크를 확인하고 새로고침하세요.' in ops_js
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
assert '성적·출결에는 들어가지 않아요.' in privacy_model
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
app_js=(WEB/'assets/app.js').read_text()
assert 'onLocalChange' in app_js
assert "save('complete')" in app_js
assert "save('code')" in app_js
assert 'applyRemote' in app_js
auth_js=(WEB/'assets/auth.js').read_text()
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
print(f'PASS: {len(examples)} example syntax checks; all browser Python examples; {len(questions)} question records and executable answers; internal links and ZIP archives.')
