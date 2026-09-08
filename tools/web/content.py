"""Authored web lessons. Run build.py after editing. Textbook pages refer to printed pages."""
import textwrap
units = {1: [], 2: []}
examples = {}
questions = []
def code(s): return textwrap.dedent(s).strip()+'\n'
def ex(id, title, files, mode='web', entry='main.py', stdin='', args='', checks='', note=''):
    examples[id] = dict(id=id,title=title,files={k:code(v) for k,v in files.items()},mode=mode,entry=entry,stdin=stdin,args=args,checks=code(checks) if checks else '',note=note)
    return id
def lesson(unit,id,title,pages,lead,paragraphs,examples_=(),tasks=(),extra=False):
    units[unit].append(dict(id=id,title=title,pages=pages,lead=lead,paragraphs=paragraphs,examples=list(examples_),tasks=list(tasks),extra=extra))
def q(unit,topic,kind,prompt,answer,hint,explain,options=None,starter='',checks='',level='기본',ref='보강'):
    questions.append(dict(id=f'u{unit}-q{sum(x["unit"]==unit for x in questions)+1:03}',unit=unit,topic=topic,kind=kind,prompt=prompt,answer=answer,hint=hint,explain=explain,options=options,starter=code(starter) if starter else '',checks=code(checks) if checks else '',level=level,ref=ref))

ex('reuse','한 번 만든 함수를 두 프로그램에서 사용하기',{'main.py':'''import calculator
print(calculator.add(3, 5))
print(calculator.add(10, -2))''','calculator.py':'''def add(a, b):
    return a + b'''},checks='assert calculator.add(0, 4) == 4\nassert calculator.add(-2, 5) == 3')
lesson(1,'overview','모듈과 패키지가 필요한 이유','8–13','복사해 둔 함수가 열 군데 있다면, 오류 하나를 어디에서 고쳐야 할까요?',[
'모듈은 함수·클래스·변수·실행문 등을 담은 파이썬 파일입니다. calculator.py의 모듈 이름은 calculator입니다. import는 다른 모듈의 이름을 현재 코드에서 사용할 수 있도록 연결합니다. 함수를 복사하는 대신 모듈을 불러오면 공통 기능을 한 곳에서 관리할 수 있습니다.',
'모듈의 이점은 코드 중복 감소, 재사용, 기능별 구조화, 네임스페이스 분리입니다. 서로 다른 모듈에 add라는 함수가 있어도 calculator.add와 another.add로 구별합니다. 너무 잘게 나누면 파일 사이 의존성을 따라가기 어려우므로 기능을 기준으로 묶습니다.',
'패키지는 관련 모듈을 폴더 계층으로 묶습니다. nature/animals/bird.py처럼 주제별로 분류하면 새 기능을 넣을 위치를 찾기 쉽습니다. 라이브러리는 재사용 가능한 코드 묶음을 가리키는 넓은 표현입니다. 모든 라이브러리가 반드시 여러 패키지로 구성되는 것은 아닙니다.',
'생각 열기: 이미지 편집·게임·웹 서비스에 쓰이는 파이썬 패키지를 하나 조사하세요. 어떤 기능을 직접 구현하지 않아도 되는지 설명하세요.'],['reuse'],['모듈과 패키지를 파일과 폴더에 대응하여 설명하세요.','한 파일과 여러 모듈 방식의 장단점을 각각 적으세요.','13쪽 확인학습: 두 수를 입력받아 합을 반환하는 모듈을 만드세요.'])
ex('sum-input','확인학습 · 두 수의 합',{'main.py':'''from sumnummod import sumnum
print("두 수의 합 :", sumnum())''','sumnummod.py':'''def sumnum():
    n1 = int(input("첫 번째 수: "))
    n2 = int(input("두 번째 수: "))
    return n1 + n2

if __name__ == "__main__":
    print(sumnum())'''},stdin='3\n5')
ex('circle-top','실행문만 있는 모듈',{'main.py':'import circle','circle.py':'''PI = 3.14
r = 3
print("반지름이 {}인 원의 둘레: {}".format(r, r * 2 * PI))
print("반지름이 {}인 원의 넓이: {}".format(r, r * r * PI))'''})
ex('circle-function','함수 정의와 호출 분리',{'main.py':'''import circle_area
circle_area.circlearea(3)''','circle_area.py':'''PI = 3.14

def circlearea(r):
    print("반지름이 {}인 원의 넓이: {}".format(r, r * r * PI))'''})
ex('circle-mixed','함수와 실행문이 함께 있을 때',{'main.py':'''import circle_area2
circle_area2.circlearea(3)''','circle_area2.py':'''PI = 3.14

def circlearea(r):
    print("반지름이 {}인 원의 넓이: {}".format(r, r*r*PI))

circlearea(4)'''})
ex('class-module','보강 · 클래스를 담은 모듈',{'main.py':'''from shapes import Circle
print(Circle(3).area())''','shapes.py':'''import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2'''})
lesson(1,'define','실행문·함수·클래스로 모듈 정의하기','15–16','import 한 줄인데 왜 두 번 출력될까요?',[
'파일을 저장하면 모듈을 만들 수 있습니다. 실행문만 있는 circle은 처음 불러올 때 계산과 출력이 이루어집니다. 함수 정의만 있는 circle_area는 함수를 호출해야 함수 본문이 실행됩니다.',
'함수 정의와 호출이 섞인 circle_area2를 임포트하면 반지름 4의 결과가 먼저 출력됩니다. 이어서 main.py가 반지름 3으로 호출하므로 두 결과가 나옵니다. 함수 정의 자체와 함수 호출의 실행 시점을 구별하세요.',
'클래스도 모듈에 정의하여 불러올 수 있습니다. 추가 예제에서는 Circle 인스턴스에 반지름을 저장하고 area 메서드가 넓이를 반환합니다. 반환한 값은 다른 계산에도 재사용할 수 있습니다.'],['sum-input','circle-top','circle-function','circle-mixed','class-module'],['실행 전에 출력되는 줄 수와 순서를 예상하세요.','원의 반지름을 바꾸고 계산 결과를 확인하세요.'])
ex('main-guard','직접 실행과 임포트 비교',{'main.py':'''import circle_area3
print("main.py의 이름:", __name__)
circle_area3.circlearea(3)''','circle_area3.py':'''PI = 3.14
print("circle_area3의 이름:", __name__)

def circlearea(r):
    print("반지름이 {}인 원의 넓이: {}".format(r, r*r*PI))

if __name__ == "__main__":
    circlearea(4)'''})
ex('rectangle','탐구 활동 · 사각형 모듈',{'main.py':'''import rectEx1
rectEx1.rect(2, 4)''','rectEx1.py':'''def rect(width, height):
    print("가로가 {} 세로가 {}인 사각형의 넓이: {}".format(width, height, width*height))

if __name__ == "__main__":
    rect(3, 5)'''})
lesson(1,'entrypoint','__name__과 __main__','17–18','실행 파일 선택을 바꾸어 같은 모듈의 두 역할을 관찰하세요.',[
'직접 실행하는 파일의 __name__은 "__main__"입니다. 다른 파일에서 임포트하면 모듈 이름이 됩니다. if __name__ == "__main__": 아래에 시험용 호출을 넣으면 임포트할 때 시험 출력이 섞이지 않습니다.',
'웹 실행창에서 main.py와 circle_area3.py를 번갈아 실행하세요. 모듈 최상위의 print는 임포트 때도 실행되지만 if 안의 호출은 직접 실행할 때만 실행됩니다.',
'보강: 같은 인터프리터에서 이미 로드한 모듈을 다시 import하면 보통 sys.modules의 캐시를 재사용합니다. 아래 실습창은 실행마다 학습 파일을 새 폴더에 준비하고 이전 학습 모듈을 정리합니다.'],['main-guard','rectangle'],['rectEx1의 조건문을 제거했을 때와 있을 때의 출력을 비교하세요.','__main__이 파일 이름이라는 설명이 왜 틀렸는지 적으세요.'])
greet={'greet.py':'''def hello():
    print("안녕하세요")

def bye():
    print("안녕히 가세요")'''}
