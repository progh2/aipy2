"""Optional lesson/example slots: pre_api, glossary, tips (history/youtube), screenshots.

Empty values are stored and omitted from HTML. Fill later without changing the generator.
"""
from html import escape as esc

SLOT_KEYS = ('pre_api', 'glossary', 'tips', 'history', 'youtube', 'screenshots', 'screenshot')

def as_list(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]

def api_items(items):
    out = []
    for item in as_list(items):
        if isinstance(item, str):
            out.append({'name': item, 'signature': '', 'note': ''})
        elif item:
            out.append({
                'name': item.get('name') or item.get('term') or '',
                'signature': item.get('signature') or item.get('sig') or '',
                'note': item.get('note') or item.get('meaning') or item.get('text') or '',
            })
    return out

def glossary_items(items):
    out = []
    for item in as_list(items):
        if isinstance(item, str):
            out.append({'term': item, 'meaning': ''})
        elif item:
            out.append({
                'term': item.get('term') or item.get('name') or '',
                'meaning': item.get('meaning') or item.get('note') or item.get('text') or '',
            })
    return out

def youtube_items(value):
    out = []
    for item in as_list(value):
        if isinstance(item, str):
            out.append({'title': '관련 영상', 'url': item, 'note': ''})
        elif item:
            out.append({
                'title': item.get('title') or item.get('label') or '관련 영상',
                'url': item.get('url') or item.get('href') or '',
                'note': item.get('note') or item.get('text') or '',
            })
    return [v for v in out if v['url']]

def tips_block(tips=None, history=None, youtube=None):
    raw = dict(tips or {})
    hist = raw.get('history', '') if history is None else history
    if isinstance(hist, dict):
        hist = hist.get('text') or hist.get('note') or hist.get('title') or ''
    yt = raw.get('youtube', []) if youtube is None else youtube
    return {'history': hist or '', 'youtube': youtube_items(yt)}

def shot_items(screenshots=None, screenshot=None):
    items = []
    if screenshot:
        items.extend(as_list(screenshot))
    if screenshots:
        items.extend(as_list(screenshots))
    out = []
    for item in items:
        if isinstance(item, str):
            out.append({'src': item, 'alt': '', 'caption': ''})
        elif item:
            src = item.get('src') or item.get('file') or item.get('path') or ''
            if src:
                out.append({
                    'src': src,
                    'alt': item.get('alt') or '',
                    'caption': item.get('caption') or item.get('title') or '',
                })
    return out

def attach(record, *, pre_api=None, glossary=None, tips=None, history=None, youtube=None, screenshots=None, screenshot=None):
    record['pre_api'] = api_items(pre_api)
    record['glossary'] = glossary_items(glossary)
    record['tips'] = tips_block(tips, history, youtube)
    record['screenshots'] = shot_items(screenshots, screenshot)
    return record

def pick_slots(kwargs):
    return {k: kwargs[k] for k in SLOT_KEYS if k in kwargs}

def has_pre(record):
    return bool(record.get('pre_api') or record.get('glossary') or record.get('pre_visual'))

def has_tips(record):
    tips = record.get('tips') or {}
    return bool(tips.get('history') or tips.get('youtube'))

def has_shots(record):
    return bool(record.get('screenshots'))

def has_slots(record):
    return has_pre(record) or has_tips(record) or has_shots(record)

def shot_href(src, prefix):
    src = src or ''
    if src.startswith(('http://', 'https://', 'data:')):
        return src
    if src.startswith(('../', '/')):
        return src
    if src.startswith('assets/'):
        return prefix + src
    return f'{prefix}assets/screenshots/{src}'

def _concept_visual_html(spec):
    """Render a concept-visual / flow / table block for pre-api (same classes as lesson visuals)."""
    if not spec:
        return ''
    from learning_design import flow, table
    title = spec.get('title') or ''
    steps = spec.get('steps') or []
    tables = list(spec.get('tables') or [])
    if spec.get('headers') is not None and spec.get('rows') is not None:
        tables.insert(0, {'headers': spec['headers'], 'rows': spec['rows']})
    extra_class = spec.get('class') or ''
    cls = 'concept-visual' + (f' {extra_class}' if extra_class else '')
    caption = ''
    if title:
        caption = f'<figcaption><span class="eyebrow">AT A GLANCE</span><h3>{esc(title)}</h3></figcaption>'
    body = flow(steps) if steps else ''
    body += ''.join(
        table(item['headers'], item['rows'])
        for item in tables if item.get('headers') is not None
    )
    if not caption and not body:
        return ''
    return f'<figure class="{esc(cls, True)}">{caption}{body}</figure>'


