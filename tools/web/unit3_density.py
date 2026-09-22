"""Unit III extra examples for #60. Imported at the end of later_units.py.

Adds role-based labs so thin overview topics (overview, use, terms,
methods, process, project) are independently complete. New APIs use
pre_api/glossary. Console examples stay screenshot-empty unless a real
science render already exists.
"""
from content import ex, units


def _lesson(lesson_id):
    return next(lesson for lesson in units[3] if lesson['id'] == lesson_id)


def _set_examples(lesson_id, ids):
    _lesson(lesson_id)['examples'] = list(ids)


ex('ml-rule-vs-learn', '규칙으로 쓰기 vs 데이터에서 배우기', {
    'main.py': '''def password_ok(password):
    return len(password) >= 8

spam_tokens = ["free", "winner", "prize"]

def looks_like_spam(text):
    words = text.lower().split()
    return any(token in words for token in spam_tokens)

print("규칙 기반 비밀번호:", password_ok("abc"), password_ok("longpass"))
print("데이터에서 본 단어:", looks_like_spam("Winner prize now"), looks_like_spam("숙제 제출합니다"))
''',
},
    checks='assert password_ok("abcdefgh") and not password_ok("short")\nassert looks_like_spam("free winner") and not looks_like_spam("숙제 제출합니다")',
    pre_api=[
        {'name': '사람이 쓴 규칙', 'signature': 'len(password) >= 8',
         'note': '조건을 코드에 직접 적습니다. 비밀번호 길이처럼 기준이 분명하면 머신러닝이 필요 없습니다.'},
        {'name': '데이터에서 본 패턴', 'signature': 'spam_tokens = ["free", "winner"]',
         'note': '자주 나온 단어를 목록에 모은 뒤 새 메일에 적용합니다. 진짜 학습 알고리즘은 아니지만, “규칙을 쓰기보다 사례를 모은다”는 역할만 보여 줍니다.'},
    ],
    glossary=[
        {'term': '규칙 기반', 'meaning': '사람이 조건과 예외를 작성합니다. 모든 인공지능이 머신러닝인 것은 아닙니다.'},
    ])

ex('ml-nesting', 'AI ⊃ 머신러닝 ⊃ 딥러닝', {
    'main.py': '''layers = [
    ("인공지능", "가장 넓은 범위", "비밀번호 길이 검사"),
    ("머신러닝", "데이터로 패턴을 배움", "스팸 분류"),
    ("딥러닝", "여러 층의 신경망", "이미지 특징 학습"),
]
for name, meaning, example in layers:
    print(f"{name}: {meaning} · 예: {example}")
print("포함 관계: 인공지능 ⊃ 머신러닝 ⊃ 딥러닝")
''',
},
    checks='assert layers[0][0] == "인공지능" and layers[-1][0] == "딥러닝"\nassert len(layers) == 3',
    pre_api=[
        {'name': '포함 관계', 'signature': '인공지능 ⊃ 머신러닝 ⊃ 딥러닝',
         'note': '딥러닝은 머신러닝의 한 종류이고, 머신러닝은 인공지능의 한 접근입니다. 방향을 뒤집으면 틀립니다.'},
    ],
    glossary=[
        {'term': '딥러닝', 'meaning': '여러 층의 신경망으로 특징을 배우는 머신러닝입니다. 모든 머신러닝이 딥러닝은 아닙니다.'},
    ])

ex('ml-history-cases', '딥 블루와 ImageNet은 같은 접근이 아니다', {
    'main.py': '''cases = [
    {"해": 1956, "이름": "다트머스", "접근": "이름과 연구 모임", "데이터 학습": "아님"},
    {"해": 1997, "이름": "딥 블루", "접근": "탐색과 평가 함수", "데이터 학습": "아님"},
    {"해": 2012, "이름": "AlexNet", "접근": "다층 신경망", "데이터 학습": "딥러닝"},
]
for row in cases:
    print(row["해"], row["이름"], row["접근"], "학습:", row["데이터 학습"])
print("딥 블루를 현대 딥러닝 모델과 같은 것으로 보지 마세요.")
''',
},
    checks='assert cases[1]["데이터 학습"] == "아님"\nassert cases[2]["데이터 학습"] == "딥러닝"',
    pre_api=[
        {'name': '접근을 구별하기', 'signature': '탐색·평가 함수  ≠  다층 신경망 학습',
         'note': '체스 프로그램의 승리가 곧 딥러닝은 아닙니다. 무엇을 데이터에서 배웠는지 먼저 묻습니다.'},
    ],
    glossary=[
        {'term': 'ImageNet 2012', 'meaning': '사진 분류 대회에서 깊은 신경망이 두드러진 성과를 낸 사례입니다. AI의 시작 연도가 아닙니다.'},
    ])