imports=[('import greet\ngreet.hello()\ngreet.bye()','모듈 전체'),('from greet import hello\nhello()','특정 함수'),('from greet import hello, bye\nhello()\nbye()','여러 함수'),('from greet import *\nhello()\nbye()','별표'),('import greet as g\ng.bye()','별칭')]
for i,(src,title) in enumerate(imports): ex(f'import-{i}',title,{'main.py':src,**greet})
lesson(1,'imports','임포트 문과 호출법 연결하기','19–21','불러온 이름이 무엇인지 알면 호출법도 결정됩니다.',[
'import greet는 greet라는 이름을 만듭니다. 따라서 greet.hello()로 호출합니다. from greet import hello는 hello를 현재 공간에 연결하므로 hello()로 호출합니다. from 문도 모듈을 로드하며 필요한 함수 부분만 따로 실행하는 것은 아닙니다.',
'import greet as g는 현재 코드에서 g라는 별칭을 사용합니다. 원래 파일명이 바뀌는 것은 아닙니다. 이 코드만 실행한 상태에서는 greet라는 이름을 연결하지 않았으므로 greet.bye()는 NameError입니다.',
'from greet import *는 공개 이름들을 가져옵니다. __all__이 없으면 밑줄로 시작하지 않는 이름이 대상입니다. 이름의 출처가 흐려지고 같은 이름이 덮어써질 수 있으므로 직접 작성하는 앱에서는 명시적 임포트를 우선하세요.'],[f'import-{i}' for i in range(5)],['같은 hello 함수를 네 가지 방식으로 호출하세요.','두 모듈에 같은 함수가 있을 때 이름을 구별해 호출하세요.'])
nature={'nature/__init__.py':'# 자연 패키지','nature/animals/__init__.py':'__all__ = ["bird", "lion"]','nature/plants/__init__.py':'__all__ = ["tree"]'}
for group,names in [('animals',{'bird':'새는 동물입니다.','lion':'사자는 동물입니다.'}),('plants',{'tree':'나무는 식물입니다.','flower':'꽃은 식물입니다.','grass':'풀은 식물입니다.'})]:
 for name,msg in names.items(): nature[f'nature/{group}/{name}.py']=f'def wild():\n    print("{msg}")'
pkgcodes=['from nature.animals import bird\nbird.wild()','from nature.animals import bird as b\nb.wild()','from nature.animals.bird import wild\nwild()','from nature.animals.bird import *\nwild()','import nature.animals.bird\nnature.animals.bird.wild()']
for i,src in enumerate(pkgcodes): ex(f'package-{i}',f'패키지 임포트 {i+1}',{'main.py':src,**nature})
ex('all','__all__의 영향 실험',{'main.py':'''from nature.plants import *
tree.wild()
# flower.wild()  # 주석을 해제하고 실행하세요.
# from nature.plants import flower  # 명시적 임포트는 가능합니다.''',**nature})
ex('animal-check','35쪽 확인학습 · 동물 패키지',{'main.py':'from nature.animals import *\nbird.wild()\nlion.wild()','mainanimal2.py':'from nature.animals.lion import wild\nwild()',**nature})
ex('stars','25쪽 탐구 · 별 출력',{'main.py':'from star import makestar\nmakestar(4, 3)\nimport star as s\ns.makestar(2, 2)','star.py':'''def makestar(c, r):
    for i in range(r):
        print("*" * c)

if __name__ == "__main__":
    makestar(4, 3)'''})
lesson(1,'packages','패키지 구조와 __all__','21–25, 35','폴더 트리의 점(.)은 어떤 경로를 가리킬까요?',[
'패키지 경로는 점으로 구분합니다. nature.animals.bird는 nature/animals/bird.py에 대응합니다. 일반 패키지에는 __init__.py를 둡니다. Python에는 이 파일 없이 구성하는 네임스페이스 패키지도 있지만 이번 실습은 일반 패키지로 통일합니다.',
'패키지의 모듈 가져오기, 별칭, 특정 함수 가져오기, 모듈의 별표 임포트, 전체 경로 임포트의 다섯 방식을 비교하세요. from nature.animals.bird import *와 from nature.animals import *는 대상이 다릅니다.',
'__init__.py의 __all__은 from 패키지 import *로 가져올 이름을 지정합니다. 외부 접근을 차단하는 보안 설정이 아닙니다. __all__에 없는 flower도 명시적으로 임포트할 수 있습니다.',
'교과서 보완: 25쪽 탐구의 설명과 정답편은 특정 함수 임포트/모듈 임포트 표현이 일치하지 않습니다. 예제는 from star import makestar와 import star as s를 각각 보여주며, 함수 별칭은 from star import makestar as s로 따로 연습할 수 있습니다.'],[f'package-{i}' for i in range(5)]+['all','animal-check','stars'],['__all__에 flower를 추가하고 달라진 결과를 확인하세요.','animals 패키지에 새 모듈을 추가하고 불러오세요.'])
ex('os','os · 가상 작업 폴더',{'main.py':'''import os
print("운영체제:", os.name)
print("현재 폴더:", os.getcwd())
os.makedirs("practice", exist_ok=True)
with open("practice/note.txt", "w", encoding="utf-8") as f:
    f.write("모듈 실습")
print(os.listdir("practice"))'''},note='웹의 폴더는 브라우저 메모리 안의 가상 파일입니다. PC 파일을 직접 읽지 않습니다.')
ex('os-pc','교과서 os 예제 · PC 명령',{'main.py':'''import os
print("현재 운영체제 :", os.name)
print("현재 작업 디렉터리 :", os.getcwd())
os.system("dir" if os.name == "nt" else "ls")'''},mode='pc',note='교과서의 dir는 Windows 명령입니다. 이 예제는 macOS/Linux에서 ls를 선택하도록 보완했습니다.')
ex('sys','실행 인자와 종료',{'main.py':'''import sys
print("실행 파일명 :", sys.argv[0])
for i, value in enumerate(sys.argv[1:], start=1):
    print("인자", i, ":", value)
sys.exit()
print("이 줄은 실행되지 않습니다.")'''},args='["param1", "param2"]')
lesson(1,'os-sys','os와 sys로 실행 환경 살펴보기','26–28','파일을 찾는 위치와 프로그램에 전달되는 값을 확인하세요.',[
'os는 운영체제와 파일·폴더 관련 기능을 제공합니다. os.name, os.getcwd(), os.system()의 역할을 구별하세요. 웹 실습에서는 os.listdir()로 가상 폴더 목록을 확인합니다. 셸 명령은 PC에서 실행합니다.',
'sys는 파이썬 인터프리터와 관련된 기능을 제공합니다. sys.argv[0]은 실행 파일명이며 그 뒤는 문자열 인자입니다. sys.exit()는 SystemExit를 발생시켜 실행을 끝냅니다. 뒤의 출력문이 실행되지 않는지 확인하세요.',
'교과서의 PyCharm Run with Parameters 설명에 대응하여 VS Code 터미널에서는 python main.py param1 param2로 실행합니다. 웹에서는 실행 인자를 JSON 배열로 입력합니다. 공백이 포함된 값도 하나의 문자열로 전달할 수 있습니다.',
'보강: 모듈 탐색은 sys.modules 캐시, 내장 모듈 처리, sys.path 등의 경로를 사용합니다. 현재 작업 폴더와 실행 스크립트 폴더는 항상 같은 것은 아닙니다. ModuleNotFoundError가 나면 파일명·실행 위치·환경을 순서대로 확인하세요.'],['os','os-pc','sys'],['실행 인자를 0개·1개·2개로 바꿔 보세요.','sys.exit 앞뒤에 출력문을 넣고 순서를 설명하세요.'])
ex('math','math의 상수와 함수',{'main.py':'''import math
print("파이:", math.pi)
print("e:", math.e)
print("올림:", math.ceil(3.5))
print("내림:", math.floor(3.5))
print("팩토리얼:", math.factorial(5))
print("최대 공약수:", math.gcd(28, 70))
print("거듭제곱:", math.pow(2, 10))
print("음수의 올림·내림:", math.ceil(-3.5), math.floor(-3.5))'''})
lesson(1,'math','math · 계산을 함수로 표현하기','29','함수 이름을 외우기 전에 어떤 계산이 필요한지 판단하세요.',[
'pi와 e는 상수이므로 괄호를 붙이지 않습니다. ceil은 주어진 수 이상인 최소 정수, floor는 주어진 수 이하인 최대 정수입니다. 음수에서는 0에 가까운 쪽이 올림이 됩니다.',
'factorial(n)은 1부터 n까지의 곱이며 0!은 1입니다. gcd는 최대 공약수입니다. math.pow(2, 10)은 실수 1024.0을 반환합니다. 정수 거듭제곱이 필요하면 2 ** 10과 비교해 보세요.'],['math'],['3.5 대신 -3.5를 사용해 올림과 내림을 설명하세요.','math.pi를 활용하는 원 넓이 함수를 작성하세요.'])
ex('random','random · 범위·선택·섞기',{'main.py':'''import random
print(random.random())
print(random.uniform(2.5, 10.0))
print(random.randrange(10))
print(random.randrange(1, 7, 2))
season = ["봄", "여름", "가을", "겨울"]
print(random.choice(season))
letters = ["가", "나", "다", "라", "마"]
result = random.shuffle(letters)
print("원본:", letters, "반환값:", result)
print(random.sample(list(range(1, 10)), 3))'''})
ex('dice','종합 평가 · n면 주사위',{'main.py':'''import random
n = int(input("주사위 면 수: "))
if n < 1:
    print("면 수는 1 이상이어야 합니다.")
else:
    print("주사위 값:", random.randrange(1, n + 1))'''},stdin='6')
