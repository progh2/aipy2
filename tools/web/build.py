"""Build static GitHub Pages site: python3 tools/web/build.py"""
from pathlib import Path
from html import escape as esc
import json, zipfile
from content import units, examples, questions
import questions as question_bank
import mascot
import later_units
import learning_design as design
import textbook
textbook.attach(units)
teacher_notes=design.prepare(units)
for u in units:
 (Path(__file__).resolve().parents[2]/f"web/units/unit0{u}").mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[2]
WEB=ROOT/'web'

def dump(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def nav(prefix): return f'''<a class="skip" href="#main">본문으로 건너뛰기</a><header class="top"><a class="brand" href="{prefix}index.html">{mascot.image(prefix,"welcome","eager","pai-brand")}인공지능 파이썬 실무</a><nav aria-label="주 메뉴"><a href="{prefix}before-you-start.html">시작하기 전에</a><a href="{prefix}units/unit01/index.html">Ⅰ 모듈</a><a href="{prefix}units/unit02/index.html">Ⅱ GUI</a><a href="{prefix}units/unit03/index.html">Ⅲ ML</a><a href="{prefix}units/unit04/index.html">Ⅳ CV</a></nav></header>'''
def layout(title,body,prefix='',unit=0): return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · AI Python Lab</title><meta name="description" content="교과서와 함께 배우는 인공지능 파이썬 실무. 모듈·GUI·머신러닝·컴퓨터 비전의 시각 자료와 코드 실습."><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/mascot.css"><link rel="stylesheet" href="{prefix}assets/learning-design.css"></head><body data-unit="{unit}" data-prefix="{prefix}">{nav(prefix)}{body}<footer><p>미림마이스터고등학교 · 2학년 · 함기훈 선생님</p><p>교과서: 멘토르 「인공지능 파이썬 실무」 · 2026학년도 2학기 운영 계획 기반</p><a href="{prefix}teacher/index.html">교사용 수업 요약</a> · <a href="{prefix}mascot.html">우리 과목 친구 파이</a> · <a href="{prefix}sources.html">출처·교과서 대응표·보완 사항</a> · <a href="https://www.mtrschool.co.kr/post/3095" target="_blank" rel="noopener">멘토르 교과서 안내 ↗</a></footer><div id="toast" role="status" aria-live="polite"></div><script src="{prefix}assets/app.js?v=visual4" defer></script><script src="{prefix}assets/learning-design.js?v=1" defer></script></body></html>'''

def progress_tools(): return '''<div class="record-tools"><button data-export>학습 기록 내보내기</button><label class="file-button">기록 불러오기<input type="file" data-import accept="application/json,.json"></label><button data-clear>이 브라우저의 기록 지우기</button></div><p class="small">코드·풀이·저널은 이 브라우저에 저장됩니다. 다른 PC에서는 기록 파일을 불러오세요. 공용 PC에서는 내보낸 뒤 기록을 지우세요. 서버로 제출되거나 공식 성적으로 처리되지 않습니다.</p>'''

home='''<main id="main"><section class="hero home-hero"><div><p class="eyebrow">2026 · SECOND SEMESTER / PYTHON LAB</p><h1>읽고, 바꾸고,<br><em>직접 만들어 보세요.</em></h1><p class="lead">교과서의 한 줄이 나만의 프로그램이 될 때까지.<br>모듈부터 머신러닝·컴퓨터 비전까지, 손으로 익히는 파이썬 실습실.</p><div class="actions"><a class="button primary" href="units/unit01/index.html">1단원 시작하기 <span>↗</span></a><a class="button" id="resume" href="before-you-start.html">이어서 학습하기 →</a></div><div class="hero-stats"><span><b>04</b> 학습 단원</span><span><b>{QUESTION_COUNT}</b> 연습 문제</span><span><b>06</b> GUI 비교 화면</span></div></div><div class="code-art" aria-label="모듈과 GUI를 연결하는 코드 예시"><div class="code-top"><span>● ● ●</span><span>my_first_app.py</span></div><pre><span class="dim"># 배운 기능을 앱으로 연결하기</span>
<span class="gold">from</span> core.logic <span class="gold">import</span> roll

<span class="gold">def</span> on_click():
    result = roll(<span class="mint">6</span>)
    label.setText(str(result))

button.clicked.connect(on_click)</pre><div class="art-output"><span class="status-dot"></span>아이디어 → 코드 → 실행 → 내 것으로</div><div class="art-card"><span>STEP 02</span><b>같은 기능, 두 가지 GUI</b><small>tkinter ↔ PySide6</small></div></div></section><section class="section" aria-labelledby="path-title"><div class="section-head"><div><p class="eyebrow">YOUR LEARNING PATH</p><h2 id="path-title">오늘은 어디부터 시작할까요?</h2></div><span class="pill">개념 → 실습 → 도전</span></div><a class="prep-card" href="before-you-start.html"><span class="number">00</span><div><h3>시작하기 전에</h3><p>Python · VS Code · Git · 디버깅 · AI 도구 설정을 준비하세요.</p></div><span>환경 준비하기 ↗</span></a><div class="course-grid">'''
for u,title,desc,tags in [(1,'모듈과 패키지 활용','코드를 나누고 연결하면서 재사용 가능한 나만의 도구를 만듭니다.',['다중 파일 실행','표준 라이브러리','60문제']),(2,'GUI 프로그래밍','tkinter로 원리를 익히고, 같은 앱을 PySide6로 확장합니다.',['실제 화면 비교','메모장 만들기','70문제']),(3,'파이썬과 머신러닝','데이터를 준비하고 모델을 학습·평가하며 그래프로 비교합니다.',['분할·전처리','모델·평가','시각 실험']),(4,'파이썬과 컴퓨터 비전','픽셀을 조작하고 이미지 처리에서 객체 검출까지 연결합니다.',['픽셀 실험실','필터·변환','Haar·YOLO'])]:
 home+=f'''<a class="course-card" href="units/unit0{u}/index.html"><div class="course-top"><span class="number">{textbook.ROMAN[u]}</span><span class="arrow">↗</span></div><h3>{title}</h3><p>교과서 {textbook.BOOK[u][1]}쪽 · 2개 중단원</p><p>{desc}</p><div class="tags">{''.join(f'<span>{t}</span>' for t in tags)}</div><div class="progress-label"><span>학습 진행</span><span data-unit-progress="{u}" data-total="{len(units[u])}">0%</span></div><progress data-unit-bar="{u}" max="100" value="0" aria-label="{u}단원 진행도"></progress></a>'''
home+='''</div><p style="margin:24px 0"><a href="https://www.mtrschool.co.kr/post/3095" target="_blank" rel="noopener">멘토르 「인공지능 파이썬 실무」 교과서 안내 ↗</a> · <a href="sources.html">교과서와 실습 대응표</a></p><p><a class="button" href="teacher/index.html">교사용 수업 요약 →</a></p></section><section class="section record"><p class="eyebrow">MY WORKSPACE</p><h2>내 학습 기록</h2>'''+progress_tools()+'''</section></main>'''
# Replace the homepage illustration with the course mascot; examples remain in lessons.
start=home.index('<div class="code-art"')
end=home.index('</section><section class="section"',start)
home=home[:start]+mascot.hero()+home[end:]
home=home.replace('{QUESTION_COUNT}',str(len(questions)))
(WEB/'index.html').write_text(layout('실습실',home))
(WEB/'mascot.html').write_text(layout('대표 캐릭터 파이',mascot.intro_page()))
with zipfile.ZipFile(WEB/'downloads/pai-character-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
 for mood in mascot.MOODS:
  name=f'pai-{mood}-v1.png'
  z.write(WEB/'assets/mascot'/name,name)
 z.write(WEB/'assets/mascot/CREATION.md','CREATION.md')
 z.writestr('README.md','# 파이 · 개발자를 꿈꾸는 여학생 / 인공지능 파이썬 실무 대표 캐릭터\n\nwelcome: 시작 / thinking: 결과 예상 / idea: 핵심 개념 / debug: 오류 원인 찾기 / celebrate: 학습 완료\n\n원본은 흰 배경 PNG입니다. 학생이 지금 해야 할 일을 짧은 문장으로 옆에 적어 사용하세요.\n')

pairs=[('hello-tk','hello-pyside','첫 인사 앱'),('widgets-tk','widgets-pyside','위젯 도감'),('layout-tk','layout-pyside','레이아웃'),('memo-tk','memo-pyside','메모장'),('project-tk','project-pyside','생활 도우미'),('memo-plus-tk','memo-plus-pyside','개선 메모장')]

def editor_markup(u): return f'''<section class="lab" id="lab"><div class="section-head"><div><p class="eyebrow">CODE WORKSPACE</p><h2>코드를 바꾸는 실습실</h2></div><span class="pill" id="run-mode">실행 환경</span></div><label>예제 선택<select id="example-select" aria-label="예제 선택"></select></label><p id="example-note" class="note"></p>{mascot.runtime_guide(u)}<div class="editor-layout"><aside class="file-panel"><p class="eyebrow">PROJECT FILES</p><div id="file-tree"></div><button id="add-file">+ 파일 추가</button><button id="delete-file">현재 파일 삭제</button></aside><div class="editor-main"><div class="editor-bar"><strong id="file-name">main.py</strong><div><button id="copy-code">복사</button><button id="download-file">파일 저장</button></div></div><label class="sr-only" for="code-editor">Python 소스 편집기</label><textarea id="code-editor" spellcheck="false" autocapitalize="off"></textarea></div></div><div class="input-grid"><label>실행 파일<select id="entry-file"></select></label><label>input()에 전달할 값 · 한 줄에 하나<textarea id="stdin" rows="2" placeholder="6"></textarea></label><label>실행 인자 · JSON 문자열 배열<input id="argv" value='[]' placeholder='["param1", "param2"]'></label></div><div class="actions"><button class="primary" id="run">Python 실행</button><button id="check-example">검사</button><button id="stop" disabled>중지</button><button id="reset-code">예제 원본 복원</button><button id="download-project">프로젝트 ZIP</button></div><p class="small" id="runtime-info">실행 엔진은 처음 실행할 때 내려받습니다. 패키지 크기에 따라 최초 준비에 최대 3분이 걸릴 수 있으며 네트워크가 필요합니다. 실행은 최대 30초이며 중지 후 다시 실행할 수 있습니다.</p><div id="plot-output" class="plot-output" aria-live="polite"></div><pre id="output" role="status" aria-live="polite">실행할 예제를 선택하세요.</pre></section>'''

def practice(u): return f'''<section id="practice" class="section exercise-section"><p class="eyebrow">PRACTICE / RETRY / UNDERSTAND</p><h2>연습 문제 <span class="count">{sum(q['unit']==u for q in questions)}</span></h2><p>실행 검사는 결과와 입력 조건을 확인합니다. 빈칸은 대표 답안과 비교하며, 다른 표현은 해설을 보고 판단하세요. GUI 코드는 PC 실행 점검까지 마치세요.</p>{mascot.card("../../","thinking","먼저 예상하고, 힌트는 한 단계씩 열어 보세요.","답을 확인한 다음에는 조건을 바꾸어 다시 풀어 보세요. 다른 올바른 풀이도 있을 수 있어요.","practice")}<div class="filter-row"><label>유형<select id="question-kind"><option value="">모든 유형</option></select></label><label>상태<select id="question-status"><option value="">전체</option><option value="todo">미완료</option><option value="retry">다시 풀기</option><option value="done">완료</option></select></label><label>검색<input id="question-search" type="search" placeholder="예: 임포트, 메모장"></label></div><p id="question-summary" aria-live="polite"></p><div id="questions"></div><div class="actions"><button id="previous-questions">← 이전 문제</button><span id="question-page"></span><button id="next-questions">다음 문제 →</button></div></section>'''

def simulator(): return '''<section id="simulator" class="section"><p class="eyebrow">INTERACTIVE GUI CONCEPTS</p><h2>눈으로 확인하는 이벤트와 배치</h2><p class="note">학습용 웹 시뮬레이션입니다. 아래 조작은 정해진 예제의 동작을 재현하며, 편집한 Python 코드를 실행하지 않습니다. 실제 tkinter·PySide6 창은 프로젝트를 내려받아 PC에서 실행하세요.</p><div class="sim-grid"><div class="demo-window"><div class="code-top">인사 앱 · 동작 체험</div><div class="demo-body"><label>이름<input id="demo-name" placeholder="이름을 입력하세요"></label><div class="actions"><button id="demo-greet" class="primary">인사하기</button><button id="demo-reset">초기화</button></div><p id="demo-result" aria-live="polite">이름을 입력하세요.</p><pre id="event-log">이벤트를 기다립니다.</pre></div></div><div class="demo-window"><div class="code-top">레이아웃 · 동작 체험</div><div class="demo-body"><label>배치 방식<select id="demo-layout"><option value="vertical">수직 · pack / QVBoxLayout</option><option value="horizontal">수평 · pack(side) / QHBoxLayout</option><option value="grid">격자 · grid / QGridLayout</option></select></label><div id="layout-preview" class="vertical"><button>A</button><button>B</button><button>C</button><button>D</button></div><p class="small">창 너비를 바꿔 배치 변화를 확인하세요.</p></div></div></div><div class="demo-window memo-demo"><div class="code-top">메모장 · 웹 동작 체험</div><div class="demo-body"><div class="actions"><label class="file-button">텍스트 열기<input type="file" id="demo-open" accept="text/plain,.txt"></label><button id="demo-save">텍스트 저장</button><button id="demo-new">새 문서</button></div><label for="demo-memo">메모 내용</label><textarea id="demo-memo" rows="6" placeholder="한글을 입력하고 저장한 뒤 다시 열어 보세요."></textarea><p id="demo-stats" aria-live="polite">0자 · 0줄</p></div></div></section>'''

gallery_items=[('tk','tkinter','Tcl/Tk 8.6','기본 위젯 · 간단한 도구','hello-tk'),('ttk','tkinter + ttk','Tcl/Tk 8.6','테마 위젯 · tkinter 확장','hello-ttk'),('pyside','PySide6','6.11.2 / Qt 6.11.2','Qt 공식 바인딩 · Qt Widgets','hello-pyside'),('pyqt','PyQt6','6.11.0 / Qt 6.11.2','Qt 바인딩 · 풍부한 위젯','hello-pyqt'),('wx','wxPython','4.2.3 / wxWidgets 3.2','OS 위젯 · 데스크톱 도구','hello-wx'),('kivy','Kivy','2.3.1','자체 렌더링 · 터치 UI','hello-kivy')]
def gallery():
 s='<section id="gallery" class="section"><p class="eyebrow">SAME TASK, DIFFERENT TOOLKITS</p><h2>실제 실행 화면으로 비교하세요.</h2><p>모두 이름 입력·인사·초기화 기능을 갖춘 앱입니다. Linux 가상 디스플레이에서 제공 소스를 실행해 캡처했습니다. OS·테마에 따라 외형은 달라집니다. Kivy 예제는 기본 글꼴에서도 보이도록 영어 문구를 사용합니다.</p><div class="gallery-grid">'
 for id,title,version,desc,example in gallery_items:
  s+=f'<article class="gallery-card"><a href="../../assets/screenshots/{id}.png" target="_blank" rel="noopener"><img src="../../assets/screenshots/{id}.png" loading="lazy" alt="{title} 인사 앱 실제 실행 화면 · 이름 입력창과 인사 및 초기화 버튼"></a><div><h3>{title}</h3><p>교과서 {textbook.BOOK[u][1]}쪽 · 2개 중단원</p><p>{desc}</p><small>{version}</small><button data-example="{example}">코드 열기 ↗</button></div></article>'
 s+='</div><h3>같은 기능의 코드 나란히 보기</h3><label>비교할 앱<select id="compare-select">'+''.join(f'<option value="{i}">{title}</option>' for i,(_,_,title) in enumerate(pairs))+'</select></label><div class="actions" role="group" aria-label="코드 보기 방식"><button data-view="both" aria-pressed="true">나란히</button><button data-view="tk" aria-pressed="false">tkinter</button><button data-view="qt" aria-pressed="false">PySide6</button></div><div id="compare" class="compare-grid"><div data-side="tk"><h4>tkinter</h4><pre id="compare-tk"></pre></div><div data-side="qt"><h4>PySide6</h4><pre id="compare-qt"></pre></div></div><p>위젯 도감·레이아웃·메모장·생활 도우미까지 같은 개념을 대응하여 볼 수 있습니다. 실제 수정과 파일 다운로드는 실습실에서 진행하세요.</p></section>'
 return s

for u,lessons in units.items():
 prefix='../../'
 title=design.META[u][0]
 ids=list(dict.fromkeys(e for l in lessons for e in l['examples']))
 dump(WEB/f'data/unit{u}.json',dict(unit=u,lessons=lessons,examples={k:examples[k] for k in ids},questions=[q for q in questions if q['unit']==u],pairs=pairs if u==2 else []))
 rail=textbook.toc(u,lessons)
 body=f'<section class="unit-hero pai-unit-hero">{mascot.image(prefix,"idea" if u==1 else "welcome","eager","pai-unit-image")}<p class="eyebrow">UNIT 0{u} / LEARN BY DOING</p><h1>{textbook.unit_label(u)}</h1><p>{design.META[u][2]}</p><div class="tags"><span>교과서 {design.META[u][1]}쪽</span><span>{len(lessons)}개 학습 주제</span></div><div class="actions"><a class="button" href="summary.html">그림으로 정리</a><a class="button primary" href="#lab">실습실 바로가기</a><a class="button" href="#practice">문제 풀기</a><a class="button" href="../../downloads/unit{u}-examples.zip">전체 예제 ZIP ↓</a></div></section><div class="course-layout"><aside class="rail"><p class="eyebrow">교과서 목차</p>{rail}<a href="#lab">코드 실습실</a>'+('<a href="#gallery">GUI 비교 갤러리</a><a href="#simulator">웹 동작 체험</a>' if u==2 else '')+'<a href="#practice">연습 문제</a><a href="#journal">학습 저널</a></aside><main id="main">'
 body+=design.experiments(u)
 for i,l in enumerate(lessons):
  body+=f'<section class="lesson" id="{l["id"]}">{textbook.badge(u,l)}<p class="eyebrow">웹 학습 주제 {i+1:02}</p><h2>{esc(l["title"])}</h2><p class="lesson-lead">{esc(l["lead"])}</p>'+design.visual(u,l)+'<details class="lesson-details"><summary>개념 더 읽기</summary>'+''.join(f'<p>{esc(p)}</p>' for p in l['paragraphs'])+'</details>'
  body+=mascot.lesson_tip(u,l['id'],prefix)
  if l['examples']:
   body+='<div class="example-links">'+''.join(f'<button data-example="{e}"><span>{"▶ 웹 실행" if examples[e]["mode"]=="web" else "↗ PC 실습"}</span>{esc(examples[e]["title"])}</button>' for e in l['examples'])+'</div>'
  if l['tasks']: body+='<div class="task-box"><h3>직접 해 보세요</h3><ol>'+''.join(f'<li>{esc(t)}</li>' for t in l['tasks'])+'</ol></div>'
  body+=f'<label class="completion"><input type="checkbox" data-complete="u{u}-{l["id"]}"> 이 주제를 실습하고 설명할 수 있습니다.</label></section>'
 body+=editor_markup(u)
 if u==2: body+=gallery()+simulator()
 body+=practice(u)+f'''<section id="journal" class="section record"><p class="eyebrow">LEARNING JOURNAL</p><h2>오늘 배운 것을 내 말로</h2>{mascot.card(prefix,"celebrate","배운 이유를 내 말로 남겨 볼까요?","처음 예상과 달랐던 점, 바꾼 코드, 다시 확인한 결과를 적으면 다음 실습의 힌트가 됩니다.","journal")}<label>오늘 이해한 개념<textarea data-journal="u{u}-learn" rows="3"></textarea></label><label>발생한 오류 · 원인 · 해결 근거<textarea data-journal="u{u}-error" rows="3"></textarea></label><label>시험한 입력과 결과 · 다음에 도전할 것<textarea data-journal="u{u}-next" rows="3"></textarea></label><button id="download-journal">저널 Markdown 저장</button>'''+progress_tools()+'</section><div class="actions end-nav">'+(f'<a class="button primary" href="../unit0{u+1}/index.html">다음: {design.META[u+1][0]} →</a>' if u<4 else '<a class="button" href="../../index.html">전체 단원으로 →</a>')+'</div></main></div>'
 (WEB/f'units/unit0{u}/index.html').write_text(layout(title,body,prefix,u))
 with zipfile.ZipFile(WEB/f'downloads/unit{u}-examples.zip','w',zipfile.ZIP_DEFLATED) as z:
  for id in ids:
   e=examples[id]
   for name,source in e['files'].items(): z.writestr(f'{id}/{name}',source)
   packages='PySide6' if 'pyside' in id else 'PyQt6' if 'pyqt' in id else 'wxPython' if '-wx' in id else 'Kivy' if 'kivy' in id else 'numpy' if id=='thirdparty' else ''
   packages=e['files'].get('requirements.txt',packages).strip().replace('\n',' ')
   if packages and 'requirements.txt' not in e['files']: z.writestr(f'{id}/requirements.txt',packages+'\n')
   z.writestr(f'{id}/README.md',f'# {e["title"]}\n\n이 폴더를 VS Code로 열고 `python {e["entry"]}`로 실행하세요.\n'+(f'먼저 가상환경에서 `python -m pip install -r requirements.txt`로 {packages}를 설치하세요.\n' if packages else '')+f'\n{e["note"]}\n')
  z.writestr('README.md','각 예제의 폴더를 따로 열어 실행하세요. tkinter는 일부 Linux에서 python3-tk 설치가 필요합니다.\n웹 예제의 input 값은 사이트에 안내되어 있습니다. 실행 인자 sys 예제: python main.py param1 param2\n')

sourcebody='<main id="main" class="source-page"><p class="eyebrow">SOURCES & COVERAGE</p><h1>출처와 학습 범위</h1><p>멘토르 「인공지능 파이썬 실무」 PDF와 2026학년도 2학기 교수·학습 및 평가 운영 계획 _g를 바탕으로 작성했습니다. 교과서 개념·예제·문항의 학습 목표를 웹 실습으로 재구성하고, 확장 내용은 표시했습니다. 원본 교과서 PDF는 사이트에 배포하지 않습니다.</p><h2>교과서 목차와 웹 실습 대응표</h2><p>교과서 4–5쪽 목차의 명칭과 번호를 따릅니다. 쪽수는 책에 인쇄된 페이지 기준이며, 범위는 다음 절 시작 전까지입니다. 대단원 범위에는 도입을 포함합니다. 한 웹 주제가 여러 소단원을 함께 다루면 각 소단원에 같은 실습 링크가 표시됩니다.</p>'
for u,ls in units.items(): sourcebody+=textbook.toc(u,ls,f'units/unit0{u}/index.html')
sourcebody+='<p><a href="teacher/index.html">교과서 정답·설명 보완 사항은 교사용 요약에 정리했습니다.</a></p><h2>공식 참고 자료</h2><ul>'
for title,url in [('멘토르 인공지능 파이썬 실무 교과서','https://www.mtrschool.co.kr/post/3095'),('Python 모듈과 패키지','https://docs.python.org/ko/3/tutorial/modules.html'),('Python 표준 라이브러리','https://docs.python.org/ko/3/library/'),('random의 정확한 동작','https://docs.python.org/3/library/random.html'),('tkinter와 ttk','https://docs.python.org/3/library/tkinter.html'),('PySide6 시작하기','https://doc.qt.io/qtforpython-6/gettingstarted.html'),('Qt 시그널과 슬롯','https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html'),('PyQt','https://www.riverbankcomputing.com/software/pyqt/'),('wxPython','https://wxpython.org/'),('Kivy','https://kivy.org/doc/stable/'),('scikit-learn 데이터 누수와 전처리','https://scikit-learn.org/stable/common_pitfalls.html'),('OpenCV 공식 튜토리얼','https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html'),('Ultralytics 예측 결과','https://docs.ultralytics.com/modes/predict/'),('PyPI','https://pypi.org/'),('Pyodide 브라우저 제약','https://pyodide.org/en/stable/usage/wasm-constraints.html')]: sourcebody+=f'<li><a href="{url}" target="_blank" rel="noopener">{title} ↗</a></li>'
sourcebody+='</ul><p><a href="teacher/index.html">수업 운영·평가 연결은 교사용 요약에서 확인하세요.</a></p><h2>실행 환경</h2><p>브라우저 Python은 Pyodide 0.27.7을 고정하여 사용합니다. 최초 실행에는 CDN 접속이 필요합니다. 다중 파일 실행은 가상 폴더에서 진행합니다. GUI는 코드 문법 확인과 웹 시뮬레이션을 제공하며 실제 동작은 PC에서 확인합니다.</p></main>'
(WEB/'sources.html').write_text(layout('출처와 대응표',sourcebody))
design.teacher_pages(WEB,layout,units,teacher_notes)
(WEB/'.nojekyll').touch()
print(f'Built {len(examples)} examples / {len(questions)} questions / {sum(map(len,units.values()))} lessons')
