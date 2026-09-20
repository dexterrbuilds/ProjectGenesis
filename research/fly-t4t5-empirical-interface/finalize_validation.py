from common import *
from check import verify
import subprocess,datetime,time
start=time.perf_counter()
test=subprocess.run([sys.executable,str(HERE/'test_interface.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(HERE/'TEST_LOG.txt').write_text(test.stdout+test.stderr);assert test.returncode==0,test.stderr
spec=subprocess.run([sys.executable,str(ROOT/'research/genesis-brain-spec-v0.1/check.py'),'--package','--experiment',str((HERE/'DEPENDENCIES.json').relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
assert spec.returncode==0,spec.stderr;write('SPEC_VALIDATION.json',json.loads(spec.stdout))
checks=verify();write('PRESERVATION.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'canonical_sha256':read('CANONICAL_AFTER.json')['sha256'],'test_exit_code':test.returncode,'tests':10,'wall_seconds':time.perf_counter()-start})
print(json.dumps(checks))
