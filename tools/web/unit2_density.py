"""Unit II extra examples for #52. Imported at the end of content.py.

Adds focused tk/PySide labs so widgets·layout·events·memo (and nearby topics)
are independently complete. New APIs use pre_api/glossary. Example screenshots
are attached later by unit2_shots (#54).
"""
from content import ex, units, core

SHOT_TK = [{'src': 'tk.png', 'alt': 'tkinter 인사 앱 실행 화면 · 이름 입력창과 인사 및 초기화 버튼',
            'caption': '같은 인사를 GUI로 만들면 이런 창이 됩니다. OS·테마에 따라 외형은 달라집니다.'}]


def _lesson(lesson_id):
    return next(lesson for lesson in units[2] if lesson['id'] == lesson_id)


def _set_examples(lesson_id, ids):
    _lesson(lesson_id)['examples'] = list(ids)


ex('ui-cli', '같은 인사 · 명령줄(CLI)', {'main.py': '''name = input("이름: ").strip() or "여러분"
print(f"{name}님, 안녕하세요!")'''},
    stdin='민지',
    pre_api=[
        {'name': 'input', 'signature': 'name = input("이름: ")', 'note': '터미널에 질문을 보여주고, 한 줄 입력을 문자열로 받습니다. GUI의 Entry와 같은 역할입니다.'},
        {'name': 'print', 'signature': 'print(f"{name}님, 안녕하세요!")', 'note': '결과를 글자로 보여 줍니다. GUI의 Label.config(text=...)와 같은 역할입니다.'},
    ],
    glossary=[
        {'term': 'CLI', 'meaning': '명령어를 타이핑해서 프로그램을 다루는 방식입니다. 반복 작업에 유리합니다.'},
        {'term': 'GUI', 'meaning': '버튼·입력창처럼 눈에 보이는 부품을 조작하는 방식입니다. 다음 예제 hello-tk가 같은 인사를 창으로 만듭니다.'},
        {'term': 'NUI', 'meaning': '음성·손짓·터치처럼 일상 행동으로 의도를 전달하는 방식입니다.'},
    ])

ex('widgets-label-entry-tk', 'Label·Entry · 한 줄 읽고 보여 주기', {'main.py': '''import tkinter as tk

def show_name():
    name = entry.get().strip() or "이름 없음"
    result.config(text=f"입력한 이름: {name}")

root = tk.Tk()
root.title("Label과 Entry")
root.geometry("420x180")
tk.Label(root, text="이름을 입력하세요.").pack(pady=8)
entry = tk.Entry(root)
entry.pack(fill="x", padx=24)
tk.Button(root, text="표시", command=show_name).pack(pady=8)
result = tk.Label(root, text="아직 입력이 없습니다.")
result.pack()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'Label', 'signature': 'tk.Label(parent, text="설명")', 'note': '짧은 글을 보여 줍니다. 나중에 config(text=...)로 바꿀 수 있습니다.'},
        {'name': 'Entry.get', 'signature': 'entry.get()', 'note': '한 줄 입력의 현재 문자열을 읽습니다. 위치 인자가 필요 없습니다.'},
        {'name': 'Label.config', 'signature': 'result.config(text=새글자)', 'note': '이미 만든 라벨의 속성만 바꿉니다. 새 Label을 또 만들면 화면에 겹칩니다.'},
    ],
    glossary=[{'term': '한 줄 입력', 'meaning': '이름·아이디처럼 줄바꿈이 없는 값입니다. 여러 줄 소개문은 Text를 씁니다.'}])

ex('widgets-choice-tk', 'Checkbutton·Radiobutton · 선택 값 읽기', {'main.py': '''import tkinter as tk

def show_choice():
    extra = "완료" if done.get() else "미완료"
    print(done.get(), grade.get(), extra)
    result.config(text=f"{grade.get()} · {extra}")

root = tk.Tk()
root.title("체크와 라디오")
root.geometry("420x240")
done = tk.BooleanVar()
tk.Checkbutton(root, text="오늘 실습 완료", variable=done).pack(anchor="w", padx=16, pady=8)
grade = tk.StringVar(value="1학년")
for value in ["1학년", "2학년", "3학년"]:
    tk.Radiobutton(root, text=value, variable=grade, value=value).pack(anchor="w", padx=16)
tk.Button(root, text="선택 확인", command=show_choice).pack(pady=8)
result = tk.Label(root, text="체크는 여러 개, 라디오는 하나.")
result.pack()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'BooleanVar', 'signature': 'done = tk.BooleanVar()', 'note': '체크 상태는 위젯이 아니라 변수에 저장됩니다. done.get()이 True 또는 False입니다.'},
        {'name': 'Checkbutton', 'signature': 'tk.Checkbutton(parent, text=..., variable=done)', 'note': '서로 독립적으로 켜고 끌 수 있습니다. 약관 동의처럼 "해도 되고 안 해도 되는" 선택입니다.'},
        {'name': 'StringVar / Radiobutton', 'signature': 'grade = tk.StringVar(value="1학년")\ntk.Radiobutton(..., variable=grade, value="1학년")', 'note': '같은 variable을 쓰는 라디오는 하나만 선택됩니다. value가 서로 달라야 구분됩니다.'},
    ],
    glossary=[{'term': '확인학습 57쪽', 'meaning': 'IDLE 화면의 Frame·Button처럼 눈에 보이는 부품을 통틀어 위젯이라고 합니다.'}])

