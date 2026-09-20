from pathlib import Path
import json,hashlib,os,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PREV=ROOT/'research/fly-t4t5-boundary'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 return h.hexdigest()
def write(name,data):
 p=HERE/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def read(name):return json.loads((HERE/name).read_text())
def firewall():
 log=[]
 def hook(event,args):
  if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
  p=Path(os.fsdecode(args[0])).resolve()
  if not p.is_relative_to(ROOT):return
  if p.is_relative_to(ROOT/'.local/fly-stage1-venv') and 'site-packages' in p.parts:return
  if not p.is_relative_to(HERE):raise PermissionError('Non-study input blocked: '+str(p))
  mode=args[1]
  if isinstance(mode,str) and any(x in mode for x in 'wax'):return
  if p.name.startswith('STAGE4_'):raise PermissionError('Post-freeze audit is not estimation input')
  log.append(str(p.relative_to(HERE)))
 sys.addaudithook(hook);return log
