"""문항 id → 실제 소단원 id 매핑 (#116).

content.py/questions.py/later_units.py에서 생성한 문항의 topic은 원래
'기초 개념'·'결과 추적'·'응용 판단' 같은 분류형 라벨이거나(1·2단원),
소단원 한글 제목이었다(3·4단원). 소단원별 문제 페이지(q-{lesson id}.html)와
연결되려면 topic이 실제 lesson id와 같아야 한다.

이 파일은 문항 id 기준 override 표다. 문항 순서·개수·id는 절대 바꾸지 않고
(question_hints.json과 학생 답안 기록이 id로 연결되어 있음), 생성이 끝난 뒤
apply()로 topic만 lesson id로 바꾼다. 원래 라벨은 'tag' 필드로 보존한다.

3·4단원의 서술(전이) 문항은 애초에 l['id']를 topic으로 쓰도록 later_units.py를
고쳤으므로 이 표에는 없다(자동으로 정확하다).
"""

# unit 1 — '기초 개념'/'결과 추적'/'응용 판단'/'main'/'sys' 분류형 라벨을
# 문항 지문 내용에 맞춰 실제 소단원으로 재배정한다.
UNIT1 = {
    'u1-q003': 'overview',    # 모듈 정의
    'u1-q004': 'packages',    # 패키지 정의
    'u1-q005': 'imports',     # import 키워드
    'u1-q006': 'entrypoint',  # 직접 실행 시 __name__
    'u1-q007': 'entrypoint',  # if __name__ == "__main__":
    'u1-q008': 'imports',     # import ... as g
    'u1-q009': 'imports',     # from ... import hello
    'u1-q010': 'packages',    # __init__.py
    'u1-q011': 'packages',    # __all__
    'u1-q012': 'os-sys',      # os.getcwd()
    'u1-q013': 'os-sys',      # sys.argv
    'u1-q014': 'os-sys',      # sys.exit()
    'u1-q015': 'math',        # math.pi
    'u1-q016': 'random',      # random.choice
    'u1-q017': 'random',      # random.shuffle
    'u1-q018': 'datetime',    # date().weekday()
    'u1-q027': 'entrypoint',  # print(__name__) 직접 실행
    'u1-q028': 'math',        # math.ceil
    'u1-q029': 'math',        # math.floor
    'u1-q030': 'math',        # math.factorial
    'u1-q031': 'math',        # math.gcd
    'u1-q032': 'math',        # math.pow
    'u1-q033': 'random',      # random.shuffle 반환값
    'u1-q034': 'datetime',    # date().weekday() 예측
    'u1-q035': 'packages',    # from pkg import *와 __all__
    'u1-q036': 'random',      # randrange 후보
    'u1-q037': 'random',      # uniform 끝 값
    'u1-q038': 'thirdparty',  # Pillow
    'u1-q039': 'thirdparty',  # Beautiful Soup
    'u1-q040': 'thirdparty',  # 설치 후 import 실패
    # main 가드 관련: 종합 평가(addcal/subcal) 출력 추적은 review 소단원의
    # 목표("임포트 시 출력 추적")와 정확히 일치한다.
    'u1-q050': 'review',
    'u1-q052': 'entrypoint',  # __main__ 가드 일반 개념 서술
    'u1-q059': 'os-sys',      # sys.argv 코딩
}

# unit 2 — '기본 코드'/'오류 찾기'/'응용 판단' 분류형 라벨.
UNIT2 = {
    'u2-q025': 'widgets',  # tk.Tk() 기본 창
    'u2-q026': 'widgets',  # Canvas
    'u2-q027': 'layout',   # pack
    'u2-q028': 'layout',   # grid
    'u2-q029': 'layout',   # place
    'u2-q030': 'events',   # command=greet
    'u2-q031': 'events',   # clicked.connect(greet)
    'u2-q032': 'events',   # root.mainloop()
    'u2-q033': 'events',   # app.exec()
    'u2-q034': 'memo',     # Text 시작 위치 "1.0"
    'u2-q035': 'memo',     # Text 끝 위치 end-1c
    'u2-q036': 'memo',     # toPlainText()
    'u2-q037': 'events',   # command=hello() 즉시 호출 오류
    'u2-q038': 'events',   # connect(hello()) 오류
    'u2-q039': 'memo',     # editor.text() → toPlainText()
    'u2-q040': 'widgets',  # label.text= → setText()
    'u2-q041': 'memo',     # QFileDialog path, _
    'u2-q042': 'memo',     # Text.delete("1.0", tk.END)
    'u2-q043': 'widgets',  # entry.get()
    'u2-q044': 'widgets',  # entry.text()
    'u2-q049': 'layout',   # 한 부모에서 pack+grid 혼용
    'u2-q050': 'memo',     # 파일 대화 상자 취소
    'u2-q051': 'events',   # 콜백에서 time.sleep
    'u2-q052': 'pyside',   # Designer 생성 파일 재생성
    'u2-q053': 'ui',       # 웹 GUI 체험 화면의 의미
    'u2-q054': 'memo',     # setCentralWidget(editor)
}

