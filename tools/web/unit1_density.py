"""Unit I extra examples for #59. Imported at the end of content.py.

Adds focused labs so thin topics (overview, math, thirdparty, and nearby
pages) are independently complete. New APIs use pre_api/glossary.
Console examples stay screenshot-empty (no GUI capture pipeline).
"""
from content import ex, units, core


def _lesson(lesson_id):
    return next(lesson for lesson in units[1] if lesson['id'] == lesson_id)


def _set_examples(lesson_id, ids):
    _lesson(lesson_id)['examples'] = list(ids)


ex('copy-twice', '같은 함수를 두 파일에 복사하면', {
    'main.py': '''import homework1
import homework2
print("두 숙제가 각자 add를 가지고 있습니다.")''',
    'homework1.py': '''def add(a, b):
    return a + b

print("숙제1:", add(3, 5))''',
    'homework2.py': '''def add(a, b):
    return a + b

print("숙제2:", add(10, -2))''',
},
    pre_api=[
        {'name': '복사한 함수', 'signature': 'homework1.py와 homework2.py의 add',
         'note': '같은 함수를 파일마다 붙여 넣으면 오류를 두 곳에서 고쳐야 합니다. 다음 예제 reuse는 한 모듈만 고칩니다.'},
        {'name': 'import와 최상위 실행', 'signature': 'import homework1',
         'note': '임포트하면 그 파일의 최상위 print가 바로 실행됩니다. 함수 정의만 쓰려면 호출을 가드 안으로 옮깁니다.'},
    ],
    glossary=[
        {'term': '중복', 'meaning': '같은 코드를 여러 파일에 두는 것입니다. 모듈은 한 정의를 여러 프로그램이 불러 쓰게 합니다.'},
    ])

ex('two-adds', '같은 이름 add, 다른 모듈', {
    'main.py': '''import calculator
import counter
print("합:", calculator.add(3, 5))
print("하나 증가:", counter.add(1))''',
    'calculator.py': '''def add(a, b):
    return a + b''',
    'counter.py': '''def add(n):
    return n + 1''',
},
    checks='assert calculator.add(0, 4) == 4\nassert counter.add(1) == 2',
    pre_api=[
        {'name': '네임스페이스', 'signature': 'calculator.add  ·  counter.add',
         'note': '함수 이름이 같아도 모듈 이름이 앞에 붙으면 서로 다른 함수입니다. 한 파일에 add만 있으면 어느 쪽인지 모호합니다.'},
    ],
    glossary=[
        {'term': '모듈 이름', 'meaning': '파일 calculator.py의 모듈 이름은 calculator입니다. 확장자 .py는 이름에 들어가지 않습니다.'},
    ])

ex('import-clash', '같은 함수 이름 · 별칭으로 구별', {
    'main.py': '''from greet import hello
from farewell import hello as bye_hello
hello()
bye_hello()''',
    'greet.py': '''def hello():
    print("안녕하세요")''',
    'farewell.py': '''def hello():
    print("안녕히 가세요")''',
},
    pre_api=[
        {'name': 'from … import … as', 'signature': 'from farewell import hello as bye_hello',
         'note': '두 모듈에 hello가 있으면 두 번째 from이 첫 이름을 덮습니다. as로 새 이름을 붙이면 둘 다 남습니다.'},
    ],
    glossary=[
        {'term': '이름 덮어쓰기', 'meaning': '같은 이름으로 두 번 연결하면 나중 것이 남습니다. 모듈 접두어(greet.hello)를 쓰면 덮이지 않습니다.'},
    ])