ex('widgets-list-canvas-tk', 'Listbox·Canvas · 목록과 그리기', {'main.py': '''import tkinter as tk

def show_pick():
    selected = listbox.curselection()
    if not selected:
        result.config(text="항목을 먼저 고르세요.")
        return
    name = listbox.get(selected[0])
    result.config(text=f"선택한 주제: {name}")
    canvas.delete("all")
    canvas.create_text(120, 30, text=name, font=("sans-serif", 14))

root = tk.Tk()
root.title("목록과 캔버스")
root.geometry("420x280")
listbox = tk.Listbox(root, height=4)
for value in ["모듈", "패키지", "GUI"]:
    listbox.insert(tk.END, value)
listbox.pack(fill="x", padx=16, pady=8)
canvas = tk.Canvas(root, width=240, height=60, bg="white")
canvas.create_oval(10, 10, 50, 50, fill="gold")
canvas.pack()
tk.Button(root, text="선택 그리기", command=show_pick).pack(pady=8)
result = tk.Label(root, text="목록에서 고른 뒤 버튼을 누르세요.")
result.pack()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'Listbox.insert', 'signature': 'listbox.insert(tk.END, value)', 'note': '목록 끝에 항목을 넣습니다. tk.END는 "지금 목록의 끝"입니다.'},
        {'name': 'curselection', 'signature': 'listbox.curselection()', 'note': '고른 칸의 인덱스 튜플을 반환합니다. 아무 것도 안 골랐으면 빈 튜플입니다.'},
        {'name': 'Canvas.create_oval', 'signature': 'canvas.create_oval(x1, y1, x2, y2, fill=...)', 'note': '왼쪽 위 (x1,y1)과 오른쪽 아래 (x2,y2)로 타원을 그립니다. 버튼이 아니라 좌표입니다.'},
        {'name': 'Canvas.delete', 'signature': 'canvas.delete("all")', 'note': '그린 도형을 지웁니다. 다시 그리기 전에 호출하면 겹치지 않습니다.'},
    ])

ex('widgets-pyside-form', 'PySide6 · 입력·체크·라디오 폼', {'main.py': '''import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QCheckBox, QRadioButton, QPushButton, QButtonGroup)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("입력 폼 · PySide6")
window.resize(420, 260)
layout = QVBoxLayout(window)
layout.addWidget(QLabel("이름을 입력하세요."))
entry = QLineEdit()
layout.addWidget(entry)
done = QCheckBox("오늘 실습 완료")
layout.addWidget(done)
group = QButtonGroup(window)
for value in ["1학년", "2학년", "3학년"]:
    radio = QRadioButton(value)
    group.addButton(radio)
    layout.addWidget(radio)
group.buttons()[0].setChecked(True)
result = QLabel("값을 읽고 아래에 표시합니다.")
layout.addWidget(result)

def show_choice():
    extra = "완료" if done.isChecked() else "미완료"
    picked = group.checkedButton()
    grade = picked.text() if picked else "?"
    result.setText(f"{entry.text().strip() or '이름 없음'} · {grade} · {extra}")

button = QPushButton("선택 확인")
button.clicked.connect(show_choice)
layout.addWidget(button)
window.show()
sys.exit(app.exec())'''}, mode='pc',
    pre_api=[
        {'name': 'QLineEdit', 'signature': 'entry = QLineEdit()', 'note': '한 줄 입력입니다. text()로 읽고, clear()로 지웁니다. tkinter Entry에 대응합니다.'},
        {'name': 'QCheckBox.isChecked', 'signature': 'done.isChecked()', 'note': '체크 여부를 bool로 읽습니다. BooleanVar 없이 위젯이 상태를 가집니다.'},
        {'name': 'QButtonGroup', 'signature': 'group = QButtonGroup(window)\ngroup.addButton(radio)', 'note': '라디오를 한 묶음으로 만듭니다. checkedButton()으로 지금 선택된 버튼을 얻습니다.'},
        {'name': 'QLabel.setText', 'signature': 'result.setText("새 글자")', 'note': '표시 문자열을 바꿉니다. result.text = "..."처럼 속성을 새로 만들면 화면에 반영되지 않습니다.'},
    ])

ex('layout-pack-tk', 'pack · expand와 fill', {'main.py': '''import tkinter as tk

root = tk.Tk()
root.title("pack · expand와 fill")
root.geometry("420x240")
tk.Label(root, text="위쪽은 가로만 늘어남", bg="#dbeafe").pack(fill="x")
tk.Button(root, text="가운데는 남은 공간을 채움", bg="#fef3c7").pack(expand=True, fill="both", padx=8, pady=8)
tk.Button(root, text="아래도 가로는 채움").pack(fill="x")
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'fill', 'signature': '위젯.pack(fill="x")', 'note': '배치 관리자가 준 칸 안에서 위젯을 늘리는 방향입니다. "x"는 가로, "both"는 가로·세로입니다.'},
        {'name': 'expand', 'signature': '위젯.pack(expand=True, fill="both")', 'note': '창에 남는 공간을 이 위젯에게 더 줄지 정합니다. expand만 켜고 fill을 빼면 칸은 커져도 위젯은 작습니다.'},
        {'name': 'side', 'signature': '위젯.pack(side="left")', 'note': '붙이는 방향입니다. 기본은 "top"(위에서 아래)입니다.'},
    ],
    glossary=[{'term': '창을 늘려 보기', 'meaning': '배치를 시험할 때는 창 모서리를 드래그하세요. 잘리거나 빈 칸이 생기면 fill·expand를 점검합니다.'}])

