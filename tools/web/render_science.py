"""Regenerate scientific figures from the shipped examples (optional build step)."""
from pathlib import Path
import os,sys,subprocess,shutil
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from content import examples
import later_units
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLBACKEND='Agg')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
OUTPUT=ROOT/'web/assets/science';OUTPUT.mkdir(exist_ok=True)
for id in ['ml-chart','ml-cluster','ml-learning-curve','cv-io','cv-filters','cv-perspective','cv-features','cv-skimage','ml-seaborn']:
 work=ROOT/'.web-build/science-results'/id;work.mkdir(parents=True,exist_ok=True)
 e=examples[id]
 for name,source in e['files'].items():(work/name).write_text(source)
 p=subprocess.run([sys.executable,'main.py'],cwd=work,capture_output=True,text=True,timeout=90)
 assert p.returncode==0,(id,p.stderr)
 print('Executed:',id)
 if id.startswith('ml-') and id!='ml-seaborn':
  source=next(work.glob('*.png'));shutil.copy2(source,OUTPUT/(id+'.png'))
 if id=='cv-skimage':shutil.copy2(work/'sobel.png',OUTPUT/'cv-sobel.png')
 if id=='cv-io':
  paths=[('scene.png','Original'),('result/gray.png','Grayscale'),('result/small.png','Resized'),('result/rotated.png','Rotation')]
 elif id=='cv-filters':paths=[('scene.png','Original'),('result/gaussian.png','Gaussian blur'),('result/canny.png','Canny edges'),('result/fixed.png','Fixed threshold'),('result/otsu.png','Otsu'),('result/adaptive.png','Adaptive')]
 elif id=='cv-features':paths=[('scene.png','Original'),('result/edges.png','Edges'),('result/corners.png','Corners'),('result/contours.png','Contours')]
 elif id=='cv-perspective':paths=[('scene.png','Original'),('result/rectified.png','Perspective transform')]
 else:continue
 fig,axes=plt.subplots(1 if len(paths)<=4 else 2,min(4,len(paths)) if len(paths)<=4 else 3,figsize=(12,3 if len(paths)<=4 else 6))
 for ax,(name,title) in zip(axes.flat,paths):
  with Image.open(work/name) as img:
   ax.imshow(img,cmap='gray',vmin=0,vmax=255)
  ax.set_title(title);ax.axis('off')
 fig.tight_layout();fig.savefig(OUTPUT/(id+'.png'),dpi=140);plt.close(fig)
print('Saved scientific figures:',OUTPUT)
