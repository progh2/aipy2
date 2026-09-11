"""Shared visual explanations and separate teacher notes, all authored for this course."""
from html import escape as esc
import textbook
META={1:('모듈과 패키지 활용','6–39','기능을 나누고 연결하기'),2:('GUI 프로그래밍','40–59','입력·이벤트·출력 연결하기'),3:('파이썬과 머신러닝','60–131','데이터로 학습하고 새 데이터로 평가하기'),4:('파이썬과 컴퓨터 비전','132–195','픽셀에서 특징과 검출까지')}
# title, process cards, table headings, table rows. Diagram labels are also readable text.
VISUALS={
'overview':('파일과 폴더로 보는 재사용',['main.py｜기능을 사용하는 입구','calculator.py｜add 함수를 정의','다른 앱｜같은 함수를 다시 사용'],['구조','비유','예'],[['모듈','기능 상자','calculator.py'],['패키지','상자를 묶은 서랍','nature/animals/'],['라이브러리','재사용 도구 모음','표준 라이브러리']]),
'define':('정의와 호출의 실행 시점',['import｜파일의 최상위 실행','def / class｜이름과 기능 정의','함수 호출｜본문 실행'],['코드 위치','임포트할 때','호출할 때'],[['최상위 print','출력','자동 반복 안 함'],['def 안의 print','정의만 준비','출력'],['class 안 메서드','메서드 정의','메서드 본문 실행']]),
'entrypoint':('같은 파일, 두 가지 역할',['직접 실행｜__name__ = "__main__"','조건 비교｜이름이 __main__인가?','참이면｜시험용 코드 실행'],['실행 방법','__name__','main 가드'],[['python circle.py','__main__','실행'],['import circle','circle','건너뜀'],['최상위 실행문','두 경우 모두','가드 밖이면 실행']]),
'imports':('불러온 이름이 호출법을 결정해요',['greet.py｜hello 정의','임포트 문｜현재 이름 연결','현재 코드｜연결한 이름으로 호출'],['임포트','연결된 이름','호출'],[['import greet','greet','greet.hello()'],['import greet as g','g','g.hello()'],['from greet import hello','hello','hello()'],['from greet import hello as h','h','h()']]),
'packages':('폴더 경로와 점 경로 연결',['nature/｜패키지','animals/｜하위 패키지','bird.py｜모듈','wild()｜함수'],['표현','대상','호출 예'],[['nature.animals.bird','모듈 경로','nature.animals.bird.wild()'],['from nature.animals import bird','bird 모듈','bird.wild()'],['__all__ = ["bird"]','별표 임포트 이름','명시적 임포트는 별개']]),
'os-sys':('환경과 실행 인자를 구별해요',['터미널｜python main.py A B','sys.argv｜[파일명, A, B]','os.getcwd()｜파일을 찾는 기준 위치'],['도구','알아내는 것','주의'],[['os.getcwd()','현재 작업 폴더','소스 파일 폴더와 다를 수 있음'],['os.listdir()','폴더 안 이름','웹에서는 가상 파일'],['sys.argv','실행 인자','모든 인자는 문자열'],['sys.exit()','실행 종료','아래 코드는 실행 안 됨']]),
'math':('음수에서도 올림과 내림은 방향으로',['−4｜floor(−3.5)','−3.5｜원래 값','−3｜ceil(−3.5)'],['함수','역할','예'],[['floor','작거나 같은 최대 정수','floor(-3.5) → -4'],['ceil','크거나 같은 최소 정수','ceil(-3.5) → -3'],['sqrt','제곱근','sqrt(81) → 9.0'],['gcd / factorial','최대공약수 / 팩토리얼','gcd(12,18) → 6']]),
'random':('난수 도구는 결과의 조건으로 골라요',['숫자 하나?｜randint / randrange','항목 하나?｜choice','여러 항목?｜sample','순서 변경?｜shuffle'],['함수','포함 범위 / 변화','반환'],[['randint(1,6)','1과 6 포함','정수'],['randrange(1,6)','6 제외','정수'],['sample(L,2)','위치 중복 없이 추출','새 리스트'],['shuffle(L)','원본 순서 변경','None']]),
'datetime':('문자열에서 날짜 계산까지',['"2026-12-25"｜문자열','date.fromisoformat｜날짜로 변환','날짜 − 날짜｜timedelta','days｜일수 꺼내기'],['도구','결과','주의'],[['date.today()','오늘 날짜','실행 날짜에 따라 다름'],['weekday()','월 0 … 일 6','요일 이름은 따로 대응'],['strftime()','표시용 문자열','계산은 날짜 상태에서'],['timedelta(days=1)','하루 간격','월말·윤년 자동 처리']]),
 'thirdparty':('설치 이름과 임포트 이름은 다를 수 있어요',['가상환경 선택','python -m pip install 패키지','같은 Python으로 import','짧은 예제로 동작 확인'],['설치','임포트','용도'],[['numpy','numpy','수치 배열'],['pillow','PIL','이미지 처리'],['beautifulsoup4','bs4','HTML 분석'],['scikit-learn','sklearn','머신러닝']]),
'ui':('사용자가 명령을 전달하는 방법',['사용자 의도','인터페이스에서 입력','프로그램 처리','결과와 상태 표시'],['종류','입력 예','특징'],[['CLI','명령어 타이핑','정확한 명령 필요'],['GUI','버튼 클릭','시각적으로 선택'],['NUI','음성·몸짓','자연스러운 상호작용']]),
'libraries':('같은 앱, 다른 GUI 도구',['공통 기능｜이름 받아 인사','화면 도구 선택','위젯과 이벤트 연결','실제 PC에서 비교'],['도구','화면 구성','학습 경로'],[['tkinter / ttk','Tk 위젯 / 테마 위젯','교과서 기본'],['PySide6 / PyQt6','Qt 위젯과 레이아웃','동일 개념 확장'],['wxPython','OS 위젯 활용','데스크톱 비교'],['Kivy','자체 그리기','터치 UI 비교']]),
'widgets':('위젯의 역할을 맞춰 보세요',['Entry / QLineEdit｜입력','Button / QPushButton｜실행 요청','Label / QLabel｜짧은 출력','Text / QPlainTextEdit｜여러 줄'],['역할','tkinter','PySide6'],[['최상위 창','Tk','QWidget / QMainWindow'],['그룹','Frame','QWidget + Layout'],['입력 읽기','entry.get()','edit.text()'],['표시 바꾸기','label.config(text=...)','label.setText(...)']]),
'layout':('좌표보다 배치 규칙을 먼저 정해요',['세로 묶음｜pack / QVBoxLayout','가로 묶음｜pack(side) / QHBoxLayout','행과 열｜grid / QGridLayout'],['선택','적합한 화면','확인할 것'],[['세로·가로 배치','버튼 모음','순서와 늘어남'],['격자 배치','입력 폼','행·열 번호'],['고정 좌표 place','정해진 위치','창 크기 변화에 취약']]),
'events':('클릭은 함수를 예약한 뒤에 발생해요',['1 연결｜command=hello','2 대기｜mainloop()','3 입력｜버튼 클릭','4 처리｜hello() 실행'],['코드','실행 시점','결과'],[['command=hello','클릭할 때','함수를 전달'],['command=hello()','화면 만들 때','반환값을 전달'],['clicked.connect(hello)','Qt 클릭할 때','시그널과 슬롯 연결']]),
'memo':('열기·저장·취소의 분기',['파일 대화상자','취소?｜화면 그대로','경로 선택?｜UTF-8 읽기/쓰기','내용과 상태 갱신'],['작업','입력','출력'],[['열기','파일 경로','Text 영역 내용'],['저장','Text 영역 내용','UTF-8 파일'],['취소','빈 경로','아무 파일도 변경 안 함'],['읽기 실패','OSError','오류 안내']]),
'pyside':('tkinter 개념을 Qt에 대응해요',['QApplication 생성','위젯과 Layout 구성','시그널 연결','show → app.exec'],['tkinter','PySide6','공통 개념'],[['Tk()','QApplication + QWidget','앱과 창'],['command=handler','clicked.connect(handler)','이벤트 연결'],['pack / grid','QVBoxLayout / QGridLayout','배치 규칙'],['mainloop()','app.exec()','이벤트 루프']]),
}

