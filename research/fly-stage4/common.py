"""Utilities confined to this unadmitted research package."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REGISTRY = '6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e'
ANATOMY = ROOT / 'research/fly-boundary-study/anatomy'


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def save(name, x):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(x, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'
    if p.exists() and p.read_bytes() != data:
        raise ValueError('Immutable artifact already exists: ' + str(p))
    if not p.exists():
        p.write_bytes(data)


def load(name):
    return json.loads((HERE / name).read_text())