ex('sys-modules', 'sys.path와 이미 불러온 모듈', {
    'main.py': '''import sys
print("sys.path[0] (지금 폴더):", sys.path[0])
print("불러오기 전 math:", "math" in sys.modules)
import math
print("불러온 뒤 math:", "math" in sys.modules)
import math
print("두 번째 import 뒤에도 pi:", math.pi)''',
},
    pre_api=[
        {'name': 'sys.path', 'signature': 'sys.path[0]',
         'note': '모듈을 찾는 폴더 목록입니다. 첫 항목은 보통 지금 실행 중인 스크립트 폴더입니다.'},
        {'name': 'sys.modules', 'signature': '"math" in sys.modules',
         'note': '이미 불러온 모듈의 캐시입니다. 같은 인터프리터에서 import를 다시 해도 파일은 보통 다시 실행되지 않습니다.'},
    ],
    glossary=[
        {'term': 'ModuleNotFoundError', 'meaning': '이름·실행 위치·sys.path를 순서대로 확인하세요. 파일명은 맞는데 폴더가 다르면 자주 납니다.'},
    ])

ex('math-circle', 'math.pi로 원 넓이', {
    'main.py': '''import math

def circle_area(r):
    return math.pi * r ** 2

print(circle_area(3))
print("소수 둘째 자리:", round(circle_area(3), 2))
print("거듭제곱 연산자:", 2 ** 10, " / math.pow:", math.pow(2, 10))''',
},
    checks='assert abs(circle_area(3) - math.pi * 9) < 1e-9',
    pre_api=[
        {'name': 'math.pi', 'signature': 'math.pi',
         'note': '원주율 상수입니다. 괄호를 붙이지 않습니다. pi()는 TypeError입니다.'},
        {'name': '** 와 math.pow', 'signature': 'r ** 2  ·  math.pow(2, 10)',
         'note': '**는 정수 거듭제곱에 자주 씁니다. math.pow는 항상 실수(1024.0)를 반환합니다.'},
    ],
    glossary=[
        {'term': '29쪽 원 넓이', 'meaning': '직접 3.14를 쓰기보다 math.pi를 쓰면 자릿수를 마음대로 줄이거나 늘릴 수 있습니다.'},
    ])

ex('math-signed', '음수에서 올림과 내림', {
    'main.py': '''import math
print("양수 3.5 → ceil", math.ceil(3.5), "/ floor", math.floor(3.5))
print("음수 -3.5 → ceil", math.ceil(-3.5), "/ floor", math.floor(-3.5))
print("0에 가까운 쪽이 올림인가?", math.ceil(-3.5) == -3)''',
},
    checks='assert math.ceil(-3.5) == -3\nassert math.floor(-3.5) == -4',
    pre_api=[
        {'name': 'math.ceil', 'signature': 'math.ceil(x)',
         'note': 'x 이상인 최소 정수입니다. -3.5의 올림은 -3입니다. 0에 가까운 쪽이 아닙니다.'},
        {'name': 'math.floor', 'signature': 'math.floor(x)',
         'note': 'x 이하인 최대 정수입니다. -3.5의 내림은 -4입니다. 수직선에서 왼쪽입니다.'},
    ],
    glossary=[
        {'term': '수직선', 'meaning': '올림·내림은 "더 크게/더 작게"입니다. 절댓값이 작아지는 방향(0으로)이 아닙니다.'},
    ])

ex('random-seed', '시드를 고정하면 같은 난수', {
    'main.py': '''import random
random.seed(42)
first = [random.randrange(1, 7) for _ in range(5)]
random.seed(42)
second = [random.randrange(1, 7) for _ in range(5)]
print(first)
print(second)
print("같은가?", first == second)''',
},
    checks='assert first == second',
    pre_api=[
        {'name': 'random.seed', 'signature': 'random.seed(42)',
         'note': '난수 생성기의 시작점을 정합니다. 같은 시드·같은 호출 순서면 같은 수가 나옵니다. 검사·시연에 씁니다.'},
    ],
    glossary=[
        {'term': '재현', 'meaning': '수업에서 "주사위가 3이어야 한다"고 검사하면 안 됩니다. 시드를 고정한 뒤 수열을 비교하세요.'},
    ])

