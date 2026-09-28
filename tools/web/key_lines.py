"""교과서 예제(ex-*.html) 핵심 줄 지정 (#135 항목2 "코드 읽기").

KEY_LINES[예제id] = [항목, ...]  항목은 int(엔트리 파일 기준 줄 번호) 또는
"파일명:줄번호"(다중 파일 예제). 그 예제에서 새로 배우는 API/개념이 쓰인 줄
(import, 객체 생성, 핵심 메서드 호출, 결과 출력 등)만 고른다. 빈 줄·주석·
반복되는 단순 print는 뺀다. build.py의 resolve_key_lines()가 이 목록을 실제
예제 files의 텍스트와 대조해 코드 문자열을 채우고, verify.py가 그 대조가
실제 코드 줄(빈 줄·주석 아님)인지 검사한다.

초안은 tools/web/*_pre_api.py 등의 패턴을 참고한 휴리스틱(가져오기·객체 생성·
핵심 메서드 호출·정의·출력 줄에 가중치)으로 전 예제(115개, 1·2·3·4단원)를
1차 생성한 뒤 표본을 검수했다. 예제를 새로 추가하면 이 표에도 항목을 추가한다.
"""

KEY_LINES = {
  'all': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'animal-check': ['main.py:1', 'mainanimal2.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1'],
  'christmas': [1, 2, 3, 5, 6],
  'circle-function': ['main.py:1', 'main.py:2', 'circle_area.py:1', 'circle_area.py:3', 'circle_area.py:4'],
  'circle-mixed': ['main.py:1', 'main.py:2', 'circle_area2.py:1', 'circle_area2.py:3', 'circle_area2.py:4'],
  'circle-top': ['main.py:1', 'circle.py:1', 'circle.py:2', 'circle.py:3', 'circle.py:4'],
  'class-module': ['main.py:1', 'shapes.py:1', 'shapes.py:3', 'shapes.py:4', 'shapes.py:7'],
  'copy-twice': ['main.py:1', 'main.py:2', 'main.py:3', 'homework1.py:1', 'homework2.py:1'],
  'core': ['main.py:1', 'main.py:2', 'core/logic.py:1', 'core/logic.py:10', 'core/logic.py:14'],
  'cv-bgr-rgb': [1, 3, 4, 7, 8],
  'cv-camera': ['main.py:1', 'main.py:2', 'main.py:5', 'main.py:10', 'main.py:13'],
  'cv-click-card': ['main.py:5', 'main.py:10', 'main.py:23', 'main.py:24', 'main.py:27'],
  'cv-count': [1, 2, 4],
  'cv-display': ['main.py:1', 'main.py:2', 'main.py:3', 'main.py:5', 'main.py:6'],
  'cv-eval-criteria': [1, 6, 8, 9],
  'cv-feature-kinds': [1, 6, 7, 8, 9],
  'cv-features': ['main.py:5', 'main.py:9', 'main.py:10', 'main.py:11', 'main.py:12'],
  'cv-filters': ['main.py:5', 'main.py:9', 'main.py:10', 'main.py:13', 'main.py:14'],
  'cv-haar': ['main.py:4', 'main.py:7', 'main.py:8', 'main.py:9', 'main.py:10'],
  'cv-haar-vs-id': [1, 2, 4, 5, 6],
  'cv-human-vs-computer': [1, 6, 7, 8, 9],
  'cv-io': ['main.py:5', 'main.py:9', 'main.py:13', 'main.py:14', 'main.py:16'],
  'cv-perspective': ['main.py:5', 'main.py:9', 'main.py:10', 'main.py:11', 'main.py:12'],
  'cv-pillow': ['main.py:1', 'main.py:2', 'main.py:3', 'main.py:4', 'main.py:7'],
  'cv-pipeline-steps': [1, 2, 10, 11],
  'cv-pixels': [1, 2, 3, 4, 5],
  'cv-plate-stages': [1, 2, 3, 4, 6],
  'cv-process-vs-vision': [1, 4, 8, 9, 10],
  'cv-scan-card': [1, 11, 12],
  'cv-shape-size': [1, 2, 3, 4, 5],
  'cv-skimage': ['main.py:1', 'main.py:6', 'main.py:8', 'main.py:10', 'main.py:12'],
  'cv-threshold-kinds': [1, 2, 3, 4, 7],
  'cv-use-fields': [1, 7, 8],
  'cv-yolo': ['main.py:1', 'main.py:3', 'main.py:6', 'main.py:7', 'main.py:10'],
  'cv-yolo-count': ['main.py:4', 'main.py:5', 'main.py:10', 'main.py:13', 'main.py:14'],
  'datetime': [1, 2, 3, 4, 9],
  'dice': [1, 2, 4, 6],
  'final-output': ['main.py:1', 'main.py:2', 'main.py:3', 'addcal.py:1', 'subcal.py:1'],
  'gift': [1, 2, 3],
  'hello-kivy': [16, 17, 18, 20, 21],
  'hello-pyqt': [5, 12, 13, 16, 18],
  'hello-pyside': [5, 12, 13, 16, 18],
  'hello-tk': [4, 5, 9, 11, 14],
  'hello-ttk': [5, 6, 10, 12, 15],
  'hello-wx': [2, 3, 4, 5, 7],
  'import-0': ['main.py:1', 'greet.py:1', 'greet.py:2', 'greet.py:4', 'greet.py:5'],
  'import-1': ['main.py:1', 'greet.py:1', 'greet.py:2', 'greet.py:4', 'greet.py:5'],
  'import-2': ['main.py:1', 'greet.py:1', 'greet.py:2', 'greet.py:4', 'greet.py:5'],
  'import-3': ['main.py:1', 'greet.py:1', 'greet.py:2', 'greet.py:4', 'greet.py:5'],
  'import-4': ['main.py:1', 'greet.py:1', 'greet.py:2', 'greet.py:4', 'greet.py:5'],
  'import-clash': ['main.py:1', 'main.py:2', 'greet.py:1', 'greet.py:2', 'farewell.py:1'],
  'layout-pyside': [3, 4, 7, 8, 12],
  'layout-tk': [2, 5, 6, 7, 8],
  'main-guard': ['main.py:1', 'main.py:2', 'main.py:3', 'circle_area3.py:4', 'circle_area3.py:5'],
  'math': [1, 2, 3, 4, 5],
  'math-circle': [1, 3, 6, 7, 8],
  'math-signed': [1, 2, 3, 4],
  'memo-plus-pyside': [11, 13, 20, 23, 51],
  'memo-plus-tk': [11, 12, 13, 14, 55],
  'memo-pyside': [11, 13, 15, 24, 33],
  'memo-tk': [5, 8, 13, 18, 21],
  'ml-clustering': ['main.py:1', 'main.py:2', 'main.py:3', 'main.py:14', 'main.py:25'],
  'ml-confusion-small': [1, 5, 6, 7, 8],
  'ml-cross-val-score': ['main.py:7', 'main.py:8', 'main.py:9', 'main.py:11', 'main.py:12'],
  'ml-cv-small': [1, 2, 4, 5, 7],
  'ml-grid-search-cv': ['main.py:1', 'main.py:2', 'main.py:6', 'main.py:9', 'main.py:12'],
  'ml-head-describe-info': ['main.py:1', 'main.py:2', 'main.py:6', 'main.py:7', 'main.py:8'],
  'ml-kmeans-small': [1, 2, 4, 6, 7],
  'ml-knn-exam': ['main.py:6', 'main.py:7', 'main.py:8', 'main.py:17', 'main.py:20'],
  'ml-knn-small': [1, 3, 4, 6, 7],
  'ml-learning-curve': ['main.py:9', 'main.py:11', 'main.py:16', 'main.py:17', 'main.py:18'],
  'ml-line-small': [1, 2, 3, 4, 7],
  'ml-linear-regression': ['main.py:6', 'main.py:7', 'main.py:8', 'main.py:17', 'main.py:22'],
  'ml-matplot-exam': ['main.py:1', 'main.py:3', 'main.py:4', 'main.py:5', 'main.py:7'],
  'ml-missing-values': ['main.py:8', 'main.py:12', 'main.py:17', 'main.py:22', 'main.py:28'],
  'ml-normalization': ['main.py:1', 'main.py:2', 'main.py:6', 'main.py:10', 'main.py:11'],
  'ml-numpy-exam': ['main.py:1', 'main.py:2', 'main.py:9', 'main.py:10', 'main.py:11'],
  'ml-one-hot-encoding': ['main.py:1', 'main.py:3', 'main.py:5', 'main.py:6', 'main.py:9'],
  'ml-pandas-exam': ['main.py:1', 'main.py:2', 'main.py:3', 'main.py:4', 'main.py:5'],
  'ml-performance-metrics': ['main.py:8', 'main.py:9', 'main.py:10', 'main.py:15', 'main.py:17'],
  'ml-read-data': ['main.py:1', 'main.py:5', 'main.py:6', 'main.py:9', 'main.py:13'],
  'ml-regression-metrics': ['main.py:9', 'main.py:10', 'main.py:11', 'main.py:14', 'main.py:17'],
  'ml-scale-small': [1, 4, 5, 7, 9],
  'ml-sklearn-exam': ['main.py:1', 'main.py:5', 'main.py:6', 'main.py:9', 'main.py:13'],
  'ml-split-small': [1, 2, 4, 5, 6],
  'ml-standardization': ['main.py:1', 'main.py:10', 'main.py:12', 'main.py:13', 'main.py:14'],
  'ml-train-test-split': ['main.py:1', 'main.py:2', 'main.py:3', 'main.py:6', 'main.py:7'],
  'ml-train-test-split2': ['main.py:6', 'main.py:7', 'main.py:8', 'main.py:16', 'main.py:17'],
  'os': [1, 2, 3, 6, 7],
  'os-pc': [1, 2, 3, 4],
  'package-0': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'package-1': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'package-2': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'package-3': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'package-4': ['main.py:1', 'nature/animals/bird.py:1', 'nature/animals/lion.py:1', 'nature/plants/tree.py:1', 'nature/plants/flower.py:1'],
  'project-pyside': ['main.py:11', 'main.py:12', 'main.py:16', 'main.py:18', 'main.py:21'],
  'project-roll': ['main.py:1', 'core/logic.py:1', 'core/logic.py:2', 'core/logic.py:10', 'core/logic.py:14'],
  'project-tk': ['main.py:15', 'main.py:18', 'main.py:20', 'main.py:21', 'main.py:22'],
  'pypi-names': [1, 7, 9, 10],
  'random': [1, 2, 7, 9, 11],
  'random-sample': [1, 2, 3, 4, 7],
  'random-seed': [1, 2, 3, 4, 8],
  'rectangle': ['main.py:1', 'rectEx1.py:1', 'rectEx1.py:2', 'rectEx1.py:4'],
  'reuse': ['main.py:1', 'main.py:2', 'main.py:3', 'calculator.py:1'],
  'review-two-files': ['main.py:1', 'greet.py:1', 'greet.py:2'],
  'stars': ['main.py:1', 'main.py:3', 'star.py:1', 'star.py:3', 'star.py:5'],
  'stdlib-json': [1, 2, 3, 4, 5],
  'sum-input': ['main.py:1', 'main.py:2', 'sumnummod.py:1', 'sumnummod.py:2', 'sumnummod.py:3'],
  'sys': [1, 2, 3, 4, 6],
  'sys-modules': [1, 2, 3, 4, 6],
  'thirdparty': ['main.py:1', 'main.py:2', 'main.py:3'],
  'two-adds': ['main.py:1', 'main.py:2', 'main.py:3', 'calculator.py:1', 'counter.py:1'],
  'weekday-fixed': [1, 2, 3, 4, 5],
  'widgets-pyside': [6, 7, 9, 12, 15],
  'widgets-tk': [2, 4, 5, 6, 7],
}