ex('layout-grid-tk', 'grid · 로그인 폼과 sticky', {'main.py': '''import tkinter as tk

root = tk.Tk()
root.title("grid · 로그인 폼")
root.geometry("420x200")
frame = tk.Frame(root, padx=16, pady=16)
frame.pack(fill="both", expand=True)
frame.columnconfigure(1, weight=1)
tk.Label(frame, text="아이디").grid(row=0, column=0, sticky="e", padx=6, pady=6)
tk.Entry(frame).grid(row=0, column=1, sticky="ew")
tk.Label(frame, text="비밀번호").grid(row=1, column=0, sticky="e", padx=6, pady=6)
tk.Entry(frame, show="*").grid(row=1, column=1, sticky="ew")
tk.Label(frame, text="계정 정보", bg="#dbeafe").grid(row=0, column=2, rowspan=2, sticky="ns", padx=8)
tk.Button(frame, text="로그인").grid(row=2, column=0, columnspan=3, sticky="ew", pady=8)
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'grid', 'signature': '위젯.grid(row=0, column=1)', 'note': '행·열 번호로 칸을 정합니다. 표 같은 입력 폼에 맞습니다.'},
        {'name': 'sticky', 'signature': '위젯.grid(..., sticky="ew")', 'note': '칸보다 위젯이 작을 때 어느 벽에 붙일지입니다. "ew"는 좌우로 늘립니다.'},
        {'name': 'columnconfigure', 'signature': 'frame.columnconfigure(1, weight=1)', 'note': '남는 가로 공간을 그 열에 줍니다. weight를 빼면 창을 늘려도 입력창이 늘어나지 않습니다.'},
        {'name': 'columnspan', 'signature': '위젯.grid(..., columnspan=3)', 'note': '로그인 버튼을 세 열에 걸쳐 놓습니다.'},
        {'name': 'rowspan', 'signature': '위젯.grid(row=0, column=2, rowspan=2)', 'note': '계정 정보 안내를 두 입력 행에 걸쳐 놓습니다. sticky="ns"로 세로를 채웁니다.'},
        {'name': 'show', 'signature': 'tk.Entry(parent, show="*")', 'note': '입력 칸에 실제 글자 대신 *를 보여 줍니다. 비밀번호 칸에 씁니다.'},
    ],
    glossary=[{'term': '같은 부모에서 pack+grid', 'meaning': '한 Frame 안에서 pack과 grid를 섞으면 배치 충돌이 납니다. 다른 Frame으로 나누면 각각 쓸 수 있습니다.'}])

ex('layout-pyside-form', 'PySide6 · QGridLayout 입력 폼', {'main.py': '''import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel,
    QLineEdit, QPushButton)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("격자 폼 · PySide6")
window.resize(420, 180)
grid = QGridLayout(window)
grid.addWidget(QLabel("아이디"), 0, 0)
grid.addWidget(QLineEdit(), 0, 1)
grid.addWidget(QLabel("비밀번호"), 1, 0)
secret = QLineEdit()
secret.setEchoMode(QLineEdit.EchoMode.Password)
grid.addWidget(secret, 1, 1)
grid.addWidget(QPushButton("로그인"), 2, 0, 1, 2)
window.show()
sys.exit(app.exec())'''}, mode='pc',
    pre_api=[
        {'name': 'QGridLayout', 'signature': 'grid = QGridLayout(window)', 'note': '행·열로 위젯을 놓습니다. tkinter grid에 대응합니다.'},
        {'name': 'addWidget', 'signature': 'grid.addWidget(위젯, 행, 열)\ngrid.addWidget(위젯, 행, 열, 행개수, 열개수)', 'note': '네 숫자를 주면 여러 칸을 차지합니다. 로그인 버튼은 두 열을 씁니다.'},
        {'name': 'setEchoMode', 'signature': 'secret.setEchoMode(QLineEdit.EchoMode.Password)', 'note': '입력 글자를 가립니다. tkinter Entry의 show="*"와 같은 목적입니다.'},
    ])

ex('events-callback', '콜백 · 지금 호출 vs 나중에 호출', {'main.py': '''def greet():
    print("인사를 실행했습니다.")
    return "반환값"

print("1) command=greet() 처럼 지금 호출하면")
wrong = greet()
print("저장된 값:", wrong)

print("2) command=greet 처럼 함수 자체를 저장하면")
right = greet
print("아직 두 번째 인사는 없습니다.")
print("클릭을 흉내 내어 호출합니다.")
right()
print("저장된 값은 함수 객체입니다:", right.__name__)'''},
    pre_api=[
        {'name': '함수 전달', 'signature': 'command=greet', 'note': '함수 이름만 넘깁니다. 클릭(또는 나중에 right())할 때 실행됩니다.'},
        {'name': '지금 호출', 'signature': 'command=greet()', 'note': '괄호가 있으면 버튼을 만드는 순간에 실행되고, command에는 반환값(없으면 None)이 들어갑니다.'},
    ],
    glossary=[
        {'term': '콜백', 'meaning': '나중에 사건이 났을 때 불러 달라고 맡겨 두는 함수입니다.'},
        {'term': '교과서 59쪽 5', 'meaning': 'command=say_hello는 버튼을 클릭할 때 실행됩니다. 생성 직후가 아닙니다.'},
    ])

ex('events-command-tk', 'Button.command · 올바른 연결과 잘못된 연결', {'main.py': '''import tkinter as tk

def greet():
    log.insert(tk.END, "클릭할 때 인사\\n")

def too_early():
    log.insert(tk.END, "버튼을 만들기 전에 이미 실행됨\\n")

root = tk.Tk()
root.title("command 전달 비교")
root.geometry("420x240")
log = tk.Text(root, height=8)
log.pack(fill="both", expand=True, padx=8, pady=8)
tk.Button(root, text="올바른 연결 command=greet", command=greet).pack(fill="x", padx=8)
tk.Button(root, text="잘못된 연결 command=too_early()", command=too_early()).pack(fill="x", padx=8, pady=8)
log.insert(tk.END, "창이 열린 직후 기록을 보세요.\\n")
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'command=함수', 'signature': 'tk.Button(parent, command=greet)', 'note': '함수 객체를 보관합니다. 클릭하면 greet()가 실행됩니다.'},
        {'name': 'command=함수()', 'signature': 'tk.Button(parent, command=too_early())', 'note': '버튼을 만드는 줄에서 이미 실행됩니다. 클릭해도 다시 실행되지 않거나, 반환값 None이 연결되어 반응이 없습니다.'},
    ],
    glossary=[{'term': '인자가 필요할 때', 'meaning': 'greet(name)처럼 값이 필요하면 command=lambda: greet(name)으로 호출을 감쌉니다. lambda greet(name)처럼 쓰면 문법 오류입니다.'}])

