"""Sequential fresh-process benchmarks; resumes without overwriting completed runs."""
import subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent
for context in ['s1','s2','s3','integrated','full']:
 for rep in ['R0','R1','R2']:
  if (H/'benchmarks'/f'{context}-{rep}'/'result.json').exists():continue
  subprocess.run([sys.executable,str(H/'benchmark.py'),'--context',context,'--rep',rep],check=True)
