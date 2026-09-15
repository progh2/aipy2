"""Unit III pre_api/glossary fill for #60. Applied after unit3_density.

Adds or completes code-before cards for every Unit III topic and example.
Does not seed history/youtube. Real science PNGs (not invented GUI shots)
are attached only where render_science.py already produced them.
"""
from content import examples, units
from slots import api_items, glossary_items, shot_items


def _ex(eid):
    return examples[eid]


def _lesson(lid):
    return next(lesson for lesson in units[3] if lesson['id'] == lid)


def _fill_api(eid, items):
    rec = _ex(eid)
    if not rec['pre_api']:
        rec['pre_api'] = api_items(items)


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


def _fill_shot(eid, src, alt, caption):
    rec = _ex(eid)
    if not rec['screenshots']:
        rec['screenshots'] = shot_items([{'src': src, 'alt': alt, 'caption': caption}])


def apply():
    """Fill Unit III pre_api/glossary after the #60 density examples exist."""
    _fill_lessons()
    _fill_missing_example_api()
    _complete_example_glossary()
    _attach_science_shots()


def _fill_lessons():
    _fill_lesson('ml-overview', pre_api=[
        {'name': '세 겹의 범위', 'signature': '인공지능 ⊃ 머신러닝 ⊃ 딥러닝',
         'note': '규칙을 쓰는 프로그램도 인공지능일 수 있습니다. 아래는 규칙 vs 학습을 같은 페이지에서 비교합니다.'},
    ], glossary=[
        {'term': '딥 블루', 'meaning': '탐색과 평가 함수로 체스를 둔 프로그램입니다. 다층 신경망을 학습한 모델이 아닙니다.'},
    ])
    _fill_lesson('ml-use', pre_api=[
        {'name': '문제 카드', 'signature': '입력 데이터 → 예측할 출력',
         'note': '규칙을 정확히 쓸 수 있으면 일반 프로그램이 낫습니다. 대출·검사·추천은 입력과 예측을 먼저 적습니다.'},
    ], glossary=[
        {'term': '대표하지 않는 데이터', 'meaning': '모은 조건 밖에서 오류가 늘어납니다. 예측을 사실로 단정하지 않습니다.'},
    ])
    _fill_lesson('ml-process', pre_api=[
        {'name': '나누는 순서', 'signature': '문제·기준 → 분할 → 훈련에서만 전처리 → 검증 → 테스트',
         'note': '평가용 자료는 먼저 떼어 둡니다. 평균·스케일도 훈련 부분에서만 구합니다.'},
    ], glossary=[
        {'term': '검증과 테스트', 'meaning': '검증은 모델·설정을 고를 때, 테스트는 선택을 마친 뒤 한 번 보고할 때 씁니다.'},
    ])
    _fill_lesson('ml-terms', pre_api=[
        {'name': 'X / y / 설정', 'signature': 'X 특성표  ·  y 정답  ·  하이퍼파라미터',
         'note': '한 행이 한 관측입니다. 가중치는 학습이 정하고, k 같은 값은 학습 전에 정합니다.'},
    ], glossary=[
        {'term': '데이터 누수', 'meaning': '예측 시점에 없는 정보를 X에 넣는 것입니다. 점수는 높아져도 현실에서 쓸 수 없습니다.'},
    ])
    _fill_lesson('ml-methods', pre_api=[
        {'name': '학습의 종류', 'signature': '지도(분류/회귀)  ·  비지도  ·  강화',
         'note': '정답이 있는지, 범주인지 숫자인지, 행동에 보상이 있는지로 먼저 고릅니다.'},
    ], glossary=[
        {'term': '정책', 'meaning': '상태를 보고 행동을 고르는 전략입니다. 한 번의 보상보다 누적 보상을 봅니다.'},
    ])
    _fill_lesson('ml-libraries', pre_api=[
        {'name': '도구 역할', 'signature': 'NumPy 배열  ·  pandas 표  ·  sklearn 학습  ·  그래프',
         'note': '웹에서는 배열·표·그래프와 작은 원리 실습을 실행합니다. 전체 파이프라인은 PC에서 돌립니다.'},
    ], glossary=[
        {'term': '설치 이름', 'meaning': 'scikit-learn을 설치하고 import sklearn 합니다. 설치 이름과 import 이름이 다릅니다.'},
    ])
    _fill_lesson('ml-preprocess', pre_api=[
        {'name': '훈련에서만 배우기', 'signature': 'fit / fit_transform(train)  →  transform(test)',
         'note': '중앙값·최솟값·범주 목록을 테스트에 맞추면 평가가 새어 나갑니다. 이상치는 삭제 전에 의미를 확인합니다.'},
    ], glossary=[
        {'term': '정규화 / 표준화', 'meaning': 'MinMax는 훈련 최솟값·최댓값, Standard는 훈련 평균·표준편차입니다. 분포 모양을 정규분포로 바꾸지는 않습니다.'},
    ])
    _fill_lesson('ml-classification', pre_api=[
        {'name': '분류기', 'signature': 'k-NN · 로지스틱 · 트리 · SVM',
         'note': '로지스틱 회귀는 분류입니다. 거리 기반 모델은 파이프라인 안에서 스케일을 배웁니다.'},
    ], glossary=[
        {'term': 'stratify', 'meaning': '나눌 때 클래스 비율을 유지합니다. 붓꽃처럼 품종 수가 비슷해야 비교가 공정합니다.'},
    ])
    _fill_lesson('ml-regression', pre_api=[
        {'name': '숫자 예측과 오차', 'signature': 'ŷ = 가중합 + 절편  ·  MAE / MSE / R²',
         'note': '잔차는 예측과 정답의 차이입니다. R²는 평균 예측 기준이라 음수가 될 수 있습니다.'},
    ], glossary=[
        {'term': '단위', 'meaning': 'MAE는 원래 목표값 단위입니다. 숫자만 보지 말고 큰 오류 사례도 확인합니다.'},
    ])
    _fill_lesson('ml-cluster', pre_api=[
        {'name': 'K-평균', 'signature': 'K개 중심 → 배정 → 평균으로 갱신',
         'note': 'labels_는 그룹 이름입니다. 번호 2가 1보다 좋은 그룹이 아닙니다. K와 스케일이 결과를 바꿉니다.'},
    ], glossary=[
        {'term': 'n_init', 'meaning': '여러 초기 중심으로 다시 시도하는 횟수입니다. 한 번의 시작점에 결과가 묶이지 않게 합니다.'},
    ])
    _fill_lesson('ml-metrics', pre_api=[
        {'name': '양성을 먼저', 'signature': 'TP FP FN TN → 정확도·정밀도·재현율·F1',
         'note': '스팸을 양성으로 두면, 정상 메일을 스팸으로 보낸 것은 FP입니다. 불균형이면 정확도만 보지 않습니다.'},
    ], glossary=[
        {'term': '임계값', 'meaning': '확률을 양성으로 부를 기준입니다. 올리면 FP는 줄거나 같고 FN은 늘거나 같습니다.'},
    ])
    _fill_lesson('ml-selection', pre_api=[
        {'name': '고르기와 보고', 'signature': '교차 검증으로 선택  ·  테스트는 마지막에 한 번',
         'note': '전처리도 각 훈련 묶음에서 다시 배우도록 Pipeline을 씁니다. 데이터 스케일과 모델 규제는 다른 말입니다.'},
    ], glossary=[
        {'term': '학습 곡선', 'meaning': '훈련 샘플 수에 따른 훈련·검증 점수입니다. 둘 다 낮으면 과소, 훈련만 높으면 과대를 의심합니다.'},
    ])
    _fill_lesson('ml-project', pre_api=[
        {'name': '보고서 한 장', 'signature': '문제·분할·전처리·모델·지표·한계',
         'note': '같은 난수로 다시 돌릴 수 있게 적습니다. 점수가 나빠진 사례를 찾아 개선안을 제안합니다.'},
    ], glossary=[
        {'term': '수행 저널', 'meaning': '코드와 함께 내는 기록입니다. 변경 이유와 최종 테스트는 검증 선택과 구별해 적습니다.'},
    ])


