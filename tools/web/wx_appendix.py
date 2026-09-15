"""Unit II appendix: rebuild the same memo/widget apps with wxPython (#55).

Imported at the end of content.py. Does not change the tk/PySide example
lists on the main Unit II topics. History/youtube seeding stays #58;
Kivy appendix is kivy_appendix.py (#56).
"""
from content import ex, lesson, units, examples, core
from slots import api_items, glossary_items

NOTE = (
    '브라우저(Pyodide)에는 wxPython이 없어 창이 뜨지 않습니다. '
    '웹에서는 문법 확인과 코드·실행 화면으로 배우고, '
    'PC에서 python -m pip install wxPython 후 python main.py로 실행하세요.'
)
WX_EXAMPLES = [
    'first-wx', 'hello-wx',
    'widgets-label-entry-wx', 'widgets-choice-wx', 'widgets-wx',
    'layout-wx', 'events-wx',
    'memo-window-wx', 'memo-wx', 'project-wx',
]

OWN = {
    'first-wx': (
        'wxPython 최소 창 · App → Frame → Show → MainLoop',
        '위젯을 더하기 전의 빈 창입니다. 이 예제를 Linux에서 실행해 캡처했습니다. OS·테마에 따라 외형은 달라집니다.'),
    'widgets-label-entry-wx': (
        'StaticText·TextCtrl 창 · 이름 입력 후 표시 버튼',
        '한 줄 입력과 SetLabel로 같은 이름을 다시 보여 줍니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'widgets-choice-wx': (
        '체크·라디오 창 · 학년과 완료 여부',
        'CheckBox.GetValue와 RadioButton 묶음으로 선택 값을 읽습니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'widgets-wx': (
        'wxPython 위젯 도감 · 설명·입력·선택·목록',
        '본편 위젯 도감을 운영체제 위젯 이름으로 대응합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'layout-wx': (
        'BoxSizer·FlexGridSizer 배치 창',
        '세로 상자 안에 가로 버튼과 격자 폼을 올립니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'events-wx': (
        'EVT_BUTTON·EVT_TEXT 연결 창',
        '글자를 쓰면 미리보기가 바뀌고, 버튼은 인사를 확정합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'memo-window-wx': (
        '메모장 뼈대 · 창과 여러 줄 TextCtrl만',
        '메뉴·파일 대화 상자 전의 최소 화면입니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'memo-wx': (
        '메모장 · wxPython 메뉴와 편집기',
        '여러 줄 TextCtrl과 파일 메뉴를 붙인 완성본입니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'project-wx': (
        '생활 도우미 · wxPython Choice와 실행 버튼',
        '같은 core.logic을 주사위·D-day·추첨에 연결합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
}


def _lesson(lesson_id):
    return next(item for item in units[2] if item['id'] == lesson_id)


ex('first-wx', 'wxPython · 최소 창 실행 순서', {'main.py': '''import wx

app = wx.App()
window = wx.Frame(None, title="첫 창 · wxPython", size=(360, 160))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(wx.StaticText(panel, label="wx.App → Frame → Show → MainLoop"), 0, wx.ALL, 24)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'wx.App', 'signature': 'app = wx.App()',
         'note': '앱 객체입니다. 창보다 먼저 만듭니다. tkinter의 Tk()가 창과 앱을 겸하는 것과 다릅니다.'},
        {'name': 'wx.Frame / Panel', 'signature': 'window = wx.Frame(None, title="제목", size=(360, 160))\npanel = wx.Panel(window)',
         'note': 'Frame은 제목 줄이 있는 창입니다. 위젯은 보통 Panel 위에 올립니다. None은 최상위 창이라는 뜻입니다.'},
        {'name': 'Show / MainLoop', 'signature': 'window.Show()\napp.MainLoop()',
         'note': 'Show로 창을 보여 주고 MainLoop로 클릭·입력을 기다립니다. tkinter의 mainloop, Qt의 exec에 대응합니다.'},
    ],
    glossary=[
        {'term': 'Phoenix', 'meaning': '지금 쓰는 wxPython 4의 이름입니다. import wx로 불러옵니다.'},
        {'term': '브라우저 실행', 'meaning': 'Pyodide에는 wx가 없습니다. 이 페이지는 코드와 캡처로 가르치고, 실제 창은 PC에서 엽니다.'},
    ])

ex('widgets-label-entry-wx', 'StaticText·TextCtrl · 한 줄 읽고 보여 주기', {'main.py': '''import wx

def show_name(event):
    name = entry.GetValue().strip() or "이름 없음"
    result.SetLabel(f"입력한 이름: {name}")

app = wx.App()
window = wx.Frame(None, title="StaticText와 TextCtrl", size=(420, 180))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(wx.StaticText(panel, label="이름을 입력하세요."), 0, wx.ALL, 8)
entry = wx.TextCtrl(panel)
layout.Add(entry, 0, wx.EXPAND | wx.ALL, 12)
button = wx.Button(panel, label="표시")
button.Bind(wx.EVT_BUTTON, show_name)
layout.Add(button, 0, wx.ALL, 8)
result = wx.StaticText(panel, label="아직 입력이 없습니다.")
layout.Add(result, 0, wx.ALL, 8)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'StaticText', 'signature': 'wx.StaticText(panel, label="설명")',
         'note': '짧은 글을 보여 줍니다. tkinter Label, Qt QLabel에 대응합니다. 나중에 SetLabel로 바꿉니다.'},
        {'name': 'TextCtrl.GetValue', 'signature': 'entry = wx.TextCtrl(panel)\nentry.GetValue()',
         'note': '한 줄 입력의 현재 문자열을 읽습니다. Entry.get() / QLineEdit.text()와 같습니다.'},
        {'name': 'SetLabel', 'signature': 'result.SetLabel(새글자)',
         'note': '이미 만든 라벨의 글자만 바꿉니다. 새 StaticText를 또 만들면 화면에 겹칩니다.'},
    ],
    glossary=[{'term': '한 줄 입력', 'meaning': '이름·아이디처럼 줄바꿈이 없는 값입니다. 여러 줄 메모는 style=wx.TE_MULTILINE을 씁니다.'}])

