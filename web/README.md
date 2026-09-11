# 인공지능 파이썬 실무 실습실

1·2단원 교과서 전체 범위를 다루는 정적 학습 사이트입니다.

- 대문: `index.html`
- 기존 준비 안내: `before-you-start.html` (기존 localStorage 키 유지)
- 1단원: `units/unit01/index.html` — 12개 주제, 60문제
- 2단원: `units/unit02/index.html` — 9개 주제, 70문제
- 출처·범위·교과서 오류 보완: `sources.html`
- 49개 예제, 6종 GUI 실제 실행 스크린샷, tkinter/PySide6 대응 실습
- 파일 탭·편집·복사·추가·삭제·실행 인자·표준 입력·ZIP 다운로드
- 기록 자동 저장 및 JSON 내보내기/복원, 저널 Markdown 다운로드

## 수정과 재생성

설명·예제: `tools/web/content.py` / 문제: `tools/web/questions.py`
HTML 생성: `tools/web/build.py` / 공통 동작과 디자인: `web/assets/`

```bash
python3 tools/web/build.py
python3 tools/web/verify.py
python3 -m http.server 8000 --directory web
```

`http://localhost:8000`으로 접속하세요. 파일을 직접 여는 file:// 방식은 학습 JSON과 Worker 로딩을 지원하지 않습니다. 생성된 단원 HTML을 직접 수정하면 재생성 시 덮어씁니다. 준비 페이지는 생성 대상이 아니므로 직접 수정합니다.

## GitHub Pages

배포 저장소: https://github.com/progh2/aipy2
학생용 주소: https://progh2.github.io/aipy2/

`.github/workflows/pages.yml`이 main의 웹·생성기 변경을 감지하여 생성·검증 후 `web/`만 배포합니다. 저장소 Settings → Pages → Source는 GitHub Actions입니다.
원본 교과서·평가 문서 및 다른 수업 작업은 배포 저장소에 포함하지 않습니다.
현재 작업 폴더에서 배포 저장소로 동기화하려면 `python3 tools/web/deploy.py`를 사용합니다. 기존 변경을 강제로 덮어쓰지 않고 통상적인 git push를 수행합니다.

## 실행·채점·저장 범위

브라우저 실행은 Pyodide 0.27.7의 실제 CPython입니다. 실행 엔진은 최초 실행에 CDN에서 내려받습니다. Worker 실행은 15초 제한, 수동 중지, 출력 30KB 제한이 있습니다. 실행마다 학습 파일과 모듈을 정리합니다. 프로그램이 만든 가상 파일은 다음 실행 때 초기화되며 ZIP에는 편집기에 있는 소스만 담깁니다.

GUI와 OS 셸·pip 예제는 PC 실행용으로 표시합니다. 웹은 Python 문법 검사만 제공하며, HTML GUI 동작 체험은 별도로 표시한 학습용 시뮬레이션입니다. 데스크톱 창 실행 또는 완전한 GUI 자동 채점으로 오해하지 않도록 안내합니다.

구현형 문제는 함수 반환값·여러 입력·경계 조건으로 검사합니다. 빈칸은 공백·따옴표를 정규화하여 대표 답안과 비교하므로, 다른 올바른 표현은 해설과 대조하세요. 서술형은 자기 점검입니다. 공개 정적 사이트의 정답은 열람 가능하며 공식 시험 보안·성적 관리 도구가 아닙니다.

학습 기록 키: `aipy-lab-v1`. 화면은 항상 이 브라우저의 localStorage를 즉시 읽고 씁니다. 학교 계정으로 로그인하면 `assets/sync.js`가 `students/{uid}/state/current`와 `progress/{uid}`에 백그라운드로 맞춥니다. 로그인·네트워크·권한 실패 시에는 로컬만 사용하며 학습을 막지 않습니다. 공용 PC에서는 로그아웃할 때 이 브라우저 기록을 지울지 묻습니다. 저장소 접근 실패 시 메모리에서 동작하며 내보내기를 안내합니다.

## 학교 계정 로그인 (Firebase)

학생은 헤더의 **학교 계정으로 로그인**에서 `@e-mirim.hs.kr` Google 계정으로 로그인합니다.
반·번호는 교사가 미리 등록한 명단(`roster`)에서 가져오므로 학생이 스스로 바꿀 수 없습니다.

