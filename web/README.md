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

학습 기록 키: `aipy-lab-v1`. 진행·코드·답안·저널은 브라우저 안에만 저장됩니다. 공용 PC에서는 내보내기 후 지우기를 사용하세요. 자동 서버 제출·PC 간 동기화는 없습니다. 저장소 접근 실패 시 메모리에서 동작하며 내보내기를 안내합니다.

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