ex('widgets-choice-wx', 'CheckBox·RadioButton · 선택 값 읽기', {'main.py': '''import wx

app = wx.App()
window = wx.Frame(None, title="체크와 라디오", size=(420, 240))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
done = wx.CheckBox(panel, label="오늘 실습 완료")
layout.Add(done, 0, wx.ALL, 8)
radios = []
for i, value in enumerate(["1학년", "2학년", "3학년"]):
    style = wx.RB_GROUP if i == 0 else 0
    radio = wx.RadioButton(panel, label=value, style=style)
    radios.append(radio)
    layout.Add(radio, 0, wx.LEFT | wx.BOTTOM, 12)
result = wx.StaticText(panel, label="체크는 여러 개, 라디오는 하나.")
layout.Add(result, 0, wx.ALL, 8)

def show_choice(event):
    extra = "완료" if done.GetValue() else "미완료"
    grade = next((item.GetLabel() for item in radios if item.GetValue()), "?")
    result.SetLabel(f"{grade} · {extra}")

button = wx.Button(panel, label="선택 확인")
button.Bind(wx.EVT_BUTTON, show_choice)
layout.Add(button, 0, wx.ALL, 8)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'CheckBox', 'signature': 'done = wx.CheckBox(panel, label="오늘 실습 완료")\ndone.GetValue()',
         'note': '서로 독립적으로 켜고 끌 수 있습니다. GetValue()가 True 또는 False입니다. BooleanVar가 따로 없습니다.'},
        {'name': 'RadioButton / RB_GROUP', 'signature': 'wx.RadioButton(panel, label="1학년", style=wx.RB_GROUP)',
         'note': '묶음의 첫 라디오에만 RB_GROUP을 줍니다. 그 다음 라디오는 같은 그룹에서 하나만 선택됩니다.'},
    ],
    glossary=[{'term': '제어 변수 없음', 'meaning': 'tkinter는 BooleanVar에 상태를 둡니다. wx는 위젯 자체에서 GetValue()로 읽습니다.'}])

ex('widgets-wx', 'wxPython 위젯 도감', {'main.py': '''import wx

app = wx.App()
window = wx.Frame(None, title="wxPython 위젯 도감", size=(420, 520))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(wx.StaticText(panel, label="StaticText: 설명을 표시합니다"), 0, wx.ALL, 8)
layout.Add(wx.TextCtrl(panel), 0, wx.EXPAND | wx.ALL, 8)
multi = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 64))
layout.Add(multi, 0, wx.EXPAND | wx.ALL, 8)
checked = wx.CheckBox(panel, label="학습 완료")
layout.Add(checked, 0, wx.ALL, 8)
for i, value in enumerate(["A", "B"]):
    style = wx.RB_GROUP if i == 0 else 0
    layout.Add(wx.RadioButton(panel, label=value, style=style), 0, wx.LEFT, 12)