def table(headers,rows):
 return '<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+esc(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(str(x))+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def flow(items):
 return '<ol class="concept-flow">'+''.join('<li><span class="flow-number">'+str(i+1)+'</span><strong>'+esc(s.split('｜')[0])+'</strong><span>'+esc(s.split('｜',1)[1] if '｜' in s else '')+'</span></li>' for i,s in enumerate(items))+'</ol>'
def spec(u,l):
 if 'visual' in l:return l['visual']
 if l['id']=='project':return ('기능에서 완성 앱까지',['요구 기능 정하기','기능 모듈 구현','입력과 오류 시험','화면 연결·기록'],['산출물','확인할 내용'],[['기능 코드','GUI 없이도 시험 가능'],['실행 결과','정상·빈 값·경계값 비교'],['학습 기록','오류 원인과 수정 근거']])
 if l['id']=='review':return ('한 단원, 세 가지 확인',['설명하기｜개념을 내 말로','예상하기｜실행 전 결과 추적','바꾸기｜조건 변경 후 검증'],['점검','질문'],[['개념','왜 이 도구를 선택했나요?'],['코드','입력과 출력은 무엇인가요?'],['검증','조건을 바꾸어도 동작하나요?']])
 return VISUALS[l['id']]
def visual(u,l,prefix="../../"):
 title,steps,headers,rows=spec(u,l)
 pictures={'ml-libraries':('ml-chart','과일 빈도 막대그래프'),'ml-cluster':('ml-cluster','군집과 중심점 산점도'),'ml-selection':('ml-learning-curve','훈련과 검증의 학습 곡선'),'cv-libraries':('cv-sobel','원본과 Sobel 에지 비교'),'cv-io':('cv-io','원본·회색조·축소·회전 결과'),'cv-filters':('cv-filters','블러·에지·세 이진화의 실제 결과'),'cv-transform':('cv-perspective','원본과 원근 변환 결과'),'cv-features':('cv-features','에지·코너·윤곽선의 차이')}
 picture=''
 if l['id'] in pictures:
  filename,alt=pictures[l['id']]
  picture=f'<a class="science-picture" href="{prefix}assets/science/{filename}.png" target="_blank" rel="noopener"><img src="{prefix}assets/science/{filename}.png" loading="lazy" alt="{alt}"><span>{alt} · 제공 Python 예제의 실제 실행 결과 · 클릭하여 확대</span></a>'
 diagram=flow(steps)
 if l['id'] in ['random','thirdparty','ui','libraries','widgets','ml-methods','ml-libraries']:
  diagram=diagram.replace('concept-flow','concept-flow comparison-flow')
 if u==1 and l['id']=='overview':
  diagram='<div class="dependency-map"><div><strong>main.py</strong><span>calculator.add(3,5)</span></div><b aria-label="불러오기">→</b><div class="shared-module"><strong>calculator.py</strong><span>add 함수를 한 곳에서 정의</span></div><b aria-label="불러오기">←</b><div><strong>other_app.py</strong><span>calculator.add(10,2)</span></div></div>'
 if l['id']=='ml-overview':
  diagram='<div class="set-map">인공지능 AI<div>머신러닝 ML<div>딥러닝 DL</div></div></div>'
 return '<figure class="concept-visual"><figcaption><span class="eyebrow">AT A GLANCE</span><h3>'+esc(title)+'</h3></figcaption>'+picture+diagram+table(headers,rows)+'</figure>'
