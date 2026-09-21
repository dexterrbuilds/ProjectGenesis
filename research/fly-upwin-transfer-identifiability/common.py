from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ROUTE=ROOT/'research/fly-upwin-route-evidence'
IDENTITY=ROOT/'research/fly-upwin-identity-mediation'
STAGE1=ROOT/'research/fly-stage1'
SPEC=ROOT/'research/genesis-brain-spec-v0.2'
def load(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4194304):h.update(b)
 return h.hexdigest()
def write(name,value):
 p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def content_hash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