listbox = wx.ListBox(panel, choices=["모듈", "패키지", "GUI"], size=(-1, 72))
layout.Add(listbox, 0, wx.EXPAND | wx.ALL, 8)
canvas = wx.Panel(panel, size=(-1, 48))
canvas.SetBackgroundColour("gold")
layout.Add(canvas, 0, wx.EXPAND | wx.ALL, 8)
button = wx.Button(panel, label="상태 출력")
button.Bind(wx.EVT_BUTTON, lambda event: print(checked.GetValue()))
layout.Add(button, 0, wx.ALL, 8)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'TE_MULTILINE', 'signature': 'wx.TextCtrl(panel, style=wx.TE_MULTILINE)',
         'note': '여러 줄 입력입니다. 한 줄은 기본 TextCtrl, 여러 줄은 이 스타일입니다. tkinter Text에 대응합니다.'},
        {'name': 'ListBox', 'signature': 'wx.ListBox(panel, choices=["모듈", "패키지"])',
         'note': '목록에서 고릅니다. tkinter Listbox.insert 대신 만들 때 choices를 넣을 수 있습니다.'},
        {'name': 'Panel 배경', 'signature': 'canvas.SetBackgroundColour("gold")',
         'note': '도형 Canvas와 일대일은 아닙니다. 색 있는 Panel로 “그리기 자리”를 표시합니다. 실제 그림은 EVT_PAINT에서 그립니다.'},
    ],
    glossary=[{'term': '이름 대응', 'meaning': 'Label→StaticText, Entry→TextCtrl, Text→TE_MULTILINE, Check→CheckBox, List→ListBox입니다. 역할로 외우세요.'}])

