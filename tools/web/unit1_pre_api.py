"""Unit I pre_api/glossary fill for #59. Applied after unit1_density.

Adds or completes code-before cards for examples that introduce a new
import form, dunder, or stdlib function. Does not seed history/youtube.
"""
from content import examples, units
from slots import api_items, glossary_items


def _ex(eid):
    return examples[eid]


def _lesson(lid):
    return next(lesson for lesson in units[1] if lesson['id'] == lid)


def _fill_api(eid, items):
    rec = _ex(eid)
    if not rec['pre_api']:
        rec['pre_api'] = api_items(items)


def _extend_api(eid, items):
    rec = _ex(eid)
    seen = {item['name'] for item in rec['pre_api']}
    for item in api_items(items):
        if item['name'] not in seen:
            rec['pre_api'].append(item)
            seen.add(item['name'])


def _fill_glossary(eid, items):
    rec = _ex(eid)
    if not rec['glossary']:
        rec['glossary'] = glossary_items(items)


def _fill_lesson(lid, *, pre_api=None, glossary=None):
    rec = _lesson(lid)
    if pre_api and not rec['pre_api']:
        rec['pre_api'] = api_items(pre_api)
    if glossary and not rec['glossary']:
        rec['glossary'] = glossary_items(glossary)


def apply():
    """Fill Unit I pre_api/glossary after the #59 density examples exist."""
    _fill_lessons()
    _fill_missing_example_api()
    _complete_example_glossary()


