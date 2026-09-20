from common import *
import shutil,subprocess,time
import numpy as np
start=__import__('time').perf_counter()
r=HERE/'replay';r.mkdir(exist_ok=True)
for f in ['common.py','models.py','fit.py','evaluate.py','CONDITIONAL_PROTOCOL.md']:shutil.copy2(HERE/f,r/f)
(r/'processed').mkdir(exist_ok=True)
for f in (HERE/'processed').glob('*.npz'):shutil.copy2(f,r/'processed'/f.name)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1')
for script in ['fit.py','evaluate.py']:
 with (r/(script+'.log')).open('w') as out:subprocess.run([sys.executable,str(r/script)],env=env,stdout=out,check=True)
a=json.loads((HERE/'FITS.json').read_text());b=json.loads((r/'FITS.json').read_text());assert a==b
with np.load(HERE/'PREDICTIONS.npz') as x,np.load(r/'PREDICTIONS.npz') as y:
 err=max(float(np.max(abs(x[k]-y[k]))) for k in x.files);assert err<=1e-10
write('replay/REPRODUCTION.json' if (HERE/'REPRODUCTION.json').exists() else 'REPRODUCTION.json',{'fresh_process_fit_exact':True,'max_prediction_absolute_difference_mV':err,'tolerance_mV':1e-10,'wall_seconds':time.perf_counter()-start,'canonical_or_old_research_read':False})
print('fresh-process reproduction passed')