ex('ml-when-not', '규칙을 쓰는 편이 나은 문제', {
    'main.py': '''problems = [
    ("두 수의 합", "규칙이 한 줄", "일반 프로그램"),
    ("비밀번호 길이", "기준이 명확", "일반 프로그램"),
    ("다음 날 대출 권수", "패턴이 복잡", "머신러닝 후보"),
    ("제품 사진의 결함", "규칙을 다 쓰기 어려움", "머신러닝 후보"),
]
for name, reason, tool in problems:
    print(f"{name:14} → {tool}  ({reason})")
''',
},
    checks='assert problems[0][2] == "일반 프로그램"\nassert problems[2][2] == "머신러닝 후보"',
    pre_api=[
        {'name': '먼저 물을 것', 'signature': '규칙을 정확히 쓸 수 있는가?',
         'note': '사칙연산·유효성 검사는 조건문이 더 단순합니다. 추천·이미지·음성처럼 예외가 많을 때 학습을 검토합니다.'},
    ],
    glossary=[
        {'term': '오류 비용', 'meaning': '틀린 예측이 사람에게 미치는 영향입니다. 대출·의료·채점에서는 사람 확인을 함께 둡니다.'},
    ])

ex('ml-loan-data', '사서 역할 · 대출 예측에 모을 열', {
    'main.py': '''rows = [
    {"요일": "월", "어제_대출": 12, "시험기간": 0, "다음날_대출": 15},
    {"요일": "화", "어제_대출": 15, "시험기간": 0, "다음날_대출": 14},
    {"요일": "수", "어제_대출": 30, "시험기간": 1, "다음날_대출": 28},
]
x_keys = ["요일", "어제_대출", "시험기간"]
y_key = "다음날_대출"
X = [{key: row[key] for key in x_keys} for row in rows]
y = [row[y_key] for row in rows]
print("X (예측 때 알 수 있는 값):", X)
print("y (맞힐 정답):", y)
print("다음날_대출은 정답이므로 X에 넣지 않습니다.")
''',
},
    checks='assert y == [15, 14, 28]\nassert all("다음날_대출" not in row for row in X)',
    pre_api=[
        {'name': '입력 열 X', 'signature': '요일 · 어제_대출 · 시험기간',
         'note': '예측하는 시점에 이미 알 수 있는 값만 넣습니다. 다음 날 대출 권수는 아직 없습니다.'},
        {'name': '정답 열 y', 'signature': '다음날_대출',
         'note': '맞히고 싶은 값입니다. 학습할 때는 과거 기록의 정답을 쓰고, 실제 서비스에서는 이 값이 없습니다.'},
    ],
    glossary=[
        {'term': '대표성', 'meaning': '모은 날이 시험 기간만이면, 방학 예측이 어긋날 수 있습니다. 데이터의 범위를 함께 적습니다.'},
    ])

ex('ml-inspect', '검사원 역할 · 입력과 예측 출력', {
    'main.py': '''services = [
    {"역할": "추천", "입력": "이용 기록·항목 특성", "예측": "선호 가능성"},
    {"역할": "제조 검사", "입력": "제품 이미지", "예측": "정상/결함"},
    {"역할": "대출량", "입력": "과거 대출·요일", "예측": "예상 권수"},
]
for row in services:
    print(f"{row['역할']}: {row['입력']} → {row['예측']}")
print("예측을 사실로 단정하지 말고, 틀린 경우의 비용도 적으세요.")
''',
},
    checks='assert services[1]["예측"] == "정상/결함"\nassert len(services) == 3',
    pre_api=[
        {'name': '서비스 카드', 'signature': '입력 → 예측',
         'note': '무엇을 보고 무엇을 맞히는지 한 줄로 씁니다. 모델 이름보다 이 카드가 먼저입니다.'},
    ],
    glossary=[
        {'term': '사람의 확인', 'meaning': '결함으로 예측된 제품을 바로 폐기하기보다, 비용이 크면 사람이 한 번 더 봅니다.'},
    ])

