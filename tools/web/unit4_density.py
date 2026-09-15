"""Unit IV extra examples for #61. Imported at the end of later_units.py.

Adds role-based labs so thin overview topics (overview, pixels, pipeline,
project) are independently complete. New APIs use pre_api/glossary.
Console examples stay screenshot-empty unless a real science render already exists.
"""
from content import ex, units


def _lesson(lesson_id):
    return next(lesson for lesson in units[4] if lesson['id'] == lesson_id)


def _set_examples(lesson_id, ids):
    _lesson(lesson_id)['examples'] = list(ids)


ex('cv-process-vs-vision', '사진을 다듬기 vs 의미를 판단하기', {
    'main.py': '''def blur_value(center, neighbors):
    return round((center + sum(neighbors)) / (1 + len(neighbors)))

detections = [
    {"이름": "네모", "상자": (30, 30, 90, 100)},
    {"이름": "원", "상자": (155, 55, 70, 70)},
]
print("영상 처리 · 가운데 밝기:", blur_value(200, [180, 190, 210]))
print("컴퓨터 비전 · 찾은 것:", [(row["이름"], row["상자"]) for row in detections])
print("다듬은 이미지는 새 그림이고, 검출 결과는 위치와 이름입니다.")
''',
},
    checks='assert blur_value(200, [180, 190, 210]) == 195\nassert detections[0]["이름"] == "네모"\nassert len(detections) == 2',
    pre_api=[
        {'name': '영상 처리', 'signature': 'blur_value(center, neighbors)',
         'note': '밝기·잡음·크기처럼 표현을 바꿉니다. 결과는 보통 새 이미지입니다.'},
        {'name': '컴퓨터 비전', 'signature': '{"이름": "네모", "상자": (x, y, w, h)}',
         'note': '물체·위치처럼 의미를 추론합니다. 전처리는 비전 시스템의 한 단계로 쓰일 수 있습니다.'},
    ],
    glossary=[
        {'term': '사람의 확인', 'meaning': '검출 결과를 사실로 단정하지 않습니다. 오판이 있으면 사람이 한 번 더 봅니다.'},
    ])

ex('cv-use-fields', '사서·교통·검사원 역할 · 이점과 오판', {
    'main.py': '''fields = [
    {"역할": "사서", "곳": "도서관", "이점": "빈자리 안내", "오판": "가방을 사람으로"},
    {"역할": "교통 보조", "곳": "교차로", "이점": "보행·차량 위치", "오판": "그늘을 차로"},
    {"역할": "검사원", "곳": "제조 라인", "이점": "흠집 후보", "오판": "먼지를 결함으로"},
]
for row in fields:
    print(f"{row['역할']}: {row['이점']}  →  오판 예: {row['오판']}")
print("촬영 자료의 이용 범위와 틀린 경우의 비용을 함께 적으세요.")
''',
},
    checks='assert fields[0]["오판"].startswith("가방")\nassert fields[2]["역할"] == "검사원"\nassert len(fields) == 3',
    pre_api=[
        {'name': '활용 카드', 'signature': '이점  ·  오판',
         'note': '어디에 쓰면 편한지만 쓰지 않습니다. 잘못 찾았을 때 누가 피해를 보는지도 한 줄로 적습니다.'},
    ],
    glossary=[
        {'term': '이용 허락', 'meaning': '실습은 제공 도형과 사용 허락을 받은 자료로 합니다. 개인 사진은 당사자 동의 없이 올리지 않습니다.'},
    ])

ex('cv-human-vs-computer', '사람은 맥락, 컴퓨터는 숫자', {
    'main.py': '''scene = {
    "픽셀": [[40, 40, 200], [40, 40, 200]],
    "사람": "오른쪽 밝은 덩어리를 컵으로 봄",
    "컴퓨터": "값 200이 모인 칸의 좌표만 계산",
}
print("격자:", scene["픽셀"])
print("사람:", scene["사람"])
print("컴퓨터:", scene["컴퓨터"])
print("조명·가림·각도가 바뀌면 같은 컵도 다른 숫자가 됩니다.")
''',
},
    checks='assert scene["픽셀"][0][2] == 200\nassert "컵" in scene["사람"]\nassert "좌표" in scene["컴퓨터"]',
    pre_api=[
        {'name': '맥락과 수치', 'signature': '사람: 장면 이해  ·  컴퓨터: 픽셀 연산',
         'note': '사람은 가려진 물건도 추측합니다. 프로그램은 지금 격자의 값만 봅니다. 조건이 바뀌면 결과가 달라집니다.'},
    ],
    glossary=[
        {'term': '조건 변화', 'meaning': '조명·가림·각도·데이터 분포가 바뀌면 같은 대상도 놓치거나 잘못 찾을 수 있습니다.'},
    ])