def prepare(units):
 notes={u:[] for u in units}
 for u,ls in units.items():
  for l in ls:
   keep=[]
   for p in l['paragraphs']:
    if p.startswith(('교과서 보완:','교과서 58쪽','운영 계획의 수행')):notes[u].append((l['title'],p))
    else:keep.append(p.replace('핵심 지도:','학습 흐름:'))
   l['paragraphs']=keep
 return notes

def experiments(u):
 if u==1:return '''<section class="section visual-lab"><h2>임포트 실행 순서 실험</h2><p>같은 파일을 직접 실행하거나 다른 파일에서 불러왔을 때의 차이를 확인하세요. 정해진 코드의 흐름을 보여 주는 모형입니다.</p><div class="trace-grid"><pre>print("모듈 시작")
if __name__ == "__main__":
    print("직접 실행 시험")</pre><div><label>실행 방법<select id="trace-mode"><option value="direct">python helper.py</option><option value="import">import helper</option></select></label><button id="trace-next">다음 단계 →</button><button id="trace-reset">처음부터</button><ol id="trace-output" aria-live="polite"></ol></div></div></section>'''
 if u==3:return '''<section class="section visual-lab"><h2>예측과 평가를 눈으로 실험하기</h2><p>학습용 수학 모형입니다. 아래 조작과 별도로 실습실의 Python 코드를 실행할 수 있습니다.</p><div class="trace-grid"><div><h3>직선의 기울기와 오차</h3><label>기울기 <output id="slope-value">2</output><input id="slope" type="range" min="0" max="4" step="0.1" value="2"></label><svg id="regression-view" viewBox="0 0 400 250" role="img" aria-label="네 데이터 점과 예측 직선의 오차"></svg><p id="regression-score" aria-live="polite"></p></div><div><h3>양성으로 예측하는 기준 바꾸기</h3><label>임계값 <output id="threshold-value">0.5</output><input id="ml-threshold" type="range" min="0" max="1" step="0.1" value="0.5"></label><p>고정 확률 [0.9, 0.8, 0.6, 0.4, 0.3, 0.1]<br>실제 정답 [1, 0, 1, 1, 0, 0]</p><div id="confusion-view" aria-live="polite"></div></div></div></section>'''
 if u==4:return '''<section class="section visual-lab"><h2>픽셀 실험실</h2><p>숫자가 바뀌면 그림이 어떻게 달라질까요? 아래는 JavaScript로 계산하는 8×8 밝기 모형입니다. 실제 Python 코드는 실습실에서 실행하세요.</p><div class="trace-grid"><div><label>변환<select id="pixel-op"><option value="original">원본</option><option value="invert">반전: 255 − 값</option><option value="threshold">이진화: 기준보다 크면 255</option><option value="blur">3×3 평균 블러</option><option value="edge">가로 밝기 차이의 절댓값</option></select></label><label>이진화 기준 <output id="pixel-level-value">128</output><input type="range" id="pixel-level" min="0" max="255" value="128"></label><div id="pixel-grid" class="pixel-grid" aria-label="변환된 8행 8열 픽셀"></div><p id="pixel-explain" aria-live="polite"></p></div><div><h3>RGB는 세 개의 숫자</h3><label>R<input id="rgb-r" type="range" min="0" max="255" value="240"></label><label>G<input id="rgb-g" type="range" min="0" max="255" value="160"></label><label>B<input id="rgb-b" type="range" min="0" max="255" value="40"></label><div id="rgb-color" class="color-swatch"></div><p id="rgb-values" aria-live="polite"></p><p>OpenCV의 기본 읽기는 BGR 순서입니다. 표시 도구가 RGB를 기대하면 채널 순서를 변환하세요.</p></div></div></section>'''
 return ''

