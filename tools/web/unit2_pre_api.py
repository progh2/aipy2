"""Unit II pre_api/glossary fill for #53. Applied after unit2_density.

Adds or completes code-before cards for examples that introduce a new
function/attribute/widget option. History/youtube seeds live in unit2_tips.py (#58).
wxPython appendix APIs are filled in wx_appendix.py (#55).
Kivy appendix APIs are filled in kivy_appendix.py (#56).
"""
from content import examples, units
from slots import api_items, glossary_items

SKIP_TOOLKIT = frozenset()


def _ex(eid):
    return examples[eid]


def _lesson(lid):
    return next(lesson for lesson in units[2] if lesson['id'] == lid)


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
    """Fill remaining Unit II pre_api/glossary after the #52 density examples exist."""
    _fill_lessons()
    _fill_missing_example_api()
    _complete_example_glossary()
    _complete_example_api()


def _fill_lessons():
    _fill_lesson('ui', pre_api=[
        {'name': '같은 인사, 다른 접점', 'signature': 'input/print  ·  Entry/Label  ·  손짓·음성',
         'note': '하는 일은 같습니다. 사용자가 의도를 전하는 방식만 다릅니다. 아래 CLI와 hello-tk를 나란히 보세요.'},
    ])
    _fill_lesson('libraries', pre_api=[
        {'name': '같은 버튼, 다른 이름', 'signature': 'tk.Button  ·  ttk.Button  ·  QPushButton',
         'note': '역할은 클릭입니다. 붙이는 법(pack / addWidget)만 다릅니다. 먼저 hello-tk의 Button·pack·command를 보세요.'},
    ], glossary=[
        {'term': '바인딩', 'meaning': '다른 언어의 GUI 툴킷을 파이썬에서 쓰게 하는 연결입니다. PySide6·PyQt6가 Qt의 바인딩입니다.'},
        {'term': 'ttk', 'meaning': 'tkinter의 테마 위젯입니다. 기능은 Label·Button과 같고 모양만 운영체제 테마를 따릅니다.'},
    ])
    _fill_lesson('widgets', glossary=[
        {'term': '컨테이너', 'meaning': '다른 위젯을 담는 상자입니다. Frame·QWidget이 컨테이너입니다.'},
        {'term': '제어 변수', 'meaning': '체크·라디오 값을 담는 BooleanVar·StringVar입니다. 위젯이 아니라 변수에서 읽습니다.'},
    ])
    _fill_lesson('layout', glossary=[
        {'term': 'expand와 fill', 'meaning': 'expand는 남는 공간을 누구에게 줄지, fill은 받은 칸을 위젯이 채울지입니다.'},
        {'term': 'sticky', 'meaning': '격자 칸보다 위젯이 작을 때 어느 벽에 붙일지입니다. "ew"는 좌우로 늘립니다.'},
    ])
    _fill_lesson('events', glossary=[
        {'term': '콜백 / 시그널', 'meaning': '나중에 사건이 나면 불러 달라고 맡기는 함수입니다. tkinter는 command, Qt는 connect입니다.'},
    ])
    _fill_lesson('memo', glossary=[
        {'term': '"1.0"', 'meaning': 'Text의 위치입니다. 첫 줄(1)의 0번째 칸입니다. 저장할 때는 끝의 자동 개행을 빼는 end-1c를 검토하세요.'},
    ])
    _fill_lesson('pyside', glossary=[
        {'term': 'objectName', 'meaning': 'Designer가 붙인 부품 이름입니다. 화면에 보이는 text와 다릅니다. 코드는 objectName으로 찾습니다.'},
    ])
    _fill_lesson('project', pre_api=[
        {'name': '기능 모듈', 'signature': 'from core.logic import roll, days_left, draw',
         'note': '화면 파일은 계산하지 않습니다. 같은 함수를 tkinter와 PySide6에서 부릅니다.'},
    ], glossary=[
        {'term': '화면과 기능 분리', 'meaning': 'core에는 tkinter·PySide6가 없습니다. 웹에서 기능을 먼저 검사한 뒤 GUI를 붙입니다.'},
    ])
    _fill_lesson('review', glossary=[
        {'term': 'Tk 객체', 'meaning': '창을 만드는 출발점입니다. 종합 평가에서 묻는 바로 그 객체입니다.'},
    ])


