"""Unit IV history/youtube tip seeds for #61. Applied after unit4_pre_api.

Fills empty tips.history / tips.youtube on Unit IV lessons. Does not invent
links: only oEmbed-verified public education videos (Crash Course, Computerphile,
freeCodeCamp, TED). Empty stays empty where nothing solid exists
(perspective-click walkthrough, project wrap-up).
"""
from content import examples, units
from slots import youtube_items

# oEmbed 200 (2026-09-15): title | channel
YT_CRASH_CV = {
    'title': 'Computer Vision: Crash Course Computer Science #35',
    'url': 'https://www.youtube.com/watch?v=-4E2-0sxVUM',
    'note': '영어 공개 강의(약 11분)입니다. 사진을 찍는 것과 장면을 이해하는 것, 픽셀·필터·얼굴 검출만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_CRASH_PIXELS = {
    **YT_CRASH_CV,
    'note': '영어 공개 강의입니다. 이미지가 숫자 격자라는 앞부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_CRASH_PIPE = {
    **YT_CRASH_CV,
    'note': '영어 공개 강의입니다. 작은 영역(커널)을 보며 특징을 쌓는 부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_FCC_CV = {
    'title': 'OpenCV Course - Full Tutorial with Python (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=oXlwWbU8l2o',
    'note': '영어 공개 강의입니다. 이미지 읽기·크기 변경 앞부분만 보면 됩니다. 나머지 긴 코스는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_BLUR = {
    'title': 'How Blurs & Filters Work - Computerphile',
    'url': 'https://www.youtube.com/watch?v=C_zFhWdM4ic',
    'note': '영어 공개 강의입니다. 평균 블러와 가우시안 커널만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_SOBEL = {
    'title': 'Finding the Edges (Sobel Operator) - Computerphile',
    'url': 'https://www.youtube.com/watch?v=uihBwtPIBxM',
    'note': '영어 공개 강의입니다. 밝기가 급변하는 곳을 경계로 보는 부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_HAAR = {
    'title': 'Detecting Faces (Viola Jones Algorithm) - Computerphile',
    'url': 'https://www.youtube.com/watch?v=uEJ71VlUmMQ',
    'note': '영어 공개 강의입니다. 밝기 패턴으로 얼굴 위치를 찾는 아이디어만 보면 됩니다. 누구인지 알아내는 이야기가 아닙니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_YOLO = {
    'title': 'How computers learn to recognize objects instantly (Joseph Redmon, TED)',
    'url': 'https://www.youtube.com/watch?v=Cgxsv1riJhI',
    'note': '영어 공개 강의(약 7분)입니다. 상자와 클래스 이름을 한 번에 찾는 아이디어만 보면 됩니다. 교과서의 YOLOv8과는 버전이 다릅니다. 학교 네트워크·연령 정책을 확인하세요.',
}


def _lesson(lid):
    return next(item for item in units[4] if item['id'] == lid)


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
    """Seed Unit IV history/youtube after density/pre_api have run."""
    _fill_lessons()
    _fill_examples()