ex('gift','탐구 · 선물 하나 고르기',{'main.py':'import random\npresents = ["문구용품", "과자", "인형"]\nprint(random.choice(presents))'})
lesson(1,'random','random · 결과보다 조건 확인하기','30–31, 33, 37','매번 결과가 달라도 올바른 프로그램인지 판단할 수 있습니다.',[
'random()은 0 이상 1 미만의 실수입니다. randrange(stop)은 끝을 제외하며 randrange(start, stop, step)은 range와 같은 후보에서 선택합니다. 주사위 1~n은 randrange(1, n+1)로 구현합니다.',
'choice는 요소 하나, sample은 지정 개수의 항목을 비복원 추출합니다. 원본에 같은 값이 여러 번 있으면 sample 결과에도 같은 값이 나올 수 있습니다. 고유한 명단을 주어야 사람 중복을 막을 수 있습니다.',
'shuffle은 원본 리스트를 직접 섞고 None을 반환합니다. result = random.shuffle(names)의 result를 추첨 결과로 쓰면 안 됩니다. 원본을 보존하려면 복사하거나 sample을 사용하세요.',
'교과서 보완: uniform(a, b)의 끝 값 b는 부동소수점 반올림에 따라 포함될 수도 있습니다. 무조건 끝 미만이라고 단정하지 않습니다. 추가 실습에서는 시드를 고정해 재현하고, 범위·개수·구성원을 검사합니다.'],['random','dice','gift'],['중복 없는 명단에서 2명을 뽑고 원본이 유지되는지 확인하세요.','주사위 결과가 특정 숫자여야 한다는 검사가 부적절한 이유를 적으세요.'])
ex('datetime','날짜·시각·요일',{'main.py':'''from datetime import datetime
now = datetime.now()
print(now)
print(now.year, now.month, now.day)
print(now.hour, now.minute, now.second)
print("요일 번호:", now.weekday())
week = "월화수목금토일"[now.weekday()]
print(f"오늘은 {now.year}년 {now.month}월 {now.day}일 {week}요일입니다.")
start = datetime(now.year, 1, 1)
print("올해 지난 시간:", now - start)'''})
ex('christmas','다음 크리스마스까지',{'main.py':'''from datetime import date
today = date.today()
target = date(today.year, 12, 25)
if target < today:
    target = date(today.year + 1, 12, 25)
print("다음 크리스마스까지", (target - today).days, "일")'''})
lesson(1,'datetime','datetime · 날짜를 계산하는 프로그램','31–33, 38','날짜를 문자열로 빼지 않고 날짜 객체로 계산합니다.',[
'datetime.now()로 현재 날짜와 시각을 얻습니다. year, month, day, hour, minute, second는 속성입니다. weekday()는 메서드이며 월요일 0부터 일요일 6까지 반환합니다. datetime 모듈과 그 안의 datetime 클래스 이름이 같다는 점에 주의하세요.',
'날짜·시각끼리 빼면 timedelta가 됩니다. .days로 일수를 읽을 수 있습니다. 시각을 포함하면 24시간 미만 부분은 정수 일수에 포함되지 않으므로 달력 날짜 차이가 목적이면 date를 사용하세요.',
'교과서의 고정된 2025년 날짜는 당시 실행 예입니다. 오늘 날짜는 실행 환경에 따라 달라집니다. 다음 크리스마스 예제는 당일에는 0, 지난 후에는 다음 해를 선택하도록 보완했습니다.'],['datetime','christmas'],['2026-12-24, 2026-12-25, 2026-12-26을 기준으로 각각 시험하세요.','현재 날짜와 요일을 한글 문장으로 출력하세요.'])
ex('thirdparty','PC · NumPy 첫 실습',{'main.py':'import numpy as np\nscores = np.array([70, 80, 90])\nprint(scores.mean())','requirements.txt':'numpy'},mode='pc',note='가상환경에서 python -m pip install -r requirements.txt를 실행하세요.')
lesson(1,'thirdparty','PyPI와 서드파티 패키지','32–33','필요한 기능을 찾고, 설치 이름과 임포트 이름을 확인하세요.',[
'표준 라이브러리는 파이썬과 함께 제공되고, 서드파티 패키지는 별도로 설치합니다. PyPI는 파이썬 패키지를 찾는 저장소이며 pip는 설치 도구입니다. PC 터미널에서 python -m venv .venv로 환경을 만들고 활성화한 뒤 python -m pip install 패키지명을 실행하세요.',
'교과서의 8종: Beautiful Soup(HTML/XML 정보 추출, 설치 beautifulsoup4·임포트 bs4), Pillow(이미지 처리, pillow·PIL), Peewee(데이터베이스 ORM, peewee), Scrapy(크롤링, scrapy), Pygame(게임, pygame), NumPy(배열·수치 계산, numpy), Django와 Flask(웹 개발, django·flask). 모두를 설치할 필요는 없으며 목적을 설명하고 필요한 패키지를 선택합니다.',
'교과서의 pip install bs4 대신 실제 배포 패키지 이름인 beautifulsoup4를 사용합니다. pip 명령은 Python 코드 입력창이 아니라 터미널에서 실행합니다. 설치한 환경과 실행하는 VS Code 인터프리터가 같은지 확인하세요.',
'보강: python -m pip show 패키지명으로 정보를 확인하고 requirements.txt에 의존성을 기록합니다. 웹 실습 환경은 PC의 pip·GUI와 지원 범위가 다르므로 설치 실습은 PC에서 수행합니다.'],['thirdparty'],['이미지 크기 변경·게임·웹페이지에서 제목 추출에 맞는 패키지를 고르세요.','설치 이름과 import 이름이 다른 예를 두 개 적으세요.'])
ex('final-output','종합 평가 8 · 출력 추적',{'main.py':'import addcal\nimport subcal\nprint("두 수의 합 :", addcal.addnum(5, 3))\nprint("두 수의 차 :", subcal.subnum(7, 2))','addcal.py':'def addnum(a, b):\n    return a + b\nprint("두 수의 합 :", addnum(1, 3))','subcal.py':'def subnum(a, b):\n    return a - b\nif __name__ == "__main__":\n    print("두 수의 차 :", subnum(4, 1))'})
lesson(1,'review','단원 마무리와 종합 평가','13, 34–39','정답을 본 뒤에는 숫자와 조건을 바꾸어 다시 풀어 보세요.',[
'핵심 지도: 파일의 기능을 모듈로 분리 → import 방식에 맞춰 호출 → 폴더를 패키지로 구성 → 표준·서드파티 기능 선택 → 동작 검증입니다. 아래 연습실에서 교과서 연계 문항과 보강 문항을 유형별로 풀 수 있습니다.',
'종합 평가의 목표 8가지: 모듈 정의 판단, 필요성 판단, student.study 호출법, nature.plants.grass 호출법, sample 사용, n면 주사위 구현, 날짜·요일 출력, 임포트 시 출력 추적입니다. 35쪽 패키지 확인학습은 앞의 동물 패키지 실습과 연결됩니다.',
'정답편 대조 및 보완: 39쪽 코드를 실행하면 합 4, 합 8, 차 5 순서입니다. 정답편 201쪽의 마지막 9는 코드와 맞지 않습니다. 아래에서 직접 실행하여 확인하세요.'],['final-output'],['힌트 없이 두 파일을 만들고 import하여 호출하세요.','단원 연습에서 틀린 문제를 다시 풀고 오류 원인을 저널에 남기세요.'])
# Unit 2: desktop examples are downloadable, editable and syntax-checkable in the browser.
ex('hello-tk','인사 앱 · tkinter',{'main.py':'''import tkinter as tk

def greet():
    name = entry.get().strip() or "여러분"
    result.config(text=f"{name}님, 안녕하세요!")

def reset():
    entry.delete(0, tk.END)
    result.config(text="이름을 입력하세요.")

root = tk.Tk()
root.title("인사 실습 · tkinter")
root.geometry("480x260")
tk.Label(root, text="나의 첫 GUI", font=("sans-serif", 20)).pack(pady=16)
entry = tk.Entry(root)
entry.pack(fill="x", padx=30)
tk.Button(root, text="인사하기", command=greet).pack(pady=8)
tk.Button(root, text="초기화", command=reset).pack()
result = tk.Label(root, text="이름을 입력하세요.")
result.pack(pady=12)
root.mainloop()'''},mode='pc')
ex('hello-ttk','인사 앱 · tkinter + ttk',{'main.py':examples['hello-tk']['files']['main.py'].replace('import tkinter as tk','import tkinter as tk\nfrom tkinter import ttk').replace('tk.Label','ttk.Label').replace('tk.Entry','ttk.Entry').replace('tk.Button','ttk.Button').replace('인사 실습 · tkinter','인사 실습 · ttk')},mode='pc')
ex('hello-pyside','인사 앱 · PySide6',{'main.py':'''import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

def greet():
    name = entry.text().strip() or "여러분"
    result.setText(f"{name}님, 안녕하세요!")

def reset():
    entry.clear()
    result.setText("이름을 입력하세요.")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("인사 실습 · PySide6")
window.resize(480, 260)
layout = QVBoxLayout(window)
layout.addWidget(QLabel("나의 첫 GUI"))
entry = QLineEdit()
layout.addWidget(entry)
button = QPushButton("인사하기")
button.clicked.connect(greet)
layout.addWidget(button)
clear_button = QPushButton("초기화")
clear_button.clicked.connect(reset)
layout.addWidget(clear_button)
result = QLabel("이름을 입력하세요.")
layout.addWidget(result)
window.show()
sys.exit(app.exec())'''},mode='pc')
ex('hello-pyqt','인사 앱 · PyQt6',{'main.py':examples['hello-pyside']['files']['main.py'].replace('PySide6','PyQt6')},mode='pc')
ex('hello-wx','인사 앱 · wxPython',{'main.py':'''import wx
app = wx.App()
window = wx.Frame(None, title="인사 실습 · wxPython", size=(480, 300))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(wx.StaticText(panel, label="나의 첫 GUI"), 0, wx.ALL, 12)
entry = wx.TextCtrl(panel)
layout.Add(entry, 0, wx.EXPAND | wx.ALL, 12)
button = wx.Button(panel, label="인사하기")
layout.Add(button, 0, wx.ALL, 8)
clear_button = wx.Button(panel, label="초기화")
layout.Add(clear_button, 0, wx.ALL, 8)
result = wx.StaticText(panel, label="이름을 입력하세요.")
layout.Add(result, 0, wx.ALL, 12)
def greet(event):
    result.SetLabel(f"{entry.GetValue().strip() or '여러분'}님, 안녕하세요!")
def reset(event):
    entry.SetValue("")
    result.SetLabel("이름을 입력하세요.")
button.Bind(wx.EVT_BUTTON, greet)
clear_button.Bind(wx.EVT_BUTTON, reset)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''},mode='pc')
ex('hello-kivy','인사 앱 · Kivy',{'main.py':'''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pathlib import Path
# 한글 표시: 실행 폴더에 NotoSansKR.ttf를 넣거나 PC의 한글 글꼴 경로를 지정하세요.
font = "NotoSansKR.ttf"
if not Path(font).exists():
    font = "Roboto"
Window.size = (480, 300)
class GreetingApp(App):
    def build(self):
        self.title = "Greeting · Kivy"
        box = BoxLayout(orientation="vertical", padding=16, spacing=8)
        box.add_widget(Label(text="My first GUI", font_name=font))
        self.entry = TextInput(multiline=False, font_name=font)
        box.add_widget(self.entry)
        button = Button(text="Greet", font_name=font)
        button.bind(on_press=self.greet)
        box.add_widget(button)
        reset = Button(text="Reset", font_name=font)
        reset.bind(on_press=self.reset)
        box.add_widget(reset)
        self.result = Label(text="Enter your name.", font_name=font)
        box.add_widget(self.result)
        return box
    def greet(self, button):
        self.result.text = "Hello, " + (self.entry.text.strip() or "everyone") + "!"
    def reset(self, button):
        self.entry.text = ""
        self.result.text = "Enter your name."
GreetingApp().run()'''},mode='pc',note='Kivy 기본 글꼴의 한글 지원을 가정하지 않습니다. 한글 글꼴을 지정하면 한국어 문구로 바꿀 수 있습니다.')
lesson(2,'ui','사용자 인터페이스 · CLI, GUI, NUI','40–44','사용자가 어떤 행동으로 프로그램에 의도를 전달하나요?',[
'UI는 사람과 시스템이 상호 작용하는 접점입니다. 화면의 버튼·입력창·메뉴뿐 아니라 색상·글꼴·배치·피드백도 사용 편의성에 영향을 줍니다. 같은 기능이라도 저장 버튼을 찾기 어렵다면 사용자는 실수하기 쉽습니다.',
'CLI는 명령어 입력 방식입니다. 반복 작업 자동화와 정확한 명령 전달에 유용하지만 문법을 배워야 합니다. GUI는 아이콘·메뉴·버튼 같은 시각 요소를 조작합니다. NUI는 음성·손짓·터치 등 자연스러운 행동을 사용합니다. 터치 GUI처럼 분류가 겹치는 사례도 있습니다.',
'생각 열기: 파일 100개 이름을 바꾸는 일과 사진 한 장을 자르는 일에 각각 어떤 인터페이스를 선택할까요? 편리함은 사용자 경험과 작업 목적에 따라 달라집니다. 44쪽 탐구의 dir 입력은 CLI, 아이콘 클릭은 GUI, 손짓으로 TV 조작은 NUI입니다.'],[],['좋은 UI와 불편한 UI 사례를 한 가지씩 설명하세요.','버튼의 색만으로 오류를 알리면 누가 불편할지 생각하세요.'])
lesson(2,'libraries','GUI 라이브러리 비교 갤러리','45–48 + 보강','같은 인사 앱을 여섯 가지 방식으로 비교하세요.',[
'교과서의 tkinter, PyQt, wxPython, Kivy에 PySide6와 ttk를 보강했습니다. tkinter는 Tcl/Tk 연결이며 파이썬 배포에 흔히 포함됩니다. 다만 일부 Linux 환경은 python3-tk를 별도 설치해야 합니다. ttk는 Tk의 테마 위젯입니다.',
'PySide6와 PyQt6는 Qt 6를 파이썬에서 사용하는 서로 다른 바인딩입니다. 이 과정의 추가 실습은 Qt 공식 바인딩인 PySide6의 Qt Widgets를 사용합니다. 두 라이브러리의 외형은 같은 Qt 스타일을 쓰면 비슷하며 화면만으로 구분하기 어렵습니다.',
'wxPython은 wxWidgets 기반으로 운영체제의 위젯을 활용합니다. Kivy는 자체 그리기 방식으로 터치와 여러 플랫폼의 인터페이스를 구성합니다. 배포 대상·필요 위젯·학습 자료·환경 지원을 기준으로 선택하세요.',
'갤러리의 화면은 제공하는 코드를 실행한 캡처입니다. OS와 테마에 따라 외형은 달라집니다. PyQt와 PySide는 배포 조건이 다르므로 실제 배포 전 각 공식 라이선스 안내를 확인하는 습관을 갖습니다.',
'좀 더 알아보기: IDLE은 tkinter를 사용하는 실제 파이썬 프로그램입니다. IDLE의 메뉴·버튼·입력창이 어떤 위젯으로 구성될지 관찰하세요. 라이브러리를 선택한 이유는 기능과 사용자를 함께 근거로 적으세요.'],['hello-tk','hello-ttk','hello-pyside','hello-pyqt','hello-wx','hello-kivy'],['같은 앱을 학교 실습용과 터치 키오스크용으로 만들 때 선택 근거를 비교하세요.','48쪽 확인학습: UI 정의, GUI 장점, NUI 설명, 라이브러리 특징을 점검하세요.'])
ex('widgets-tk','tkinter 위젯 9종 체험',{'main.py':'''import tkinter as tk
root = tk.Tk()
root.title("tkinter 위젯 도감")
frame = tk.Frame(root, padx=16, pady=16)
frame.pack(fill="both", expand=True)
tk.Label(frame, text="Label: 설명을 표시합니다").pack()
tk.Entry(frame).pack(fill="x")
tk.Text(frame, height=3).pack(fill="x")
checked = tk.BooleanVar()
tk.Checkbutton(frame, text="학습 완료", variable=checked).pack()
choice = tk.StringVar(value="A")
for value in ["A", "B"]:
    tk.Radiobutton(frame, text=value, variable=choice, value=value).pack()
listbox = tk.Listbox(frame, height=3)
for value in ["모듈", "패키지", "GUI"]:
    listbox.insert(tk.END, value)
listbox.pack()
canvas = tk.Canvas(frame, width=240, height=60, bg="white")
canvas.create_oval(10, 10, 50, 50, fill="gold")
canvas.pack()
tk.Button(frame, text="상태 출력", command=lambda: print(checked.get(), choice.get())).pack()
root.mainloop()'''},mode='pc')
ex('widgets-pyside','PySide6 위젯과 그리기 공간',{'main.py':'''import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QCheckBox, QRadioButton, QListWidget,
    QPushButton, QGraphicsScene, QGraphicsView)
from PySide6.QtGui import QBrush, QColor
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PySide6 위젯 도감")
layout = QVBoxLayout(window)
layout.addWidget(QLabel("QLabel: 설명을 표시합니다"))
layout.addWidget(QLineEdit())
text = QPlainTextEdit()
text.setMaximumHeight(80)
layout.addWidget(text)
checked = QCheckBox("학습 완료")
layout.addWidget(checked)
for value in ["A", "B"]:
    layout.addWidget(QRadioButton(value))
items = QListWidget()
items.addItems(["모듈", "패키지", "GUI"])
layout.addWidget(items)
scene = QGraphicsScene()
scene.addEllipse(10, 10, 40, 40, brush=QBrush(QColor("gold")))
view = QGraphicsView(scene)
view.setMaximumHeight(80)
layout.addWidget(view)
button = QPushButton("상태 출력")
button.clicked.connect(lambda: print(checked.isChecked()))
layout.addWidget(button)
window.show()
sys.exit(app.exec())'''},mode='pc')
lesson(2,'widgets','창과 위젯 · 화면을 구성하는 부품','50','보여줄 정보와 받을 입력에 따라 위젯을 선택합니다.',[
'Tk 객체는 기본 창입니다. Label은 표시, Button은 명령, Entry는 한 줄 입력, Text는 여러 줄 입력입니다. Checkbutton은 독립적인 선택, Radiobutton은 묶음 중 하나의 선택, Listbox는 목록 선택입니다. Canvas는 도형·이미지 그리기 공간이며 Frame은 위젯을 묶는 컨테이너입니다.',
'위젯을 생성한 것만으로 배치가 완료되지는 않습니다. 부모 창이나 Frame을 지정하고 배치 관리자를 호출해야 합니다. BooleanVar·StringVar 같은 변수를 통해 체크 상태와 선택 값을 읽을 수 있습니다.',
'PySide6에서는 QApplication이 앱 실행을 관리하고 QWidget이 창·컨테이너 역할을 합니다. Label→QLabel, Button→QPushButton, Entry→QLineEdit, Text→QPlainTextEdit, Checkbutton→QCheckBox, Radiobutton→QRadioButton, Listbox→QListWidget으로 개념을 연결합니다. Canvas는 일대일 대응이 아니며 여기서는 QGraphicsScene/View로 도형을 그립니다.'],['widgets-tk','widgets-pyside'],['회원 가입 화면의 이름·소개·약관 동의·학년 선택에 알맞은 위젯을 고르세요.','체크박스와 라디오 버튼의 차이를 직접 조작하며 설명하세요.'])
ex('layout-tk','tkinter · 세 가지 배치',{'main.py':'''import tkinter as tk
root = tk.Tk()
root.title("배치 비교")
root.geometry("520x400")
# 서로 다른 부모 Frame 안에서 배치 방식을 비교합니다.
for kind in ["pack", "grid", "place"]:
    frame = tk.LabelFrame(root, text=kind, height=110)
    frame.pack(fill="x", padx=16, pady=8)
    if kind == "pack":
        for value in ["A", "B", "C"]:
            tk.Button(frame, text=value).pack(side="left", expand=True, fill="x")
    elif kind == "grid":
        for i, value in enumerate(["A", "B", "C"]):
            tk.Button(frame, text=value).grid(row=0, column=i, sticky="ew")
            frame.columnconfigure(i, weight=1)
    else:
        for i, value in enumerate(["A", "B", "C"]):
            tk.Button(frame, text=value).place(x=20 + i*80, y=10)
root.mainloop()'''},mode='pc')
ex('layout-pyside','PySide6 · 수평·수직·격자 배치',{'main.py':'''import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Qt 레이아웃")
window.resize(520, 300)
vertical = QVBoxLayout(window)
horizontal = QHBoxLayout()
for name in ["열기", "저장", "종료"]:
    horizontal.addWidget(QPushButton(name))
vertical.addLayout(horizontal)
grid = QGridLayout()
for i in range(6):
    grid.addWidget(QPushButton(str(i + 1)), i // 3, i % 3)
vertical.addLayout(grid)
window.show()
sys.exit(app.exec())'''},mode='pc')
lesson(2,'layout','배치 관리자와 반응하는 화면','51 + 보강','창을 늘렸을 때도 사용하기 좋은 화면을 만드세요.',[
'pack은 순서와 방향으로 배치하고, grid는 행·열로 배치하며, place는 좌표나 상대 위치를 지정합니다. 고정 좌표는 창 크기·글꼴 변화에 취약하므로 폼에는 grid, 순차 영역에는 pack부터 검토하세요.',
'pack(expand=True, fill="both")에서 expand는 여유 공간 배분, fill은 배정 영역 안에서 위젯을 늘리는 방향입니다. grid의 sticky="ew"와 columnconfigure(weight=1)는 가로 확장에 사용합니다. 같은 부모 안에서 pack과 grid를 혼용하지 마세요. 다른 Frame 안에서는 각각 사용할 수 있습니다.',
'Qt의 QVBoxLayout·QHBoxLayout·QGridLayout은 자식 위젯의 크기와 배치를 관리합니다. QWidget에 레이아웃을 설정하고 addWidget 또는 addLayout으로 구성합니다. tkinter 코드를 단어만 바꾸는 대신 배치 의도를 옮기세요.'],['layout-tk','layout-pyside'],['창을 좁게·넓게 바꾸어 잘리는 요소를 찾으세요.','웹 배치 체험에서 수평·수직·격자를 비교하세요.'])
lesson(2,'events','이벤트 · 사용자의 행동에 반응하기','51, 54 + 보강','버튼 생성 시점과 클릭 시점은 다릅니다.',[
'콜백은 나중에 호출할 함수입니다. command=greet는 함수 자체를 전달합니다. command=greet()는 지금 함수를 실행하고 반환값을 전달하므로 의도와 다릅니다. 인자가 필요하면 lambda: greet(name)처럼 호출을 감쌉니다.',
'tkinter의 mainloop는 이벤트 루프입니다. PySide6에서는 clicked.connect(greet)로 버튼의 시그널과 함수를 연결하고 app.exec()로 이벤트 루프를 시작합니다. connect(greet())도 같은 이유로 잘못된 사용입니다.',
'입력 변화는 tkinter의 bind나 변수 추적, PySide6의 textChanged 같은 시그널로 다룰 수 있습니다. GUI 이벤트 안에서 긴 반복·time.sleep을 실행하면 화면 반응이 늦어집니다. 주기 작업에는 after 또는 QTimer를 사용하고 긴 작업 분리는 심화 주제로 다룹니다.'],['hello-tk','hello-pyside'],['인사 버튼에 빈 이름을 넣어도 동작하도록 만드세요.','버튼을 두 번 눌렀을 때 상태가 어떻게 바뀌는지 추적하세요.'])
tk_memo='''import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", tk.END))

window = tk.Tk()
window.title("나만의 메모장 · tkinter")
window.geometry("640x420")
text_area = tk.Text(window, wrap="word")
text_area.pack(expand=True, fill="both")
menu = tk.Menu(window)
window.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="파일", menu=file_menu)
file_menu.add_command(label="열기", command=open_file)
file_menu.add_command(label="저장", command=save_file)
file_menu.add_command(label="종료", command=window.quit)
window.mainloop()'''
ex('memo-tk','교과서 메모장 · tkinter 전체 코드',{'main.py':tk_memo},mode='pc')
qt_memo='''import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QAction

class MemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("나만의 메모장 · PySide6")
        self.resize(640, 420)
        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)
        menu = self.menuBar().addMenu("파일")
        for title, handler in [("열기", self.open_file), ("저장", self.save_file), ("종료", self.close)]:
            action = QAction(title, self)
            action.triggered.connect(handler)
            menu.addAction(action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "열기", "", "텍스트 (*.txt);;모든 파일 (*)")
        if not path:
            return
        try:
            self.editor.setPlainText(Path(path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "열기 실패", str(error))

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "저장", "memo.txt", "텍스트 (*.txt)")
        if not path:
            return
        try:
            Path(path).write_text(self.editor.toPlainText(), encoding="utf-8")
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "저장 실패", str(error))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoWindow()
    window.show()
    sys.exit(app.exec())'''
ex('memo-pyside','메모장 · PySide6 전체 코드',{'main.py':qt_memo},mode='pc')
lesson(2,'memo','교과서 메모장 · 여덟 단계로 완성','52–55','열기와 저장을 만드는 동안 1단원의 import와 함수가 다시 등장합니다.',[
'① tkinter와 filedialog를 임포트합니다. ② Tk()로 창을 만들고 title로 제목을 정합니다. ③ Text(window, wrap="word")를 생성하고 pack(expand=True, fill="both")로 창을 채웁니다.',
'④ 열기 함수: askopenfilename → 취소 여부 확인 → UTF-8로 읽기 → delete("1.0", END)로 기존 내용 제거 → insert로 새 내용 삽입입니다. "1.0"은 첫 줄 0번째 문자입니다.',
'⑤ 저장 함수: asksaveasfilename(defaultextension=".txt") → 취소 확인 → Text.get으로 읽기 → UTF-8 파일 쓰기입니다. 교과서의 END는 Text가 유지하는 마지막 개행까지 포함합니다. 추가 개행을 제외하려면 "end-1c"를 사용합니다.',
'⑥ Menu에 열기·저장·종료를 연결합니다. ⑦ mainloop()로 이벤트를 기다립니다. ⑧ 전체 코드를 실행하고 한글 파일 저장→재열기를 시험합니다. 교과서 55쪽 탐구의 라이브러리 이름은 tkinter입니다.',
'PySide6 비교: QMainWindow의 중앙에 QPlainTextEdit를 두고 QAction을 메뉴에 연결합니다. QFileDialog는 (경로, 선택 필터)를 반환하므로 path, _로 받습니다. setPlainText/toPlainText가 텍스트 넣기·읽기 역할입니다.'],['memo-tk','memo-pyside'],['새 파일 저장, 기존 파일 열기, 대화 상자 취소를 각각 시험하세요.','파일 열기 코드의 순서를 섞은 뒤 다시 배열하세요.','메뉴를 누르기 전에 파일 대화 상자가 뜬다면 어떤 코드를 확인할까요?'])
lesson(2,'pyside','PySide6 시작과 Qt Designer','확장 학습','기본 위젯으로 익힌 개념을 Qt Widgets로 옮깁니다.',[
'PC의 프로젝트 폴더에서 python -m venv .venv를 실행합니다. Windows PowerShell은 .venv\\Scripts\\Activate.ps1, macOS/Linux는 source .venv/bin/activate로 활성화합니다. 이후 python -m pip install PySide6로 설치하고 python main.py로 실행합니다. VS Code에서 같은 .venv 인터프리터를 선택하세요.',
'첫 예제는 함수 기반으로 QApplication → QWidget → 레이아웃 → 위젯 → connect → show → exec 순서를 익힙니다. 메모장은 QMainWindow를 상속하는 클래스로 상태와 메서드를 묶습니다. self.editor는 여러 메서드에서 같은 입력창을 사용하게 합니다.',
'Qt Designer는 pyside6-designer로 실행합니다. Widget 폼에 라벨·입력창·버튼을 배치하고 레이아웃을 적용한 다음 form.ui로 저장하세요. pyside6-uic form.ui -o ui_form.py로 Python 코드를 생성할 수 있습니다.',
'생성 파일은 다시 생성하면 덮어써집니다. 직접 작성하는 main.py에서 Ui_Form을 가져와 setupUi(window)를 호출하고 이벤트를 연결하세요. 버튼의 objectName을 확인해야 코드에서 올바른 이름으로 접근할 수 있습니다. Qt Quick/QML은 별도 UI 기술이며 이번 기본 실습은 Qt Widgets입니다.'],['hello-pyside','memo-pyside'],['Designer의 objectName과 화면에 보이는 text가 다른 속성임을 확인하세요.','tkinter의 이벤트와 Qt 시그널을 자신의 말로 비교하세요.'],extra=True)
# Two front ends reuse one core package.
core={'core/__init__.py':'# GUI와 독립적인 기능','core/logic.py':'''from datetime import date
import random