def _fill_missing_example_api():
    _fill_api('hello-pyqt', [
        {'name': 'PyQt6', 'signature': 'from PyQt6.QtWidgets import QApplication, ...',
         'note': '위젯 이름과 호출은 PySide6와 같습니다. import 줄의 패키지 이름만 바꿉니다.'},
    ])
    _fill_api('core', [
        {'name': 'roll', 'signature': 'roll(sides)',
         'note': '1부터 sides까지 정수 하나를 뽑습니다. 면 수가 1보다 작으면 ValueError입니다.'},
        {'name': 'days_left', 'signature': 'days_left("2026-12-25", today)',
         'note': '목표 날짜까지 남은 일수를 정수로 반환합니다. 오늘을 빼면 검사하기 쉽습니다.'},
        {'name': 'draw', 'signature': 'draw(["민지", "수빈"], 2)',
         'note': '공백·중복을 정리한 뒤 count명을 뽑습니다. 인원이 부족하면 ValueError입니다.'},
    ])
    _fill_api('project-tk', [
        {'name': 'messagebox.showwarning', 'signature': 'messagebox.showwarning("입력 확인", 메시지)',
         'note': '잘못된 입력을 창으로 알립니다. print만 하면 창을 보는 사용자는 모릅니다.'},
        {'name': 'textvariable', 'signature': 'result = tk.StringVar()\ntk.Label(root, textvariable=result)',
         'note': 'Label이 변수를 구독합니다. result.set("글자")하면 화면이 바뀝니다. config(text=...)와 같은 목적입니다.'},
        {'name': 'Entry.insert', 'signature': 'entry.insert(0, "6")',
         'note': '시작할 때 칸에 기본값을 넣습니다. 0은 맨 앞 위치입니다.'},
    ])
    _fill_api('project-pyside', [
        {'name': 'QComboBox', 'signature': 'self.mode.addItems(["주사위", "D-day", "추첨"])\nself.mode.currentText()',
         'note': '드롭다운으로 모드를 고릅니다. tkinter 라디오+StringVar를 한 위젯으로 대신합니다.'},
        {'name': 'QMessageBox.warning', 'signature': 'QMessageBox.warning(self, "입력 확인", str(error))',
         'note': 'messagebox.showwarning에 대응합니다. 첫 인자는 부모 창입니다.'},
        {'name': '클래스와 self', 'signature': 'self.entry = QLineEdit("6")',
         'note': 'run_task에서 같은 입력칸을 쓰려면 위젯을 self에 둡니다. 함수만 쓰면 이름이 사라집니다.'},
    ])


