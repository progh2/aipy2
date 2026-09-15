"""Unit II example screenshot slots and capture catalog (#54).

Hello-gallery files stay tk/ttk/pyside/pyqt/wx/kivy.png. Other GUI examples
use web/assets/screenshots/{example-id}.png produced by capture_gui.py.
CLI/print examples stay empty. wx appendix shots are registered by wx_appendix (#55).
Kivy appendix shots are registered by kivy_appendix (#56).
"""
from slots import shot_items

CAPTION = '이 예제를 Linux에서 실행해 캡처한 화면입니다. OS·테마에 따라 외형은 달라집니다.'

# Gallery filenames used by build.py#gallery and the hello-* examples.
HELLO_FILE = {
    'hello-tk': 'tk.png',
    'hello-ttk': 'ttk.png',
    'hello-pyside': 'pyside.png',
    'hello-pyqt': 'pyqt.png',
    'hello-wx': 'wx.png',
    'hello-kivy': 'kivy.png',
}

# Dedicated captures. Filename is always {id}.png.
OWN = {
    'widgets-label-entry-tk': (
        'Label·Entry 창 · 이름 입력 후 표시 버튼',
        '한 줄 입력과 Label.config로 같은 이름을 다시 보여 줍니다. ' + CAPTION),
    'widgets-choice-tk': (
        '체크·라디오 창 · 학년과 완료 여부',
        'BooleanVar와 StringVar로 선택 값을 읽습니다. ' + CAPTION),
    'widgets-list-canvas-tk': (
        'Listbox·Canvas 창 · 고른 주제를 캔버스에 그림',
        '목록에서 고른 뒤 Canvas에 글자를 그립니다. ' + CAPTION),
    'widgets-tk': (
        'tkinter 위젯 도감 · Label·Entry·Text·선택·목록·Canvas',
        '한 창에 위젯 9종을 모아 비교합니다. ' + CAPTION),
    'widgets-pyside': (
        'PySide6 위젯 도감 · QLabel·입력·체크·목록·도형',
        '같은 역할을 Qt 위젯 이름으로 대응합니다. ' + CAPTION),
    'widgets-pyside-form': (
        'PySide6 입력 폼 · 이름·체크·라디오',
        'QLineEdit·QCheckBox·QButtonGroup으로 값을 읽습니다. ' + CAPTION),
    'layout-pack-tk': (
        'pack 배치 · expand와 fill을 켠 세 영역',
        '위·가운데·아래가 창 너비에 어떻게 붙는지 봅니다. ' + CAPTION),
    'layout-grid-tk': (
        'grid 로그인 폼 · sticky와 두 열',
        '라벨은 오른쪽, 입력칸은 가로로 늘어납니다. ' + CAPTION),
    'layout-tk': (
        'pack·grid·place를 한 창에서 비교',
        '부모 Frame을 나누면 세 배치를 같이 볼 수 있습니다. ' + CAPTION),
    'layout-pyside': (
        'Qt 레이아웃 · 가로 버튼과 격자',
        'QHBoxLayout 위에 QGridLayout을 올립니다. ' + CAPTION),
    'layout-pyside-form': (
        'QGridLayout 로그인 폼',
        '아이디·비밀번호와 두 열을 차지하는 버튼입니다. ' + CAPTION),
    'events-command-tk': (
        'command 전달 비교 · 잘못된 연결이 생성 시점에 실행됨',
        '창이 열린 직후 기록이 이미 있으면 괄호를 붙인 것입니다. ' + CAPTION),
    'events-bind-tk': (
        'bind · Enter 키로 인사하는 창',
        '버튼 클릭과 Enter가 같은 greet 함수를 부릅니다. ' + CAPTION),
    'events-after-tk': (
        'after 타이머 · 이벤트 루프를 막지 않는 카운트',
        'sleep 대신 after로 기다린 뒤 글자가 바뀝니다. ' + CAPTION),
    'events-pyside-signal': (
        'clicked·textChanged 시그널 창',
        '글자를 쓰면 미리보기가 바뀌고, 버튼은 인사를 확정합니다. ' + CAPTION),
    'memo-window-tk': (
        '메모장 뼈대 · 창과 Text만',
        '메뉴·파일 대화 상자 전의 최소 화면입니다. ' + CAPTION),
    'memo-files-tk': (
        '메모장 · 열기·저장 버튼과 편집기',
        '위쪽 Frame에 버튼을 두고 Text가 나머지를 채웁니다. ' + CAPTION),
    'memo-tk': (
        '교과서 메모장 · 파일 메뉴가 있는 창',
        '열기·저장·종료는 메뉴에 연결됩니다. ' + CAPTION),
    'memo-pyside': (
        '메모장 · PySide6 QMainWindow',
        'QPlainTextEdit를 중앙에 두고 파일 메뉴를 붙입니다. ' + CAPTION),
    'memo-plus-tk': (
        '개선 메모장 · 글자 수와 미저장 표시',
        '상태 줄과 제목 앞 *가 dirty 상태를 보여 줍니다. ' + CAPTION),
    'memo-plus-pyside': (
        '개선 메모장 · PySide6 상태 줄',
        '글자 수와 수정 여부가 창 제목·상태 줄에 나타납니다. ' + CAPTION),
    'pyside-first': (
        'PySide6 최소 창 · QApplication 실행 순서',
        '위젯을 더하기 전의 빈 창입니다. ' + CAPTION),
    'pyside-ui-file': (
        'Qt Designer .ui를 불러 온 인사 폼',
        'objectName으로 입력칸·버튼을 찾아 연결합니다. ' + CAPTION),
    'review-scratch-tk': (
        '확인학습 · 창·버튼·콜백만 있는 최소 GUI',
        'Tk → Label → Button(command) → mainloop를 다시 타이핑하는 창입니다. ' + CAPTION),
    'project-button-tk': (
        '기능 모듈 한 줄 연결 · 주사위 버튼',
        '클릭하면 core.logic.roll 결과를 Label에 씁니다. ' + CAPTION),
    'project-tk': (
        '생활 도우미 · tkinter 라디오와 실행 버튼',
        '같은 core.logic을 주사위·D-day·추첨에 연결합니다. ' + CAPTION),
    'project-pyside': (
        '생활 도우미 · PySide6 콤보 상자',
        '모드만 바꾸고 같은 기능 모듈을 부릅니다. ' + CAPTION),
}

