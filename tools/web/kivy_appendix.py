"""Unit II appendix: rebuild the same memo/widget apps with Kivy (#56).

Imported at the end of content.py. Does not change the tk/PySide/wx example
lists on the main Unit II topics. History/youtube seeding stays #58.
"""
from content import ex, lesson, units, examples, core
from slots import api_items, glossary_items

NOTE = (
    '브라우저(Pyodide)에는 Kivy가 없어 창이 뜨지 않습니다. '
    '웹에서는 문법 확인과 코드·실행 화면으로 배우고, '
    'PC에서 python -m pip install kivy 후 python main.py로 실행하세요. '
    '기본 글꼴은 한글을 가정하지 않습니다. 실행 폴더에 NotoSansKR.ttf를 넣으면 한국어 문구로 바꿀 수 있습니다.'
)
KIVY_EXAMPLES = [
    'first-kivy', 'hello-kivy',
    'widgets-label-entry-kivy', 'widgets-choice-kivy', 'widgets-kivy',
    'layout-kivy', 'events-kivy',
    'memo-window-kivy', 'memo-kivy', 'project-kivy',
]
FONT = '''from pathlib import Path
font = "NotoSansKR.ttf"
if not Path(font).exists():
    font = "Roboto"
'''

OWN = {
    'first-kivy': (
        'Kivy 최소 창 · App → build → run',
        '위젯을 더하기 전의 빈 창입니다. 이 예제를 Linux에서 실행해 캡처했습니다. OS·테마에 따라 외형은 달라집니다.'),
    'widgets-label-entry-kivy': (
        'Label·TextInput 창 · 이름 입력 후 Show 버튼',
        '한 줄 입력과 Label.text로 같은 이름을 다시 보여 줍니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'widgets-choice-kivy': (
        'CheckBox·ToggleButton 창 · 학년과 완료 여부',
        'CheckBox.active와 ToggleButton 묶음으로 선택 값을 읽습니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'widgets-kivy': (
        'Kivy 위젯 도감 · 설명·입력·선택·목록',
        '본편 위젯 도감을 자체 렌더링 위젯 이름으로 대응합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'layout-kivy': (
        'BoxLayout·GridLayout 배치 창',
        '세로 상자 안에 가로 버튼과 격자 폼을 올립니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'events-kivy': (
        'on_press·text 연결 창',
        '글자를 쓰면 미리보기가 바뀌고, 버튼은 인사를 확정합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'memo-window-kivy': (
        '메모장 뼈대 · 창과 여러 줄 TextInput만',
        '파일 버튼 전의 최소 화면입니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'memo-kivy': (
        '메모장 · Kivy 저장·열기 버튼',
        '여러 줄 TextInput과 파일 버튼으로 만든 메모 형태입니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
    'project-kivy': (
        '생활 도우미 · Kivy Spinner와 실행 버튼',
        '같은 core.logic을 주사위·D-day·추첨에 연결합니다. 이 예제를 Linux에서 실행해 캡처했습니다.'),
}


def _lesson(lesson_id):
    return next(item for item in units[2] if item['id'] == lesson_id)


ex('first-kivy', 'Kivy · 최소 창 실행 순서', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

Window.size = (480, 220)

class FirstApp(App):
    def build(self):
        self.title = "First window · Kivy"
        box = BoxLayout(padding=24)
        box.add_widget(Label(text="App -> build() -> run()", font_name=font))
        return box

FirstApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'App / build', 'signature': 'class FirstApp(App):\n    def build(self):\n        return Label(...)',
         'note': '앱 클래스입니다. build()가 첫 화면 위젯을 반환합니다. tkinter의 Tk()가 창과 앱을 겸하는 것과 다릅니다.'},
        {'name': 'Window.size', 'signature': 'Window.size = (480, 220)',
         'note': '처음 창 크기입니다. tkinter geometry, wx Frame size에 대응합니다. App보다 먼저 지정할 수 있습니다.'},
        {'name': 'run', 'signature': 'FirstApp().run()',
         'note': '이벤트 루프를 시작합니다. tkinter mainloop, Qt exec, wx MainLoop에 대응합니다.'},
    ],
    glossary=[
        {'term': '자체 렌더링', 'meaning': '운영체제 버튼이 아니라 Kivy가 직접 그립니다. 터치·여러 플랫폼 UI에 맞습니다.'},
        {'term': '브라우저 실행', 'meaning': 'Pyodide에는 Kivy가 없습니다. 이 페이지는 코드와 캡처로 가르치고, 실제 창은 PC에서 엽니다.'},
    ])

