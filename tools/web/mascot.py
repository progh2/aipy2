"""Pai: original course mascot and topic-specific learning prompts."""
from html import escape as esc
MOODS = {
    'welcome': ('반가워요', '손을 흔들며 반갑게 웃는 파이', '처음에는 결과를 예상하고, 실행한 다음 한 가지 조건을 바꿔 보세요.'),
    'thinking': ('생각 중', '고개를 갸웃하며 생각하는 파이', '실행 버튼을 누르기 전에 어떤 이름과 값이 필요한지 먼저 적어 보세요.'),
    'idea': ('아하!', '전구 옆에서 아이디어를 설명하는 파이', '왜 그렇게 동작하는지 한 문장으로 설명하면, 다음 문제에도 같은 원리를 쓸 수 있어요.'),
    'debug': ('오류 탐정', '돋보기를 들고 원인을 살펴보는 파이', '오류 메시지의 마지막 줄부터 읽고, 파일명 → 줄 번호 → 변수 값을 차례로 확인하세요.'),
    'celebrate': ('해냈어요', '두 팔을 들고 기뻐하는 파이', '조건을 바꾼 문제도 풀어 보세요. 스스로 설명할 수 있다면 내 것이 된 거예요!'),
}
TIPS = {
 1: {
  'overview': ('idea','파일 하나는 기능 상자, 패키지는 상자를 정리한 서랍이에요.','계산 기능은 calculator.py에, 사용하는 코드는 main.py에 두고 연결해 보세요.'),
  'define': ('thinking','함수를 만드는 줄과 함수를 부르는 줄을 구별해 볼까요?','def 안의 코드는 호출할 때 실행돼요. 모듈 바깥쪽 실행문은 처음 임포트할 때도 실행됩니다.'),
  'entrypoint': ('idea','같은 파일도 직접 실행할 때와 불러올 때 역할이 달라져요.','직접 실행 → __main__ / 임포트 → 모듈 이름. 실행 파일을 바꿔 두 결과를 비교하세요.'),
  'imports': ('debug','지금 내 코드에 연결된 이름부터 찾아보세요.','import greet as g로 불러왔다면 g.hello()! 별칭은 파일 이름을 바꾸는 기능이 아니에요.'),
  'packages': ('idea','점(.)으로 쓴 경로를 폴더 트리에서 따라가 보세요.','nature.animals.bird → nature/animals/bird.py. __all__은 별표 임포트 목록이지 접근 금지 목록이 아닙니다.'),
  'os-sys': ('debug','파일이 있는 곳과 실행하는 곳을 함께 확인해요.','os.getcwd()로 작업 폴더를, sys.argv로 전달된 값을 확인하세요. 인자는 문자열로 들어옵니다.'),
  'math': ('thinking','음수를 넣으면 올림과 내림이 더 분명해져요.','−3.5의 ceil은 −3, floor는 −4. 수직선에서 어느 방향으로 움직였는지 생각하세요.'),
  'random': ('debug','무작위 결과는 숫자 하나보다 조건으로 검사해요.','범위 안인가요? 필요한 개수인가요? 원본이 유지되나요? shuffle의 반환값은 None이라는 것도 확인하세요.'),
  'datetime': ('thinking','달력의 하루와 정확히 24시간은 다를 수 있어요.','날짜끼리의 일수는 date로 계산해 보세요. 12월 24일·25일·26일을 넣어 연도 전환을 검사하세요.'),
  'thirdparty': ('idea','설치한 곳과 실행하는 곳이 같은 환경인가요?','패키지는 도구를 추가하는 것! python -m pip와 VS Code의 선택된 인터프리터를 함께 확인하세요.'),
  'review': ('celebrate','외운 답을 넘어, 이유까지 말해 볼까요?','숫자나 import 방법을 바꾼 뒤 결과를 다시 예상하세요. 마지막 뺄셈은 실제 코드의 7 − 2 = 5입니다.'),
  'project': ('idea','화면 없이도 검사할 수 있는 기능부터 만들어요.','입력 → 함수의 반환값 → 검사. 같은 core.logic을 다음 단원의 두 GUI에서 재사용합니다.'),
 },
 2: {
  'ui': ('thinking','누가 어떤 작업을 하는 화면인지 먼저 생각해요.','한 번 고르는 작업과 백 번 반복하는 작업은 편리한 입력 방식이 다를 수 있어요.'),
  'libraries': ('idea','겉모습과 함께 도구의 역할도 비교해 볼까요?','같은 인사 앱의 창 생성·배치·이벤트 연결 부분을 찾아보세요. PySide6와 PyQt6는 같은 Qt를 사용하는 별도 바인딩입니다.'),
  'widgets': ('idea','위젯은 역할이 다른 화면 부품이에요.','한 줄 입력은 Entry / QLineEdit, 여러 줄 입력은 Text / QPlainTextEdit. 먼저 받을 정보의 형태를 정하세요.'),
  'layout': ('debug','부품을 만들었는데 안 보인다면, 배치를 확인해요.','부모 → 위젯 생성 → 배치 순서로 확인하세요. 같은 부모 안에서는 pack과 grid를 섞지 않습니다.'),
  'events': ('thinking','지금 실행할까요, 클릭할 때 실행할까요?','command=greet와 clicked.connect(greet)는 함수를 맡겨 두는 코드예요. greet()는 지금 호출합니다.'),
  'memo': ('debug','취소 버튼도 꼭 눌러 봐야 하는 시험 입력이에요.','경로 선택 → 취소 확인 → 읽기·쓰기 → 화면 반영. 취소했을 때 기존 문서가 남는지 확인하세요.'),
  'pyside': ('idea','새 도구에서도 창·부품·배치·이벤트를 찾아요.','QApplication → 창과 위젯 → connect → show → exec. Designer의 objectName은 코드에서 부품을 찾는 이름입니다.'),
  'project': ('celebrate','두 가지 화면이 같은 기능 상자를 사용해요!','GUI는 입력과 표시를, core는 계산을 담당합니다. 같은 입력을 넣어 두 화면의 결과를 비교하세요.'),
  'review': ('thinking','버튼을 누른 뒤 일어나는 일을 순서대로 말해 보세요.','입력 읽기 → 기능 호출 → 결과 표시. 어디에서 잘못됐는지 설명할 수 있으면 디버깅도 쉬워져요.'),
 }
}
def image(prefix,mood='welcome',loading='lazy',cls='pai-image'):
 return f'<img class="{cls}" src="{prefix}assets/mascot/pai-{mood}-v1.webp" width="1254" height="1254" loading="{loading}" decoding="async" alt="{MOODS[mood][1]}">'