ex('events-bind-tk', 'bind · Enter 키로 같은 함수 호출', {'main.py': '''import tkinter as tk

def greet(event=None):
    name = entry.get().strip() or "여러분"
    result.config(text=f"{name}님, 안녕하세요!")

root = tk.Tk()
root.title("bind · Enter 키")
root.geometry("420x180")
entry = tk.Entry(root)
entry.pack(fill="x", padx=20, pady=12)
entry.bind("<Return>", greet)
tk.Button(root, text="인사하기", command=greet).pack()
result = tk.Label(root, text="이름을 쓰고 Enter를 눌러 보세요.")
result.pack(pady=12)
entry.focus()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'bind', 'signature': 'entry.bind("<Return>", greet)', 'note': '특정 사건(여기선 Enter)이 나면 greet을 호출합니다. command는 버튼 클릭 전용, bind는 키·마우스 등 여러 사건에 씁니다.'},
        {'name': 'event 인자', 'signature': 'def greet(event=None):', 'note': 'bind는 이벤트 정보를 첫 인자로 넘깁니다. command는 인자를 넘기지 않으므로 기본값 None을 두면 버튼과 키를 한 함수로 받을 수 있습니다.'},
        {'name': '<Return>', 'signature': '"<Return>"', 'note': 'Enter 키의 이벤트 이름입니다. 문자열 "Return"이 아니라 꺾쇠를 포함한 이름입니다.'},
    ])

ex('events-after-tk', 'after · 이벤트 루프를 막지 않는 타이머', {'main.py': '''import tkinter as tk

root = tk.Tk()
root.title("after 타이머")
root.geometry("420x180")
label = tk.Label(root, text="3초 뒤에 인사합니다.", font=("sans-serif", 16))
label.pack(padx=24, pady=24)

def tick(left):
    if left == 0:
        label.config(text="안녕하세요! after가 호출했습니다.")
        return
    label.config(text=f"{left}초 남았습니다.")
    root.after(1000, lambda: tick(left - 1))

tk.Button(root, text="카운트 시작", command=lambda: tick(3)).pack()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'after', 'signature': 'root.after(1000, 함수)', 'note': '지정한 밀리초 뒤에 함수를 한 번 호출합니다. 그 동안에도 창은 클릭·그리기를 계속합니다.'},
        {'name': 'time.sleep을 쓰지 않는 이유', 'signature': '# 콜백 안에서 time.sleep(3) 금지', 'note': 'sleep은 이벤트 루프를 멈춰 화면이 하얗게 멈춘 것처럼 보입니다. 기다림은 after로 나눕니다.'},
    ],
    glossary=[{'term': '이벤트 루프', 'meaning': '클릭·키·타이머를 순서대로 처리하는 반복입니다. mainloop가 그 일을 합니다.'}])