ex('widgets-label-entry-kivy', 'Label·TextInput · 한 줄 읽고 보여 주기', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Window.size = (420, 180)

class LabelEntryApp(App):
    def build(self):
        self.title = "Label and TextInput"
        box = BoxLayout(orientation="vertical", padding=16, spacing=8)
        box.add_widget(Label(text="Enter a name.", font_name=font, size_hint_y=None, height=32))
        self.entry = TextInput(multiline=False, font_name=font, size_hint_y=None, height=36)
        box.add_widget(self.entry)
        button = Button(text="Show", font_name=font, size_hint_y=None, height=40)
        button.bind(on_press=self.show_name)
        box.add_widget(button)
        self.result = Label(text="No input yet.", font_name=font)
        box.add_widget(self.result)
        return box

    def show_name(self, button):
        name = self.entry.text.strip() or "no name"
        self.result.text = "Name: " + name

LabelEntryApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'Label', 'signature': 'Label(text="설명", font_name=font)',
         'note': '짧은 글을 보여 줍니다. tkinter Label, wx StaticText에 대응합니다. 나중에 .text로 바꿉니다.'},
        {'name': 'TextInput.text', 'signature': 'entry = TextInput(multiline=False)\nentry.text',
         'note': '한 줄 입력의 현재 문자열입니다. Entry.get() / TextCtrl.GetValue()와 같습니다.'},
        {'name': 'on_press', 'signature': 'button.bind(on_press=self.show_name)',
         'note': '버튼을 누르는 순간에 함수를 부릅니다. command= / Bind(EVT_BUTTON)에 대응합니다. show_name()처럼 괄호를 붙이면 지금 실행됩니다.'},
    ],
    glossary=[{'term': '한 줄 입력', 'meaning': '이름·아이디처럼 줄바꿈이 없는 값입니다. 여러 줄 메모는 multiline=True를 씁니다.'}])

ex('widgets-choice-kivy', 'CheckBox·ToggleButton · 선택 값 읽기', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton

Window.size = (420, 280)

class ChoiceApp(App):
    def build(self):
        self.title = "Check and toggle"
        box = BoxLayout(orientation="vertical", padding=16, spacing=8)
        row = BoxLayout(size_hint_y=None, height=36)
        self.done = CheckBox(active=False, size_hint_x=None, width=40)
        row.add_widget(self.done)
        row.add_widget(Label(text="Practice done", font_name=font))
        box.add_widget(row)
        self.grades = []
        for i, value in enumerate(["Grade 1", "Grade 2", "Grade 3"]):
            toggle = ToggleButton(
                text=value, group="grade", font_name=font,
                state="down" if i == 0 else "normal", size_hint_y=None, height=36)
            self.grades.append(toggle)
            box.add_widget(toggle)
        self.result = Label(text="Check is independent. Toggle group picks one.", font_name=font)
        box.add_widget(self.result)
        button = Button(text="Read choice", font_name=font, size_hint_y=None, height=40)
        button.bind(on_press=self.show_choice)
        box.add_widget(button)
        return box

    def show_choice(self, button):
        extra = "done" if self.done.active else "not done"
        grade = next((item.text for item in self.grades if item.state == "down"), "?")
        self.result.text = f"{grade} · {extra}"

ChoiceApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'CheckBox.active', 'signature': 'done = CheckBox(active=False)\ndone.active',
         'note': '서로 독립적으로 켜고 끌 수 있습니다. True 또는 False입니다. BooleanVar가 따로 없습니다.'},
        {'name': 'ToggleButton / group', 'signature': 'ToggleButton(text="Grade 1", group="grade")',
         'note': '같은 group 문자열을 주면 하나만 내려간 상태(state="down")가 됩니다. RadioButton / RB_GROUP에 대응합니다.'},
    ],
    glossary=[{'term': '제어 변수 없음', 'meaning': 'tkinter는 BooleanVar에 상태를 둡니다. Kivy는 위젯 속성(active, state)에서 읽습니다.'}])

