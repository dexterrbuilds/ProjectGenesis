"""Read-only hash comparison; does not import or execute research models."""
import hashlib,json
from pathlib import Path

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
frozen=json.load(open('outputs/awakening-preparation/FROZEN_BEFORE.json'))
failures=[p for p,h in frozen.items() if not Path(p).is_file() or sha(p)!=h]
previous={}
for name in ['completion-audit','foundation-repair','memory-pass']:
 base=Path('verification')/name
 manifest=json.load(open(base/'ARTIFACT_MANIFEST.json'))
 files=manifest['files']
 previous[name]=[p for p,h in files.items() if not (base/p).is_file() or sha(base/p)!=h]
result={'filesChecked':len(frozen),'mismatches':failures,'priorPackages':previous}
Path('verification/life-state-pass/preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
if failures or any(previous.values()):raise SystemExit(1)
