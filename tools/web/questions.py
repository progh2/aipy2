from content import q, questions
# Carefully authored tasks; execution checks accept equivalent implementations.
def choice(u,t,p,a,opts,h,e,ref='보강'): q(u,t,'선택',p,a,h,e,options=opts,ref=ref)
def blank(u,t,p,a,h,e,ref='보강'): q(u,t,'빈칸',p,a,h,e,ref=ref)
def written(u,t,p,a,h,e,ref='보강'): q(u,t,'서술',p,a,h,e,ref=ref)
def coding(u,t,p,s,a,test,h,e,kind='구현'): q(u,t,kind,p,a,h,e,starter=s,checks=test)
choice(1,'overview','모듈에 대한 설명으로 틀린 것을 고르세요.','저장한 Python 파일은 모듈이 될 수 없습니다.',['파일 이름은 모듈 이름의 기준입니다.','함수를 담을 수 있습니다.','변수와 실행문도 담을 수 있습니다.','저장한 Python 파일은 모듈이 될 수 없습니다.','기능별로 코드를 나눌 수 있습니다.'],'모듈의 가장 기본적인 단위를 떠올리세요.','Python 파일은 모듈로 사용할 수 있습니다.','교과서 36쪽 1')
choice(1,'overview','모듈화의 목적과 가장 거리가 먼 것은?','아무 이름이나 더 많이 만들기',['중복 줄이기','코드 재사용','유지보수','아무 이름이나 더 많이 만들기','구조화'],'이름의 수보다 역할이 중요합니다.','모듈화는 코드의 재사용과 관리를 돕습니다.','교과서 36쪽 2')
for p,a,h,e in [
('함수·변수·클래스 등을 담은 Python 파일은?','모듈','파일 단위입니다.','모듈은 하나의 파일에 관련 기능을 묶습니다.'),
('관련 모듈을 폴더 계층으로 묶은 구조는?','패키지','nature/animals를 떠올리세요.','패키지는 관련 모듈을 분류합니다.'),
('다른 모듈을 가져오는 키워드는?','import','영어로 가져오기입니다.','import로 모듈을 연결합니다.'),
('직접 실행한 파일의 __name__ 값은?','__main__','앞뒤 밑줄이 각각 두 개입니다.','임포트된 경우에는 모듈 이름입니다.'),
('if __name__ == "____": 의 빈칸을 채우세요.','__main__','직접 실행일 때만 시험 코드를 실행합니다.','조건 안의 코드는 임포트 시 실행되지 않습니다.'),
('import greet as g 이후 인사 함수 호출은?','g.hello()','별칭을 통해 접근합니다.','파일명이 아니라 현재 연결된 이름 g를 사용합니다.'),
('from greet import hello 이후 호출은?','hello()','모듈 접두어가 필요 없습니다.','hello라는 이름을 직접 가져왔습니다.'),
('일반 패키지의 초기화 파일 이름은?','__init__.py','밑줄 두 개를 앞뒤에 씁니다.','일반 패키지와 네임스페이스 패키지를 구분하세요.'),
('별표 임포트로 공개할 이름 목록을 지정하는 변수는?','__all__','all 앞뒤에 밑줄 두 개입니다.','__all__은 별표 임포트의 목록을 지정합니다.'),
('현재 작업 폴더를 반환하는 os 함수 호출은?','os.getcwd()','get current working directory입니다.','실행 스크립트 위치와 항상 같지는 않습니다.'),
('실행 인자를 저장하는 sys 속성은?','sys.argv','argument vector입니다.','첫 항목은 실행 파일명입니다.'),
('프로그램을 종료하는 sys 함수 호출은?','sys.exit()','exit를 사용합니다.','SystemExit를 발생시킵니다.'),
('math의 원주율 상수는?','math.pi','상수에는 호출 괄호가 없습니다.','pi는 실수 상수입니다.'),
('목록에서 요소 하나를 고르는 random 함수 이름은?','choice','선택을 뜻합니다.','choice(sequence)는 요소 하나를 반환합니다.'),
('목록 자체를 섞는 함수 이름은?','shuffle','반환값은 None입니다.','원본 리스트를 수정합니다.'),
('날짜 객체의 요일을 얻는 메서드 호출은?','weekday()','속성과 메서드를 구분하세요.','월요일은 0, 일요일은 6입니다.')]:
 blank(1,'기초 개념',p,a,h,e)