def _fill_missing_example_api():
    _fill_api('ml-split-small', [
        {'name': '세 묶음', 'signature': 'train, validation, test = samples[:6], samples[6:8], samples[8:]',
         'note': '섞은 뒤 앞부분을 훈련, 가운데를 검증, 끝을 테스트로 둡니다. 세 묶음에 같은 번호가 겹치면 안 됩니다.'},
        {'name': 'random.Random(42)', 'signature': 'random.Random(42).shuffle(samples)',
         'note': '시드를 고정하면 같은 분할이 나옵니다. 수업에서 결과를 비교할 때 씁니다.'},
    ])
    _fill_api('ml-tools', [
        {'name': 'numpy.array', 'signature': 'np.array([10, 20, 30])',
         'note': '같은 형의 값을 담는 배열입니다. + 5처럼 원소마다 연산할 수 있습니다.'},
        {'name': 'DataFrame', 'signature': 'pd.DataFrame({"name": [...], "score": [...]})',
         'note': '열 이름이 있는 표입니다. head는 앞부분, describe는 수치 요약, info는 자료형과 결측입니다.'},
    ])
    _fill_api('ml-chart', [
        {'name': 'Counter', 'signature': 'Counter(["apple", "banana", "apple"])',
         'note': '항목별 개수 딕셔너리입니다. 막대 높이는 이 개수와 같아야 합니다.'},
        {'name': 'plt.bar / savefig', 'signature': 'plt.bar(이름, 개수)\nplt.savefig("frequency.png")',
         'note': '실행한 Python이 PNG를 만듭니다. 웹 결과 아래에 그림이 붙습니다.'},
    ])
    _fill_api('ml-seaborn', [
        {'name': 'to_excel / read_excel', 'signature': 'frame.to_excel("fruit.xlsx")\npd.read_excel(...)',
         'note': '엑셀 입출력입니다. openpyxl이 필요하고 PC에서 실행합니다.'},
        {'name': 'sns.countplot', 'signature': 'sns.countplot(data=frame, x="fruit")',
         'note': '범주 열의 빈도를 막대로 그립니다. Matplotlib 위에 통계 그림을 얹습니다.'},
    ])
    _fill_api('ml-scale-small', [
        {'name': '훈련 통계량', 'signature': 'mean, std, min, max = 훈련에서만',
         'note': '테스트 값 50을 정규화하면 (50-10)/(30-10)=2 입니다. 1을 넘을 수 있습니다.'},
        {'name': '표준화 / 정규화', 'signature': '(v-mean)/std  ·  (v-low)/(high-low)',
         'note': '둘 다 훈련 기준으로 새 값을 변환합니다. 표준화가 정규분포를 만들어 주지는 않습니다.'},
    ])
    _fill_api('ml-clean', [
        {'name': 'isna / dropna / fillna', 'signature': 'frame.isna().sum()\nframe.dropna()\nframe.fillna(...)',
         'note': '결측 개수를 본 뒤 지우거나 채웁니다. 예측 모델에서는 분할 후 훈련 통계량으로 채웁니다.'},
        {'name': '이상치 범위', 'signature': 'score < 0 또는 score > 100',
         'note': '1000점이 오타인지 실제 값인지 확인하기 전에 삭제하지 않습니다.'},
    ])
    _fill_api('ml-scale', [
        {'name': 'SimpleImputer', 'signature': 'imputer.fit_transform(train)\nimputer.transform(test)',
         'note': '중앙값 등 채울 값을 훈련에서 배웁니다. 테스트에는 transform만 씁니다.'},
        {'name': 'Scaler / OneHotEncoder', 'signature': 'MinMaxScaler · StandardScaler · OneHotEncoder',
         'note': 'handle_unknown="ignore"면 본 적 없는 범주는 0 벡터가 됩니다. 새 도시는 훈련 목록에 없습니다.'},
    ])
    _fill_api('ml-knn-small', [
        {'name': '거리와 k', 'signature': 'sorted(..., key=거리)[:k]',
         'note': '입력에 가까운 순서대로 k개를 고르고, 레이블 다수결로 예측합니다. k는 미리 정합니다.'},
    ])
    _fill_api('ml-classify', [
        {'name': 'train_test_split', 'signature': 'train_test_split(..., stratify=y, random_state=42)',
         'note': '같은 난수면 같은 분할입니다. stratify=y는 품종 비율을 유지합니다.'},
        {'name': 'make_pipeline', 'signature': 'make_pipeline(StandardScaler(), model)',
         'note': '스케일을 파이프라인 안에서 훈련합니다. 테스트에 따로 fit하지 않습니다.'},
    ])
    _fill_api('ml-line-small', [
        {'name': '최소제곱 기울기', 'signature': 'w = Σ(x-μx)(y-μy) / Σ(x-μx)²',
         'note': '직선 y = wx + b를 훈련 점으로 직접 구합니다. 훈련 MAE=0이 새 데이터 정확을 보장하지는 않습니다.'},
    ])
    _fill_api('ml-regression', [
        {'name': 'LinearRegression', 'signature': 'model.fit(X_train, y_train)\nmodel.predict(X_test)',
         'note': '특성의 가중합과 절편으로 숫자를 예측합니다. score는 훈련 R²입니다.'},
        {'name': '오차 지표', 'signature': 'mean_absolute_error · mean_squared_error · r2_score',
         'note': 'MAE는 원래 단위, MSE는 제곱, R²는 평균 예측과 비교합니다.'},
    ])
    _fill_api('ml-housing', [
        {'name': 'fetch_california_housing', 'signature': 'fetch_california_housing(return_X_y=True)',
         'note': '첫 실행에 자료를 내려받습니다. 네트워크가 없으면 내장 diabetes 예제를 쓰세요. 개인 예측용이 아닙니다.'},
    ])
    _fill_api('ml-kmeans-small', [
        {'name': '배정과 갱신', 'signature': '가까운 중심 → 그룹 평균 → 새 중심',
         'note': '중심이 더 이상 바뀌지 않으면 멈춥니다. 이 숫자는 1차원 개념 실습입니다.'},
    ])
    _fill_api('ml-cluster', [
        {'name': 'KMeans', 'signature': 'KMeans(n_clusters=3, n_init=10, random_state=42)',
         'note': 'labels_는 샘플별 번호, cluster_centers_는 중심 좌표입니다. 번호는 실행마다 뒤바뀔 수 있습니다.'},
        {'name': '산점도', 'signature': 'plt.scatter(..., c=labels)\nplt.savefig("clusters.png")',
         'note': '색은 그룹 이름입니다. 항상 동그란 덩어리가 있다고 가정하지 마세요.'},
    ])
    _fill_api('ml-confusion-small', [
        {'name': '임계값', 'signature': 'pred = int(p >= 0.5)',
         'note': '확률을 양성으로 부를 기준입니다. TP/FP/FN/TN을 직접 셉니다.'},
        {'name': '정밀도 / 재현율', 'signature': 'TP/(TP+FP)  ·  TP/(TP+FN)',
         'note': '분모가 0이면 계산하지 않습니다. 양성이 무엇인지에 따라 숫자가 달라집니다.'},
    ])
    _fill_api('ml-metrics', [
        {'name': 'confusion_matrix', 'signature': 'confusion_matrix(y_true, y_pred, labels=[0, 1])',
         'note': '행이 실제, 열이 예측입니다. labels를 지정해야 0/1 순서가 고정됩니다.'},
        {'name': '네 지표', 'signature': 'accuracy · precision · recall · f1',
         'note': '같은 예측 쌍으로 네 숫자를 비교합니다. 한 지표만으로 모델을 고르지 않습니다.'},
    ])
    _fill_api('ml-cv-small', [
        {'name': '폴드', 'signature': '한 묶음은 검증, 나머지는 훈련',
         'note': '역할을 번갈아 맡깁니다. 최종 테스트는 이 묶음 밖에 따로 둡니다.'},
    ])
    _fill_api('ml-selection', [
        {'name': 'cross_val_score', 'signature': 'cross_val_score(pipe, X_train, y_train, cv=3)',
         'note': '훈련 부분만 나눕니다. 테스트는 넘기지 않습니다.'},
        {'name': 'GridSearchCV', 'signature': 'GridSearchCV(pipe, {이웃 수: [3,5,7]}, cv=3)',
         'note': '설정 후보를 교차 검증으로 비교합니다. best_score_와 최종 테스트 점수는 다를 수 있습니다.'},
    ])
    _fill_api('ml-learning-curve', [
        {'name': 'learning_curve', 'signature': 'learning_curve(model, X, y, train_sizes=[...], cv=...)',
         'note': '훈련 샘플을 늘리며 훈련·검증 점수를 그립니다. 간격과 수준을 보고 다음 실험을 정합니다.'},
    ])