def roll(sides):
    if sides < 1:
        raise ValueError("면 수는 1 이상이어야 합니다.")
    return random.randint(1, sides)

def days_left(target, today=None):
    today = today or date.today()
    return (date.fromisoformat(target) - today).days

def draw(names, count):
    names = list(dict.fromkeys(name.strip() for name in names if name.strip()))
    if not 1 <= count <= len(names):
        raise ValueError("추첨 수를 명단 인원 안에서 정하세요.")
    return random.sample(names, count)'''}
ex('core','프로젝트 · 기능 모듈을 웹에서 검사',{'main.py':'''from core.logic import roll, days_left, draw
from datetime import date
print("주사위:", roll(6))
print("남은 날짜:", days_left("2026-12-25", date(2026, 12, 24)))
print("추첨:", draw(["민지", "수빈", "하늘"], 2))''',**core},checks='assert days_left("2026-12-25", date(2026,12,24)) == 1\nassert 1 <= roll(6) <= 6\nassert len(draw(["A", "A", "B"], 2)) == 2')
ex('project-tk','생활 도우미 · tkinter',{'main.py':'''import tkinter as tk
from tkinter import messagebox
from core.logic import roll, days_left, draw

def run_task():
    try:
        if mode.get() == "주사위":
            result.set(str(roll(int(entry.get()))))
        elif mode.get() == "D-day":
            result.set(str(days_left(entry.get())) + "일")
        else:
            result.set(", ".join(draw(entry.get().split(","), 1)))
    except ValueError as error:
        messagebox.showwarning("입력 확인", str(error))