def _fill_lessons():
    _fill_lesson(
        'cv-overview',
        history='1966년 MIT 여름 비전 프로젝트는 “여름이면 컴퓨터가 볼 수 있다”고 너무 쉽게 보았습니다. 사진을 저장하는 일과 장면을 이해하는 일은 그 뒤에도 따로 발전했습니다.',
        youtube=YT_CRASH_CV,
    )
    _fill_lesson(
        'cv-pixels',
        history='디지털 이미지는 1960년대부터 밝기 격자로 저장되었습니다. 한 칸의 0~255 값과 RGB 세 채널은 그 표현을 교실에서 다루는 기본 단위입니다.',
    )
    _fill_lesson(
        'cv-pipeline',
        history='1982년 마어(Marr)는 시각을 입력에서 표현을 단계적으로 만드는 계산 문제로 정리했습니다. 한 단계의 오류가 다음 해석을 흔드는 이유입니다.',
    )
    _fill_lesson(
        'cv-libraries',
        history='OpenCV는 2000년 인텔에서 시작되었고, Pillow는 PIL의 후속입니다. 입출력·편집·표시·분석 도구가 파이썬에서 나란히 쓰이게 되었습니다.',
        youtube=YT_FCC_CV,
    )
    _fill_lesson(
        'cv-io',
        history='파일을 숫자 배열로 읽는 습관은 디지털 사진 형식(JPEG·PNG)과 함께 자리 잡았습니다. 읽기 실패를 None으로 확인하는 것은 OpenCV의 오랜 약속입니다.',
    )
    _fill_lesson(
        'cv-filters',
        history='가우시안 흐림은 19세기 통계의 정규분포에서, Canny 에지는 1986년 John Canny의 논문에서 이어집니다. 커널이 커지면 잡음과 함께 세부도 사라질 수 있습니다.',
        youtube=YT_BLUR,
    )
    _fill_lesson(
        'cv-transform',
        history='원근 변환은 사영기하의 호모그래피입니다. 평면의 네 점을 새 사각형에 대응시키는 방법은 사진 측량과 문서 스캔에서 오래 쓰였습니다.',
    )
    _fill_lesson(
        'cv-features',
        history='Sobel(1968)과 Canny(1986)는 경계를, Harris(1988) 계열은 코너를 찾습니다. 윤곽선은 이진 영역의 둘레를 잇는 고전적인 측정입니다.',
        youtube=YT_SOBEL,
    )
    _fill_lesson(
        'cv-haar',
        history='2001년 Viola와 Jones는 Haar-like 특징과 단계적 분류로 얼굴을 빠르게 찾았습니다. 위치 검출이지 개인 식별이 아닙니다.',
        youtube=YT_HAAR,
    )
    _fill_lesson(
        'cv-yolo',
        history='2016년 Redmon 등의 YOLO는 상자와 클래스 점수를 한 번에 예측했습니다. 이 단원은 교과서의 YOLOv8 경로를 다루며, 특정 버전을 최신이라고 부르지 않습니다.',
        youtube=YT_YOLO,
    )
    _fill_lesson(
        'cv-project',
        history='실험 조건을 한 장에 남기는 형식은 실험실 노트에서 왔습니다. 입력·처리 순서·비교·한계를 적으면 같은 사진을 다시 돌릴 수 있습니다.',
    )


def _fill_examples():
    _fill_example(
        'cv-process-vs-vision',
        history='영상 처리는 화질을 바꾸는 일에, 컴퓨터 비전은 장면에서 기호를 읽는 일에 가깝습니다. 두 단어가 섞여 쓰이던 시절부터 교실에서는 출력을 보고 구별합니다.',
    )
    _fill_example(
        'cv-use-fields',
        history='공장 검사와 교통 안내는 비전을 일찍 쓴 분야입니다. 이점만 적고 오판을 빼면 수업 설계가 기울어집니다.',
    )
    _fill_example(
        'cv-shape-size',
        history='배열의 size와 화면의 픽셀 수를 헷갈리는 일은 컬러 채널이 생기면서 늘었습니다. 교과서 150쪽도 이 구별을 요구합니다.',
    )
    _fill_example(
        'cv-pillow',
        history='PIL은 1990년대 파이썬 이미지 편집의 기본 도구였고, Pillow가 그 인터페이스를 이어 받았습니다.',
    )
    _fill_example(
        'cv-filters',
        history='같은 사진에 여러 필터를 나란히 두는 비교는 교재의 기본 습관입니다. 커널과 임계값을 바꾸고 표를 남깁니다.',
    )
    _fill_example(
        'cv-features',
        history='경계·꼭짓점·둘레를 한 장에 비교하는 방법은 특징 검출 장의 고전입니다. 그림의 점 개수는 설정에 따라 달라집니다.',
    )
    _fill_example(
        'cv-haar-vs-id',
        history='얼굴이 있는 칸을 찾는 일과 신원을 맞히는 일은 연구도 제품도 오래 분리되어 있었습니다. 교실 예제는 앞쪽만 다룹니다.',
    )
    _fill_example(
        'cv-count',
        history='프레임마다 다시 세는 습관은 실시간 검출 시연에서 왔습니다. 합계를 방문자 수로 읽으면 같은 사람을 여러 번 셉니다.',
    )
    _fill_example(
        'cv-scan-card',
        history='문서 스캔 파이프라인은 원근 보정과 이진화의 교실 프로젝트로 자주 쓰입니다. 한 순서를 정답처럼 외우지 말고 같은 입력에서 비교합니다.',
    )


def unit4_history_lessons():
    """Lessons that must show a history one-liner after #61."""
    return [lesson['id'] for lesson in units[4]]


def unit4_youtube_lessons():
    """Lessons that have a verified public video (transform/project stay empty).

    cv-pixels/cv-pipeline share the same Crash Course video as cv-overview,
    and cv-io shares the same OpenCV course video as cv-libraries (#63
    dedup); those URLs stay on cv-overview and cv-libraries only.
    """
    return [
        'cv-overview', 'cv-libraries',
        'cv-filters', 'cv-features', 'cv-haar', 'cv-yolo',
    ]