ex('events-pyside-signal', 'clicked·textChanged · 시그널 연결', {'main.py': '''import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

def greet():
    name = entry.text().strip() or "여러분"
    result.setText(f"{name}님, 안녕하세요!")

def preview(text):
    result.setText(f"미리보기: {text or '빈 칸'}")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("시그널 · PySide6")
window.resize(420, 200)
layout = QVBoxLayout(window)
entry = QLineEdit()
entry.textChanged.connect(preview)
layout.addWidget(entry)
button = QPushButton("인사하기")
button.clicked.connect(greet)
layout.addWidget(button)
result = QLabel("글자를 쓰면 미리보기가 바뀝니다.")
layout.addWidget(result)
window.show()
sys.exit(app.exec())'''}, mode='pc',
    pre_api=[
        {'name': 'clicked.connect', 'signature': 'button.clicked.connect(greet)', 'note': '버튼의 클릭 시그널에 함수를 연결합니다. connect(greet())처럼 괄호를 붙이면 지금 실행되고 반환값이 연결됩니다.'},
        {'name': 'textChanged', 'signature': 'entry.textChanged.connect(preview)', 'note': '한 글자가 바뀔 때마다 preview(text)를 호출합니다. 미리보기·실시간 검사에 씁니다.'},
        {'name': 'app.exec', 'signature': 'sys.exit(app.exec())', 'note': 'Qt의 이벤트 루프입니다. tkinter의 mainloop에 대응합니다. show() 뒤에 호출합니다.'},
    ])

ex('memo-window-tk', '메모장 ① · 창과 Text만', {'main.py': '''import tkinter as tk

window = tk.Tk()
window.title("나만의 메모장 · 창만")
window.geometry("640x420")
text_area = tk.Text(window, wrap="word")
text_area.pack(expand=True, fill="both")
window.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'Tk', 'signature': 'window = tk.Tk()', 'note': '기본 창을 만듭니다. title은 제목, geometry는 처음 크기입니다.'},
        {'name': 'Text', 'signature': 'tk.Text(window, wrap="word")', 'note': '여러 줄 편집기입니다. wrap="word"는 단어 단위로 줄을 바꿉니다. Entry는 한 줄입니다.'},
        {'name': 'pack(expand, fill)', 'signature': 'text_area.pack(expand=True, fill="both")', 'note': '창이 커져도 편집기가 남는 공간을 채웁니다. 메모장 본문에 쓰는 배치입니다.'},
    ],
    glossary=[{'term': '단계 1–3', 'meaning': '임포트 → 창 만들기 → Text를 붙이기까지가 메모장의 뼈대입니다. 파일 대화 상자는 다음 예제입니다.'}])

ex('memo-files-tk', '메모장 ② · 열기·저장 버튼', {'main.py': '''import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if not file_path:
        return
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_area.get("1.0", "end-1c"))

window = tk.Tk()
window.title("나만의 메모장 · 열기·저장")
window.geometry("640x420")
buttons = tk.Frame(window)
buttons.pack(fill="x")
tk.Button(buttons, text="열기", command=open_file).pack(side="left", padx=4, pady=4)
tk.Button(buttons, text="저장", command=save_file).pack(side="left")
text_area = tk.Text(window, wrap="word")
text_area.pack(expand=True, fill="both")
window.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'askopenfilename', 'signature': 'filedialog.askopenfilename()', 'note': '열 파일을 고르는 대화 상자입니다. 취소를 누르면 빈 문자열이 돌아오므로 바로 열지 말고 검사합니다.'},
        {'name': 'asksaveasfilename', 'signature': 'filedialog.asksaveasfilename(defaultextension=".txt")', 'note': '저장 경로를 고릅니다. defaultextension은 확장자를 빼먹었을 때 .txt를 붙입니다.'},
        {'name': 'Text 위치 "1.0"', 'signature': 'text_area.delete("1.0", tk.END)', 'note': '"줄.칸"입니다. 첫 줄은 1, 첫 칸은 0입니다. 위 격자에서 왼쪽 위가 "1.0"입니다. 열기 전에 기존 글을 지웁니다.'},
        {'name': 'end-1c', 'signature': 'text_area.get("1.0", "end-1c")', 'note': 'Text는 끝에 줄바꿈을 하나 더 가지고 있습니다. 저장할 때 그 한 글자를 빼면 다시 열 때마다 빈 줄이 늘지 않습니다. 위 표에서 end와 비교하세요.'},
    ],
    glossary=[
        {'term': '취소 시험', 'meaning': '열기·저장 대화 상자에서 취소를 눌러 보세요. 기존 글이 그대로면 분기 검사가 맞은 것입니다.'},
        {'term': 'UTF-8', 'meaning': '한글 파일을 읽고 쓸 때 지정하는 인코딩입니다. 빼면 환경에 따라 글자가 깨질 수 있습니다.'},
    ])