ex('random-sample', 'sample은 원본을 남긴다', {
    'main.py': '''import random
random.seed(7)
names = ["민지", "수빈", "하늘", "지우"]
picked = random.sample(names, 2)
print("추첨:", picked)
print("원본:", names)
copied = names.copy()
random.shuffle(copied)
print("섞은 복사본:", copied)
print("원본 유지:", names)''',
},
    checks='assert names == ["민지", "수빈", "하늘", "지우"]\nassert len(picked) == 2',
    pre_api=[
        {'name': 'random.sample', 'signature': 'random.sample(names, 2)',
         'note': '지정 개수를 비복원으로 뽑아 새 리스트를 반환합니다. 원본 순서는 그대로입니다.'},
        {'name': 'list.copy', 'signature': 'copied = names.copy()',
         'note': 'shuffle은 원본을 바꿉니다. 원본을 남기려면 복사한 뒤 섞거나 sample을 씁니다.'},
    ],
    glossary=[
        {'term': '비복원', 'meaning': '한 번 뽑힌 위치는 다시 뽑히지 않습니다. 명단에 같은 이름이 두 번 있으면 결과는 중복될 수 있습니다.'},
    ])

ex('weekday-fixed', '고정 날짜의 요일', {
    'main.py': '''from datetime import date
day = date(2026, 9, 15)
week = "월화수목금토일"
print(day.isoformat(), week[day.weekday()] + "요일")
print("weekday()는 월요일 0:", day.weekday())
print("일요일은 6:", date(2026, 9, 20).weekday())''',
},
    checks='assert date(2026, 9, 15).weekday() == 1\nassert date(2026, 9, 20).weekday() == 6',
    pre_api=[
        {'name': 'date(y, m, d)', 'signature': 'date(2026, 9, 15)',
         'note': '달력 날짜 객체입니다. 시각이 없어 일수 계산에 유리합니다. datetime.now()와 빼면 타입이 다를 수 있습니다.'},
        {'name': 'weekday', 'signature': 'day.weekday()',
         'note': '월요일 0 … 일요일 6입니다. 요일 글자는 문자열로 따로 대응합니다. 괄호가 있는 메서드입니다.'},
    ],
    glossary=[
        {'term': '38쪽 요일', 'meaning': 'year·month·day는 속성(괄호 없음), weekday는 메서드(괄호 있음)입니다.'},
    ])

ex('pypi-names', '설치 이름과 import 이름', {
    'main.py': '''pairs = [
    ("beautifulsoup4", "bs4", "HTML에서 정보 추출"),
    ("pillow", "PIL", "이미지 크기·형식"),
    ("numpy", "numpy", "배열·수치 계산"),
    ("scikit-learn", "sklearn", "머신러닝"),
]
print("설치 이름 → import 이름")
for install, imported, use in pairs:
    print(f"{install:16} → {imported:8}  ({use})")
print("pip 명령은 터미널에서 실행합니다. 코드 입력창이 아닙니다.")''',
},
    pre_api=[
        {'name': '설치 이름', 'signature': 'python -m pip install beautifulsoup4',
         'note': 'PyPI에 올라간 배포 이름입니다. 교과서의 pip install bs4 대신 beautifulsoup4를 씁니다.'},
        {'name': 'import 이름', 'signature': 'import bs4  ·  from PIL import Image',
         'note': '코드에서 쓰는 이름입니다. 설치 이름과 다를 수 있습니다. 공식 문서의 Import 줄을 확인하세요.'},
    ],
    glossary=[
        {'term': 'PyPI', 'meaning': '파이썬 패키지를 찾는 공개 저장소입니다. pip가 여기서 내려받습니다.'},
    ])