ex('ml-success-mae', '성공 기준을 숫자로 적기', {
    'main.py': '''actual = [10, 12, 8, 14]
baseline = [11, 11, 11, 11]
model = [10, 11, 9, 12]

def mae(true, pred):
    return sum(abs(a - p) for a, p in zip(true, pred)) / len(true)

print("평균 예측 MAE:", mae(actual, baseline))
print("모델 MAE:", mae(actual, model))
print("성공?", mae(actual, model) < mae(actual, baseline))
''',
},
    checks='assert mae(actual, baseline) == 2\nassert mae(actual, model) == 1\nassert mae(actual, model) < mae(actual, baseline)',
    pre_api=[
        {'name': 'MAE', 'signature': 'sum(|정답-예측|) / n',
         'note': '권·원처럼 원래 단위의 평균 오차입니다. 모델이 나은지는 단순한 평균 예측과 비교해야 드러납니다.'},
    ],
    glossary=[
        {'term': '성공 기준', 'meaning': '“잘 맞힌다”만 쓰지 말고, 어떤 지표가 비교 대상보다 낮아야 하는지 적습니다.'},
    ])

ex('ml-xy-table', '같은 행의 X와 y를 맞추기', {
    'main.py': '''rows = [
    (["월", 12], 15),
    (["화", 15], 14),
    (["수", 30], 28),
]
X = [row[0] for row in rows]
y = [row[1] for row in rows]
print("샘플 수:", len(X), "특성 수:", len(X[0]))
print("X 형태: (샘플 수, 특성 수) =", (len(X), len(X[0])))
print("y 형태: (샘플 수,) =", (len(y),))
print("1번 행 X:", X[1], "→ y:", y[1])
''',
},
    checks='assert (len(X), len(X[0])) == (3, 2)\nassert len(y) == 3 and y[1] == 14',
    pre_api=[
        {'name': '한 행 = 한 관측', 'signature': 'X[i] 와 y[i]',
         'note': 'i번째 입력과 i번째 정답이 같은 사례여야 합니다. 순서가 어긋나면 학습이 잘못된 짝을 봅니다.'},
        {'name': '형태', 'signature': 'X: (샘플 수, 특성 수)  ·  y: (샘플 수,)',
         'note': '표의 열 개수가 특성 수입니다. 정답 열은 X에 넣지 않습니다.'},
    ],
    glossary=[
        {'term': '특성 / 레이블', 'meaning': '특성은 예측에 쓰는 입력, 레이블은 맞힐 정답입니다. 같은 행에서 짝을 이룹니다.'},
    ])

ex('ml-param-hyper', '배우는 값과 미리 정하는 값', {
    'main.py': '''from collections import Counter
training = [(1, "A"), (2, "A"), (8, "B"), (9, "B")]
x = 3
k = 3
neighbors = sorted(training, key=lambda row: abs(row[0] - x))[:k]
voted = Counter(label for _, label in neighbors).most_common(1)[0][0]
print("하이퍼파라미터 k:", k)
print("가까운 이웃:", neighbors)
print("이 데이터에서 정해진 예측:", voted)
''',
},
    checks='assert k == 3 and voted == "A"\nassert len(neighbors) == 3',
    pre_api=[
        {'name': '하이퍼파라미터', 'signature': 'k = 3',
         'note': '학습을 시작하기 전에 사람이 정합니다. 이웃 수 k, 트리의 최대 깊이가 이 자리에 해당합니다.'},
        {'name': '파라미터', 'signature': 'voted = 이웃의 다수결',
         'note': '이 예제의 예측은 주어진 자료에서 계산됩니다. 선형 모델의 가중치처럼, 데이터에 따라 달라지는 값이 파라미터입니다.'},
    ],
    glossary=[
        {'term': '과대 / 과소 적합', 'meaning': '훈련만 좋고 검증이 낮으면 과대, 둘 다 낮으면 과소 적합을 의심합니다. k를 바꾸며 검증 점수를 봅니다.'},
    ])

