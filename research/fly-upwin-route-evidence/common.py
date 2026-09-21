from pathlib import Path
import json,hashlib,datetime
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SPEC=ROOT/'research/genesis-brain-spec-v0.2'
SPEC_SHA='23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88'
PACKAGE_SHA='9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b'
PYTHON='/Users/mac/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(Path(p).read_text())
def write(name,x):
 p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,allow_nan=False,ensure_ascii=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