ex('layout-wx', 'wxPython · 상자 배치와 격자 폼', {'main.py': '''import wx

app = wx.App()
window = wx.Frame(None, title="wx 레이아웃", size=(520, 260))
panel = wx.Panel(window)
vertical = wx.BoxSizer(wx.VERTICAL)
horizontal = wx.BoxSizer(wx.HORIZONTAL)
for name in ["열기", "저장", "종료"]:
    horizontal.Add(wx.Button(panel, label=name), 1, wx.EXPAND | wx.ALL, 4)
vertical.Add(horizontal, 0, wx.EXPAND | wx.ALL, 8)
grid = wx.FlexGridSizer(2, 2, 8, 8)
grid.AddGrowableCol(1, 1)
grid.Add(wx.StaticText(panel, label="아이디"), 0, wx.ALIGN_CENTER_VERTICAL)
grid.Add(wx.TextCtrl(panel), 0, wx.EXPAND)
grid.Add(wx.StaticText(panel, label="비밀번호"), 0, wx.ALIGN_CENTER_VERTICAL)
secret = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
grid.Add(secret, 0, wx.EXPAND)
vertical.Add(grid, 0, wx.EXPAND | wx.ALL, 8)
panel.SetSizer(vertical)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'BoxSizer', 'signature': 'vertical = wx.BoxSizer(wx.VERTICAL)\nhorizontal = wx.BoxSizer(wx.HORIZONTAL)',
         'note': '세로 묶음과 가로 묶음입니다. pack / QVBoxLayout·QHBoxLayout에 대응합니다.'},
        {'name': 'Add 비율', 'signature': 'sizer.Add(위젯, 1, wx.EXPAND | wx.ALL, 4)',
         'note': '두 번째 숫자 1은 남는 공간을 받겠다는 뜻입니다. 0이면 내용 크기만 씁니다. EXPAND는 받은 칸을 채웁니다.'},
        {'name': 'FlexGridSizer', 'signature': 'grid = wx.FlexGridSizer(2, 2, 8, 8)\ngrid.AddGrowableCol(1, 1)',
         'note': '행·열 격자입니다. AddGrowableCol(1)은 둘째 열(입력칸)이 창과 함께 늘어나게 합니다. tkinter grid+weight와 같습니다.'},
        {'name': 'TE_PASSWORD', 'signature': 'wx.TextCtrl(panel, style=wx.TE_PASSWORD)',
         'note': '입력 글자를 가립니다. Entry의 show="*" / QLineEdit EchoMode.Password와 같은 목적입니다.'},
    ],
    glossary=[{'term': 'Sizer', 'meaning': '위젯의 자리를 정하는 배치 관리자입니다. Frame이 아니라 Panel에 SetSizer로 붙입니다.'}])

ex('events-wx', 'Bind · EVT_BUTTON과 EVT_TEXT', {'main.py': '''import wx

def greet(event):
    name = entry.GetValue().strip() or "여러분"
    result.SetLabel(f"{name}님, 안녕하세요!")

def preview(event):
    text = entry.GetValue()
    result.SetLabel(f"미리보기: {text or '빈 칸'}")

app = wx.App()
window = wx.Frame(None, title="이벤트 · wxPython", size=(420, 200))
panel = wx.Panel(window)
layout = wx.BoxSizer(wx.VERTICAL)
entry = wx.TextCtrl(panel)
entry.Bind(wx.EVT_TEXT, preview)
layout.Add(entry, 0, wx.EXPAND | wx.ALL, 12)
button = wx.Button(panel, label="인사하기")
button.Bind(wx.EVT_BUTTON, greet)
layout.Add(button, 0, wx.ALL, 8)
result = wx.StaticText(panel, label="글자를 쓰면 미리보기가 바뀝니다.")
layout.Add(result, 0, wx.ALL, 12)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'Bind', 'signature': 'button.Bind(wx.EVT_BUTTON, greet)',
         'note': '사건에 함수를 맡깁니다. command= / clicked.connect에 대응합니다. Bind(..., greet())처럼 괄호를 붙이면 지금 실행됩니다.'},
        {'name': 'EVT_BUTTON', 'signature': 'button.Bind(wx.EVT_BUTTON, greet)',
         'note': '버튼 클릭입니다. 처리 함수는 event 인자 하나를 받습니다. 쓰지 않아도 매개변수는 있어야 합니다.'},
        {'name': 'EVT_TEXT', 'signature': 'entry.Bind(wx.EVT_TEXT, preview)',
         'note': '한 글자가 바뀔 때마다 preview(event)를 호출합니다. Qt textChanged와 같습니다.'},
        {'name': 'event 인자', 'signature': 'def greet(event):',
         'note': 'wx는 항상 이벤트 객체를 넘깁니다. tkinter command는 인자가 없습니다. 함수 머리를 그대로 옮기면 TypeError가 납니다.'},
    ],
    glossary=[
        {'term': '이벤트 테이블', 'meaning': '위젯과 사건과 함수의 연결입니다. Bind가 한 줄을 추가합니다.'},
        {'term': '지금 호출', 'meaning': 'Bind(wx.EVT_BUTTON, greet())는 창을 만들 때 이미 실행됩니다. 함수 이름만 넘기세요.'},
    ])