root = tk.Tk()
root.title("우리 반 생활 도우미 · tkinter")
root.geometry("520x280")
mode = tk.StringVar(value="주사위")
for name in ["주사위", "D-day", "추첨"]:
    tk.Radiobutton(root, text=name, variable=mode, value=name).pack(anchor="w")
tk.Label(root, text="면 수 / YYYY-MM-DD / 쉼표로 나눈 이름을 입력하세요.").pack()
entry = tk.Entry(root)
entry.insert(0, "6")
entry.pack(fill="x", padx=16)
tk.Button(root, text="실행", command=run_task).pack(pady=12)
result = tk.StringVar(value="결과가 여기에 표시됩니다.")
tk.Label(root, textvariable=result).pack()
root.mainloop()''',**core},mode='pc')
ex('project-pyside','생활 도우미 · PySide6',{'main.py':'''import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox,
    QLabel, QLineEdit, QPushButton, QMessageBox)
from core.logic import roll, days_left, draw

class HelperWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("우리 반 생활 도우미 · PySide6")
        self.resize(520, 280)
        layout = QVBoxLayout(self)
        self.mode = QComboBox()
        self.mode.addItems(["주사위", "D-day", "추첨"])
        layout.addWidget(self.mode)
        layout.addWidget(QLabel("면 수 / YYYY-MM-DD / 쉼표로 나눈 이름"))
        self.entry = QLineEdit("6")
        layout.addWidget(self.entry)
        button = QPushButton("실행")
        button.clicked.connect(self.run_task)
        layout.addWidget(button)
        self.result = QLabel("결과가 여기에 표시됩니다.")
        layout.addWidget(self.result)

    def run_task(self):
        try:
            value = self.entry.text()
            mode = self.mode.currentText()
            if mode == "주사위":
                output = str(roll(int(value)))
            elif mode == "D-day":
                output = str(days_left(value)) + "일"
            else:
                output = ", ".join(draw(value.split(","), 1))
            self.result.setText(output)
        except ValueError as error:
            QMessageBox.warning(self, "입력 확인", str(error))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelperWindow()
    window.show()
    sys.exit(app.exec())''',**core},mode='pc')
lesson(1,'project','1단원 프로젝트 · 우리 반 기능 패키지','보강 · 수행평가 연결','GUI 없이도 시험할 수 있는 기능부터 만듭니다.',[
'core/logic.py에 주사위, 날짜 계산, 명단 추첨 함수를 작성하세요. 함수는 결과를 반환하고 main.py에서 출력합니다. 화면·입력·계산을 분리하면 다음 단원에서 GUI만 추가할 수 있습니다.',
'기본: 제공된 기능을 실행하고 인자를 바꿉니다. 도전: 중복 명단 정리와 잘못된 입력을 처리합니다. 확장: 새 기능을 하나 추가하고 테스트 입력 3개를 설명합니다.'],['core'],['파일 트리와 각 파일의 역할을 제출 설명에 적으세요.','정상 입력·경계 입력·잘못된 입력을 하나씩 시험하세요.'],extra=True)
lesson(2,'project','통합 프로젝트 · 두 GUI, 하나의 기능 모듈','수행평가 연결 + 확장','1단원의 패키지에 화면을 연결하여 앱을 완성합니다.',[
'같은 core.logic을 tkinter와 PySide6에서 임포트합니다. 각 GUI는 입력값을 읽어 함수에 전달하고 결과를 표시합니다. core에는 tkinter·PySide6 코드가 없으므로 웹에서도 기능을 검사할 수 있습니다.',
'기본 완성 조건: 위젯 배치, 버튼 이벤트, 모듈 분리, 잘못된 입력 안내입니다. 확장 과제: 추첨 인원 입력, 결과 기록, 설명 문구 개선 중 하나를 선택하세요. 두 버전 모두 실행하고 같은 입력의 의미가 유지되는지 비교합니다.',
'운영 계획의 수행①은 기능·이벤트 10점, 모듈 구조·코드 품질 5점, 저널 5점입니다. 이 사이트의 체크·연습 점수는 공식 성적이 아닙니다. PySide6 학습은 확장 경로이며 별도 평가 조건을 추가하지 않습니다.',
'수행평가에서는 교사가 명시적으로 허용하지 않은 AI 도움 없이 스스로 작성해야 합니다. 저널에는 구현 내용, 오류, 해결 근거를 기록하고 코드와 함께 제출하세요.'],['core','project-tk','project-pyside'],['빈 입력, 0면 주사위, 잘못된 날짜, 중복 이름을 시험하세요.','프로젝트 ZIP과 학습 기록을 내려받아 선생님이 정한 경로로 제출하세요.'],extra=True)
lesson(2,'review','2단원 마무리 · 개념에서 앱까지','56–59','어떤 위젯을 왜 배치했고, 어떤 이벤트에 반응하는지 설명하세요.',[
'중단원 정리: Tk 객체가 창을 만들고, 위젯이 입력·표시 기능을 맡고, 배치 관리자가 위치를 정하며, 이벤트 함수가 사용자 행동에 반응합니다. mainloop가 이벤트를 기다립니다.',
'57쪽 확인학습의 IDLE 코드에서 컨테이너는 Frame, 클릭 요소는 Button, 이 요소들의 통칭은 위젯입니다. 종합 평가에서는 Tk 객체, UI 편의성, UI 정의, GUI 사례, 버튼 콜백, 배치 방식, pack 호출을 모두 확인합니다.',
'교과서 58쪽 4번의 "사용자 정의 예외" 표현은 보기 내용과 맞지 않습니다. 웹에서는 아이콘 클릭 사례의 인터페이스 유형을 판단하는 문제로 명확히 적었습니다.'],[],['예제 없이 창·버튼·콜백·이벤트 루프를 작성하세요.','교과서 확인학습과 종합평가 연계 문제를 풀고 틀린 이유를 기록하세요.'])
# Optional, complete memo improvements: state, shortcuts and guarded close.
ex('memo-plus-tk','개선 메모장 · tkinter',{'main.py':'''import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