ex('ml-leakage', '미래 정답을 X에 넣으면', {
    'main.py': '''honest = {"어제_대출": 12, "시험기간": 1}
leaky = {"어제_대출": 12, "시험기간": 1, "다음날_대출": 28}
print("정직한 X:", honest)
print("새어 나간 X:", leaky)
print("예측 시점에는 다음날_대출을 모릅니다. 테스트 점수만 높아집니다.")
available_at_predict_time = set(honest)
print("누수?", "다음날_대출" in leaky and "다음날_대출" not in available_at_predict_time)
''',
},
    checks='assert "다음날_대출" not in honest\nassert "다음날_대출" in leaky',
    pre_api=[
        {'name': '데이터 누수', 'signature': '다음날_대출을 X에 포함',
         'note': '실제 서비스에서 없는 정보를 학습·평가에 쓰면 점수가 부풀려집니다. 미래 정답·시험 답안이 대표 사례입니다.'},
    ],
    glossary=[
        {'term': '예측 시점에 알 수 있는가', 'meaning': '특성인지 확인할 질문입니다. 아니오라면 y이거나 누수입니다.'},
    ])

ex('ml-classify-vs-regress', '범주를 맞히나, 숫자를 맞히나', {
    'main.py': '''tasks = [
    ("이메일 스팸 여부", "범주", "분류", "지도"),
    ("내일 기온", "연속 수치", "회귀", "지도"),
    ("고객을 비슷한 묶음으로", "정답 없음", "군집", "비지도"),
    ("미로에서 출구 찾기", "보상", "정책 학습", "강화"),
]
for name, target, kind, family in tasks:
    print(f"{family:4} | {kind:6} | {name} ({target})")
''',
},
    checks='assert tasks[0][2] == "분류" and tasks[1][2] == "회귀"\nassert tasks[2][3] == "비지도" and tasks[3][3] == "강화"',
    pre_api=[
        {'name': '세 갈래', 'signature': '정답 있음 / 정답 없음 / 상태·행동·보상',
         'note': '지도는 입력-정답 짝, 비지도는 구조, 강화는 행동의 누적 보상을 배웁니다. 군집은 비지도입니다.'},
    ],
    glossary=[
        {'term': '분류와 회귀', 'meaning': '둘 다 지도 학습입니다. 차이는 정답이 이름(범주)인지 숫자인지입니다.'},
    ])

ex('ml-unsupervised-groups', '정답 없이 가까운 값 묶기', {
    'main.py': '''values = [1, 2, 3, 18, 19, 21]
cut = (min(values) + max(values)) / 2
low = [v for v in values if v < cut]
high = [v for v in values if v >= cut]
print("기준:", cut)
print("묶음 0:", low)
print("묶음 1:", high)
print("0과 1은 이름일 뿐 순위가 아닙니다.")
''',
},
    checks='assert low == [1, 2, 3]\nassert high == [18, 19, 21]',
    pre_api=[
        {'name': '정답 열 없음', 'signature': 'values만 있고 y는 없음',
         'note': '비슷한 것끼리 묶는 것이 목적입니다. 이 예제의 기준은 최솟값·최댓값의 가운데로, 개념만 보여 줍니다.'},
    ],
    glossary=[
        {'term': '군집 번호', 'meaning': '그룹을 구별하는 이름입니다. 2번이 1번보다 좋은 그룹이라는 뜻은 없습니다.'},
    ])

ex('ml-rl-reward', '미로 보상 설계하기', {
    'main.py': '''reward = {"출구": 100, "벽": -10, "이동": -1, "제자리": -2}

def step(kind):
    return reward[kind]

path = ["이동", "이동", "벽", "이동", "출구"]
total = sum(step(kind) for kind in path)
print("경로:", path)
print("누적 보상:", total)
print("제자리만 반복하면:", step("제자리") * 5)
''',
},
    checks='assert step("출구") == 100 and step("벽") == -10\nassert total == 100 - 10 - 1 * 3',
    pre_api=[
        {'name': '보상', 'signature': '출구 +100  ·  벽 -10  ·  이동 -1',
         'note': '환경이 행동에 주는 점수입니다. 제자리 반복이 이득이 되지 않게 설계해야 합니다.'},
        {'name': '정책', 'signature': '상태 → 행동',
         'note': '지금 칸에서 어느 쪽으로 갈지 정하는 전략입니다. 장기 누적 보상을 높이도록 배웁니다.'},
    ],
    glossary=[
        {'term': 'Q-learning', 'meaning': '여러 강화 학습 알고리즘 중 하나입니다. 강화 학습 전체를 가리키는 말은 아닙니다.'},
    ])

