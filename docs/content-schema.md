# 콘텐츠 스키마 — API 선설명 · 팁 · 스크린샷

이슈 [#57](https://github.com/progh2/aipy2/issues/57)의 계약입니다. **라온**이 교재 칸을 채우고, **건우**가 `tools/web` 생성·검증을 유지합니다.

빈 칸도 주제 페이지에 그대로 그립니다. 지금은 전 주제를 채우지 않습니다. 시드 채우기는 [#58](https://github.com/progh2/aipy2/issues/58)(역사·유튜브), [#53](https://github.com/progh2/aipy2/issues/53)(선설명 본문), [#54](https://github.com/progh2/aipy2/issues/54)(예제별 스샷)입니다.

생성 HTML(`web/units/**/*.html`)은 손대지 않습니다. `tools/web/`만 고친 뒤 `python tools/web/build.py`로 다시 만듭니다.

| 항목 | 위치 |
| --- | --- |
| 정규화·렌더 | `tools/web/content_schema.py` |
| 레슨·예제 원본 | `tools/web/content.py` (Ⅰ·Ⅱ), `tools/web/later_units.py` (Ⅲ·Ⅳ) |
| 페이지 생성 | `tools/web/build.py` → `web/units/unit0N/{id}.html` |
| 검증 | `tools/web/verify.py` |
| 갭 배경 | [content-gap-audit.md](content-gap-audit.md) §7 |

---

## 1. 필드 (영어 키)

레슨(`lesson`)과 예제(`ex`)에 **같은 네 칸**을 둡니다. 빼도 되고, 빼면 빈 칸으로 렌더됩니다.

| 키 | 한글 이름 | 형 | 비어 있음 | 어디에 보이나 |
| --- | --- | --- | --- | --- |
| `api` | API 선설명 | 목록 | `[]` | 본문 다음, **코드 실습실 앞** |
| `history` | 역사 팁 | 문자열 | `''` | 파이 코칭 팁 옆 슬롯 |
| `youtube` | 유튜브 팁 | 객체 | `{}` | 역사 팁 옆 슬롯. **링크만** (삽입 재생 없음) |
| `screenshot` | 실행 결과 화면 | 객체 | `{}` | 실습실 직전. 레슨+그 주제 예제를 모음 |

파이 코칭(`mascot.TIPS`)과 다릅니다. 파이는 “지금 무엇을 해볼까”이고, `history`/`youtube`는 배경 지식·영상입니다.

기존 키(`id`, `title`, `pages`, `lead`, `paragraphs`, `examples`, `tasks`, `extra`, `files`, `mode`, `note` …)는 그대로입니다.

---

## 2. 각 칸의 뜻

### `api` — 코드에 나오기 전에

코드에 **처음 등장하는** 함수·클래스·속성·메서드를 한 줄로 적습니다. 긴 문단은 `paragraphs`에 두고, 여기는 이름 카드입니다.

한 줄:

| 키 | 필수 | 예 |
| --- | --- | --- |
| `name` | 예 | `tk.Button`, `pack`, `command` |
| `kind` | 아니오 | `클래스`, `함수`, `메서드`, `속성` |
| `meaning` | 아니오 | 한 문장 |

튜플도 됩니다: `(name, meaning)` 또는 `(name, kind, meaning)`.

주제(`lesson`)에 적으면 그 페이지 공통 선설명입니다. 예제(`ex`)에 적으면 그 예제가 속한 주제 페이지에 **이름이 겹치지 않게** 이어 붙습니다.

### `history` — 한 줄 역사

두세 문장을 넘기지 않습니다. 연도·출처가 있으면 같이 적습니다. 파이 대사처럼 쓰지 않습니다.

### `youtube` — 같이 보면 좋은 영상

| 키 | 필수 | 예 |
| --- | --- | --- |
| `url` | 예 | `https://www.youtube.com/watch?v=…` 또는 `https://youtu.be/…` |
| `title` | 아니오 | 화면에 보이는 제목 |

문자열 URL만 넣어도 됩니다. `youtube.com` / `youtu.be`만 허용합니다. 연령·저작권·광고를 확인한 공개 영상만 (#58). 페이지에는 새 탭 링크만 넣고 iframe은 넣지 않습니다.

### `screenshot` — 실행하면 이런 화면

| 키 | 필수 | 예 |
| --- | --- | --- |
| `src` | 예 | `tk.png` |
| `alt` | 아니오 | 대체 텍스트 |
| `caption` | 아니오 | 그림 아래 한 줄 |

`src` 규칙:

- `tk.png` → `web/assets/screenshots/tk.png`
- `science/ml-chart.png` → `web/assets/science/ml-chart.png`
- `http…` 는 그대로 (가능하면 저장소 파일을 씁니다)

문자열만 넣으면 `src`로 봅니다. 갤러리 6장(`tk`…`kivy`)과 과학 그림은 기존 경로를 재사용해도 됩니다. 새 예제 스샷 촬영은 #54입니다.

---

## 3. 적는 위치

```python
# tools/web/content.py  · 예제
ex(
    'hello-tk',
    '인사 앱 · tkinter',
    {'main.py': '...'},
    mode='pc',
    screenshot={
        'src': 'tk.png',
        'alt': 'tkinter 인사 앱 실제 실행 화면',
        'caption': '이름 입력창과 인사·초기화 버튼',
    },
)

# tools/web/content.py  · 레슨
lesson(
    2, 'widgets', '창과 위젯 · 화면을 구성하는 부품', '50',
    '보여줄 정보와 받을 입력에 따라 위젯을 선택합니다.',
    ['위젯을 생성한 것만으로 배치는 끝나지 않습니다.'],
    ['widgets-tk'],
    ['체크박스와 라디오 버튼의 차이를 설명하세요.'],
    api=[
        ('tk.Button', '클래스', '클릭하면 command에 맡긴 함수를 실행합니다.'),
        ('pack', '메서드', '위젯을 부모 안에 놓습니다.'),
    ],
    history='tkinter는 파이썬과 함께 배포되는 Tcl/Tk 연결입니다.',
    youtube={'url': 'https://www.youtube.com/watch?v=…', 'title': '짧은 소개'},
)

# tools/web/later_units.py  · Ⅲ·Ⅳ도 같은 키워드
topic(3, 'ml-overview', '...', '...', '...', [...], [...], [...], [...],
      history='1956년 다트머스 워크숍은 AI라는 이름을 모은 자리입니다.')
example('ml-chart', '...', '...', 'matplotlib',
        screenshot={'src': 'science/ml-chart.png', 'alt': '과일 빈도 막대그래프'})
```

칸을 생략한 기존 `lesson()` / `ex()` / `topic()` / `example()` 호출은 그대로 동작합니다.

---

## 4. 페이지에 나오는 순서

주제 독립 페이지 `units/unit0N/{id}.html` (#51/#66):

1. 교과서 위치 · 제목 · 도입(`lead`) · 한눈에 보기
2. 개념 본문(`paragraphs`, 접지 않음)
3. **`api` 슬롯** — 코드에 나오기 전에
4. 파이 코칭 팁 (기존)
5. **`history` + `youtube` 슬롯**
6. 직접 해 보세요
7. **`screenshot` 슬롯** (레슨 + 이 주제 예제)
8. 코드 실습실
9. 이 주제 연습 문제

단원 안내 `index.html`에는 이 칸을 그리지 않습니다. 학생이 읽는 본편은 주제 페이지입니다.

빈 칸 표시:

- `data-slot="api|history|youtube|screenshot"`
- `data-filled="true|false"`
- 비어 있으면 `content-slot--empty`와 “아직 없습니다” 문장

채워진 칸만 남기고 빈 칸을 숨기는 일은 하지 않습니다. 라온이 자리를 보고 채울 수 있게 합니다.

---

## 5. JSON

`web/data/unit{n}.json`의 각 lesson/example에 네 키가 들어갑니다. 프론트는 아직 이 JSON으로 슬롯을 그리지 않고, 생성 HTML이 그립니다.

---

## 6. 지금 들어 있는 시드 (계약 확인용)

전 주제를 채운 것이 아닙니다.

| 칸 | 어디 | 내용 |
| --- | --- | --- |
| `api` | 레슨 `widgets` | `Label` / `Button` / `Entry` / `pack` / `command` |
| `history` | 레슨 `libraries` | Tcl/Tk·ttk·Qt 바인딩 한 줄 |
| `screenshot` | 예제 `hello-tk` | 기존 `assets/screenshots/tk.png` |
| `youtube` | (없음) | 모든 페이지에 빈 칸 |

---

## 7. 검증

`python tools/web/verify.py`가 확인합니다.

- 모든 레슨·예제에 네 키가 있다
- 모든 `units/unit0N/{id}.html`에 네 슬롯이 있다
- `screenshot.src`가 있으면 파일이 있고 1KB가 넘는다
- `youtube.url`이 있으면 YouTube 주소이다
- 위 시드가 `widgets.html` / `libraries.html`에 보인다