ex('widgets-kivy', 'Kivy 위젯 도감', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

Window.size = (420, 520)

class ColorBlock(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0.84, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class WidgetsApp(App):
    def build(self):
        self.title = "Kivy widget gallery"
        box = BoxLayout(orientation="vertical", padding=12, spacing=6)
        box.add_widget(Label(text="Label: short text", font_name=font, size_hint_y=None, height=28))
        box.add_widget(TextInput(multiline=False, font_name=font, size_hint_y=None, height=36))
        box.add_widget(TextInput(multiline=True, font_name=font, size_hint_y=None, height=64))
        row = BoxLayout(size_hint_y=None, height=32)
        self.checked = CheckBox(active=True, size_hint_x=None, width=40)
        row.add_widget(self.checked)
        row.add_widget(Label(text="Done", font_name=font))
        box.add_widget(row)
        for i, value in enumerate(["A", "B"]):
            box.add_widget(ToggleButton(
                text=value, group="pick", font_name=font,
                state="down" if i == 0 else "normal", size_hint_y=None, height=32))
        box.add_widget(Spinner(text="module", values=["module", "package", "GUI"], font_name=font, size_hint_y=None, height=36))
        box.add_widget(ColorBlock(size_hint_y=None, height=48))
        button = Button(text="Print check", font_name=font, size_hint_y=None, height=40)
        button.bind(on_press=lambda btn: print(self.checked.active))
        box.add_widget(button)
        return box

WidgetsApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'multiline=True', 'signature': 'TextInput(multiline=True)',
         'note': '여러 줄 입력입니다. 한 줄은 multiline=False입니다. tkinter Text, wx TE_MULTILINE에 대응합니다.'},
        {'name': 'Spinner', 'signature': 'Spinner(text="module", values=["module", "package"])',
         'note': '목록에서 고릅니다. Listbox / wx.ListBox / QComboBox를 드롭다운으로 대신합니다.'},
        {'name': 'canvas', 'signature': 'with self.canvas:\n    Color(1, 0.84, 0)\n    Rectangle(...)',
         'note': '도형 Canvas와 일대일은 아닙니다. canvas에 색과 사각형을 올려 “그리기 자리”를 표시합니다.'},
    ],
    glossary=[{'term': '이름 대응', 'meaning': 'Label→Label, Entry→TextInput, Text→multiline, Check→CheckBox, List→Spinner입니다. 역할로 외우세요.'}])

ex('layout-kivy', 'Kivy · 상자 배치와 격자 폼', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Window.size = (520, 260)

class LayoutApp(App):
    def build(self):
        self.title = "Kivy layout"
        vertical = BoxLayout(orientation="vertical", padding=12, spacing=8)
        horizontal = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=44)
        for name in ["Open", "Save", "Quit"]:
            horizontal.add_widget(Button(text=name, font_name=font))
        vertical.add_widget(horizontal)
        grid = GridLayout(cols=2, spacing=8, size_hint_y=None, height=96)
        grid.add_widget(Label(text="ID", font_name=font))
        grid.add_widget(TextInput(multiline=False, font_name=font))
        grid.add_widget(Label(text="Password", font_name=font))
        grid.add_widget(TextInput(multiline=False, password=True, font_name=font))
        vertical.add_widget(grid)
        return vertical

LayoutApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'BoxLayout', 'signature': 'BoxLayout(orientation="vertical")\nBoxLayout(orientation="horizontal")',
         'note': '세로 묶음과 가로 묶음입니다. pack / QVBoxLayout·QHBoxLayout / BoxSizer에 대응합니다.'},
        {'name': 'size_hint', 'signature': 'Button(..., size_hint_y=None, height=44)',
         'note': 'size_hint는 부모 공간의 비율입니다. None이면 height·width 픽셀을 씁니다. wx Add의 비율 숫자와 같은 생각입니다.'},
        {'name': 'GridLayout', 'signature': 'grid = GridLayout(cols=2, spacing=8)',
         'note': '열 개수를 정한 격자입니다. tkinter grid, wx FlexGridSizer에 대응합니다.'},
        {'name': 'password=True', 'signature': 'TextInput(multiline=False, password=True)',
         'note': '입력 글자를 가립니다. Entry의 show="*" / wx TE_PASSWORD와 같은 목적입니다.'},
    ],
    glossary=[{'term': 'Layout', 'meaning': '위젯의 자리를 정하는 배치 관리자입니다. add_widget으로 자식만 올리면 됩니다. pack을 따로 호출하지 않습니다.'}])

ex('events-kivy', 'bind · on_press와 text', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Window.size = (420, 200)

class EventsApp(App):
    def build(self):
        self.title = "Events · Kivy"
        box = BoxLayout(orientation="vertical", padding=16, spacing=8)
        self.entry = TextInput(multiline=False, font_name=font, size_hint_y=None, height=36)
        self.entry.bind(text=self.preview)
        box.add_widget(self.entry)
        button = Button(text="Greet", font_name=font, size_hint_y=None, height=40)
        button.bind(on_press=self.greet)
        box.add_widget(button)
        self.result = Label(text="Type to see a preview.", font_name=font)
        box.add_widget(self.result)
        return box

    def greet(self, button):
        name = self.entry.text.strip() or "everyone"
        self.result.text = f"Hello, {name}!"

    def preview(self, widget, value):
        self.result.text = f"Preview: {value or 'empty'}"

EventsApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'bind', 'signature': 'button.bind(on_press=self.greet)',
         'note': '사건에 함수를 맡깁니다. command= / clicked.connect / Bind에 대응합니다. greet()를 넘기면 창을 만들 때 이미 실행됩니다.'},
        {'name': 'on_press', 'signature': 'button.bind(on_press=self.greet)',
         'note': '버튼을 누르는 순간입니다. 처리 함수는 위젯 인자 하나를 받습니다. 쓰지 않아도 매개변수는 있어야 합니다.'},
        {'name': 'text 속성', 'signature': 'entry.bind(text=self.preview)\ndef preview(self, widget, value):',
         'note': '한 글자가 바뀔 때마다 preview(widget, value)를 호출합니다. Qt textChanged, wx EVT_TEXT와 같습니다.'},
        {'name': '위젯 인자', 'signature': 'def greet(self, button):',
         'note': 'Kivy는 이벤트를 보낸 위젯을 넘깁니다. tkinter command는 인자가 없습니다. 함수 머리를 그대로 옮기면 TypeError가 납니다.'},
    ],
    glossary=[
        {'term': '속성 이벤트', 'meaning': 'bind(text=...)처럼 속성 이름이 사건입니다. 값이 바뀔 때 함수가 호출됩니다.'},
        {'term': '지금 호출', 'meaning': 'bind(on_press=self.greet())는 창을 만들 때 이미 실행됩니다. 함수 이름만 넘기세요.'},
    ])

ex('memo-window-kivy', '메모장 ① · 창과 여러 줄 TextInput만', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

Window.size = (640, 420)

class MemoWindowApp(App):
    def build(self):
        self.title = "Memo · window only"
        self.editor = TextInput(multiline=True, font_name=font)
        return self.editor

MemoWindowApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'Window.size', 'signature': 'Window.size = (640, 420)',
         'note': '처음 창 크기입니다. tkinter geometry("640x420")에 대응합니다.'},
        {'name': 'multiline=True', 'signature': 'TextInput(multiline=True)',
         'note': '여러 줄 편집기가 창을 채웁니다. build()가 이 위젯만 반환하면 레이아웃 없이 가득 찹니다.'},
    ],
    glossary=[{'term': '단계 1', 'meaning': '창과 편집기만 있으면 메모장의 뼈대입니다. 열기·저장은 다음 예제입니다.'}])