ex('ml-logistic-name', '이름에 회귀가 있어도 분류인 모델', {
    'main.py': '''models = [
    ("로지스틱 회귀", "스팸/정상 확률", "분류"),
    ("선형 회귀", "다음 날 대출 권수", "회귀"),
    ("k-NN", "품종 이름", "분류"),
    ("결정 트리", "조건으로 나눈 범주", "분류"),
]
for name, output, kind in models:
    print(f"{name:8} → {output:14} ({kind})")
print("LogisticRegression은 분류 문제에 씁니다.")
''',
},
    checks='assert models[0][2] == "분류" and models[1][2] == "회귀"',
    pre_api=[
        {'name': '로지스틱 회귀', 'signature': '확률 → 범주',
         'note': '이름에 회귀가 들어 있지만 교실에서는 분류 모델로 다룹니다. 출력은 클래스 확률입니다.'},
    ],
    glossary=[
        {'term': 'stratify=y', 'meaning': '나눌 때 클래스 비율을 비슷하게 맞춥니다. 한쪽에 품종이 몰리면 평가가 흔들립니다.'},
    ])

ex('ml-report-card', '재현 가능한 보고서 카드', {
    'main.py': '''report = {
    "문제": "다음 날 총 대출 권수",
    "정답": "다음날_대출",
    "특성": ["요일", "어제_대출", "시험기간"],
    "분할": "시간 순서, 뒤 20%는 테스트",
    "난수": 42,
    "지표": "MAE (권)",
    "비교": "과거 평균 예측",
    "한계": "시험 기간 자료가 적으면 방학 예측이 어긋날 수 있음",
}
for key, value in report.items():
    print(f"{key}: {value}")
print("같은 난수·같은 분할이면 다른 사람도 같은 실험을 다시 할 수 있습니다.")
''',
},
    checks='assert report["지표"].startswith("MAE")\nassert report["난수"] == 42\nassert "다음날_대출" not in report["특성"]',
    pre_api=[
        {'name': '남길 항목', 'signature': '문제 · 특성 · 분할 · 난수 · 지표 · 한계',
         'note': '점수 숫자만 적지 않습니다. 같은 조건으로 다시 돌릴 수 있어야 보고서입니다.'},
    ],
    glossary=[
        {'term': '재현', 'meaning': '다른 사람이 같은 코드·같은 난수로 같은 표를 얻을 수 있는 상태입니다. 수행평가 저널의 뼈대입니다.'},
    ])


