"""Isolated diagnostic utilities. No imports of Stage-4 simulation or Genesis."""
from pathlib import Path
import json
import hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGE4=ROOT/'research/fly-stage4'


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False,ensure_ascii=False).encode()


def digest(x):return hashlib.sha256(canonical(x)).hexdigest()


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def load(p):return json.loads((HERE/p).read_text())


def save(p,x):
    path=HERE/p;path.parent.mkdir(parents=True,exist_ok=True)
    b=json.dumps(x,sort_keys=True,indent=2,allow_nan=False,ensure_ascii=False).encode()+b'\n'
    if path.exists():assert path.read_bytes()==b, 'Refusing different replacement: '+str(path)
    else:path.write_bytes(b)
