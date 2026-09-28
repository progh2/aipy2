"""3단원(파이썬과 머신러닝) 소단원별 슬라이드·설명·실습 데이터 (#131).

형식은 tools/web/deck_u2.py 머리말과 완전히 같다 — build.py가 LESSONS를 읽어
"PPT 슬라이드 화면 → 설명 → 실습 → 연습 문제 → 저널" 순서로 소단원 페이지를
만든다. explain·practice는 비워 둔다(C 담당: 3단원 설명·실습 채우기).

LESSONS[소단원id] = dict(title=..., pages=..., slides=[dict(n=.., alt=.., explain=[]), ...],
                          practice=[예제id 문자열 또는 dict(kind='tutorial', ...), ...])

## A가 정리한 예제 keep/exclude 목록 (practice 채울 때 참고용 — 강제 아님)

교과서에 실린 코드·실행 결과를 재현한 예제만 "keep" 후보로 남긴다. 이름은
설명적이지만 교과서에 없는 상황을 지어낸 예제("억지 예제")는 제외한다.
이 예제들은 unit3_density.py가 정의하지만(제거하지 않음, 하위 호환), 어떤
소단원 practice도 더는 이들을 가리키지 않는다:
  EXCLUDE: ml-rule-vs-learn, ml-nesting, ml-history-cases, ml-when-not,
           ml-loan-data, ml-report-card
           (unit3_density.py가 이 6개를 lesson['examples']에 강제로 덮어쓰지만
           practice 목록에는 넣지 않는다)

KEEP 후보 (later_units.py 정의, 교과서 쪽 연계):
  ml-overview:      (교과서 62~67쪽은 개념 설명 위주 — 전용 코드 예제 없음)
  ml-use:           (68~70쪽도 개념 설명 위주 — 전용 코드 예제 없음)
  ml-process:       ml-split-small (훈련/검증/테스트 분할 원리, 웹 실행)
  ml-terms:         (76~78쪽 — 전용 코드 예제 없음. X/y 표는 ml-classify로 연결 가능)
  ml-methods:       (79~84쪽 — 전용 코드 예제 없음)
  ml-libraries:     ml-tools(85~89쪽 NumPy·pandas), ml-chart(빈도 막대그래프),
                     ml-seaborn(Seaborn countplot, PC 실행)
  ml-preprocess:    ml-clean(결측치·이상치), ml-scale(스케일링·인코딩, 90~100쪽)
  ml-classification: ml-classify(103~105쪽 붓꽃 4모델 비교), ml-knn-small(웹 원리)
  ml-regression:    ml-regression(106~107, 121~123쪽 MAE/MSE/R²), ml-housing(PC),
                     ml-line-small(웹 원리)
  ml-cluster:       ml-cluster(108~111쪽 K-평균), ml-kmeans-small(웹 원리)
  ml-metrics:       ml-metrics(117~120쪽 혼동행렬), ml-confusion-small(웹 원리)
  ml-selection:     ml-selection(112~116, 124~128쪽 교차검증/GridSearchCV),
                     ml-learning-curve(학습 곡선), ml-cv-small(웹 원리)
  ml-project:       (129~131쪽 종합 — 앞 소단원 예제 재사용 권장, 전용 예제 없음)

전체 sklearn 파이프라인 예제(ml-classify/ml-housing/ml-selection/ml-learning-curve
등)는 mode='pc'로 이미 표시돼 있다 — 브라우저에서는 문법만 확인하고 실제 실행은
PC에서 한다(later_units.py의 기존 설계, 그대로 유지).
"""

