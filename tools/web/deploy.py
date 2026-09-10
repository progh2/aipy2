"""Publish only the classroom site and its generators; never upload original documents."""
from pathlib import Path
import subprocess,shutil,json
ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'.web-build/publish'
REPO='https://github.com/progh2/aipy2.git'
def run(*args,cwd=ROOT):subprocess.run(args,cwd=cwd,check=True)
run('python3','tools/web/build.py');run('python3','tools/web/verify.py')
if not (TARGET/'.git').exists():
 TARGET.parent.mkdir(exist_ok=True)
 run('git','clone',REPO,str(TARGET))
else:
 actual=subprocess.check_output(['git','remote','get-url','origin'],cwd=TARGET,text=True).strip()
 assert actual==REPO,'Unexpected deployment remote'
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=TARGET,text=True).strip(),'Deployment checkout has pending changes'
 run('git','pull','--ff-only',cwd=TARGET)
OWNED=['web','tools/web','.github/workflows','firebase','docs','README.md']
for rel in OWNED:
 source_root=ROOT/rel
 if source_root.is_file():
  shutil.copy2(source_root,TARGET/rel);continue
 destination=TARGET/rel
 destination.mkdir(parents=True,exist_ok=True)
 # Copy maintained files without deleting anything outside these owned paths.
 for source in source_root.rglob('*'):
  if not source.is_file() or '__pycache__' in source.parts:continue
  target=destination/source.relative_to(source_root)
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
run('git','add','web','tools/web','.github/workflows/pages.yml','firebase','docs','README.md',cwd=TARGET)
changed=subprocess.run(['git','diff','--cached','--quiet'],cwd=TARGET).returncode
if changed:
 if subprocess.run(['git','config','--get','user.email'],cwd=TARGET,stdout=subprocess.DEVNULL).returncode:
  account=json.loads(subprocess.check_output(['gh','api','user'],text=True))
  run('git','config','user.name',account['login'],cwd=TARGET)
  run('git','config','user.email',f"{account['id']}+{account['login']}@users.noreply.github.com",cwd=TARGET)
 run('git','commit','-m','Update Python classroom lessons and practice',cwd=TARGET)
 run('git','push','origin','main',cwd=TARGET)
print('Deployment: https://github.com/progh2/aipy2/actions')
