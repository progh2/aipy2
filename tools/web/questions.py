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

# -- events: 콜백 연결 문법(코드 완성 — 이미 코드가 제시되는 형태라 유지).
#    grid()/place()/mainloop() 이름 암기 문항(구 q028·029·032)은 삭제하고
#    새 코드 예측·오류 찾기(u2-q117·118·121·123·132)로 대체한다.
blank(2,'events','btn = tk.Button(root, command=____)에 함수 greet를 연결하세요.','greet','지금 실행하지 않습니다.','함수 자체를 전달하므로 괄호를 붙이지 않습니다.',qid='u2-q030')

# -- memo: Text 위젯 인덱스(53쪽).
blank(2,'memo','tkinter Text의 마지막 자동 개행을 빼고 읽는 끝 위치는?','end-1c','끝에서 문자 하나를 제외합니다.','저장할 때 불필요한 개행 누적을 줄입니다.',level='심화',qid='u2-q035')

# -- events: command=hello() 즉시 호출 오류(51쪽 개념의 흔한 오개념). 클릭 없이
#    미리 실행돼 버리는 사례라 실제로 판단이 필요해 심화로 올린다.
blank(2,'events','command=hello()에서 의도하지 않은 즉시 호출을 고치세요.','command=hello','괄호를 제거하세요.','함수를 전달해야 클릭 때 실행됩니다.',level='심화',qid='u2-q037')
# -- memo: 파일 열기 코드(52쪽)의 delete 라인 그대로.
blank(2,'memo','tkinter Text에서 기존 내용을 제거하는 코드는?','text_area.delete("1.0", tk.END)','새 파일을 열기 전에 이전 내용을 지웁니다.','insert만 하면 기존 텍스트에 덧붙게 됩니다.',qid='u2-q042')

# -- memo: 파일 열기·저장 순서(52~53쪽 코드 그대로).
q(2,'memo','순서','파일 열기 처리를 순서대로 배열하세요.',['파일 선택 대화 상자','취소 여부 확인','UTF-8로 파일 읽기','기존 텍스트 지우기','새 텍스트 넣기'],'취소했을 때 빈 경로를 열면 안 됩니다.','읽기에 성공한 뒤 기존 내용을 바꿉니다.','',ref='교과서 53쪽 연계',level='심화',qid='u2-q045')
q(2,'memo','순서','저장 순서를 배열하세요.',['저장 경로 선택','취소 여부 확인','편집기 텍스트 읽기','UTF-8로 파일 쓰기'],'사용자가 경로를 선택해야 합니다.','대화 상자 취소 시 쓰기를 건너뜁니다.',level='심화',qid='u2-q047')

written(2,'ui','UI가 사용자 편의성과 어떤 관련이 있는지 설명하세요.','찾기 쉬운 버튼, 읽기 쉬운 글자, 명확한 피드백은 작업 시간과 실수를 줄입니다.','구체적인 화면 요소 하나를 근거로 드세요.','UI 요소와 실제 사용 효과를 연결하세요.','교과서 58쪽 2',qid='u2-q068')
# -- events: 콜백 참조 vs 호출 예측(코드 예측형 — #131 후속 피드백에서 우수 사례로 지목되어 계열을 늘렸다).
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\nprint(len(calls))','0','함수를 저장하는 것과 호출하는 것은 다릅니다.','callback()을 호출해야 리스트가 바뀝니다.',qid='u2-q069')
q(2,'events','예측','calls=[]\ndef hello():\n    calls.append("인사")\ncallback=hello\ncallback()\ncallback()\nprint(len(calls))','2','콜백을 두 번 호출했습니다.','GUI 클릭도 연결된 함수를 호출하는 사건입니다.',level='심화',qid='u2-q070')

choice(1,'thirdparty','관계형 데이터베이스를 객체 형태로 다루는 경량 ORM은?','Peewee',['Peewee','Pillow','Pygame','Kivy','math'],'교과서의 패키지 목록을 확인하세요.','Peewee는 데이터베이스 모델과 쿼리를 Python 객체로 다루도록 돕습니다.','교과서 33쪽')