for imp,answer in [('from student import study','study()'),('import student','student.study()'),('import student as s','s.study()')]:
 blank(1,'imports',f'{imp}\n위 코드 다음에 study 함수를 호출하세요.',answer,'현재 연결된 이름을 확인하세요.','임포트 방식에 맞춰 함수에 접근합니다.','교과서 36쪽 3')
for imp,answer in [('from nature.plants import grass as g','g.wild()'),('from nature.plants.grass import wild','wild()'),('from nature.plants.grass import *','wild()'),('import nature.plants.grass','nature.plants.grass.wild()')]:
 blank(1,'packages',f'{imp}\nwild 함수 호출 코드를 쓰세요.',answer,'모듈을 가져왔는지 함수를 가져왔는지 확인하세요.','접두어가 필요한지는 현재 네임스페이스의 이름으로 결정됩니다.','교과서 37쪽 4')
choice(1,'random','고유한 항목의 리스트 L에서 중복 없이 2개를 뽑는 코드는?','random.sample(L, 2)',['random.random()','random.sample()','random.randrange()','random.randrange(2)','random.sample(L, 2)'],'모집단과 개수를 함께 전달합니다.','sample은 비복원 추출입니다.','교과서 37쪽 5')
for p,a,explanation in [
('print(__name__)을 직접 실행했을 때 출력은?','__main__','실행 진입점의 이름입니다.'),
('import math\nprint(math.ceil(-3.5))','-3','-3.5 이상인 최소 정수입니다.'),
('import math\nprint(math.floor(-3.5))','-4','-3.5 이하인 최대 정수입니다.'),
('import math\nprint(math.factorial(0))','1','0!은 1입니다.'),
('import math\nprint(math.gcd(28,70))','14','28과 70을 모두 나누는 가장 큰 양의 정수입니다.'),
('import math\nprint(math.pow(2,10))','1024.0','math.pow는 실수를 반환합니다.'),
('import random\na=[1,2,3]\nprint(random.shuffle(a))','None','shuffle은 제자리 변경 후 None을 반환합니다.'),
('from datetime import date\nprint(date(2026,12,25).weekday())','4','2026년 12월 25일은 금요일입니다.')]:
 q(1,'결과 추적','예측',p,a,'손으로 먼저 계산한 뒤 실습창에서 확인하세요.',explanation)
