"""Lesson/example slots: API 선설명, history/YouTube tips, run-result screenshot.

Empty values are valid. Build always renders the four slots on topic pages.
라온 fills copy later; 건우 keeps this contract in tools/web.
"""
from html import escape as esc

SLOT_KEYS = ('api', 'history', 'youtube', 'screenshot')
TITLES = {
    'api': '코드에 나오기 전에',
    'history': '한 줄 역사',
    'youtube': '같이 보면 좋은 영상',
    'screenshot': '실행하면 이런 화면',
}
EYEBROWS = {
    'api': 'API 선설명',
    'history': 'TIP / HISTORY',
    'youtube': 'TIP / YOUTUBE',
    'screenshot': 'RUN RESULT',
}
EMPTY = {
    'api': '이 주제에서 새로 나오는 함수·속성의 선설명이 아직 없습니다.',
    'history': '역사 팁이 아직 없습니다.',
    'youtube': '관련 영상 링크가 아직 없습니다.',
    'screenshot': '실행 결과 화면이 아직 없습니다.',
}

def text(value):
    return str(value or '').strip()

def api_items(value):
    items = []
    for row in value or ():
        if isinstance(row, dict):
            name = text(row.get('name'))
            if not name:
                continue
            items.append({'name': name, 'kind': text(row.get('kind')), 'meaning': text(row.get('meaning'))})
            continue
        if isinstance(row, (list, tuple)) and row:
            name = text(row[0])
            if not name:
                continue
            if len(row) == 1:
                items.append({'name': name, 'kind': '', 'meaning': ''})
            elif len(row) == 2:
                items.append({'name': name, 'kind': '', 'meaning': text(row[1])})
            else:
                items.append({'name': name, 'kind': text(row[1]), 'meaning': text(row[2])})
            continue
        name = text(row)
        if name:
            items.append({'name': name, 'kind': '', 'meaning': ''})
    return items

def as_youtube(value):
    if not value:
        return {}
    if isinstance(value, str):
        url = text(value)
        return {'url': url, 'title': ''} if url else {}
    url = text(value.get('url') if isinstance(value, dict) else '')
    if not url:
        return {}
    return {'url': url, 'title': text(value.get('title'))}

def as_screenshot(value):
    if not value:
        return {}
    if isinstance(value, str):
        src = text(value)
        return {'src': src, 'alt': '', 'caption': ''} if src else {}
    src = text(value.get('src') if isinstance(value, dict) else '')
    if not src:
        return {}
    return {'src': src, 'alt': text(value.get('alt')), 'caption': text(value.get('caption'))}

def attach(record, api=(), history='', youtube=None, screenshot=None):
    record['api'] = api_items(api)
    record['history'] = text(history)
    record['youtube'] = as_youtube(youtube)
    record['screenshot'] = as_screenshot(screenshot)
    return record

def youtube_ok(url):
    u = text(url).lower()
    return 'youtube.com/' in u or 'youtu.be/' in u

def asset_href(src, prefix='../../'):
    src = text(src)
    if not src:
        return ''
    if src.startswith(('http://', 'https://', '/', '../')):
        return src
    if src.startswith(('screenshots/', 'science/', 'mascot/')):
        return f'{prefix}assets/{src}'
    if '/' in src:
        return f'{prefix}assets/{src}'
    return f'{prefix}assets/screenshots/{src}'

def asset_path(src):
    src = text(src)
    if not src or src.startswith(('http://', 'https://')):
        return ''
    if src.startswith(('screenshots/', 'science/', 'mascot/')):
        return f'assets/{src}'
    if '/' in src:
        return f'assets/{src}'
    return f'assets/screenshots/{src}'

def page_api(lesson, examples):
    items = list(lesson.get('api') or [])
    seen = {item['name'] for item in items}
    for eid in lesson.get('examples') or ():
        for item in (examples.get(eid) or {}).get('api') or ():
            if item['name'] not in seen:
                items.append(item)
                seen.add(item['name'])
    return items

