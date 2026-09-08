"""Actual example execution and screenshots. One toolkit per process."""
import sys,os,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/web'))
from content import examples
kind=sys.argv[1]
ns={'__name__':'__main__'}
output=ROOT/'web/assets/screenshots'/f'{kind}.png'
output.parent.mkdir(parents=True,exist_ok=True)
id={'tk':'hello-tk','ttk':'hello-ttk','pyside':'hello-pyside','pyqt':'hello-pyqt','wx':'hello-wx','kivy':'hello-kivy'}[kind]
src=examples[id]['files']['main.py']
if kind in ['tk','ttk']:
 src=src.replace('root.mainloop()','').replace('root = tk.Tk()','root = tk.Tk()\nroot.option_add("*Font", "{Noto Sans CJK KR} 11")')
 exec(src,ns)
 root=ns['root'];root.update()
 ns['entry'].insert(0,'파이썬');ns['greet']();root.update()
 assert ns['result'].cget('text')=='파이썬님, 안녕하세요!'
 subprocess.run(['import','-window',str(root.winfo_id()),str(output)],check=True)
 ns['reset']();assert ns['entry'].get()==''
 root.destroy()
elif kind in ['pyside','pyqt']:
 src=src.replace('sys.exit(app.exec())','')
 exec(src,ns)
 if kind=='pyside': from PySide6.QtGui import QFont
 else: from PyQt6.QtGui import QFont
 ns['app'].setFont(QFont('Noto Sans CJK KR',11))
 ns['entry'].setText('파이썬');ns['button'].click();ns['app'].processEvents()
 assert ns['result'].text()=='파이썬님, 안녕하세요!'
 ns['window'].grab().save(str(output))
 ns['clear_button'].click();assert ns['entry'].text()==''
 ns['window'].close()
elif kind=='wx':
 src=src.replace('app.MainLoop()','')
 exec(src,ns)
 import wx
 ns['entry'].SetValue('파이썬');ns['greet'](None)
 wx.Yield()
 assert ns['result'].GetLabel()=='파이썬님, 안녕하세요!'
 bitmap=wx.Bitmap(ns['window'].GetSize())
 memory=wx.MemoryDC(bitmap)
 memory.Blit(0,0,*ns['window'].GetSize(),wx.WindowDC(ns['window']),0,0)
 memory.SelectObject(wx.NullBitmap)
 bitmap.SaveFile(str(output),wx.BITMAP_TYPE_PNG)
 ns['reset'](None);assert ns['entry'].GetValue()==''
 ns['window'].Destroy()
else:
 src=src.replace('GreetingApp().run()','')
 exec(src,ns)
 from kivy.clock import Clock
 app=ns['GreetingApp']()
 def capture(dt):
  app.entry.text='Python';app.greet(None)
  Clock.schedule_once(save,0.3)
 def save(dt):
  assert app.result.text=='Hello, Python!'
  generated=ns['Window'].screenshot(name=str(output))
  if generated and Path(generated)!=output: Path(generated).replace(output)
  app.reset(None);assert app.entry.text==''
  app.stop()
 Clock.schedule_once(capture,0.5)
 app.run()
print('PASS',kind,output)