def resolve(example):
    """example: content.examples[id] 딕셔너리. KEY_LINES[예제id]를 실제 코드 줄로 바꾼다.
    반환: [{'ref': 'main.py_12' 또는 '12', 'file': 파일명 또는 '', 'line': 줄번호, 'code': 코드 텍스트}, ...]
    항목이 실제로 존재하지 않는 파일·빈 줄을 가리키면 건너뛰고 조용히 무시한다
    (verify.py가 전수 검사해 이 상황이 없는지 확인한다).
    """
    eid = example.get('id')
    items = KEY_LINES.get(eid) or []
    files = example.get('files') or {}
    entry = example.get('entry')
    out = []
    for item in items:
        if isinstance(item, str) and ':' in item:
            fname, _, lnstr = item.rpartition(':')
        else:
            fname, lnstr = entry, str(item)
        if fname not in files or not lnstr.isdigit():
            continue
        lines = files[fname].split('\n')
        ln = int(lnstr)
        if ln < 1 or ln > len(lines):
            continue
        code = lines[ln - 1]
        if not code.strip():
            continue
        ref = f'{fname}_{ln}' if fname != entry else str(ln)
        out.append({'ref': ref, 'file': fname if fname != entry else '', 'line': ln, 'code': code.strip()})
    return out


def all_ids():
    return list(KEY_LINES.keys())
