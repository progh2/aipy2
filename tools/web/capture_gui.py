"""Capture real GUI example windows to web/assets/screenshots/.

One toolkit per process (Qt/Tk/Kivy must not share a process).

Usage:
  python tools/web/capture_gui.py tk                 # hello-tk → tk.png (gallery)
  python tools/web/capture_gui.py hello-tk           # same
  python tools/web/capture_gui.py widgets-tk         # widgets-tk.png
  python tools/web/capture_gui.py --unit2            # dedicated Unit II shots
  python tools/web/capture_gui.py --list

Needs a display (Xvfb is fine), python3-tk, ImageMagick `import` for Tk,
PySide6 plus libEGL/libGL for Qt, wxPython for wx appendix shots, and Kivy
for Kivy appendix shots. Gallery hello shots keep toolkit filenames.
Qt: `apt install libegl1` if import fails on libEGL.so.1.
"""
import os, re, sys, tempfile, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHOT_DIR = ROOT / 'web/assets/screenshots'
sys.path.insert(0, str(Path(__file__).parent))
from content import examples
import unit2_shots

HELLO_KIND = {
    'tk': 'hello-tk', 'ttk': 'hello-ttk', 'pyside': 'hello-pyside',
    'pyqt': 'hello-pyqt', 'wx': 'hello-wx', 'kivy': 'hello-kivy',
}
FONT = 'Noto Sans CJK KR'
MEMO = '오늘 실습 메모\n1. 열기·저장을 시험한다.\n2. 한글 UTF-8이 유지되는지 확인한다.\n'


def toolkit_of(src):
    low = src.lower()
    if 'from kivy' in low or 'import kivy' in low:
        return 'kivy'
    if 'import wx' in src or 'from wx' in src:
        return 'wx'
    if 'PyQt6' in src:
        return 'pyqt'
    if 'PySide6' in src:
        return 'pyside'
    if 'tkinter' in src:
        return 'tk'
    return None


def strip_loop(src):
    for old in (
        'root.mainloop()', 'window.mainloop()',
        'sys.exit(app.exec())', 'app.exec()',
        'app.MainLoop()',
    ):
        src = src.replace(old, '')
    return re.sub(r'\w+App\(\)\.run\(\)', '', src)


def inject_tk_font(src):
    for name in ('root', 'window'):
        needle = f'{name} = tk.Tk()'
        idx = src.find(needle)
        if idx == -1:
            continue
        line_start = src.rfind('\n', 0, idx) + 1
        indent = src[line_start:idx]
        extra = f'\n{indent}{name}.option_add("*Font", "{{{FONT}}} 11")'
        return src[:idx] + needle + extra + src[idx + len(needle):]
    return src


KIVY_FONT_CANDIDATES = (
    Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
    Path('/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'),
)


def write_work(example):
    work = Path(tempfile.mkdtemp(prefix=f'aipy-cap-{example["id"]}-'))
    for name, text in example['files'].items():
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    if 'kivy' in example['id'] or 'from kivy' in example['files'].get('main.py', ''):
        for font in KIVY_FONT_CANDIDATES:
            if font.is_file():
                (work / 'NotoSansKR.ttf').write_bytes(font.read_bytes())
                break
    return work


def tk_root(ns):
    for key in ('root', 'window'):
        if ns.get(key) is not None:
            return ns[key]
    app = ns.get('app')
    if app is not None and getattr(app, 'root', None) is not None:
        return app.root
    import tkinter as tk
    return tk._default_root


def wx_window(ns):
    if ns.get('window') is not None:
        return ns['window']
    import wx
    frames = [w for w in wx.GetTopLevelWindows() if w]
    if not frames:
        raise RuntimeError('no wx Frame')
    return frames[0]


def wx_ui_font():
    import wx
    for name in (FONT, 'NanumGothic', '나눔고딕', 'WenQuanYi Micro Hei', 'Noto Sans CJK JP'):
        font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, name)
        if font.IsOk() and font.GetFaceName():
            return font
    return wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)


def apply_wx_font(widget, font):
    widget.SetFont(font)
    for child in widget.GetChildren():
        apply_wx_font(child, font)