- 설정값: `web/assets/firebase-config.js` (`apiKey`는 비밀키가 아니라 식별자이므로 공개해도 됩니다)
- 로그인 동작: `web/assets/auth.js` · 표시: `web/assets/account.css`
- 권한 규칙: `firebase/firestore.rules` · 콘솔 설정 절차: `firebase/README.md`
- 설정값이 비어 있으면 로그인 UI가 나타나지 않고 사이트는 기존처럼 동작합니다.
- `before-you-start.html`은 독립 페이지라 계정 영역이 없습니다.
- 교사용 명단 관리: `teacher/admin.html` · 동작은 `assets/admin.js`. 교사 대문에서 링크됩니다.
  CSV 열은 `email,studentId,admissionYear,name,grade,classroom,number`이며 번호만 선택입니다.
- 교사 관리 뼈대: `teacher/admin.html` · `teacher/board.html` · `teacher/session.html`이
  `assets/teacher-shell.js`로 같은 헤더·반 선택을 씁니다. 반 ID는 `{학년}-{반}`(예: `2-3`)이며
  교사 이메일별 `localStorage`(`aipy-teacher-class:{email}`)에 남습니다. 명단 목록은 선택한 반만 보여 줍니다.
- 수업 따라가기(M5): `teacher/session.html`에서 세션 시작·종료·초점·시선 모으기.
  학생 화면은 `assets/follow.js`가 자기 반 `sessions/{학년}-{반}`만 구독합니다.
  교사가 단원 페이지에서 주제·예제를 누르면 `assets/teacher-focus.js`가 같은
  `sessions/{반}.focus`를 갱신합니다. 반은 `window.aipyClass`가 있으면 그걸 쓰고,
  없으면 관리 화면에서 고른 값(`localStorage` `aipy-teacher-class:{email}`)을 씁니다.
  교사 권한이 없거나 그 반 세션이 없으면 쓰지 않고 학습만 합니다.
  단원·주제 목록은 생성기가 만드는 `data/catalog.json`입니다. Firestore 규칙 배포는
  `firebase/README.md`를 보세요. 로그인·네트워크 실패 시 따라가기만 꺼지고 학습은 그대로입니다.
- 학습 기록 동기화(M2): `assets/sync.js` · 병합·요약 순수 함수는 `assets/sync-model.js`.
  생성기 훅은 `tools/web/build.py`의 `layout()`에 `sync.js` 한 줄을 넣는 것이 전부입니다.
  `app.js`는 `save(kind)`와 `window.aipyLearning.onLocalChange` / `getState` / `applyRemote`만 노출합니다.
  완료 체크·정답 확인은 즉시, 코드·저널은 약 25초 유휴와 `pagehide`에 올립니다.
- 이해도 신호와 도움 요청(M3): `assets/understanding.js` · `assets/help.js`.
  완료 체크(`.completion`) 옆에 이해했어요/조금 어려워요/어려워요를 붙이고,
  실습실·문제 영역에 도움 요청을 붙입니다. 값은 `progress/{uid}.understanding`과
  `feedback`·`helpRequests`에 쓰며, 교사 보드는 `assets/teacher-board.js`가
  `teacher/board.html`에서 선택된 반만 구독합니다. 평가에 반영되지 않습니다.

GitHub Pages는 서버 비밀을 둘 수 없으므로 학교 도메인 확인·반 정보 검증·교사 권한은 모두 Firestore 규칙이 판단합니다.
브라우저 자동채점 결과는 위조가 가능하므로, 제출물에는 결과와 함께 소스와 출력을 남겨 교사가 확인할 수 있게 설계합니다.

## 검증

`tools/web/verify.py`: 모든 예제 문법, 웹 예제 실행, 정답 검사 및 미완성 코드 실패, 문항 수, 내부 링크/앵커, ZIP 무결성.
실제 브라우저 검증: 다중 파일, __main__, 인자, 무한 반복 중지/재실행, 구현형 채점, 기록 복원, ZIP, GUI 문법 검사·시뮬레이션, 390px 모바일 넘침.
실제 GUI 검증: 6종 인사 앱의 인사·초기화, tkinter/PySide6 위젯·레이아웃·프로젝트, 기본·개선 메모장 한글 저장/열기/취소/미저장 확인. Linux 가상 디스플레이에서 검사했으며 Windows/macOS 외형은 다를 수 있습니다.