def _pre_html(record, heading_id=''):
    cards = []
    for item in record.get('pre_api') or []:
        sig = f'<code>{esc(item["signature"])}</code>' if item.get('signature') else ''
        note = f'<p>{esc(item["note"])}</p>' if item.get('note') else ''
        cards.append(f'<article class="api-card"><strong>{esc(item["name"])}</strong>{sig}{note}</article>')
    terms = []
    for item in record.get('glossary') or []:
        meaning = f'<p>{esc(item["meaning"])}</p>' if item.get('meaning') else ''
        terms.append(f'<article class="glossary-card"><strong>{esc(item["term"])}</strong>{meaning}</article>')
    visual = _concept_visual_html(record.get('pre_visual'))
    if not cards and not terms and not visual:
        return ''
    hid = f' id="{heading_id}"' if heading_id else ''
    body = visual
    if cards:
        body += f'<div class="api-grid">{"".join(cards)}</div>'
    if terms:
        body += f'<div class="glossary-grid">{"".join(terms)}</div>'
    return f'<section class="content-slots pre-api"{hid}><p class="eyebrow">BEFORE THE CODE</p><h3>코드 전에 알아 두기</h3><p class="small">새 이름·속성이 코드에 나오기 전에 짧게 봅니다. 외우기보다 역할을 먼저 구별하세요.</p>{body}</section>'

def _tips_html(record, heading_id=''):
    tips = record.get('tips') or {}
    parts = []
    if tips.get('history'):
        parts.append(f'<article class="tip-history"><h4>역사 한 줄</h4><p>{esc(tips["history"])}</p></article>')
    for video in tips.get('youtube') or []:
        note = f'<p class="small">{esc(video["note"])}</p>' if video.get('note') else ''
        parts.append(f'<article class="tip-youtube"><h4>영상</h4><p><a href="{esc(video["url"], True)}" target="_blank" rel="noopener">{esc(video["title"])} ↗</a></p>{note}</article>')
    if not parts:
        return ''
    hid = f' id="{heading_id}"' if heading_id else ''
    return f'<section class="content-slots content-tips"{hid}><p class="eyebrow">HISTORY / VIDEO</p><h3>더 알아보는 팁</h3><div class="tip-grid">{"".join(parts)}</div></section>'

def _shots_html(record, prefix, heading_id=''):
    figs = []
    for shot in record.get('screenshots') or []:
        href = shot_href(shot['src'], prefix)
        alt = shot.get('alt') or shot.get('caption') or '실행 결과 화면'
        cap = f'<figcaption>{esc(shot["caption"])}</figcaption>' if shot.get('caption') else ''
        figs.append(f'<figure class="content-shot"><a href="{esc(href, True)}" target="_blank" rel="noopener"><img src="{esc(href, True)}" loading="lazy" alt="{esc(alt)}"></a>{cap}</figure>')
    if not figs:
        return ''
    hid = f' id="{heading_id}"' if heading_id else ''
    return f'<section class="content-slots content-shots"{hid}><p class="eyebrow">RESULT PREVIEW</p><h3>실행하면 이렇게 보여요</h3><div class="shot-grid">{"".join(figs)}</div></section>'

def render(record, prefix, *, ids=None):
    """Render present slots. ids={'pre','tips','shots'} assigns stable heading ids (lesson level)."""
    ids = ids or {}
    return _pre_html(record, ids.get('pre', '')) + _tips_html(record, ids.get('tips', '')) + _shots_html(record, prefix, ids.get('shots', ''))

def render_example(example, prefix):
    if not has_slots(example):
        return ''
    inner = render(example, prefix, ids={
        'pre': f'pre-api-{example["id"]}',
        'tips': f'content-tips-{example["id"]}',
        'shots': f'screenshots-{example["id"]}',
    })
    return f'<article class="example-guide" data-example-guide="{esc(example["id"], True)}"><h3>{esc(example["title"])}</h3>{inner}</article>'

def render_examples(example_ids, examples, prefix):
    cards = [render_example(examples[eid], prefix) for eid in example_ids if eid in examples]
    cards = [c for c in cards if c]
    if not cards:
        return ''
    return f'<div id="example-guides" class="example-guides">{"".join(cards)}</div>'

def flags(*records):
    return {
        'pre': any(has_pre(r) for r in records),
        'tips': any(has_tips(r) for r in records),
        'shots': any(has_shots(r) for r in records),
    }
