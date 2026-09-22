"""Unit I history/youtube tip seeds for #59. Applied after unit1_pre_api.

Fills empty tips.history / tips.youtube on Unit I lessons. Does not invent
links: only oEmbed-verified public education videos (Corey Schafer,
freeCodeCamp). Empty stays empty where nothing solid exists (math lesson
video, project/review wrap-up).
"""
from content import examples, units
from slots import youtube_items

# oEmbed 200 (2026-09-15): title | channel
YT_MODULES = {
    'title': 'Python Tutorial for Beginners 9: Import Modules and Exploring The Standard Library (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=CqvZ3vGoGs0',
    'note': '영어 공개 강의입니다. 모듈을 만들고 import하는 앞부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_MODULES_CREATE = {
    **YT_MODULES,
    'note': '영어 공개 강의입니다. 자기 .py를 모듈로 저장하고 불러오는 구간이 이 주제와 맞습니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_MODULES_IMPORT = {
    **YT_MODULES,
    'note': '영어 공개 강의입니다. import / from / as 형태만 먼저 보고, 표준 라이브러리 탐색은 나중에 보세요. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_PACKAGES = {
    'title': 'Intermediate Python Programming Course (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=HGOBQPFzWKo',
    'note': '영어 공개 강의입니다. 목차의 Modules·Packages 구간만 보면 됩니다. 나머지 중급 주제는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_NAMEMAIN = {
    'title': "Python Tutorial: if __name__ == '__main__' (Corey Schafer)",
    'url': 'https://www.youtube.com/watch?v=sugvnHA7ElY',
    'note': '영어 공개 강의(약 8분)입니다. 직접 실행과 임포트일 때 __name__이 달라지는 것만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_OS = {
    'title': 'Python Tutorial: OS Module — Use Underlying Operating System Functionality (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=tJxcKyFMTGo',
    'note': '영어 공개 강의입니다. getcwd·listdir·경로만 먼저 보고, 삭제·환경 변수는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_RANDOM = {
    'title': 'Python Tutorial: Generate Random Numbers and Data Using the random Module (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=KzqSDvzOFNA',
    'note': '영어 공개 강의입니다. randrange·choice·sample·seed만 보면 이 주제와 맞습니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_DATETIME = {
    'title': 'Python Tutorial: Datetime Module — Dates, Times, Timedeltas, and Timezones (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=eirjjyP2qcQ',
    'note': '영어 공개 강의입니다. date·datetime·timedelta와 weekday만 먼저 보세요. 시간대는 나중에 봐도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_PIP = {
    'title': 'Python Tutorial: pip — An in-depth look at the package management system (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=U2ZN104hIcc',
    'note': '영어 공개 강의입니다. 설치·가상환경·requirements.txt만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}


def _lesson(lid):
    return next(item for item in units[1] if item['id'] == lid)


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
    """Seed Unit I history/youtube after density/pre_api have run."""
    _fill_lessons()
    _fill_examples()


def _fill_lessons():
    _fill_lesson(
        'overview',
        history='파이썬은 1991년 공개 때부터 .py 파일을 모듈로 불러왔습니다. 폴더를 패키지로 묶는 방식은 1997년 Python 1.5에서 공식화되었습니다.',
    )
    _fill_lesson(
        'define',
        history='모듈은 특별한 파일 형식이 아닙니다. 처음부터 함수·클래스·실행문을 담은 .py가 곧 모듈이었고, 파일 이름이 모듈 이름이 되었습니다.',
    )
    _fill_lesson(
        'entrypoint',
        history='if __name__ == "__main__"은 초기 파이썬부터 쓰인 관용구입니다. 직접 실행일 때만 시험 코드를 돌리고, 임포트할 때는 함수만 제공합니다.',
        youtube=YT_NAMEMAIN,
    )
    _fill_lesson(
        'imports',
        history='import와 from … import는 둘 다 모듈을 로드합니다. 차이는 현재 이름 공간에 어떤 이름을 연결하느냐이며, as 별칭도 같은 시기에 자리 잡았습니다.',
        youtube=YT_MODULES_IMPORT,
    )
    _fill_lesson(
        'packages',
        history='패키지는 1997년 Python 1.5에서 도입되었습니다. 폴더에 __init__.py를 두면 점(.)으로 경로를 나누고, 나중에 __all__로 별표 임포트 대상을 적게 되었습니다.',
        youtube=YT_PACKAGES,
    )
    _fill_lesson(
        'os-sys',
        history='os와 sys는 파이썬 표준 라이브러리의 오래된 모듈입니다. os는 운영체제·파일, sys는 인터프리터·실행 인자를 처음부터 맡았습니다.',
        youtube=YT_OS,
    )
    _fill_lesson(
        'math',
        history='math 모듈은 C 표준 수학 함수를 파이썬 이름으로 제공합니다. 상수 pi·e와 올림·내림처럼 자주 쓰는 계산을 한곳에 모아 두었습니다.',
    )
    _fill_lesson(
        'random',
        history='random은 2003년 Python 2.3부터 메르센 트위스터를 기본 생성기로 씁니다. 주사위·추첨처럼 재현 가능한 가짜 난수가 필요할 때 씁니다.',
        youtube=YT_RANDOM,
    )
    _fill_lesson(
        'datetime',
        history='datetime은 2003년 Python 2.3에 들어왔습니다. 날짜를 문자열이 아니라 객체로 다루어 빼기·요일 계산을 안전하게 합니다.',
        youtube=YT_DATETIME,
    )
    _fill_lesson(
        'thirdparty',
        history='PyPI는 2003년 열렸고, pip는 2011년 전후 파이썬 패키지 설치의 기본 도구가 되었습니다. 설치 이름과 import 이름은 처음부터 다를 수 있었습니다.',
        youtube=YT_PIP,
    )
    _fill_lesson(
        'project',
        history='화면과 계산을 나누는 생각은 1979년 Smalltalk의 MVC에서 분명해졌습니다. 1단원에서는 GUI 없이 core.logic만 먼저 검사합니다.',
    )
    _fill_lesson(
        'review',
        history='1단원은 파일→모듈→임포트→패키지→표준·서드파티 순으로 쌓입니다. 불러올 때 실행되는 줄과 호출해야 실행되는 줄만 구별해도 종합 평가의 뼈대가 됩니다.',
    )


def _fill_examples():
    _fill_example(
        'reuse',
        history='한 파일에 함수를 두고 여러 프로그램이 불러 쓰는 방식은 1970년대부터 라이브러리의 기본이었습니다. 파이썬은 그 단위를 .py 모듈로 단순화했습니다.',
    )
    _fill_example(
        'main-guard',
        history='__name__ 검사는 “이 파일이 프로그램의 입구인가, 부품인가”를 가릅니다. 스크립트와 모듈을 같은 파일에 두는 파이썬의 오랜 습관입니다.',
    )
    _fill_example(
        'all',
        history='__all__은 “별표로 공개할 이름”을 적는 약속입니다. 없는 이름을 숨기는 보안 기능이 아니라, from … import *의 목록일 뿐입니다.',
    )
    _fill_example(
        'os',
        history='os 모듈은 운영체제가 달라도 같은 파이썬 이름으로 폴더를 다루게 하려고 만들어졌습니다. 웹 실습의 폴더는 그 개념을 가상 파일로 보여 줍니다.',
    )
    _fill_example(
        'pypi-names',
        history='설치 이름과 import 이름이 다른 전통은 오래된 패키지에서 흔합니다. Beautiful Soup의 beautifulsoup4/bs4가 교실에서 가장 자주 만나는 예입니다.',
    )
    _fill_example(
        'core',
        history='기능 모듈을 화면보다 먼저 만드는 순서는 GUI 단원의 생활 도우미와 같습니다. 1단원에서는 return 값만 검사합니다.',
    )


def unit1_history_lessons():
    """Lessons that must show a history one-liner after #59."""
    return [lesson['id'] for lesson in units[1]]


def unit1_youtube_lessons():
    """Lessons that have a verified public video (math/project/review stay empty).

    overview/define share the same modules video as imports (#63 dedup);
    that URL stays on imports only.
    """
    return [
        'entrypoint', 'imports', 'packages',
        'os-sys', 'random', 'datetime', 'thirdparty',
    ]