스크린샷: `assets/screenshots/`. 제공 예제의 실제 실행 화면을 `tools/web/capture_gui.py`로 촬영했습니다. 캡처 환경의 글꼴은 Noto Sans CJK KR입니다. Kivy는 기본 글꼴 지원을 위해 영어 문구를 사용했습니다.

## 대표 캐릭터 파이

개발자를 꿈꾸는 여학생 ‘파이’를 과목의 학습 친구로 사용합니다. 반가움·생각·발견·디버깅·성취의 5가지 표정을 각각 다른 학습 단계에 연결했습니다.

- 소개 및 원본 다운로드: `mascot.html`
- 원본 PNG / 웹 표시 WebP: `assets/mascot/pai-*-v1.*`
- 5종 원본 ZIP: `downloads/pai-character-pack.zip`
- 생성 도구와 전체 프롬프트: `assets/mascot/CREATION.md`
- 소단원별 개념 안내: `tools/web/mascot.py`
- 대문 표정 선택, 문제 피드백, 학습 완료, 실행 결과 안내: `assets/app.js`

이미지의 대사는 그림에 굽지 않고 HTML 텍스트로 제공합니다. 각 표정의 의미와 학습 안내를 글로 함께 읽을 수 있으며, 캐릭터가 코드·버튼을 덮는 떠다니는 UI는 사용하지 않습니다. 원본은 흰 배경 PNG이고, 웹용 WebP는 원본을 보존한 압축본입니다. built-in image_gen으로 제작했으며 CLI fallback은 사용하지 않았습니다.

## 학생·교사 분리와 3·4단원

- 학생 본문: 45개 주제의 구조도와 표, 접어서 읽는 설명, 코드 실습.
- 학생 시각 요약: `units/unit01/summary.html`부터 `unit04/summary.html`.
- 교사용: `teacher/index.html`, 단원별 요약·발문·시연·오개념·평가 연결.
- 교사 화면의 ‘수업 화면으로 보기’는 설명용 도식만 표시합니다. 방향키로 이동하고 ESC로 전체 보기에 돌아옵니다. 인쇄에서는 교사 메모를 제외합니다.
- 3단원: 데이터·전처리·분류·회귀·군집·교차 검증·튜닝·평가·학습 곡선.
- 4단원: 픽셀·라이브러리·입출력·필터·원근·특징·Haar·YOLOv8.
- 수학·픽셀 조작은 JavaScript 학습 모형으로 표시합니다. Python 실습은 Pyodide에서 실행하며 생성 PNG를 결과 아래에 표시합니다.
- PC 표시 예제는 문법 확인만 제공합니다. 카메라·개인 사진·YOLO 가중치는 PC에서 준비하며 자동으로 켜거나 업로드하지 않습니다.
- 도형 기반 OpenCV 및 과학 그래프는 `tools/web/render_science.py`로 실제 생성했습니다. 필요 패키지: numpy, pandas, scikit-learn, matplotlib, pillow, opencv-python, scikit-image, seaborn, openpyxl.
- 기본 검증: `python -m pip install numpy pandas scikit-learn matplotlib pillow` 후 `python tools/web/verify.py`.
- 3·4단원은 원문을 웹 학습용으로 재구성했습니다. 일부 예제는 내장·합성 자료를 사용하고, 원문의 외부 데이터·카메라 경로는 PC 예제로 구분했습니다.

브라우저 성능을 위해 scikit-learn·SciPy·OpenCV·Ultralytics 전체 코드는 PC 경로로 제공합니다. 웹에서 k-NN·최소제곱 직선·K-평균·전처리·혼동행렬·교차 검증 구조를 작은 자료로 직접 계산하는 별도 Python 예제를 제공합니다.

Windows에서 생성·검증을 실행할 때는 UTF-8 모드가 필요합니다: `set PYTHONUTF8=1` 후 실행하세요.