# Lesson-level preview uses an already-captured example file (no extra PNG).
LESSON = {
    'widgets': ('widgets-tk.png', 'tkinter 위젯 도감 실행 화면',
                '위젯을 역할별로 고른 뒤 아래 예제에서 값을 읽어 보세요. ' + CAPTION),
    'layout': ('layout-tk.png', 'pack·grid·place 비교 창',
               '창을 늘려 보며 잘리는 칸을 찾는 것이 배치 확인입니다. ' + CAPTION),
    'events': ('events-command-tk.png', 'command 연결과 잘못된 연결 비교',
               '괄호 유무가 실행 시점을 바꿉니다. 아래 예제에서 기록을 보세요. ' + CAPTION),
    'memo': ('memo-tk.png', '교과서 메모장 실행 화면',
             '창·Text·메뉴 순으로 쌓은 완성본입니다. 단계는 아래 예제에 있습니다. ' + CAPTION),
    'pyside': ('pyside-first.png', 'PySide6 최소 창',
               'QApplication → show → exec 순서를 이 창으로 확인합니다. ' + CAPTION),
    'project': ('project-tk.png', '생활 도우미 tkinter 실행 화면',
                '화면은 입력과 표시만 하고 계산은 core에 맡깁니다. ' + CAPTION),
    'review': ('review-scratch-tk.png', '처음부터 만든 최소 인사 창',
               '예제 없이 이 네 줄(창·위젯·배치·콜백)을 다시 타이핑해 보세요. ' + CAPTION),
}


def _item(src, alt, caption):
    return shot_items([{'src': src, 'alt': alt, 'caption': caption}])


def output_name(example_id):
    return HELLO_FILE.get(example_id, f'{example_id}.png')


def capture_ids():
    """Example ids that produce a dedicated {id}.png (not the hello gallery)."""
    return list(OWN)


def apply():
    """Attach screenshot slots after density/pre_api have run."""
    from content import examples, units
    for eid, (alt, caption) in OWN.items():
        examples[eid]['screenshots'] = _item(f'{eid}.png', alt, caption)
    for lesson in units[2]:
        spec = LESSON.get(lesson['id'])
        if spec and not lesson['screenshots']:
            lesson['screenshots'] = _item(*spec)