for p,a,opts,h,e in [
('from pkg import *에서 __all__에 없는 이름은 명시적으로 import할 수 없나요?','명시적으로 가져올 수 있습니다.',['항상 금지됩니다.','명시적으로 가져올 수 있습니다.','파일이 삭제됩니다.','폴더 이름이 바뀝니다.','Python이 종료됩니다.'],'별표 임포트의 범위를 정하는 설정입니다.','__all__은 접근 제어 장치가 아닙니다.'),
('random.randrange(1,7,2)의 후보는?','1, 3, 5',['1, 2, 3','1, 3, 5','1, 3, 5, 7','2, 4, 6','1, 7'],'range와 같은 범위입니다.','끝 7은 포함하지 않습니다.'),
('uniform(2.5,10.0)의 끝 값 설명으로 정확한 것은?','반올림에 따라 10.0이 포함될 수도 있습니다.',['항상 10.0 미만입니다.','항상 10.0입니다.','정수만 나옵니다.','반올림에 따라 10.0이 포함될 수도 있습니다.','2.5는 제외합니다.'],'부동소수점 연산을 고려하세요.','교과서의 끝 미만 설명을 보완합니다.'),
('이미지 크기를 바꾸는 패키지는?','Pillow',['Pillow','Flask','Django','Peewee','Scrapy'],'이미지 처리 도구입니다.','설치 이름 pillow와 임포트 이름 PIL이 다릅니다.'),
('HTML에서 제목을 추출할 때 선택할 도구는?','Beautiful Soup',['Pygame','Beautiful Soup','NumPy','Peewee','tkinter'],'HTML/XML 파싱을 돕습니다.','beautifulsoup4를 설치하고 bs4를 임포트합니다.'),
('설치 성공 후 import가 실패할 때 먼저 확인할 것은?','설치 환경과 실행 인터프리터',['키보드 색상','설치 환경과 실행 인터프리터','모니터 크기','파일 확장자를 jpg로 변경','함수 이름을 모두 변경'],'python -m pip를 사용한 이유입니다.','다른 가상환경에 설치했을 수 있습니다.')]: choice(1,'응용 판단',p,a,opts,h,e)
coding(1,'define','add(a,b)가 합을 반환하게 완성하세요.','def add(a,b):\n    pass','def add(a,b):\n    return a+b','assert add(3,5)==8\nassert add(-2,5)==3\nassert add(0,0)==0','print와 return을 구분하세요.','반환값을 검사하므로 출력만 하면 통과하지 않습니다.')
coding(1,'math','radius가 반지름인 원의 넓이를 반환하세요.','import math\ndef area(radius):\n    pass','import math\ndef area(radius):\n    return math.pi * radius ** 2','import math\nassert math.isclose(area(3), math.pi*9)\nassert area(0)==0','원의 넓이는 πr²입니다.','여러 반지름으로 검사합니다.')
coding(1,'random','roll(n)이 1부터 n 사이 정수를 반환하게 하세요.','import random\ndef roll(n):\n    return random.randrange(n)','import random\ndef roll(n):\n    return random.randrange(1,n+1)','assert roll(1)==1\nfor _ in range(100):\n    x=roll(6)\n    assert isinstance(x,int) and 1<=x<=6','끝 값은 제외됩니다.','0이 나오지 않아야 하며 1면 주사위는 항상 1입니다.','오류 수정')
coding(1,'random','pick(names)가 서로 다른 2명을 반환하고 원본을 보존하게 만드세요.','import random\ndef pick(names):\n    pass','import random\ndef pick(names):\n    return random.sample(names,2)','names=["A","B","C"]\na=pick(names)\nassert len(a)==2 and len(set(a))==2\nassert set(a)<=set(names)\nassert names==["A","B","C"]','sample을 사용할 수 있습니다.','반환 개수·중복·원본 보존을 검사합니다.')
coding(1,'datetime','두 ISO 날짜 사이 일수를 반환하세요.','from datetime import date\ndef days(start,end):\n    pass','from datetime import date\ndef days(start,end):\n    return (date.fromisoformat(end)-date.fromisoformat(start)).days','assert days("2026-12-24","2026-12-25")==1\nassert days("2026-12-25","2026-12-24")==-1\nassert days("2024-02-28","2024-03-01")==2','문자열을 date로 바꾸세요.','윤년·역순 날짜도 검사합니다.')
coding(1,'imports','별칭을 사용한 코드를 고치세요.','import math as m\nvalue = math.sqrt(81)','import math as m\nvalue = m.sqrt(81)','assert value==9','현재 사용할 수 있는 이름은 m입니다.','명시적으로 연결하지 않은 math 이름을 호출했습니다.','오류 수정')
coding(1,'random','원본을 섞되 함수가 섞인 리스트를 반환하도록 고치세요.','import random\ndef mix(values):\n    return random.shuffle(values)','import random\ndef mix(values):\n    random.shuffle(values)\n    return values','values=[1,2,3]\nr=mix(values)\nassert sorted(r)==[1,2,3] and r is values','shuffle의 반환값을 떠올리세요.','변경된 원본 리스트를 반환합니다.','오류 수정')
coding(1,'datetime','날짜의 한글 요일 한 글자를 반환하세요.','from datetime import date\ndef weekday_name(value):\n    pass','from datetime import date\ndef weekday_name(value):\n    return "월화수목금토일"[date.fromisoformat(value).weekday()]','assert weekday_name("2026-12-25")=="금"\nassert weekday_name("2026-12-27")=="일"','weekday()는 월요일 0입니다.','숫자를 요일 목록의 인덱스로 사용합니다.')
q(1,'packages','순서','모듈을 만들고 실행하는 순서로 배열하세요.',['프로젝트 폴더 만들기','tools.py에 함수 저장','main.py에서 tools 임포트','tools의 함수 호출','main.py 실행'],'파일을 먼저 준비합니다.','만들기→연결하기→호출하기→실행하기 순서입니다.')
q(1,'main','순서','addcal에 최상위 print가 있고 subcal 시험 코드에는 main 가드가 있습니다. main의 실행 순서를 배열하세요.',['addcal 최상위 출력','subcal 정의 로드','main의 덧셈 호출','main의 뺄셈 호출'],'임포트된 모듈의 최상위부터 확인하세요.','main 가드 안의 subcal 시험 출력은 건너뜁니다.')
written(1,'overview','모듈과 패키지의 개념 및 필요성을 각각 설명하세요.','모듈은 관련 코드를 담은 파일이며 패키지는 관련 모듈의 계층입니다. 중복 감소·재사용·구조화·이름 충돌 구분에 유용합니다.','파일과 폴더 예를 한 개씩 넣으세요.','파일/폴더 구분과 구체적인 장점 두 가지를 포함했는지 점검하세요.','교과서 10·12·13쪽')
written(1,'main','__main__ 가드가 필요한 이유와 실행 결과 차이를 설명하세요.','직접 실행할 때만 시험 코드를 돌려서 임포트하는 프로그램에 불필요한 출력과 동작이 섞이지 않도록 합니다.','임포트도 최상위 코드를 실행합니다.','조건 유무에 따른 출력 차이를 설명했는지 점검하세요.')
written(1,'project','기능 모듈을 GUI와 분리하면 어떤 점을 쉽게 검사할 수 있나요?','화면 없이 함수에 여러 입력을 전달하여 결과와 예외를 검사하고 두 GUI에서 같은 기능을 재사용할 수 있습니다.','core.logic의 역할을 떠올리세요.','테스트와 재사용 두 관점을 포함하세요.')
written(1,'review','39쪽 마지막 출력이 5인 이유를 설명하세요.','subnum(7,2)는 7-2를 반환하므로 5입니다. subcal의 시험 호출은 임포트 시 실행되지 않습니다.','정답편 숫자보다 코드를 추적하세요.','출력 순서는 합 4, 합 8, 차 5입니다.','교과서 39쪽 8 · 정답편 보완')
# Additional debugging tasks with distinct checks.
coding(1,'define','둘레 함수를 출력 대신 반환하도록 수정하세요.','def perimeter(w,h):\n    print(2*(w+h))','def perimeter(w,h):\n    return 2*(w+h)','assert perimeter(2,4)==12\nassert perimeter(0,3)==6','다른 함수가 사용할 결과가 필요합니다.','print의 반환값은 None입니다.','오류 수정')
coding(1,'math','한 상자에 4개씩 담을 때 필요한 상자 수를 반환하세요.','import math\ndef boxes(n):\n    return n//4','import math\ndef boxes(n):\n    return math.ceil(n/4)','assert boxes(5)==2\nassert boxes(4)==1\nassert boxes(0)==0','남는 물건에도 상자 하나가 필요합니다.','올림 또는 동등한 정수 계산을 사용할 수 있습니다.','오류 수정')
coding(1,'datetime','올해 12월 25일이 지났으면 다음 해를 선택하세요.','from datetime import date\ndef christmas(today):\n    return date(today.year,12,25)','from datetime import date\ndef christmas(today):\n    target=date(today.year,12,25)\n    if target<today:\n        target=date(today.year+1,12,25)\n    return target','assert christmas(date(2026,12,24))==date(2026,12,25)\nassert christmas(date(2026,12,25))==date(2026,12,25)\nassert christmas(date(2026,12,26))==date(2027,12,25)','당일은 올해 날짜를 유지합니다.','경계 날짜를 검사해야 연도 전환 오류를 찾습니다.','오류 수정')
coding(1,'random','공백·중복 이름을 정리하고 입력 순서를 유지하세요.','def clean(names):\n    return names','def clean(names):\n    return list(dict.fromkeys(n.strip() for n in names if n.strip()))','assert clean([" A ","A","","B"])==["A","B"]\nassert clean([])==[]','문자열 정리 후 중복을 제거하세요.','중복 값이 있는 모집단은 추첨에서 같은 사람이 중복될 수 있습니다.','오류 수정')
coding(1,'sys','문자열 실행 인자 두 개의 합을 반환하세요.','def sum_args(args):\n    return args[0]+args[1]','def sum_args(args):\n    return int(args[0])+int(args[1])','assert sum_args(["3","5"])==8\nassert sum_args(["-1","2"])==1','sys.argv의 요소는 문자열입니다.','정수 변환 없이 더하면 문자열 연결입니다.','오류 수정')

