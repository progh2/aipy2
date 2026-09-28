from content import q, questions
# Carefully authored tasks; execution checks accept equivalent implementations.
def choice(u,t,p,a,opts,h,e,ref='보강',level='기본',qid=None): q(u,t,'선택',p,a,h,e,options=opts,ref=ref,level=level,qid=qid)
def blank(u,t,p,a,h,e,ref='보강',level='기본',qid=None): q(u,t,'빈칸',p,a,h,e,ref=ref,level=level,qid=qid)
def written(u,t,p,a,h,e,ref='보강',level='기본',qid=None): q(u,t,'서술',p,a,h,e,ref=ref,level=level,qid=qid)
def coding(u,t,p,s,a,test,h,e,kind='구현',level='기본',qid=None): q(u,t,kind,p,a,h,e,starter=s,checks=test,level=level,qid=qid)
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

# Unit 2 (#131 전면 재편): pyside/wx/kivy 세부 문항 삭제, 뻔한 문항을
# 코드 판단형으로 상향, 교과서 확인 학습·종합 평가 원문을 모두 포함한다.
# 유지 문항은 원래 qid 그대로 두고(question_hints.json 지문 일치 필수),
# 수정·신규 문항은 u2-q101부터 새 번호를 쓴다.

# -- libraries: GUI 라이브러리 비교(45~48쪽). tkinter/wxPython/Kivy는 교과서
#    범위이지만 PySide6는 교과서에 없으므로 삭제(구 q004), wxPython/IDLE
#    문항은 유지한다.
choice(2,'libraries','운영체제 고유 위젯을 활용하는 라이브러리는?','wxPython',['tkinter','PyQt6','wxPython','Kivy','Django'],'wxWidgets를 기반으로 합니다.','네이티브 위젯을 활용합니다.','교과서 48쪽 4',qid='u2-q003')
choice(2,'libraries','IDLE 구현에 사용된 GUI 라이브러리는?','tkinter',['Kivy','tkinter','Django','Flask','Pygame'],'파이썬의 기본 개발 환경입니다.','실제 프로그램의 tkinter 활용 사례입니다.','교과서 46·55쪽',qid='u2-q005')

# -- events: 버튼 콜백의 실행 시점(51·54쪽).
choice(2,'events','버튼 command=say_hello의 실행 시점은?','버튼을 클릭할 때',['버튼 생성 전','항상 실행하지 않음','버튼을 클릭할 때','창 제목 변경 때','import 때'],'괄호가 없으므로 함수 자체를 전달했습니다.','이벤트 발생 때 콜백을 호출합니다.','교과서 51·54쪽 연계',qid='u2-q007')

# -- widgets: tkinter 위젯 이름 8종(50쪽 표). Qt 대응 문항(pyside)은 삭제.
widgets=[('설명 글자 표시','Label'),('클릭 명령','Button'),('한 줄 입력','Entry'),('여러 줄 텍스트','Text'),('독립 선택','Checkbutton'),('그룹 중 하나 선택','Radiobutton'),('항목 목록','Listbox'),('컨테이너','Frame')]
for i,(desc,tk) in enumerate(widgets):
 blank(2,'widgets',f'tkinter에서 {desc}에 사용하는 위젯 이름은?',tk,'위젯 도감에서 역할을 확인하세요.',f'{tk}는 {desc}을 담당합니다.','교과서 50쪽 연계',qid=f'u2-q{9+2*i:03}')
blank(2,'widgets','tkinter에서 그림과 도형을 그릴 위젯 이름은?','Canvas','그림을 그리는 바탕입니다.','create_oval 같은 메서드로 그립니다.','교과서 50쪽',qid='u2-q026')

# -- layout: pack/grid/place(51쪽).
blank(2,'layout','행과 열을 지정하는 tkinter 배치 메서드는?','grid','row와 column을 받습니다.','폼과 격자 구성에 유용합니다.','교과서 51쪽',qid='u2-q028')
blank(2,'layout','좌표로 배치하는 tkinter 메서드는?','place','x와 y를 지정합니다.','창 크기 변화도 고려해야 합니다.','교과서 51쪽',qid='u2-q029')