ex('pyside-first', 'PySide6 · 최소 창 실행 순서', {'main.py': '''import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("첫 창 · PySide6")
window.resize(360, 160)
layout = QVBoxLayout(window)
layout.addWidget(QLabel("QApplication → 창 → show → exec"))
window.show()
sys.exit(app.exec())'''}, mode='pc',
    pre_api=[
        {'name': 'QApplication', 'signature': 'app = QApplication(sys.argv)', 'note': 'Qt 앱을 하나 만듭니다. 위젯보다 먼저 필요합니다. tkinter의 Tk()가 창과 앱을 겸하는 것과 다릅니다.'},
        {'name': 'QWidget', 'signature': 'window = QWidget()', 'note': '빈 창(또는 컨테이너)입니다. setWindowTitle·resize로 제목과 크기를 정합니다.'},
        {'name': 'show / exec', 'signature': 'window.show()\nsys.exit(app.exec())', 'note': 'show는 창을 화면에 올리고, exec는 클릭을 기다립니다. exec를 빼면 프로그램이 바로 끝납니다.'},
    ],
    glossary=[{'term': 'sys.argv', 'meaning': '실행 인자 목록입니다. QApplication이 일부 Qt 옵션을 읽을 수 있도록 넘깁니다.'}])

FORM_UI = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>200</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Designer 실습 · PySide6</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QLabel" name="titleLabel">
     <property name="text">
      <string>이름을 입력하세요</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLineEdit" name="nameEdit"/>
   </item>
   <item>
    <widget class="QPushButton" name="greetButton">
     <property name="text">
      <string>인사하기</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="resultLabel">
     <property name="text">
      <string>결과가 여기에 표시됩니다.</string>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

ex('pyside-ui-file', 'Qt Designer · .ui 불러와 이벤트 연결', {
    'main.py': '''import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

app = QApplication(sys.argv)
ui_path = Path(__file__).with_name("form.ui")
ui_file = QFile(str(ui_path))
ui_file.open(QFile.OpenModeFlag.ReadOnly)
window = QUiLoader().load(ui_file)
ui_file.close()

def greet():
    name = window.nameEdit.text().strip() or "여러분"
    window.resultLabel.setText(f"{name}님, 안녕하세요!")

window.greetButton.clicked.connect(greet)
window.show()
sys.exit(app.exec())''',
    'form.ui': FORM_UI,
}, mode='pc',
    pre_api=[
        {'name': 'objectName', 'signature': 'window.nameEdit / window.greetButton', 'note': 'Designer에서 붙인 부품 이름입니다. 화면에 보이는 text와 다릅니다. 코드는 objectName으로 위젯을 찾습니다.'},
        {'name': 'QUiLoader.load', 'signature': 'window = QUiLoader().load(ui_file)', 'note': 'form.ui를 실행 중에 읽어 창을 만듭니다. 다른 방법은 pyside6-uic form.ui -o ui_form.py로 파이썬을 생성하는 것입니다.'},
        {'name': '생성 파일과 main.py', 'signature': 'from ui_form import Ui_Form', 'note': 'uic가 만든 파일은 다시 생성하면 덮어써집니다. 이벤트 연결은 직접 쓰는 main.py에 둡니다.'},
    ],
    glossary=[{'term': 'pyside6-designer', 'meaning': '가상환경을 켠 뒤 실행하는 Designer 명령입니다. Widget 폼을 배치하고 form.ui로 저장합니다.'}],
    note='form.ui는 Designer가 저장하는 XML입니다. 이 예제는 실행 때 QUiLoader로 읽습니다. pyside6-uic로 파이썬을 만드는 경로와 결과 화면은 같습니다.')