# Unit 2: concept questions, widget matching, code repair and transfer.
for p,a,opts,h,e,ref in [
('사용자 인터페이스 설명 중 틀린 것은?','CLI는 그래픽 버튼으로만 조작합니다.',['UI에는 버튼과 색상이 포함됩니다.','CLI는 그래픽 버튼으로만 조작합니다.','GUI는 메뉴를 클릭합니다.','NUI는 손짓을 사용합니다.','UI는 상호 작용의 접점입니다.'],'CLI의 C는 Command입니다.','CLI는 명령어 기반입니다.','교과서 48쪽 1'),
('아이콘을 클릭하여 그림판을 열었습니다. 유형은?','GUI',['CLI','GUI','NUI','API','TUI'],'시각적인 아이콘을 조작했습니다.','교과서의 문항 제목 오류를 보완한 인터페이스 분류 문제입니다.','교과서 58쪽 4'),
('운영체제 고유 위젯을 활용하는 라이브러리는?','wxPython',['tkinter','PyQt6','wxPython','Kivy','Django'],'wxWidgets를 기반으로 합니다.','네이티브 위젯을 활용합니다.','교과서 48쪽 4'),
('Qt의 공식 Python 바인딩은?','PySide6',['Flask','NumPy','PySide6','Pillow','Scrapy'],'Qt for Python의 구성 요소입니다.','PyQt6와 별도의 프로젝트입니다.','보강'),
('IDLE 구현에 사용된 GUI 라이브러리는?','tkinter',['Kivy','tkinter','Django','Flask','Pygame'],'파이썬의 기본 개발 환경입니다.','실제 프로그램의 tkinter 활용 사례입니다.','교과서 46·55쪽'),
('배치 관리자가 아닌 것은?','center()',['pack()','grid()','place()','center()','QGridLayout'],'tkinter에서 제공하는 이름인지 확인하세요.','center()는 tkinter 배치 관리자가 아닙니다. QGridLayout은 Qt 레이아웃입니다.','교과서 59쪽 6 연계'),
('버튼 command=say_hello의 실행 시점은?','버튼을 클릭할 때',['버튼 생성 전','항상 실행하지 않음','버튼을 클릭할 때','창 제목 변경 때','import 때'],'괄호가 없으므로 함수 자체를 전달했습니다.','이벤트 발생 때 콜백을 호출합니다.','교과서 59쪽 5'),
('UI의 정의에 가장 가까운 것은?','사용자와 시스템이 상호 작용하는 접점',['DB 테이블 구조','운영체제 설치 절차','내부 계산식만','사용자와 시스템이 상호 작용하는 접점','CPU 명령 집합'],'사용자가 보고 조작하는 요소입니다.','화면 구성·입력·피드백을 포함합니다.','교과서 58쪽 3')]: choice(2,'ui',p,a,opts,h,e,ref)
widgets=[('설명 글자 표시','Label','QLabel'),('클릭 명령','Button','QPushButton'),('한 줄 입력','Entry','QLineEdit'),('여러 줄 텍스트','Text','QPlainTextEdit'),('독립 선택','Checkbutton','QCheckBox'),('그룹 중 하나 선택','Radiobutton','QRadioButton'),('항목 목록','Listbox','QListWidget'),('컨테이너','Frame','QWidget')]
for desc,tk,qt in widgets:
 blank(2,'widgets',f'tkinter에서 {desc}에 사용하는 위젯 이름은?',tk,'위젯 도감에서 역할을 확인하세요.',f'{tk}는 {desc}을 담당합니다.','교과서 50쪽 연계')
 blank(2,'pyside',f'{tk}의 {desc} 역할을 Qt Widgets로 옮기면?',qt,'이름은 대문자 Q로 시작합니다.',f'이번 예제에서는 {qt}로 개념을 연결합니다.')
