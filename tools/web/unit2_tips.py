"""Unit II history/youtube tip seeds for #58. Applied after appendices.

Fills empty tips.history / tips.youtube on Unit II lessons and a few
first-of-toolkit examples. Does not invent links: only oEmbed-verified
public education videos (Crash Course, freeCodeCamp). Empty stays empty
where nothing solid exists (wxPython lesson video, incremental examples).
"""
from content import examples, units
from slots import youtube_items

# oEmbed 200 (2026-09-15): title | channel
YT_CRASH_GUI = {
    'title': 'Graphical User Interfaces: Crash Course Computer Science #26',
    'url': 'https://www.youtube.com/watch?v=XIGSJshYb90',
    'note': '영어 공개 강의(약 13분)입니다. CLI와 창·아이콘·마우스가 어떻게 달라졌는지만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_TK = {
    'title': 'Tkinter Course — Create Graphic User Interfaces in Python Tutorial (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=YXPyB4XeYLA',
    'note': '영어 공개 강의입니다. 처음에는 창·Label·Button·pack만 따라 보고, 나머지는 필요할 때 이어서 보세요. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_TK_WIDGETS = {
    **YT_TK,
    'note': '영어 공개 강의입니다. Label·Button·입력칸·라디오만 먼저 보고, 계산기·데이터베이스는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_TK_LAYOUT = {
    **YT_TK,
    'note': '영어 공개 강의입니다. 초반 Positioning with Grid만 보면 이 주제와 맞습니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_TK_EVENTS = {
    **YT_TK,
    'note': '영어 공개 강의입니다. Button을 만드는 구간에서 command에 함수를 맡기는 것만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_TK_MEMO = {
    **YT_TK,
    'note': '영어 공개 강의입니다. Text·파일 열기 대화 상자 구간이 메모장과 맞습니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_PYSIDE = {
    'title': 'Learn Python GUI Development for Desktop — PySide6 and Qt Tutorial (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=Z1N9JzNax2k',
    'note': '영어 공개 강의입니다. 설치·QWidget·시그널만 먼저 보고, Designer는 필요할 때 이어서 보세요. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_KIVY = {
    'title': 'Kivy Course — Create Python Games and Mobile Apps (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=l8Imtec4ReQ',
    'note': '영어 공개 강의입니다. 앞부분의 Label·Button·레이아웃만 보고, 게임 프로젝트는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}


def _lesson(lid):
    return next(item for item in units[2] if item['id'] == lid)


def _fill_tips(rec, *, history=None, youtube=None):
    tips = rec['tips']
    if history and not tips.get('history'):
        tips['history'] = history
    if youtube and not tips.get('youtube'):
        tips['youtube'] = youtube_items(youtube)


def _fill_lesson(lid, *, history=None, youtube=None):
    _fill_tips(_lesson(lid), history=history, youtube=youtube)


def _fill_example(eid, *, history=None, youtube=None):
    _fill_tips(examples[eid], history=history, youtube=youtube)


def apply():
    """Seed Unit II history/youtube after wx/Kivy lessons exist."""
    _fill_lessons()
    _fill_examples()


def _fill_lessons():
    _fill_lesson(
        'ui',
        history='1960년대까지 컴퓨터는 명령어(CLI)로 다루었습니다. 1973년 Xerox Alto와 1984년 매킨토시 이후 창·아이콘·마우스를 만지는 GUI가 일상 인터페이스가 되었습니다.',
        youtube=YT_CRASH_GUI,
    )
    _fill_lesson(
        'libraries',
        history='파이썬 GUI는 한 가지가 아닙니다. Tk(1991)는 표준에 가깝고, Qt(1995 공개)는 위젯이 많으며, wxWidgets(1992)는 운영체제 모양, Kivy(2011)는 터치·자체 그리기를 골랐습니다.',
    )
    _fill_lesson(
        'widgets',
        history='위젯(widget)은 window와 gadget을 붙인 말입니다. 창 안의 재사용 부품을 가리키며, Tk의 Label·Button과 Qt의 QLabel·QPushButton은 같은 역할을 다른 이름으로 합니다.',
        youtube=YT_TK_WIDGETS,
    )
    _fill_lesson(
        'layout',
        history='Tk는 처음부터 pack·grid·place 세 배치 관리자를 두었습니다. 위젯을 만드는 일과 자리를 정하는 일을 나누어, 창 크기가 바뀌어도 다시 계산하게 했습니다.',
    )
    _fill_lesson(
        'events',
        history='GUI는 코드를 위에서 아래로 끝내지 않고, 클릭·키 입력이 올 때까지 루프에서 기다립니다. 이 사건 기반 방식은 Xerox PARC의 Smalltalk 이후 창 프로그램의 기본이 되었습니다.',
    )
    _fill_lesson(
        'memo',
        history='간단한 텍스트 편집기는 GUI 교재의 단골 완성 과제입니다. 파이썬 기본 IDE인 IDLE도 tkinter로 만든 실제 프로그램입니다.',
    )
    _fill_lesson(
        'pyside',
        history='Qt는 1991년 노르웨이에서 시작해 1995년 공개된 C++ GUI 프레임워크입니다. PySide는 Qt 공식 파이썬 바인딩이고, 이 과정은 Qt Widgets를 사용합니다.',
        youtube=YT_PYSIDE,
    )
    _fill_lesson(
        'project',
        history='화면과 계산을 나누는 생각은 1979년 Smalltalk의 MVC에서 분명해졌습니다. core에 기능을 두면 tkinter와 PySide6가 같은 함수를 부를 수 있습니다.',
    )
    _fill_lesson(
        'review',
        history='2단원은 접점(CLI/GUI) → 툴킷 → 위젯·배치·이벤트 → 메모장 순으로 쌓입니다. 창을 띄우는 Tk 객체와, 나중에 호출할 콜백만 구별해도 종합 평가의 뼈대는 됩니다.',
    )
    _fill_lesson(
        'wx',
        history='wxWidgets는 1992년 Julian Smart가 wxWindows로 시작했습니다. 운영체제 위젯을 쓰므로 창 모양이 그 환경의 기본 앱과 가깝습니다. wxPython은 이를 파이썬에서 붙입니다.',
    )
    _fill_lesson(
        'kivy',
        history='Kivy는 2011년 공개된 파이썬 UI 프레임워크입니다. 운영체제 위젯 대신 직접 그려, 터치와 여러 화면 크기를 같은 코드로 노립니다.',
        youtube=YT_KIVY,
    )


def _fill_examples():
    _fill_example(
        'ui-cli',
        history='명령줄 인터페이스는 1960년대 텔레타이프·터미널에서 이어진 방식입니다. 문법을 알면 빠르지만, 무엇을 입력해야 할지는 배워야 합니다.',
    )
    _fill_example(
        'hello-ttk',
        history='ttk는 2007년 Tk 8.5에 들어온 테마 위젯입니다. 역할은 tk.Button과 같고, 테두리·색만 운영체제 테마를 따릅니다.',
    )
    _fill_example(
        'hello-pyside',
        history='Nokia가 2009년 PySide를 열었고, 지금은 Qt Company가 Qt for Python(PySide6)으로 공식 지원합니다. 위젯 이름은 PyQt와 같고 배포 조건이 다릅니다.',
    )
    _fill_example(
        'hello-pyqt',
        history='PyQt는 Riverbank Computing이 만든 Qt 파이썬 바인딩입니다. 호출은 PySide6와 거의 같고, 상용 배포 전에 라이선스를 확인해야 합니다.',
    )
    _fill_example(
        'hello-wx',
        history='wxPython은 C++ 라이브러리 wxWidgets를 파이썬에서 쓰는 바인딩입니다. 1992년 wxWindows로 시작해, 창을 운영체제의 기본 위젯으로 그립니다.',
    )
    _fill_example(
        'hello-kivy',
        history='Kivy는 2011년 공개된 오픈 소스 UI 프레임워크입니다. 운영체제 버튼을 빌리지 않고 직접 그리므로, 기본 글꼴의 한글은 별도 지정해야 할 수 있습니다.',
    )
    _fill_example(
        'events-callback',
        history='콜백은 ‘지금 실행’이 아니라 ‘사건이 나면 불러 달라’고 맡기는 함수입니다. 버튼 생성 때 greet()처럼 괄호를 붙이면, 클릭 전에 이미 실행됩니다.',
    )
    _fill_example(
        'pyside-first',
        history='Qt는 창(QWidget)과 앱(QApplication)을 나눕니다. tkinter의 Tk()가 둘을 겸하는 것과 달리, exec 루프는 앱 객체가 돌립니다.',
    )
    _fill_example(
        'pyside-ui-file',
        history='Qt Designer는 위젯을 끌어다 놓아 .ui XML을 만듭니다. 1990년대부터 Qt 도구 모음에 들어 있으며, 코드는 objectName으로 부품을 찾습니다.',
    )
    _fill_example(
        'memo-tk',
        history='메뉴·열기·저장이 있는 편집기는 1980년대 GUI의 대표 형태입니다. tkinter의 filedialog와 Text가 그 뼈대를 만듭니다.',
    )
    _fill_example(
        'first-wx',
        history='wx.App과 MainLoop는 Tk의 Tk()·mainloop에 대응합니다. 프레임워크 이름은 1992년 wxWindows에서 왔으며, 2004년 wxWidgets로 바뀌었습니다.',
    )
    _fill_example(
        'first-kivy',
        history='Kivy 앱은 App 클래스의 build()가 첫 위젯 트리를 돌려 줍니다. 2011년 공개 이후 터치·여러 화면 크기를 같은 코드로 다루는 쪽이 목표가 되었습니다.',
    )


def unit2_history_lessons():
    """Lessons that must show a history one-liner after #58."""
    return [lesson['id'] for lesson in units[2]]


def unit2_youtube_lessons():
    """Lessons that have a verified public video (wx/project/review stay empty).

    layout/events/memo share the same Tk course video as widgets (#63 dedup);
    that URL stays on widgets only.
    """
    return ['ui', 'widgets', 'pyside', 'kivy']