def card(prefix,mood,title,text,kind='lesson'):
 return f'<aside class="pai-note pai-note--{kind}" data-pai-mood="{mood}" aria-label="파이의 학습 안내">{image(prefix,mood)}<div><span class="pai-label">파이의 한 줄 힌트 · {MOODS[mood][0]}</span><strong>{esc(title)}</strong><p>{esc(text)}</p></div></aside>'
def lesson_tip(u,id,prefix):
 mood,title,text=TIPS[u][id]
 return card(prefix,mood,title,text)
def hero():
 return '<aside class="pai-hero" aria-labelledby="pai-hello"><div class="pai-hero-copy"><span class="pai-label">우리 과목의 학습 친구</span><h2 id="pai-hello">안녕하세요, <em>파이</em>예요!</h2><p>같이 생각하고, 오류를 찾고,<br>작은 성공을 쌓아 가요.</p></div>'+image('','welcome','eager','pai-hero-image')+'<div class="pai-speech" role="status" aria-live="polite"><b id="pai-mood-title">반가워요</b><p id="pai-mood-description">'+MOODS['welcome'][2]+'</p></div><div class="pai-mood-buttons" role="group" aria-label="파이의 표정과 학습 안내">'+''.join(f'<button data-pai-preview="{mood}" data-pai-description="{esc(info[2],quote=True)}" data-pai-alt="{esc(info[1],quote=True)}" aria-pressed="{str(mood=="welcome").lower()}">{info[0]}</button>' for mood,info in MOODS.items())+'</div><a class="pai-about" href="mascot.html">파이를 소개합니다 · 캐릭터 내려받기 ↗</a></aside>'
def intro_page():
 body='<main id="main" class="source-page mascot-page"><p class="eyebrow">MEET PAI / OUR PYTHON COMPANION</p><h1>함께 배우는 친구, 파이</h1><p class="lead">호기심 많은 아기 비단뱀 파이는 인공지능 파이썬 실무의 대표 캐릭터입니다. 정답을 대신 풀어 주기보다, 스스로 생각할 질문과 확인할 순서를 알려 줘요.</p><div class="pai-intro">'+image('','welcome','eager')+'<div><h2>작은 한 번의 실험이<br>큰 이해로 이어져요.</h2><p>파이썬에서 따온 이름, 파이. 금빛 몸과 네이비 후드, 민트색 끈, 동그랗게 말린 꼬리가 특징이에요. 후드 주머니의 꺾쇠 모양은 코딩을 좋아하는 마음을 담았어요.</p><p>표정과 대사는 학습 단계에 맞춰 바뀝니다. 색이나 표정을 구별하지 않아도, 함께 적힌 안내를 읽고 학습할 수 있어요.</p><a class="button primary" href="downloads/pai-character-pack.zip">캐릭터 5종 원본 묶음 ↓</a></div></div><h2>표정에 담긴 학습 약속</h2><div class="pai-sheet">'
 for mood,(label,alt,description) in MOODS.items():
  body+='<article>'+image('',mood)+f'<h3>{label}</h3><p>{description}</p><a href="assets/mascot/pai-{mood}-v1.png" download>원본 PNG ↓</a></article>'
 body+='</div><h2>수업 자료에 사용하는 방법</h2><p>개념 설명에는 전구를 든 파이, 결과 예상에는 생각하는 파이, 오류 원인 찾기에는 돋보기를 든 파이를 배치해 보세요. 옆에는 학생이 지금 할 일을 한두 문장으로 적어 주세요.</p><p>캐릭터는 이 과목을 위해 새로 제작했으며, 교과서 원문에 등장하는 인물이나 Python 공식 로고가 아닙니다. 원본은 흰 배경 PNG이고 웹에서는 압축한 WebP를 사용합니다.</p><p><a href="assets/mascot/CREATION.md">제작 도구와 전체 프롬프트 기록</a></p><div class="actions"><a class="button" href="units/unit01/index.html">1단원에서 파이 만나기 →</a><a class="button" href="units/unit02/index.html">2단원에서 파이 만나기 →</a></div></main>'
 return body
def runtime_guide(u):
 text = ('파일을 오가며 코드를 바꾼 뒤 실행 파일을 확인하세요. 실행 전에는 결과를 먼저 예상해 보세요.' if u==1 else '웹에서는 GUI 코드의 문법을 확인해요. 실제 창·버튼 동작은 ZIP을 내려받아 PC에서 실행해 보세요.')
 return card('../../','thinking','실행 전에 한 번 예상해 볼까요?',text,'runtime').replace('<aside','<aside id="pai-run-guide"',1)
