"""Canonical hierarchy verified against the supplied textbook TOC (pp. 4–5).
Ranges include section content, excluding the following review/opening pages.
Existing web topic IDs and progress keys stay stable.
"""
from html import escape as esc
ROMAN={1:'Ⅰ',2:'Ⅱ',3:'Ⅲ',4:'Ⅳ'}
BOOK={
1:('모듈과 패키지 활용','6–39',[
 ('모듈, 패키지의 개요','8–13',[('모듈의 개념 및 필요성','9–10'),('패키지의 개념 및 필요성','11–12')], [('중단원 마무리','13'),('확인 학습','13')]),
 ('모듈, 패키지 활용','14–35',[('모듈 정의하기','15–18'),('모듈과 패키지 사용하기','19–25'),('여러 가지 모듈 활용하기','26–33')],[('중단원 마무리','34'),('확인 학습','35')])], '36–39'),
2:('GUI 프로그래밍','40–59',[
 ('GUI 프로그래밍 개요','42–48',[('사용자 인터페이스','43–44'),('파이썬 GUI','45–46')],[('중단원 마무리','47'),('확인 학습','48')]),
 ('GUI 프로그래밍 작성','49–57',[('tkinter의 구성 요소','50–51'),('GUI 앱 개발','52–55')],[('중단원 마무리','56'),('확인 학습','57')])], '58–59'),
3:('파이썬과 머신러닝','60–131',[
 ('머신러닝 개요','62–84',[('머신러닝이란?','63–67'),('머신러닝의 필요성과 활용','68–70'),('머신러닝 문제 해결 과정','71–75'),('머신러닝의 주요 용어','76–78'),('머신러닝 학습 방법의 종류','79–82')],[('중단원 마무리','83'),('확인 학습','84')]),
 ('머신러닝 라이브러리 활용','85–128',[('파이썬 머신러닝 라이브러리 소개','86–89'),('데이터 준비와 전처리','90–102'),('주요 머신러닝 알고리즘 활용','103–111'),('모델 평가와 선택','112–126')],[('중단원 마무리','127'),('확인 학습','128')])], '129–131'),
4:('파이썬과 컴퓨터 비전','132–195',[
 ('컴퓨터 비전 개요','134–146',[('컴퓨터 비전이란?','135–136'),('컴퓨터 비전의 활용 분야','137–139'),('컴퓨터 비전의 기본 개념','140–144')],[('중단원 마무리','145'),('확인 학습','146')]),
 ('컴퓨터 비전 라이브러리 활용','147–193',[('컴퓨터 비전 라이브러리 소개','148–154'),('이미지 데이터 다루기','155–162'),('이미지 전처리와 변환','163–172'),('이미지에서 중요한 부분 찾기','173–176'),('컴퓨터 비전 프로젝트 실습','177–191')],[('중단원 마무리','192'),('확인 학습','193')])], '194–195')}
# Each pair is (middle section, small section), numbered exactly as the book.
MAP={
1:{'overview':[(1,1),(1,2)],'define':[(2,1)],'entrypoint':[(2,1)],'imports':[(2,2)],'packages':[(2,2)], **{k:[(2,3)] for k in ['os-sys','math','random','datetime','thirdparty']},'review':[],'project':[]},
2:{'ui':[(1,1)],'libraries':[(1,2)],'widgets':[(2,1)],'layout':[(2,1)],'events':[(2,1),(2,2)],'memo':[(2,2)],'pyside':[],'project':[],'review':[]},
3:{'ml-overview':[(1,1)],'ml-use':[(1,2)],'ml-process':[(1,3),(2,2)],'ml-terms':[(1,4)],'ml-methods':[(1,5)],'ml-libraries':[(2,1)],'ml-preprocess':[(2,2)],'ml-classification':[(2,3)],'ml-regression':[(2,3),(2,4)],'ml-cluster':[(2,3)],'ml-metrics':[(2,4)],'ml-selection':[(2,4)],'ml-project':[]},
4:{'cv-overview':[(1,1),(1,2)],'cv-pixels':[(1,3)],'cv-pipeline':[(1,3)],'cv-libraries':[(2,1)],'cv-io':[(2,2)],'cv-filters':[(2,3)],'cv-transform':[(2,3)],'cv-features':[(2,4)],'cv-haar':[(2,5)],'cv-yolo':[(2,5)],'cv-project':[]}}
REVIEW={1:['review'],2:['review'],3:['ml-project'],4:['cv-project']}
def unit_label(u):return f'{ROMAN[u]}. {BOOK[u][0]}'
def references(u,l):
 result=[]
 for m,s in MAP[u][l['id']]:
  middle=BOOK[u][2][m-1]; small=middle[2][s-1]
  result.append(dict(middle=f'{m:02}. {middle[0]}',middle_pages=middle[1],small=f'{s:02}. {small[0]}',pages=small[1]))
 return result
def attach(units):
 for u,ls in units.items():
  assert set(MAP[u])=={l['id'] for l in ls}
  for l in ls:l['textbook']=references(u,l)

def badge(u,l):
 s=f'<div class="book-location"><p><b>대단원 {unit_label(u)}</b> <span>교과서 {BOOK[u][1]}쪽</span></p>'
 for r in references(u,l):
  s+=f'<p>중단원 {r["middle"]} <span>· {r["middle_pages"]}쪽</span><br><strong>소단원 {r["small"]}</strong> <span>· {r["pages"]}쪽</span></p>'
 if not references(u,l):
  s+='<p><strong>'+('마무리·종합 평가 연계' if l['id'] in REVIEW[u] else '추가 실습 · 교과서 밖 확장')+'</strong></p>'
 pages=l['pages'].replace(' + ', '쪽 + ')
 if any(c.isdigit() for c in pages) and '쪽' not in pages:pages+='쪽'
 s+=f'<p class="book-topic-pages">이 웹 주제의 연계 범위: {esc(pages)}</p></div>'
 return s

def toc(u,ls,target=''):
 s=f'<nav class="book-toc" aria-label="교과서 단원 목차"><h2>{unit_label(u)}</h2><p>대단원 · {BOOK[u][1]}쪽</p>'
 for m,(title,pages,smalls,reviews) in enumerate(BOOK[u][2],1):
  s+=f'<div class="book-middle"><h3>중단원 {m:02}. {title}</h3><p>{pages}쪽</p><ol>'
  for n,(name,pp) in enumerate(smalls,1):
   related=[l for l in ls if (m,n) in MAP[u][l['id']]]
   assert related, (u,m,n)
   s+=f'<li><strong>소단원 {n:02}. {name}</strong><span class="book-pages">{pp}쪽</span><ul>'+''.join(f'<li><a href="{target}#{l["id"]}">웹 실습 · {esc(l["title"])}</a></li>' for l in related)+'</ul></li>'
  s+='</ol><p class="book-review">'+ ' · '.join(f'{name} {pp}쪽' for name,pp in reviews)+'</p></div>'
 s+=f'<p class="book-review"><b>대단원 종합 평가</b> {BOOK[u][3]}쪽</p><div class="book-extra"><h3>복습·추가 실습</h3>'+''.join(f'<a href="{target}#{l["id"]}">{esc(l["title"])} <small>({"평가 연계" if l["id"] in REVIEW[u] else "확장"})</small></a>' for l in ls if not MAP[u][l['id']])+'</div></nav>'
 return s
