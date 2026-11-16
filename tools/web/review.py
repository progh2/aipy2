"""기말고사 총정리 페이지(web/review.html) 데이터 조립과 HTML 생성.

- 소단원 데이터: review_data1.py(Ⅰ·Ⅱ), review_data2.py(Ⅲ), review_data3.py(Ⅳ)
- build.py가 body(WEB)를 불러 layout()으로 감싸 web/review.html을 쓴다.
- 코드 발췌 실행 확인: python3 tools/web/review.py --check /tmp/review_shots/code_checks.txt
  (파이썬은 /tmp/mlenv/bin/python이 있으면 그것을, 없으면 현재 인터프리터를 쓴다)

교과서에 있는 내용만 쓰고 쪽수를 표기한다. 객관식 문항은 만들지 않는다.
"""
import html
import re
import sys
from pathlib import Path

from review_data1 import UNIT1, UNIT2
from review_data2 import UNIT3
from review_data3 import UNIT4

UNITS = [UNIT1, UNIT2, UNIT3, UNIT4]
ROMAN = {1: 'Ⅰ', 2: 'Ⅱ', 3: 'Ⅲ', 4: 'Ⅳ'}
TIME = {1: 60, 2: 45, 3: 100, 4: 90}  # 단원별 권장 공부 시간(분)
EXAM = dict(
    when='2026년 12월 9일(수) 2교시',
    scope='교과서 전체 Ⅰ~Ⅳ단원',
    form='선택형(5지선다)',
)

esc = html.escape


def _h1_of(WEB, rel):
    """생성된 소단원 페이지의 h1 텍스트(링크 문구)."""
    p = Path(WEB) / rel
    if not p.exists():
        raise FileNotFoundError(f'총정리 링크 대상이 없습니다: {rel}')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', p.read_text(encoding='utf-8'), re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else rel


def _links(WEB, unit_n, lesson):
    out = []
    qs = []
    for name in lesson['web']:
        rel = f'units/unit0{unit_n}/{name}.html'
        out.append(f'<a href="{rel}">{esc(_h1_of(WEB, rel))}</a>')
        q = f'units/unit0{unit_n}/q-{name}.html'
        if (Path(WEB) / q).exists():
            qs.append(f'<a href="{q}">{esc(_h1_of(WEB, rel))} 문제</a>')
    if not qs:
        qs.append(f'<a href="units/unit0{unit_n}/practice.html">단원 전체 연습 문제</a>')
    return out, qs


def _code_html(code):
    if not code:
        return ''
    parts = [f'<div class="review-code"><p class="review-code-title">{esc(code["title"])}</p>']
    for name, src in code['files']:
        parts.append(f'<p class="review-file">{esc(name)}</p><pre><code>{esc(src.rstrip())}</code></pre>')
    if code.get('result') is not None:
        parts.append(f'<p class="review-file">실행 결과</p><pre class="review-out"><code>{esc(code["result"])}</code></pre>')
    else:
        parts.append('<p class="review-file">실행 결과 없음(창이나 파일이 필요한 코드입니다)</p>')
    parts.append(f'<p class="review-note">{esc(code["note"])}</p></div>')
    return ''.join(parts)


def _card(WEB, unit_n, lesson):
    lid = 'r-' + lesson['id']
    items = ''.join(f'<li>{esc(t)}</li>' for t in lesson['summary'])
    pit = ''.join(f'<li>{esc(t)}</li>' for t in lesson['pitfalls'])
    checks = ''.join(
        f'<li><p class="review-q">{esc(q)}</p><details><summary>답 보기</summary><p>{esc(a)}</p></details></li>'
        for q, a in lesson['checks']
    )
    webs, qs = _links(WEB, unit_n, lesson)
    return (
        f'<article class="review-card" id="{lid}">'
        f'<header><p class="review-no">{ROMAN[unit_n]}-{lesson["no"]}</p><h3>{esc(lesson["title"])}</h3>'
        f'<p class="review-pages">교과서 {esc(lesson["pages"])}</p></header>'
        f'<h4>핵심 개념</h4><ul class="review-points">{items}</ul>'
        f'{_code_html(lesson["code"])}'
        f'<h4>헷갈리기 쉬운 점</h4><ul class="review-pit">{pit}</ul>'
        f'<h4>스스로 점검</h4><ol class="review-checks">{checks}</ol>'
        f'<p class="review-links"><span>웹 학습</span> {" · ".join(webs)}</p>'
        f'<p class="review-links"><span>연습 문제</span> {" · ".join(qs)}</p>'
        f'</article>'
    )