ex('stdlib-json', '표준 라이브러리로 먼저 해결', {
    'main.py': '''import json
data = {"scores": [70, 80, 90]}
text = json.dumps(data, ensure_ascii=False)
print(text)
print(json.loads(text)["scores"])''',
},
    checks='assert json.loads(text)["scores"] == [70, 80, 90]',
    pre_api=[
        {'name': 'json.dumps', 'signature': 'json.dumps(data, ensure_ascii=False)',
         'note': '딕셔너리를 JSON 문자열로 바꿉니다. 한글을 그대로 두려면 ensure_ascii=False입니다.'},
        {'name': 'json.loads', 'signature': 'json.loads(text)',
         'note': '문자열을 다시 파이썬 객체로 읽습니다. 외부 패키지 없이 표준 라이브러리만 사용합니다.'},
    ],
    glossary=[
        {'term': '표준 vs 서드파티', 'meaning': 'json·math·random은 설치 없이 쓸 수 있습니다. NumPy처럼 배열이 필요할 때만 pip를 씁니다.'},
    ])

ex('project-roll', '기능 모듈 한 함수만 검사', {
    'main.py': '''from core.logic import roll
print("6면:", roll(6))
print("20면:", roll(20))''',
    **core,
},
    checks='assert 1 <= roll(6) <= 6\nassert 1 <= roll(20) <= 20',
    pre_api=[
        {'name': 'from core.logic import roll', 'signature': 'from core.logic import roll',
         'note': '패키지 core의 모듈 logic에서 함수 하나만 가져옵니다. 화면 코드는 아직 없습니다.'},
    ],
    glossary=[
        {'term': '한 함수부터', 'meaning': '주사위만 통과하면 days_left·draw를 같은 파일에 추가하기 쉽습니다. 다음 예제 core가 세 함수를 함께 검사합니다.'},
    ])

ex('review-two-files', '처음부터 두 파일 만들고 호출', {
    'main.py': '''import greet
greet.hello()''',
    'greet.py': '''def hello():
    print("안녕하세요")''',
},
    pre_api=[
        {'name': '두 파일', 'signature': 'greet.py + main.py',
         'note': '예제를 보지 않고 함수 정의 파일과 import 파일을 직접 만듭니다. greet.hello()처럼 모듈 이름을 붙입니다.'},
    ],
    glossary=[
        {'term': '종합 평가 뼈대', 'meaning': '모듈 정의 → import 방식에 맞춘 호출 → 임포트 때 실행되는 줄 구별. 아래 final-output에서 출력을 추적하세요.'},
    ])