def apply():
    """Patch Unit III lesson lists/prose after later_units has defined the base lessons."""
    _lesson('ml-overview')['paragraphs'].append(
        '규칙을 코드에 쓰는 일과 사례를 모아 패턴을 쓰는 일을 나란히 보세요. '
        '포함 관계는 인공지능이 가장 넓고, 딥 블루는 탐색 프로그램이지 딥러닝이 아닙니다. '
        '아래는 규칙 vs 학습 → 포함 관계 → 역사 사례 순서입니다.'
    )
    _lesson('ml-use')['paragraphs'].append(
        '합·길이 검사처럼 규칙이 분명하면 일반 프로그램이 낫습니다. '
        '사서 역할에서는 예측 시점에 알 수 있는 열만 X로 모으고, 검사원 역할에서는 입력과 예측을 한 줄로 적습니다.'
    )
    _lesson('ml-process')['paragraphs'].append(
        '성공 기준을 “평균 예측보다 MAE가 낮은가”처럼 숫자로 먼저 적으세요. '
        '그다음 자료를 훈련·검증·테스트로 나누고, 전처리 값은 훈련 부분에서만 구합니다.'
    )
    _lesson('ml-terms')['paragraphs'].append(
        '표의 한 행이 한 관측입니다. X와 y의 개수와 순서를 맞춘 뒤, k처럼 미리 정하는 값과 데이터에서 정해지는 값을 구별하세요. '
        '미래 정답을 X에 넣으면 점수가 높아 보여도 현실에서는 쓸 수 없습니다.'
    )
    _lesson('ml-methods')['paragraphs'].append(
        '정답이 범주면 분류, 숫자면 회귀입니다. 정답이 없으면 가까운 값끼리 묶는 비지도이고, '
        '미로처럼 행동에 점수를 주면 강화 학습입니다. 제자리 반복이 이득이 되지 않게 보상을 설계하세요.'
    )
    _lesson('ml-libraries')['paragraphs'].append(
        '배열(NumPy) → 표(pandas) → 그래프(Matplotlib/Seaborn) → 학습(scikit-learn) 순으로 연결합니다. '
        '웹에서는 표와 그래프를 먼저 실행하고, 전체 모델은 PC에서 돌립니다.'
    )
    _lesson('ml-preprocess')['paragraphs'].append(
        '결측을 채우기 전에 그 값이 무엇을 뜻하는지 적습니다. 스케일과 범주 목록은 훈련에서만 배우고, '
        '테스트에는 transform만 적용합니다. 1000점이 오타인지 먼저 묻는 과제를 빼지 마세요.'
    )
    _lesson('ml-classification')['paragraphs'].append(
        '로지스틱 회귀는 이름과 달리 분류에 씁니다. 웹 원리에서는 가까운 이웃의 표를 직접 세고, '
        'PC 예제에서 같은 분할로 네 모델을 비교합니다. 테스트 점수로 k를 고르지 마세요.'
    )
    _lesson('ml-regression')['paragraphs'].append(
        '예측 숫자와 정답의 차이를 잔차라고 합니다. MAE는 원래 단위, MSE는 큰 오차에 더 민감하고, '
        'R²는 평균 예측보다 나은지를 보므로 음수가 될 수 있습니다.'
    )
    _lesson('ml-cluster')['paragraphs'].append(
        '정한 개수 K의 중심으로 가까운 점을 묶습니다. labels_의 번호는 정답 이름도 순위도 아닙니다. '
        'K와 스케일을 바꾸면 같은 자료도 다른 그림이 됩니다.'
    )
    _lesson('ml-metrics')['paragraphs'].append(
        '양성이 무엇인지 먼저 정하고 TP·FP·FN·TN을 셉니다. 스팸을 양성이라 두면, '
        '정상 메일을 스팸으로 보낸 것은 FP이므로 정밀도를 함께 봅니다. 불균형이면 정확도만으로 비교하지 않습니다.'
    )
    _lesson('ml-selection')['paragraphs'].append(
        '교차 검증은 훈련 자료를 여러 묶음으로 나눠 검증 역할을 바꿉니다. '
        'best_score_는 그 평균이고, 최종 테스트는 따로 보관한 데이터의 점수입니다. 둘이 다를 수 있습니다.'
    )
    _lesson('ml-project')['paragraphs'].append(
        '문제·특성·분할·난수·지표·한계를 한 카드에 적으세요. '
        '아래 보고서 카드 예제로 항목을 채운 뒤, 같은 파이프라인에서 k 후보를 하나 추가하고 선택 근거를 남깁니다.'
    )

    _set_examples('ml-overview', ['ml-rule-vs-learn', 'ml-nesting', 'ml-history-cases'])
    _set_examples('ml-use', ['ml-when-not', 'ml-loan-data', 'ml-inspect'])
    _set_examples('ml-process', ['ml-success-mae', 'ml-split-small'])
    _set_examples('ml-terms', ['ml-xy-table', 'ml-param-hyper', 'ml-leakage'])
    _set_examples('ml-methods', ['ml-classify-vs-regress', 'ml-unsupervised-groups', 'ml-rl-reward'])
    _set_examples('ml-libraries', ['ml-tools', 'ml-chart', 'ml-seaborn'])
    _set_examples('ml-preprocess', ['ml-scale-small', 'ml-clean', 'ml-scale'])
    _set_examples('ml-classification', ['ml-logistic-name', 'ml-knn-small', 'ml-classify'])
    _set_examples('ml-regression', ['ml-line-small', 'ml-regression', 'ml-housing'])
    _set_examples('ml-cluster', ['ml-kmeans-small', 'ml-cluster'])
    _set_examples('ml-metrics', ['ml-confusion-small', 'ml-metrics'])
    _set_examples('ml-selection', ['ml-cv-small', 'ml-selection', 'ml-learning-curve'])
    # 교차 검증·튜닝 예제는 'ml-selection' 소단원에서 실습한다(중복 배치 제거).
    _set_examples('ml-project', ['ml-report-card'])
