from pathlib import Path
import json,hashlib,datetime
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PRIOR=ROOT/'research/fly-upwin-route-evidence'
def load(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4194304):h.update(b)
 return h.hexdigest()
def write(n,v):
 p=HERE/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