def capture_wx(window, output):
    import wx
    apply_wx_font(window, wx_ui_font())
    window.Show()
    try:
        window.Raise()
    except Exception:
        pass
    width, height = window.GetSize()
    if width > 900 or height > 700 or width < 120 or height < 80:
        window.SetSize((520, 280))
    window.Layout()
    window.Update()
    wx.Yield()
    time.sleep(0.25)
    wx.Yield()
    width, height = window.GetClientSize()
    if width < 80 or height < 40:
        width, height = 520, 260
        window.SetClientSize((width, height))
        window.Update()
        wx.Yield()
        width, height = window.GetClientSize()
    bitmap = wx.Bitmap(width, height)
    memory = wx.MemoryDC(bitmap)
    memory.Blit(0, 0, width, height, wx.ClientDC(window), 0, 0)
    memory.SelectObject(wx.NullBitmap)
    ok = bitmap.SaveFile(str(output), wx.BITMAP_TYPE_PNG)
    assert ok and output.is_file() and output.stat().st_size > 1000, (output, output.stat().st_size if output.is_file() else 0)
    # A desktop wallpaper blit is usually hundreds of KB; GUI shots stay small.
    assert output.stat().st_size < 80000, ('wx shot too large', output, output.stat().st_size)


def qt_window(ns):
    if ns.get('window') is not None:
        return ns['window']
    app = ns.get('app')
    if app is None:
        if 'PyQt6' in ns.get('__src__', ''):
            from PyQt6.QtWidgets import QApplication
        else:
            from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
    widgets = [w for w in app.topLevelWidgets() if w.isWindow()]
    return widgets[0]