def _fill_lessons():
    _fill_lesson('overview', pre_api=[
        {'name': '모듈과 패키지', 'signature': 'calculator.py  ·  nature/animals/',
         'note': '모듈은 기능을 담은 파일, 패키지는 그 파일들을 묶은 폴더입니다. 아래는 복사본과 한 모듈 재사용을 나란히 봅니다.'},
    ], glossary=[
        {'term': '라이브러리', 'meaning': '재사용 가능한 코드 묶음을 가리키는 넓은 말입니다. 모든 라이브러리가 여러 패키지로 나뉘지는 않습니다.'},
        {'term': '네임스페이스', 'meaning': '이름이 속한 공간입니다. calculator.add와 counter.add는 함수 이름이 같아도 구별됩니다.'},
    ])
    _fill_lesson('define', pre_api=[
        {'name': '정의와 호출', 'signature': 'def circlearea(r): …    /    circlearea(3)',
         'note': 'def는 이름만 준비합니다. 본문은 호출할 때 실행됩니다. 최상위 print는 import 순간에 실행됩니다.'},
    ], glossary=[
        {'term': '최상위 실행문', 'meaning': 'if나 def 밖에 있는 줄입니다. 모듈을 처음 불러올 때 바로 실행됩니다.'},
    ])
    _fill_lesson('entrypoint', pre_api=[
        {'name': '__name__', 'signature': 'if __name__ == "__main__":',
         'note': '직접 실행하면 값이 "__main__"이고, 임포트하면 모듈 이름입니다. 시험 호출을 이 아래에 둡니다.'},
    ], glossary=[
        {'term': '__main__', 'meaning': '파일 이름이 아닙니다. “지금 직접 실행 중인 모듈”이라는 표시입니다.'},
    ])
    _fill_lesson('imports', pre_api=[
        {'name': '연결된 이름', 'signature': 'import greet  →  greet.hello()\nfrom greet import hello  →  hello()',
         'note': 'import는 모듈을 로드하고, 어떤 이름을 현재 코드에 붙일지만 다릅니다. from도 모듈 전체를 실행합니다.'},
    ], glossary=[
        {'term': '별표 임포트', 'meaning': 'from greet import *는 출처가 흐려집니다. 같은 이름이 덮일 수 있어 앱 코드에서는 명시적 임포트를 우선합니다.'},
    ])
    _fill_lesson('packages', pre_api=[
        {'name': '점 경로', 'signature': 'nature.animals.bird  ↔  nature/animals/bird.py',
         'note': '점(.)은 폴더 구분입니다. from 패키지 import *의 대상과 from 모듈 import *의 대상은 다릅니다.'},
    ], glossary=[
        {'term': '__all__', 'meaning': 'from 패키지 import *로 가져올 이름을 적습니다. 없는 이름을 막는 보안 장치가 아닙니다.'},
        {'term': '__init__.py', 'meaning': '일반 패키지임을 표시하는 파일입니다. 패키지를 불러올 때 실행됩니다.'},
    ])
    _fill_lesson('os-sys', pre_api=[
        {'name': 'os / sys', 'signature': 'os.getcwd()  ·  sys.argv  ·  sys.exit()',
         'note': 'os는 운영체제와 폴더, sys는 인터프리터와 실행 인자입니다. 웹의 폴더는 브라우저 메모리의 가상 파일입니다.'},
    ], glossary=[
        {'term': '작업 폴더', 'meaning': '파일을 찾는 기준 위치입니다. 소스 파일이 있는 폴더와 항상 같지는 않습니다.'},
    ])
    _fill_lesson('math', pre_api=[
        {'name': '상수와 함수', 'signature': 'math.pi  ·  math.ceil(x)',
         'note': '상수에는 괄호가 없습니다. 계산 함수에는 괄호가 있습니다. 어떤 계산이 필요한지 먼저 고르세요.'},
    ], glossary=[
        {'term': '음수 올림', 'meaning': 'ceil은 “이상인 최소 정수”입니다. -3.5의 올림은 -3입니다.'},
    ])
    _fill_lesson('random', pre_api=[
        {'name': '범위와 개수', 'signature': 'randrange  ·  choice  ·  sample  ·  shuffle',
         'note': '끝은 보통 포함되지 않습니다(randrange). shuffle은 None을 반환하고 원본을 바꿉니다.'},
    ], glossary=[
        {'term': '가짜 난수', 'meaning': '컴퓨터가 규칙으로 만든 수입니다. 같은 시드면 같은 수열이 나와 검사에 쓸 수 있습니다.'},
    ])
    _fill_lesson('datetime', pre_api=[
        {'name': '날짜 객체', 'signature': 'date.today()  ·  datetime.now()  ·  weekday()',
         'note': '날짜끼리 빼면 timedelta가 됩니다. 달력 일수가 목적이면 date를 쓰고 .days를 읽습니다.'},
    ], glossary=[
        {'term': '모듈과 클래스', 'meaning': 'from datetime import datetime처럼 모듈 이름과 클래스 이름이 같습니다. now는 클래스의 메서드입니다.'},
    ])
    _fill_lesson('thirdparty', pre_api=[
        {'name': 'pip와 import', 'signature': 'pip install beautifulsoup4  →  import bs4',
         'note': '설치 이름과 코드의 import 이름이 다를 수 있습니다. pip는 터미널에서, import는 코드에서 실행합니다.'},
    ], glossary=[
        {'term': '가상환경', 'meaning': '프로젝트마다 패키지를 따로 담는 폴더입니다. python -m venv .venv 후 활성화하고 설치합니다.'},
    ])
    _fill_lesson('project', pre_api=[
        {'name': '기능 패키지', 'signature': 'from core.logic import roll, days_left, draw',
         'note': '화면 없이 반환값만 검사합니다. 같은 함수를 다음 단원에서 tkinter·PySide6에 연결합니다.'},
    ], glossary=[
        {'term': '반환과 출력', 'meaning': '함수는 값을 return하고, print는 main에서 합니다. GUI는 이 반환값을 Label에 보여 줍니다.'},
    ])
    _fill_lesson('review', pre_api=[
        {'name': '한 줄로 복습', 'signature': '파일에 정의 → import → 이름에 맞춰 호출',
         'note': '임포트 때 실행되는 줄과 호출해야 실행되는 줄을 구별하면 종합 평가의 출력 추적이 됩니다.'},
    ], glossary=[
        {'term': '39쪽 순서', 'meaning': 'addcal을 불러오면 합 4가 먼저 나오고, 이어서 합 8, 가드가 있는 subcal은 차 5만 이어집니다.'},
    ])