for p,a,h,e,ref in [
('tkinter 기본 창을 만드는 호출은?','tk.Tk()','tkinter as tk로 임포트했습니다.','Tk 인스턴스가 루트 창입니다.','교과서 51·58쪽'),
('tkinter에서 그림과 도형을 그릴 위젯 이름은?','Canvas','그림을 그리는 바탕입니다.','create_oval 같은 메서드로 그립니다.','교과서 50쪽'),
('라벨을 순서대로 배치하려면 label.____()의 빈칸은?','pack','위젯을 생성한 뒤 배치합니다.','생성만 해서는 화면에 배치되지 않습니다.','교과서 59쪽 7'),
('행과 열을 지정하는 tkinter 배치 메서드는?','grid','row와 column을 받습니다.','폼과 격자 구성에 유용합니다.','교과서 51쪽'),
('좌표로 배치하는 tkinter 메서드는?','place','x와 y를 지정합니다.','창 크기 변화도 고려해야 합니다.','교과서 51쪽'),
('btn = tk.Button(root, command=____)에 함수 greet를 연결하세요.','greet','지금 실행하지 않습니다.','함수 자체를 전달하므로 괄호를 붙이지 않습니다.','보강'),
('button.clicked.connect(____)에 함수 greet를 연결하세요.','greet','Qt에서도 함수 자체를 전달합니다.','시그널에 콜백을 연결합니다.','보강'),
('tkinter 이벤트 루프 호출은?','root.mainloop()','루트 변수 이름은 root입니다.','사용자 이벤트를 기다립니다.','교과서 54쪽'),
('Qt 이벤트 루프 호출은?','app.exec()','QApplication 이름은 app입니다.','show 후 이벤트 루프를 시작합니다.','보강'),
('tkinter Text의 처음 위치 문자열은?','1.0','줄은 1, 문자는 0부터 셉니다.','첫 줄의 첫 위치입니다.','교과서 53쪽'),
('tkinter Text의 마지막 자동 개행을 빼고 읽는 끝 위치는?','end-1c','끝에서 문자 하나를 제외합니다.','저장할 때 불필요한 개행 누적을 줄입니다.','보강'),
('Qt 텍스트 편집기의 내용을 문자열로 읽는 메서드는?','toPlainText()','서식 없는 텍스트를 반환합니다.','QPlainTextEdit의 메서드입니다.','보강')]: blank(2,'기본 코드',p,a,h,e,ref)
for p,a,h,e in [
('command=hello()에서 의도하지 않은 즉시 호출을 고치세요.','command=hello','괄호를 제거하세요.','함수를 전달해야 클릭 때 실행됩니다.'),
('button.clicked.connect(hello())를 고치세요.','button.clicked.connect(hello)','connect가 받을 것은 호출 가능한 객체입니다.','함수의 반환값을 전달하지 마세요.'),
('editor.text()를 QPlainTextEdit에 맞게 고치세요.','editor.toPlainText()','QLineEdit와 메서드가 다릅니다.','위젯 종류에 따라 읽기 API가 다릅니다.'),
('label.text = "완료"를 QLabel에 맞게 고치세요.','label.setText("완료")','속성을 새로 만드는 대신 메서드를 호출합니다.','setText가 실제 표시 문자열을 바꿉니다.'),
('QFileDialog.getOpenFileName 결과를 path 하나로 받았습니다. 두 값을 받는 왼쪽 코드를 쓰세요.','path, _','경로와 필터의 튜플입니다.','선택 필터를 사용하지 않으면 _로 받을 수 있습니다.'),
('tkinter Text에서 기존 내용을 제거하는 코드는?','text_area.delete("1.0", tk.END)','새 파일을 열기 전에 이전 내용을 지웁니다.','insert만 하면 기존 텍스트에 덧붙게 됩니다.'),
('Tk 입력창 entry의 한 줄 값을 읽는 코드는?','entry.get()','get 메서드를 사용합니다.','Entry는 Text와 달리 위치 인자가 필요 없습니다.'),
('Qt 입력창 entry의 한 줄 값을 읽는 코드는?','entry.text()','QLineEdit입니다.','QPlainTextEdit와 구분하세요.')]: q(2,'오류 찾기','빈칸',p,a,h,e)
q(2,'memo','순서','파일 열기 처리를 순서대로 배열하세요.',['파일 선택 대화 상자','취소 여부 확인','UTF-8로 파일 읽기','기존 텍스트 지우기','새 텍스트 넣기'],'취소했을 때 빈 경로를 열면 안 됩니다.','읽기에 성공한 뒤 기존 내용을 바꿉니다.','',ref='교과서 53쪽 연계')
q(2,'pyside','순서','Qt 앱의 기본 실행 순서를 배열하세요.',['QApplication 생성','창과 레이아웃 생성','위젯과 이벤트 연결','window.show()','app.exec()'],'앱 객체가 위젯보다 먼저 필요합니다.','화면을 보여준 뒤 이벤트 루프를 실행합니다.')
q(2,'memo','순서','저장 순서를 배열하세요.',['저장 경로 선택','취소 여부 확인','편집기 텍스트 읽기','UTF-8로 파일 쓰기'],'사용자가 경로를 선택해야 합니다.','대화 상자 취소 시 쓰기를 건너뜁니다.')
q(2,'layout','순서','격자 폼을 만드는 흐름을 배열하세요.',['부모 Frame 생성','Label과 Entry 생성','grid로 행·열 지정','열 확장 weight 지정','창 크기 변경 시험'],'부모와 자식 관계부터 정합니다.','레이아웃은 크기 변화에서도 시험합니다.')
for p,a,opts,h,e in [
('한 부모 안에서 pack과 grid를 섞으면?','배치 충돌 오류가 날 수 있습니다.',['항상 자동 변환됩니다.','배치 충돌 오류가 날 수 있습니다.','Tk가 Qt로 바뀝니다.','텍스트만 사라집니다.','항상 잘 동작합니다.'],'다른 Frame으로 나누면 됩니다.','동일 부모 안에서 혼용하지 않습니다.'),
('파일 대화 상자를 취소했다면?','함수에서 돌아갑니다.',['빈 경로를 엽니다.','파일을 삭제합니다.','함수에서 돌아갑니다.','아무 파일이나 저장합니다.','텍스트를 무조건 지웁니다.'],'경로가 빈 값인지 검사합니다.','기존 내용을 유지해야 합니다.'),
('긴 time.sleep을 GUI 콜백에서 실행하면?','화면 반응이 멈출 수 있습니다.',['자동으로 병렬 실행됩니다.','더 부드러워집니다.','화면 반응이 멈출 수 있습니다.','창 크기가 커집니다.','코드가 저장됩니다.'],'이벤트 루프가 기다립니다.','타이머와 작업 분리를 고려합니다.'),
('Designer 생성 파일을 직접 수정할 때의 문제는?','재생성하면 변경이 사라질 수 있습니다.',['절대로 실행되지 않습니다.','재생성하면 변경이 사라질 수 있습니다.','Qt가 삭제됩니다.','Python 버전이 바뀝니다.','파일이 이미지가 됩니다.'],'생성 코드와 작성 코드를 나눕니다.','직접 작성한 main에서 이벤트를 연결하세요.'),
('웹 GUI 체험 화면의 의미는?','예제 동작을 재현한 학습용 시뮬레이션',['임의의 PySide 코드를 실제 실행','PC 모든 파일에 접근','예제 동작을 재현한 학습용 시뮬레이션','실행 검증이 모두 완료됨','운영체제 자체'],'실제 실행은 PC에서 확인합니다.','웹 코드 확인과 실제 GUI 검증을 구분합니다.'),
('QMainWindow에 편집기를 넣는 방식은?','setCentralWidget(editor)',['window.pack()','setCentralWidget(editor)','window.grid()','editor.mainloop()','app.setText(editor)'],'메인 창의 중앙 영역입니다.','메뉴와 상태 표시줄 외의 중앙 위젯을 지정합니다.')]: choice(2,'응용 판단',p,a,opts,h,e)
# GUI-independent functions: genuinely runnable web tests.
coding(2,'events','빈 이름에는 "여러분"을 사용하는 인사 함수를 작성하세요.','def greeting(name):\n    pass','def greeting(name):\n    return f"{name.strip() or \'여러분\'}님, 안녕하세요!"','assert greeting(" 민지 ")=="민지님, 안녕하세요!"\nassert greeting(" ")=="여러분님, 안녕하세요!"','입력 정리를 GUI 밖의 함수로 만듭니다.','입력 공백과 빈 이름을 검사합니다.')
coding(2,'memo','텍스트의 글자 수와 줄 수를 튜플로 반환하세요. 빈 문서는 (0,0)입니다.','def stats(text):\n    pass','def stats(text):\n    return len(text), len(text.splitlines())','assert stats("")==(0,0)\nassert stats("가나\\n다")== (4,2)\nassert stats("가\\n")== (2,1)','splitlines로 줄을 구분합니다.','이 과제는 마지막 개행 뒤의 빈 줄을 추가 줄로 세지 않습니다.')
coding(2,'project','추첨 인원 문자열을 1~total의 정수로 검사하세요. 잘못된 값은 None입니다.','def parse_count(text,total):\n    pass','def parse_count(text,total):\n    try:\n        n=int(text)\n        return n if 1<=n<=total else None\n    except ValueError:\n        return None','assert parse_count("2",3)==2\nassert parse_count("0",3) is None\nassert parse_count("x",3) is None\nassert parse_count("4",3) is None','변환 오류와 범위 오류를 나누세요.','GUI의 경고 표시와 검증 로직을 분리합니다.')
coding(2,'memo','저장 취소인 빈 경로에는 False, 유효 경로에는 True를 반환하세요.','def should_save(path):\n    return True','def should_save(path):\n    return bool(path)','assert should_save("") is False\nassert should_save("memo.txt") is True','빈 경로는 false로 평가됩니다.','취소했을 때 파일 작업을 건너뛰게 합니다.','오류 수정')
coding(2,'events','상태 n을 1 증가시키되 최대 10을 넘지 않게 하세요.','def increment(n):\n    return n+1','def increment(n):\n    return min(n+1,10)','assert increment(0)==1\nassert increment(9)==10\nassert increment(10)==10','버튼 연속 클릭의 경계를 생각하세요.','UI 상태에도 경계 조건 검사가 필요합니다.','오류 수정')
coding(2,'memo','제목에 미저장 표시 *를 붙이는 함수를 작성하세요.','def title(name,modified):\n    pass','def title(name,modified):\n    return ("* " if modified else "")+name','assert title("메모장",True)=="* 메모장"\nassert title("메모장",False)=="메모장"','불리언 상태에 따라 접두어를 선택합니다.','같은 함수를 두 GUI에서 사용할 수 있습니다.')
written(2,'ui','GUI의 장점과 CLI가 더 편리할 수 있는 상황을 설명하세요.','GUI는 조작 대상을 시각적으로 보여줍니다. 반복 파일 작업은 CLI 명령과 자동화가 효율적일 수 있습니다.','사용자와 작업 목적을 함께 생각하세요.','한 방식이 언제나 우월하다고 단정하지 마세요.','교과서 42·48쪽')
written(2,'ui','NUI를 설명하고 사례를 하나 적으세요.','음성·손짓 같은 자연스러운 행동을 통해 상호 작용하는 방식입니다. 음성으로 스피커에 음악 재생을 요청하는 것이 예입니다.','입력 수단을 구체적으로 적으세요.','정의와 사례가 일치하는지 확인하세요.','교과서 48쪽 3')
written(2,'project','모듈 구조·이벤트·입력 오류 처리의 구현 근거를 작성하세요.','core에서 계산을 담당하고 GUI는 입력·표시를 맡습니다. 버튼에 함수를 연결하고 잘못된 값을 경고로 안내합니다.','실제 파일명과 시험 입력을 포함하세요.','기능, 구조, 저널을 평가 기준에 연결하세요.')
written(2,'libraries','학교용 메모장의 라이브러리를 선택하고 이유를 설명하세요.','tkinter는 설치 환경이 갖추어져 있으면 작은 앱을 빠르게 만들 수 있습니다. PySide6는 풍부한 위젯과 Designer가 필요한 확장 앱에 적합합니다.','설치·사용자·필요 기능을 근거로 삼으세요.','취향만이 아니라 프로젝트 조건을 설명하세요.','교과서 46쪽 탐구')
choice(1,'thirdparty','관계형 데이터베이스를 객체 형태로 다루는 경량 ORM은?','Peewee',['Peewee','Pillow','Pygame','Kivy','math'],'교과서의 패키지 목록을 확인하세요.','Peewee는 데이터베이스 모델과 쿼리를 Python 객체로 다루도록 돕습니다.','교과서 33쪽')
blank(2,'widgets','57쪽 IDLE 코드에서 Frame과 Button 같은 요소를 통칭하는 말은?','위젯','화면의 구성 요소입니다.','위젯마다 표시·입력·컨테이너 역할이 있습니다.','교과서 57쪽')
blank(2,'pyside','QLineEdit의 입력 변화 시그널 이름은?','textChanged','text 뒤에 Changed가 옵니다.','입력 변화에 따라 미리보기나 검증을 연결할 수 있습니다.')
blank(2,'pyside','Qt Designer 실행 명령은?','pyside6-designer','PySide6 가상환경을 활성화하세요.','폼을 시각적으로 배치하고 .ui로 저장합니다.')
written(2,'ui','UI가 사용자 편의성과 어떤 관련이 있는지 설명하세요.','찾기 쉬운 버튼, 읽기 쉬운 글자, 명확한 피드백은 작업 시간과 실수를 줄입니다.','구체적인 화면 요소 하나를 근거로 드세요.','UI 요소와 실제 사용 효과를 연결하세요.','교과서 58쪽 2')
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\nprint(len(calls))','0','함수를 저장하는 것과 호출하는 것은 다릅니다.','callback()을 호출해야 리스트가 바뀝니다.')
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\ncallback()\ncallback()\nprint(len(calls))','2','콜백을 두 번 호출했습니다.','GUI 클릭도 연결된 함수를 호출하는 사건입니다.')