ex('cv-shape-size', 'shape의 픽셀 수와 size의 원소 수', {
    'main.py': '''shape = (2, 3, 3)
height, width, channels = shape
pixels = height * width
size = height * width * channels
print("shape:", shape, "→ 높이", height, "너비", width, "채널", channels)
print("픽셀 수:", pixels)
print("원소 수 size:", size)
print("Pillow.size는 (너비, 높이)이고, OpenCV shape는 (높이, 너비, 채널)입니다.")
''',
},
    checks='assert pixels == 6 and size == 18\nassert shape == (2, 3, 3)',
    pre_api=[
        {'name': 'shape', 'signature': '(높이, 너비, 채널)',
         'note': 'NumPy 이미지의 축 순서입니다. (2, 3, 3)은 행 2·열 3·채널 3입니다.'},
        {'name': '픽셀 수 / size', 'signature': '높이×너비  ·  높이×너비×채널',
         'note': '픽셀은 위치의 개수입니다. size는 채널 값을 모두 센 원소 수라서 컬러면 더 큽니다.'},
    ],
    glossary=[
        {'term': 'Pillow.size', 'meaning': '(너비, 높이)입니다. OpenCV의 shape와 앞뒤가 반대이므로 나란히 적습니다.'},
    ])

ex('cv-bgr-rgb', 'OpenCV BGR과 화면 RGB', {
    'main.py': '''bgr = (20, 80, 240)

def bgr_to_rgb(pixel):
    b, g, r = pixel
    return (r, g, b)

rgb = bgr_to_rgb(bgr)
print("OpenCV 기본 읽기 BGR:", bgr)
print("화면·Pillow RGB:", rgb)
print("가운데 G는 그대로입니다. 순서를 바꾸지 않으면 빨강과 파랑이 뒤바뀝니다.")
''',
},
    checks='assert bgr_to_rgb((20, 80, 240)) == (240, 80, 20)\nassert bgr_to_rgb((0, 0, 0)) == (0, 0, 0)',
    pre_api=[
        {'name': '채널 순서', 'signature': 'BGR (B, G, R)  →  RGB (R, G, B)',
         'note': 'OpenCV imread의 기본 컬러는 BGR입니다. Matplotlib·Pillow는 보통 RGB를 기대합니다.'},
    ],
    glossary=[
        {'term': 'cvtColor', 'meaning': '색 공간을 바꿉니다. BGR↔RGB, BGR→GRAY처럼 변환 코드를 명시합니다.'},
    ])

ex('cv-pipeline-steps', '입력부터 평가까지 한 줄로', {
    'main.py': '''steps = ["입력", "전처리", "특징·위치", "의미 해석", "출력·평가"]
example = {
    "입력": "교차로 카메라 한 장",
    "전처리": "크기 축소·회색조",
    "특징·위치": "차량 상자",
    "의미 해석": "차선 안 정차",
    "출력·평가": "표시 + 오탐·누락 수",
}
for name in steps:
    print(f"{name}: {example[name]}")
print("한 단계가 틀리면 다음 단계도 같이 흔들립니다.")
''',
},
    checks='assert steps[0] == "입력" and steps[-1] == "출력·평가"\nassert example["특징·위치"] == "차량 상자"',
    pre_api=[
        {'name': '처리 과정', 'signature': '입력 → 전처리 → 특징 → 해석 → 출력',
         'note': '패턴 매칭·특징점·학습 모델은 도구입니다. 목적과 입력 조건에 따라 고릅니다.'},
    ],
    glossary=[
        {'term': '전처리', 'meaning': '특징을 찾기 쉽게 이미지를 다듬는 단계입니다. 그 자체로 물체의 종류를 아는 것은 아닙니다.'},
    ])

