"""Serial fresh-process jobs; never repeats a sealed completed condition."""
import json,subprocess,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;O=Path('outputs/fly-boundary-study')
start=time.perf_counter()
for level in range(4):
 for stage in (1,2,3):
  if level==0 and stage==1:continue
  log=O/f's{stage}-L{level}.log'
  with log.open('a') as f:
   p=subprocess.run([sys.executable,str(H/'run.py'),'--stage',str(stage),'--level',str(level)],stdout=f,stderr=subprocess.STDOUT)
  print(json.dumps({'stage':stage,'level':level,'exit':p.returncode,'elapsed':time.perf_counter()-start}),flush=True)
  if p.returncode:sys.exit(p.returncode)
