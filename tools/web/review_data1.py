"""기말 총정리 데이터 1: Ⅰ단원(모듈과 패키지)·Ⅱ단원(GUI). 교과서 쪽수는 인쇄 쪽 기준.

소단원 dict 키
  id, no, title, pages(교과서 쪽), web(소단원 웹 페이지 파일명 목록, unit 폴더 기준),
  summary(핵심 개념 3~5줄), code(dict | None), pitfalls(1~2개), checks([(질문, 답)] 2개)
code 키: title, files[(경로, 소스)], run(실행할 파일 | None), result(실행 결과 | None), note
"""

UNIT1 = dict(
    n=1,
    title='모듈과 패키지 활용',
    flow=[
        '코드가 길어지면 기능별로 나누어 파일 하나하나를 모듈로 만듭니다.',
        '모듈이 많아지면 폴더(패키지)로 묶어 용도별로 정리합니다.',
        '다른 파일의 코드는 import로 불러오고, 직접 실행했을 때만 돌릴 코드는 __name__ 검사로 감쌉니다.',
        '표준 라이브러리(os, sys, math, random, datetime)와 pip로 설치하는 써드파티 패키지를 가져다 씁니다.',
    ],
    terms=[
        ('모듈(module)', '함수, 클래스, 변수, 실행문 등의 파이썬 코드를 담은 파일. 모듈 이름은 파일명을 따릅니다.'),
        ('임포트(import)', '다른 모듈에 정의된 함수, 변수, 클래스를 현재 코드에서 쓸 수 있게 불러오는 일입니다.'),
        ('네임스페이스', '이름을 기준으로 객체를 구분해 저장하는 공간. 모듈마다 독립적입니다.'),
        ('패키지', '여러 모듈을 용도나 주제별로 디렉터리에 나누어 담아 관리하는 구조입니다.'),
        ('__name__', '현재 모듈의 이름이 저장된 내장 변수. 직접 실행하면 "__main__"이 됩니다.'),
        ('__init__.py', '패키지의 초기 설정이나 공통 실행 코드를 쓰는 파일. __all__을 정의할 수 있습니다.'),
        ('__all__', 'from 패키지 import * 로 가져올 모듈 목록을 지정하는 변수입니다.'),
        ('표준 라이브러리', '파이썬이 기본으로 제공하는 모듈 모음(os, sys, math, random, datetime 등)입니다.'),
        ('써드파티 패키지', '제3자가 개발한 패키지. PyPI에서 공유하며 pip install 프로젝트명으로 설치합니다.'),
    ],
    lessons=[
        dict(
            id='1-01-01', no='01-01', title='모듈의 개념 및 필요성', pages='9~10쪽', web=['overview'],
            summary=[
                '모듈은 함수, 클래스, 변수, 실행문 등의 파이썬 코드를 담은 파일입니다. 모듈은 파일 단위이고 이름은 파일명을 따릅니다.',
                '다른 모듈에 정의된 함수, 변수, 클래스를 불러와 쓰는 과정을 임포트라고 합니다.',
                '필요성은 네 가지입니다. 중복 방지와 유지·보수 효율, 재사용성, 프로그램 구조화, 네임스페이스 분리와 충돌 방지입니다.',
                '임포트하면 현재 작업 디렉터리, 환경 변수에 지정된 경로, 표준 라이브러리 디렉터리 순으로 모듈을 찾습니다(9쪽 좀 더 알아보기).',
            ],
            code=None,
            pitfalls=[
                '모듈은 함수 하나가 아니라 파일 하나입니다. 기능을 나눈 .py 파일이 곧 모듈입니다.',
                '공통 코드를 모듈 한 곳에 두면 수정할 때 그 모듈만 고치면 전체 프로그램에 반영됩니다. 함수를 프로그램마다 복사해 쓰면 이 장점이 사라집니다.',
            ],
            checks=[
                ('모듈이 무엇인지 한 문장으로 설명하세요.', '함수, 클래스, 변수, 실행문 등의 파이썬 코드를 담은 파일이며, 특정 기능을 하는 코드를 하나의 파일로 묶은 단위입니다(9쪽).'),
                ('서로 다른 모듈에 같은 이름의 함수가 있어도 구분해 호출할 수 있는 까닭은 무엇인가요?', '모듈마다 독립적인 네임스페이스가 있기 때문입니다(10쪽).'),
            ],
        ),
        dict(
            id='1-01-02', no='01-02', title='패키지의 개념 및 필요성', pages='11~12쪽', web=['overview'],
            summary=[
                '패키지는 여러 모듈을 용도나 주제별로 디렉터리에 나누어 담아 체계적으로 관리하기 위한 구조입니다.',
                '교과서 예시는 nature/ 아래에 animals/(bird.py, lion.py)와 plants/(tree.py, flower.py, grass.py)로 나눈 구조입니다(11쪽).',
                '필요성은 프로그램 규모가 커질수록 모듈 수가 늘기 때문입니다. 기능별로 나누고 폴더 단위로 묶으면 전체 구조가 한눈에 들어옵니다.',
                '새 기능을 넣을 위치와 고칠 위치를 쉽게 파악할 수 있습니다(12쪽).',
            ],
            code=None,
            pitfalls=[
                '모듈은 파일, 패키지는 폴더(디렉터리)입니다. 모듈을 한 폴더에 모아 두어도 임포트는 편하지만 한눈에 보기 어렵고 관리가 불편합니다(11쪽).',
            ],
            checks=[
                ('패키지를 한 문장으로 설명하세요.', '여러 모듈을 용도나 주제별로 디렉터리에 나누어 담아 체계적으로 관리하기 위한 구조입니다(11쪽).'),
                ('패키지를 쓰면 좋은 점을 두 가지 쓰세요.', '관련 모듈을 폴더 단위로 묶어 코드를 논리적으로 그룹화할 수 있고, 새 기능이나 수정할 코드의 위치를 쉽게 파악할 수 있습니다(12쪽).'),
            ],
        ),
        dict(
            id='1-02-01', no='02-01', title='모듈 정의하기', pages='15~18쪽', web=['define', 'entrypoint'],
            summary=[
                '모듈을 만드는 방법은 실행문, 함수, 클래스가 담긴 파이썬 코드를 파일로 저장하는 것입니다. 저장한 파일이 곧 모듈입니다.',
                '실행문만 있는 모듈은 임포트하는 순간 최상위 실행문이 즉시 실행됩니다. 재사용하기에는 유연성이 낮습니다.',
                '함수와 실행문이 함께 있으면 임포트할 때 실행문이 한 번 실행되어 예상과 다른 결과가 나올 수 있습니다.',
                '__name__은 직접 실행하면 "__main__", 임포트되면 모듈 이름이 됩니다. if __name__ == "__main__": 안의 코드는 직접 실행할 때만 동작합니다.',
            ],
            code=dict(
                title='circle_area3.py와 circle_main.py (18쪽)',
                files=[
                    ('circle_area3.py', 'PI = 3.14\ndef circlearea(r):\n    print("반지름이 {}인 원의 넓이: {}".format(r, r*r*PI))\nif __name__ == "__main__":\n    circlearea(4)\n'),
                    ('circle_main.py', 'import circle_area3\ncircle_area3.circlearea(3)\n'),
                ],
                run='circle_main.py',
                result='반지름이 3인 원의 넓이: 28.26',
                note='circle_main.py를 실행한 결과입니다. circle_area3.py를 직접 실행하면 반지름 4인 원의 넓이가 출력됩니다.',
            ),
            pitfalls=[
                'if __name__ == "__main__": 검사가 없는 circle_area2를 임포트하면 모듈 안의 circlearea(4)가 먼저 실행되어 출력 순서가 달라집니다(16쪽).',
                '같은 파일이라도 직접 실행하면 __name__은 "__main__"이고, 임포트되면 그 모듈의 이름(예: nameEx1)입니다(17쪽).',
            ],
            checks=[
                ('모듈을 직접 실행했을 때와 임포트했을 때 __name__ 값은 각각 무엇인가요?', '직접 실행하면 "__main__", 임포트되면 해당 모듈의 이름입니다(17쪽).'),
                ('임포트될 때는 실행되지 않고 직접 실행할 때만 동작하도록 하려면 어떻게 쓰나요?', 'if __name__ == "__main__": 아래에 그 실행문을 넣습니다(18쪽).'),
            ],
        ),
        dict(
            id='1-02-02', no='02-02', title='모듈과 패키지 사용하기', pages='19~25쪽', web=['imports', 'packages'],
            summary=[
                '모듈 임포트는 네 가지입니다. import 모듈(모듈명.함수()로 호출), from 모듈 import 함수(함수명만으로 호출), from 모듈 import *, import 모듈 as 새이름입니다.',
                'as로 이름을 바꾸면 원래 모듈 이름으로는 접근할 수 없습니다(21쪽).',
                '패키지 안의 모듈도 import로 가져옵니다. 경로는 점(.)으로 구분합니다. 예: from nature.animals import bird',
                'import 패키지.모듈 형식은 호출할 때마다 전체 경로를 써야 합니다. __init__.py의 __all__은 from 패키지 import * 로 가져올 모듈 목록을 정합니다.',
            ],
            code=dict(
                title='main_nature2.py (22쪽)',
                files=[
                    ('nature/animals/bird.py', 'def wild():\n    print("새는 동물입니다.")\n'),
                    ('main_nature2.py', 'from nature.animals import bird as b\n\nb.wild()\n'),
                ],
                run='main_nature2.py',
                result='새는 동물입니다.',
                note='교과서는 하위 호환성을 위해 각 폴더에 __init__.py를 만들도록 안내합니다(21쪽).',
            ),
            pitfalls=[
                'from greet import hello 로 가져오면 greet.hello()는 오류입니다. 반대로 import greet 로 가져오면 hello()만 쓸 수 없습니다(19~20쪽).',
                '__all__ = ["tree"] 이면 from nature.plants import * 후에 flower.wild()를 호출할 때 NameError가 납니다. 목록에 "flower"를 추가해야 합니다(24~25쪽).',
            ],
            checks=[
                ('from nature.animals import bird as b 로 가져온 뒤 bird.wild()를 호출하면 어떻게 되나요?', '원래 이름 bird로는 접근할 수 없어 오류가 납니다. b.wild()로 호출해야 합니다(22쪽).'),
                ('from 모듈 import * 의 단점을 쓰세요.', '모듈 간에 함수 이름이 겹칠 수 있고, 어떤 모듈의 코드인지 파악하기 어려워 유지·보수가 어려워집니다(20쪽).'),
            ],
        ),
        dict(
            id='1-02-03', no='02-03', title='여러 가지 모듈 활용하기', pages='26~33쪽', web=['os-sys', 'math', 'random', 'datetime', 'thirdparty'],
            summary=[
                'os 모듈은 운영체제와 관련된 기능(os.name, os.getcwd(), os.system() 등)을, sys 모듈은 시스템 정보(sys.argv, sys.exit())를 제공합니다.',
                'math는 pi, e 상수와 ceil, floor, factorial, gcd, pow 등 수학 계산을 제공합니다.',
                'random은 random(), uniform(), randrange(), choice(), shuffle(), sample()을, datetime은 now(), year, month, day, weekday() 등을 제공합니다.',
                '표준 라이브러리 밖의 제3자 모듈이 써드파티 패키지이며 PyPI에서 공유됩니다. pip install 프로젝트명으로 설치합니다.',
                'datetime.now()로 현재 날짜·시각을 구하고 year, month, day, hour, minute, second 속성으로 각 값을 꺼냅니다(32쪽).',
            ],
            code=dict(
                title='mathmodule.py 일부 (29쪽)',
                files=[
                    ('mathmodule.py', "import math\n\nprint(math.ceil(3.5), math.floor(3.5))\nprint(math.factorial(5), math.gcd(28, 70), math.pow(2, 10))\n"),
                ],
                run='mathmodule.py',
                result='4 3\n120 14 1024.0',
                note='올림, 내림, 5!, 최대 공약수, 2의 10승 순서이며 교과서 실행 결과(29쪽)와 같은 값입니다. 교과서의 설명 문구는 줄였습니다.',
            ),
            pitfalls=[
                'math.pow(2, 10)의 결과는 1024가 아니라 1024.0(실수)입니다(29쪽).',
                'random.shuffle(리스트)는 원래 리스트의 순서를 바꾸지만, random.choice(리스트)는 리스트를 바꾸지 않습니다(31쪽).',
                'datetime의 weekday()는 속성이 아니라 메서드이며 월요일~일요일을 0~6으로 돌려줍니다(32쪽).',
            ],
            checks=[
                ('리스트 L에서 값 2개를 중복 없이 뽑는 random 함수를 쓰세요.', 'random.sample(L, 2) 입니다(31쪽).'),
                ('pip로 써드파티 패키지를 설치하는 명령 형식은 무엇인가요?', 'pip install 프로젝트명 입니다(33쪽).'),
            ],
        ),
    ],
)

