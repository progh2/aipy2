"""2단원(GUI 프로그래밍) 소단원별 슬라이드·설명·실습 데이터 (#131).

build.py가 이 파일의 LESSONS를 읽어 소단원 페이지를 "PPT 슬라이드 화면 → 설명 →
실습 → 연습 문제 → 저널" 순서로 만든다. 이 파일만 고치면 build.py를 건드리지
않고도 화면이 바뀐다 (B 담당: 2단원 설명·실습 채우기).

LESSONS 형식
------------
LESSONS[소단원id] = dict(
    title=...,           # 소단원 표제 (교과서 표기 그대로)
    pages=...,           # 교과서 쪽수. 예: '43–44'
    slides=[
        dict(
            n=5,          # 원본 슬라이드 번호. /tmp/slides/u2/s-05.png 원본을
                          # tools/web/slide_images.py로 변환한
                          # web/assets/slides/u2/s05.webp를 가리킨다.
            alt='...',    # <img alt> — 슬라이드 핵심 문구 요약(대체 텍스트). A가 채움.
            explain=[],   # 학생용 설명 문단 리스트(HTML 문자열). 비어 있으면 설명 생략.
                          # 예: ['<p>...</p>'] 처럼 이미 <p> 태그를 포함해도 되고,
                          # 그냥 문장만 넣으면 build.py가 <p>로 감싼다(HTML 이스케이프 없음 —
                          # 굵게·코드 강조가 필요하면 <b>/<code>를 직접 써도 된다).
        ),
        ...
    ],
    practice=[
        # 교과서 예제를 가리킬 때는 examples 딕셔너리의 예제 id 문자열 하나만 적는다.
        # 예: 'hello-tk'  →  기존 ex-hello-tk.html 카드로 연결된다.
        #
        # 텍스트 자료가 없는 새 "따라 하기" 튜토리얼을 만들 때는 dict를 쓴다:
        # dict(kind='tutorial', id='memo-steps', title='메모장 따라 만들기',
        #      steps=[
        #          dict(text='먼저 창을 만듭니다.', code='root = tk.Tk()', expect='빈 창이 뜹니다.'),
        #          ...
        #      ])
        # steps 안의 code/expect는 없어도 된다(설명만 있는 단계 허용).
    ],
)

지금은 explain·practice를 비워 둔다(B가 채울 자리). slides의 n·alt와 pages·title은
A(이 파일 작성자)가 슬라이드 배정까지 마친 값이므로 그대로 두면 된다.

## A가 정리한 예제 참고 목록 (practice 채울 때 참고용 — 강제 아님)
tkinter 계열은 유지, PySide6/PyQt/wxPython/Kivy 비교 예제는 전부 제외했다
(교과서 밖 확장이자 #131 개편 대상). content.py에 정의는 남아 있지만 어떤
소단원도 더는 참조하지 않는다.
  ui:        hello-tk, ui-cli
  libraries: (코드 예제 없음 — 교과서 45~46쪽은 라이브러리 소개 텍스트뿐)
  widgets:   widgets-tk, widgets-label-entry-tk, widgets-choice-tk, widgets-list-canvas-tk
  layout:    layout-tk, layout-pack-tk, layout-grid-tk
  events:    events-callback, events-command-tk, events-bind-tk, events-after-tk
  memo:      memo-tk, memo-window-tk, memo-files-tk, memo-plus-tk
  review:    review-scratch-tk
  project:   core, project-tk, project-button-tk (tkinter만 — 아래 참고)

## project 소단원 판단
PySide6 비교 없이도 "1단원 core 패키지 + tkinter GUI" 통합 실습으로 가치가
있어 페이지는 남긴다(수행평가① 직결). 교과서 본문 슬라이드가 없어 slides는
비워 둔다 — explain만으로 안내하는 페이지가 된다.
"""