ex('memo-kivy', '메모 형태 · Kivy 저장·열기 버튼', {'main.py': FONT + '''from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Window.size = (640, 420)

class MemoApp(App):
    def build(self):
        self.title = "Memo · Kivy"
        self.path = Path("memo.txt")
        root = BoxLayout(orientation="vertical", padding=8, spacing=8)
        bar = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=40)
        for name, handler in [("Open", self.open_file), ("Save", self.save_file), ("Clear", self.clear_text)]:
            button = Button(text=name, font_name=font)
            button.bind(on_press=handler)
            bar.add_widget(button)
        root.add_widget(bar)
        self.editor = TextInput(multiline=True, font_name=font)
        root.add_widget(self.editor)
        self.status = Label(text="Buttons write memo.txt in this folder.", font_name=font, size_hint_y=None, height=28)
        root.add_widget(self.status)
        return root

    def open_file(self, button):
        if not self.path.exists():
            self.status.text = "No memo.txt yet. Save first or cancel stays empty."
            return
        try:
            self.editor.text = self.path.read_text(encoding="utf-8")
            self.status.text = "Opened memo.txt"
        except (OSError, UnicodeError) as error:
            self.status.text = "Open failed: " + str(error)

    def save_file(self, button):
        try:
            self.path.write_text(self.editor.text, encoding="utf-8")
            self.status.text = "Saved memo.txt"
        except (OSError, UnicodeError) as error:
            self.status.text = "Save failed: " + str(error)

    def clear_text(self, button):
        self.editor.text = ""
        self.status.text = "Cleared. File is unchanged until Save."

MemoApp().run()'''}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'Path.read_text / write_text', 'signature': 'Path("memo.txt").write_text(self.editor.text, encoding="utf-8")',
         'note': 'UTF-8로 읽고 씁니다. tk/wx 메모장과 같은 파일 내용입니다. 운영체제 파일 대화 상자는 쓰지 않습니다.'},
        {'name': '없는 파일', 'signature': 'if not self.path.exists():\n    return',
         'note': '열을 파일이 없으면 편집기를 비우지 않습니다. wx FileDialog에서 취소를 누른 것과 같은 분기입니다.'},
        {'name': 'status Label', 'signature': 'self.status.text = "Saved memo.txt"',
         'note': '성공·실패를 창 안에 보여 줍니다. MessageBox / filedialog 대신 상태 줄을 씁니다.'},
    ],
    glossary=[
        {'term': 'memo-ish', 'meaning': 'Kivy는 OS 메뉴·파일 대화 상자가 기본이 아닙니다. FileChooser를 붙일 수 있지만, 먼저 고정 파일로 열기·저장 분기를 익힙니다.'},
        {'term': '취소 시험', 'meaning': '파일이 없을 때 Open을 눌러 보세요. 기존 글이 그대로면 분기가 맞은 것입니다.'},
    ])