# -- #131 후속(코디네이터 피드백): 뻔한 암기·허수 보기·GUI와 무관한 순수
# 함수형 문항을 코드 제시형(예측·오류 찾기·코드 완성)으로 교체한다. 아래
# tkinter 동작은 모두 `xvfb-run -a python3`으로 직접 실행해 확인했다
# (문항 옆 ref에 '실행 검증'으로 표시). 위젯 9종의 단순 이름 암기는
# '상황 → 위젯' 매칭 2문항으로 압축한다.
written(2,'widgets','메모장 화면에 다음 요소가 필요하다. 각 요소에 알맞은 tkinter 위젯 이름을 쓰세요.\n① 설명 문구만 보여 주고 입력은 받지 않는 안내 글자\n② 사용자가 누르면 저장 동작이 실행되는 버튼\n③ 이름처럼 한 줄짜리 값을 입력받는 칸\n④ 메모 내용처럼 여러 줄을 입력·표시하는 칸\n⑤ 여러 위젯을 하나로 묶는 컨테이너','① Label ② Button ③ Entry ④ Text ⑤ Frame','표시용인지 입력용인지, 한 줄인지 여러 줄인지 구분하세요.','컨테이너는 다른 위젯을 그룹으로 묶을 때 씁니다.','교과서 50쪽',qid='u2-q115')
written(2,'widgets','설정 화면에 다음 요소가 필요하다. 각 요소에 알맞은 tkinter 위젯 이름을 쓰세요.\n① 자동 저장 여부처럼 여러 옵션을 각각 독립적으로 켜고 끄는 요소\n② 글꼴 크기처럼 여러 선택지 중 하나만 고르게 하는 요소\n③ 최근에 연 파일처럼 여러 항목을 목록으로 나열해 그중 하나를 고르는 요소\n④ 그림이나 도형을 직접 그릴 수 있는 공간','① Checkbutton ② Radiobutton ③ Listbox ④ Canvas','체크 박스와 라디오 버튼의 차이는 동시에 여러 개를 고를 수 있는지입니다.','목록에서 고르는 것과 그림을 그리는 것은 서로 다른 위젯입니다.','교과서 50쪽',qid='u2-q116')
q(2,'layout','예측','import tkinter as tk\nroot = tk.Tk()\ntk.Label(root, text="A").pack()\ntk.Label(root, text="B").pack()\ntk.Label(root, text="C").pack()\nroot.mainloop()','A, B, C 순서로 위에서 아래로 쌓인다','pack()의 기본 방향을 떠올리세요.','생성한 순서와 화면에 쌓이는 순서를 비교하세요.',ref='실행 검증',qid='u2-q117')
written(2,'layout','다음 코드에서 위젯 b를 먼저 만들었지만 실행 화면에서는 위젯 a가 왼쪽(B보다 작은 x좌표)에 나타난다. 그 이유를 한 문장으로 설명하세요.\nimport tkinter as tk\nroot = tk.Tk()\nb = tk.Label(root, text="B"); b.grid(row=0, column=1)\na = tk.Label(root, text="A"); a.grid(row=0, column=0)\nroot.mainloop()','grid()는 위젯을 만든 순서가 아니라 지정한 row·column 값으로 위치를 정하기 때문이다.','grid는 행과 열 번호로 위치를 지정합니다.','코드가 실행된 순서와 화면에 배치되는 규칙은 다릅니다.',level='심화',qid='u2-q118')
written(2,'widgets','다음 코드를 실행하면 버튼이 화면에 보이지 않는다. 빠진 한 줄을 쓰세요.\nimport tkinter as tk\nroot = tk.Tk()\nbtn = tk.Button(root, text="Go")\nroot.mainloop()','btn.pack() (또는 btn.grid()·btn.place())','위젯은 생성만으로는 화면에 나타나지 않습니다.','배치 관리자 중 하나를 호출해야 합니다.','실행 검증',level='심화',qid='u2-q119')
written(2,'events','다음 코드를 실행하면 버튼을 한 번도 클릭하지 않았는데 print(len(calls))가 1을 출력한다. 그 이유를 설명하세요.\ncalls = []\ndef hello():\n    calls.append("run")\n\nimport tkinter as tk\nroot = tk.Tk()\nbtn = tk.Button(root, text="클릭", command=hello())\nprint(len(calls))','command=hello()는 괄호가 있어 버튼을 만드는 시점에 hello가 즉시 호출되고, 그 반환값(None)이 command에 전달되기 때문이다.','괄호가 있으면 지금 당장 실행하라는 뜻입니다.','클릭 이벤트가 아니라 버튼 생성 줄 자체가 hello()를 호출합니다.','실행 검증',level='심화',qid='u2-q120')
written(2,'layout','다음 코드는 실행하면 TclError가 발생한다(오류 메시지: "cannot use geometry manager grid inside . which already has slaves managed by pack"). 오류가 나지 않도록 고치는 방법을 한 가지 쓰세요.\nimport tkinter as tk\nroot = tk.Tk()\ntk.Label(root, text="이름").pack()\ntk.Entry(root).grid(row=0, column=1)\nroot.mainloop()','같은 부모(root) 안에서는 pack()과 grid() 중 하나만 써야 한다. Entry도 pack()으로 바꾸거나, Entry를 별도 Frame에 넣어 그 Frame만 root에 pack()한다.','같은 부모 안에서 배치 관리자를 섞으면 충돌합니다.','다른 Frame으로 나누면 각 Frame 안에서는 다른 방식을 써도 됩니다.','실행 검증',level='심화',qid='u2-q121')
written(2,'memo','다음은 교과서 53쪽 save_file() 함수이다. 사용자가 대화 상자에서 "취소"를 눌렀다면 file_path에는 어떤 값이 들어오며, 그 다음 코드는 어떻게 동작하는가?\ndef save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, \'w\', encoding=\'utf-8\') as file:\n            file.write(text_area.get(\'1.0\', tk.END))','file_path에는 빈 문자열("")이 들어오고, if file_path가 거짓으로 평가되어 open() 이하가 실행되지 않고 함수가 그대로 끝난다.','빈 문자열은 조건문에서 거짓으로 취급됩니다.','취소했을 때 파일을 쓰지 않아야 기존 파일이 안전합니다.','교과서 53쪽',level='심화',qid='u2-q122')
written(2,'events','다음 코드에는 window.mainloop() 호출이 없다. 실행하면 어떤 일이 일어나는지 설명하세요.\nimport tkinter as tk\nroot = tk.Tk()\ntk.Label(root, text="안녕").pack()\nprint("끝")','이벤트 루프가 시작되지 않아 "끝"이 출력된 뒤 프로그램이 곧바로 종료된다. 창이 화면에 제대로 뜨지 못하고 사라진다.','mainloop()는 사용자 이벤트를 기다리는 반복문입니다.','이 호출이 없으면 프로그램이 끝까지 실행되어 버립니다.','실행 검증',qid='u2-q123')
coding(2,'memo','53쪽 save_file()의 file_path = filedialog.asksaveasfilename(...) 다음 줄인 if file_path: 조건을 함수로 옮기세요. 취소(빈 문자열)면 False, 유효한 경로면 True를 반환합니다.','def should_save(path):\n    return True','def should_save(path):\n    return bool(path)','assert should_save("") is False\nassert should_save("memo.txt") is True','빈 문자열은 False로 평가됩니다.','if file_path: 조건과 같은 판단을 하는 함수입니다.','교과서 53쪽',level='심화',qid='u2-q124')
blank(2,'memo','다음은 교과서 53쪽 save_file() 함수이다. 빈칸 ①에 들어갈 코드를 쓰세요.\ndef save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, \'w\', encoding=\'utf-8\') as file:\n            ①','file.write(text_area.get(\'1.0\', tk.END))','편집기의 전체 내용을 문자열로 읽어야 합니다.','파일 쓰기는 open()이 반환한 file 객체로 합니다.','교과서 53쪽',qid='u2-q127')
blank(2,'memo','다음은 교과서 52쪽 open_file() 함수이다. 빈칸 ①에 들어갈 코드를 쓰세요.\ndef open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, \'r\', encoding=\'utf-8\') as file:\n            text = file.read()\n            ①\n            text_area.insert(tk.END, text)','text_area.delete(\'1.0\', tk.END)','새 내용을 넣기 전에 기존 내용부터 지워야 합니다.','insert만 하면 이전 텍스트 뒤에 새 텍스트가 덧붙습니다.','교과서 52쪽',level='심화',qid='u2-q128')
written(2,'memo','교과서의 나만의 메모장 코드에서 open_file()과 save_file()은 모두 사용자의 "취소"를 어떻게 공통으로 처리하는지 설명하세요.\ndef open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path: ...\ndef save_file():\n    file_path = filedialog.asksaveasfilename(...)\n    if file_path: ...','두 함수 모두 대화 상자의 반환값이 빈 문자열이면 if file_path가 거짓이 되어 open() 이하를 실행하지 않고 그대로 끝난다. 그 덕분에 취소했을 때 기존 텍스트가 지워지거나 잘못된 경로에 저장되는 문제를 막는다.','두 함수의 두 번째 줄 조건문 형태가 똑같습니다.','대화 상자가 취소되면 항상 빈 문자열을 돌려줍니다.','교과서 52~53쪽',level='심화',qid='u2-q129')
choice(2,'events','다음처럼 버튼 클릭 이벤트 처리 함수 안에서 time.sleep(5)를 실행하면 어떤 문제가 생기는가?\ndef on_click():\n    time.sleep(5)\n    label.config(text="완료")\n\nbtn = tk.Button(root, text="실행", command=on_click)','5초 동안 다른 버튼 클릭이나 창 이동 등 화면 반응이 멈춘다.',['5초 동안 다른 버튼 클릭이나 창 이동 등 화면 반응이 멈춘다.','sleep이 실행되는 동안 새 스레드가 자동으로 생겨 화면은 그대로 반응한다.','sleep(5)는 5밀리초만 멈추므로 체감상 문제가 없다.','label.config가 먼저 실행되고 그 다음에 5초가 지나간다.','이벤트 루프가 알아서 sleep을 건너뛴다.'],'tkinter의 mainloop()는 하나의 스레드에서 이벤트를 순서대로 처리합니다.','sleep은 그 스레드 전체를 멈추게 해 다른 이벤트도 처리하지 못합니다.','보강',level='심화',qid='u2-q130')
q(2,'events','예측','handlers = []\ndef add_handler(name):\n    handlers.append(name)\n\nbtn1_command = add_handler\nbtn2_command = add_handler("저장")\n\nprint(handlers)','[\'저장\']','괄호가 있으면 그 자리에서 바로 실행됩니다.','btn1_command은 함수를 참조만 했고, btn2_command는 호출까지 했습니다.',level='심화',qid='u2-q131')
q(2,'layout','예측','import tkinter as tk\nroot = tk.Tk()\nroot.geometry("300x200")\ne = tk.Entry(root)\ne.place(x=50, y=80)\nroot.mainloop()','x=50, y=80 위치','place()는 좌표를 직접 지정합니다.','창의 크기(300x200)와 상관없이 지정한 좌표에 그대로 나타납니다.',ref='실행 검증',qid='u2-q132')