ex('memo-window-wx', '메모장 ① · 창과 여러 줄 TextCtrl만', {'main.py': '''import wx

app = wx.App()
window = wx.Frame(None, title="나만의 메모장 · 창만", size=(640, 420))
panel = wx.Panel(window)
editor = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(editor, 1, wx.EXPAND)
panel.SetSizer(layout)
window.Show()
app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'Frame size', 'signature': 'wx.Frame(None, title="제목", size=(640, 420))',
         'note': '처음 창 크기입니다. tkinter geometry("640x420")에 대응합니다.'},
        {'name': 'TE_MULTILINE + 비율 1', 'signature': 'layout.Add(editor, 1, wx.EXPAND)',
         'note': '여러 줄 편집기가 남는 공간을 채웁니다. pack(expand=True, fill="both")와 같은 의도입니다.'},
    ],
    glossary=[{'term': '단계 1', 'meaning': '창과 편집기만 있으면 메모장의 뼈대입니다. 열기·저장은 다음 예제입니다.'}])

ex('memo-wx', '교과서 메모장 · wxPython 전체 코드', {'main.py': '''import wx
from pathlib import Path

class MemoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="나만의 메모장 · wxPython", size=(640, 420))
        panel = wx.Panel(self)
        self.editor = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.editor, 1, wx.EXPAND)
        panel.SetSizer(layout)
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        open_item = file_menu.Append(wx.ID_OPEN, "열기\tCtrl+O")
        save_item = file_menu.Append(wx.ID_SAVE, "저장\tCtrl+S")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "종료")
        menubar.Append(file_menu, "파일")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.open_file, open_item)
        self.Bind(wx.EVT_MENU, self.save_file, save_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def open_file(self, event):
        with wx.FileDialog(self, "열기", wildcard="텍스트 (*.txt)|*.txt|모든 파일 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
        try:
            self.editor.SetValue(Path(path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            wx.MessageBox(str(error), "열기 실패", wx.OK | wx.ICON_WARNING)

    def save_file(self, event):
        with wx.FileDialog(self, "저장", wildcard="텍스트 (*.txt)|*.txt",
                           defaultFile="memo.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
        try:
            Path(path).write_text(self.editor.GetValue(), encoding="utf-8")
        except (OSError, UnicodeError) as error:
            wx.MessageBox(str(error), "저장 실패", wx.OK | wx.ICON_WARNING)

    def on_exit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    window = MemoFrame()
    window.Show()
    app.MainLoop()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'MenuBar / Menu', 'signature': 'menubar = wx.MenuBar()\nfile_menu.Append(wx.ID_OPEN, "열기")\nself.SetMenuBar(menubar)',
         'note': '창 위쪽 메뉴 줄입니다. tkinter Menu.add_cascade, Qt QAction에 대응합니다.'},
        {'name': 'EVT_MENU', 'signature': 'self.Bind(wx.EVT_MENU, self.open_file, open_item)',
         'note': '메뉴 항목에 함수를 연결합니다. 세 번째 인자로 어떤 항목인지 지정합니다.'},
        {'name': 'FileDialog', 'signature': 'with wx.FileDialog(self, "열기", style=wx.FD_OPEN) as dialog:\n    if dialog.ShowModal() == wx.ID_CANCEL:\n        return\n    path = dialog.GetPath()',
         'note': 'ShowModal()이 ID_CANCEL이면 취소를 누른 것입니다. 빈 경로를 열지 마세요. QFileDialog의 빈 경로 검사와 같습니다.'},
        {'name': 'SetValue / GetValue', 'signature': 'editor.SetValue(글)\neditor.GetValue()',
         'note': '여러 줄 텍스트를 넣거나 읽습니다. setPlainText/toPlainText, Text.insert/get에 대응합니다.'},
    ],
    glossary=[
        {'term': 'ID_OPEN / ID_SAVE', 'meaning': '운영체제가 아는 표준 메뉴 번호입니다. 단축키와 아이콘을 기본으로 붙일 수 있습니다.'},
        {'term': '취소 시험', 'meaning': '열기·저장에서 취소를 눌러 보세요. 기존 글이 그대로면 분기가 맞은 것입니다.'},
    ])

ex('project-wx', '생활 도우미 · wxPython', {'main.py': '''import wx
from core.logic import roll, days_left, draw

class HelperFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="우리 반 생활 도우미 · wxPython", size=(520, 280))
        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        self.mode = wx.Choice(panel, choices=["주사위", "D-day", "추첨"])
        self.mode.SetSelection(0)
        layout.Add(self.mode, 0, wx.EXPAND | wx.ALL, 8)
        layout.Add(wx.StaticText(panel, label="면 수 / YYYY-MM-DD / 쉼표로 나눈 이름"), 0, wx.ALL, 8)
        self.entry = wx.TextCtrl(panel, value="6")
        layout.Add(self.entry, 0, wx.EXPAND | wx.ALL, 8)
        button = wx.Button(panel, label="실행")
        button.Bind(wx.EVT_BUTTON, self.run_task)
        layout.Add(button, 0, wx.ALL, 8)
        self.result = wx.StaticText(panel, label="결과가 여기에 표시됩니다.")
        layout.Add(self.result, 0, wx.ALL, 8)
        panel.SetSizer(layout)

    def run_task(self, event):
        try:
            value = self.entry.GetValue()
            mode = self.mode.GetStringSelection()
            if mode == "주사위":
                output = str(roll(int(value)))
            elif mode == "D-day":
                output = str(days_left(value)) + "일"
            else:
                output = ", ".join(draw(value.split(","), 1))
            self.result.SetLabel(output)
        except ValueError as error:
            wx.MessageBox(str(error), "입력 확인", wx.OK | wx.ICON_WARNING)

if __name__ == "__main__":
    app = wx.App()
    window = HelperFrame()
    window.Show()
    app.MainLoop()''' , **core}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'from core.logic import roll', 'signature': 'from core.logic import roll, days_left, draw',
         'note': '화면 파일은 계산을 직접 쓰지 않습니다. 웹의 core 예제·tk/PySide 생활 도우미와 같은 함수입니다.'},
        {'name': 'Choice', 'signature': 'self.mode = wx.Choice(panel, choices=["주사위", "D-day", "추첨"])\nself.mode.GetStringSelection()',
         'note': '드롭다운으로 모드를 고릅니다. tkinter 라디오, Qt QComboBox를 한 위젯으로 대신합니다.'},
        {'name': 'MessageBox', 'signature': 'wx.MessageBox(메시지, "입력 확인", wx.OK | wx.ICON_WARNING)',
         'note': '잘못된 입력을 창으로 알립니다. messagebox.showwarning / QMessageBox.warning에 대응합니다.'},
    ],
    glossary=[{'term': '화면과 기능 분리', 'meaning': 'core에는 wx가 없습니다. 같은 roll을 세 GUI에서 부를 수 있습니다.'}])