def _unit_section(WEB, u):
    n = u['n']
    flow = ''.join(f'<li>{esc(t)}</li>' for t in u['flow'])
    terms = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td></tr>' for a, b in u['terms'])
    cards = ''.join(_card(WEB, n, l) for l in u['lessons'])
    return (
        f'<details class="review-unit" id="unit-{n}"><summary><span class="review-unit-no">{ROMAN[n]}</span>'
        f'<span class="review-unit-title">{esc(u["title"])}</span>'
        f'<span class="review-unit-count">소단원 {len(u["lessons"])}개</span></summary>'
        f'<div class="review-unit-body">'
        f'<h3 class="review-sub">이 단원 한 장 요약</h3><ol class="review-flow">{flow}</ol>'
        f'<h3 class="review-sub">핵심 용어</h3><div class="table-wrap"><table class="review-terms">'
        f'<thead><tr><th scope="col">용어</th><th scope="col">뜻</th></tr></thead><tbody>{terms}</tbody></table></div>'
        f'{cards}</div></details>'
    )


# 단원을 가로지르는 헷갈리기 쉬운 개념: (단원, 제목, 왼쪽 이름, 왼쪽 설명, 오른쪽 이름, 오른쪽 설명, 쪽)
CONFUSIONS = [
    (1, 'import 방식과 호출 방식', 'import 모듈', 'greet.hello()처럼 모듈 이름을 붙여 호출합니다.',
     'from 모듈 import 함수', 'hello()처럼 이름만으로 호출합니다. greet.hello()는 오류입니다.', '19~21쪽'),
    (1, '직접 실행과 임포트', '직접 실행', '__name__ 값이 "__main__"이 되어 if __name__ == "__main__": 안의 코드가 실행됩니다.',
     '임포트', '__name__ 값이 모듈 이름이 되어 그 안의 코드는 실행되지 않습니다.', '17~18쪽'),
    (1, '모듈과 패키지', '모듈', '함수, 클래스, 변수, 실행문을 담은 파일 하나입니다.',
     '패키지', '여러 모듈을 용도별로 묶어 둔 디렉터리 구조입니다.', '9쪽, 11쪽'),
    (2, 'CLI, GUI, NUI', 'CLI와 GUI', 'CLI는 키보드로 명령어를 입력하고, GUI는 마우스나 터치로 아이콘과 버튼을 조작합니다.',
     'NUI', '음성, 손짓, 터치 등 신체 동작으로 상호 작용합니다.', '43~44쪽'),
    (2, 'Tk 객체와 위젯', 'Tk()', '프로그램의 기본 창(root window)을 만드는 객체입니다.',
     '위젯', 'Label, Button, Entry 등 그 창 위에 놓는 요소입니다.', '50~51쪽'),
    (2, '배치 관리자', 'pack()', '위에서 아래로, 왼쪽에서 오른쪽으로 차례대로 배치합니다.',
     'grid()와 place()', 'grid()는 행과 열로, place()는 좌표 (x, y)를 지정해 배치합니다.', '51쪽'),
    (3, '검증과 테스트', '검증', '학습 중간에 성능을 점검하고 모델 선택과 하이퍼파라미터 조정에 씁니다.',
     '테스트', '학습이 끝난 뒤 처음 보는 데이터로 최종 성능을 평가합니다.', '77쪽'),
    (3, '정밀도와 재현율', '정밀도', '긍정이라고 예측한 것 중 실제 긍정의 비율입니다. FP를 줄이는 것이 중요할 때 봅니다.',
     '재현율', '실제 긍정 중 긍정으로 맞힌 비율입니다. FN을 줄이는 것이 중요할 때 봅니다.', '120쪽'),
    (3, '정규화와 표준화', '정규화', '값의 범위를 0~1로 맞춥니다. 이상치에 민감합니다.',
     '표준화', '평균 0, 표준편차 1로 바꿉니다.', '96~99쪽'),
    (4, '영상 처리와 컴퓨터 비전', '영상 처리', '이미지 품질을 개선하거나 변형하며 출력은 수정된 이미지입니다.',
     '컴퓨터 비전', '의미 있는 정보를 추출하고 이해하며 출력은 분석 결과입니다.', '135쪽'),
    (4, 'OpenCV와 Pillow', 'OpenCV', '색상은 BGR 순서이고 shape는 (높이, 너비, 채널)입니다.',
     'Pillow', '색상은 RGB 순서이고 size는 (너비, 높이)입니다.', '156쪽'),
    (4, 'Haar Cascade와 YOLOv8', 'Haar Cascade', '얼굴, 눈처럼 정해진 형태를 CPU로 빠르게 찾을 때 알맞습니다.',
     'YOLOv8', '여러 종류의 객체를 동시에 실시간으로 높은 정확도로 찾을 때 알맞습니다.', '191쪽'),
]


