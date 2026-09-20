"""Class arm queued behind the independent Stage1 L3 batch, max two active batches."""
import subprocess,sys,time,json
from pathlib import Path
H=Path(__file__).resolve().parent;O=Path('outputs/fly-boundary-study');started=time.perf_counter()
last=H/'runs/s1-L3-primary-A-0.2-matched_dan/files.json'
while not last.exists():time.sleep(15)
for level in (1,2,3):
 for stage in (1,2,3):
  with (O/f'class-s{stage}-L{level}.log').open('a') as f:
   p=subprocess.run([sys.executable,str(H/'run_class.py'),'--stage',str(stage),'--level',str(level)],stdout=f,stderr=subprocess.STDOUT)
  print(json.dumps({'stage':stage,'level':level,'exit':p.returncode,'elapsed_including_queue':time.perf_counter()-started}),flush=True)
  if p.returncode:sys.exit(p.returncode)