def capture_tk(root, output):
    root.update_idletasks()
    root.deiconify()
    root.lift()
    try:
        root.wait_visibility()
    except Exception:
        pass
    root.update()
    time.sleep(0.15)
    root.update()
    wid = hex(int(root.winfo_id()))
    try:
        subprocess.run(['import', '-window', str(root.winfo_id()), str(output)], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        xwd = output.with_suffix('.xwd')
        subprocess.run(['xwd', '-silent', '-id', wid, '-out', str(xwd)], check=True)
        subprocess.run(['convert', str(xwd), str(output)], check=True)
        xwd.unlink(missing_ok=True)
    assert output.is_file() and output.stat().st_size > 1000, output


def capture_qt(window, app, output):
    app.processEvents()
    time.sleep(0.15)
    app.processEvents()
    ok = window.grab().save(str(output))
    assert ok and output.is_file() and output.stat().st_size > 1000, output


def demo_noop(ns):
    return


def demo_label_entry(ns):
    ns['entry'].insert(0, '민지')
    ns['show_name']()


def demo_choice(ns):
    ns['done'].set(True)
    ns['show_choice']()


def demo_list_canvas(ns):
    ns['listbox'].selection_set(2)
    ns['show_pick']()


def demo_bind(ns):
    ns['entry'].insert(0, '파이썬')
    ns['greet']()


def demo_after(ns):
    ns['tick'](0)


def demo_review(ns):
    ns['say_hello']()


def demo_project_button(ns):
    ns['show']()


def demo_project_tk(ns):
    ns['run_task']()


def demo_pyside_form(ns):
    ns['entry'].setText('민지')
    ns['done'].setChecked(True)
    ns['show_choice']()


def demo_pyside_signal(ns):
    ns['entry'].setText('파이썬')
    ns['greet']()


def demo_pyside_ui(ns):
    ns['window'].nameEdit.setText('파이썬')
    ns['greet']()


def demo_project_pyside(ns):
    ns['window'].run_task()


def demo_memo_tk(ns):
    text = ns.get('text_area') or ns.get('text')
    if text is None and ns.get('app') is not None:
        text = getattr(ns['app'], 'text', None)
    if text is None:
        return
    text.insert('1.0', MEMO)
    app = ns.get('app')
    if app is not None and hasattr(app, 'refresh'):
        app.dirty = True
        app.refresh()


def demo_memo_qt(ns):
    editor = getattr(ns['window'], 'editor', None)
    if editor is not None:
        editor.setPlainText(MEMO)


def demo_wx_label_entry(ns):
    ns['entry'].SetValue('민지')
    ns['show_name'](None)


def demo_wx_choice(ns):
    ns['done'].SetValue(True)
    ns['show_choice'](None)


def demo_wx_events(ns):
    ns['entry'].SetValue('파이썬')
    ns['greet'](None)


def demo_wx_memo(ns):
    editor = ns.get('editor')
    if editor is None and ns.get('window') is not None:
        editor = getattr(ns['window'], 'editor', None)
    if editor is not None:
        editor.SetValue(MEMO)


def demo_wx_project(ns):
    ns['window'].entry.SetValue('6')
    ns['window'].run_task(None)


def kivy_app_class(ns):
    from kivy.app import App
    for value in ns.values():
        if isinstance(value, type) and issubclass(value, App) and value is not App:
            return value
    raise RuntimeError('no Kivy App class')


def demo_kivy_label_entry(app, ns):
    app.entry.text = 'Minji'
    app.show_name(None)


def demo_kivy_choice(app, ns):
    app.done.active = True
    app.show_choice(None)


def demo_kivy_events(app, ns):
    app.entry.text = 'Python'
    app.greet(None)


def demo_kivy_memo(app, ns):
    app.editor.text = 'Practice notes\n1. Try save and open.\n2. Check UTF-8 stays.\n'


def demo_kivy_project(app, ns):
    app.entry.text = '6'
    app.mode.text = 'Dice'
    app.run_task(None)


def capture_kivy(ns, output, demo=None):
    from kivy.clock import Clock
    from kivy.core.window import Window
    app = kivy_app_class(ns)()

    def after_start(dt):
        if demo:
            demo(app, ns)
        Clock.schedule_once(save, 0.4)

    def save(dt):
        generated = Window.screenshot(name=str(output))
        if generated and Path(generated) != output:
            Path(generated).replace(output)
        assert output.is_file() and output.stat().st_size > 1000, (output, output.stat().st_size if output.is_file() else 0)
        app.stop()

    Clock.schedule_once(after_start, 0.6)
    app.run()


DEMO = {
    'widgets-label-entry-tk': demo_label_entry,
    'widgets-choice-tk': demo_choice,
    'widgets-list-canvas-tk': demo_list_canvas,
    'events-bind-tk': demo_bind,
    'events-after-tk': demo_after,
    'review-scratch-tk': demo_review,
    'project-button-tk': demo_project_button,
    'project-tk': demo_project_tk,
    'widgets-pyside-form': demo_pyside_form,
    'events-pyside-signal': demo_pyside_signal,
    'pyside-ui-file': demo_pyside_ui,
    'project-pyside': demo_project_pyside,
    'memo-window-tk': demo_memo_tk,
    'memo-files-tk': demo_memo_tk,
    'memo-tk': demo_memo_tk,
    'memo-plus-tk': demo_memo_tk,
    'memo-pyside': demo_memo_qt,
    'memo-plus-pyside': demo_memo_qt,
    'widgets-label-entry-wx': demo_wx_label_entry,
    'widgets-choice-wx': demo_wx_choice,
    'events-wx': demo_wx_events,
    'memo-window-wx': demo_wx_memo,
    'memo-wx': demo_wx_memo,
    'project-wx': demo_wx_project,
    'widgets-label-entry-kivy': demo_kivy_label_entry,
    'widgets-choice-kivy': demo_kivy_choice,
    'events-kivy': demo_kivy_events,
    'memo-window-kivy': demo_kivy_memo,
    'memo-kivy': demo_kivy_memo,
    'project-kivy': demo_kivy_project,
}


def capture_hello(kind):
    """Original greeting-app path. Output stays {kind}.png for the gallery."""
    output = SHOT_DIR / f'{kind}.png'
    output.parent.mkdir(parents=True, exist_ok=True)
    eid = HELLO_KIND[kind]
    ns = {'__name__': '__main__'}
    src = examples[eid]['files']['main.py']
    if kind in ('tk', 'ttk'):
        src = src.replace('root.mainloop()', '')
        src = src.replace('root = tk.Tk()', 'root = tk.Tk()\nroot.option_add("*Font", "{Noto Sans CJK KR} 11")')
        exec(src, ns)
        root = ns['root']
        root.update()
        ns['entry'].insert(0, '파이썬')
        ns['greet']()
        root.update()
        assert ns['result'].cget('text') == '파이썬님, 안녕하세요!'
        capture_tk(root, output)
        ns['reset']()
        assert ns['entry'].get() == ''
        root.destroy()
    elif kind in ('pyside', 'pyqt'):
        src = src.replace('sys.exit(app.exec())', '')
        exec(src, ns)
        if kind == 'pyside':
            from PySide6.QtGui import QFont
        else:
            from PyQt6.QtGui import QFont
        ns['app'].setFont(QFont(FONT, 11))
        ns['entry'].setText('파이썬')
        ns['button'].click()
        ns['app'].processEvents()
        assert ns['result'].text() == '파이썬님, 안녕하세요!'
        capture_qt(ns['window'], ns['app'], output)
        ns['clear_button'].click()
        assert ns['entry'].text() == ''
        ns['window'].close()
    elif kind == 'wx':
        src = src.replace('app.MainLoop()', '')
        exec(src, ns)
        import wx
        ns['entry'].SetValue('파이썬')
        ns['greet'](None)
        wx.Yield()
        assert ns['result'].GetLabel() == '파이썬님, 안녕하세요!'
        bitmap = wx.Bitmap(ns['window'].GetSize())
        memory = wx.MemoryDC(bitmap)
        memory.Blit(0, 0, *ns['window'].GetSize(), wx.WindowDC(ns['window']), 0, 0)
        memory.SelectObject(wx.NullBitmap)
        bitmap.SaveFile(str(output), wx.BITMAP_TYPE_PNG)
        ns['reset'](None)
        assert ns['entry'].GetValue() == ''
        ns['window'].Destroy()
    else:
        src = src.replace('GreetingApp().run()', '')
        exec(src, ns)
        from kivy.clock import Clock
        app = ns['GreetingApp']()

        def capture(dt):
            app.entry.text = 'Python'
            app.greet(None)
            Clock.schedule_once(save, 0.3)

        def save(dt):
            assert app.result.text == 'Hello, Python!'
            generated = ns['Window'].screenshot(name=str(output))
            if generated and Path(generated) != output:
                Path(generated).replace(output)
            app.reset(None)
            assert app.entry.text == ''
            app.stop()

        Clock.schedule_once(capture, 0.5)
        app.run()
    print('PASS', kind, output)


def capture_example(eid):
    example = examples[eid]
    src = example['files']['main.py']
    kind = toolkit_of(src)
    if kind is None:
        raise SystemExit(f'{eid}: not a GUI example')
    if kind in HELLO_KIND and eid in HELLO_KIND.values():
        return capture_hello(next(k for k, v in HELLO_KIND.items() if v == eid))
    output = SHOT_DIR / unit2_shots.output_name(eid)
    output.parent.mkdir(parents=True, exist_ok=True)
    work = write_work(example)
    cwd = os.getcwd()
    os.chdir(work)
    sys.path.insert(0, str(work))
    ns = {'__name__': '__main__', '__file__': str(work / example['entry']), '__src__': src}
    try:
        prepared = strip_loop(src)
        if kind == 'tk':
            prepared = inject_tk_font(prepared)
        exec(prepared, ns)
        if kind == 'kivy':
            capture_kivy(ns, output, DEMO.get(eid))
        else:
            DEMO.get(eid, demo_noop)(ns)
            if kind == 'tk':
                root = tk_root(ns)
                capture_tk(root, output)
                root.destroy()
            elif kind in ('pyside', 'pyqt'):
                if kind == 'pyside':
                    from PySide6.QtGui import QFont
                else:
                    from PyQt6.QtGui import QFont
                app = ns.get('app')
                window = qt_window(ns)
                app.setFont(QFont(FONT, 11))
                window.show()
                capture_qt(window, app, output)
                window.close()
            elif kind == 'wx':
                import wx
                window = wx_window(ns)
                wx.Yield()
                capture_wx(window, output)
                window.Destroy()
            else:
                raise SystemExit(f'{eid}: unsupported GUI toolkit')
    finally:
        sys.path = [p for p in sys.path if p != str(work)]
        os.chdir(cwd)
    print('PASS', eid, output)


def run_unit2():
    failed = []
    for eid in unit2_shots.capture_ids():
        cmd = [sys.executable, str(Path(__file__)), eid]
        if not os.environ.get('DISPLAY'):
            cmd = ['xvfb-run', '-a', '-s', '-screen 0 1280x800x24'] + cmd
        result = subprocess.run(cmd)
        if result.returncode != 0:
            failed.append(eid)
    if failed:
        raise SystemExit('FAILED: ' + ', '.join(failed))
    print('PASS unit2', len(unit2_shots.capture_ids()), 'shots')


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return
    if argv[0] == '--list':
        print('hello:', ' '.join(HELLO_KIND))
        print('unit2:', ' '.join(unit2_shots.capture_ids()))
        return
    if argv[0] == '--unit2':
        run_unit2()
        return
    target = argv[0]
    if target in HELLO_KIND:
        capture_hello(target)
        return
    if target in examples:
        capture_example(target)
        return
    raise SystemExit(f'unknown target: {target}')


if __name__ == '__main__':
    main(sys.argv[1:])
