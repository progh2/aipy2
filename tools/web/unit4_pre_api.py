"""Unit IV pre_api/glossary fill for #61. Applied after unit4_density.

Adds or completes code-before cards for every Unit IV topic and example.
Does not seed history/youtube. Real science PNGs (not invented GUI shots)
are attached only where render_science.py already produced them.
"""
from content import examples, units
from slots import api_items, glossary_items, shot_items


def _ex(eid):
    return examples[eid]


def _lesson(lid):
    return next(lesson for lesson in units[4] if lesson['id'] == lid)


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
    """Fill Unit IV pre_api/glossary after the #61 density examples exist."""
    _fill_lessons()
    _fill_missing_example_api()
    _complete_example_glossary()
    _attach_science_shots()


def _fill_lessons():
    _fill_lesson('cv-overview', pre_api=[
        {'name': '두 작업', 'signature': '영상 처리 → 새 이미지  ·  비전 → 위치·의미',
         'note': '블러는 그림을 바꾸고, 검출은 이름과 상자를 줍니다. 아래는 처리 vs 비전을 같은 페이지에서 비교합니다.'},
    ], glossary=[
        {'term': '오판 비용', 'meaning': '빈자리를 틀리게 안내하거나 먼지를 결함으로 보면 사람이 피해를 봅니다. 이점과 함께 적습니다.'},
    ])
    _fill_lesson('cv-pixels', pre_api=[
        {'name': '격자', 'signature': '픽셀 (행, 열)  ·  채널 0~255',
         'note': '한 칸의 숫자 하나가 한 채널 값입니다. RGB는 세 채널, 그레이스케일은 밝기 하나입니다.'},
    ], glossary=[
        {'term': '해상도', 'meaning': '너비×높이입니다. 배열 size는 채널을 포함한 원소 수라서 픽셀 수와 다릅니다.'},
    ])
    _fill_lesson('cv-pipeline', pre_api=[
        {'name': '한 줄 과정', 'signature': '입력 → 전처리 → 특징 → 해석 → 출력·평가',
         'note': '번호판 위치와 글자 내용은 다른 단계입니다. 정확도·시간·지연·안정성을 같이 비교합니다.'},
    ], glossary=[
        {'term': '도구 선택', 'meaning': '패턴 매칭·특징점·머신러닝·딥러닝은 목적과 입력 조건에 따라 고릅니다. 한 방법이 항상 최선은 아닙니다.'},
    ])
    _fill_lesson('cv-libraries', pre_api=[
        {'name': '도구 역할', 'signature': 'OpenCV 입출력  ·  Pillow 편집  ·  그래프  ·  scikit-image 분석',
         'note': '설치 이름과 import 이름이 다릅니다. opencv-python → cv2, pillow → PIL.'},
    ], glossary=[
        {'term': '크기 표기', 'meaning': 'Pillow.size는 (너비, 높이), NumPy/OpenCV shape는 (높이, 너비, 채널)입니다.'},
    ])
    _fill_lesson('cv-io', pre_api=[
        {'name': '읽기 확인', 'signature': 'img = cv2.imread(path)  →  None이면 중단',
         'note': '실패하면 shape를 읽지 않습니다. 경로·권한·파일 형식을 먼저 봅니다.'},
    ], glossary=[
        {'term': '창 정리', 'meaning': 'imshow 뒤에는 waitKey로 키를 기다리고, destroyAllWindows로 창을 닫습니다.'},
    ])
    _fill_lesson('cv-filters', pre_api=[
        {'name': '부드럽게 / 경계 / 두 값', 'signature': '블러  ·  Canny  ·  threshold',
         'note': '커널이 크면 세부 정보도 사라질 수 있습니다. 이진화 기준과 값이 같으면 0입니다.'},
    ], glossary=[
        {'term': 'Otsu / 적응형', 'meaning': 'Otsu는 밝기 분포로 전역 기준을 고르고, 적응형은 주변 영역별 기준을 씁니다.'},
    ])
    _fill_lesson('cv-transform', pre_api=[
        {'name': '네 점 대응', 'signature': 'getPerspectiveTransform(src, dst)  →  warpPerspective',
         'note': '왼쪽 위→오른쪽 위→오른쪽 아래→왼쪽 아래 순서를 양쪽에서 같게 맞춥니다.'},
    ], glossary=[
        {'term': '잘림', 'meaning': '회전·변환의 출력 크기를 작게 잡으면 영역 밖이 잘립니다. 출력 (너비, 높이)를 확인합니다.'},
    ])
    _fill_lesson('cv-features', pre_api=[
        {'name': '중요한 부분', 'signature': 'Canny  ·  goodFeaturesToTrack  ·  findContours',
         'note': '선·점·닫힌 경계 중 목적이 있는 것을 고릅니다. 코너가 없으면 None일 수 있습니다.'},
    ], glossary=[
        {'term': '면적 걸러 내기', 'meaning': '윤곽선은 잡음 점에도 생깁니다. contourArea로 작은 영역을 제외합니다.'},
    ])
    _fill_lesson('cv-haar', pre_api=[
        {'name': '위치만', 'signature': 'detectMultiScale(gray, scaleFactor, minNeighbors)',
         'note': '얼굴 상자를 찾습니다. 이름·감정은 나오지 않습니다. scaleFactor는 크기 간격, minNeighbors는 후보 유지입니다.'},
    ], glossary=[
        {'term': '카메라 자원', 'meaning': 'VideoCapture → read 성공 확인 → 처리 → finally에서 release와 창 닫기입니다.'},
    ])
    _fill_lesson('cv-yolo', pre_api=[
        {'name': '한 장 검출', 'signature': 'boxes.cls  ·  conf  ·  xyxy',
         'note': '클래스 번호, 점수, 상자 좌표입니다. 프레임마다 Counter를 새로 만들어 현재 개수만 셉니다.'},
    ], glossary=[
        {'term': '합계 ≠ 방문자', 'meaning': '같은 사람이 여러 프레임에 다시 나옵니다. 누적 통행량에는 추적이 필요합니다.'},
    ])
    _fill_lesson('cv-project', pre_api=[
        {'name': '보고서 한 장', 'signature': '입력 · 처리 순서 · 비교 표 · 한계',
         'note': '같은 사진에서 순서를 바꿔 글자와 경계가 살아 있는지 봅니다. GUI는 함수 호출만 담당합니다.'},
    ], glossary=[
        {'term': '수행 저널', 'meaning': '이미지·오류 조건·처리 시간·한계를 코드와 함께 제출합니다. 한 순서가 항상 최선은 아닙니다.'},
    ])


