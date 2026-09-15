# 콘텐츠 갭 감사 — 교과서 TOC ↔ 웹 학습

이슈 [#50](https://github.com/progh2/aipy2/issues/50)의 산출물입니다. 마스터 품질 기준과 현재 사이트를 대조하고, 후속 이슈 [#51](https://github.com/progh2/aipy2/issues/51)–[#61](https://github.com/progh2/aipy2/issues/61)로 넘길 우선순위를 고정합니다.

이 PR은 **감사 문서만** 추가합니다. 레슨·예제·생성 HTML은 고치지 않습니다.

| 항목 | 값 |
| --- | --- |
| 대조 기준일 | 2026-09-15 |
| 기준 커밋 | `9f98674` (`main`) |
| 교과서 TOC 원본 | `tools/web/textbook.py`의 `BOOK` / `MAP` (인쇄본 4–5쪽) |
| 레슨 원본 | `tools/web/content.py` (Ⅰ·Ⅱ), `tools/web/later_units.py` (Ⅲ·Ⅳ) |
| 생성 데이터 | `web/data/unit1.json` … `unit4.json`, `web/data/catalog.json` |
| 생성기 | `tools/web/build.py` → `web/units/unit0N/index.html` |

생성 HTML은 결과물입니다. 이후 콘텐츠·페이지 구조 변경은 `tools/web/`만 고친 뒤 `python tools/web/build.py`로 다시 만듭니다. 손 편집 예외는 `web/before-you-start.html` 하나입니다.

---

## 1. 잠긴 품질 기준과 한줄 판정

| # | 기준 | 현재 | 판정 |
| --- | --- | --- | --- |
| 1 | 교과서 소단원(또는 학습 주제)마다 **독립 완결 페이지** | 단원당 HTML 1장. 주제는 `#id` 앵커 섹션 | **미달** |
| 2 | GUI 예제 수·설명이 충분 | Ⅱ단원 9주제 / 고유 예제 17개. widgets·layout·events가 특히 얇음 | **미달 (얇음)** |
| 3 | 새 API·속성을 코드 **등장 전에** 설명 | 문단은 있으나 `<details>`에 접힘. 스키마 필드 없음 | **미달** |
| 4 | 실습 실행 결과 **스크린샷을 페이지에** | 인사 앱 6장만 갤러리에 노출. 예제별 스샷 없음 | **미달** |
| 5 | 역사 / 유튜브 **팁 슬롯** | 파이 코칭 팁만 있음(Ⅰ·Ⅱ). `history`/`youtube` 필드 없음 | **미달** |
| 6 | 교과서 범위 전부 커버 | `BOOK` 소단원 26개는 모두 `MAP`에 ≥1개 웹 주제 | **매핑은 충족** / 페이지 깊이는 미달 |
| 7 | 부록 wxPython + Kivy | 인사 앱 `hello-wx`·`hello-kivy`만. 위젯·메모장 대응 없음 | **미달** |

**요약:** 교과서 소단원 *링크*는 빠짐없이 걸려 있습니다. 품질 기준이 요구하는 *독립 완결 학습 페이지*는 아직 아닙니다. 가장 얇은 본편은 단원 Ⅱ의 widgets / layout / events입니다.

---

## 2. 페이지가 어떻게 만들어지는가

`build.py`는 단원마다 **하나의** `web/units/unit0N/index.html`을 씁니다.

- 각 학습 주제는 `<section class="lesson" id="{lesson_id}">`입니다.
- 사이드 목차(`textbook.toc`)와 갤러리 링크는 `index.html#{id}` 앵커입니다. **주제별 HTML 파일이 없습니다.**
- 개념 본문은 `<details class="lesson-details"><summary>개념 더 읽기</summary>` 안에 접혀 있습니다.
- 파이 팁(`mascot.lesson_tip`)은 주제마다 붙지만, Ⅰ·Ⅱ만 주제별 문장이 있고 Ⅲ·Ⅳ는 공통 문구로 떨어집니다.
- 코드 실습실은 단원 페이지에 **에디터 1개**를 두고, 주제의 예제 버튼이 그 에디터를 엽니다.
- 연습 문제·저널도 같은 단원 페이지 하단에 묶입니다.
- 단원별 `summary.html`은 그림 요약 페이지이고, 소단원 본편이 아닙니다.

즉 지금 구조는 “4단원 × 장문 스크롤 페이지 + 앵커”입니다. 기준 1(독립 완결 페이지)과 [#51](https://github.com/progh2/aipy2/issues/51)이 요구하는 형태가 아닙니다.

학생·교사가 한 주제로 점프해도, 그 섹션만으로는 실습실·문제·스샷이 완결되지 않습니다. 실습실은 페이지 안 다른 위치로 이동하고, 문제는 맨 아래 공용 목록입니다.

---

## 3. 규모 스냅샷 (생성 JSON과 일치)

| 단원 | 웹 주제 | 고유 예제 | 예제 슬롯(재사용 포함) | web / pc | 연습 문제 |
| --- | ---: | ---: | ---: | --- | ---: |
| Ⅰ 모듈과 패키지 | 12 | 33 | 33 | 31 / 2 | 60 |
| Ⅱ GUI | 9 | 17 | 21 | 1 / 16 | 70 |
| Ⅲ 머신러닝 | 13 | 19 | 20 | 10 / 9 | 44 |
| Ⅳ 컴퓨터 비전 | 11 | 14 | 16 | 3 / 11 | 39 |
| **합** | **45** | **82** (Ⅰ·Ⅱ가 `core`를 공유) | — | — | **213** |

README의 “학습 주제 45 · 예제 82 · 연습 문제 213”과 같습니다. 숫자는 충분해 보여도, **페이지 단위·예제 밀도·스샷·선설명**이 기준에 못 미칩니다.

---

## 4. 교과서 소단원 ↔ 웹 주제

`textbook.toc()`는 모든 소단원에 관련 웹 주제가 있다고 `assert`합니다. 아래는 그 매핑의 *질*입니다.

### 4.1 단원 Ⅰ · 모듈과 패키지 활용 (6–39쪽)

| 교과서 | 쪽 | 웹 주제 | 예제 수 | 비고 |
| --- | --- | --- | ---: | --- |
| 01-01 모듈의 개념 및 필요성 | 9–10 | `overview` | 1 | 01-02와 **한 주제**로 묶임 |
| 01-02 패키지의 개념 및 필요성 | 11–12 | `overview` | (동일) | 패키지 실습은 `packages`로 미룸 |
| 01 마무리·확인학습 | 13 | `review`에 흡수 | — | 독립 페이지 아님 |
| 02-01 모듈 정의하기 | 15–18 | `define`, `entrypoint` | 5+2 | 소단원을 두 주제로 나눔 |
| 02-02 모듈과 패키지 사용하기 | 19–25 | `imports`, `packages` | 5+8 | 비교적 두꺼움 |
| 02-03 여러 가지 모듈 활용하기 | 26–33 | `os-sys`, `math`, `random`, `datetime`, `thirdparty` | 3+1+3+2+1 | 모듈별 주제는 있음. `math`·`thirdparty`는 예제 1개 |
| 02 마무리·확인학습 | 34–35 | `review` + `packages`의 35쪽 예제 | — | |
| 대단원 종합 평가 | 36–39 | `review` | 1 | |
| (교과서 밖) | — | `project` | 1 | `MAP` 빈 쌍 · `extra=True` |

Ⅰ은 소단원 커버와 예제 수가 네 단원 중 가장 낫습니다. 기준 1·3·4·5는 여전히 미달이라 [#59](https://github.com/progh2/aipy2/issues/59)로 동일 품질 보강이 필요합니다.

### 4.2 단원 Ⅱ · GUI 프로그래밍 (40–59쪽) — 본편 최우선

| 교과서 | 쪽 | 웹 주제 | 고유 예제 | 비고 |
| --- | --- | --- | ---: | --- |
| 01-01 사용자 인터페이스 | 43–44 | `ui` | **0** | 개념만. CLI/GUI/NUI 실습 없음 |
| 01-02 파이썬 GUI | 45–46 | `libraries` | 6 | 인사 앱 6종. 갤러리 스샷이 여기만 연결됨 |
| 01 마무리·확인학습 | 47–48 | `libraries` 과제 + `review` | — | |
| 02-01 tkinter의 구성 요소 | 50–51 | `widgets`, `layout`, `events` | 2+2+**0고유** | events는 `hello-tk`/`hello-pyside` **재사용** |
| 02-02 GUI 앱 개발 | 52–55 | `events`, `memo` | (재사용)+4 | 메모장은 통짜 완성본 + 개선본 |
| 02 마무리·확인학습 | 56–57 | `review` | **0** | |
| 대단원 종합 평가 | 58–59 | `review` | 0 | |
| (교과서 밖) | — | `pyside`, `project` | 재사용+3 | `extra=True` |

교과서 소단원은 **4개**인데 웹 주제는 **9개**입니다. 잘게 나눈 것처럼 보이지만, 실제로는 한 장에 붙어 있고 본편 예제가 갤러리·완성 앱에 치우쳐 있습니다.

### 4.3 단원 Ⅲ · 파이썬과 머신러닝 (60–131쪽)

| 교과서 | 쪽 | 웹 주제 | 예제 | 비고 |
| --- | --- | --- | --- | --- |
| 01-01 머신러닝이란? | 63–67 | `ml-overview` | 0 | 개념·표만 |
| 01-02 필요성과 활용 | 68–70 | `ml-use` | 0 | |
| 01-03 문제 해결 과정 | 71–75 | `ml-process` | 1 (웹 원리) | 02-02에도 매핑 |
| 01-04 주요 용어 | 76–78 | `ml-terms` | 0 | |
| 01-05 학습 방법의 종류 | 79–82 | `ml-methods` | 0 | |
| 01 마무리·확인학습 | 83–84 | 문제 은행 | — | 독립 페이지 아님 |
| 02-01 라이브러리 소개 | 86–89 | `ml-libraries` | 3 | science 스샷 `ml-chart` |
| 02-02 데이터 준비와 전처리 | 90–102 | `ml-process`, `ml-preprocess` | 1+3 | |
| 02-03 주요 알고리즘 | 103–111 | `ml-classification`, `ml-regression`, `ml-cluster` | 2+3+2 | |
| 02-04 모델 평가와 선택 | 112–126 | `ml-regression`, `ml-metrics`, `ml-selection` | (공유)+2+3 | 회귀 지표가 02-03·02-04에 걸침 |
| 02 마무리·확인학습 | 127–128 | `ml-selection` / 문제 | — | |
| 대단원 종합 평가 | 129–131 | `ml-project` | `ml-selection` 재사용 | |

개요 5개 소단원 중 3개가 예제 0입니다. 후반부는 웹 원리 예제(`ml-*-small`)와 PC scikit-learn이 있어 실행 경로는 있으나, 페이지·선설명·스샷·팁은 [#60](https://github.com/progh2/aipy2/issues/60) 대상입니다.

### 4.4 단원 Ⅳ · 파이썬과 컴퓨터 비전 (132–195쪽)

| 교과서 | 쪽 | 웹 주제 | 예제 | 비고 |
| --- | --- | --- | --- | --- |
| 01-01 컴퓨터 비전이란? | 135–136 | `cv-overview` | 0 | 01-02와 **한 주제** |
| 01-02 활용 분야 | 137–139 | `cv-overview` | (동일) | |
| 01-03 기본 개념 | 140–144 | `cv-pixels`, `cv-pipeline` | 1+0 | pipeline은 예제 없음 |
| 01 마무리·확인학습 | 145–146 | 문제 은행 | — | |
| 02-01 라이브러리 소개 | 148–154 | `cv-libraries` | 2 | science `cv-sobel` |
| 02-02 이미지 데이터 다루기 | 155–162 | `cv-io` | 2 | science `cv-io` |
| 02-03 전처리와 변환 | 163–172 | `cv-filters`, `cv-transform` | 1+2 | science 2장 |
| 02-04 중요한 부분 찾기 | 173–176 | `cv-features` | 1 | science 1장 |
| 02-05 프로젝트 실습 | 177–191 | `cv-haar`, `cv-yolo` | 2+3 | Haar/YOLO는 PC·외부 파일 의존 |
| 02 마무리·확인학습 | 192–193 | `cv-project` | 재사용 2 | |
| 대단원 종합 평가 | 194–195 | `cv-project` | (동일) | |

소단원 매핑은 있습니다. 01-01과 01-02를 한 페이지 주제로 합친 점, 실행 결과 스샷이 일부 주제의 “한눈에 보기”에만 있는 점이 [#61](https://github.com/progh2/aipy2/issues/61) 갭입니다.

---

## 5. 단원 Ⅱ 얇은 지점 (widgets / layout / events)

기준 2의 “얇음”을 이 세 주제에 한정해 적습니다. `libraries`(인사 6종)와 `memo`(완성·개선 4개)는 상대적으로 두껍습니다.

### 5.1 `widgets` — 창과 위젯 (교과서 50쪽)

- 예제 **2개**: `widgets-tk`, `widgets-pyside`. 각각 한 창에 Label/Entry/Text/Check/Radio/List/Canvas(또는 Qt 대응)를 **한 번에** 쌓습니다.
- 위젯별 독립 예제·독립 페이지가 없습니다.
- 문단에서 위젯 이름을 나열하지만, 코드 등장 전 속성(`text`, `variable`, `value`, `height` 등)을 위젯 단위로 선설명하지 않습니다.
- 실행 결과 스샷이 페이지에 없습니다. 갤러리는 인사 앱만 보여 줍니다.

### 5.2 `layout` — 배치 관리자 (교과서 51쪽)

- 예제 **2개**: pack/grid/place를 한 창에 비교(`layout-tk`), QVBox/QHBox/QGrid를 한 창에 비교(`layout-pyside`).
- `expand`/`fill`/`sticky`/`columnconfigure`/`addLayout`을 단계별로 보여 주는 예제가 없습니다.
- 웹 시뮬레이터(`#simulator`)가 수직·수평·격자를 보여 주지만, 편집한 Python을 실행하지 않는 학습용 모형입니다.
- 스샷 없음.

### 5.3 `events` — 이벤트 (교과서 51, 54쪽)

- **고유 예제 0.** `hello-tk`, `hello-pyside`를 `libraries`에서 다시 엽니다.
- `command=` vs `command=()` , `bind`, `after`, `textChanged`, `QTimer`는 문단에만 있고 전용 예제가 없습니다.
- 첫 GUI 코드(인사 앱)가 Button/`pack`/`command`/`mainloop`를 동시에 도입합니다. 선설명 기준과 충돌합니다.

### 5.4 인접 얇음

| 주제 | 예제 | 메모 |
| --- | ---: | --- |
| `ui` | 0 | 인터페이스 유형만. 확인학습 48쪽은 과제 문장으로만 연결 |
| `review` | 0 | 56–59쪽 마무리·종합평가를 한 섹션에 압축 |
| `pyside` | 재사용 2 | Designer 설명은 있으나 전용 `.ui` 예제 없음 |
| `memo` | 4 | 통짜 완성 → 개선. 여덟 단계를 **단계별 예제**로 쪼개지 않음 |

목표 밀도(후속 작업용): 본편 소주제마다 tk 예제 3+ / 대응 PySide 1+ / 선설명 블록 / 실행 스샷 1+. 지금 widgets·layout는 toolkit당 1개, events는 0개입니다. 확충은 [#52](https://github.com/progh2/aipy2/issues/52)입니다.

---

## 6. 스크린샷 파이프라인

### 6.1 GUI (`tools/web/capture_gui.py`)

- 인자 하나(`tk`/`ttk`/`pyside`/`pyqt`/`wx`/`kivy`)로 **프로세스 하나·툴킷 하나**를 실행합니다.
- 소스 고정: `hello-tk` … `hello-kivy`만. 이름을 넣고 인사한 뒤 PNG를 저장합니다.
- 출력: `web/assets/screenshots/{kind}.png` (현재 6장, 약 4–9KB).
- `verify.py`는 이 6장이 1000바이트를 넘기는지만 검사합니다.
- `build.py` 갤러리는 단원 Ⅱ 페이지 하단 `#gallery`에만 이 6장을 붙입니다. **레슨 섹션·예제 카드에는 넣지 않습니다.**

없는 것:

- `widgets-*`, `layout-*`, `memo-*`, `project-*` 캡처
- 예제 ID ↔ 파일명 스키마 (`screenshot` 필드 없음)
- 캡처 스크립트를 `hello-*` 너머로 일반화하는 목록
- 실습 실행 결과를 주제 본문에 끼우는 렌더 경로

이 확장이 [#54](https://github.com/progh2/aipy2/issues/54)입니다.

### 6.2 과학 그림 (`tools/web/render_science.py` → `web/assets/science/`)

| 파일 | 붙는 주제 |
| --- | --- |
| `ml-chart.png` | `ml-libraries` |
| `ml-cluster.png` | `ml-cluster` |
| `ml-learning-curve.png` | `ml-selection` |
| `cv-sobel.png` | `cv-libraries` |
| `cv-io.png` | `cv-io` |
| `cv-filters.png` | `cv-filters` |
| `cv-perspective.png` | `cv-transform` |
| `cv-features.png` | `cv-features` |

8장뿐이고 `learning_design.visual()`의 “한눈에 보기”에만 붙습니다. Ⅰ단원 콘솔 결과, Ⅲ 개요 주제, Haar/YOLO, 확인학습 페이지용 스샷은 없습니다.

---

## 7. 데이터 모델 — 선설명·팁·스샷 슬롯이 없음

`lesson()`이 쓰는 키:

`id`, `title`, `pages`, `lead`, `paragraphs`, `examples`, `tasks`, `extra`  
(+ 생성 시 `textbook` 뱃지, Ⅲ·Ⅳ는 `visual`)

`ex()`가 쓰는 키:

`id`, `title`, `files`, `mode`, `entry`, `stdin`, `args`, `checks`, `note`

없는 키(기준 3·4·5, [#57](https://github.com/progh2/aipy2/issues/57)):

| 슬롯 | 의도 | 현재 대용 |
| --- | --- | --- |
| API 선설명 | 코드 위 짧은 속성/시그니처 카드 | `paragraphs` (접힌 details) |
| `screenshot` | 예제·주제별 실행 결과 | 갤러리 6장 + science 8장 |
| `history` | 짧은 역사 팁 | 없음 |
| `youtube` | 검증된 공개 영상 | 없음 (출처 페이지는 문서 링크만) |

`mascot.TIPS`는 **학습 코칭**입니다. 역사/유튜브가 아닙니다. Ⅰ·Ⅱ는 주제별 문장이 있고, Ⅲ·Ⅳ는 기본 문장입니다. 시드 채우기는 스키마 합의([#57](https://github.com/progh2/aipy2/issues/57)) 후 Ⅱ부터([#58](https://github.com/progh2/aipy2/issues/58))입니다.

선설명 실패의 대표 경로(Ⅱ): 학생이 처음 만나는 GUI 코드는 `libraries`의 `hello-tk`입니다. `Tk()`, `title`, `geometry`, `Label`, `Entry`, `Button`, `pack`, `command`, `mainloop`가 한 예제에 등장합니다. 위젯 선설명은 그 아래 `widgets` 섹션(같은 페이지, 접힌 본문)에 있습니다.

---

## 8. 부록 wxPython · Kivy

교과서 45–46쪽은 tkinter / PyQt / wxPython / Kivy를 소개합니다. 웹은 PySide6·ttk를 보강한 비교 갤러리까지는 있습니다.

| 본편 (tk / PySide) | wxPython | Kivy |
| --- | --- | --- |
| 인사 앱 | `hello-wx` | `hello-kivy` (영문 문구) |
| 위젯 도감 | 없음 | 없음 |
| 배치 | 없음 | 없음 |
| 이벤트 | 없음 | 없음 |
| 메모장 | 없음 | 없음 |
| 생활 도우미 | 없음 | 없음 |
| 독립 부록 페이지 | 없음 | 없음 |

부록은 본편을 대체하지 않고, 같은 앱을 툴킷만 바꿔 재구성합니다. [#55](https://github.com/progh2/aipy2/issues/55), [#56](https://github.com/progh2/aipy2/issues/56).

---

## 9. 우선순위 표 → 이슈 #51–#61

마일스톤은 저장소 이슈와 같습니다. **이 감사(#50)를 닫은 뒤 위에서 아래로** 진행합니다.

| 우선 | 마일스톤 | 갭 | 근거(이 문서) | 이슈 |
| --- | --- | --- | --- | --- |
| P0 | M0 갭 감사·품질 기준 | 기준 고정·현황 기록 | 본 문서 | [#50](https://github.com/progh2/aipy2/issues/50) ← 이 PR |
| P1 | M1 단원Ⅱ GUI 본편 | 주제를 독립 완결 페이지로 | §2, §4.2 | [#51](https://github.com/progh2/aipy2/issues/51) |
| P1 | M1 | widgets·layout·events·memo 예제·단계 설명 | §5 | [#52](https://github.com/progh2/aipy2/issues/52) |
| P1 | M1 | Button/`pack`/`bind` 등 코드 전 선설명 블록 | §7 | [#53](https://github.com/progh2/aipy2/issues/53) |
| P1 | M1 | 예제별 실행 스샷을 페이지에. `capture_gui.py` 확장 | §6.1 | [#54](https://github.com/progh2/aipy2/issues/54) |
| P2 | M2 GUI 부록 | 같은 메모장/위젯을 wx로 | §8 | [#55](https://github.com/progh2/aipy2/issues/55) |
| P2 | M2 | 같은 앱을 Kivy로 | §8 | [#56](https://github.com/progh2/aipy2/issues/56) |
| P3 | M3 전 단원 공통 룰 | lesson/ex에 api·tip·history·youtube·screenshot 표준화 | §7 | [#57](https://github.com/progh2/aipy2/issues/57) |
| P3 | M3 | Ⅱ부터 역사·유튜브 시드 (저작권·연령 확인) | §7 | [#58](https://github.com/progh2/aipy2/issues/58) |
| P4 | M4 Ⅰ·Ⅲ·Ⅳ 동일 기준 | Ⅰ 독립 페이지·예제·선설명·스샷/팁 | §4.1 | [#59](https://github.com/progh2/aipy2/issues/59) |
| P4 | M4 | Ⅲ 개요 예제 공백·시각·커버 | §4.3, §6.2 | [#60](https://github.com/progh2/aipy2/issues/60) |
| P4 | M4 | Ⅳ 소단원 분리·예제·스샷 | §4.4, §6.2 | [#61](https://github.com/progh2/aipy2/issues/61) |

관련 이슈(이 표 밖): [#62](https://github.com/progh2/aipy2/issues/62) 검증·Pages 스모크, [#63](https://github.com/progh2/aipy2/issues/63) 학생 테스터. 콘텐츠를 나눈 뒤 회귀 확인용입니다.

### 권장 순서 (의존)

1. **#51** 생성기가 주제(또는 소단원)당 HTML을 내게 한다. 진행 키(`u{n}-{id}`)와 `catalog.json` 앵커를 깨지 않는다.
2. **#57**을 #52–#54와 겹치기 전에, 또는 첫 본편 보강과 동시에 스키마를 고정한다. 필드 없이 예제만 늘리면 다시 옮겨야 한다.
3. **#52 · #53 · #54**는 Ⅱ 본편을 같이 채운다. 예제를 늘리면서 선설명과 스샷을 같은 PR 묶음으로 넣는 편이 낫다.
4. **#55 · #56**은 본편 위젯·메모장 API가 안정된 뒤 대응 포팅한다.
5. **#58**은 #57 슬롯이 렌더된 뒤 Ⅱ부터 시드를 넣는다.
6. **#59 · #60 · #61**은 Ⅱ에서 검증한 페이지·스키마·스샷 룰을 복제한다.

---

## 10. 이 감사가 하지 않는 일

- 레슨·예제·문제 본문 재작성
- `web/units/**/*.html` 손 편집
- 스크린샷 재촬영, 유튜브 URL 확정, wx/Kivy 본문 작성
- `BOOK`/`MAP` 변경 (TOC는 이미 인쇄본과 맞음)

후속 PR은 `tools/web/`을 고치고 재생성합니다.