def page_history(lesson, examples):
    if lesson.get('history'):
        return lesson['history']
    for eid in lesson.get('examples') or ():
        value = (examples.get(eid) or {}).get('history') or ''
        if value:
            return value
    return ''

def page_youtube(lesson, examples):
    if lesson.get('youtube', {}).get('url'):
        return lesson['youtube']
    for eid in lesson.get('examples') or ():
        value = (examples.get(eid) or {}).get('youtube') or {}
        if value.get('url'):
            return value
    return {}

def page_shots(lesson, examples):
    shots = []
    own = lesson.get('screenshot') or {}
    if own.get('src'):
        shots.append({**own, 'from': 'lesson', 'id': lesson.get('id', ''), 'title': lesson.get('title', '')})
    for eid in lesson.get('examples') or ():
        example = examples.get(eid) or {}
        shot = example.get('screenshot') or {}
        if shot.get('src'):
            shots.append({**shot, 'from': 'example', 'id': eid, 'title': example.get('title', eid)})
    return shots

def _slot(kind, inner, filled):
    state = 'true' if filled else 'false'
    extra = '' if filled else ' content-slot--empty'
    return (
        f'<aside class="content-slot{extra}" data-slot="{kind}" data-filled="{state}">'
        f'<p class="eyebrow">{EYEBROWS[kind]}</p><h3>{TITLES[kind]}</h3>{inner}</aside>'
    )

def render_api(items):
    filled = bool(items)
    if not filled:
        return _slot('api', f'<p class="slot-empty">{EMPTY["api"]}</p>', False)
    rows = []
    for item in items:
        kind = f'<span class="api-kind">{esc(item["kind"])}</span>' if item.get('kind') else ''
        meaning = esc(item['meaning']) if item.get('meaning') else '설명이 아직 없습니다.'
        rows.append(f'<div><dt><code>{esc(item["name"])}</code>{kind}</dt><dd>{meaning}</dd></div>')
    return _slot('api', '<dl class="api-pre">'+''.join(rows)+'</dl>', True)

def render_history(value):
    if not value:
        return _slot('history', f'<p class="slot-empty">{EMPTY["history"]}</p>', False)
    return _slot('history', f'<p>{esc(value)}</p>', True)

def render_youtube(value):
    url = text((value or {}).get('url'))
    if not url:
        return _slot('youtube', f'<p class="slot-empty">{EMPTY["youtube"]}</p>', False)
    title = text((value or {}).get('title')) or url
    return _slot('youtube', f'<p><a href="{esc(url, True)}" target="_blank" rel="noopener">{esc(title)} ↗</a></p>', True)

def render_shots(shots, prefix='../../'):
    if not shots:
        return _slot('screenshot', f'<p class="slot-empty">{EMPTY["screenshot"]}</p>', False)
    cards = []
    for shot in shots:
        href = asset_href(shot['src'], prefix)
        alt = shot.get('alt') or shot.get('title') or '실행 결과 화면'
        caption = shot.get('caption') or shot.get('title') or ''
        label = f'<figcaption>{esc(caption)}</figcaption>' if caption else ''
        cards.append(
            f'<figure class="run-shot" data-shot-from="{esc(shot.get("from", ""))}" data-shot-id="{esc(shot.get("id", ""))}">'
            f'<a href="{esc(href, True)}" target="_blank" rel="noopener">'
            f'<img src="{esc(href, True)}" loading="lazy" alt="{esc(alt, True)}"></a>{label}</figure>'
        )
    return _slot('screenshot', '<div class="run-shots">'+''.join(cards)+'</div>', True)

def render_api_block(lesson, examples):
    return render_api(page_api(lesson, examples))

def render_tips(lesson, examples):
    return render_history(page_history(lesson, examples)) + render_youtube(page_youtube(lesson, examples))

def render_shot_block(lesson, examples, prefix='../../'):
    return render_shots(page_shots(lesson, examples), prefix)