lesson(2, 'wx', '부록 · wxPython으로 같은 앱 다시 만들기', '부록 · 확장 학습',
       '본편에서 익힌 창·위젯·배치·이벤트·메모장을 운영체제 위젯으로 옮깁니다.',
       [
           '이 페이지는 본편 tkinter/PySide6 경로를 대체하지 않습니다. 같은 인사·위젯 도감·배치·이벤트·메모장·생활 도우미를 wxPython으로 다시 구성합니다. 수행평가의 기본 도구는 여전히 tkinter입니다.',
           '브라우저의 Pyodide에는 wxPython이 포함되지 않습니다. 웹 실습실은 문법을 확인하고, 아래 코드와 실행 화면으로 역할을 배웁니다. 실제 창·버튼·파일 대화 상자는 PC에서 확인하세요. 가상환경을 켠 뒤 python -m pip install wxPython 을 실행하고 python main.py로 엽니다. Windows PowerShell은 .venv\\Scripts\\Activate.ps1, macOS/Linux는 source .venv/bin/activate입니다.',
           '실행 순서는 wx.App() → Frame → Panel → Sizer → Bind → Show → MainLoop입니다. tkinter의 Tk·pack·command·mainloop, Qt의 QApplication·Layout·connect·exec를 역할로 옮기세요. 단어만 바꾸면 event 인자나 Panel/Sizer에서 막힙니다.',
           '위젯 이름은 Label→StaticText, Entry→TextCtrl, Text→TextCtrl(TE_MULTILINE), Checkbutton→CheckBox, Radiobutton→RadioButton(첫 항목에 RB_GROUP), Listbox→ListBox, Button→Button입니다. 체크 상태는 BooleanVar가 아니라 GetValue()로 읽습니다.',
           '배치는 BoxSizer(VERTICAL/HORIZONTAL)와 FlexGridSizer입니다. Add의 두 번째 숫자가 남는 공간 비율이고, EXPAND는 받은 칸을 채웁니다. 이벤트는 Bind(wx.EVT_BUTTON, greet)처럼 함수 자체를 맡깁니다. greet()를 넘기면 창을 만들 때 이미 실행됩니다.',
           '메모장은 여러 줄 TextCtrl과 MenuBar, FileDialog로 본편과 같은 열기·저장·취소 분기를 만듭니다. 생활 도우미는 같은 core.logic을 Choice에 연결합니다. 빈 입력·0면 주사위·잘못된 날짜를 시험하세요.',
       ],
       WX_EXAMPLES,
       [
           '본편 위젯 하나를 골라 wx 이름을 짝 짓고, 값을 읽는 메서드를 적으세요.',
           '열기 대화 상자에서 취소를 눌렀을 때 기존 글이 남는지 설명하세요.',
           '웹에서 실행 버튼이 창을 열지 않는 이유를 한 문장으로 적으세요.',
       ],
       extra=True)


