"""Unit III history/youtube tip seeds for #60. Applied after unit3_pre_api.

Fills empty tips.history / tips.youtube on Unit III lessons. Does not invent
links: only oEmbed-verified public education videos (Crash Course, StatQuest,
Google Developers, Corey Schafer, freeCodeCamp). Empty stays empty where
nothing solid exists (preprocess walkthrough, project wrap-up).
"""
from content import examples, units
from slots import youtube_items

# oEmbed 200 (2026-09-15): title | channel
YT_CRASH_ML = {
    'title': 'Machine Learning & Artificial Intelligence: Crash Course Computer Science #34',
    'url': 'https://www.youtube.com/watch?v=z-EtmaFJieY',
    'note': '영어 공개 강의(약 12분)입니다. AI와 머신러닝이 어떻게 다른지, 스팸·추천처럼 어디에 쓰이는지만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_CRASH_ML_TYPES = {
    **YT_CRASH_ML,
    'note': '영어 공개 강의입니다. 데이터를 보고 예측하는 부분과 강화 학습(AlphaGo) 언급만 보면 이 주제와 맞습니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_STATQUEST_INTRO = {
    'title': 'A Gentle Introduction to Machine Learning (StatQuest)',
    'url': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI',
    'note': '영어 공개 강의입니다. 특성·정답·모델이 무엇인지만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_FCC_ML = {
    'title': 'Machine Learning for Everybody – Full Course (freeCodeCamp)',
    'url': 'https://www.youtube.com/watch?v=i_LwzRVP7bg',
    'note': '영어 공개 강의입니다. 목차의 train/test 분할 구간만 보면 됩니다. 나머지 긴 코스는 건너뛰어도 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_PANDAS = {
    'title': 'Python Pandas Tutorial (Part 1): Getting Started with Data Analysis (Corey Schafer)',
    'url': 'https://www.youtube.com/watch?v=ZyhVh-qRZPA',
    'note': '영어 공개 강의입니다. DataFrame을 만들고 head로 앞부분을 보는 앞부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_RECIPES = {
    'title': 'Hello World — Machine Learning Recipes #1 (Google for Developers)',
    'url': 'https://www.youtube.com/watch?v=cKxRvEZd3Mw',
    'note': '영어 공개 강의(약 7분)입니다. 과일을 분류하는 첫 모델만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_LINEAR = {
    'title': 'Linear Regression, Clearly Explained!!! (StatQuest)',
    'url': 'https://www.youtube.com/watch?v=nk2CQITm_eo',
    'note': '영어 공개 강의입니다. 직선으로 숫자를 예측하는 아이디어만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_KMEANS = {
    'title': 'StatQuest: K-means clustering',
    'url': 'https://www.youtube.com/watch?v=4b5d3muPQmA',
    'note': '영어 공개 강의입니다. 중심을 정하고 가까운 점을 묶는 반복만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_CONFUSION = {
    'title': 'Machine Learning Fundamentals: The Confusion Matrix (StatQuest)',
    'url': 'https://www.youtube.com/watch?v=Kdsp6soqA7o',
    'note': '영어 공개 강의입니다. 실제와 예측을 표로 나누는 부분만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}
YT_CV = {
    'title': 'Machine Learning Fundamentals: Cross Validation (StatQuest)',
    'url': 'https://www.youtube.com/watch?v=fSytzGwwBVw',
    'note': '영어 공개 강의입니다. 훈련 자료를 나눠 검증 역할을 바꾸는 이유만 보면 됩니다. 학교 네트워크·연령 정책을 확인하세요.',
}


def _lesson(lid):
    return next(item for item in units[3] if item['id'] == lid)


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
    """Seed Unit III history/youtube after density/pre_api have run."""
    _fill_lessons()
    _fill_examples()


def _fill_lessons():
    _fill_lesson(
        'ml-overview',
        history='1956년 다트머스 워크숍에서 AI라는 이름이 쓰였고, 1959년 Arthur Samuel이 머신러닝이라는 말을 썼습니다. 2012년 ImageNet의 AlexNet은 딥러닝이 사진 분류에서 두드러진 사례입니다.',
        youtube=YT_CRASH_ML,
    )
    _fill_lesson(
        'ml-use',
        history='1990년대 스팸 필터와 2000년대 추천 시스템은, 규칙을 다 쓰기 어려운 패턴을 데이터에서 배우는 쪽이 더 실용적임을 보여 주었습니다.',
        youtube=YT_CRASH_ML,
    )
    _fill_lesson(
        'ml-process',
        history='훈련과 평가를 나누는 습관은 1990년대 이후 표준이 되었습니다. 전처리 값도 훈련 부분에서만 구해야 새 데이터 평가가 공정합니다.',
        youtube=YT_FCC_ML,
    )
    _fill_lesson(
        'ml-terms',
        history='퍼셉트론(1958)은 데이터로 가중치를 배웠습니다. k-NN의 k처럼 학습 전에 고르는 값은 나중에 하이퍼파라미터라고 부르게 되었습니다.',
        youtube=YT_STATQUEST_INTRO,
    )
    _fill_lesson(
        'ml-methods',
        history='지도 학습은 정답이 있는 자료, 비지도는 정답 없이 구조를 찾습니다. 강화 학습은 벨만의 동적 계획과 서튼의 시행착오 학습에서 이어집니다.',
        youtube=YT_CRASH_ML_TYPES,
    )
    _fill_lesson(
        'ml-libraries',
        history='NumPy(2006), pandas(2008), scikit-learn(2007~2010)은 배열·표·학습 도구를 파이썬에서 같은 흐름으로 쓰게 했습니다.',
        youtube=YT_PANDAS,
    )
    _fill_lesson(
        'ml-preprocess',
        history='결측과 스케일 변환은 통계의 표준화에서 왔습니다. 평균과 최댓값을 전체 데이터로 구하면 평가가 새어 나갑니다.',
    )
    _fill_lesson(
        'ml-classification',
        history='k-NN은 1951년 Fix·Hodges의 이웃 규칙에서, 로지스틱 회귀는 통계의 범주 모형에서, SVM은 1995년 Vapnik 등에서 이어집니다.',
        youtube=YT_RECIPES,
    )
    _fill_lesson(
        'ml-regression',
        history='최소제곱 직선은 1800년대 초 가우스·르장드르가 정리했습니다. 머신러닝에서는 같은 식을 예측 모델로 씁니다.',
        youtube=YT_LINEAR,
    )
    _fill_lesson(
        'ml-cluster',
        history='K-평균은 1957년 Steinhaus, 1967년 MacQueen으로 이어진 중심 갱신 방법입니다. 군집 번호 자체에는 순위가 없습니다.',
        youtube=YT_KMEANS,
    )
    _fill_lesson(
        'ml-metrics',
        history='혼동행렬은 의학·정보검색에서 쓰이던 오류 분류표입니다. 정밀도·재현율은 어떤 실수를 줄일지에 따라 고릅니다.',
        youtube=YT_CONFUSION,
    )
    _fill_lesson(
        'ml-selection',
        history='교차 검증은 1974년 Stone 등이 일반화 성능을 나누어 추정하려고 정리했습니다. 설정 선택은 검증, 최종 보고는 테스트입니다.',
        youtube=YT_CV,
    )
    _fill_lesson(
        'ml-project',
        history='재현 가능한 실험 기록은 과학 논문의 습관입니다. 문제·분할·난수·지표·한계를 한 카드에 남기면 같은 코드를 다시 돌릴 수 있습니다.',
    )


def _fill_examples():
    _fill_example(
        'ml-rule-vs-learn',
        history='초기의 많은 인공지능은 규칙을 직접 입력했습니다. 데이터가 늘면서, 사례에서 패턴을 모으는 쪽이 스팸·추천처럼 예외가 많은 문제에 쓰이기 시작했습니다.',
    )
    _fill_example(
        'ml-loan-data',
        history='예측 시점에 없는 열을 빼는 습관은 시계열·시험 점수처럼 “아직 모르는 값”을 다루는 통계에서 오래되었습니다.',
    )
    _fill_example(
        'ml-split-small',
        history='한 번 본 점수로 모델을 고르면 그 점수는 더 이상 독립적인 평가가 아닙니다. 검증과 테스트를 나누는 이유입니다.',
        youtube=YT_FCC_ML,
    )
    _fill_example(
        'ml-tools',
        history='표 계산은 스프레드시트보다 코드로 반복하기 위해 pandas가 만들어졌습니다. 배열 연산의 뼈대는 NumPy입니다.',
        youtube=YT_PANDAS,
    )
    _fill_example(
        'ml-classify',
        history='같은 자료로 여러 분류기를 나란히 두는 비교는 교재와 경진 대회의 기본 습관입니다. 선택은 테스트가 아니라 검증으로 합니다.',
        youtube=YT_RECIPES,
    )
    _fill_example(
        'ml-cluster',
        history='중심을 옮기며 묶는 방법은 통계 군집화의 고전입니다. 그림의 색은 이름일 뿐 순위가 아닙니다.',
        youtube=YT_KMEANS,
    )
    _fill_example(
        'ml-report-card',
        history='실험 조건을 한 장에 남기는 형식은 실험실 노트에서 왔습니다. 수행평가 저널도 같은 항목을 코드와 함께 제출합니다.',
    )


def unit3_history_lessons():
    """Lessons that must show a history one-liner after #60."""
    return [lesson['id'] for lesson in units[3]]


def unit3_youtube_lessons():
    """Lessons that have a verified public video (preprocess/project stay empty)."""
    return [
        'ml-overview', 'ml-use', 'ml-process', 'ml-terms', 'ml-methods',
        'ml-libraries', 'ml-classification', 'ml-regression', 'ml-cluster',
        'ml-metrics', 'ml-selection',
    ]