ex('review-scratch-tk', '확인학습 · 창·버튼·콜백을 처음부터', {'main.py': '''import tkinter as tk

def say_hello():
    label.config(text="반갑습니다!")

root = tk.Tk()
root.title("처음부터 만들기")
label = tk.Label(root, text="버튼을 눌러 보세요.")
label.pack(pady=12)
tk.Button(root, text="인사", command=say_hello).pack()
root.mainloop()'''}, mode='pc',
    pre_api=[
        {'name': 'Tk 객체', 'signature': 'root = tk.Tk()', 'note': '창을 만드는 출발점입니다. 종합 평가에서 묻는 Tk 객체입니다.'},
        {'name': 'pack', 'signature': 'label.pack()', 'note': '생성만 하고 pack/grid/place를 빼면 화면에 보이지 않습니다. 59쪽 7번과 연결됩니다.'},
        {'name': 'command', 'signature': 'tk.Button(root, command=say_hello)', 'note': '함수 자체를 넘깁니다. 클릭할 때 실행됩니다.'},
        {'name': 'mainloop', 'signature': 'root.mainloop()', 'note': '이벤트를 기다리는 루프입니다. 이 줄이 없으면 창이 바로 사라질 수 있습니다.'},
    ],
    glossary=[
        {'term': '57쪽 IDLE 코드', 'meaning': 'Frame은 컨테이너, Button은 클릭 요소, 둘을 통칭하면 위젯입니다.'},
        {'term': '확인학습 커버', 'meaning': '이 네 줄(창·위젯·배치·콜백·루프)을 예제 없이 다시 타이핑해 보세요. 그런 다음 조건을 바꾸어 검사합니다.'},
    ])

ex('project-button-tk', '기능 모듈 한 줄 연결 · 주사위 버튼', {'main.py': '''import tkinter as tk
from core.logic import roll

def show():
    result.config(text=f"주사위: {roll(6)}")

root = tk.Tk()
root.title("기능 연결 · 주사위")
root.geometry("360x160")
tk.Button(root, text="굴리기", command=show).pack(pady=20)
result = tk.Label(root, text="버튼을 누르면 core.logic.roll을 호출합니다.")
result.pack()
root.mainloop()''', **core}, mode='pc',
    pre_api=[
        {'name': 'from core.logic import roll', 'signature': 'from core.logic import roll', 'note': '화면 파일은 계산을 직접 쓰지 않고 기능 모듈을 부릅니다. 웹의 core 예제와 같은 함수입니다.'},
        {'name': 'command=show', 'signature': 'tk.Button(root, command=show)', 'note': '클릭하면 show가 roll(6)을 호출하고 Label에 결과를 씁니다. GUI는 입력·표시만 담당합니다.'},
    ],
    glossary=[{'term': '화면과 기능 분리', 'meaning': 'core에는 tkinter가 없습니다. 같은 roll을 PySide6 버튼에도 연결할 수 있습니다.'}])