ex('cv-plate-stages', '번호판 위치와 글자는 다른 단계', {
    'main.py': '''plate = {"상자": (40, 80, 120, 36), "글자": "12가3456"}
print("검출 단계 · 위치:", plate["상자"])
print("인식 단계 · 내용:", plate["글자"])
print("위치를 잘 찾아도 글자를 잘못 읽을 수 있습니다. 오류를 단계별로 셉니다.")
found_box = plate["상자"][2] > 0
read_text = len(plate["글자"]) >= 4
print("검출 성공?", found_box, "/ 인식 길이 OK?", read_text)
''',
},
    checks='assert plate["상자"] == (40, 80, 120, 36)\nassert plate["글자"] == "12가3456"',
    pre_api=[
        {'name': '검출', 'signature': '상자 (x, y, w, h)',
         'note': '어디 있는지만 찾습니다. 글자 내용과는 다른 문제입니다.'},
        {'name': '인식(OCR)', 'signature': '글자 문자열',
         'note': '상자 안을 읽어 번호를 만듭니다. 검출 오류와 인식 오류를 한 숫자로 합치지 마세요.'},
    ],
    glossary=[
        {'term': '단계별 평가', 'meaning': '검출 누락과 오인식은 원인이 다릅니다. 같은 사진에서 두 표를 따로 적습니다.'},
    ])

ex('cv-eval-criteria', '정확도만으로 고르지 않기', {
    'main.py': '''candidates = [
    {"이름": "느린 정확", "맞춤": 19, "장당_ms": 400, "조명변화": "약함"},
    {"이름": "빠른 대충", "맞춤": 12, "장당_ms": 20, "조명변화": "보통"},
    {"이름": "균형", "맞춤": 17, "장당_ms": 80, "조명변화": "보통"},
]
print("20장 시험")
for row in candidates:
    print(row["이름"], "맞춤", row["맞춤"], "/ 시간", row["장당_ms"], "ms / 조명", row["조명변화"])
print("실시간 안내면 지연도 보고, 교실 조명이 바뀌면 안정성도 봅니다.")
''',
},
    checks='assert candidates[0]["맞춤"] == 19\nassert candidates[1]["장당_ms"] == 20\nassert len(candidates) == 3',
    pre_api=[
        {'name': '비교 기준', 'signature': '정확성 · 처리 시간 · 실시간 지연 · 안정성',
         'note': '빠르게 틀리는 시스템은 교실·교차로에 맞지 않습니다. 무엇을 놓치고 잘못 찾는지 함께 적습니다.'},
    ],
    glossary=[
        {'term': '실시간성', 'meaning': '한 장을 처리하는 시간과, 입력부터 화면에 나오기까지의 지연은 다를 수 있습니다.'},
    ])

ex('cv-threshold-kinds', '고정·분포·주변으로 이진화하기', {
    'main.py': '''values = [40, 90, 127, 128, 200]
fixed_t = 127
fixed = [255 if v > fixed_t else 0 for v in values]
otsu_t = 100
otsu = [255 if v > otsu_t else 0 for v in values]
block = [40, 90, 200]
local_t = sum(block) / len(block) - 7
adaptive_center = 255 if block[1] > local_t else 0
print("고정 127:", fixed)
print("Otsu 예 100:", otsu, "(실제 Otsu는 분포로 기준을 고름)")
print("적응형 가운데:", adaptive_center, "지역 기준", round(local_t, 1))
print("THRESH_BINARY는 기준과 같으면 0입니다.")
''',
},
    checks='assert fixed == [0, 0, 0, 255, 255]\nassert otsu[1] == 0 and otsu[2] == 255\nassert adaptive_center in (0, 255)',
    pre_api=[
        {'name': 'THRESH_BINARY', 'signature': 'v > t  →  255   /   그 외 0',
         'note': '값이 기준보다 클 때만 흰색입니다. 127과 기준 127은 검정 0입니다.'},
        {'name': '세 가지 기준', 'signature': '고정  ·  Otsu(분포)  ·  적응형(주변)',
         'note': '그림자가 있으면 전역 한 줄보다 영역별 기준이 나을 수 있습니다. 실제 Otsu 값은 OpenCV가 계산합니다.'},
    ],
    glossary=[
        {'term': 'blockSize', 'meaning': '적응형에서 주변을 보는 홀수 칸입니다. C는 그 평균에서 빼는 값입니다.'},
    ])