ex('project-kivy', '생활 도우미 · Kivy', {'main.py': FONT + '''from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from core.logic import roll, days_left, draw

Window.size = (520, 280)

class HelperApp(App):
    def build(self):
        self.title = "Class helper · Kivy"
        box = BoxLayout(orientation="vertical", padding=12, spacing=8)
        self.mode = Spinner(text="Dice", values=["Dice", "D-day", "Draw"], font_name=font, size_hint_y=None, height=40)
        box.add_widget(self.mode)
        box.add_widget(Label(text="sides / YYYY-MM-DD / comma names", font_name=font, size_hint_y=None, height=28))
        self.entry = TextInput(text="6", multiline=False, font_name=font, size_hint_y=None, height=36)
        box.add_widget(self.entry)
        button = Button(text="Run", font_name=font, size_hint_y=None, height=40)
        button.bind(on_press=self.run_task)
        box.add_widget(button)
        self.result = Label(text="Result appears here.", font_name=font)
        box.add_widget(self.result)
        return box

    def run_task(self, button):
        try:
            value = self.entry.text
            mode = self.mode.text
            if mode == "Dice":
                output = str(roll(int(value)))
            elif mode == "D-day":
                output = str(days_left(value)) + " days"
            else:
                output = ", ".join(draw(value.split(","), 1))
            self.result.text = output
        except ValueError as error:
            Popup(title="Check input", content=Label(text=str(error), font_name=font), size_hint=(0.8, 0.4)).open()

HelperApp().run()''' , **core}, mode='pc', note=NOTE,
    pre_api=[
        {'name': 'from core.logic import roll', 'signature': 'from core.logic import roll, days_left, draw',
         'note': '화면 파일은 계산을 직접 쓰지 않습니다. 웹의 core 예제·tk/PySide/wx 생활 도우미와 같은 함수입니다.'},
        {'name': 'Spinner', 'signature': 'self.mode = Spinner(text="Dice", values=["Dice", "D-day", "Draw"])\nself.mode.text',
         'note': '드롭다운으로 모드를 고릅니다. tkinter 라디오, Qt QComboBox, wx Choice를 한 위젯으로 대신합니다.'},
        {'name': 'Popup', 'signature': 'Popup(title="Check input", content=Label(text=메시지), size_hint=(0.8, 0.4)).open()',
         'note': '잘못된 입력을 창으로 알립니다. messagebox.showwarning / wx.MessageBox에 대응합니다.'},
    ],
    glossary=[{'term': '화면과 기능 분리', 'meaning': 'core에는 Kivy가 없습니다. 같은 roll을 네 GUI에서 부를 수 있습니다.'}])

lesson(2, 'kivy', '부록 · Kivy로 같은 앱 다시 만들기', '부록 · 확장 학습',
       '본편에서 익힌 창·위젯·배치·이벤트·메모장을 자체 렌더링 터치 UI로 옮깁니다.',
       [
           '이 페이지는 본편 tkinter/PySide6 경로와 wxPython 부록을 대체하지 않습니다. 같은 인사·위젯 도감·배치·이벤트·메모 형태·생활 도우미를 Kivy로 다시 구성합니다. 수행평가의 기본 도구는 여전히 tkinter입니다.',
           '브라우저의 Pyodide에는 Kivy가 포함되지 않습니다. C 확장과 창 시스템을 불러올 수 없어 웹 실습실은 창을 열지 않습니다. 문법을 확인하고, 아래 코드와 실행 화면으로 역할을 배웁니다. 실제 창·버튼·파일 저장은 PC에서 확인하세요. 가상환경을 켠 뒤 python -m pip install kivy 를 실행하고 python main.py로 엽니다. Windows PowerShell은 .venv\\Scripts\\Activate.ps1, macOS/Linux는 source .venv/bin/activate입니다.',
           '실행 순서는 App 클래스 → build()가 위젯을 반환 → run()입니다. tkinter의 Tk·pack·command·mainloop, Qt의 QApplication·Layout·connect·exec, wx의 App·Sizer·Bind·MainLoop를 역할로 옮기세요. 단어만 바꾸면 bind 인자의 위젯 매개변수에서 막힙니다.',
           '위젯 이름은 Label→Label, Entry→TextInput(multiline=False), Text→TextInput(multiline=True), Checkbutton→CheckBox, Radiobutton→ToggleButton(같은 group), Listbox→Spinner, Button→Button입니다. 체크 상태는 BooleanVar가 아니라 active로 읽습니다.',
           '배치는 BoxLayout(orientation="vertical"/"horizontal")과 GridLayout(cols=...)입니다. size_hint는 부모 공간의 비율이고, None이면 height 픽셀을 씁니다. 이벤트는 button.bind(on_press=self.greet)처럼 함수 자체를 맡깁니다. greet()를 넘기면 창을 만들 때 이미 실행됩니다.',
           '메모는 OS 메뉴·파일 대화 상자 대신 Open/Save 버튼과 memo.txt로 같은 열기·저장·없는 파일 분기를 만듭니다. FileChooser를 붙이면 경로를 고를 수 있습니다. 생활 도우미는 같은 core.logic을 Spinner에 연결합니다. 빈 입력·0면 주사위·잘못된 날짜를 시험하세요. 기본 글꼴은 한글을 가정하지 않으므로 캡처는 영어 문구입니다.',
       ],
       KIVY_EXAMPLES,
       [
           '본편 위젯 하나를 골라 Kivy 이름을 짝 짓고, 값을 읽는 속성을 적으세요.',
           'memo.txt가 없을 때 Open을 누르면 기존 글이 남는지 설명하세요.',
           '웹에서 실행 버튼이 창을 열지 않는 이유를 한 문장으로 적으세요.',
       ],
       extra=True)


