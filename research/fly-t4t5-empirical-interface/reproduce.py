"""Fresh interpreter, copied empirical inputs only. Never reads old-stage outputs."""
from common import *
import shutil,subprocess,numpy as np,time
dest=HERE/'replay';dest.mkdir(exist_ok=False)
files=['common.py','empirical.py','validate_empirical.py','atlas/records.json','atlas/waveforms.npz','COVERAGE_ATLAS.json']
for n in files:
 (dest/n).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/n,dest/n)
start=time.perf_counter();p=subprocess.run([sys.executable,str(dest/'validate_empirical.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True);assert p.returncode==0,p.stderr
checked=['PREDICTION_METRICS.json','HOLDOUT_COVERAGE.json','VALIDATION_RESULTS.json','UNCERTAINTY.json','FAMILY_HOLDOUT.json']
same={n:sha(dest/n)==sha(HERE/n) for n in checked}
with np.load(dest/'HELDOUT_PREDICTIONS.npz') as a,np.load(HERE/'HELDOUT_PREDICTIONS.npz') as b:
 arrays={k:bool(np.array_equal(a[k],b[k])) for k in a.files}
assert all(same.values()) and all(arrays.values())
write('REPRODUCTION.json',{'fresh_process':True,'input_hashes':{n:sha(dest/n) for n in files},'identical_json':same,'identical_arrays':arrays,'tolerance':0,'wall_seconds':time.perf_counter()-start,'stdout':p.stdout})
print('Fresh-process predictions and intervals identical.')