# -- events: 콜백 연결 문법(보강)과 이벤트 루프(54쪽).
blank(2,'events','btn = tk.Button(root, command=____)에 함수 greet를 연결하세요.','greet','지금 실행하지 않습니다.','함수 자체를 전달하므로 괄호를 붙이지 않습니다.',qid='u2-q030')
blank(2,'events','tkinter 이벤트 루프 호출은?','root.mainloop()','루트 변수 이름은 root입니다.','사용자 이벤트를 기다립니다.','교과서 54쪽',qid='u2-q032')

# -- memo: Text 위젯 인덱스(53쪽).
blank(2,'memo','tkinter Text의 처음 위치 문자열은?','1.0','줄은 1, 문자는 0부터 셉니다.','첫 줄의 첫 위치입니다.','교과서 53쪽',qid='u2-q034')
blank(2,'memo','tkinter Text의 마지막 자동 개행을 빼고 읽는 끝 위치는?','end-1c','끝에서 문자 하나를 제외합니다.','저장할 때 불필요한 개행 누적을 줄입니다.',level='심화',qid='u2-q035')

# -- events: command=hello() 즉시 호출 오류(51쪽 개념의 흔한 오개념).
blank(2,'events','command=hello()에서 의도하지 않은 즉시 호출을 고치세요.','command=hello','괄호를 제거하세요.','함수를 전달해야 클릭 때 실행됩니다.',qid='u2-q037')
# -- memo: 파일 열기 코드(52쪽)의 delete 라인 그대로.
blank(2,'memo','tkinter Text에서 기존 내용을 제거하는 코드는?','text_area.delete("1.0", tk.END)','새 파일을 열기 전에 이전 내용을 지웁니다.','insert만 하면 기존 텍스트에 덧붙게 됩니다.',qid='u2-q042')
# -- widgets: Entry.get()은 교과서 표 밖 심화 보강.
blank(2,'widgets','Tk 입력창 entry의 한 줄 값을 읽는 코드는?','entry.get()','get 메서드를 사용합니다.','Entry는 Text와 달리 위치 인자가 필요 없습니다.',level='심화',qid='u2-q043')

# -- memo: 파일 열기·저장 순서(52~53쪽 코드 그대로).
q(2,'memo','순서','파일 열기 처리를 순서대로 배열하세요.',['파일 선택 대화 상자','취소 여부 확인','UTF-8로 파일 읽기','기존 텍스트 지우기','새 텍스트 넣기'],'취소했을 때 빈 경로를 열면 안 됩니다.','읽기에 성공한 뒤 기존 내용을 바꿉니다.','',ref='교과서 53쪽 연계',qid='u2-q045')
q(2,'memo','순서','저장 순서를 배열하세요.',['저장 경로 선택','취소 여부 확인','편집기 텍스트 읽기','UTF-8로 파일 쓰기'],'사용자가 경로를 선택해야 합니다.','대화 상자 취소 시 쓰기를 건너뜁니다.',qid='u2-q047')

# -- 응용 판단(layout/memo/events): GUI 배치·파일·반응성 적용 문제.
choice(2,'layout','한 부모 안에서 pack과 grid를 섞으면?','배치 충돌 오류가 날 수 있습니다.',['항상 자동 변환됩니다.','배치 충돌 오류가 날 수 있습니다.','Tk가 Qt로 바뀝니다.','텍스트만 사라집니다.','항상 잘 동작합니다.'],'다른 Frame으로 나누면 됩니다.','동일 부모 안에서 혼용하지 않습니다.',qid='u2-q049')
choice(2,'memo','파일 대화 상자를 취소했다면?','함수에서 돌아갑니다.',['빈 경로를 엽니다.','파일을 삭제합니다.','함수에서 돌아갑니다.','아무 파일이나 저장합니다.','텍스트를 무조건 지웁니다.'],'경로가 빈 값인지 검사합니다.','기존 내용을 유지해야 합니다.',qid='u2-q050')
choice(2,'events','긴 time.sleep을 GUI 콜백에서 실행하면?','화면 반응이 멈출 수 있습니다.',['자동으로 병렬 실행됩니다.','더 부드러워집니다.','화면 반응이 멈출 수 있습니다.','창 크기가 커집니다.','코드가 저장됩니다.'],'이벤트 루프가 기다립니다.','타이머와 작업 분리를 고려합니다.',qid='u2-q051')