# unit 3 — 자유 한글 라벨('AI 관계'·'학습 방식'·'pandas' 등)을 페이지 인용과
# 소단원 본문 내용을 함께 확인해 재배정한다. 128~131쪽은 여러 개념을 섞은
# 종합 평가/탐구 묶음 페이지라 내용으로 판단했다(unit1 36쪽·unit4 195쪽과 같은 패턴).
UNIT3 = {
    'u3-q001': 'ml-overview',       # AI ⊃ ML ⊃ DL 포함 관계
    'u3-q002': 'ml-methods',        # 비지도 학습 정의
    'u3-q003': 'ml-methods',        # 회귀 문제 유형
    'u3-q004': 'ml-methods',        # 강화 학습
    'u3-q005': 'ml-cluster',        # KMeans
    'u3-q006': 'ml-terms',          # 데이터 누수(미래 정답을 X에)
    'u3-q007': 'ml-preprocess',     # StandardScaler.fit은 훈련 데이터
    'u3-q008': 'ml-libraries',      # DataFrame에 문자열 열
    'u3-q009': 'ml-metrics',        # 정밀도 · 스팸 FP
    'u3-q010': 'ml-selection',      # 과대 적합
    'u3-q011': 'ml-methods',        # 분류 문제 판별
    'u3-q012': 'ml-classification', # 지도 학습 알고리즘 vs KMeans
    'u3-q013': 'ml-preprocess',     # 정규화 후 범위 밖 값
    'u3-q014': 'ml-terms',          # 하이퍼파라미터
    'u3-q015': 'ml-selection',      # 테스트로 반복 선택하면 안 됨
    'u3-q016': 'ml-regression',     # R² 음수 가능
    'u3-q017': 'ml-cluster',        # 군집 번호는 순위가 아님
    'u3-q018': 'ml-metrics',        # 정확도·정밀도·재현율은 분류
    'u3-q019': 'ml-libraries',      # import pandas as pd
    'u3-q020': 'ml-libraries',      # pd.DataFrame
    'u3-q021': 'ml-libraries',      # df.describe()
    'u3-q022': 'ml-classification', # model.fit
    'u3-q023': 'ml-classification', # model.predict
    'u3-q024': 'ml-metrics',        # 정밀도 계산
    'u3-q025': 'ml-regression',     # MSE 계산
    'u3-q026': 'ml-process',        # 데이터 누수 없는 파이프라인 순서
    'u3-q027': 'ml-selection',      # 교차 검증·튜닝·최종 평가 순서
    'u3-q028': 'ml-regression',     # mae() 구현
    'u3-q029': 'ml-metrics',        # precision() 구현
    'u3-q030': 'ml-preprocess',     # fill() 결측 평균 대체
    'u3-q031': 'ml-regression',     # predict(x,w,b) 오류 수정
}

# unit 4 — 마찬가지로 자유 한글 라벨. 195쪽은 여러 소단원을 아우르는 종합
# 평가 묶음 페이지라 내용으로 판단했다.
UNIT4 = {
    'u4-q001': 'cv-overview',   # 영상 처리 vs 컴퓨터 비전
    'u4-q002': 'cv-pixels',     # shape (2,3,3) 픽셀 수
    'u4-q003': 'cv-pixels',     # size 값
    'u4-q004': 'cv-io',         # imread 기본 컬러 순서 BGR
    'u4-q005': 'cv-io',         # imread 실패 시 None
    'u4-q006': 'cv-io',         # cv2.resize 크기 인자 순서
    'u4-q007': 'cv-filters',    # THRESH_BINARY 경계값
    'u4-q008': 'cv-filters',    # 적응형 이진화
    'u4-q009': 'cv-features',   # 코너 · 파노라마 대응
    'u4-q010': 'cv-features',   # 윤곽선 · 면적/외곽
    'u4-q011': 'cv-haar',       # Haar 검출과 신원 확인은 다름
    'u4-q012': 'cv-haar',       # ROI 눈 좌표 → 전역 좌표
    'u4-q013': 'cv-yolo',       # 프레임별 합계는 고유 방문자 수 아님
    'u4-q014': 'cv-pipeline',   # 처리 속도 외 평가 기준
    'u4-q015': 'cv-libraries',  # 실시간 입출력+검출 대표 도구 OpenCV
    'u4-q016': 'cv-libraries',  # 픽셀 단위 분석 도구 scikit-image
    'u4-q017': 'cv-haar',       # haarcascade_frontalface_default.xml
    'u4-q018': 'cv-haar',       # detectMultiScale
    'u4-q019': 'cv-io',         # cv2.imshow
    'u4-q020': 'cv-io',         # cv2.imread
    'u4-q021': 'cv-io',         # cv2.cvtColor
    'u4-q022': 'cv-pixels',     # 8비트 반전 값
    'u4-q023': 'cv-project',    # 문서 스캔 처리 경로(원근→블러→대비→이진화)
    'u4-q024': 'cv-haar',       # 카메라 프로그램 기본 순서(cv-camera 예제)
    'u4-q025': 'cv-filters',    # binary() THRESH_BINARY 구현
    'u4-q026': 'cv-libraries',  # bgr_to_rgb() 채널 순서
    'u4-q027': 'cv-haar',       # global_point() ROI→전역 좌표
    'u4-q028': 'cv-yolo',       # counts() 프레임별 클래스 개수
}

OVERRIDES = {**UNIT1, **UNIT2, **UNIT3, **UNIT4}


def apply(questions):
    """문항 생성이 모두 끝난 뒤 한 번 호출한다. topic을 lesson id로 바꾸고
    원래 라벨은 tag에 보존한다. override가 없는 문항은 tag=''."""
    for item in questions:
        new_topic = OVERRIDES.get(item['id'])
        if new_topic:
            item['tag'] = item['topic']
            item['topic'] = new_topic
        else:
            item.setdefault('tag', '')