def _fill_missing_example_api():
    _fill_api('reuse', [
        {'name': 'import 모듈', 'signature': 'import calculator\nprint(calculator.add(3, 5))',
         'note': '파일 calculator.py를 불러 모듈 이름 calculator를 만듭니다. 함수는 모듈 이름으로 호출합니다.'},
    ])
    _fill_api('sum-input', [
        {'name': 'from … import', 'signature': 'from sumnummod import sumnum',
         'note': '모듈에서 함수 이름만 현재 공간에 연결합니다. sumnum()으로 호출합니다.'},
        {'name': 'input / int', 'signature': 'n1 = int(input("첫 번째 수: "))',
         'note': '한 줄을 문자열로 받은 뒤 정수로 바꿉니다. 웹 실습의 표준 입력칸에 두 줄을 넣습니다.'},
    ])
    _fill_api('circle-top', [
        {'name': '최상위 실행', 'signature': 'import circle',
         'note': 'circle.py에 실행문만 있으면 불러오는 순간 둘레와 넓이가 출력됩니다. 함수를 호출할 필요가 없습니다.'},
    ])
    _fill_api('circle-function', [
        {'name': '함수 정의', 'signature': 'def circlearea(r):',
         'note': '임포트할 때는 이름만 준비됩니다. 넓이를 보려면 circle_area.circlearea(3)처럼 호출해야 합니다.'},
    ])
    _fill_api('circle-mixed', [
        {'name': '정의와 호출이 한 파일', 'signature': 'def circlearea(r): …\ncirclearea(4)',
         'note': '임포트하면 반지름 4가 먼저 출력되고, main이 3으로 다시 호출하므로 결과가 두 줄입니다.'},
    ])
    _fill_api('class-module', [
        {'name': 'class', 'signature': 'class Circle:\n    def area(self):',
         'note': '클래스도 모듈에 두고 가져올 수 있습니다. Circle(3)이 인스턴스를 만들고 area()가 값을 반환합니다.'},
        {'name': 'from … import 클래스', 'signature': 'from shapes import Circle',
         'note': '모듈 접두어 없이 Circle을 씁니다. 반환값은 다른 계산에도 재사용할 수 있습니다.'},
    ])
    _fill_api('main-guard', [
        {'name': '__name__', 'signature': 'print(__name__)\nif __name__ == "__main__":',
         'note': '직접 실행 파일은 "__main__", 임포트된 파일은 모듈 이름입니다. if 안의 호출은 직접 실행할 때만 돕니다.'},
    ])
    _fill_api('rectangle', [
        {'name': '탐구용 가드', 'signature': 'if __name__ == "__main__":\n    rect(3, 5)',
         'note': '조건을 지우면 import만 해도 가로 3 세로 5가 출력됩니다. 가드가 있으면 main의 rect(2, 4)만 보입니다.'},
    ])
    _fill_api('import-0', [
        {'name': 'import 모듈', 'signature': 'import greet\ngreet.hello()',
         'note': '모듈 전체 이름 greet가 생깁니다. 함수는 greet.hello()로 호출합니다.'},
    ])
    _fill_api('import-1', [
        {'name': 'from 모듈 import 함수', 'signature': 'from greet import hello\nhello()',
         'note': 'hello만 현재 공간에 연결합니다. greet.hello()는 NameError입니다. 모듈은 이미 로드된 상태입니다.'},
    ])
    _fill_api('import-2', [
        {'name': '여러 이름', 'signature': 'from greet import hello, bye',
         'note': '쉼표로 필요한 함수만 가져옵니다. 별표보다 출처가 분명합니다.'},
    ])
    _fill_api('import-3', [
        {'name': 'from 모듈 import *', 'signature': 'from greet import *\nhello()',
         'note': '__all__이 없으면 밑줄로 시작하지 않는 이름을 가져옵니다. 출처가 흐려지므로 직접 작성하는 앱에서는 피하세요.'},
    ])
    _fill_api('import-4', [
        {'name': 'import … as', 'signature': 'import greet as g\ng.bye()',
         'note': '현재 코드에서만 별칭 g를 씁니다. 파일명이 바뀌지는 않습니다. 이 상태에서는 greet라는 이름이 없습니다.'},
    ])
    _fill_api('package-0', [
        {'name': '하위 모듈 가져오기', 'signature': 'from nature.animals import bird\nbird.wild()',
         'note': '패키지에서 모듈 bird를 가져옵니다. 함수는 bird.wild()입니다.'},
    ])
    _fill_api('package-1', [
        {'name': '모듈 별칭', 'signature': 'from nature.animals import bird as b\nb.wild()',
         'note': '긴 경로 대신 b를 씁니다. 원래 폴더 이름은 그대로입니다.'},
    ])
    _fill_api('package-2', [
        {'name': '패키지 속 함수', 'signature': 'from nature.animals.bird import wild\nwild()',
         'note': '모듈이 아니라 함수를 현재 공간에 연결합니다. bird.wild()는 이 문만으로는 쓸 수 없습니다.'},
    ])
    _fill_api('package-3', [
        {'name': '모듈의 별표', 'signature': 'from nature.animals.bird import *\nwild()',
         'note': '대상은 bird 모듈입니다. from nature.animals import *와 가져오는 이름이 다릅니다.'},
    ])
    _fill_api('package-4', [
        {'name': '전체 경로', 'signature': 'import nature.animals.bird\nnature.animals.bird.wild()',
         'note': '점 경로 그대로 호출합니다. 이름이 길지만 출처가 가장 분명합니다.'},
    ])
    _fill_api('all', [
        {'name': '__all__', 'signature': '__all__ = ["tree"]\nfrom nature.plants import *',
         'note': '별표로 가져올 이름만 적습니다. flower는 목록에 없어 *로는 안 되고, from … import flower는 됩니다.'},
    ])
    _fill_api('animal-check', [
        {'name': '35쪽 동물 패키지', 'signature': 'from nature.animals import *\nbird.wild()',
         'note': 'animals의 __all__이 bird와 lion입니다. 같은 패키지를 두 진입점(main.py / mainanimal2.py)으로 불러 보세요.'},
    ])
    _fill_api('stars', [
        {'name': '25쪽 탐구', 'signature': 'from star import makestar\nimport star as s',
         'note': '특정 함수 가져오기와 모듈 별칭을 한 예제에서 비교합니다. 함수 별칭은 from star import makestar as s입니다.'},
    ])
    _fill_api('os', [
        {'name': 'os.getcwd / makedirs', 'signature': 'os.getcwd()\nos.makedirs("practice", exist_ok=True)',
         'note': '현재 폴더를 읽고, 실습 폴더를 만듭니다. exist_ok=True면 이미 있어도 오류가 아닙니다.'},
        {'name': 'os.listdir', 'signature': 'os.listdir("practice")',
         'note': '폴더 안 이름 목록입니다. 웹에서는 브라우저 메모리의 가상 파일만 보입니다.'},
    ])
    _fill_api('os-pc', [
        {'name': 'os.name / os.system', 'signature': 'os.name  ·  os.system("ls")',
         'note': 'os.name이 nt면 Windows입니다. 교과서 dir는 Windows 명령이라 이 예제는 다른 환경에서 ls를 고릅니다.'},
    ])
    _fill_api('sys', [
        {'name': 'sys.argv', 'signature': 'sys.argv[0]  ·  sys.argv[1:]',
         'note': '0번은 실행 파일명, 그 뒤는 문자열 인자입니다. 웹에서는 JSON 배열로 전달합니다.'},
        {'name': 'sys.exit', 'signature': 'sys.exit()',
         'note': 'SystemExit를 일으켜 실행을 끝냅니다. 이 줄 아래 print는 실행되지 않습니다.'},
    ])
    _fill_api('math', [
        {'name': 'math.pi / math.e', 'signature': 'math.pi  ·  math.e',
         'note': '상수입니다. 괄호를 붙이지 않습니다.'},
        {'name': 'ceil / floor / factorial / gcd', 'signature': 'math.ceil(3.5)  ·  math.factorial(5)',
         'note': '올림·내림·팩토리얼·최대 공약수입니다. 0!은 1입니다. 음수 ceil/floor는 옆 예제에서 따로 봅니다.'},
    ])
    _fill_api('random', [
        {'name': 'random / randrange / choice', 'signature': 'random.random()\nrandom.randrange(1, 7)',
         'note': 'random()은 0 이상 1 미만입니다. randrange의 끝은 제외입니다. 주사위 1~6은 randrange(1, 7)입니다.'},
        {'name': 'shuffle 반환값', 'signature': 'result = random.shuffle(letters)',
         'note': '원본 리스트를 섞고 None을 반환합니다. result를 추첨 결과로 쓰면 안 됩니다.'},
    ])
    _fill_api('dice', [
        {'name': 'n면 주사위', 'signature': 'random.randrange(1, n + 1)',
         'note': '1부터 n까지 포함하려면 끝을 n+1로 둡니다. n이 1보다 작으면 안내만 하고 뽑지 않습니다.'},
    ])
    _fill_api('gift', [
        {'name': 'random.choice', 'signature': 'random.choice(presents)',
         'note': '리스트에서 항목 하나를 고릅니다. 비어 있는 리스트는 IndexError입니다.'},
    ])
    _fill_api('datetime', [
        {'name': 'datetime.now', 'signature': 'now = datetime.now()\nnow.year  ·  now.weekday()',
         'note': '현재 날짜와 시각입니다. year는 속성(괄호 없음), weekday()는 메서드(월요일 0)입니다.'},
    ])
    _fill_api('christmas', [
        {'name': 'date / timedelta.days', 'signature': 'date(today.year, 12, 25)\n(target - today).days',
         'note': '날짜끼리 빼면 일수를 .days로 읽습니다. 이미 지났으면 다음 해 12월 25일을 고릅니다.'},
    ])
    _fill_api('thirdparty', [
        {'name': 'numpy.array', 'signature': 'import numpy as np\nnp.array([70, 80, 90]).mean()',
         'note': '설치 이름과 import 이름은 둘 다 numpy입니다. 가상환경에서 pip install numpy 후 PC에서 실행합니다.'},
    ])
    _fill_api('final-output', [
        {'name': '임포트 때 출력', 'signature': 'import addcal  →  합 4\nimport subcal  →  (가드, 출력 없음)',
         'note': 'addcal은 최상위에서 바로 출력하고, subcal은 가드 안에 있습니다. 이어서 main이 합 8, 차 5를 출력합니다.'},
    ])
    # core may already have cards from unit2_pre_api; keep them if present.
    _fill_api('core', [
        {'name': 'roll', 'signature': 'roll(sides)',
         'note': '1부터 sides까지 정수 하나를 뽑습니다. 면 수가 1보다 작으면 ValueError입니다.'},
        {'name': 'days_left', 'signature': 'days_left("2026-12-25", today)',
         'note': '목표 날짜까지 남은 일수를 정수로 반환합니다. 오늘을 빼면 검사하기 쉽습니다.'},
        {'name': 'draw', 'signature': 'draw(["민지", "수빈"], 2)',
         'note': '공백·중복을 정리한 뒤 count명을 뽑습니다. 인원이 부족하면 ValueError입니다.'},
    ])