def _complete_example_glossary():
    _fill_glossary('hello-ttk', [
        {'term': '테마 위젯', 'meaning': '역할은 tk.Label·tk.Button과 같고, 테두리·색만 운영체제 테마를 따릅니다. command·pack은 그대로입니다.'},
    ])
    _fill_glossary('core', [
        {'term': '반환과 출력', 'meaning': '함수는 값을 return하고, print는 main에서 합니다. GUI는 이 반환값을 Label에 보여 줍니다.'},
    ])
    _fill_glossary('project-tk', [
        {'term': '입력 확인', 'meaning': '빈 칸·0면·잘못된 날짜는 core가 ValueError를 냅니다. GUI는 try/except로 메시지를 보여 줍니다.'},
    ])
    _fill_glossary('project-pyside', [
        {'term': 'currentText', 'meaning': '지금 고른 콤보 항목의 글자입니다. StringVar.get()에 대응합니다.'},
    ])
    _fill_glossary('widgets-list-canvas-tk', [
        {'term': '인덱스', 'meaning': '목록의 몇 번째인지입니다. 0부터 셉니다. curselection()이 그 번호를 줍니다.'},
        {'term': '좌표', 'meaning': 'Canvas는 칸이 아니라 (x, y)로 그립니다. 왼쪽 위가 (0, 0)입니다.'},
    ])
    _fill_glossary('widgets-tk', [
        {'term': '도감', 'meaning': '한 창에 여러 위젯을 모아 비교합니다. 실제 화면은 필요한 위젯만 고릅니다.'},
    ])
    _fill_glossary('widgets-pyside', [
        {'term': '이름 대응', 'meaning': 'Label→QLabel, Entry→QLineEdit, Text→QPlainTextEdit, Check→QCheckBox입니다. 역할로 외우세요.'},
    ])
    _fill_glossary('widgets-pyside-form', [
        {'term': 'QButtonGroup', 'meaning': '라디오를 한 묶음으로 만듭니다. 묶지 않으면 여러 개가 같이 켜질 수 있습니다.'},
    ])
    _fill_glossary('layout-pyside', [
        {'term': '중첩 레이아웃', 'meaning': '세로 상자 안에 가로 상자를 넣을 수 있습니다. addLayout은 레이아웃, addWidget은 위젯입니다.'},
    ])
    _fill_glossary('layout-pyside-form', [
        {'term': '칸 병합', 'meaning': 'addWidget(위젯, 행, 열, 행개수, 열개수)의 뒤 두 숫자로 여러 칸을 차지합니다.'},
    ])
    _fill_glossary('events-bind-tk', [
        {'term': '이벤트 이름', 'meaning': '"<Return>"처럼 꺾쇠를 포함한 문자열입니다. "Return"만 쓰면 연결되지 않습니다.'},
    ])
    _fill_glossary('events-pyside-signal', [
        {'term': '시그널', 'meaning': '위젯이 알리는 사건입니다. clicked·textChanged가 시그널이고, connect로 함수를 붙입니다.'},
    ])
    _fill_glossary('memo-pyside', [
        {'term': 'QMainWindow', 'meaning': '메뉴·중앙 위젯이 있는 문서 창입니다. 인사 앱의 QWidget보다 메모장에 맞습니다.'},
    ])
    _fill_glossary('memo-plus-tk', [
        {'term': 'dirty', 'meaning': '저장 이후 글이 바뀌었는지입니다. 제목 앞 *와 닫기 확인의 기준입니다.'},
    ])
    _fill_glossary('memo-plus-pyside', [
        {'term': 'isModified', 'meaning': 'Qt가 기억하는 dirty 플래그입니다. 저장 후 setModified(False)로 되돌립니다.'},
    ])


def _complete_example_api():
    _extend_api('hello-pyqt', [
        {'name': '바꿔 볼 곳', 'signature': 'examples["hello-pyside"]의 import를 PyQt6로',
         'note': 'setWindowTitle·clicked.connect·app.exec는 그대로입니다. 한 줄만 바꿔 같은 창이 열리는지 확인하세요.'},
    ])
    _extend_api('memo-plus-tk', [
        {'name': 'undo=True', 'signature': 'tk.Text(root, wrap="word", undo=True)',
         'note': 'Ctrl+Z로 되돌리기를 켭니다. 기본 Text는 undo가 꺼져 있습니다.'},
        {'name': 'accelerator', 'signature': 'file_menu.add_command(..., accelerator="Ctrl+S")',
         'note': '메뉴에 단축키 글자만 보여 줍니다. 실제 키 동작은 bind가 합니다. 둘 다 넣으세요.'},
    ])
    _extend_api('memo-plus-pyside', [
        {'name': 'QMessageBox.question', 'signature': 'QMessageBox.question(..., B.Save | B.Discard | B.Cancel)',
         'note': '저장/버리기/취소 세 갈래입니다. askyesnocancel에 대응합니다.'},
    ])
    _extend_api('layout-tk', [
        {'name': '세 배치를 한 창에서', 'signature': 'LabelFrame마다 pack / grid / place',
         'note': '부모를 나누면 한 창에서 비교할 수 있습니다. 같은 Frame 안에서는 pack과 grid를 섞지 마세요.'},
    ])
    _extend_api('widgets-tk', [
        {'name': 'pack을 빼면', 'signature': '위젯.pack()  # 생성만으로는 안 보임',
         'note': '도감의 위젯도 모두 pack을 호출합니다. 생성과 배치는 다른 단계입니다.'},
    ])


def unit2_pre_coverage():
    """Examples that must show a code-before card."""
    ids = []
    for lesson in units[2]:
        for eid in lesson['examples']:
            if eid in SKIP_TOOLKIT:
                continue
            if eid not in ids:
                ids.append(eid)
    return ids