RUBRICS={
1:[['연결 수행','1·2단원 기능 모듈과 GUI를 함께 확인','수행①과 연결']],
2:[['기능 구현·이벤트 처리','정상 입력·빈 값·취소·오류 복구','10점'],['모듈 구조·코드 품질','화면과 기능 분리·가독성','5점'],['저널 기록·제출 충실도','과정과 해결 근거·제출률','5점']],
3:[['데이터 전처리·모델 구현','분할·전처리·학습의 정확성','10점'],['평가 지표 해석·결과 분석','지표 의미·오류·개선안','5점'],['저널 기록·제출 충실도','과정과 해결 근거·제출률','5점']],
4:[['이미지 처리·검출 구현','입출력·처리·검출 정확성','10점'],['응용·프로그램 완성도','응용 기능·오류 처리·완성도','5점'],['저널 기록·제출 충실도','과정과 해결 근거·제출률','5점']]}
CAUTIONS={
1:['교과서 39쪽 마지막 출력은 subnum(7,2)에 따라 5입니다. 정답편 201쪽의 9와 다릅니다.','25쪽 star 탐구는 함수 임포트와 모듈 임포트 표현이 혼재합니다. 명시적으로 두 호출법을 구별합니다.','__all__은 접근 금지가 아니고 별표 임포트의 이름 목록입니다.'],
2:['58쪽 4번의 사용자 정의 예외 표현은 보기의 GUI 사례와 맞지 않아 인터페이스 분류로 재작성했습니다.','GUI의 문법 확인은 실제 창·버튼 동작 검증이 아닙니다. PC 시연을 별도로 확인합니다.','PySide6는 교과서 tkinter 이후 확장 학습입니다. 확장 사용 자체를 별도 평가 요건으로 추가하지 않습니다.'],
3:['브라우저는 작은 원리 구현과 배열·표·그래프 실습을 제공합니다. scikit-learn 전체 예제는 PC 경로이며 Python 문법 확인과 ZIP 다운로드가 가능합니다.','84쪽 확인학습 1③은 정답 없는 패턴 학습을 지도 학습이라고 하므로 ×입니다. 정답편 206쪽의 ○ 표기와 다릅니다.','128쪽 순서 문제의 정답편은 변환 뒤 분할합니다. 실제 모델 실습에서는 먼저 테스트를 떼고 훈련 데이터로 전처리 통계량을 학습합니다.','65쪽 딥 블루 사례를 현대의 데이터 학습형 딥러닝과 동일시하지 않습니다.','정규화(normalization)와 규제(regularization)는 용어가 겹쳐 번역될 수 있으나 기능이 다릅니다.','분류 지표는 양성 레이블을 먼저 명시합니다. R²는 음수가 될 수 있습니다.'],
4:['150쪽 img.size는 컬러 이미지에서 픽셀 수가 아니라 채널을 포함한 원소 수입니다.','교과서의 얼굴 인식 표현 중 Haar 예제는 얼굴 위치 검출입니다. 개인 식별이나 감정 판단을 수행하지 않습니다.','169쪽 import cv2, import numpy as np 구문을 두 import 문으로 수정했습니다.','YOLOv8을 최신 버전이라고 표현하지 않습니다. 교과서 모델의 재현 경로로 제공합니다.','프레임별 객체 개수의 합은 고유 방문자 수가 아닙니다.','카메라·외부 가중치·개인 사진은 PC에서 별도 준비가 필요합니다. 도형 기반 처리를 먼저 확인하고 확장합니다.']}