def _complete_example_glossary():
    _fill_glossary('reuse', [
        {'term': '재사용', 'meaning': '한 파일에 함수를 두고 여러 프로그램이 import합니다. 고칠 곳은 한 곳입니다.'},
    ])
    _fill_glossary('circle-mixed', [
        {'term': '두 번 출력', 'meaning': '모듈 최상위 호출 + main의 호출입니다. import가 함수를 두 번 정의해서가 아닙니다.'},
    ])
    _fill_glossary('import-3', [
        {'term': '__all__', 'meaning': '모듈에도 둘 수 있습니다. 없으면 밑줄로 시작하지 않는 이름이 별표 대상입니다.'},
    ])
    _fill_glossary('os-pc', [
        {'term': 'PC 전용', 'meaning': 'os.system은 웹(Pyodide)에서 기대한 셸이 아닙니다. 문법만 보고 실제 dir/ls는 PC에서 실행하세요.'},
    ])
    _fill_glossary('thirdparty', [
        {'term': 'requirements.txt', 'meaning': '설치할 패키지 목록입니다. python -m pip install -r requirements.txt로 한 번에 맞춥니다.'},
    ])
    _fill_glossary('final-output', [
        {'term': '정답편 201쪽', 'meaning': '마지막 값을 9로 적은 곳은 코드와 맞지 않습니다. 실행하면 차 5가 마지막입니다.'},
    ])
    _fill_glossary('core', [
        {'term': '반환과 출력', 'meaning': '함수는 값을 return하고, print는 main에서 합니다. GUI는 이 반환값을 Label에 보여 줍니다.'},
    ])


def unit1_pre_coverage():
    """Examples that must show a code-before card."""
    ids = []
    for lesson in units[1]:
        for eid in lesson['examples']:
            if eid not in ids:
                ids.append(eid)
    return ids
