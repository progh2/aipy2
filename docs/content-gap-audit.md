# 콘텐츠 갭 감사 · 교과서 TOC ↔ `tools/web`

> **M0 / #50.** `web/` 생성물은 읽기만 했고 수정하지 않았다. 집계·경로는 빌드가 소비하는 `tools/web` 원본과, 그 결과물인 `web/data/unit{1–4}.json`을 대조했다.

## TLDR

- **교과서 소단원 20개**는 모두 웹 주제에 매핑되어 있다. “범위가 비어 있는 소단원”은 없다. 갭은 **커버 누락이 아니라 품질·밀도**다.
- **독립 완결 페이지는 0/45.** 네 단원 모두 `units/unit0N/index.html` 한 장에 `<section id="주제">` 앵커만 있다. (#51)
- **단원Ⅱ가 가장 얇다.** 웹 주제 9 · 고유 예제 17(할당 21, 그중 3개가 재사용). `ui`·`review` 예제 0. `events`/`pyside`는 hello·memo를 다시 가리킨다. 팀이 잠근 “GUI 예제 부족” 판단과 같다. **M1 = #51 → #54.**
- **선설명·역사/유튜브 팁 스키마가 없다.** lesson/ex 키는 `id, title, pages, lead, paragraphs, examples, tasks, extra` (+ III·IV `visual`)뿐. 슬롯 45×2 = **90칸 전부 빈칸** — 라온이 #57 합의 후 채운다.
- **실행 결과 스샷:** GUI 인사앱 6장(`hello-*`) + 과학 그래프 8장. widgets/layout/events/memo/project 전용 스샷 **없음**. (#54)
- **부록 wxPython·Kivy:** `hello-wx` / `hello-kivy` 갤러리 1쌍만. 위젯·배치·메모장 대응 없음. (#55·#56)
- 파이 학습 힌트(마스코트)는 I·II만 주제별 원고가 있고, III·IV는 기본 문장 fallback이다. 이건 **역사/유튜브 팁이 아니다.**

---

## 1. 조사 범위와 가정

| 사용한 원본 | 역할 |
| --- | --- |
| `tools/web/textbook.py` → `BOOK`, `MAP` | 교과서 4–5쪽 목차(쪽수·중단원·소단원 번호)의 **저장소 정본**. PDF는 저장소에 없음. |
| `tools/web/content.py` | 단원 I·II 레슨·예제 |
| `tools/web/later_units.py` | 단원 III·IV 레슨·예제(+ 웹 원리 `*-small`) |
| `tools/web/build.py` | 단원 1페이지 HTML, 갤러리, `web/data/unitN.json` 덤프 |
| `tools/web/mascot.py` → `TIPS` | 주제별 파이 힌트(역사/유튜브와 별개) |
| `tools/web/learning_design.py` | 개념 도식 + 과학 PNG 연결 |
| `tools/web/capture_gui.py` | `hello-{tk,ttk,pyside,pyqt,wx,kivy}` 6장만 캡처 |
| `web/data/unit{1–4}.json` | 파이프라인이 실제로 소비하는 레슨/예제 스냅샷(읽기 전용) |

**가정 (지어낸 TOC 행 없음)**

1. 소단원·쪽수는 `BOOK`에서만 가져왔다. `MAP`에 없는 웹 주제(`project`, `pyside`, `review`(II), `ml-project`, `cv-project`)는 **교과서 밖 확장**으로 따로 표기했다.
2. 확인학습·중단원 마무리·대단원 평가는 `BOOK`의 review/eval 문자열이고, 웹에서는 `review` / `ml-project` / `cv-project` 또는 확인학습 예제(`sum-input`, `animal-check` 등)로 흩어져 있다.
3. **상태(OK / thin / missing)** 는 아래 7기준 중 해당 행에 적용되는 항목을 종합한다. 커버만 있고 품질이 모자라면 `thin`.
4. **빈칸** = 데이터 필드가 없거나 값이 비어 라온이 나중에 채울 자리. `—` 는 해당 기준이 그 행에 적용되지 않음(예: 개념-only 소단원의 함수 선설명).

교과서 표기는 멘토르 「인공지능 파이썬 실무」(README·푸터). 이슈 문구의 「미림」은 학교(미림마이스터고) 맥락이다.

---

## 2. 품질 기준 (열·체크리스트)

| # | 기준 | 현재 판정 | 후속 |
| --- | --- | --- | --- |
| 1 | 소단원/학습 주제마다 **독립 완결 페이지** | **missing** — 단원당 HTML 1장, 공유 에디터 1개(`build.py`가 첫 예제 있는 주제에 `#lab`을 붙임) | #51 (II), 이후 #59–#61 |
| 2 | GUI 예제 수·설명 충분 | **thin** — II = 9주제 / 고유 17예제. widgets~memo가 단계 예제 부족 | #52 |
| 3 | 새 함수/속성 **등장 전 선설명** | **missing(스키마)** — 산문은 `paragraphs`에 섞임. `preexplain`/`api` 필드 없음 | #53, #57 |
| 4 | 실습 실행 결과 **스크린샷** | **thin** — 인사앱 6 + 과학 8. 예제별 파이프라인·페이지 노출 없음 | #54 |
| 5 | 역사 / 유튜브 **팁 슬롯** | **missing(스키마)** — 45주제 전부 빈칸. 파이 힌트는 별 트랙 | #57, #58 |
| 6 | 교과서 범위 전부 커버 | **OK(매핑)** — `textbook.toc`가 소단원마다 `related`를 assert. 밀도는 thin인 곳이 있음 | #59–#61 |
| 7 | 부록 wxPython · Kivy | **thin→missing** — 갤러리 hello만. 본편 대응 부록 페이지 없음 | #55, #56 |

---

## 3. 단원별 요약 카운트

집계일: 2026-09-15. 레슨 = `units[N]` 항목. 예제(고유) = 그 단원 JSON에 들어간 예제 id. 예제(할당) = 주제 `examples` 리스트 합(재사용 포함).

| 단원 | 웹 주제 | 예제 고유 | 예제 할당 | 문제 | 페이지 수 | GUI/과학 스샷 | 파이 힌트 원고 | 선설명 슬롯 | 역사 팁 | 유튜브 팁 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Ⅰ** 모듈과 패키지 | 12 | 33 | 33 | 60 | 1 (`unit01/index.html`) | 0 | 12/12 | **빈칸 12** | **빈칸 12** | **빈칸 12** |
| **Ⅱ** GUI | **9** | **17** | 21 | 70 | 1 (`unit02/index.html`) | GUI 6 (hello만) | 9/9 | **빈칸 9** | **빈칸 9** | **빈칸 9** |
| **Ⅲ** 머신러닝 | 13 | 19 | 20 | 44 | 1 (`unit03/index.html`) | 과학 3 | 0/13 (fallback) | **빈칸 13** | **빈칸 13** | **빈칸 13** |
| **Ⅳ** 컴퓨터 비전 | 11 | 14 | 16 | 39 | 1 (`unit04/index.html`) | 과학 5 | 0/11 (fallback) | **빈칸 11** | **빈칸 11** | **빈칸 11** |
| **부록** wx · Kivy | 0 | 2 (`hello-wx`, `hello-kivy`) | 2 (Ⅱ `libraries`에 포함) | 0 | 0 | 2 (갤러리) | — | **빈칸** | **빈칸** | **빈칸** |
| **합** | **45** | **82** (README와 동일. `core`가 I·II에 중복) | — | 213 | 4 | 14 | 21 원고 + 24 fallback | **빈칸 45** | **빈칸 45** | **빈칸 45** |

재사용(같은 예제 id가 두 주제에 할당):

- Ⅱ: `hello-tk`, `hello-pyside` (`libraries` + `events` + `pyside`), `memo-pyside` (`memo` + `pyside`)
- Ⅲ: `ml-selection` (`ml-selection` + `ml-project`)
- Ⅳ: `cv-perspective`, `cv-features` (`본 주제` + `cv-project`)

스샷 파일 (저장소에 존재, 예제 필드가 아님):

- `web/assets/screenshots/{tk,ttk,pyside,pyqt,wx,kivy}.png` — `build.py` 갤러리, `verify.py`가 6장만 검사
- `web/assets/science/{ml-chart,ml-cluster,ml-learning-curve,cv-sobel,cv-io,cv-filters,cv-perspective,cv-features}.png` — `learning_design.visual()`이 8개 주제에만 붙임

---

## 4. 단원Ⅱ 갭 (M1 우선 · #51→#54)

단원Ⅱ 교과서 분량은 40–59쪽으로 **가장 짧지만**, 웹은 이미 tk↔PySide 확장·갤러리·시뮬레이터를 얹어 **한 페이지에 몰려 있다.** 독립 페이지로 쪼개면 주제당 예제·선설명·스샷이 더 드러난다.

| 웹 주제 | 경로 | 예제 | 독립 페이지 | 선설명 | 스샷 | 역사/유튜브 | 상태 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ui` | `content.py` → `units/unit02/index.html#ui` | **0** | missing | — (개념) | 0 | 빈칸 / 빈칸 | **thin** | CLI/GUI/NUI 산문만. 확인학습 연결은 문제 쪽. |
| `libraries` | `#libraries` | 6: `hello-{tk,ttk,pyside,pyqt,wx,kivy}` | missing | 빈칸 (툴킷 소개 산문 있음) | **6** 갤러리 | 빈칸 / 빈칸 | thin | 비교 갤러리는 강점. wx·Kivy는 여기서 끝. |
| `widgets` | `#widgets` | 2: `widgets-tk`, `widgets-pyside` | missing | 빈칸 (위젯 목록 산문) | **0** | 빈칸 / 빈칸 | **thin** | #52 핵심. 위젯별 단계 예제·스샷 없음. |
| `layout` | `#layout` | 2: `layout-tk`, `layout-pyside` | missing | 빈칸 (`pack`/`grid`/`place` 산문) | **0** | 빈칸 / 빈칸 | **thin** | 웹 시뮬레이터는 단원 하단 공유. |
| `events` | `#events` | 2: **재사용** `hello-tk`, `hello-pyside` | missing | 빈칸 (`command=` vs `()` 산문) | 0 (hello 갤러리와 중복) | 빈칸 / 빈칸 | **thin** | 전용 bind/after/시그널 예제 없음. |
| `memo` | `#memo` | 4: `memo-tk`, `memo-pyside`, `memo-plus-*` | missing | 빈칸 (①–⑧ 단계 산문이 가장 가까움) | **0** | 빈칸 / 빈칸 | thin | 교과서 본편. 단계별 중간 스샷 없음. |
| `pyside` | `#pyside` · `extra=True` | 2: 재사용 hello/memo | missing | 빈칸 (설치·Designer 산문) | 0 | 빈칸 / 빈칸 | thin | 교과서 밖 확장. Designer `.ui` 예제 파일 없음. |
| `project` | `#project` · `extra=True` | 3: `core`, `project-tk`, `project-pyside` | missing | 빈칸 | **0** | 빈칸 / 빈칸 | thin | 수행평가 연결. 실행 화면 스샷 없음. |
| `review` | `#review` | **0** | missing | — | 0 | 빈칸 / 빈칸 | **thin** | 56–59쪽 마무리. 예제 없이 문제만. |

**M1에서 손댈 우선순위 (짧음)**

1. **#51 독립 완결 페이지** — `ui` / `libraries` / `widgets` / `layout` / `events` / `memo` / `pyside` / `project` / `review`를 단독으로 읽고 실습 가능하게. 생성기는 `tools/web` 유지.
2. **#52 예제·설명 확충** — `widgets`·`layout`·`events`·`memo`에 **전용** 단계 예제. `ui`에 인터페이스 분류 미니 실습 또는 명시적 개념 완결. `events`의 hello 재사용 해소.
3. **#53 선설명 블록** — 최소 `Button`/`pack`/`grid`/`command`/`bind`/`Text`/`filedialog`/`clicked.connect`가 **코드보다 위**에 짧은 칸으로.
4. **#54 예제별 실행 스샷** — `capture_gui.py` 확장. 갤러리 6장 외에 widgets/layout/memo/project를 페이지에 노출.

스키마 표준화(#57)와 역사/유튜브 시드(#58), 부록(#55·#56)은 M1 본편 다음.

---

## 5. 대응표 · 단원Ⅰ

| 교과서 TOC | 쪽 | 웹 주제 / 예제 경로 | 상태 | 독립 완결 페이지 | 예제 수 | 선설명 | 스샷 | 역사/유튜브 팁 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ⅰ. 모듈과 패키지 활용 | 6–39 | `units/unit01/index.html` | thin | missing | 33 | 스키마 빈칸 | 0 | 빈칸 / 빈칸 | 단원 1장. |
| 01. 모듈, 패키지의 개요 | 8–13 | `#overview` | thin | missing | 1 (`reuse`) | 빈칸 | 0 | 빈칸 / 빈칸 | 소단원 2개를 한 주제로 압축. |
| 01-01 모듈의 개념 및 필요성 | 9–10 | `content.py` `overview` / `reuse` | thin | missing | (위와 공유) | 빈칸 | 0 | 빈칸 / 빈칸 | |
| 01-02 패키지의 개념 및 필요성 | 11–12 | 같은 `overview` | thin | missing | 패키지 전용 예제 없음 | 빈칸 | 0 | 빈칸 / 빈칸 | 패키지 실습은 `#packages`로 미룸. |
| 01 마무리·확인학습 | 13 | `#review` + `sum-input` (`#define`) | thin | missing | 확인학습 예제는 define에 있음 | 빈칸 | 0 | 빈칸 / 빈칸 | |
| 02. 모듈, 패키지 활용 | 14–35 | 아래 5주제 | OK(커버) | missing | 다수 | 빈칸 | 0 | 빈칸 / 빈칸 | 밀도는 I 중 가장 나음. |
| 02-01 모듈 정의하기 | 15–18 | `#define` (15–16), `#entrypoint` (17–18) | OK | missing | 5+2 | 산문 있음 / 슬롯 빈칸 | 0 | 빈칸 / 빈칸 | `__name__` 분리 잘됨. |
| 02-02 모듈과 패키지 사용하기 | 19–25 | `#imports`, `#packages` | OK | missing | 5+8 | 산문 있음 / 슬롯 빈칸 | 0 | 빈칸 / 빈칸 | 25쪽 탐구 `stars`, `__all__` 보완 주석. |
| 02-03 여러 가지 모듈 활용하기 | 26–33 | `#os-sys` `#math` `#random` `#datetime` `#thirdparty` | OK | missing | 3+1+3+2+1 | 산문 있음 / 슬롯 빈칸 | 0 | 빈칸 / 빈칸 | 표준 모듈을 웹 5주제로 쪼갬. `thirdparty`는 PC 1예. |
| 02 마무리·확인학습 | 34–35 | `#review`, `animal-check` | thin | missing | 확인학습은 packages | 빈칸 | 0 | 빈칸 / 빈칸 | |
| 대단원 종합 평가 | 36–39 | `#review` / `final-output` | thin | missing | 1 | 빈칸 | 0 | 빈칸 / 빈칸 | 정답편 201쪽 불일치 주석. |
| *(확장)* 1단원 프로젝트 | 교과서 밖 | `#project` `extra` / `core` | thin | missing | 1 | 빈칸 | 0 | 빈칸 / 빈칸 | 수행평가 연결. |

---

## 6. 대응표 · 단원Ⅱ (본표)

| 교과서 TOC | 쪽 | 웹 주제 / 예제 경로 | 상태 | 독립 완결 페이지 | 예제 수 | 선설명 | 스샷 | 역사/유튜브 팁 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ⅱ. GUI 프로그래밍 | 40–59 | `units/unit02/index.html` | **thin** | missing | 17 고유 | 전부 빈칸 | hello 6만 | 빈칸 / 빈칸 | 갤러리+시뮬레이터+9주제가 한 장. |
| 01. GUI 프로그래밍 개요 | 42–48 | `#ui` + `#libraries` | thin | missing | 0+6 | 빈칸 | 6 | 빈칸 / 빈칸 | |
| 01-01 사용자 인터페이스 | 43–44 | `content.py` `ui` | **thin** | missing | **0** | — | 0 | 빈칸 / 빈칸 | #52. |
| 01-02 파이썬 GUI | 45–46 | `libraries` + hello 6 | thin | missing | 6 | 빈칸 | 6 | 빈칸 / 빈칸 | 교과서 tk/PyQt/wx/Kivy + 웹이 ttk·PySide 보강. |
| 01 마무리·확인학습 | 47–48 | `#libraries` 과제 + 문제 | thin | missing | 0 전용 | 빈칸 | — | 빈칸 / 빈칸 | |
| 02. GUI 프로그래밍 작성 | 49–57 | `#widgets` `#layout` `#events` `#memo` | **thin** | missing | 2+2+2재사용+4 | 빈칸 | **0** | 빈칸 / 빈칸 | M1 본편. |
| 02-01 tkinter의 구성 요소 | 50–51 | widgets + layout + events | **thin** | missing | 실고유 4 (events는 hello 재사용) | 빈칸 | 0 | 빈칸 / 빈칸 | 한 소단원 → 웹 3주제. 페이지는 여전히 한 장. |
| 02-02 GUI 앱 개발 | 52–55 | events + memo | thin | missing | memo 4 + events 재사용 | 빈칸 (memo ①–⑧) | 0 | 빈칸 / 빈칸 | 교과서 본편 메모장. |
| 02 마무리·확인학습 | 56–57 | `#review` | **thin** | missing | **0** | — | 0 | 빈칸 / 빈칸 | IDLE 위젯 문제는 문항만. |
| 대단원 종합 평가 | 58–59 | `#review` + 문항 | thin | missing | 0 | — | 0 | 빈칸 / 빈칸 | 58쪽 4번 표현 보완은 문제에 반영. |
| *(확장)* PySide6·Designer | 교과서 밖 | `#pyside` | thin | missing | 2 재사용 | 빈칸 | 0 | 빈칸 / 빈칸 | |
| *(확장)* 통합 프로젝트 | 교과서 밖 | `#project` | thin | missing | 3 | 빈칸 | 0 | 빈칸 / 빈칸 | |

---

## 7. 대응표 · 단원Ⅲ

| 교과서 TOC | 쪽 | 웹 주제 / 예제 경로 | 상태 | 독립 완결 페이지 | 예제 수 | 선설명 | 스샷 | 역사/유튜브 팁 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ⅲ. 파이썬과 머신러닝 | 60–131 | `units/unit03/index.html` | thin | missing | 19 | 빈칸 13 | 과학 3 | 빈칸 / 빈칸 | 파이 힌트 fallback 13. |
| 01-01 머신러닝이란? | 63–67 | `later_units.py` `ml-overview` | thin | missing | **0** | 빈칸 (역사 연도는 산문) | 0 | **빈칸** (다트머스·딥블루·ImageNet이 산문에만) | #58 후보. |
| 01-02 필요성과 활용 | 68–70 | `ml-use` | thin | missing | **0** | — | 0 | 빈칸 / 빈칸 | |
| 01-03 문제 해결 과정 | 71–75 | `ml-process` | thin | missing | 1 (`ml-split-small`) | 빈칸 | 0 | 빈칸 / 빈칸 | 90–102 전처리와 MAP이 겹침. |
| 01-04 주요 용어 | 76–78 | `ml-terms` | thin | missing | **0** | 빈칸 | 0 | 빈칸 / 빈칸 | |
| 01-05 학습 방법의 종류 | 79–82 | `ml-methods` | thin | missing | **0** | 빈칸 | 0 | 빈칸 / 빈칸 | 확인학습 83–84도 이 주제 pages에 포함. |
| 01 마무리·확인학습 | 83–84 | `ml-methods` + 문항 | thin | missing | 0 | — | 0 | 빈칸 / 빈칸 | 84쪽 1③ 정답편 불일치 주석. |
| 02-01 라이브러리 소개 | 86–89 | `ml-libraries` | thin | missing | 3 (`ml-tools`, `ml-chart`, `ml-seaborn`) | 빈칸 | **ml-chart.png** | 빈칸 / 빈칸 | seaborn은 PC. |
| 02-02 데이터 준비와 전처리 | 90–102 | `ml-process` + `ml-preprocess` | thin | missing | 1+3 | 빈칸 | 0 | 빈칸 / 빈칸 | `ml-scale` 등은 PC(sklearn). |
| 02-03 주요 알고리즘 활용 | 103–111 | `ml-classification` `ml-regression` `ml-cluster` | thin | missing | 2+3+2 | 빈칸 | **ml-cluster.png** | 빈칸 / 빈칸 | 분류·회귀·군집을 웹 3주제로 분리. |
| 02-04 모델 평가와 선택 | 112–126 | `ml-regression`(지표) `ml-metrics` `ml-selection` | thin | missing | (회귀 공유)+2+3 | 빈칸 | **ml-learning-curve.png** | 빈칸 / 빈칸 | |
| 02 마무리·확인학습 | 127–128 | 문항 + `ml-selection` | thin | missing | — | 빈칸 | — | 빈칸 / 빈칸 | 128쪽 분할 순서 보완 주석. |
| 대단원 종합 평가 | 129–131 | `ml-project` | thin | missing | 1 (재사용 `ml-selection`) | 빈칸 | 0 | 빈칸 / 빈칸 | 확장. |

개요 5소단원 중 3개(`overview`/`use`/`terms`/`methods`)가 **코드 예제 0** — #60에서 미니 실습 또는 명시적 개념 완결이 필요.

---

## 8. 대응표 · 단원Ⅳ

| 교과서 TOC | 쪽 | 웹 주제 / 예제 경로 | 상태 | 독립 완결 페이지 | 예제 수 | 선설명 | 스샷 | 역사/유튜브 팁 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ⅳ. 파이썬과 컴퓨터 비전 | 132–195 | `units/unit04/index.html` | thin | missing | 14 | 빈칸 11 | 과학 5 | 빈칸 / 빈칸 | 파이 fallback 11. |
| 01-01 컴퓨터 비전이란? | 135–136 | `cv-overview` | thin | missing | **0** | — | 0 | 빈칸 / 빈칸 | 01-02와 한 주제. |
| 01-02 활용 분야 | 137–139 | 같은 `cv-overview` | thin | missing | 0 | — | 0 | 빈칸 / 빈칸 | |
| 01-03 기본 개념 | 140–144 | `cv-pixels` + `cv-pipeline` | thin | missing | 1+0 | 빈칸 | 0 (픽셀 실험실은 JS) | 빈칸 / 빈칸 | pipeline 예제 0. |
| 01 마무리·확인학습 | 145–146 | 문항 | thin | missing | 0 | — | 0 | 빈칸 / 빈칸 | |
| 02-01 라이브러리 소개 | 148–154 | `cv-libraries` | thin | missing | 2 | 빈칸 | **cv-sobel.png** | 빈칸 / 빈칸 | |
| 02-02 이미지 데이터 다루기 | 155–162 | `cv-io` | thin | missing | 2 | 빈칸 | **cv-io.png** | 빈칸 / 빈칸 | `cv-display`는 PC 창. |
| 02-03 전처리와 변환 | 163–172 | `cv-filters` + `cv-transform` | thin | missing | 1+2 | 빈칸 | **cv-filters.png**, **cv-perspective.png** | 빈칸 / 빈칸 | |
| 02-04 중요한 부분 찾기 | 173–176 | `cv-features` | thin | missing | 1 | 빈칸 | **cv-features.png** | 빈칸 / 빈칸 | |
| 02-05 프로젝트 실습 | 177–191 | `cv-haar` + `cv-yolo` | thin | missing | 2+3 | 빈칸 | **0** (카메라·가중치 PC) | 빈칸 / 빈칸 | photo.jpg·yolov8n 학생 준비. |
| 02 마무리 / 종합 | 192–195 | `cv-project` | thin | missing | 2 재사용 | 빈칸 | 0 | 빈칸 / 빈칸 | |

Haar/YOLO는 실행 결과 스샷이 페이지에 없다(과학 PNG 맵에도 없음).

---

## 9. 부록 · wxPython · Kivy

교과서 `BOOK`에는 부록 단원이 없다. 품질 기준 7과 #55·#56이 **별도 산출물**로 요구한다.

| 항목 | 교과서 위치 | 현재 경로 | 상태 | 독립 페이지 | 예제 수 | 선설명 | 스샷 | 역사/유튜브 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wxPython | Ⅱ 01-02 파이썬 GUI (45–46)에 이름만 | `hello-wx` · `screenshots/wx.png` · 문항 1 | **missing**(부록) | missing | 1 | 빈칸 | 1 (인사만) | 빈칸 / 빈칸 | widgets/layout/memo/project 대응 없음. |
| Kivy | 같음 | `hello-kivy` · `screenshots/kivy.png` | **missing**(부록) | missing | 1 | 빈칸 | 1 (영문 문구) | 빈칸 / 빈칸 | 글꼴 제약 주석만. |
| 부록 목차/페이지 | — | 없음 (`units/` 또는 `appendix/`) | **missing** | missing | 0 | 빈칸 | — | 빈칸 / 빈칸 | 생성 파이프라인에 부록 유닛 없음. |

---

## 10. 선설명 · 팁 빈칸 (라온)

`#57`이 `lesson`/`ex`에 `preexplain` · `history` · `youtube` · `screenshot`을 표준화하면 아래 id에 칸을 붙이면 된다. **지금은 필드 자체가 없어 값을 적지 않았다.**

### 10.1 선설명 (`preexplain` / API 등장 전)

산문에 함수 이름이 섞여 있어도 슬롯은 빈칸이다. “산문 힌트”는 라온이 옮길 때 참고용.

| unit | lesson id | 슬롯 | 산문에 이미 나오는 API (참고, 복붙 아님) |
| --- | --- | --- | --- |
| 1 | overview | **빈칸** | import, 모듈/패키지 정의 |
| 1 | define | **빈칸** | def, class, 최상위 실행 |
| 1 | entrypoint | **빈칸** | `__name__`, `__main__` |
| 1 | imports | **빈칸** | import / from / as / * |
| 1 | packages | **빈칸** | `__init__.py`, `__all__` |
| 1 | os-sys | **빈칸** | `os.name`, `getcwd`, `sys.argv`, `sys.exit` |
| 1 | math | **빈칸** | `pi`, `e`, `ceil`, `floor`, `factorial`, `gcd`, `pow` |
| 1 | random | **빈칸** | `random`, `randrange`, `choice`, `sample`, `shuffle` |
| 1 | datetime | **빈칸** | `now`, `weekday`, `timedelta`, `date` |
| 1 | thirdparty | **빈칸** | pip, 설치명≠import명 |
| 1 | review | **빈칸** | — |
| 1 | project | **빈칸** | `roll`, `days_left`, `draw` |
| 2 | ui | **빈칸** | — (CLI/GUI/NUI) |
| 2 | libraries | **빈칸** | Tk, Qt, wxWidgets, Kivy |
| 2 | widgets | **빈칸** | Label, Button, Entry, Text, Var, QLabel… |
| 2 | layout | **빈칸** | pack, grid, place, QVBoxLayout… |
| 2 | events | **빈칸** | command=, mainloop, clicked.connect, exec |
| 2 | memo | **빈칸** | filedialog, Text `"1.0"`, Menu, QFileDialog |
| 2 | pyside | **빈칸** | QApplication, setupUi, objectName |
| 2 | project | **빈칸** | messagebox, QMessageBox |
| 2 | review | **빈칸** | — |
| 3 | ml-overview … ml-project (13) | **각 빈칸** | fit/predict, scaler, KMeans `labels_` 등은 산문·표 |
| 4 | cv-overview … cv-project (11) | **각 빈칸** | imread, cvtColor, resize, Canny, detectMultiScale, boxes.cls |

### 10.2 역사 팁 (`history`) · 유튜브 (`youtube`)

검증된 공개 영상만. 저작권·연령은 #58.

| unit | lesson id | history | youtube | 메모 |
| --- | --- | --- | --- | --- |
| 1 | overview … project (12행) | **빈칸** | **빈칸** | 모듈/PyPI 역사 후보. |
| 2 | ui | **빈칸** | **빈칸** | Xerox/PARC, 마우스 GUI. #58 시드 우선. |
| 2 | libraries | **빈칸** | **빈칸** | Tk, Qt, wx, Kivy 연혁. |
| 2 | widgets | **빈칸** | **빈칸** | |
| 2 | layout | **빈칸** | **빈칸** | |
| 2 | events | **빈칸** | **빈칸** | 이벤트 루프. |
| 2 | memo | **빈칸** | **빈칸** | |
| 2 | pyside | **빈칸** | **빈칸** | Qt / Riverbank / LGPL. |
| 2 | project | **빈칸** | **빈칸** | |
| 2 | review | **빈칸** | **빈칸** | |
| 3 | ml-overview | **빈칸** | **빈칸** | 산문에 1956/1997/2012 — 슬롯으로 옮길 후보. |
| 3 | 나머지 12 | **빈칸** | **빈칸** | |
| 4 | 11행 | **빈칸** | **빈칸** | Haar, YOLO 논문/공식 튜토리얼. |
| 부록 | wxPython | **빈칸** | **빈칸** | |
| 부록 | Kivy | **빈칸** | **빈칸** | |

파이 힌트(`mascot.TIPS`)는 역사/유튜브와 **다른 칸**이다. I·II는 원고 있음, III·IV는 fallback 한 줄.

---

## 11. 후속 이슈

| 이슈 | 마일스톤 | 이 감사와의 관계 |
| --- | --- | --- |
| #50 | M0 갭 감사 | 이 문서 |
| **#51** | M1 단원Ⅱ | 독립 페이지 |
| **#52** | M1 | widgets~memo 예제 |
| **#53** | M1 | 선설명 블록 |
| **#54** | M1 | 스샷 파이프라인 |
| #55 | (부록) | wxPython 재구성 |
| #56 | (부록) | Kivy 재구성 |
| #57 | M3 공통 룰 | tip/history/youtube/screenshot 스키마 |
| #58 | | Ⅱ부터 역사·유튜브 시드 |
| #59 | | 단원Ⅰ 동일 품질 |
| #60 | | 단원Ⅲ |
| #61 | | 단원Ⅳ |
| #63 | | M1 본편 머지 후 중2 테스터 (지금은 호출하지 않음) |

---

## 12. 생성 파이프라인 메모 (감사 범위 밖, 구현 힌트)

- 사람이 고치는 곳: `tools/web/*.py`. `web/units/**`, `web/data/unit*.json`은 `build.py` 산출물.
- 독립 페이지(#51)는 `build.py`의 단원 루프(`section.lesson`)를 주제 단위 파일로 나누는 생성기 변경이다. 이 감사는 그 코드를 바꾸지 않았다.
- 예제 추가는 `content.py` `ex()` + `lesson(..., examples_=...)`. III·IV는 `later_units.example` / `browser_example`.
- 갤러리 스샷을 늘리려면 `capture_gui.py` + `verify.py`의 6장 assert를 함께 봐야 한다.
