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
        pages='43–44, 47–48',
        slides=[
            dict(n=6, alt='사용자 인터페이스(UI)란 무엇인가 — 사람과 컴퓨터가 상호작용하는 접점', explain=[
                '<b>사용자 인터페이스(UI, User Interface)</b>란, 사용자가 컴퓨터 시스템·소프트웨어·스마트폰·웹사이트 등을 쉽고 효율적으로 사용할 수 있도록 도와주는 장치나 화면 구성을 의미합니다. 즉, 사람과 기계가 만나는 접점이라 할 수 있습니다.',
                'UI에는 사용자가 직접 보고 조작할 수 있는 모든 요소, 즉 버튼, 메뉴, 스크롤바, 입력 창, 알림 메시지, 폰트 크기, 색상 등이 포함됩니다. UI는 버튼의 위치, 메뉴의 크기, 색깔, 글꼴, 사용 순서 등을 모두 포함하는 개념으로, 프로그램을 얼마나 쉽고 효과적으로 사용할 수 있는지를 결정합니다.',
            ]),
            dict(n=7, alt='인터페이스의 종류 — CLI · GUI · NUI 비교', explain=[
                '인터페이스의 종류에는 대표적으로 <b>CLI</b>, <b>GUI</b>, <b>NUI</b>가 있습니다. 다음 슬라이드에서 하나씩 살펴봅니다.',
            ]),
            dict(n=8, alt='CLI(명령어 기반 인터페이스)의 정의와 특징', explain=[
                '<b>CLI</b>(Command Line Interface)는 명령어 기반 인터페이스로, 사용자가 키보드로 직접 명령어를 입력하여 컴퓨터와 소통하는 방식입니다. 이 방식은 빠르고 가벼우며, 숙련된 사용자에게는 매우 강력한 도구가 될 수 있습니다.',
                '그러나 명령어를 외워야 하고 입력 형식이 까다로워 초보자가 접근하기 어렵다는 단점이 있습니다. 주로 서버 관리, 개발 환경 등에서 사용합니다.',
            ]),
            dict(n=9, alt='GUI(그래픽 기반 인터페이스)의 정의와 특징', explain=[
                '<b>GUI</b>(Graphical User Interface)는 그래픽 기반의 사용자 인터페이스로, 사용자가 마우스나 터치를 이용하여 화면에 보이는 아이콘, 버튼, 메뉴 등을 조작함으로써 컴퓨터와 상호 작용하는 방식입니다. 명령어를 몰라도 직관적으로 사용할 수 있어 일반적으로 널리 사용됩니다. 대부분의 운영체제와 소프트웨어의 기본 인터페이스는 GUI입니다.',
                '예를 들어 리눅스 터미널에서 <code>cat</code> 명령어로 파일 내용을 확인하는 것은 CLI이고, 윈도에서 파일을 메모장으로 열어 내용을 확인하는 것은 GUI입니다. 같은 목적(파일 내용 확인)이라도 인터페이스에 따라 조작 방법이 다릅니다.',
            ]),
            dict(n=10, alt='NUI(자연스러운 사용자 인터페이스)의 정의와 특징', explain=[
                '<b>NUI</b>(Natural User Interface)는 자연스러운 사용자 인터페이스로, 음성, 손짓, 터치 등 사람의 신체 동작을 기반으로 컴퓨터와 상호 작용하는 방식입니다. 별도의 학습 없이도 쉽게 사용할 수 있으며, 최근에는 스마트폰, 스마트 TV, 인공지능 스피커, 가상현실 기기 등에서 활발히 활용되고 있습니다.',
                '탐구 활동(44쪽): 사용자 인터페이스가 무엇인지 자신의 말로 설명해 보고, "dir 입력", "아이콘 클릭", "손짓으로 TV 조작"이 각각 어떤 인터페이스에 해당하는지 아래 「직접 해 보세요」에 적어 보세요.',
            ]),
        ],
        practice=['hello-tk'],
    ),
    'libraries': dict(
        title='파이썬 GUI 라이브러리',
        pages='45–48',
        slides=[
            dict(n=14, alt='파이썬으로 GUI를 만든다는 것 — 버튼 클릭·텍스트 입력 같은 그래픽 요소 다루기', explain=[
                'GUI 프로그래밍은 버튼 클릭, 텍스트 입력, 드래그 같은 그래픽 위젯을 통해 사용자와 프로그램이 상호 작용하도록 만드는 방식입니다. 파이썬에서 활용할 수 있는 대표적인 GUI 라이브러리 네 가지를 살펴봅니다.',
            ]),
            dict(n=15, alt='1. tkinter — 파이썬 기본 GUI 라이브러리', explain=[
                '<b>tkinter</b>는 파이썬에서 기본으로 제공하는 GUI 라이브러리입니다. 별도의 설치 없이 사용할 수 있으며, 간단한 창 구성과 기본 위젯(버튼, 텍스트 입력 창, 라벨 등)을 지원합니다. 구조가 단순하고 사용법이 쉬워 GUI 입문자에게 적합한 도구로 평가받습니다.',
                'tkinter를 사용하면 최소한의 코드로 창을 만들 수 있으며, 창 크기나 배치, 색상 등을 간단하게 설정할 수 있습니다. 하지만 디자인 측면에서는 현대적인 느낌이 부족하며, 고급 기능 구현에는 한계가 있습니다. 교육용 예제, 프로토타입, 소규모 도구 제작 등에 적합합니다. 이 단원의 실습은 모두 tkinter로 진행합니다.',
            ]),
            dict(n=16, alt='2. PyQt · 3. wxPython 라이브러리 소개', explain=[
                '<b>PyQt</b>는 C++로 만들어진 Qt 프레임워크를 파이썬에서 사용할 수 있도록 만든 라이브러리입니다. 풍부한 위젯 구성과 정교한 이벤트 처리 기능을 갖추고 있으며, 실제 상업용 프로그램에서도 널리 사용됩니다. 단, 설치 과정이 필요하고 상업적으로 사용하려면 라이선스 조건을 확인해야 합니다.',
                '<b>wxPython</b>은 C++ 기반의 wxWidgets를 파이썬에서 사용하도록 한 GUI 툴킷입니다. 가장 큰 특징은 각 운영체제의 네이티브 위젯을 활용해 플랫폼 고유의 인터페이스가 그대로 구현된다는 점입니다. 다만 Qt 계열에 비해 자료와 최신 예제가 상대적으로 적습니다.',
            ]),
            dict(n=17, alt='4. Kivy 및 네 가지 GUI 라이브러리 비교', explain=[
                '<b>Kivy</b>는 터치 기반 사용자 인터페이스를 포함한 멀티 플랫폼 GUI 개발을 지원하는 프레임워크입니다. 모바일과 데스크탑 모두에서 실행할 수 있으며, 게임이나 앱과 같은 동적인 인터페이스 구성에 적합합니다. GPU 가속을 지원하지만 학습 곡선이 높아 입문용보다는 고급 프로젝트에 알맞은 도구입니다.',
                '네 라이브러리 중 어떤 것을 선택할지는 목적에 따라 달라집니다. 쉬운 입문·교육용에는 tkinter, 전문적인 데스크탑 앱에는 PyQt, 운영체제 고유 외형이 필요하면 wxPython, 터치·모바일·게임에는 Kivy가 적합합니다.',
            ]),
            dict(n=23, alt='좀 더 알아보기 — IDLE도 tkinter로 만들어졌다고?', explain=[
                '<b>좀 더 알아보기(46쪽): IDLE도 tkinter로 만들어졌다고?</b> 파이썬을 설치하면 함께 제공되는 기본 개발 환경인 IDLE은 초보자가 파이썬을 배우기에 매우 좋은 도구입니다. 그런데 놀랍게도 이 IDLE 프로그램 자체도 tkinter로 만들어진 GUI 애플리케이션입니다.',
                'IDLE에서 사용되는 tkinter 코드의 일부입니다.',
                '<pre><code>def fix_scaling(root):\n    import tkinter.font\n    scaling = float(root.tk.call(\'tk\', \'scaling\'))\n    if scaling > 1.4:\n        for name in tkinter.font.names(root):\n            font = tkinter.font.Font(root=root, name=name, exists=True)\n            size = int(font[\'size\'])\n            if size < 0:\n                font[\'size\'] = round(-0.75*size)</code></pre>',
                '우리가 지금 쓰고 있는 도구도 결국 누군가가 tkinter로 만든 프로그램입니다. 이번 단원을 마치면 여러분도 만들 수 있습니다.',
            ]),
        ],
        practice=[],
    ),
    'widgets': dict(
        title='창과 위젯 · 화면을 구성하는 부품',
        pages='49–50',
        slides=[
            dict(n=31, alt='중단원 02 학습 목표와 생각 열기 — GUI 요소를 조합해 애플리케이션 만들기', explain=[
                '<b>학습 목표(49쪽)</b>: GUI 요소들을 조합하여 간단한 애플리케이션을 설계하고 구현할 수 있습니다. 이 중단원에서는 tkinter의 구성 요소를 배운 뒤, 그 지식을 모아 나만의 메모장 애플리케이션을 만들어 봅니다.',
                '생각 열기: 간단하게 만들 수 있는 GUI 프로그램에는 어떤 것들이 있을까요? 계산기, 단어 암기 카드, 타이머, 할 일 목록, 간단한 그림판, 성적 계산기, 학급 자리 뽑기처럼 만들고 싶은 GUI 애플리케이션을 자유롭게 떠올려 보세요.',
            ]),
            dict(n=32, alt='tkinter를 이루는 네 가지 요소 한눈에 보기', explain=[
                'tkinter 라이브러리를 통해 그래픽 기반의 인터페이스를 손쉽게 만들 수 있습니다. tkinter는 파이썬에 기본적으로 포함된 GUI 라이브러리로, 별도의 설치 없이 사용할 수 있으며, 다양한 버튼, 레이블, 입력창 등의 <b>위젯(widget)</b>을 제공합니다.',
                'tkinter를 이루는 네 가지 요소는 <b>Tk 객체</b>, <b>위젯</b>, <b>배치 관리자</b>, <b>이벤트 처리</b>입니다. 이번 소단원에서는 Tk 객체와 위젯을, 다음 소단원에서 배치 관리자와 이벤트 처리를 배웁니다.',
            ]),
            dict(n=33, alt='1. Tk 객체 — 모든 것은 창에서 시작한다', explain=[
                'tkinter 프로그램을 시작하려면 가장 먼저 <b>Tk</b> 클래스의 객체를 생성해야 합니다. 이 객체는 프로그램의 기본 창(root window)이 되며, 모든 위젯은 이 창 위에 생성됩니다.',
                '<pre><code>01  import tkinter as tk\n02  root = tk.Tk()             # GUI 창 생성</code></pre>',
                '01행은 tkinter 모듈을 tk라는 이름으로 불러옵니다. 02행은 Tk 클래스의 객체 root를 만듭니다. 이 root가 앞으로 만들 모든 위젯의 부모 창이 됩니다.',
            ]),
            dict(n=34, alt='2. 위젯 — tkinter가 제공하는 9가지 요소', explain=[
                'tkinter는 다양한 종류의 <b>위젯</b>을 제공합니다. 각 위젯은 특정한 기능을 수행하며, 사용자와의 상호 작용에 활용됩니다.',
                '<b>Label</b>은 텍스트나 이미지를 표시하는 데 사용됩니다. <b>Button</b>은 사용자가 클릭할 수 있는 버튼을 만듭니다. <b>Entry</b>는 한 줄짜리 텍스트 입력창을, <b>Text</b>는 여러 줄의 텍스트를 입력할 수 있는 입력창을 제공합니다.',
                '<b>Checkbutton</b>은 체크 박스를 만들어 사용자의 선택을 받을 수 있고, <b>Radiobutton</b>은 여러 항목 중 하나만 선택하도록 합니다. <b>Listbox</b>는 목록에서 여러 항목을 나열하고 선택할 수 있게 하며, <b>Canvas</b>는 그림·도형·이미지 등을 그릴 수 있는 공간입니다. <b>Frame</b>은 여러 위젯을 그룹으로 묶을 수 있는 컨테이너 역할을 합니다.',
            ]),
        ],
        practice=['widgets-tk', dict(kind='tutorial', id='widgets-greeting', title='입력한 이름을 Label에 인사로 띄우기',
            pc=True, steps=[
                dict(mode='full',text='창을 만들고 이름을 입력할 Entry 위젯을 하나 붙입니다.',
                     code='import tkinter as tk\n\nroot = tk.Tk()\nroot.title("이름 인사")\n\nname_entry = tk.Entry(root)\nname_entry.pack(pady=10)\n\nroot.mainloop()',
                     expect='빈 입력창 하나가 있는 작은 창이 뜹니다.'),
                dict(mode='blank',text='인사말을 보여 줄 Label을 Entry 아래에 추가합니다. mainloop() 앞에 두 줄을 더합니다.',
                     code='greeting = tk.____(root, text="이름을 입력하세요")\ngreeting.____(pady=10)',
                     answer_code='greeting = tk.Label(root, text="이름을 입력하세요")\ngreeting.pack(pady=10)',
                     blanks=['첫 번째 빈칸: 텍스트를 표시하는 위젯 클래스 이름','두 번째 빈칸: 위젯을 화면에 배치하는 메서드 이름'],
                     expect='입력창 아래에 "이름을 입력하세요"라는 글자가 보입니다.'),
                dict(mode='blank',text='버튼을 누르면 입력한 이름으로 인사말을 바꾸는 함수를 만들고, Button의 command에 연결합니다. 역시 mainloop() 앞에 추가합니다.',
                     code='def greet():\n    name = name_entry.____()\n    greeting.____(text=f"{name}님, 안녕하세요!")\n\ngreet_button = tk.Button(root, text="인사하기", command=____)\ngreet_button.pack(pady=10)',
                     answer_code='def greet():\n    name = name_entry.get()\n    greeting.config(text=f"{name}님, 안녕하세요!")\n\ngreet_button = tk.Button(root, text="인사하기", command=greet)\ngreet_button.pack(pady=10)',
                     blanks=['첫 번째 빈칸: Entry에 입력된 문자열을 읽어오는 메서드 이름','두 번째 빈칸: 위젯의 속성을 바꾸는 메서드 이름','세 번째 빈칸: 클릭 시 호출할 함수 이름 — 괄호 없이'],
                     expect='입력창에 이름을 쓰고 "인사하기" 버튼을 누르면 라벨의 문구가 "○○○님, 안녕하세요!"로 바뀝니다.'),
                dict(mode='describe',text='지금까지 만든 세 조각(Entry, Label, greet 함수+버튼)을 순서대로 모아 전체 코드를 완성하세요. command=greet처럼 함수 이름만 전달했는지(괄호를 붙이지 않았는지) 다시 확인하세요.',
                     answer_code='import tkinter as tk\n\nroot = tk.Tk()\nroot.title("이름 인사")\n\nname_entry = tk.Entry(root)\nname_entry.pack(pady=10)\n\ngreeting = tk.Label(root, text="이름을 입력하세요")\ngreeting.pack(pady=10)\n\ndef greet():\n    name = name_entry.get()\n    greeting.config(text=f"{name}님, 안녕하세요!")\n\ngreet_button = tk.Button(root, text="인사하기", command=greet)\ngreet_button.pack(pady=10)\n\nroot.mainloop()',
                     expect='이름을 바꿔 여러 번 눌러도 라벨 문구가 매번 새 이름으로 바뀝니다.'),
            ])],
    ),
    'layout': dict(
        title='배치 관리자',
        pages='51',
        slides=[
            dict(n=35, alt='3. 배치 관리자 — 위젯을 어디에 둘 것인가', explain=[
                '위젯을 창에 배치할 때는 단순히 생성만 하는 것이 아니라 위치와 정렬을 지정하는 <b>배치 관리자</b>가 필요합니다. tkinter는 세 가지 배치 방식을 제공합니다.',
                '<b>pack()</b>은 위젯을 위에서 아래로, 왼쪽에서 오른쪽으로 차례대로 배치합니다. <b>grid()</b>는 행(row)과 열(column)로 구분하여 배치할 수 있습니다. <b>place()</b>는 좌표(x, y)를 지정하여 정확한 위치에 위젯을 배치합니다.',
                '탐구 활동(51쪽): 다음 중 tkinter의 GUI 창을 생성하는 객체는 무엇인지 골라 보세요. ① Tk() ② Entry() ③ Frame() ④ Label() ⑤ Button() — 아래 「직접 해 보세요」에 답과 이유를 적어 보세요.',
            ]),
        ],
        practice=['layout-tk', dict(kind='tutorial', id='layout-same-form', title='pack·grid로 같은 폼 배치해 보기',
            pc=True, steps=[
                dict(mode='full',text='이름·학번을 입력받는 폼을 pack()으로 위에서 아래로 배치합니다.',
                     code='import tkinter as tk\n\nroot = tk.Tk()\nroot.title("pack으로 배치하기")\n\ntk.Label(root, text="이름").pack()\ntk.Entry(root).pack()\ntk.Label(root, text="학번").pack()\ntk.Entry(root).pack()\n\nroot.mainloop()',
                     expect='이름 라벨·입력창, 학번 라벨·입력창이 위에서 아래로 순서대로 나타납니다.'),
                dict(mode='blank',text='같은 폼을 grid()로 다시 만들어 비교합니다. 새 Frame을 만들고 그 안에 행·열로 배치합니다. mainloop() 앞에 추가합니다.',
                     code='grid_frame = tk.____(root)\ngrid_frame.pack(pady=10)\ntk.Label(grid_frame, text="이름").____(row=0, column=0)\ntk.Entry(grid_frame).grid(row=0, column=1)\ntk.Label(grid_frame, text="학번").grid(row=1, column=0)\ntk.Entry(grid_frame).grid(row=1, column=1)',
                     answer_code='grid_frame = tk.Frame(root)\ngrid_frame.pack(pady=10)\ntk.Label(grid_frame, text="이름").grid(row=0, column=0)\ntk.Entry(grid_frame).grid(row=0, column=1)\ntk.Label(grid_frame, text="학번").grid(row=1, column=0)\ntk.Entry(grid_frame).grid(row=1, column=1)',
                     blanks=['첫 번째 빈칸: 여러 위젯을 묶는 컨테이너 클래스 이름','두 번째 빈칸: 행·열로 배치하는 메서드 이름'],
                     expect='pack 폼 아래에 이름·학번 폼이 한 번 더 나타나는데, 이번에는 라벨과 입력창이 행·열로 나란히 정렬됩니다.'),
                dict(mode='describe',text='확인 버튼을 만들어 grid_frame에 추가하고, 두 열에 걸쳐(columnspan=2) 넓게 배치하세요. grid()의 sticky 옵션으로 좌우로 늘어나게 해 보세요.',
                     answer_code='confirm = tk.Button(grid_frame, text="확인")\nconfirm.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)',
                     expect='grid 폼 아래에 입력창 두 칸 너비만큼 넓은 "확인" 버튼이 보입니다.'),
            ])],
    ),
    'events': dict(
        title='이벤트 처리',
        pages='51',
        slides=[
            dict(n=36, alt='4. 이벤트 처리 — 사용자 동작에 반응하기', explain=[
                'GUI에서는 버튼 클릭, 텍스트 입력 등 다양한 <b>이벤트</b>가 발생합니다. tkinter는 이러한 사용자 동작에 반응하기 위해 이벤트 처리 함수(콜백, callback)를 연결할 수 있도록 지원합니다.',
                '예를 들어, 버튼을 클릭했을 때 특정 동작을 실행하고 싶다면 다음과 같이 작성합니다.',
                '<pre><code>def 인사():\n    print("안녕하세요")\n\nbtn = tk.Button(root, text="누르기", command=인사)\nbtn.pack()</code></pre>',
                '<code>command=인사</code>처럼 함수 이름만 전달해야 합니다. <code>command=인사()</code>처럼 괄호를 붙이면 버튼을 만드는 시점에 바로 함수가 실행되어 버리므로, 정작 버튼을 클릭했을 때는 아무 일도 일어나지 않습니다. 함수는 클릭이라는 이벤트가 발생한 뒤에 호출되어야 합니다.',
            ]),
        ],
        practice=[dict(kind='tutorial', id='events-click-counter', title='버튼 클릭 수 세기',
            pc=True, steps=[
                dict(mode='full',text='클릭 수를 보여 줄 Label을 만듭니다.',
                     code='import tkinter as tk\n\nroot = tk.Tk()\nroot.title("클릭 수 세기")\n\ncount = 0\ncount_label = tk.Label(root, text="클릭 수: 0")\ncount_label.pack(pady=10)\n\nroot.mainloop()',
                     expect='"클릭 수: 0"이라는 글자가 있는 창이 뜹니다.'),
                dict(mode='blank',text='누를 때마다 count를 1씩 늘리고 라벨을 갱신하는 함수를 만들어 버튼에 연결합니다. count는 함수 밖의 변수이므로 함수 안에서 global로 선언합니다. mainloop() 앞에 추가합니다.',
                     code='def click():\n    ____ count\n    count += 1\n    count_label.____(text=f"클릭 수: {count}")\n\nclick_button = tk.Button(root, text="누르기", command=click)\nclick_button.pack()',
                     answer_code='def click():\n    global count\n    count += 1\n    count_label.config(text=f"클릭 수: {count}")\n\nclick_button = tk.Button(root, text="누르기", command=click)\nclick_button.pack()',
                     blanks=['첫 번째 빈칸: 함수 밖 변수를 함수 안에서 수정하려 할 때 쓰는 키워드','두 번째 빈칸: 위젯의 속성을 바꾸는 메서드 이름'],
                     expect='"누르기" 버튼을 누를 때마다 "클릭 수: 1", "클릭 수: 2"처럼 숫자가 하나씩 늘어납니다.'),
                dict(mode='describe',text='count를 0으로 되돌리는 초기화 함수 reset()을 만들고, "초기화" 버튼을 만들어 연결하세요. click() 함수에서 global을 어떻게 썼는지 떠올려 같은 방식으로 작성하세요.',
                     answer_code='def reset():\n    global count\n    count = 0\n    count_label.config(text="클릭 수: 0")\n\nreset_button = tk.Button(root, text="초기화", command=reset)\nreset_button.pack()',
                     expect='여러 번 누른 뒤 "초기화" 버튼을 누르면 클릭 수가 다시 0으로 돌아갑니다.'),
            ])],
    ),
    'memo': dict(
        title='GUI 앱 개발 · 나만의 메모장 만들기',
        pages='52–55',
        slides=[
            dict(n=44, alt='나만의 메모장 만들기 — 오늘의 목표', explain=[
                '텍스트 중심의 코드를 넘어서, 시각적인 인터페이스를 가진 앱을 만드는 과정은 매우 흥미롭고 실생활에도 유용하게 활용될 수 있습니다. 이 소단원에서는 파이썬의 tkinter 라이브러리를 활용하여 간단한 <b>메모장 애플리케이션</b>을 제작합니다.',
                '사용자로부터 입력을 받아 저장하고, 저장된 파일을 다시 열어 내용을 확인할 수 있는 기능을 구현함으로써 GUI 구성 요소의 활용과 파일 입출력 기능을 종합적으로 이해할 수 있습니다. 전체 과정은 여덟 단계로 나누어 진행합니다.',
            ]),
            dict(n=45, alt='1. 라이브러리 불러오기 · 2. 메인 창 구성', explain=[
                '<b>1. 필요한 라이브러리 불러오기</b>',
                '<pre><code>import tkinter as tk\nfrom tkinter import filedialog</code></pre>',
                'tkinter는 GUI 구성에 필요한 기본 위젯을 제공하고, filedialog는 파일 열기 및 저장 대화 상자 기능을 제공합니다.',
                '<b>2. 메인 창 구성</b>',
                '<pre><code>window = tk.Tk()\nwindow.title("나만의 메모장")</code></pre>',
                'Tk()를 통해 GUI 창을 생성하고, title()로 제목을 설정합니다.',
            ]),
            dict(n=46, alt='4. 파일 열기 기능 · 5. 파일 저장 기능', explain=[
                '<b>3. 텍스트 입력 영역 구성</b>(45쪽 슬라이드에서 이어짐): <code>text_area = tk.Text(window, wrap="word")</code>로 여러 줄 입력 영역을 만들고, <code>text_area.pack(expand=1, fill="both")</code>로 창의 남는 공간을 모두 채우도록 배치합니다. <code>wrap="word"</code>는 단어 단위로 줄을 바꾼다는 뜻입니다.',
                '<b>4. 파일 열기 기능</b>',
                '<pre><code>def open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            text = file.read()\n            text_area.delete("1.0", tk.END)\n            text_area.insert(tk.END, text)</code></pre>',
                '<code>askopenfilename()</code>을 통해 사용자가 파일을 선택할 수 있습니다. 선택된 파일을 열어 내용을 텍스트 영역에 삽입합니다. 사용자가 대화 상자를 취소하면 file_path가 빈 문자열이 되어 <code>if file_path:</code>가 거짓이 되므로 아무 일도 일어나지 않습니다.',
                '<b>5. 파일 저장 기능</b>',
                '<pre><code>def save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.write(text_area.get("1.0", tk.END))</code></pre>',
                '<code>asksaveasfilename()</code>을 통해 저장할 위치를 설정하고, 텍스트 내용을 파일로 저장합니다.',
            ]),
            dict(n=47, alt='6. 메뉴 구성 · 7. 프로그램 실행', explain=[
                '<b>6. 메뉴 구성</b>',
                '<pre><code>menu = tk.Menu(window)\nwindow.config(menu=menu)\n\nfile_menu = tk.Menu(menu, tearoff=0)\nmenu.add_cascade(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_command(label="종료", command=window.quit)</code></pre>',
                '메뉴는 Menu 클래스를 통해 생성하며, 하위 항목을 추가하여 기능을 연결합니다. <code>add_cascade</code>는 상위 메뉴("파일")를 달고, <code>add_command</code>는 그 아래 항목을 만듭니다.',
                '<b>7. 프로그램 실행</b>',
                '<pre><code>window.mainloop()</code></pre>',
                '<code>mainloop()</code>는 tkinter 이벤트 루프를 실행시켜 사용자 입력을 기다립니다. 이 줄이 있어야 창이 닫히지 않고 유지됩니다.',
            ]),
            dict(n=48, alt='8. 전체 코드 ① — 01~20행', explain=[
                '<b>8. 전체 코드</b>: 앞서 배운 내용을 기반으로 작성한 전체 코드의 앞부분(01~23행)입니다.',
                '<pre><code>01  import tkinter as tk\n02  from tkinter import filedialog\n03\n04  # 메모장 열기 기능 정의\n05  def open_file():\n06      file_path = filedialog.askopenfilename()\n07      if file_path:\n08          with open(file_path, "r", encoding="utf-8") as file:\n09              content = file.read()\n10              text_area.delete("1.0", tk.END)\n11              text_area.insert(tk.END, content)\n12\n13  # 메모장 저장 기능 정의\n14  def save_file():\n15      file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n16      if file_path:\n17          with open(file_path, "w", encoding="utf-8") as file:\n18              file.write(text_area.get("1.0", tk.END))\n19\n20  # 윈도우 창 생성\n21  window = tk.Tk()\n22  window.title("나만의 메모장")\n23  window.geometry("600x400")</code></pre>',
                '01~02행은 라이브러리 임포트, 05~11행은 열기 기능, 14~18행은 저장 기능입니다. 함수는 <b>정의</b>만 되어 있고, 아직 호출되지 않습니다. 21~23행에서 창을 만들고 제목과 크기를 정합니다.',
            ]),
            dict(n=49, alt='8. 전체 코드 ② — 21~41행', explain=[
                '전체 코드의 나머지 부분(25~41행)입니다.',
                '<pre><code>25  # 텍스트 입력창 생성\n26  text_area = tk.Text(window, wrap="word")\n27  text_area.pack(expand=1, fill="both")\n28\n29  # 메뉴 구성\n30  menu_bar = tk.Menu(window)\n31  window.config(menu=menu_bar)\n32\n33  file_menu = tk.Menu(menu_bar, tearoff=0)\n34  menu_bar.add_cascade(label="파일", menu=file_menu)\n35  file_menu.add_command(label="열기", command=open_file)\n36  file_menu.add_command(label="저장", command=save_file)\n37  file_menu.add_separator()\n38  file_menu.add_command(label="종료", command=window.quit)\n39\n40  # GUI 실행\n41  window.mainloop()</code></pre>',
                '26~27행은 텍스트 입력창, 30~38행은 메뉴 구성입니다. 37행 <code>add_separator()</code>는 항목 사이에 구분선을 넣습니다. 41행 <code>mainloop()</code>가 실행되어야 비로소 창이 화면에 나타나고 클릭·입력을 받기 시작합니다.',
                '탐구 활동(55쪽): IDLE의 macosx.py 코드 일부입니다. 빈칸에 들어갈 라이브러리 이름과 코드를 적어 보세요. <pre><code>import ______\n\ndef _init_tk_type():\n    global _tk_type\n    if platform == \'darwin\':\n        root = ______.Tk()\n        ws = root.tk.call(\'tk\', \'windowingsystem\')\n        if \'x11\' in ws:\n            _tk_type = "xquartz"</code></pre> IDLE도 GUI 애플리케이션입니다 — 어떤 라이브러리로 만들어졌을지 생각해 보세요.',
            ]),
            dict(n=50, alt='실행하고 확인하기 — 체크리스트', explain=[
                '완성한 메모장을 실행하면서 다음을 확인하세요. 창 제목과 크기가 설정한 대로 보이는지, 텍스트 입력창에 자유롭게 글을 쓸 수 있는지, 파일 메뉴의 열기·저장이 실제로 동작하는지, 취소를 눌렀을 때 오류 없이 창이 그대로 유지되는지입니다.',
            ]),
            dict(n=60, alt='내가 만든 GUI, 이 다섯 가지를 확인해요(입력·이벤트·배치·파일·설명 점검표)', explain=[
                '메모장을 완성한 뒤 다섯 가지를 스스로 점검해 보세요. ① 입력: Text 위젯으로 여러 줄을 입력할 수 있는가. ② 이벤트: 메뉴 클릭이 open_file·save_file 함수를 정확히 호출하는가. ③ 배치: pack의 expand·fill로 창 크기에 맞게 입력창이 늘어나는가. ④ 파일: 열기·저장이 UTF-8로 올바르게 동작하고 취소 시 오류가 없는가. ⑤ 설명: 각 단계의 코드가 무슨 일을 하는지 내 말로 설명할 수 있는가.',
            ]),
        ],
        practice=['memo-tk', dict(kind='tutorial', id='memo-steps', title='교과서 메모장 여덟 단계로 따라 만들기',
            pc=True, steps=[
                dict(mode='full',text='① 라이브러리 불러오기. tkinter와 파일 대화 상자를 담당하는 filedialog를 불러옵니다.',
                     code='import tkinter as tk\nfrom tkinter import filedialog',
                     expect='아직 화면에 보이는 것은 없습니다. 오류 없이 실행되면 다음 단계로 넘어가세요.'),
                dict(mode='full',text='② 메인 창 구성. Tk()로 창을 만들고 title·geometry로 제목과 크기를 정합니다.',
                     code='import tkinter as tk\nfrom tkinter import filedialog\n\nwindow = tk.Tk()\nwindow.title("나만의 메모장")\nwindow.geometry("600x400")\n\nwindow.mainloop()',
                     expect='"나만의 메모장" 제목의 600×400 크기 빈 창이 뜹니다.'),
                dict(mode='full',text='③ 텍스트 입력 영역 구성. Text 위젯을 만들고 창을 가득 채우도록 배치합니다. mainloop() 앞에 추가합니다.',
                     code='text_area = tk.Text(window, wrap="word")\ntext_area.pack(expand=1, fill="both")',
                     expect='창 안에 여러 줄을 쓸 수 있는 흰 입력 영역이 창 전체를 채웁니다.'),
                dict(mode='blank',text='④ 파일 열기 기능. 창을 만들기 전(라이브러리 불러오기 다음)에 open_file() 함수를 정의합니다.',
                     code='def open_file():\n    file_path = filedialog.____()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            content = file.read()\n            text_area.____("1.0", tk.END)\n            text_area.insert(tk.END, content)',
                     answer_code='def open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            content = file.read()\n            text_area.delete("1.0", tk.END)\n            text_area.insert(tk.END, content)',
                     blanks=['첫 번째 빈칸: 파일 선택 대화 상자를 여는 함수 이름','두 번째 빈칸: 텍스트 영역의 기존 내용을 지우는 메서드 이름'],
                     expect='아직 실행 화면은 바뀌지 않습니다. 이 함수를 호출할 메뉴는 다음에 연결합니다.'),
                dict(mode='blank',text='⑤ 파일 저장 기능. open_file() 아래에 save_file() 함수를 이어서 정의합니다.',
                     code='def save_file():\n    file_path = filedialog.____(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.____(text_area.get("1.0", tk.END))',
                     answer_code='def save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.write(text_area.get("1.0", tk.END))',
                     blanks=['첫 번째 빈칸: 저장 위치를 묻는 대화 상자를 여는 함수 이름','두 번째 빈칸: 파일 객체에 내용을 쓰는 메서드 이름'],
                     expect='마찬가지로 아직 실행 화면은 바뀌지 않습니다.'),
                dict(mode='blank',text='⑥ 메뉴 구성. text_area.pack() 다음, mainloop() 앞에 메뉴를 추가합니다.',
                     code='menu_bar = tk.____(window)\nwindow.config(menu=menu_bar)\n\nfile_menu = tk.Menu(menu_bar, tearoff=False)\nmenu_bar.____(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_separator()\nfile_menu.add_command(label="종료", command=window.quit)',
                     answer_code='menu_bar = tk.Menu(window)\nwindow.config(menu=menu_bar)\n\nfile_menu = tk.Menu(menu_bar, tearoff=False)\nmenu_bar.add_cascade(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_separator()\nfile_menu.add_command(label="종료", command=window.quit)',
                     blanks=['첫 번째 빈칸: 메뉴를 만드는 클래스 이름','두 번째 빈칸: 상위 메뉴("파일")를 다는 메서드 이름'],
                     expect='창 위에 "파일" 메뉴가 생기고, 누르면 열기·저장·(구분선)·종료 항목이 보입니다.'),
                dict(mode='describe',text='⑦ 프로그램 실행. 지금까지 만든 조각을 모두 이어 붙여(라이브러리 → 함수 정의 → 창·텍스트 영역·메뉴 구성 → mainloop) 실행하세요. 메뉴의 "열기"로 텍스트 파일을 선택하면 내용이 입력창에 나타나고, "저장"을 누르면 입력한 내용이 파일로 저장되어야 합니다. 대화 상자에서 취소해도 오류 없이 창이 그대로 유지되는지 확인하세요.',
                     answer_code='import tkinter as tk\nfrom tkinter import filedialog\n\ndef open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            content = file.read()\n            text_area.delete("1.0", tk.END)\n            text_area.insert(tk.END, content)\n\ndef save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.write(text_area.get("1.0", tk.END))\n\nwindow = tk.Tk()\nwindow.title("나만의 메모장")\nwindow.geometry("600x400")\n\ntext_area = tk.Text(window, wrap="word")\ntext_area.pack(expand=1, fill="both")\n\nmenu_bar = tk.Menu(window)\nwindow.config(menu=menu_bar)\n\nfile_menu = tk.Menu(menu_bar, tearoff=False)\nmenu_bar.add_cascade(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_separator()\nfile_menu.add_command(label="종료", command=window.quit)\n\nwindow.mainloop()',
                     expect='열기·저장·취소를 각각 시험해 오류 없이 동작하는지 확인합니다.'),
                dict(mode='describe',text='⑧ 전체 코드. 지금까지 만든 코드를 순서대로 모으면 교과서 54~55쪽의 완성 코드가 됩니다. 함수 정의(열기·저장)가 먼저, 창 생성이 그 다음, 텍스트 영역·메뉴 구성이 이어지고, 마지막이 mainloop()라는 순서를 스스로 다시 적어 보세요.',
                     answer_code='import tkinter as tk\nfrom tkinter import filedialog\n\n# 메모장 열기 기능 정의\ndef open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            content = file.read()\n            text_area.delete("1.0", tk.END)\n            text_area.insert(tk.END, content)\n\n# 메모장 저장 기능 정의\ndef save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.write(text_area.get("1.0", tk.END))\n\n# 윈도우 창 생성\nwindow = tk.Tk()\nwindow.title("나만의 메모장")\nwindow.geometry("600x400")\n\n# 텍스트 입력창 생성\ntext_area = tk.Text(window, wrap="word")\ntext_area.pack(expand=1, fill="both")\n\n# 메뉴 구성\nmenu_bar = tk.Menu(window)\nwindow.config(menu=menu_bar)\n\nfile_menu = tk.Menu(menu_bar, tearoff=0)\nmenu_bar.add_cascade(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_separator()\nfile_menu.add_command(label="종료", command=window.quit)\n\n# GUI 실행\nwindow.mainloop()',
                     expect='메모장 앱이 정상적으로 실행되며, 열기·저장·종료가 모두 동작합니다. 이 코드는 practice 카드의 「교과서 메모장 · tkinter 전체 코드」 예제와 같습니다.'),
            ])],
    ),
    'review': dict(
        title='2단원 마무리 · 개념에서 앱까지',
        pages='56–59',
        slides=[
            dict(n=61, alt='02. GUI 프로그래밍 작성 핵심 정리 — tkinter 개요·구성 요소·메모장 개발 사례', explain=[
                '<b>1. tkinter의 개요와 역할</b>: tkinter는 파이썬에서 기본 제공되는 GUI 라이브러리로, 별도 설치 없이 사용 가능합니다. 버튼, 텍스트 상자, 메뉴 등 다양한 위젯을 통해 창 기반 프로그램을 쉽게 만들 수 있습니다.',
                '<b>2. tkinter의 구성 요소</b>: Tk 객체(<code>root = tk.Tk()</code>)가 기본 창을 생성하고, 위젯이 사용자와 상호 작용하는 인터페이스 요소이며, 배치 관리자(<code>pack()</code>, <code>grid()</code>, <code>place()</code>)가 위젯을 창에 배치하고, 이벤트 처리가 사용자의 동작에 따라 특정 동작을 수행합니다.',
                '<b>3. 주요 위젯 종류</b>: Label(표시), Button(클릭), Entry(한 줄 입력), Text(여러 줄 입력), Checkbutton(체크박스), Radiobutton(여러 옵션 중 하나), Listbox(목록 선택), Canvas(그리기), Frame(컨테이너)입니다.',
                '<b>4. GUI 앱 개발 사례: 메모장 만들기</b>: Tk()로 창 생성, title()과 geometry()로 제목과 크기 설정, Text 위젯으로 텍스트 입력 영역 구성, filedialog로 파일 열기·저장, Menu로 파일 메뉴 구성 및 버튼과 기능 연결, mainloop()로 프로그램을 실행했습니다.',
                '확인 학습(57쪽): 디버거 GUI 코드에서 ①·②·③에 들어갈 말이 무엇인지 아래 연습 문제에서 직접 풀어 보세요.',
            ]),
            dict(n=65, alt='정리하며 — UI 종류, tkinter 네 요소, 위젯 배치와 mainloop를 세 문장으로', explain=[
                '이 단원을 세 문장으로 정리하면 다음과 같습니다. ① 인터페이스에는 명령어를 입력하는 CLI, 클릭·터치로 조작하는 GUI, 음성·몸짓으로 조작하는 NUI가 있습니다. ② tkinter는 Tk 객체·위젯·배치 관리자·이벤트 처리, 네 요소로 GUI를 구성합니다. ③ 위젯을 만든 뒤 pack·grid·place로 배치하고, command로 이벤트를 연결하고, mainloop()로 실행해야 완성된 프로그램이 됩니다.',
                '대단원 종합 평가(58~59쪽)에서는 Tk 객체, UI의 정의, GUI 사례 구분, 버튼 클릭 결과, pack·place 등 배치 방식, 빈칸에 들어갈 배치 코드를 확인합니다.',
            ]),
        ],
        practice=[],
    ),
    'project': dict(
        title='통합 프로젝트 · 우리 반 생활 도우미',
        pages='수행평가 연결 · 확장',
        slides=[],
        practice=[dict(kind='tutorial', id='project-helper-app', title='메모장에서 배운 것으로 작은 도우미 앱 만들기',
            pc=True, steps=[
                dict(mode='full',text='메모장과 같은 방식으로 새 창을 만들고, 오늘 할 일을 적을 Entry와 "추가" 버튼, 목록을 보여줄 Listbox를 준비합니다.',
                     code='import tkinter as tk\n\nroot = tk.Tk()\nroot.title("우리 반 할 일 도우미")\n\ntask_entry = tk.Entry(root)\ntask_entry.pack(fill="x", padx=10, pady=6)\n\ntask_list = tk.Listbox(root)\ntask_list.pack(fill="both", expand=True, padx=10, pady=6)\n\nroot.mainloop()',
                     expect='할 일을 입력할 칸과 빈 목록 상자가 있는 창이 뜹니다.'),
                dict(mode='blank',text='"추가" 버튼을 눌렀을 때 입력한 할 일을 목록에 넣고 입력칸을 비우는 함수를 연결합니다. Entry가 비어 있으면 추가하지 않도록 if로 막습니다.',
                     code='def add_task():\n    text = task_entry.get().strip()\n    if text:\n        task_list.____(tk.END, text)\n        task_entry.____(0, tk.END)\n\nadd_button = tk.Button(root, text="추가", command=add_task)\nadd_button.pack(pady=4)',
                     answer_code='def add_task():\n    text = task_entry.get().strip()\n    if text:\n        task_list.insert(tk.END, text)\n        task_entry.delete(0, tk.END)\n\nadd_button = tk.Button(root, text="추가", command=add_task)\nadd_button.pack(pady=4)',
                     blanks=['첫 번째 빈칸: Listbox 끝에 항목을 추가하는 메서드 이름','두 번째 빈칸: Entry의 내용을 지우는 메서드 이름'],
                     expect='할 일을 쓰고 "추가"를 누르면 목록에 줄이 하나 늘고 입력칸이 비워집니다. 빈 채로 누르면 아무 일도 일어나지 않습니다.'),
                dict(mode='describe',text='목록에서 항목을 고른 뒤 "삭제" 버튼으로 지우는 remove_task() 함수를 만들고 버튼에 연결하세요. task_list.curselection()으로 선택한 위치(튜플)를 읽고, 선택된 것이 있을 때만 그 위치를 지우세요.',
                     answer_code='def remove_task():\n    selected = task_list.curselection()\n    if selected:\n        task_list.delete(selected[0])\n\nremove_button = tk.Button(root, text="삭제", command=remove_task)\nremove_button.pack(pady=4)',
                     expect='목록에서 항목을 클릭해 고른 뒤 "삭제"를 누르면 그 항목이 목록에서 사라집니다.'),
            ])],
    ),
}