ex('cv-feature-kinds', '선·점·닫힌 경계 고르기', {
    'main.py': '''jobs = [
    ("밝기가 급변하는 경계", "에지"),
    ("여러 방향으로 바뀌는 위치", "코너"),
    ("이진 영역의 둘레와 면적", "윤곽선"),
]
need = "도형 개수와 면적"
picked = next(name for goal, name in jobs if "면적" in goal)
print("목적:", need)
print("고른 도구:", picked)
for goal, name in jobs:
    print(f"{name}: {goal}")
print("에지를 찾았다고 물체의 종류나 신원을 안 것은 아닙니다.")
''',
},
    checks='assert picked == "윤곽선"\nassert jobs[1][1] == "코너"',
    pre_api=[
        {'name': '세 단서', 'signature': '에지 · 코너 · 윤곽선',
         'note': '파노라마 대응은 코너, 개수·면적은 윤곽선, 형태 스케치는 에지에 가깝습니다. 목적부터 고릅니다.'},
    ],
    glossary=[
        {'term': 'None', 'meaning': '코너가 없으면 goodFeaturesToTrack이 None을 줄 수 있습니다. 그리기 전에 확인합니다.'},
    ])

ex('cv-haar-vs-id', '얼굴 상자 ≠ 누구인지', {
    'main.py': '''faces = [(100, 50, 80, 90), (220, 40, 70, 80)]
print("찾은 얼굴 수:", len(faces))
for i, (x, y, w, h) in enumerate(faces):
    print(f"상자 {i}: 원점 ({x}, {y}) 크기 {w}×{h}")
print("위치만 있습니다. 이름·감정은 이 결과로 단정하지 않습니다.")
eye_in_roi = (12, 18)
origin = faces[0][:2]
eye_on_image = (origin[0] + eye_in_roi[0], origin[1] + eye_in_roi[1])
print("ROI 눈 좌표", eye_in_roi, "→ 원본", eye_on_image)
''',
},
    checks='assert len(faces) == 2\nassert eye_on_image == (112, 68)',
    pre_api=[
        {'name': '검출 상자', 'signature': '(x, y, w, h)',
         'note': '얼굴이 있을 법한 사각형입니다. 개인을 식별하거나 웃음을 감정으로 읽지 않습니다.'},
        {'name': 'ROI 좌표', 'signature': '원본 = 얼굴 원점 + ROI 좌표',
         'note': '눈·웃음은 얼굴 잘라 낸 그림에서 찾습니다. 전체 화면에 그리려면 얼굴의 (x, y)를 더합니다.'},
    ],
    glossary=[
        {'term': 'Haar Cascade', 'meaning': '밝기 패턴과 단계적 판별로 후보 영역을 찾습니다. 학습한 다중 클래스 검출기와는 역할이 다릅니다.'},
    ])

ex('cv-scan-card', '문서 스캔 보고서 카드', {
    'main.py': '''report = {
    "입력": "기울고 어두운 문서 한 장",
    "목표": "글자가 읽히는 이진 이미지",
    "처리": ["원근 보정", "가우시안 블러", "대비 조정", "이진화"],
    "비교": "순서 하나 빼고 같은 입력으로 다시 실행",
    "확인": "경계가 살아 있는지, 글자가 뭉개지지 않는지",
    "한계": "한 순서가 모든 사진에 최선은 아님",
    "확장": "정적 이미지로 검증한 뒤 카메라 입력",
}
for key, value in report.items():
    print(f"{key}: {value}")
print("GUI 버튼은 처리 함수만 호출하고, 배열 코드와 창 코드를 나눕니다.")
''',
},
    checks='assert report["처리"][0] == "원근 보정"\nassert "카메라" in report["확장"]\nassert report["한계"].startswith("한 순서")',
    pre_api=[
        {'name': '남길 항목', 'signature': '입력 · 처리 순서 · 비교 · 한계',
         'note': '결과 그림만 제출하지 않습니다. 같은 입력에서 순서를 바꿔 본 표가 보고서입니다.'},
    ],
    glossary=[
        {'term': '모듈 분리', 'meaning': '2단원 GUI의 버튼은 이미지 함수를 호출만 합니다. 경로 오류·취소도 창 쪽에서 처리합니다.'},
    ])