def _fill_missing_example_api():
    _fill_api('cv-pixels', [
        {'name': '반전', 'signature': '255 - v',
         'note': '8비트 한 채널에서 밝기를 뒤집습니다. 255는 0이 됩니다.'},
        {'name': '이진화', 'signature': '255 if v > threshold else 0',
         'note': 'OpenCV THRESH_BINARY와 같습니다. 기준과 같으면 0입니다.'},
    ])
    _fill_api('cv-pillow', [
        {'name': 'Image.new', 'signature': 'Image.new("RGB", (너비, 높이), "white")',
         'note': '빈 그림을 만듭니다. size는 (너비, 높이)입니다.'},
        {'name': 'resize / rotate', 'signature': 'img.resize((120, 80))\nimg.rotate(30, expand=True)',
         'note': '크기를 바꾸거나 돌립니다. expand=True면 잘리지 않게 캔버스를 늘립니다.'},
    ])
    _fill_api('cv-skimage', [
        {'name': 'filters.sobel', 'signature': 'edges = filters.sobel(img)',
         'note': '밝기 변화의 경계를 강조합니다. 원본과 나란히 그려 비교합니다.'},
    ])
    _fill_api('cv-io', [
        {'name': 'imread / imwrite', 'signature': 'cv2.imread("scene.png")\ncv2.imwrite(경로, 이미지)',
         'note': '읽기 실패는 None입니다. 저장 전에 result 폴더를 만들고 성공 여부를 확인합니다.'},
        {'name': 'cvtColor / resize / 회전', 'signature': 'COLOR_BGR2GRAY  ·  resize((너비,높이))  ·  warpAffine',
         'note': 'resize 인자는 (너비, 높이)입니다. 회전 행렬은 중심과 각도로 만듭니다.'},
    ])
    _fill_api('cv-display', [
        {'name': '창 표시', 'signature': 'imshow → waitKey(0) → destroyAllWindows',
         'note': 'waitKey가 키 입력과 창 이벤트를 처리합니다. 화면이 있는 PC에서만 실행합니다.'},
    ])
    _fill_api('cv-filters', [
        {'name': '세 블러', 'signature': 'blur  ·  GaussianBlur  ·  medianBlur',
         'note': '평균·가중 평균·중앙값입니다. 커널이 홀수여야 하는 함수가 있습니다.'},
        {'name': 'Canny / 이진화', 'signature': 'Canny(gray, 50, 150)\nthreshold / adaptiveThreshold',
         'note': 'Canny는 하한·상한 두 기준입니다. Otsu는 0을 넣고 플래그로 자동 기준을 받습니다.'},
    ])
    _fill_api('cv-perspective', [
        {'name': '원근 행렬', 'signature': 'src, dst = float32 네 점\ngetPerspectiveTransform → warpPerspective',
         'note': '점 순서가 같아야 합니다. 출력 크기는 (너비, 높이)입니다.'},
    ])
    _fill_api('cv-click-card', [
        {'name': '마우스 콜백', 'signature': 'setMouseCallback(창, clicked)',
         'note': '왼쪽 클릭마다 점을 모읍니다. 네 점이 되면 변환하고, ESC는 취소입니다.'},
        {'name': '사각형 검사', 'signature': 'contourArea(src)',
         'note': '한 직선 위의 점은 면적이 거의 0입니다. 순서대로 네 꼭짓점을 고릅니다.'},
    ])
    _fill_api('cv-features', [
        {'name': 'Canny / 코너 / 윤곽', 'signature': 'Canny  ·  goodFeaturesToTrack  ·  findContours',
         'note': '코너는 None일 수 있습니다. 윤곽을 그리기 전에 이진화와 면적을 확인합니다.'},
    ])
    _fill_api('cv-haar', [
        {'name': 'CascadeClassifier', 'signature': 'cv2.data.haarcascades + "haarcascade_frontalface_default.xml"',
         'note': 'empty()이면 XML 경로를 확인합니다. 얼굴 영역(ROI) 안에서 눈·웃음 패턴을 찾습니다.'},
        {'name': 'detectMultiScale', 'signature': 'detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)',
         'note': '값에 따라 속도와 오탐·누락이 달라집니다. 같은 사진에서 표를 만들어 비교합니다.'},
    ])
    _fill_api('cv-camera', [
        {'name': 'VideoCapture', 'signature': 'cap = cv2.VideoCapture(0)\nok, frame = cap.read()',
         'note': '열기와 읽기 실패를 확인합니다. q로 종료하고 finally에서 release합니다. 이 예제는 영상을 저장하지 않습니다.'},
    ])
    _fill_api('cv-yolo', [
        {'name': 'YOLO', 'signature': 'YOLO("yolov8n.pt")\nresult = model(경로, device="cpu", conf=0.5)',
         'note': '교과서의 YOLOv8 경로입니다. 첫 실행에 가중치를 내려받습니다. 최신 버전이라고 단정하지 않습니다.'},
        {'name': 'boxes', 'signature': 'cls  ·  conf  ·  xyxy',
         'note': '클래스 번호, 점수, 상자입니다. names[cls]로 이름을 읽습니다.'},
    ])
    _fill_api('cv-yolo-count', [
        {'name': '프레임별 개수', 'signature': 'Counter(이름 for box in result.boxes)',
         'note': '매 프레임 새 Counter입니다. 여러 프레임을 더해도 고유 객체 수가 아닙니다.'},
    ])
    _fill_api('cv-count', [
        {'name': 'Counter', 'signature': 'Counter(["person", "car", "person"])',
         'note': '지금 목록의 이름별 개수입니다. 다음 프레임에 같은 이름이 다시 나올 수 있습니다.'},
    ])