def apply():
    """Register the appendix topic, wx API cards, and screenshot catalog."""
    import unit2_shots
    hello = examples['hello-wx']
    if not hello['pre_api']:
        hello['pre_api'] = api_items([
            {'name': 'wx.App', 'signature': 'app = wx.App()',
             'note': '앱 객체입니다. 창보다 먼저 만듭니다.'},
            {'name': 'wx.Frame', 'signature': 'window = wx.Frame(None, title="제목", size=(480, 300))',
             'note': '제목 줄이 있는 창입니다. 위젯은 Panel 위에 올립니다.'},
            {'name': 'BoxSizer', 'signature': 'layout = wx.BoxSizer(wx.VERTICAL)\nlayout.Add(위젯, 0, wx.ALL, 12)',
             'note': '위에서 아래로 붙입니다. pack() 대신 Sizer가 자리를 정합니다.'},
            {'name': 'TextCtrl', 'signature': 'entry = wx.TextCtrl(panel)\nentry.GetValue()  ·  entry.SetValue("")',
             'note': '한 줄 입력입니다. tkinter Entry의 get/delete에 대응합니다.'},
            {'name': 'Bind', 'signature': 'button.Bind(wx.EVT_BUTTON, greet)',
             'note': '클릭 사건에 함수를 맡깁니다. Bind(..., greet())처럼 괄호를 붙이면 지금 실행됩니다. greet는 event 인자를 받습니다.'},
            {'name': 'MainLoop', 'signature': 'window.Show()\napp.MainLoop()',
             'note': '이벤트 루프입니다. Show 뒤에 호출합니다. tkinter mainloop / Qt exec에 대응합니다.'},
        ])
    if not hello['glossary']:
        hello['glossary'] = glossary_items([
            {'term': 'wxPython', 'meaning': 'wxWidgets의 파이썬 바인딩입니다. 운영체제의 버튼·입력창을 그대로 활용합니다.'},
            {'term': 'event 인자', 'meaning': '처리 함수의 첫 매개변수입니다. 쓰지 않아도 선언해야 TypeError가 나지 않습니다.'},
        ])
    if not hello['note']:
        hello['note'] = NOTE

    wx_lesson = _lesson('wx')
    wx_lesson['examples'] = list(WX_EXAMPLES)
    wx_lesson['pre_api'] = api_items([
        {'name': '실행 순서', 'signature': 'wx.App → Frame·Panel·Sizer → Bind → Show → MainLoop',
         'note': '본편 Tk·pack·command·mainloop를 wx 이름으로 옮긴 순서입니다. 브라우저에서는 창이 뜨지 않습니다.'},
    ])
    wx_lesson['glossary'] = glossary_items([
        {'term': '부록', 'meaning': '본편을 다시 배우는 길이 아닙니다. 같은 앱을 세 번째 툴킷으로 대조하는 확장입니다.'},
        {'term': 'Pyodide', 'meaning': '사이트 안의 Python입니다. C 확장인 wxPython을 불러올 수 없어 PC 실습으로 표시합니다.'},
    ])

    libraries = _lesson('libraries')
    pointer = '위젯·배치·이벤트·메모장을 wxPython으로 다시 만드는 과정은 부록 주제에서 이어집니다. 본편 tkinter/PySide6 경로는 그대로입니다.'
    if pointer not in libraries['paragraphs']:
        libraries['paragraphs'].append(pointer)

    unit2_shots.OWN.update(OWN)
    unit2_shots.LESSON['wx'] = (
        'widgets-wx.png', 'wxPython 위젯 도감 실행 화면',
        '본편에서 고른 위젯을 wx 이름으로 옮긴 뒤 값을 읽어 보세요. 이 예제를 Linux에서 실행해 캡처했습니다.',
    )