# GUI-independent functions: genuinely runnable web tests.
coding(2,'events','빈 이름에는 "여러분"을 사용하는 인사 함수를 작성하세요.','def greeting(name):\n    pass','def greeting(name):\n    return f"{name.strip() or \'여러분\'}님, 안녕하세요!"','assert greeting(" 민지 ")=="민지님, 안녕하세요!"\nassert greeting(" ")=="여러분님, 안녕하세요!"','입력 정리를 GUI 밖의 함수로 만듭니다.','입력 공백과 빈 이름을 검사합니다.',qid='u2-q055')
coding(2,'memo','텍스트의 글자 수와 줄 수를 튜플로 반환하세요. 빈 문서는 (0,0)입니다.','def stats(text):\n    pass','def stats(text):\n    return len(text), len(text.splitlines())','assert stats("")==(0,0)\nassert stats("가나\\n다")== (4,2)\nassert stats("가\\n")== (2,1)','splitlines로 줄을 구분합니다.','이 과제는 마지막 개행 뒤의 빈 줄을 추가 줄로 세지 않습니다.',qid='u2-q056')
# project 소단원은 존폐 미정이므로 review로 재배정(내용은 그대로 유지).
coding(2,'review','추첨 인원 문자열을 1~total의 정수로 검사하세요. 잘못된 값은 None입니다.','def parse_count(text,total):\n    pass','def parse_count(text,total):\n    try:\n        n=int(text)\n        return n if 1<=n<=total else None\n    except ValueError:\n        return None','assert parse_count("2",3)==2\nassert parse_count("0",3) is None\nassert parse_count("x",3) is None\nassert parse_count("4",3) is None','변환 오류와 범위 오류를 나누세요.','GUI의 경고 표시와 검증 로직을 분리합니다.',qid='u2-q057')
coding(2,'memo','저장 취소인 빈 경로에는 False, 유효 경로에는 True를 반환하세요.','def should_save(path):\n    return True','def should_save(path):\n    return bool(path)','assert should_save("") is False\nassert should_save("memo.txt") is True','빈 경로는 false로 평가됩니다.','취소했을 때 파일 작업을 건너뛰게 합니다.','오류 수정',qid='u2-q058')
coding(2,'events','상태 n을 1 증가시키되 최대 10을 넘지 않게 하세요.','def increment(n):\n    return n+1','def increment(n):\n    return min(n+1,10)','assert increment(0)==1\nassert increment(9)==10\nassert increment(10)==10','버튼 연속 클릭의 경계를 생각하세요.','UI 상태에도 경계 조건 검사가 필요합니다.','오류 수정',qid='u2-q059')
coding(2,'memo','제목에 미저장 표시 *를 붙이는 함수를 작성하세요.','def title(name,modified):\n    pass','def title(name,modified):\n    return ("* " if modified else "")+name','assert title("메모장",True)=="* 메모장"\nassert title("메모장",False)=="메모장"','불리언 상태에 따라 접두어를 선택합니다.','같은 함수를 두 GUI에서 사용할 수 있습니다.',qid='u2-q060')
written(2,'review','모듈 구조·이벤트·입력 오류 처리의 구현 근거를 작성하세요.','core에서 계산을 담당하고 GUI는 입력·표시를 맡습니다. 버튼에 함수를 연결하고 잘못된 값을 경고로 안내합니다.','실제 파일명과 시험 입력을 포함하세요.','기능, 구조, 저널을 평가 기준에 연결하세요.',qid='u2-q063')
written(2,'ui','UI가 사용자 편의성과 어떤 관련이 있는지 설명하세요.','찾기 쉬운 버튼, 읽기 쉬운 글자, 명확한 피드백은 작업 시간과 실수를 줄입니다.','구체적인 화면 요소 하나를 근거로 드세요.','UI 요소와 실제 사용 효과를 연결하세요.','교과서 58쪽 2',qid='u2-q068')
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\nprint(len(calls))','0','함수를 저장하는 것과 호출하는 것은 다릅니다.','callback()을 호출해야 리스트가 바뀝니다.',qid='u2-q069')
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\ncallback()\ncallback()\nprint(len(calls))','2','콜백을 두 번 호출했습니다.','GUI 클릭도 연결된 함수를 호출하는 사건입니다.',qid='u2-q070')

choice(1,'thirdparty','관계형 데이터베이스를 객체 형태로 다루는 경량 ORM은?','Peewee',['Peewee','Pillow','Pygame','Kivy','math'],'교과서의 패키지 목록을 확인하세요.','Peewee는 데이터베이스 모델과 쿼리를 Python 객체로 다루도록 돕습니다.','교과서 33쪽')