# -- 신규(#131): 교과서 확인 학습(48·57쪽)·종합 평가(58~59쪽) 원문 그대로 +
# 라이브러리 선택 서술 재작성(PySide6 언급 삭제).
choice(2,'ui','다음 중 사용자 인터페이스(User Interface)의 설명으로 옳지 않은 것은?','CLI는 직관적인 그래픽 환경을 제공하는 인터페이스이다.',['UI의 구성 요소에는 버튼, 색상, 입력창 등이 포함된다.','CLI는 직관적인 그래픽 환경을 제공하는 인터페이스이다.','UI는 사용자가 컴퓨터와 상호 작용하는 모든 요소를 포함한다.','GUI는 마우스나 터치로 화면의 버튼이나 메뉴를 조작할 수 있다.','NUI는 음성, 제스처 등 자연스러운 방식으로 컴퓨터와 상호 작용할 수 있다.'],'CLI의 C는 Command(명령어)입니다.','그래픽 환경으로 조작하는 것은 GUI의 특징입니다.','교과서 48쪽 1',qid='u2-q101')
written(2,'ui','GUI 프로그래밍을 하면 어떤 장점이 있는지 서술하시오.','사용자가 마우스나 버튼으로 프로그램을 쉽게 조작할 수 있고, 텍스트 기반 CLI보다 직관적이고 시각적이다.','명령어를 몰라도 사용할 수 있다는 점을 떠올리세요.','마우스·터치 조작과 시각적 피드백을 함께 언급하세요.','교과서 48쪽 2·정답 202쪽',qid='u2-q102')
written(2,'ui','NUI 프로그래밍이 무엇인지 서술하시오.','음성, 손짓, 터치, 눈동자 움직임 등 사람의 자연스러운 신체 동작을 이용해 컴퓨터와 상호 작용할 수 있도록 만드는 프로그램 개발 방식이다. 별도의 조작법을 배우지 않아도 직관적으로 사용할 수 있다.','자연스러운 신체 동작이 핵심 키워드입니다.','별도 학습이 필요 없다는 점과 스마트 기기 사례를 함께 적으세요.','교과서 48쪽 3·정답 202쪽',qid='u2-q103')
written(2,'libraries','아래의 GUI 라이브러리와 설명을 바르게 연결하시오.\n① tkinter  ② PyQt  ③ wxPython  ④ Kivy\n㉠ 멀티 플랫폼, 터치 중심 GUI 프레임워크  ㉡ 운영체제 네이티브 스타일 제공  ㉢ C++ Qt 기반, 상업용 앱에도 적합  ㉣ 파이썬 기본 GUI 라이브러리','①-㉣, ②-㉢, ③-㉡, ④-㉠','tkinter는 설치가 필요 없는 기본 라이브러리입니다.','wxPython은 운영체제 고유(네이티브) 위젯을 사용합니다.','교과서 48쪽 4',qid='u2-q104')
blank(2,'memo','다음은 IDLE에서 macOS와 관련된 macosx.py 코드의 일부이다. 빈칸에 공통으로 들어갈 모듈 이름을 쓰세요.\nimport ____\n\ndef _init_tk_type():\n    global _tk_type\n    if platform == \'darwin\':\n        root = ____.Tk()','tkinter','root.Tk()를 만들 수 있는 모듈입니다.','이 단원에서 계속 사용해 온 GUI 기본 라이브러리입니다.','교과서 55쪽',qid='u2-q106')
written(2,'widgets','다음은 56쪽 디버거 GUI 코드의 일부이다. ①·②·③에 들어갈 말을 각각 쓰세요.\nfrom tkinter import *\nfrom tkinter.ttk import ① , Scrollbar\n...\nself.bframe = bframe = ① (top)\n...\nself.bcont = b = ② (bframe, text="Go", command=self.cont)\n...\n①과 ②처럼 사용자와 상호 작용하는 인터페이스 요소를 ③이라 한다.','① Frame ② Button ③ 위젯','①은 여러 위젯을 묶는 컨테이너, ②는 클릭 버튼입니다.','①·②를 모두 포함하는 상위 개념이 ③입니다.','교과서 57쪽',qid='u2-q107')
blank(2,'widgets','tkinter에서 GUI 창을 생성할 때 사용하는 기본 객체는 무엇인가?','Tk() 객체','tk.Tk()로 만듭니다.','이 객체가 프로그램의 기본 창(root window)입니다.','교과서 58쪽 1',qid='u2-q108')
choice(2,'ui','다음 중 사용자 인터페이스(User Interface)의 정의로 가장 적절한 것은?','사용자와 기계가 상호 작용하는 기능의 집합',['프로그램의 내부 동작 방식','데이터베이스를 설계하는 구조','컴퓨터의 운영체제를 설치하는 방식','사용자가 명령어를 작성하는 개발 환경','사용자와 기계가 상호 작용하는 기능의 집합'],'UI의 정의를 떠올리세요.','특정 기술(DB·OS 설치·개발 환경)이 아니라 상호 작용 자체를 가리킵니다.','교과서 58쪽 3',qid='u2-q109')
choice(2,'ui','다음 상황은 어떤 인터페이스에 해당하는가?\n"아이콘을 클릭해서 그림판을 열었어요."','GUI',['CLI','GUI','NUI','API','TUI'],'아이콘을 마우스로 클릭했습니다.','그래픽 요소를 조작하는 방식입니다.','교과서 58쪽 4',qid='u2-q110')
choice(2,'events','보기 코드의 실행 결과로 올바른 것을 고르시오.\nimport tkinter as tk\n\ndef say_hello():\n    print("안녕하세요")\n\nwindow = tk.Tk()\nbtn = tk.Button(window, text="클릭", command=say_hello)\nbtn.pack()\nwindow.mainloop()','"클릭" 버튼이 보이고, 누르면 "안녕하세요"가 출력된다.',['PyQT를 사용하였다.','코드는 에러가 발생한다.','버튼을 누르면 창이 닫힌다.','창만 뜨고 버튼은 보이지 않는다.','"클릭" 버튼이 보이고, 누르면 "안녕하세요"가 출력된다.'],'btn.pack()으로 버튼이 화면에 배치됩니다.','command=say_hello는 클릭했을 때 함수를 호출합니다.','교과서 58쪽 5',qid='u2-q111')
choice(2,'layout','다음 중 tkinter의 배치 방식과 설명이 올바르게 연결되지 않은 것은?','center() – 위젯을 화면 중앙에 자동 배치한다.',['grid() – 행과 열 기준으로 위젯을 배치한다.','center() – 위젯을 화면 중앙에 자동 배치한다.','place() – 좌표를 직접 지정해 위젯을 배치한다.','pack() – 기본적으로 많이 사용되는 배치 방식이다.','pack() – 위에서 아래로 순차적으로 위젯을 배치한다.'],'tkinter의 배치 관리자는 pack·grid·place 세 가지입니다.','center()라는 배치 관리자는 tkinter에 없습니다.','교과서 59쪽 6',level='심화',qid='u2-q112')
choice(2,'layout','다음 빈칸에 들어갈 코드로 적절한 것은?\nimport tkinter as tk\nwindow = tk.Tk()\nlabel = tk.Label(window, text="안녕하세요")\nlabel.____\n\nwindow.mainloop()','pack()',['click()','draw()','pack()','open()','show()'],'위젯은 생성만으로는 화면에 나타나지 않습니다.','배치 관리자 메서드를 호출해야 화면에 보입니다.','교과서 59쪽 7',qid='u2-q113')
written(2,'libraries','학교용 메모장을 만든다면 tkinter, PyQt, wxPython, Kivy 중 어떤 라이브러리를 선택할지 고르고 이유를 설명하세요.','tkinter를 선택한다. 별도 설치 없이 기본 제공되어 간단한 메모장을 빠르게 만들 수 있고, 학교 실습 환경에서 설치 문제 없이 바로 사용할 수 있다.','설치 여부와 프로그램의 규모를 함께 생각하세요.','간단한 학습용 앱인지 상업용 앱인지에 따라 적합한 라이브러리가 다릅니다.','교과서 46쪽 탐구',qid='u2-q114')