UNIT2 = dict(
    n=2,
    title='GUI 프로그래밍',
    flow=[
        '사용자 인터페이스(UI)는 사람과 기계가 만나는 접점이며 CLI, GUI, NUI로 나눕니다.',
        '파이썬 GUI 라이브러리로는 tkinter, PyQt, wxPython, Kivy가 있고, 이 교재는 기본 제공되는 tkinter로 실습합니다.',
        'tkinter 프로그램은 Tk 객체(창), 위젯, 배치 관리자, 이벤트 처리의 네 요소로 구성합니다.',
        '이를 합쳐 filedialog와 Menu로 파일 열기·저장이 되는 메모장 앱을 만들고 mainloop()로 실행합니다.',
    ],
    terms=[
        ('UI(사용자 인터페이스)', '사용자가 컴퓨터 시스템이나 소프트웨어를 쉽고 효율적으로 쓰도록 돕는 장치나 화면 구성. 사람과 기계가 만나는 접점입니다.'),
        ('CLI', '키보드로 명령어를 입력해 컴퓨터와 소통하는 명령줄 인터페이스입니다.'),
        ('GUI', '아이콘, 버튼, 메뉴 등을 마우스나 터치로 조작하는 그래픽 사용자 인터페이스입니다.'),
        ('NUI', '음성, 손짓, 터치 등 신체 동작을 기반으로 하는 자연 사용자 인터페이스입니다.'),
        ('tkinter', '파이썬에 기본으로 포함된 GUI 라이브러리. 별도 설치가 필요 없습니다.'),
        ('위젯(widget)', 'Label, Button, Entry 등 사용자와 상호 작용하는 인터페이스 요소입니다.'),
        ('배치 관리자', '위젯을 창에 배치하는 도구. pack(), grid(), place()가 있습니다.'),
        ('이벤트 처리(콜백)', '버튼 클릭 같은 사용자 동작에 반응해 실행되는 함수입니다.'),
        ('mainloop()', 'tkinter 이벤트 루프를 실행해 사용자 입력을 기다리게 하는 함수입니다.'),
    ],
    lessons=[
        dict(
            id='2-01-01', no='01-01', title='사용자 인터페이스', pages='43~44쪽', web=['ui'],
            summary=[
                '사용자 인터페이스(UI)는 사용자가 컴퓨터 시스템, 소프트웨어 등을 쉽고 효율적으로 쓰도록 돕는 장치나 화면 구성이며, 사람과 기계가 만나는 접점입니다.',
                'UI에는 버튼, 메뉴, 스크롤바, 입력 창, 알림 메시지, 폰트 크기, 색상 등 사용자가 보고 조작하는 모든 요소가 들어갑니다.',
                'CLI는 명령어를 키보드로 입력하는 방식으로 빠르고 가볍지만 명령어를 외워야 합니다. 주로 서버 관리, 개발 환경에서 씁니다.',
                'GUI는 마우스나 터치로 아이콘, 버튼, 메뉴를 조작하는 방식이고, NUI는 음성, 손짓, 터치 등 신체 동작을 기반으로 하는 방식입니다.',
            ],
            code=None,
            pitfalls=[
                'CLI는 그래픽 환경을 제공하는 인터페이스가 아니라 명령어를 입력하는 방식입니다. 확인 학습에서 옳지 않은 설명으로 나오는 대표 유형입니다(48쪽).',
                'UI는 화면 그림만이 아니라 버튼 위치, 메뉴 크기, 색깔, 글꼴, 사용 순서까지 포함합니다(43쪽).',
            ],
            checks=[
                ('"dir이라고 입력하면 폴더 목록이 나와요"는 어떤 인터페이스인가요?', 'CLI 입니다(44쪽 탐구 활동).'),
                ('"손을 흔들면 스마트 TV가 반응해요"는 어떤 인터페이스인가요?', 'NUI 입니다(44쪽 탐구 활동).'),
            ],
        ),
        dict(
            id='2-01-02', no='01-02', title='파이썬 GUI', pages='45~46쪽', web=['libraries'],
            summary=[
                'tkinter는 파이썬에서 기본 제공하는 GUI 라이브러리로 별도 설치가 필요 없고 입문자에게 적합합니다. 디자인이 현대적이지 않고 고급 기능에는 한계가 있습니다.',
                'PyQt는 C++ Qt 프레임워크를 파이썬에서 쓰게 한 것으로, 시각적으로 UI를 구성하는 Qt Designer를 제공하며 상업용 프로그램에도 쓰입니다. 설치가 필요하고 상업적 사용 시 라이선스를 확인해야 합니다.',
                'wxPython은 wxWidgets 기반으로 각 운영체제의 네이티브 위젯을 활용합니다.',
                'Kivy는 터치 기반 UI를 포함한 멀티 플랫폼 프레임워크로 GPU 가속을 지원하며, 복잡한 인터페이스나 애니메이션에 어울립니다.',
            ],
            code=None,
            pitfalls=[
                '라이브러리와 설명을 짝지을 때, 네이티브 스타일은 wxPython, 터치 중심 멀티 플랫폼은 Kivy, C++ Qt 기반은 PyQt, 기본 제공은 tkinter입니다(47~48쪽).',
                '파이썬 기본 개발 환경인 IDLE도 tkinter로 만든 GUI 애플리케이션입니다(46쪽).',
            ],
            checks=[
                ('별도 설치 없이 쓸 수 있는 파이썬 기본 GUI 라이브러리는 무엇인가요?', 'tkinter 입니다(45쪽).'),
                ('운영체제의 네이티브 위젯을 활용해 플랫폼 고유의 인터페이스를 구현하는 라이브러리는 무엇인가요?', 'wxPython 입니다(45쪽).'),
            ],
        ),
        dict(
            id='2-02-01', no='02-01', title='tkinter의 구성 요소', pages='50~51쪽', web=['widgets', 'layout', 'events'],
            summary=[
                'tkinter는 Tk 객체, 위젯, 배치 관리자, 이벤트 처리의 네 가지 요소로 구성합니다.',
                'Tk 객체(root = tk.Tk())는 프로그램의 기본 창이며 모든 위젯은 이 창 위에 생성됩니다.',
                '위젯은 Label, Button, Entry, Text, Checkbutton, Radiobutton, Listbox, Canvas, Frame 등입니다. 배치 관리자는 pack()(순차), grid()(행과 열), place()(좌표)입니다.',
                '이벤트 처리는 버튼 클릭 같은 동작에 반응하는 함수(callback)를 연결하는 것입니다. 예: Button(root, text="누르기", command=인사)',
                "레이블 글자를 바꿀 때는 label.config(text=...)를 쓰고, 버튼 함수 안에서 바깥 변수 값을 바꾸려면 global로 선언합니다(웹 실습 '이벤트 처리').",
            ],
            code=dict(
                title='이벤트 처리 예 (51쪽)',
                files=[
                    ('event_demo.py', 'import tkinter as tk\n\nroot = tk.Tk()\ndef 인사():\n    print("안녕하세요")\nbtn = tk.Button(root, text="누르기", command=인사)\nbtn.pack()\n'),
                ],
                run=None,
                result=None,
                note='창을 띄워야 하는 코드라 실행 결과를 적지 않았습니다. 교과서 발췌에는 root.mainloop()가 없으므로 실제로 창을 유지하려면 마지막에 추가해야 합니다(54쪽).',
            ),
            pitfalls=[
                'GUI 창을 만드는 객체는 Tk()입니다. Entry(), Frame(), Label(), Button()은 창이 아니라 위젯입니다(51쪽 탐구 활동).',
                '위젯은 만들기만 하면 끝이 아니라 pack(), grid(), place() 같은 배치 관리자로 위치와 정렬을 정해야 합니다(51쪽).',
            ],
            checks=[
                ('pack(), grid(), place()는 각각 위젯을 어떻게 배치하나요?', 'pack()은 위에서 아래로 차례대로, grid()는 행과 열로, place()는 좌표(x, y)를 지정해 배치합니다(51쪽).'),
                ('버튼을 눌렀을 때 함수가 실행되게 하려면 Button에 어떤 옵션을 쓰나요?', 'command=함수이름 옵션으로 이벤트 처리 함수를 연결합니다(51쪽).'),
            ],
        ),
        dict(
            id='2-02-02', no='02-02', title='GUI 앱 개발', pages='52~55쪽', web=['memo'],
            summary=[
                '메모장 앱은 tkinter와 filedialog를 불러오는 것에서 시작합니다. filedialog는 파일 열기·저장 대화 상자를 제공합니다.',
                'tk.Tk()로 창을 만들고 title()로 제목, geometry()로 크기를 정합니다. Text(window, wrap="word")는 여러 줄 입력 영역이며 pack(expand=1, fill="both")으로 남는 공간을 채웁니다.',
                '파일 열기는 askopenfilename()으로 경로를 받아 읽은 뒤 Text에 넣고, 저장은 asksaveasfilename()으로 경로를 받아 Text 내용을 씁니다.',
                'Menu로 파일 메뉴를 만들어 열기, 저장, 종료를 command로 연결하고, 마지막에 mainloop()로 이벤트 루프를 실행합니다.',
                'asksaveasfilename(defaultextension=".txt")는 저장할 때 확장자를 입력하지 않으면 .txt를 붙여 줍니다(53쪽 코드).',
            ],
            code=dict(
                title='open_file 함수 (53쪽)',
                files=[
                    ('open_file_part.py', "def open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, 'r', encoding='utf-8') as file:\n            text = file.read()\n            text_area.delete('1.0', tk.END)\n            text_area.insert(tk.END, text)\n"),
                ],
                run=None,
                result=None,
                note='파일 선택 창이 필요해 실행 결과를 적지 않았습니다. 전체 코드는 54~55쪽에 있습니다.',
            ),
            pitfalls=[
                'mainloop()를 호출해야 이벤트 루프가 돌며 사용자 입력을 기다립니다. 실행 부분의 마지막 줄입니다(54쪽).',
                '파일을 열 때는 기존 내용을 delete("1.0", tk.END)로 지운 뒤 insert하고, 저장할 때는 get("1.0", tk.END)로 전체 내용을 읽어 씁니다(53쪽).',
            ],
            checks=[
                ('메모장 앱에서 파일 열기와 저장에 쓰는 filedialog 함수 이름을 각각 쓰세요.', '열기는 askopenfilename(), 저장은 asksaveasfilename() 입니다(53쪽).'),
                ('메뉴(Menu)에 열기·저장·종료 항목을 어떻게 연결하나요?', 'add_cascade로 "파일" 메뉴를 붙이고, add_command(label=..., command=...)로 각 함수를 연결합니다(53쪽).'),
            ],
        ),
    ],
)
