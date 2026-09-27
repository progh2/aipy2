"""학생 페이지 <main> 안의 주요 블록에 data-fb="b{n}"을 순서대로 붙인다(#126).

follow-model.js의 블록 앵커('{id}~b{n}@{비율}')가 이 속성을 가리켜 화면 단위로 따라가기를
지원한다. id를 새로 추가하지 않고 전용 data 속성만 쓴다 — 기존 앵커·follow-model.js의
페이지 해석 규칙에는 전혀 영향이 없다(블록 부분은 스크롤에만 쓰고 경로 판정에는 쓰지 않음).

번호는 문서 안에서 등장 순서대로 매기며, 페이지마다 새로 1부터 시작한다(결정론적).
"""
import re

# 블록으로 볼 요소: 제목(h2/h3), 문단(p), 코드·그림·표(pre/figure/table), 개념 도식과
# 카드 목록(named 컨테이너), 예제 페이지의 편집기 섹션(#lab). 문항 카드(#questions .question)는
# 빌드 시점에는 존재하지 않는 JS 생성 요소라 여기서 다루지 않는다 — 그 카드는 이미 자기 id를
# 블록 키로 쓴다(follow-model.js/teacher-focus.js 쪽 설명 참조).
_BLOCK_TAG_RE = re.compile(
 r'<h2\b[^>]*>'
 r'|<h3\b[^>]*>'
 r'|<p\b[^>]*>'
 r'|<pre\b[^>]*>'
 r'|<figure\b[^>]*>'
 r'|<table\b[^>]*>'
 r'|<section\s+class="lab"\s+id="lab"[^>]*>'
 r'|<div\s+class="task-box"[^>]*>'
 r'|<div\s+class="lesson-workspace"[^>]*>'
 r'|<div\s+class="example-links"[^>]*>'
 r'|<div\s+class="course-grid"[^>]*>'
 r'|<div\s+class="topic-grid"[^>]*>'
 r'|<div\s+class="gallery-grid"[^>]*>'
 r'|<div\s+class="sim-grid"[^>]*>'
 r'|<div\s+class="filter-row"[^>]*>'
 r'|<div\s+class="question-progress"[^>]*>'
)


def mark_focus_blocks(html):
 """완성된 페이지 HTML 문자열을 받아 <main>...</main> 안의 블록에만 data-fb를 매긴다.
 <main>이 없으면 그대로 돌려준다(교사 관리 화면 등 이 함수를 안 거는 페이지는 호출 자체를 안 함)."""
 m = re.search(r'<main\b[^>]*>', html)
 if not m:
  return html
 start = m.end()
 end = html.find('</main>', start)
 if end == -1:
  return html
 inner = html[start:end]
 counter = [0]

 def repl(match):
  counter[0] += 1
  tag = match.group(0)
  # 이 태그들은 속성값에 '>'가 들어가지 않으므로 마지막 '>' 앞에 속성을 끼워 넣으면 된다.
  return tag[:-1] + f' data-fb="b{counter[0]}">'

 inner = _BLOCK_TAG_RE.sub(repl, inner)
 return html[:start] + inner + html[end:]
