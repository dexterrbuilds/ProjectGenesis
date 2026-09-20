"""Measure diagnostic analysis cost only, not neural simulation throughput."""
import subprocess
import sys
import os
import time
import json
import platform
import resource
from common import HERE, save, sha

if len(sys.argv)>1:
    mode=sys.argv[1];start=time.perf_counter();cpu=time.process_time()
    if mode=='workbook':
        from independent_data import analyze
        analyze()
    elif mode=='anatomy':
        from anatomy_audit import run
        run()
    else:raise ValueError(mode)
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system()!='Darwin':rss*=1024
    print(json.dumps({'mode':mode,'wall_s':time.perf_counter()-start,'cpu_s':time.process_time()-cpu,'peak_rss_bytes':rss}))
else:
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    results=[]
    for mode in ('workbook','anatomy'):
        p=subprocess.run([sys.executable,__file__,mode],check=True,capture_output=True,text=True,env=env)
        results.append(json.loads(p.stdout))
    save('PERFORMANCE.json',{'scope':'fresh subprocess read-only diagnostic analysis; no neural throughput estimate',
         'python':sys.version,'platform':platform.platform(),'logical_cpu_count':os.cpu_count(),'measurements':results,
         'storage_source_workbook_bytes':(HERE/'data/contrast-source.xls').stat().st_size})
    print(json.dumps(results))
