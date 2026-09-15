# 교사 스모크 체크리스트 (단원 Ⅰ–Ⅳ)

수업 전, 또는 콘텐츠를 `main`에 넣은 뒤에 **페이지가 열리는지 · 실습실이 보이는지 · 팁이 보이는지**만 짧게 확인합니다.
자동 검증(`verify.py`)이 PASS여도 브라우저에서 한 번씩 열어 보세요.

생성 HTML(`web/units/**/*.html`)은 직접 고치지 않습니다. 고칠 내용은 `tools/web/` → `python3 tools/web/build.py`입니다.

---

## 1. 자동 검증 · 로컬 · Pages

의존성(과학 예제 실행용):

```bash
python3 -m pip install numpy pandas scikit-learn matplotlib pillow
```

Windows는 먼저 `set PYTHONUTF8=1` 을 켭니다. `file://`로 HTML을 직접 열면 학습 데이터와 Worker가 동작하지 않습니다.

```bash
python3 tools/web/build.py      # 생성
python3 tools/web/verify.py     # 한 줄로 PASS 가 나와야 함
python3 -m http.server 8000 --directory web
```

| 경로 | 주소 |
| --- | --- |
| 로컬 | http://127.0.0.1:8000/ |
| 학생용 Pages | https://progh2.github.io/aipy2/ |

- [ ] `verify.py`가 `PASS:` 한 줄로 끝난다
- [ ] PR에서는 GitHub Actions **Build and verify** (`.github/workflows/verify.yml`)가 초록이다
- [ ] `main`에 푸시하면 **Build and deploy Python classroom** (`.github/workflows/pages.yml`)이 같은 생성·검증 뒤 Pages에 올린다
- [ ] 배포 후 Pages 대문이 열리고, 로컬과 같은 경로(`units/unit0N/…`)가 있다

아래 체크는 **Pages 또는 로컬** 중 한곳에서 하면 됩니다. 경로는 Pages 기준입니다.

---

## 2. 공통 · 교사 화면

- [ ] [대문](https://progh2.github.io/aipy2/) — Ⅰ–Ⅳ 카드, 「시작하기 전에」, 「교사용 수업 요약」
- [ ] [시작하기 전에](https://progh2.github.io/aipy2/before-you-start.html)
- [ ] [교사용 수업 요약](https://progh2.github.io/aipy2/teacher/index.html) — 단원 Ⅰ–Ⅳ 요약 링크
- [ ] [교사 · Ⅰ](https://progh2.github.io/aipy2/teacher/unit01.html) · [Ⅱ](https://progh2.github.io/aipy2/teacher/unit02.html) · [Ⅲ](https://progh2.github.io/aipy2/teacher/unit03.html) · [Ⅳ](https://progh2.github.io/aipy2/teacher/unit04.html) — 「학생 실습실 →」가 해당 단원 안내로 간다

로그인·명단·세션은 이 목록의 범위가 아닙니다.

---

## 3. 단원 Ⅰ 모듈

각 주제에서 **코드 전에 알아 두기** · **실습실(`#lab`)** · **더 알아보는 팁**(역사 한 줄 / 유튜브)을 봅니다.

- [ ] [단원 안내](https://progh2.github.io/aipy2/units/unit01/index.html) — 주제 목록, 「첫 주제 시작하기」
- [ ] [모듈이 필요한 이유](https://progh2.github.io/aipy2/units/unit01/overview.html) — 선설명, 웹 실습 실행, 팁(역사 + Corey Schafer 모듈 강의)
- [ ] [math](https://progh2.github.io/aipy2/units/unit01/math.html) — 선설명·실습·역사. **유튜브 없음이 정상**
- [ ] 안내 페이지에서 연습 문제 영역(`#practice`)이 보인다

---

## 4. 단원 Ⅱ GUI

웹은 문법 확인·시뮬레이션입니다. 창이 뜨는 실행은 PC입니다.

- [ ] [단원 안내](https://progh2.github.io/aipy2/units/unit02/index.html)
- [ ] [창과 위젯](https://progh2.github.io/aipy2/units/unit02/widgets.html) — 선설명, `#lab`, 「실행하면 이렇게 보여요」 스샷, 팁(역사 + Tkinter 강의)
- [ ] [부록 wx](https://progh2.github.io/aipy2/units/unit02/wx.html) · [부록 Kivy](https://progh2.github.io/aipy2/units/unit02/kivy.html) — 실습실·선설명·스샷. wx는 **유튜브 없음이 정상**, Kivy는 강의가 있다
- [ ] PC 예제에 「PC에서 실행」 안내가 보인다

---

## 5. 단원 Ⅲ 머신러닝

- [ ] [단원 안내](https://progh2.github.io/aipy2/units/unit03/index.html)
- [ ] [AI·머신러닝·딥러닝](https://progh2.github.io/aipy2/units/unit03/ml-overview.html) — 선설명, 웹 실습 실행, 팁(다트머스 역사 + Crash Course). **가짜 GUI 스샷 없음이 정상**
- [ ] [군집](https://progh2.github.io/aipy2/units/unit03/ml-cluster.html) — 팁 영상, 실제 생성 그림(`assets/science/ml-cluster.png`)
- [ ] [프로젝트](https://progh2.github.io/aipy2/units/unit03/ml-project.html) — 선설명·역사. **유튜브 없음이 정상**

---

## 6. 단원 Ⅳ 컴퓨터 비전

카메라·개인 사진·YOLO 가중치는 PC 준비입니다. 자동으로 켜지거나 올라가지 않아야 합니다.

- [ ] [단원 안내](https://progh2.github.io/aipy2/units/unit04/index.html)
- [ ] [컴퓨터 비전과 영상 처리](https://progh2.github.io/aipy2/units/unit04/cv-overview.html) — 선설명, 웹 실습 실행, 팁(MIT 역사 + Crash Course #35)
- [ ] [블러·에지·이진화](https://progh2.github.io/aipy2/units/unit04/cv-filters.html) — 실습실, Computerphile 블러, science 비교 그림
- [ ] [원근 변환](https://progh2.github.io/aipy2/units/unit04/cv-transform.html) · [프로젝트](https://progh2.github.io/aipy2/units/unit04/cv-project.html) — 역사만, **유튜브 없음이 정상**

---

## 7. 실패가 아닌 비움

검증된 공개 강의가 없거나 콘솔 예제인 경우입니다. 빈칸을 억지로 채우지 않습니다.

| 단원 | 유튜브 없음 | 가짜 실행 스샷 없음 |
| --- | --- | --- |
| Ⅰ | `math` · `project` · `review` | 콘솔 주제 전반 |
| Ⅱ | `wx` · `project` · `review` · `libraries` | — (본편·부록은 실제 GUI 스샷) |
| Ⅲ | `ml-preprocess` · `ml-project` | 개요·역할 예제 |
| Ⅳ | `cv-transform` · `cv-project` | 개요·역할 예제 |

---

## 8. 깨진 것이 있으면

1. 경로와 증상을 이슈나 PR에 남긴다
2. `tools/web/`만 고친다
3. `python3 tools/web/build.py` 후 `python3 tools/web/verify.py`가 다시 PASS인지 본다