def apply():
    """Patch Unit IV lesson lists/prose after later_units has defined the base lessons."""
    _lesson('cv-overview')['paragraphs'].append(
        '사진을 부드럽게 만드는 일과 사진 속 물체의 위치·이름을 적는 일을 나란히 보세요. '
        '사서·교통·검사원 역할에서는 이점과 오판을 한 카드에 쓰고, 사람은 맥락을 보지만 프로그램은 숫자만 봅니다. '
        '아래는 처리 vs 비전 → 활용 카드 → 사람 vs 컴퓨터 순서입니다.'
    )
    _lesson('cv-pixels')['paragraphs'].append(
        'shape의 앞 두 칸을 곱하면 픽셀 수이고, 채널까지 곱하면 size입니다. '
        'OpenCV 기본 컬러는 BGR이라 화면 RGB와 빨강·파랑이 뒤바뀔 수 있습니다. 값 128과 기준 128은 검정입니다.'
    )
    _lesson('cv-pipeline')['paragraphs'].append(
        '입력부터 평가까지를 한 줄로 적은 뒤, 번호판처럼 위치 찾기와 글자 읽기를 다른 단계로 나누세요. '
        '맞춤 개수만 보지 말고 처리 시간과 조명 변화도 같은 표에 둡니다.'
    )
    _lesson('cv-libraries')['paragraphs'].append(
        'OpenCV는 입출력·검출, Pillow는 편집·형식, Matplotlib은 비교 그림, scikit-image는 분석 필터입니다. '
        '웹에서는 Pillow로 만들고 크기를 바꾸고, Sobel 비교는 PC에서 봅니다.'
    )
    _lesson('cv-io')['paragraphs'].append(
        'imread가 None이면 shape를 읽지 않습니다. resize의 (너비, 높이)는 shape 순서와 반대입니다. '
        '창은 imshow → waitKey → destroyAllWindows 순으로 정리하고, 저장 폴더는 먼저 만듭니다.'
    )
    _lesson('cv-filters')['paragraphs'].append(
        '커널이 커지면 잡음과 함께 세부 경계도 흐려질 수 있습니다. '
        '고정·Otsu·적응형 이진화를 같은 밝기 목록에서 비교한 뒤, PC 예제에서 실제 PNG를 여세요.'
    )
    _lesson('cv-transform')['paragraphs'].append(
        '원본 네 점과 목적지 네 점의 순서를 왼쪽 위부터 같게 맞춥니다. '
        '한쪽만 바꾸면 결과가 뒤틀립니다. ESC는 취소이고, 한 직선 위의 점은 사각형이 아닙니다.'
    )
    _lesson('cv-features')['paragraphs'].append(
        '목적이 경계인지, 대응점인지, 면적인지 먼저 고릅니다. '
        '네모 꼭짓점은 코너로 잡히기 쉽고, 원은 설정에 따라 코너가 적습니다. 개수는 고정 정답이 아닙니다.'
    )
    _lesson('cv-haar')['paragraphs'].append(
        '상자는 얼굴이 있을 법한 위치입니다. 누구인지는 알 수 없고, 웃음 패턴만으로 감정을 단정하지 않습니다. '
        '눈 좌표는 ROI 원점에 얼굴 (x, y)를 더해 원본으로 옮깁니다. finally에서 카메라와 창을 닫습니다.'
    )
    _lesson('cv-yolo')['paragraphs'].append(
        '한 프레임의 클래스별 개수를 먼저 세고, 합계를 방문자 수로 읽지 마세요. '
        'conf를 높이면 낮은 점수 후보가 빠져 검출 수가 줄 수 있습니다. 오탐 감소와 누락을 같이 적습니다.'
    )
    _lesson('cv-project')['paragraphs'].append(
        '입력·처리 순서·비교·한계를 한 카드에 적으세요. '
        '아래 스캔 카드로 항목을 채운 뒤, 같은 사진에서 원근 변환 순서를 바꾸고 글자가 살아 있는지 비교합니다.'
    )

    _set_examples('cv-overview', ['cv-process-vs-vision', 'cv-use-fields', 'cv-human-vs-computer'])
    _set_examples('cv-pixels', ['cv-pixels', 'cv-shape-size', 'cv-bgr-rgb'])
    _set_examples('cv-pipeline', ['cv-pipeline-steps', 'cv-plate-stages', 'cv-eval-criteria'])
    _set_examples('cv-libraries', ['cv-pillow', 'cv-skimage'])
    _set_examples('cv-io', ['cv-io', 'cv-display'])
    _set_examples('cv-filters', ['cv-threshold-kinds', 'cv-filters'])
    _set_examples('cv-transform', ['cv-perspective', 'cv-click-card'])
    _set_examples('cv-features', ['cv-feature-kinds', 'cv-features'])
    _set_examples('cv-haar', ['cv-haar-vs-id', 'cv-haar', 'cv-camera'])
    _set_examples('cv-yolo', ['cv-count', 'cv-yolo', 'cv-yolo-count'])
    _set_examples('cv-project', ['cv-scan-card', 'cv-perspective'])