# -- 신규(#131): 교과서 확인 학습(48·57쪽)·종합 평가(58~59쪽) 원문 그대로 +
# 라이브러리 선택 서술 재작성(PySide6 언급 삭제).
choice(2,'ui','다음 중 사용자 인터페이스(User Interface)의 설명으로 옳지 않은 것은?','CLI는 직관적인 그래픽 환경을 제공하는 인터페이스이다.',['UI의 구성 요소에는 버튼, 색상, 입력창 등이 포함된다.','CLI는 직관적인 그래픽 환경을 제공하는 인터페이스이다.','UI는 사용자가 컴퓨터와 상호 작용하는 모든 요소를 포함한다.','GUI는 마우스나 터치로 화면의 버튼이나 메뉴를 조작할 수 있다.','NUI는 음성, 제스처 등 자연스러운 방식으로 컴퓨터와 상호 작용할 수 있다.'],'CLI의 C는 Command(명령어)입니다.','그래픽 환경으로 조작하는 것은 GUI의 특징입니다.','교과서 48쪽 1',qid='u2-q101')
written(2,'ui','GUI 프로그래밍을 하면 어떤 장점이 있는지 서술하시오.','사용자가 마우스나 버튼으로 프로그램을 쉽게 조작할 수 있고, 텍스트 기반 CLI보다 직관적이고 시각적이다.','명령어를 몰라도 사용할 수 있다는 점을 떠올리세요.','마우스·터치 조작과 시각적 피드백을 함께 언급하세요.','교과서 48쪽 2·정답 202쪽',qid='u2-q102')
written(2,'ui','NUI 프로그래밍이 무엇인지 서술하시오.','음성, 손짓, 터치, 눈동자 움직임 등 사람의 자연스러운 신체 동작을 이용해 컴퓨터와 상호 작용할 수 있도록 만드는 프로그램 개발 방식이다. 별도의 조작법을 배우지 않아도 직관적으로 사용할 수 있다.','자연스러운 신체 동작이 핵심 키워드입니다.','별도 학습이 필요 없다는 점과 스마트 기기 사례를 함께 적으세요.','교과서 48쪽 3·정답 202쪽',qid='u2-q103')
written(2,'libraries','아래의 GUI 라이브러리와 설명을 바르게 연결하시오.\n① tkinter  ② PyQt  ③ wxPython  ④ Kivy\n㉠ 멀티 플랫폼, 터치 중심 GUI 프레임워크  ㉡ 운영체제 네이티브 스타일 제공  ㉢ C++ Qt 기반, 상업용 앱에도 적합  ㉣ 파이썬 기본 GUI 라이브러리','①-㉣, ②-㉢, ③-㉡, ④-㉠','tkinter는 설치가 필요 없는 기본 라이브러리입니다.','wxPython은 운영체제 고유(네이티브) 위젯을 사용합니다.','교과서 48쪽 4',qid='u2-q104')
choice(2,'widgets','다음 중 Tkinter의 GUI 창을 생성하는 객체는 무엇인지 골라 보자.','Tk()',['Tk()','Entry()','Frame()','Label()','Button()'],'루트 창(root window)을 만드는 클래스입니다.','다른 보기는 모두 위젯이며 창 자체가 아닙니다.','교과서 51쪽',qid='u2-q105')
blank(2,'memo','다음은 IDLE에서 macOS와 관련된 macosx.py 코드의 일부이다. 빈칸에 공통으로 들어갈 모듈 이름을 쓰세요.\nimport ____\n\ndef _init_tk_type():\n    global _tk_type\n    if platform == \'darwin\':\n        root = ____.Tk()','tkinter','root.Tk()를 만들 수 있는 모듈입니다.','이 단원에서 계속 사용해 온 GUI 기본 라이브러리입니다.','교과서 55쪽',qid='u2-q106')
written(2,'widgets','다음은 56쪽 디버거 GUI 코드의 일부이다. ①·②·③에 들어갈 말을 각각 쓰세요.\nfrom tkinter import *\nfrom tkinter.ttk import ① , Scrollbar\n...\nself.bframe = bframe = ① (top)\n...\nself.bcont = b = ② (bframe, text="Go", command=self.cont)\n...\n①과 ②처럼 사용자와 상호 작용하는 인터페이스 요소를 ③이라 한다.','① Frame ② Button ③ 위젯','①은 여러 위젯을 묶는 컨테이너, ②는 클릭 버튼입니다.','①·②를 모두 포함하는 상위 개념이 ③입니다.','교과서 57쪽',qid='u2-q107')
blank(2,'widgets','tkinter에서 GUI 창을 생성할 때 사용하는 기본 객체는 무엇인가?','Tk() 객체','tk.Tk()로 만듭니다.','이 객체가 프로그램의 기본 창(root window)입니다.','교과서 58쪽 1',qid='u2-q108')
choice(2,'ui','다음 중 사용자 인터페이스(User Interface)의 정의로 가장 적절한 것은?','사용자와 기계가 상호 작용하는 기능의 집합',['프로그램의 내부 동작 방식','데이터베이스를 설계하는 구조','컴퓨터의 운영체제를 설치하는 방식','사용자가 명령어를 작성하는 개발 환경','사용자와 기계가 상호 작용하는 기능의 집합'],'UI의 정의를 떠올리세요.','특정 기술(DB·OS 설치·개발 환경)이 아니라 상호 작용 자체를 가리킵니다.','교과서 58쪽 3',qid='u2-q109')
choice(2,'ui','다음 상황은 어떤 인터페이스에 해당하는가?\n"아이콘을 클릭해서 그림판을 열었어요."','GUI',['CLI','GUI','NUI','API','TUI'],'아이콘을 마우스로 클릭했습니다.','그래픽 요소를 조작하는 방식입니다.','교과서 58쪽 4',qid='u2-q110')
choice(2,'events','보기 코드의 실행 결과로 올바른 것을 고르시오.\nimport tkinter as tk\n\ndef say_hello():\n    print("안녕하세요")\n\nwindow = tk.Tk()\nbtn = tk.Button(window, text="클릭", command=say_hello)\nbtn.pack()\nwindow.mainloop()','"클릭" 버튼이 보이고, 누르면 "안녕하세요"가 출력된다.',['PyQT를 사용하였다.','코드는 에러가 발생한다.','버튼을 누르면 창이 닫힌다.','창만 뜨고 버튼은 보이지 않는다.','"클릭" 버튼이 보이고, 누르면 "안녕하세요"가 출력된다.'],'btn.pack()으로 버튼이 화면에 배치됩니다.','command=say_hello는 클릭했을 때 함수를 호출합니다.','교과서 58쪽 5',qid='u2-q111')
choice(2,'layout','다음 중 tkinter의 배치 방식과 설명이 올바르게 연결되지 않은 것은?','center() – 위젯을 화면 중앙에 자동 배치한다.',['grid() – 행과 열 기준으로 위젯을 배치한다.','center() – 위젯을 화면 중앙에 자동 배치한다.','place() – 좌표를 직접 지정해 위젯을 배치한다.','pack() – 기본적으로 많이 사용되는 배치 방식이다.','pack() – 위에서 아래로 순차적으로 위젯을 배치한다.'],'tkinter의 배치 관리자는 pack·grid·place 세 가지입니다.','center()라는 배치 관리자는 tkinter에 없습니다.','교과서 59쪽 6',level='심화',qid='u2-q112')
choice(2,'layout','다음 빈칸에 들어갈 코드로 적절한 것은?\nimport tkinter as tk\nwindow = tk.Tk()\nlabel = tk.Label(window, text="안녕하세요")\nlabel.____\n\nwindow.mainloop()','pack()',['click()','draw()','pack()','open()','show()'],'위젯은 생성만으로는 화면에 나타나지 않습니다.','배치 관리자 메서드를 호출해야 화면에 보입니다.','교과서 59쪽 7',qid='u2-q113')
written(2,'libraries','학교용 메모장을 만든다면 tkinter, PyQt, wxPython, Kivy 중 어떤 라이브러리를 선택할지 고르고 이유를 설명하세요.','tkinter를 선택한다. 별도 설치 없이 기본 제공되어 간단한 메모장을 빠르게 만들 수 있고, 학교 실습 환경에서 설치 문제 없이 바로 사용할 수 있다.','설치 여부와 프로그램의 규모를 함께 생각하세요.','간단한 학습용 앱인지 상업용 앱인지에 따라 적합한 라이브러리가 다릅니다.','교과서 46쪽 탐구',qid='u2-q114')
