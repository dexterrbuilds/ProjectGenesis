from pathlib import Path
import json,hashlib,sys,os
HERE=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 return h.hexdigest()
def write(name,data):
 (HERE/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def firewall(mode):
 """Reject any old study input. Optimizer additionally cannot read test arrays/raw data."""
 log=[]
 def audit(event,args):
  if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
  p=Path(os.fsdecode(args[0])).resolve()
  workspace=next((a for a in HERE.parents if (a/'core').is_dir() and (a/'research').is_dir()),HERE.parent.parent)
  if not p.is_relative_to(workspace):return
  if 'site-packages' in p.parts and p.is_relative_to(workspace/'.local/fly-stage1-venv'):return
  if not p.is_relative_to(HERE):raise PermissionError('Frozen workspace input blocked: '+str(p))
  readmode=args[1]
  if isinstance(readmode,str) and any(x in readmode for x in 'wax'):return
  allowed={'common.py','models.py','fit.py','CONDITIONAL_PROTOCOL.md','FITS.json','TRAINING_PROFILE.json','FIT_FREEZE.json'}
  training=p.parent==HERE/'processed' and p.name.startswith('cell_') and p.name.endswith('_train.npz')
  if mode=='fit' and not (training or (p.parent==HERE and p.name in allowed)):raise PermissionError('Non-training input blocked: '+str(p))
  log.append(str(p.relative_to(HERE)))
 sys.addaudithook(audit)
 return log