def _complete_example_glossary():
    _fill_glossary('cv-pixels', [
        {'term': '기준과 같은 값', 'meaning': '128이 기준 128이면 검정입니다. 픽셀 실험실에서 확인해 보세요.'},
    ])
    _fill_glossary('cv-pillow', [
        {'term': '제공 도형', 'meaning': '외부 사진 없이 네모와 원을 그려 저장합니다. 웹에서도 실행할 수 있습니다.'},
    ])
    _fill_glossary('cv-skimage', [
        {'term': 'Agg', 'meaning': '화면 창 없이 그림을 파일로 저장하는 Matplotlib 백엔드입니다.'},
    ])
    _fill_glossary('cv-io', [
        {'term': 'scene.png', 'meaning': '예제가 도형 이미지를 직접 만듭니다. 교과서 원본 사진 파일이 없어도 됩니다.'},
    ])
    _fill_glossary('cv-filters', [
        {'term': 'CLAHE', 'meaning': '영역별로 대비를 조절합니다. 전역 equalizeHist와 결과가 다를 수 있습니다.'},
    ])
    _fill_glossary('cv-perspective', [
        {'term': 'float32', 'meaning': '변환 행렬을 구하는 점은 실수 배열이어야 합니다. 정수 목록을 그대로 넣지 않습니다.'},
    ])
    _fill_glossary('cv-features', [
        {'term': 'CHAIN_APPROX_SIMPLE', 'meaning': '윤곽의 꼭짓점만 남겨 점을 줄입니다. 모든 경계 픽셀이 필요하지 않을 때 씁니다.'},
    ])
    _fill_glossary('cv-haar', [
        {'term': 'photo.jpg', 'meaning': '사용 허락을 받은 사진을 예제 폴더에 직접 넣습니다. 신원 확인용이 아닙니다.'},
    ])
    _fill_glossary('cv-yolo', [
        {'term': 'conf', 'meaning': '이 점수 아래 후보는 버립니다. 높이면 검출 수가 줄 수 있고, 놓치는 물체도 늘 수 있습니다.'},
    ])
    _fill_glossary('cv-count', [
        {'term': '현재 프레임', 'meaning': '지금 목록만 셉니다. 통행 인원·방문자 수로 해석하지 않습니다.'},
    ])


