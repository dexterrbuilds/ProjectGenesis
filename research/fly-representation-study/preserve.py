"""Read-only source preservation, never imports the application or old models."""
import argparse,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parent.parent
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 f=H/'FROZEN_BEFORE.json'
 if a.check:
  m=json.loads(f.read_text())
  for path,digest in m.items():assert sha(ROOT/path)==digest,path
  print(json.dumps({'protected_files_unchanged':len(m)}));return
 assert not f.exists()
 old=json.loads((ROOT/'research/fly-physiology-study/FROZEN_BEFORE.json').read_text())
 for path,digest in old.items():assert sha(ROOT/path)==digest,path
 for x in (ROOT/'research/fly-physiology-study').rglob('*'):
  if x.is_file() and '__pycache__' not in x.parts:old[str(x.relative_to(ROOT))]=sha(x)
 f.write_text(json.dumps(old,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'protected_files':len(old)}))
if __name__=='__main__':main()