def apply():
    """Patch Unit I lesson lists/prose after content.py has defined the base lessons."""
    _lesson('overview')['paragraphs'].append(
        '복사를 두 파일에 두면 같은 오류를 두 번 고칩니다. 같은 이름 add라도 calculator.add와 counter.add로 구별됩니다. '
        '아래는 복사본 → 한 모듈 재사용 → 이름 충돌 없는 호출 순서입니다. 13쪽 확인학습의 합 모듈은 define의 sum-input에서 이어서 만듭니다.'
    )
    _lesson('define')['paragraphs'].append(
        '실행문만 있는 파일, 함수만 있는 파일, 둘이 섞인 파일을 같은 페이지에서 비교하세요. '
        'import 한 줄에 출력이 두 번이면, 모듈 최상위 호출이 먼저 실행된 것입니다. 클래스는 인스턴스를 만든 뒤 메서드를 호출합니다.'
    )
    _lesson('entrypoint')['paragraphs'].append(
        '__main__은 파일 이름이 아닙니다. 지금 직접 실행 중인 모듈의 __name__ 값입니다. '
        '웹 실습창에서 circle_area3.py를 진입점으로 바꾸면 if 안이 실행되고, main.py로 실행하면 건너뜁니다.'
    )
    _lesson('imports')['paragraphs'].append(
        '다섯 문장을 외우기보다 "지금 연결된 이름이 무엇인가"만 보세요. '
        '두 모듈에 hello가 있으면 from … import hello를 두 번 쓰지 말고, 한쪽은 as로 바꾸거나 모듈 접두어를 유지하세요.'
    )
    _lesson('packages')['paragraphs'].append(
        'from nature.animals import *는 __all__에 적힌 모듈 이름만 가져옵니다. '
        'from nature.animals.bird import *는 bird 모듈의 함수를 가져옵니다. 대상이 패키지인지 모듈인지 먼저 구별하세요.'
    )
    _lesson('os-sys')['paragraphs'].append(
        '파일을 못 찾으면 이름보다 실행 위치를 보세요. sys.path[0]이 지금 폴더입니다. '
        '이미 import한 모듈은 sys.modules에 남으므로, 같은 실행에서 파일을 고친 뒤 다시 import만 하면 예전 코드가 남을 수 있습니다.'
    )
    _lesson('math')['paragraphs'].append(
        '상수(pi, e)에는 괄호가 없고, 계산 함수에는 괄호가 있습니다. '
        '원 넓이는 math.pi * r ** 2로 두고, 음수 ceil/floor는 수직선에서 오른쪽/왼쪽인지 아래 전용 예제로 확인하세요.'
    )
    _lesson('random')['paragraphs'].append(
        '결과가 달라도 범위·개수·원본 유지가 맞으면 올바른 프로그램입니다. '
        '시드를 고정한 예제로 재현을 보고, sample과 shuffle을 나란히 실행해 원본이 바뀌는지 확인하세요.'
    )
    _lesson('datetime')['paragraphs'].append(
        '요일은 weekday() 번호에 한글을 대응합니다. 고정 날짜 예제로 월=0, 일=6을 확인하고, '
        '크리스마스까지는 date끼리 뺀 뒤 .days를 읽으세요. datetime.now()에서 .days만 보면 24시간 미만이 버려집니다.'
    )
    _lesson('thirdparty')['paragraphs'].append(
        '설치 이름과 import 이름을 표로 먼저 보세요. JSON처럼 표준 라이브러리로 되는 일은 pip 없이 해결합니다. '
        'NumPy 평균은 PC에서 가상환경을 켠 뒤 실행하세요. 웹에는 numpy가 없을 수 있습니다.'
    )
    _lesson('project')['paragraphs'].append(
        '주사위 한 함수부터 검사하세요. 통과하면 같은 core.logic에 날짜·추첨을 추가합니다. '
        '화면은 다음 단원에서 붙입니다. 빈 값·0면·잘못된 날짜는 함수가 ValueError를 내게 두는 편이 검사하기 쉽습니다.'
    )
    _lesson('review')['paragraphs'].append(
        '힌트 없이 두 파일을 만들고 import해 보세요. 그다음 final-output에서 임포트 때 출력되는 줄을 추적합니다. '
        '39쪽을 실행하면 합 4, 합 8, 차 5 순서입니다. 정답편의 마지막 9는 코드와 맞지 않습니다.'
    )

    _set_examples('overview', ['copy-twice', 'reuse', 'two-adds'])
    _set_examples('define', ['sum-input', 'circle-top', 'circle-function', 'circle-mixed', 'class-module'])
    _set_examples('entrypoint', ['main-guard', 'rectangle'])
    _set_examples('imports', [
        'import-0', 'import-1', 'import-2', 'import-3', 'import-4', 'import-clash',
    ])
    _set_examples('packages', [f'package-{i}' for i in range(5)] + ['all', 'animal-check', 'stars'])
    _set_examples('os-sys', ['os', 'os-pc', 'sys', 'sys-modules'])
    _set_examples('math', ['math', 'math-circle', 'math-signed'])
    _set_examples('random', ['random', 'random-seed', 'random-sample', 'dice', 'gift'])
    _set_examples('datetime', ['datetime', 'weekday-fixed', 'christmas'])
    _set_examples('thirdparty', ['pypi-names', 'stdlib-json', 'thirdparty'])
    _set_examples('project', ['project-roll', 'core'])
    _set_examples('review', ['review-two-files', 'final-output'])