def _attach_science_shots():
    _fill_shot(
        'cv-skimage',
        'assets/science/cv-sobel.png',
        '원본과 Sobel 에지 비교',
        '제공 예제를 실행해 저장한 비교 그림입니다. 오른쪽이 밝기 변화의 경계입니다.',
    )
    _fill_shot(
        'cv-io',
        'assets/science/cv-io.png',
        '원본·회색조·축소·회전 결과',
        '제공 예제가 만든 scene.png와 result 폴더의 실제 결과입니다. 가짜 콘솔 화면이 아닙니다.',
    )
    _fill_shot(
        'cv-filters',
        'assets/science/cv-filters.png',
        '블러·에지·세 이진화의 실제 결과',
        '같은 도형 이미지에 가우시안·Canny·고정·Otsu·적응형을 적용한 실행 결과입니다.',
    )
    _fill_shot(
        'cv-perspective',
        'assets/science/cv-perspective.png',
        '원본과 원근 변환 결과',
        '제공 예제의 네 점 대응으로 만든 변환 결과입니다. 점 순서가 바뀌면 그림이 뒤틀립니다.',
    )
    _fill_shot(
        'cv-features',
        'assets/science/cv-features.png',
        '에지·코너·윤곽선의 차이',
        '같은 도형에서 경계·꼭짓점·둘레를 그린 실행 결과입니다. 코너 개수는 고정 정답이 아닙니다.',
    )


def unit4_pre_coverage():
    """Examples that must show a code-before card."""
    ids = []
    for lesson in units[4]:
        for eid in lesson['examples']:
            if eid not in ids:
                ids.append(eid)
    return ids