def _complete_example_glossary():
    _fill_glossary('ml-tools', [
        {'term': 'shape', 'meaning': '배열이나 표의 축별 길이입니다. (행, 열)을 먼저 확인합니다.'},
    ])
    _fill_glossary('ml-chart', [
        {'term': 'Agg', 'meaning': '화면 창 없이 그림을 파일로 저장하는 Matplotlib 백엔드입니다. 웹·서버에서 씁니다.'},
    ])
    _fill_glossary('ml-clean', [
        {'term': '탐색과 학습', 'meaning': '이 예제는 표를 살펴보는 용도입니다. 모델에 넣을 때는 분할 후 훈련 통계량을 씁니다.'},
    ])
    _fill_glossary('ml-classify', [
        {'term': '관찰용 비교', 'meaning': '테스트로 네 모델을 한 번 보는 실습입니다. 실제 선택은 훈련 부분 교차 검증으로 합니다.'},
    ])
    _fill_glossary('ml-regression', [
        {'term': '내장 자료', 'meaning': 'diabetes 자료는 원리 연습용입니다. 실제 개인 건강을 예측하는 용도가 아닙니다.'},
    ])
    _fill_glossary('ml-cluster', [
        {'term': '원형 가정', 'meaning': 'K-평균은 중심에 가까운 덩어리를 잘 찾습니다. 길쭉하거나 고리가 있으면 다른 방법을 검토합니다.'},
    ])
    _fill_glossary('ml-selection', [
        {'term': 'n_jobs=1', 'meaning': '병렬을 켜지 않습니다. 교실 컴퓨터에서 재현하기 쉽게 한 코어로 둡니다.'},
    ])


def _attach_science_shots():
    _fill_shot(
        'ml-chart',
        'assets/science/ml-chart.png',
        '과일 빈도 막대그래프',
        '제공 예제를 실행해 저장한 막대그래프입니다. 막대 높이는 Counter 개수와 같습니다.',
    )
    _fill_shot(
        'ml-cluster',
        'assets/science/ml-cluster.png',
        'K-평균 군집과 중심점',
        '제공 예제의 산점도입니다. 색은 군집 번호, 빨간 X는 중심입니다. 번호에 순위는 없습니다.',
    )
    _fill_shot(
        'ml-learning-curve',
        'assets/science/ml-learning-curve.png',
        '훈련·검증 학습 곡선',
        '제공 예제의 학습 곡선입니다. 샘플 수에 따라 두 점수가 어떻게 달라지는지 봅니다.',
    )


def unit3_pre_coverage():
    """Examples that must show a code-before card."""
    ids = []
    for lesson in units[3]:
        for eid in lesson['examples']:
            if eid not in ids:
                ids.append(eid)
    return ids