class MemoApp:
    def __init__(self, root):
        self.root = root
        self.path = None
        self.dirty = False
        root.geometry("680x440")
        self.text = tk.Text(root, wrap="word", undo=True)
        self.text.pack(expand=True, fill="both")
        self.status = tk.Label(root, anchor="w")
        self.status.pack(fill="x")
        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="열기", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="저장", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="다른 이름으로 저장", command=lambda: self.save_file(True))
        file_menu.add_command(label="종료", command=self.close)
        root.bind("<Control-o>", lambda event: self.open_file())
        root.bind("<Control-s>", lambda event: self.save_file())
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.text.bind("<<Modified>>", self.changed)
        self.refresh()

    def refresh(self):
        name = self.path.name if self.path else "제목 없음"
        self.root.title(("* " if self.dirty else "") + name + " · tkinter")
        self.status.config(text=f"{len(self.text.get('1.0', 'end-1c'))}자 · UTF-8")

    def changed(self, event=None):
        if self.text.edit_modified():
            self.dirty = True
            self.text.edit_modified(False)
            self.refresh()

    def confirm_discard(self):
        if not self.dirty:
            return True
        answer = messagebox.askyesnocancel("미저장 문서", "변경 내용을 저장할까요?")
        if answer is None:
            return False
        return self.save_file() if answer else True

    def open_file(self):
        if not self.confirm_discard():
            return
        name = filedialog.askopenfilename()
        if not name:
            return
        try:
            content = Path(name).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            messagebox.showerror("열기 실패", str(error))
            return
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.text.edit_modified(False)
        self.path, self.dirty = Path(name), False
        self.refresh()

    def save_file(self, save_as=False):
        target = self.path
        if target is None or save_as:
            name = filedialog.asksaveasfilename(defaultextension=".txt")
            if not name:
                return False
            target = Path(name)
        try:
            target.write_text(self.text.get("1.0", "end-1c"), encoding="utf-8")
        except (OSError, UnicodeError) as error:
            messagebox.showerror("저장 실패", str(error))
            return False
        self.path, self.dirty = target, False
        self.text.edit_modified(False)
        self.refresh()
        return True

    def close(self):
        if self.confirm_discard():
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoApp(root)
    root.mainloop()'''},mode='pc')
ex('memo-plus-pyside','개선 메모장 · PySide6',{'main.py':'''import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QAction, QKeySequence

class MemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.resize(680, 440)
        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)
        menu = self.menuBar().addMenu("파일")
        for label, handler, key in [
            ("열기", self.open_file, QKeySequence.StandardKey.Open),
            ("저장", self.save_file, QKeySequence.StandardKey.Save),
            ("다른 이름으로 저장", lambda: self.save_file(True), QKeySequence.StandardKey.SaveAs),
            ("종료", self.close, QKeySequence.StandardKey.Quit),
        ]:
            action = QAction(label, self)
            action.setShortcut(QKeySequence(key))
            # triggered(bool)의 checked를 save_as로 잘못 전달하지 않도록 감쌉니다.
            action.triggered.connect(lambda checked=False, fn=handler: fn())
            menu.addAction(action)
        self.editor.textChanged.connect(self.refresh)
        self.editor.document().modificationChanged.connect(self.refresh)
        self.refresh()

    def refresh(self):
        name = self.path.name if self.path else "제목 없음"
        dirty = self.editor.document().isModified()
        self.setWindowTitle(("* " if dirty else "") + name + " · PySide6")
        self.statusBar().showMessage(f"{len(self.editor.toPlainText())}자 · UTF-8")

    def confirm_discard(self):
        if not self.editor.document().isModified():
            return True
        B = QMessageBox.StandardButton
        answer = QMessageBox.question(self, "미저장 문서", "변경 내용을 저장할까요?", B.Save | B.Discard | B.Cancel)
        if answer == B.Cancel:
            return False
        return self.save_file() if answer == B.Save else True

    def open_file(self):
        if not self.confirm_discard():
            return
        name, _ = QFileDialog.getOpenFileName(self, "열기", "", "텍스트 (*.txt);;모든 파일 (*)")
        if not name:
            return
        try:
            content = Path(name).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "열기 실패", str(error))
            return
        self.path = Path(name)
        self.editor.setPlainText(content)
        self.editor.document().setModified(False)
        self.refresh()

    def save_file(self, save_as=False):
        target = self.path
        if target is None or save_as:
            name, _ = QFileDialog.getSaveFileName(self, "저장", "memo.txt", "텍스트 (*.txt)")
            if not name:
                return False
            target = Path(name)
        try:
            target.write_text(self.editor.toPlainText(), encoding="utf-8")
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "저장 실패", str(error))
            return False
        self.path = target
        self.editor.document().setModified(False)
        self.refresh()
        return True

    def closeEvent(self, event):
        if self.confirm_discard():
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoWindow()
    window.show()
    sys.exit(app.exec())'''},mode='pc')
for l in units[2]:
 if l['id']=='memo':
  l['examples'] += ['memo-plus-tk','memo-plus-pyside']
  l['paragraphs'].append('확장 완성 예제에는 글자 수, Ctrl+O/Ctrl+S, 다른 이름으로 저장, 창 닫기 시 미저장 확인, UTF-8 읽기·쓰기 실패 안내가 들어 있습니다. 저장 대화 상자를 취소하면 닫기도 취소되도록 반환값을 연결했습니다. 기본 메모장과 비교하며 한 기능씩 옮기세요.')
