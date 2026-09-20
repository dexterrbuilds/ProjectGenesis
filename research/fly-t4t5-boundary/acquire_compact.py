"""Retrieve pinned author experimental input arrays, not generated model outputs."""
from pathlib import Path
import concurrent.futures,subprocess,hashlib,json
P=Path(__file__).resolve().parent
PIN='fe52053dda84d49a124e6c1f141dd461eba9630c'
files=[f'data_cell_{i}_{kind}.mat' for i in range(1,18) for kind in ('all','spfr')]+['LICENSE','README.md','optimize_model.m']
D=P/'data/t5-compact';D.mkdir(exist_ok=True)
def get(name):
 p=D/name
 if not p.exists():
  subprocess.run(['curl','-L','--fail','--retry','2','--max-time','180','--silent','--show-error',f'https://raw.githubusercontent.com/reiserlab/T5ConductanceModel/{PIN}/{name}','-o',str(p)+'.part'],check=True)
  Path(str(p)+'.part').rename(p)
 return {'file':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0'+p.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:r=list(pool.map(get,files))
(P/'metadata/compact-acquisition.json').write_text(json.dumps({'commit':PIN,'source':'https://github.com/reiserlab/T5ConductanceModel','files':r},indent=2)+'\n')
print(json.dumps({'files':len(r),'bytes':sum(f['bytes'] for f in r)}))
