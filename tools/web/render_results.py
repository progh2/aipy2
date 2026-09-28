"""실제 실행 결과(표준 출력 텍스트·이미지)를 캡처해 tools/web/results.json에 기록한다 (#132).

재실행 가능. 교과서 원본 파일에 의존하지 않고 content.py의 examples 정의만 쓴다.
build.py는 이 매니페스트와 web/assets/results/의 이미지가 있으면 ex-*.html의
코드 아래에 "실행 결과" 섹션을 붙인다. 없으면 조용히 생략한다.

사용:
  /tmp/mlenv/bin/python tools/web/render_results.py            # 전체 다시 생성
  /tmp/mlenv/bin/python tools/web/render_results.py --list     # 대상 id만 출력
  /tmp/mlenv/bin/python tools/web/render_results.py ml-clustering hello-tk  # 일부만

tkinter 캡처(단원II 튜토리얼 마지막 단계)는 xvfb-run + 시스템 python3 서브프로세스로
실행한다(mlenv에는 tkinter가 없을 수 있고, 이 프로세스에는 DISPLAY가 없다).
  python3 tools/web/render_results.py --tk-capture <code.py> <out.png>
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / 'web'
RESULT_DIR = WEB / 'assets/results'
MANIFEST = Path(__file__).parent / 'results.json'
SYS_PY = shutil.which('python3') or sys.executable
MLENV_PY = '/tmp/mlenv/bin/python' if Path('/tmp/mlenv/bin/python').exists() else sys.executable
FONT = 'Noto Sans CJK KR'

sys.path.insert(0, str(Path(__file__).parent))


# 튜토리얼 완성 코드는 빈 상태로도 뜨지만, 채운 상태를 보여 주는 편이 학생에게
# 더 유용하다. 알려진 변수·함수 이름만 건드리는 얕은 데모(없으면 조용히 건너뜀).
def _tk_demo(tid, ns):
    try:
        if tid == 'widgets-greeting':
            ns['name_entry'].insert(0, '민지')
            ns['greet']()
        elif tid == 'events-click-counter':
            ns['click'](); ns['click'](); ns['click']()
        elif tid == 'memo-steps':
            ns['text_area'].insert('1.0', MEMO)
        elif tid == 'project-helper-app':
            ns['task_entry'].insert(0, '수학 숙제')
            ns['add_task']()
            ns['task_entry'].insert(0, '체육복 챙기기')
            ns['add_task']()
    except Exception as e:
        print('  [demo skip]', tid, e)


MEMO = '오늘 실습 메모\n1. 열기·저장을 시험한다.\n2. 한글 UTF-8이 유지되는지 확인한다.\n'


# --- tkinter 창 캡처(서브프로세스 진입점) ------------------------------------
def _tk_capture_main(code_path, out_path, tid=None):
    """xvfb-run 아래에서 실행된다. code_path의 코드를 mainloop 직전까지 돌리고
    창을 캡처한다."""
    src = Path(code_path).read_text()
    for old in ('root.mainloop()', 'window.mainloop()'):
        src = src.replace(old, '')
    for name in ('root', 'window'):
        needle = f'{name} = tk.Tk()'
        idx = src.find(needle)
        if idx != -1:
            line_start = src.rfind('\n', 0, idx) + 1
            indent = src[line_start:idx]
            src = src[:idx] + needle + f'\n{indent}{name}.option_add("*Font", "{{{FONT}}} 11")' + src[idx + len(needle):]
            break
    ns = {'__name__': '__main__'}
    exec(src, ns)
    root = ns.get('root') or ns.get('window')
    if tid:
        _tk_demo(tid, ns)
    import time
    root.update_idletasks(); root.deiconify(); root.lift()
    try: root.wait_visibility()
    except Exception: pass
    root.update(); time.sleep(0.15); root.update()
    out = Path(out_path)
    try:
        subprocess.run(['import', '-window', str(root.winfo_id()), str(out)], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        wid = hex(int(root.winfo_id()))
        xwd = out.with_suffix('.xwd')
        subprocess.run(['xwd', '-silent', '-id', wid, '-out', str(xwd)], check=True)
        subprocess.run(['convert', str(xwd), str(out)], check=True)
        xwd.unlink(missing_ok=True)
    assert out.is_file() and out.stat().st_size > 300, out
    root.destroy()
    print('TK_CAPTURE_OK', out)


def capture_tk_code(code, dest_webp, label):
    """code(전체 실행 가능한 tkinter 스크립트)를 xvfb-run 서브프로세스로 캡처해
    dest_webp(webp)로 저장한다. 실패하면 None을 반환하고 경고를 출력한다."""
    with tempfile.TemporaryDirectory(prefix='aipy-tkcap-') as tmp:
        code_path = Path(tmp) / 'snippet.py'
        code_path.write_text(code)
        png_path = Path(tmp) / 'shot.png'
        cmd = ['xvfb-run', '-a', '-s', '-screen 0 1280x800x24', SYS_PY, str(Path(__file__)),
               '--tk-capture', str(code_path), str(png_path), label]
        if os.environ.get('DISPLAY'):
            cmd = [SYS_PY, str(Path(__file__)), '--tk-capture', str(code_path), str(png_path), label]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        if proc.returncode != 0 or not png_path.is_file():
            print(f'  [skip] tk capture 실패: {label}\n{proc.stderr[-800:]}')
            return None
        to_webp(png_path, dest_webp)
        return dest_webp


# --- 콘솔 실행 -----------------------------------------------------------
def run_console(files, entry, stdin, py, timeout=25):
    """files(딕셔너리 name->source)를 임시 폴더에 써서 entry를 실행하고
    (stdout, 새로 생긴 이미지 파일 목록)을 돌려준다. 실패하면 (None, [])."""
    with tempfile.TemporaryDirectory(prefix='aipy-run-') as tmp:
        work = Path(tmp)
        for name, source in files.items():
            p = work / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(source)
        before = set(work.rglob('*.png'))
        stdin_text = (stdin or '').strip()
        stdin_text = (stdin_text + '\n') if stdin_text else ''
        try:
            proc = subprocess.run([py, entry], cwd=work, input=stdin_text,
                                   capture_output=True, text=True, timeout=timeout,
                                   env={**os.environ, 'MPLBACKEND': 'Agg', 'PYTHONIOENCODING': 'utf-8'})
        except subprocess.TimeoutExpired:
            print(f'  [skip] 시간 초과: {entry}')
            return None, []
        if proc.returncode != 0:
            print(f'  [skip] 실행 실패({proc.returncode}): {entry}\n{proc.stderr[-600:]}')
            return None, []
        after = set(work.rglob('*.png')) | set(work.rglob('*.jpg'))
        new_imgs = sorted(p for p in after if p not in before)
        # 이미지는 임시 폴더가 사라지기 전에 바로 옮겨 담아야 하므로 바이트로 반환
        img_bytes = [(p.name, p.read_bytes()) for p in new_imgs]
        stdout = proc.stdout.replace(str(work), '내 프로젝트 폴더')
        return stdout, img_bytes


def to_webp(src, dest, max_width=900, quality=80):
    from PIL import Image
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert('RGB') if im.mode in ('P', 'RGBA') else im
        if im.width > max_width:
            ratio = max_width / im.width
            im = im.resize((max_width, max(1, int(im.height * ratio))))
        im.save(dest, 'WEBP', quality=quality)


def clean_text(stdout, limit=2500):
    text = (stdout or '').rstrip('\n')
    if not text.strip():
        return ''
    if len(text) > limit:
        text = text[:limit] + '\n…(이하 생략)'
    return text


# --- 예제 처리 -------------------------------------------------------------
def process_example(eid, ex, manifest):
    files = ex['files']
    entry = ex.get('entry') or 'main.py'
    needs_ml = bool((files.get('requirements.txt') or '').strip())
    py = MLENV_PY if needs_ml else SYS_PY
    print(f'- {eid} ({py.split("/")[-2] if "mlenv" in py else "system"})')
    stdout, img_bytes = run_console(files, entry, ex.get('stdin', ''), py)
    if stdout is None and not img_bytes:
        return
    entry_out = {}
    text = clean_text(stdout)
    stdin_lines = [l for l in (ex.get('stdin') or '').splitlines() if l.strip()]
    if text and stdin_lines:
        # input()은 파이프 실행 시 입력값을 화면에 그대로 보여 주지 않으므로(터미널
        # 에코 없음), 무엇을 넣었는지 실행 결과 아래에 덧붙여 학생이 헷갈리지 않게 한다.
        text += '\n\n(입력한 값: ' + ', '.join(stdin_lines) + ')'
    if text:
        entry_out['text'] = text
    imgs = []
    for i, (name, data) in enumerate(img_bytes, 1):
        tmp_src = RESULT_DIR / f'.__tmp_{eid}_{i}.png'
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        tmp_src.write_bytes(data)
        dest = RESULT_DIR / f'{eid}-{i}.webp'
        to_webp(tmp_src, dest)
        tmp_src.unlink()
        imgs.append(f'assets/results/{eid}-{i}.webp')
    if imgs:
        entry_out['img'] = imgs
    if entry_out:
        manifest[eid] = entry_out


# --- 단원II 예제 자체의 실행 화면 ------------------------------------------
# hello-tk는 content.py에 직접 screenshots=[tk.png]가 박혀 있어 ex-hello-tk.html에
# 이미 "실행하면 이렇게 보여요" 섹션으로 나온다(#72). 반면 widgets-tk/layout-tk/
# memo-tk는 같은 파이프라인(capture_gui.py --unit2)으로 web/assets/screenshots/에
# PNG가 이미 있는데도, 2·3단원을 PPT 슬라이드 체계로 옮긴 #131 이후 그 슬롯을 채우던
# unit2_shots.apply()를 더는 호출하지 않아 화면에 붙지 않는 채로 남아 있었다(사각지대).
# 새로 캡처하지 않고 기존 PNG를 그대로 재사용해 결과 매니페스트에 채운다.
LEGACY_GUI_SHOTS = {
    'widgets-tk': 'widgets-tk.png',
    'layout-tk': 'layout-tk.png',
    'memo-tk': 'memo-tk.png',
}


def process_legacy_gui_shots(manifest):
    src_dir = WEB / 'assets/screenshots'
    for eid, fname in LEGACY_GUI_SHOTS.items():
        src = src_dir / fname
        if not src.is_file():
            print(f'  [skip] 기존 스크린샷 없음: {eid} ({fname})')
            continue
        print(f'- legacy-gui-shot {eid}')
        dest = RESULT_DIR / f'{eid}-1.webp'
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        to_webp(src, dest)
        manifest[eid] = {'img': [f'assets/results/{eid}-1.webp']}


# --- 단원II 튜토리얼 마지막 단계(완성 코드) 캡처 -----------------------------
TK_TUTORIALS = ['widgets-greeting', 'layout-same-form', 'events-click-counter',
                 'memo-steps', 'project-helper-app']


def process_tk_tutorials(manifest, only=None):
    import deck_u2
    items_by_id = {}
    for lesson in deck_u2.LESSONS.values():
        for it in (lesson.get('practice') or []):
            if isinstance(it, dict) and it.get('kind') == 'tutorial':
                items_by_id[it['id']] = it
    for tid in TK_TUTORIALS:
        if only and tid not in only:
            continue
        item = items_by_id.get(tid)
        if not item:
            print(f'  [skip] 튜토리얼을 찾을 수 없음: {tid}')
            continue
        steps = item.get('steps') or []
        # 마지막으로 tk.Tk()+mainloop()를 모두 담은(=독립 실행 가능한) 단계를 "기반
        # 코드"로 찾는다. 그 뒤에 이어지는 단계(함수·버튼 추가 등, 예: project-helper-app
        # 처럼 "전체 코드" 단계가 따로 없는 튜토리얼)는 mainloop() 앞에 이어 붙인다.
        base_idx = None
        for i, s in enumerate(steps):
            code = s.get('code') or ''
            if 'mainloop()' in code and 'tk.Tk()' in code:
                base_idx = i
        if base_idx is None:
            print(f'  [skip] 완성 코드 단계를 찾지 못함: {tid}')
            continue
        final_code = steps[base_idx]['code']
        extra = [s['code'].strip() for s in steps[base_idx + 1:] if (s.get('code') or '').strip()]
        if extra:
            for mn in ('root.mainloop()', 'window.mainloop()'):
                if mn in final_code:
                    final_code = final_code.replace(mn, '\n\n'.join(extra) + '\n\n' + mn)
                    break
        print(f'- tk-tutorial {tid}')
        dest = RESULT_DIR / f'{tid}-1.webp'
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        ok = capture_tk_code(final_code, dest, tid)
        if ok:
            manifest[tid] = {'img': [f'assets/results/{tid}-1.webp']}


# --- 대상 id 수집 -----------------------------------------------------------
def collect_ids():
    from content import examples
    import later_units
    import deck_u2, deck_u3

    def practice_ids(deck):
        ids = []
        for lesson in deck.values():
            for it in (lesson.get('practice') or []):
                if isinstance(it, str):
                    ids.append(it)
        return list(dict.fromkeys(ids))

    from content import units
    unit1_ids = list(dict.fromkeys(e for l in units[1] for e in l['examples']))
    unit3_ids = practice_ids(deck_u3.LESSONS)
    cv_text_ids = ['cv-process-vs-vision', 'cv-use-fields', 'cv-human-vs-computer', 'cv-pixels',
                   'cv-shape-size', 'cv-bgr-rgb', 'cv-pipeline-steps', 'cv-plate-stages',
                   'cv-eval-criteria', 'cv-threshold-kinds', 'cv-feature-kinds', 'cv-haar-vs-id',
                   'cv-count', 'cv-scan-card', 'cv-pillow']
    return unit1_ids, unit3_ids, cv_text_ids


def main(argv):
    if argv[:1] == ['--tk-capture']:
        _tk_capture_main(argv[1], argv[2], argv[3] if len(argv) > 3 else None)
        return
    unit1_ids, unit3_ids, unit4_ids = collect_ids()
    if argv[:1] == ['--list']:
        print('unit1:', len(unit1_ids), unit1_ids)
        print('unit3:', len(unit3_ids), unit3_ids)
        print('unit4:', len(unit4_ids), unit4_ids)
        print('tk-tutorials:', TK_TUTORIALS)
        return

    from content import examples
    only = set(argv) if argv else None

    manifest = {}
    if MANIFEST.is_file():
        manifest = json.loads(MANIFEST.read_text())

    targets = unit1_ids + unit3_ids + unit4_ids
    for eid in targets:
        if only and eid not in only:
            continue
        process_example(eid, examples[eid], manifest)

    if not only or (only & set(LEGACY_GUI_SHOTS)):
        process_legacy_gui_shots(manifest)

    if not only or (only & set(TK_TUTORIALS)):
        process_tk_tutorials(manifest, only=only)

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    n_img = sum(len(v.get('img', [])) for v in manifest.values())
    n_text = sum(1 for v in manifest.values() if v.get('text'))
    print(f'\n완료: {len(manifest)}개 항목 (이미지 {n_img}장, 텍스트 {n_text}건) -> {MANIFEST}')


if __name__ == '__main__':
    main(sys.argv[1:])