def apply():
    """Patch lesson lists/prose after content.py has defined the base Unit II lessons."""
    _lesson('ui').update({
        'glossary': [
            {'term': 'UI', 'meaning': '사람과 시스템이 의도를 주고받는 접점입니다. 버튼·색·배치·피드백이 모두 UI입니다.'},
            {'term': 'CLI / GUI / NUI', 'meaning': '명령어 / 아이콘·메뉴·버튼 / 음성·손짓·터치. 분류가 겹치는 사례(터치 GUI)도 있습니다.'},
        ],
        'screenshots': SHOT_TK,
    })
    _lesson('ui')['paragraphs'].append(
        '48쪽 확인학습은 UI 정의, GUI 장점, NUI 사례, 라이브러리 특징을 묻습니다. 아래 CLI 예제와 같은 인사를 창으로 만든 hello-tk를 나란히 실행해 보세요. 파일 100개 이름 바꾸기는 CLI가, 사진 한 장 자르기는 GUI가 편한 경우가 많습니다.'
    )
    _lesson('widgets')['paragraphs'].append(
        '위젯을 한 창에 모두 쌓기 전에, 역할별로 나누어 보세요. Label·Entry는 한 줄 읽고 보여 주기, Checkbutton·Radiobutton은 선택 값 읽기, Listbox·Canvas는 목록과 좌표 그리기입니다. 회원 가입의 이름·소개·약관 동의·학년 선택에 각각 어떤 위젯이 맞는지 고른 뒤 예제에서 값을 읽어 보세요. 57쪽 확인학습의 Frame·Button도 위젯입니다.'
    )
    _lesson('layout')['paragraphs'].append(
        'expand는 "남는 공간을 누구에게 줄까", fill은 "받은 칸을 위젯이 채울까"입니다. 격자 폼에서는 sticky와 columnconfigure(weight=1)를 함께 써야 창을 넓혀도 입력칸이 늘어납니다. 같은 부모에서 pack과 grid를 섞지 마세요. 창을 좁게·넓게 바꾸며 잘리는 요소를 찾는 것이 51쪽 배치의 확인 방법입니다.'
    )
    _lesson('events')['paragraphs'].append(
        '이벤트 전용 예제부터 보세요. 웹의 콜백 예제는 괄호 유무만 추적하고, command 비교 창은 잘못된 연결이 생성 시점에 실행되는 모습을 보여 줍니다. bind는 Enter 키, after는 기다림, Qt는 clicked와 textChanged입니다. 인사 앱(hello-tk / hello-pyside)은 같은 원리가 실제 입력창에 붙은 완성 예입니다. 콜백 안에서 time.sleep을 쓰지 마세요.'
    )
    _lesson('memo')['paragraphs'].append(
        '완성본을 한 번에 외우지 말고 단계를 나누세요. ① 창과 Text, ② 열기·저장 버튼과 취소 검사, ③ 메뉴를 붙인 교과서 전체 코드, ④ PySide6 대응, ⑤ 미저장 확인이 있는 개선본입니다. 53쪽 열기 순서는 대화 상자 → 취소 확인 → UTF-8 읽기 → 기존 글 삭제 → 삽입입니다. 저장은 경로 선택 → 취소 확인 → get → 쓰기입니다.'
    )
    _lesson('pyside')['paragraphs'].append(
        '이 페이지만 열어도 순서를 실습할 수 있습니다. 최소 창으로 QApplication → show → exec를 확인하고, 인사 앱에서 위젯과 connect를 본 뒤, form.ui를 불러 와 objectName으로 버튼을 연결하세요. Designer의 보이는 글자(text)와 코드가 찾는 이름(objectName)은 다른 속성입니다.'
    )
    _lesson('project')['paragraphs'].append(
        '한 버튼만 연결한 주사위 예제부터 시작하세요. 동작이 보이면 라디오·입력칸이 있는 생활 도우미로 옮깁니다. 빈 입력, 0면 주사위, 잘못된 날짜, 중복 이름은 기능 모듈이 예외를 내고 GUI는 메시지로 보여 줍니다.'
    )
    _lesson('review')['paragraphs'].append(
        '56–59쪽을 이 페이지에서 다시 닫습니다. 처음부터 만들기 예제로 Tk 객체·pack·command·mainloop를 타이핑하고, 57쪽 IDLE 코드에서 컨테이너(Frame)·클릭 요소(Button)·통칭(위젯)을 찾으세요. 58쪽 4번은 보기 내용이 GUI 사례이므로 인터페이스 유형을 고르는 문제로 읽습니다.'
    )

    _set_examples('ui', ['ui-cli', 'hello-tk'])
    _set_examples('widgets', [
        'widgets-label-entry-tk', 'widgets-choice-tk', 'widgets-list-canvas-tk',
        'widgets-tk', 'widgets-pyside', 'widgets-pyside-form',
    ])
    _set_examples('layout', [
        'layout-pack-tk', 'layout-grid-tk', 'layout-tk', 'layout-pyside', 'layout-pyside-form',
    ])
    _set_examples('events', [
        'events-callback', 'events-command-tk', 'events-bind-tk', 'events-after-tk',
        'events-pyside-signal', 'hello-tk', 'hello-pyside',
    ])
    _set_examples('memo', [
        'memo-window-tk', 'memo-files-tk', 'memo-tk', 'memo-pyside',
        'memo-plus-tk', 'memo-plus-pyside',
    ])
    _set_examples('pyside', ['pyside-first', 'hello-pyside', 'pyside-ui-file', 'memo-pyside'])
    _set_examples('project', ['core', 'project-button-tk', 'project-tk', 'project-pyside'])
    _set_examples('review', ['review-scratch-tk'])

    for lesson in units[2]:
        if lesson['id'] == 'widgets':
            lesson['pre_api'] = [
                {'name': '위젯 선택', 'signature': '보여줄 글 → Label / 한 줄 → Entry / 여러 줄 → Text',
                 'note': '받을 정보의 형태를 먼저 정하면 위젯 이름이 따라옵니다. 아래 예제는 역할별로 나뉘어 있습니다.'},
            ]
        elif lesson['id'] == 'layout':
            lesson['pre_api'] = [
                {'name': '배치 관리자', 'signature': 'pack() / grid() / place()',
                 'note': '위젯을 생성한 것만으로는 화면에 나타나지 않습니다. 부모를 정하고 배치를 호출해야 합니다.'},
            ]
        elif lesson['id'] == 'events':
            lesson['pre_api'] = [
                {'name': 'command / connect', 'signature': 'command=greet  ·  clicked.connect(greet)',
                 'note': '함수 자체를 맡깁니다. greet()는 지금 호출입니다. 아래 웹 예제에서 괄호 유무를 먼저 보세요.'},
            ]
        elif lesson['id'] == 'memo':
            lesson['pre_api'] = [
                {'name': 'filedialog', 'signature': 'from tkinter import filedialog',
                 'note': '열기·저장 창은 별도 모듈입니다. 경로가 비었으면(취소) 파일을 읽거나 쓰지 않습니다.'},
            ]
        elif lesson['id'] == 'pyside':
            lesson['pre_api'] = [
                {'name': '실행 순서', 'signature': 'QApplication → 창·레이아웃 → connect → show → exec',
                 'note': 'tkinter의 Tk·pack·command·mainloop를 Qt 이름으로 옮긴 순서입니다. 단어만 바꾸기보다 역할을 옮기세요.'},
            ]
        elif lesson['id'] == 'review':
            lesson['pre_api'] = [
                {'name': '한 줄로 복습', 'signature': 'Tk() → 위젯 → pack → command → mainloop()',
                 'note': '예제를 보지 않고 이 순서로 창을 만들 수 있으면 2단원 본편을 닫을 수 있습니다.'},
            ]