LESSONS = {
    'ml-overview': dict(
        title='머신러닝이란? — AI·머신러닝·딥러닝의 관계',
        pages='63–67',
        slides=[
            dict(n=6, alt='인공지능·머신러닝·딥러닝의 차이점', explain=[]),
            dict(n=7, alt='세 개념의 포함 관계 — AI ⊃ 머신러닝 ⊃ 딥러닝', explain=[]),
            dict(n=8, alt='머신러닝의 역사와 발전(1950~현재)', explain=[]),
            dict(n=9, alt='현실 속 머신러닝 적용 사례', explain=[]),
        ],
        practice=[],
    ),
    'ml-use': dict(
        title='머신러닝의 필요성과 활용',
        pages='68–70',
        slides=[
            dict(n=11, alt='데이터 기반 의사 결정의 중요성', explain=[]),
            dict(n=12, alt='다양한 산업 분야에서의 머신러닝 활용', explain=[]),
            dict(n=13, alt='미래 사회와 머신러닝', explain=[]),
        ],
        practice=[],
    ),
    'ml-process': dict(
        title='머신러닝 문제 해결 과정',
        pages='71–75',
        slides=[
            dict(n=16, alt='여섯 단계로 문제를 해결한다', explain=[]),
            dict(n=17, alt='1. 문제 정의 — 예측하고자 하는 것 찾기', explain=[]),
            dict(n=18, alt='2. 데이터 수집과 탐색', explain=[]),
            dict(n=19, alt='3. 데이터 전처리 — 정제와 변환', explain=[]),
            dict(n=20, alt='4. 모델 선택 · 5. 모델 학습과 평가', explain=[]),
            dict(n=21, alt='6. 결과 해석과 응용', explain=[]),
        ],
        practice=[],
    ),
    'ml-terms': dict(
        title='머신러닝의 주요 용어',
        pages='76–78',
        slides=[
            dict(n=23, alt='데이터 세트 · 특성 · 레이블', explain=[]),
            dict(n=24, alt='훈련 · 검증 · 테스트', explain=[]),
            dict(n=25, alt='과대 적합 · 과소 적합', explain=[]),
            dict(n=26, alt='하이퍼파라미터 · 성능 평가 지표', explain=[]),
        ],
        practice=[],
    ),
    'ml-methods': dict(
        title='머신러닝 학습 방법의 종류',
        pages='79–82',
        slides=[
            dict(n=30, alt='1. 지도 학습 — 분류와 회귀', explain=[]),
            dict(n=31, alt='2. 비지도 학습 — 군집화와 차원 축소', explain=[]),
            dict(n=32, alt='3. 강화 학습 — 보상을 통한 학습', explain=[]),
            dict(n=33, alt='세 가지 학습 방식 한눈에 비교', explain=[]),
            dict(n=37, alt='01. 머신러닝 개요 핵심 정리(개념·역사·문제 해결 과정·용어·학습 방법)', explain=[]),
        ],
        practice=[],
    ),
    'ml-libraries': dict(
        title='파이썬 머신러닝 라이브러리 소개',
        pages='86–89',
        slides=[
            dict(n=41, alt='1. scikit-learn — 대표적인 머신러닝 라이브러리', explain=[]),
            dict(n=42, alt='2. numpy — 수치 계산', explain=[]),
            dict(n=43, alt='3. pandas — 데이터 처리', explain=[]),
            dict(n=44, alt='4. matplotlib · seaborn — 데이터 시각화', explain=[]),
            dict(n=48, alt='네 라이브러리는 한 팀입니다 — pandas→numpy→scikit-learn→시각화', explain=[]),
            dict(n=49, alt='시각화 코드는 실행하면 이렇게 보입니다(88쪽 matplot_exam.py 실행 결과)', explain=[]),
        ],
        practice=[],
    ),
    'ml-preprocess': dict(
        title='데이터 준비와 전처리',
        pages='90–102',
        slides=[
            dict(n=50, alt='1. 데이터 불러오기 — CSV, Excel', explain=[]),
            dict(n=51, alt='2. 데이터 탐색 — head() · describe() · info()', explain=[]),
            dict(n=52, alt='탐색 결과 읽는 법(head·describe 실행 결과)', explain=[]),
            dict(n=53, alt='3. 결측치 확인 — isnull().sum()', explain=[]),
            dict(n=54, alt='결측치 제거와 채우기 — dropna() · fillna()', explain=[]),
            dict(n=55, alt='평균·중앙값으로 채우기, 이상치 처리', explain=[]),
            dict(n=56, alt='4. 데이터 변환 ① 정규화(Min-Max)', explain=[]),
            dict(n=57, alt='4. 데이터 변환 ② 표준화(Standardization)', explain=[]),
            dict(n=58, alt='5. 범주형 데이터 인코딩 — 원-핫 인코딩', explain=[]),
            dict(n=59, alt='6. 데이터 분할 — train_test_split', explain=[]),
            dict(n=60, alt='전처리 흐름 정리(불러오기→탐색→결측·이상치→변환→분할)', explain=[]),
            dict(n=63, alt='스케일링을 하면 무엇이 변할까요(99쪽 표준화 그림 읽기)', explain=[]),
            dict(n=64, alt='전처리의 함정 — 테스트 데이터로 fit 하지 않는다', explain=[]),
        ],
        practice=[],
    ),
    'ml-classification': dict(
        title='주요 알고리즘 활용 · 분류',
        pages='103–105',
        slides=[
            dict(n=67, alt='1. 분류 — 네 가지 대표 알고리즘(k-NN·로지스틱·트리·SVM)', explain=[]),
            dict(n=68, alt='K-최근접 이웃으로 붓꽃 분류하기 — 코드', explain=[]),
            dict(n=69, alt='K-최근접 이웃 — 실행 결과와 해석', explain=[]),
            dict(n=78, alt='K를 바꾸면 성능이 어떻게 변할까요(같은 분할에서 k 비교)', explain=[]),
            dict(n=79, alt='결정 경계로 보는 K의 의미(꽃잎 길이·너비 2특성 시각화)', explain=[]),
        ],
        practice=[],
    ),
    'ml-regression': dict(
        title='주요 알고리즘 활용 · 회귀 / 회귀와 수치 오차',
        pages='106–107, 121–123',
        slides=[
            dict(n=72, alt='2. 회귀 — 선형 회귀(Linear Regression)', explain=[]),
            dict(n=73, alt='선형 회귀 — 계수와 절편 읽는 법', explain=[]),
            dict(n=91, alt='회귀 모델 성능 평가 지표 — MSE · MAE · R²', explain=[]),
            dict(n=92, alt='주택 가격 모델 — 지표 읽는 법', explain=[]),
        ],
        practice=[],
    ),
    'ml-cluster': dict(
        title='주요 알고리즘 활용 · 군집화',
        pages='108–111',
        slides=[
            dict(n=74, alt='3. 군집화 — K-평균(K-Means)', explain=[]),
            dict(n=75, alt='K-평균 — 결과 해석과 장단점', explain=[]),
            dict(n=80, alt='군집화 그래프, 실제로 이렇게 나옵니다(110쪽 clustering 실행 결과)', explain=[]),
            dict(n=81, alt='K는 어떻게 정할까요 — 엘보 방법', explain=[]),
        ],
        practice=[],
    ),
    'ml-metrics': dict(
        title='모델 평가와 선택 · 분류 지표',
        pages='117–120',
        slides=[
            dict(n=85, alt='4. 분류 평가의 출발점 — 혼동 행렬', explain=[]),
            dict(n=86, alt='분류 지표 실습 — 유방암 데이터', explain=[]),
            dict(n=87, alt='정확도 · 정밀도 · 재현율 · F1 점수', explain=[]),
            dict(n=88, alt='유방암 모델 결과 해석 — 두 가지 오류(FP·FN)', explain=[]),
            dict(n=95, alt='혼동 행렬을 그림으로 읽어요(119쪽 실행 결과 히트맵)', explain=[]),
        ],
        practice=[],
    ),
    'ml-selection': dict(
        title='모델 평가와 선택 · 교차 검증·튜닝·학습 곡선',
        pages='112–116, 124–128',
        slides=[
            dict(n=82, alt='1. 데이터 분할 — 일반화 성능을 재는 저울', explain=[]),
            dict(n=83, alt='2. 교차 검증 — 더 믿을 수 있는 평가', explain=[]),
            dict(n=84, alt='3. 하이퍼파라미터 튜닝 — GridSearchCV', explain=[]),
            dict(n=93, alt='5. 모델 성능 시각화 — 학습 곡선', explain=[]),
            dict(n=94, alt='학습 곡선 실습 — learning_curve.py', explain=[]),
            dict(n=96, alt='학습 곡선, 실제 그래프로 진단해요(126쪽 실행 결과)', explain=[]),
            dict(n=97, alt='실습 미션: 고치고, 바꾸고, 근거를 남겨요', explain=[]),
            dict(n=98, alt='수행② 전, 이 다섯 가지를 확인해요', explain=[]),
        ],
        practice=[],
    ),
    'ml-project': dict(
        title='모델 구현·평가 프로젝트와 단원 정리',
        pages='129–131 + 확장',
        slides=[
            dict(n=99, alt='종합 실습 — Iris 데이터로 분류 모델 만들고 수행②로 연결', explain=[]),
            dict(n=100, alt='02. 머신러닝 라이브러리 활용 핵심 정리', explain=[]),
            dict(n=104, alt='정리하며 — 머신러닝은 데이터로 스스로 배운다(단원 전체 세 문장 요약)', explain=[]),
        ],
        practice=[],
    ),
}
