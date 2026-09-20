from common import *
import subprocess,sys,os
assert not (HERE/'PRESERVATION_BEFORE.json').exists(),'Do not replace initial baseline'
checks=verify_packages()
old=load(ROOT/'research/fly-t4t5-empirical-interface/FROZEN_BEFORE.json')
for folder in [BASE,ROOT/'research/fly-t4t5-empirical-interface']:
 for p in folder.rglob('*'):
  if p.is_file():old[str(p.relative_to(ROOT))]=sha(p)
for rel,h in old.items():assert sha(ROOT/rel)==h,rel
write('PRESERVATION_BEFORE.json',old)
proc=subprocess.run([sys.executable,str(BASE/'check.py'),'--package'],cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));assert proc.returncode==0,proc.stderr
write('V01_VALIDATION.json',json.loads(proc.stdout))
write('DEPENDENCY_VERIFICATION.json',{'at_utc':now(),'packages':checks,'base_registry_sha256':BASE_SHA,'protected_files':len(old),'neural_runs':0})
print(json.dumps({'verified_packages':list(checks),'protected_files':len(old)}))