def _confusions():
    rows = []
    for n, title, la, lt, ra, rt, pg in CONFUSIONS:
        rows.append(
            f'<article class="review-conf"><p class="review-no">{ROMAN[n]}단원 · 교과서 {esc(pg)}</p><h3>{esc(title)}</h3>'
            f'<dl><div><dt>{esc(la)}</dt><dd>{esc(lt)}</dd></div><div><dt>{esc(ra)}</dt><dd>{esc(rt)}</dd></div></dl></article>'
        )
    return ''.join(rows)


def _plan():
    rows = []
    for u in UNITS:
        n = u['n']
        rows.append(
            f'<li><label><input type="checkbox" data-review="plan-{n}"><span>{ROMAN[n]}단원 {esc(u["title"])} '
            f'(소단원 {len(u["lessons"])}개) 약 {TIME[n]}분</span></label></li>'
        )
    rows.append('<li><label><input type="checkbox" data-review="plan-conf"><span>자주 헷갈리는 개념 모음 약 20분</span></label></li>')
    rows.append('<li><label><input type="checkbox" data-review="plan-final"><span>마지막 점검표로 빠진 소단원 확인 약 10분</span></label></li>')
    total = sum(TIME.values()) + 30
    return rows, total


def _final_list():
    groups = []
    for u in UNITS:
        n = u['n']
        li = ''.join(
            f'<li><label><input type="checkbox" data-review="r-{l["id"]}" data-review-lesson>'
            f'<span>{ROMAN[n]}-{l["no"]} {esc(l["title"])}</span></label>'
            f'<a class="review-jump" href="#r-{l["id"]}">카드</a></li>'
            for l in u['lessons']
        )
        groups.append(f'<section><h3>{ROMAN[n]}. {esc(u["title"])}</h3><ul>{li}</ul></section>')
    return ''.join(groups)