LESSONS = {
    'ui': dict(
        title='사용자 인터페이스 · CLI, GUI, NUI',
        pages='43–44',
        slides=[
            dict(n=6, alt='사용자 인터페이스(UI)란 무엇인가 — 사람과 컴퓨터가 상호작용하는 접점', explain=[]),
            dict(n=7, alt='인터페이스의 종류 — CLI · GUI · NUI 비교', explain=[]),
            dict(n=8, alt='CLI(명령어 기반 인터페이스)의 정의와 특징', explain=[]),
            dict(n=9, alt='GUI(그래픽 기반 인터페이스)의 정의와 특징', explain=[]),
            dict(n=10, alt='NUI(자연스러운 사용자 인터페이스)의 정의와 특징', explain=[]),
        ],
        practice=[],
    ),
    'libraries': dict(
        title='파이썬 GUI 라이브러리',
        pages='45–46',
        slides=[
            dict(n=14, alt='파이썬으로 GUI를 만든다는 것 — 버튼 클릭·텍스트 입력 같은 그래픽 요소 다루기', explain=[]),
            dict(n=15, alt='1. tkinter — 파이썬 기본 GUI 라이브러리', explain=[]),
            dict(n=16, alt='2. PyQt · 3. wxPython 라이브러리 소개', explain=[]),
            dict(n=17, alt='4. Kivy 및 네 가지 GUI 라이브러리 비교', explain=[]),
        ],
        practice=[],
    ),
    'widgets': dict(
        title='창과 위젯 · 화면을 구성하는 부품',
        pages='50',
        slides=[
            dict(n=32, alt='tkinter를 이루는 네 가지 요소 한눈에 보기', explain=[]),
            dict(n=33, alt='1. Tk 객체 — 모든 것은 창에서 시작한다', explain=[]),
            dict(n=34, alt='2. 위젯 — tkinter가 제공하는 9가지 요소', explain=[]),
        ],
        practice=[],
    ),
    'layout': dict(
        title='배치 관리자',
        pages='51',
        slides=[
            dict(n=35, alt='3. 배치 관리자 — 위젯을 어디에 둘 것인가', explain=[]),
        ],
        practice=[],
    ),
    'events': dict(
        title='이벤트 처리',
        pages='51',
        slides=[
            dict(n=36, alt='4. 이벤트 처리 — 사용자 동작에 반응하기', explain=[]),
        ],
        practice=[],
    ),
    'memo': dict(
        title='GUI 앱 개발 · 나만의 메모장 만들기',
        pages='52–55',
        slides=[
            dict(n=44, alt='나만의 메모장 만들기 — 오늘의 목표', explain=[]),
            dict(n=45, alt='1. 라이브러리 불러오기 · 2. 메인 창 구성', explain=[]),
            dict(n=46, alt='4. 파일 열기 기능 · 5. 파일 저장 기능', explain=[]),
            dict(n=47, alt='6. 메뉴 구성 · 7. 프로그램 실행', explain=[]),
            dict(n=48, alt='8. 전체 코드 ① — 01~20행', explain=[]),
            dict(n=49, alt='8. 전체 코드 ② — 21~41행', explain=[]),
            dict(n=50, alt='실행하고 확인하기 — 체크리스트', explain=[]),
            dict(n=60, alt='내가 만든 GUI, 이 다섯 가지를 확인해요(입력·이벤트·배치·파일·설명 점검표)', explain=[]),
        ],
        practice=[],
    ),
    'review': dict(
        title='2단원 마무리 · 개념에서 앱까지',
        pages='56–59',
        slides=[
            dict(n=61, alt='02. GUI 프로그래밍 작성 핵심 정리 — tkinter 개요·구성 요소·메모장 개발 사례', explain=[]),
            dict(n=65, alt='정리하며 — UI 종류, tkinter 네 요소, 위젯 배치와 mainloop를 세 문장으로', explain=[]),
        ],
        practice=[],
    ),
    'project': dict(
        title='통합 프로젝트 · 우리 반 생활 도우미',
        pages='수행평가 연결 · 확장',
        slides=[],
        practice=[],
    ),
}