def apply():
    """Register the appendix topic, Kivy API cards, and screenshot catalog."""
    import unit2_shots
    hello = examples['hello-kivy']
    if not hello['pre_api']:
        hello['pre_api'] = api_items([
            {'name': 'App / build', 'signature': 'class GreetingApp(App):\n    def build(self):\n        return box',
             'note': '앱 클래스입니다. build()가 첫 화면을 반환합니다. 창보다 앱이 먼저입니다.'},
            {'name': 'BoxLayout', 'signature': 'box = BoxLayout(orientation="vertical", padding=16, spacing=8)',
             'note': '위에서 아래로 붙입니다. pack() 대신 Layout이 자리를 정합니다.'},
            {'name': 'TextInput', 'signature': 'self.entry = TextInput(multiline=False)\nself.entry.text  ·  self.entry.text = ""',
             'note': '한 줄 입력입니다. tkinter Entry의 get/delete에 대응합니다.'},
            {'name': 'bind', 'signature': 'button.bind(on_press=self.greet)',
             'note': '누르는 사건에 함수를 맡깁니다. bind(..., self.greet())처럼 괄호를 붙이면 지금 실행됩니다. greet는 버튼 인자를 받습니다.'},
            {'name': 'run', 'signature': 'GreetingApp().run()',
             'note': '이벤트 루프입니다. tkinter mainloop / Qt exec / wx MainLoop에 대응합니다.'},
        ])
    if not hello['glossary']:
        hello['glossary'] = glossary_items([
            {'term': 'Kivy', 'meaning': '자체 렌더링 GUI 도구입니다. 운영체제 위젯이 아니라 터치·여러 플랫폼 화면에 맞습니다.'},
            {'term': '위젯 인자', 'meaning': '처리 함수의 첫 매개변수입니다. 쓰지 않아도 선언해야 TypeError가 나지 않습니다.'},
        ])
    hello['note'] = NOTE

    kivy_lesson = _lesson('kivy')
    kivy_lesson['examples'] = list(KIVY_EXAMPLES)
    kivy_lesson['pre_api'] = api_items([
        {'name': '실행 순서', 'signature': 'App 클래스 → build() → run()',
         'note': '본편 Tk·pack·command·mainloop를 Kivy 이름으로 옮긴 순서입니다. 브라우저에서는 창이 뜨지 않습니다.'},
    ])
    kivy_lesson['glossary'] = glossary_items([
        {'term': '부록', 'meaning': '본편을 다시 배우는 길이 아닙니다. 같은 앱을 네 번째 툴킷으로 대조하는 확장입니다.'},
        {'term': 'Pyodide', 'meaning': '사이트 안의 Python입니다. C 확장인 Kivy를 불러올 수 없어 PC 실습으로 표시합니다.'},
    ])

    libraries = _lesson('libraries')
    pointer = '위젯·배치·이벤트·메모 형태를 Kivy로 다시 만드는 과정은 부록 주제에서 이어집니다. 본편 tkinter/PySide6와 wxPython 부록 경로는 그대로입니다.'
    if pointer not in libraries['paragraphs']:
        libraries['paragraphs'].append(pointer)

    unit2_shots.OWN.update(OWN)
    unit2_shots.LESSON['kivy'] = (
        'widgets-kivy.png', 'Kivy 위젯 도감 실행 화면',
        '본편에서 고른 위젯을 Kivy 이름으로 옮긴 뒤 값을 읽어 보세요. 이 예제를 Linux에서 실행해 캡처했습니다.',
    )