def body(WEB):
    total_lessons = sum(len(u['lessons']) for u in UNITS)
    assert total_lessons == 26, total_lessons
    plan_rows, plan_total = _plan()
    chips = ''.join(
        f'<a href="#unit-{u["n"]}"><b>{ROMAN[u["n"]]}</b> {esc(u["title"])} <small>소단원 {len(u["lessons"])}개</small></a>'
        for u in UNITS
    )
    sections = ''.join(_unit_section(WEB, u) for u in UNITS)
    return f'''<main id="main" class="review-page">
<section class="review-hero"><p class="eyebrow">FINAL REVIEW</p><h1>기말고사 총정리</h1>
<p class="lead">교과서 Ⅰ~Ⅳ단원의 소단원 {total_lessons}개를 한 곳에 모았습니다. 각 카드에는 교과서 쪽수가 적혀 있으니 헷갈리면 교과서와 웹 학습 페이지로 돌아가 확인하세요.</p></section>
<section class="review-block" id="review-info"><h2>시험 안내</h2>
<dl class="review-info"><div><dt>일시</dt><dd>{esc(EXAM['when'])}</dd></div><div><dt>범위</dt><dd>{esc(EXAM['scope'])}</dd></div><div><dt>형식</dt><dd>{esc(EXAM['form'])}</dd></div></dl></section>
<section class="review-block" id="review-plan"><h2>공부 순서 제안</h2>
<ol class="review-steps"><li>단원 한 장 요약과 핵심 용어를 먼저 읽습니다.</li><li>소단원 카드의 핵심 개념과 헷갈리기 쉬운 점을 읽고, 코드는 직접 실행해 결과를 확인합니다.</li><li>스스로 점검의 답을 가린 채 말이나 글로 먼저 답한 뒤 열어 봅니다.</li><li>막힌 곳은 교과서 쪽을 펴서 확인하고 연습 문제를 풉니다.</li><li>마지막에 점검표를 채우며 빠진 소단원이 없는지 확인합니다.</li></ol>
<p class="small">단원별 권장 시간은 합계 약 {plan_total}분입니다. 하루에 몰아서 하지 말고 며칠에 나누어 진행하세요. 체크 표시는 이 브라우저에 저장됩니다.</p>
<ul class="review-plan">{''.join(plan_rows)}</ul></section>
<nav class="review-chips" id="review-nav" aria-label="단원 바로가기"><h2>단원 바로가기</h2><div>{chips}</div>
<p class="review-tools"><button type="button" data-review-toggle="open">모든 단원 펼치기</button><button type="button" data-review-toggle="close">모든 단원 접기</button><button type="button" data-review-print>인쇄하기</button></p></nav>
<section class="review-units" aria-label="단원별 정리">{sections}</section>
<section class="review-block" id="review-confusions"><h2>자주 헷갈리는 개념</h2><p class="small">단원마다 비교해서 구분해 두면 좋은 짝을 모았습니다.</p><div class="review-conf-grid">{_confusions()}</div></section>
<section class="review-block review-final" id="review-final"><h2>마지막 점검 체크리스트</h2>
<p>소단원마다 "설명할 수 있다"고 느낄 때 체크하세요. 체크 상태는 이 브라우저에만 저장되고 서버로 보내지지 않습니다.</p>
<div class="review-progress"><progress id="review-progress" max="{total_lessons}" value="0" aria-label="총정리 점검 진행도"></progress><span id="review-progress-text" aria-live="polite">0 / {total_lessons}</span></div>
<div class="review-final-grid">{_final_list()}</div>
<p class="review-tools"><button type="button" data-review-reset>점검 표시 모두 지우기</button></p></section>
</main>'''


# ---------------------------------------------------------------- 코드 실행 확인
def check(out_path):
    """코드 발췌를 실제로 실행해 결과가 데이터와 같은지 확인하고 기록한다."""
    import shutil
    import subprocess
    import tempfile
    import ast

    py = '/tmp/mlenv/bin/python' if Path('/tmp/mlenv/bin/python').exists() else sys.executable
    lines = [f'코드 발췌 실행 확인 (python: {py})', '']
    ok_count = 0
    fail = []
    for u in UNITS:
        for l in u['lessons']:
            code = l['code']
            tag = f'{ROMAN[u["n"]]}-{l["no"]} {l["title"]}'
            if not code:
                lines.append(f'[코드 없음] {tag}')
                continue
            if code['run'] is None:
                for name, src in code['files']:
                    ast.parse(src)
                lines.append(f'[문법 확인만] {tag} - 창이나 파일이 필요해 실행하지 않음')
                continue
            d = Path(tempfile.mkdtemp(prefix='review_chk_'))
            try:
                for name, src in code['files']:
                    p = d / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(src, encoding='utf-8')
                r = subprocess.run([py, code['run']], cwd=d,
                                   capture_output=True, text=True, timeout=120,
                                   env={'PYTHONPATH': str(d), 'PATH': '/usr/bin:/bin', 'PYTHONIOENCODING': 'utf-8'})
                got = '\n'.join(s.rstrip() for s in r.stdout.strip().splitlines())
                want = '\n'.join(s.rstrip() for s in code['result'].strip().splitlines())
                same = r.returncode == 0 and got == want
                lines.append(f'[{"일치" if same else "불일치"}] {tag}\n    기대: {want!r}\n    실제: {got!r}')
                if r.stderr.strip() and not same:
                    lines.append('    stderr: ' + r.stderr.strip().splitlines()[-1])
                if same:
                    ok_count += 1
                else:
                    fail.append(tag)
            finally:
                shutil.rmtree(d, ignore_errors=True)
    lines += ['', f'실행 일치 {ok_count}건, 불일치 {len(fail)}건']
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))
    return not fail


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--check':
        sys.exit(0 if check(sys.argv[2]) else 1)
    print('사용법: python3 tools/web/review.py --check 출력파일')
