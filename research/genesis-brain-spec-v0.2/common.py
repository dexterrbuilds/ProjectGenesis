"""Evidence governance only. No model/runtime imports or neural execution."""
from pathlib import Path
import hashlib,json,datetime
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/'research/genesis-brain-spec-v0.1'
BASE_SHA='6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e'
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(Path(p).read_text())
def write(name,x):
 p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(canonical(x)+b'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
PACKAGES={'stage4':('fly-stage4','405d5e982b75846c0e24949f27effd122c3171ebbec77932a30da17b90e3c66a'), 'diagnostic':('fly-lplc2-diagnostic','f427dca560d609e8e4892a91d8577f22608daf82f2f094c0636042cfde7290ca'), 'boundary':('fly-t4t5-boundary','37ae2325016a747574815d215b21edaf53783e741ac158cd9e1a23367e73ffe9'), 'empirical':('fly-t4t5-empirical-interface','805c3c3c79e859dbb0133e62a0dfff8c3473740825c54ae3079facb50c67e904')}
def verify_packages():
 result={}
 for name,(folder,expected) in PACKAGES.items():
  base=ROOT/'research'/folder;p=base/'PACKAGE_MANIFEST.json';m=load(p)
  if name in ['stage4','diagnostic']:actual=digest(m['files'])
  elif name=='boundary':actual=hashlib.sha256(json.dumps({'files':m['files'],'large_sources':m['large_sources']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
  else:actual=hashlib.sha256(json.dumps({k:v for k,v in m.items() if k!='content_sha256'},sort_keys=True,separators=(',',':')).encode()).hexdigest()
  assert actual==m['content_sha256']==expected,(name,'content hash')
  for rel,h in m['files'].items():assert sha(base/rel)==h,(name,rel)
  for rel,item in m.get('large_sources',{}).items():assert sha(base/rel)==item['sha256'] and (base/rel).stat().st_size==item['bytes'],rel
  result[name]={'path':str(p.relative_to(ROOT)),'manifest_file_sha256':sha(p),'content_sha256':expected,'files':len(m['files']),'large_sources':len(m.get('large_sources',{})),'verified':True}
 return result