def teacher_pages(web,layout,units,notes):
 root=web/'teacher';root.mkdir(exist_ok=True)
 home='<main id="main" class="teacher-page"><p class="eyebrow">TEACHER DESK</p><h1>교사용 수업 요약</h1><p class="lead">단원별 설명 흐름, 시연 포인트, 오개념, 평가 연결을 한곳에서 확인합니다. 수업 화면 보기를 누르면 학생에게 보여 줄 개념 도식만 한 장씩 표시합니다.</p><div class="learning-map">'
 for u in units:home+=f'<a href="unit0{u}.html"><b>{textbook.ROMAN[u]}</b><span>{META[u][0]}</span><small>교과서 {textbook.BOOK[u][1]}쪽 · {len(units[u])}개 개념 화면</small></a>'
 home+='</div><h2>자료 사용 순서</h2>'+flow(['교사용 요약에서 목표·오개념 확인','수업 화면으로 구조 설명','학생용 실습 링크로 전환','결과·설명·저널 확인'])+'<section class="teacher-note"><h2>차시와 평가의 기준</h2><p>평가 항목은 제공된 2026학년도 2학기 운영 계획 _g에 근거합니다. 아래 시간 배분은 50분 수업 운영 제안이며 확정 시수나 평가 기준을 변경하지 않습니다. 기존 학생 화면의 일률적인 “6차시” 표기는 제거했습니다.</p><p>성취기준·세부 점수 부여와 실제 제출 경로는 학교의 확정 문서에 따릅니다. 웹 연습 완료·자동 검사는 공식 성적이 아닙니다.</p></section><p><a href="admin.html">수업 관리 · 명단 →</a> · <a href="board.html">반 현황 보드 →</a> · <a href="session.html">수업 세션 →</a> · <a href="../index.html">학생용 대문으로 →</a></p></main>'
 (root/'index.html').write_text(layout('교사용 수업 요약',home,'../'))
 for u,ls in units.items():
  title=META[u][0]
  s=f'<main id="main" class="teacher-page"><p class="eyebrow">TEACHER / UNIT 0{u}</p><h1>{textbook.unit_label(u)} · 수업 요약</h1><p class="lead">교과서 {META[u][1]}쪽 · 도식 → 시연 → 학생 실험 → 설명 확인</p><div class="slide-toolbar"><a href="index.html">교사 대문</a><button id="present-toggle">수업 화면으로 보기</button><button id="slide-prev">← 이전</button><span id="slide-position"></span><button id="slide-next">다음 →</button><button id="print-summary">도식 인쇄 / PDF</button><a href="../units/unit0{u}/index.html">학생 실습실 →</a></div><section class="teacher-overview"><h2>50분 수업 운영 제안</h2>'+table(['단계','시간','교사 확인'],[['도입·결과 예상','5분','정답 전에 입력·출력 예상 받기'],['구조 설명·시연','10분','도식과 코드의 각 부분 연결'],['학생 코드 변형','25분','정상·경계·오류 조건 확인'],['설명·저널','10분','결과 이유와 수정 근거 확인']])+ '<h2>평가 연결</h2>'+table(['항목','관찰할 증거','배점/연결'],RUBRICS[u])+'</section><details class="teacher-note"><summary>교과서 대조·지도 유의사항</summary><ul>'+''.join('<li>'+esc(p)+'</li>' for p in CAUTIONS[u])+''.join('<li>'+esc(title+': '+p)+'</li>' for title,p in notes[u])+'</ul></details>'
  summary=f'<main id="main" class="summary-page"><p class="eyebrow">VISUAL SUMMARY / UNIT 0{u}</p><h1>{textbook.unit_label(u)} · 그림으로 정리</h1><p class="lead">흐름도와 표를 보고 각 단계를 내 말로 설명하세요.</p><a href="index.html">단원 실습으로 돌아가기 →</a>'
  s+=textbook.toc(u,ls)
  summary+=textbook.toc(u,ls)
  for i,l in enumerate(ls):
   fig=visual(u,l,"../")
   s+=f'<section class="teaching-slide" id="{l["id"]}">{textbook.badge(u,l)}<p class="eyebrow">웹 학습 주제 {i+1:02}</p><h2>{esc(l["title"])}</h2><p class="lesson-lead">{esc(l["lead"])}</p>'+fig+f'<a href="../units/unit0{u}/index.html#{l["id"]}">이 개념 실습으로 →</a><details class="teacher-note"><summary>시연·발문·확인</summary><p><b>발문:</b> {esc(l["lead"])}</p><p><b>시연:</b> '+('연결 예제를 실행하기 전에 결과를 예상하게 하고 입력·조건 하나를 바꿔 비교합니다.' if l['examples'] else '표의 예시를 학생의 학교생활 사례로 바꾸어 입력과 출력을 구별하게 합니다.')+'</p><p><b>확인:</b> '+esc(l['tasks'][0] if l['tasks'] else '각 단계의 입력과 출력을 설명할 수 있는지 확인합니다.')+'</p></details></section>'
   summary+=f'<section class="teaching-slide" id="{l["id"]}">{textbook.badge(u,l)}<h2>{esc(l["title"])}</h2>'+visual(u,l)+f'<a href="index.html#{l["id"]}">실습하기 →</a></section>'
  s+='</main>';summary+='</main>'
  (root/f'unit0{u}.html').write_text(layout(title+' · 교사용',s,'../'))
  (web/f'units/unit0{u}/summary.html').write_text(layout(title+' · 시각 요약',summary,'../../'))
