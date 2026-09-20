"""Measure full frozen-kernel extension cost before applying prospective run budget."""
import hashlib,json,time,resource,gc
import numpy as np
from context import Expanded,H
rows=[]
for s,duration in ((1,220),(2,70),(3,240)):
 start=time.perf_counter();c=Expanded(s,4);m=c.make();init=time.perf_counter()-start
 u=np.zeros(c.n);u[c.groups['PN'][:16]]=1;wall=time.perf_counter();cpu=time.process_time()
 for _ in range(100):
  if s==3:m.step(u,.2)
  else:m.step(u)
 elapsed=time.perf_counter()-wall
 row={'stage':s,'initialization_seconds':init,'pilot_simulated_seconds':1.,'pilot_wall_seconds':elapsed,'cpu_seconds':time.process_time()-cpu,'predicted_acquisition_seconds':elapsed*duration,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'finite':bool(np.all(np.isfinite(m.r))),'max_rate':float(m.r.max()),'extension':m.extension,'rate_hash':hashlib.sha256(m.r.tobytes()).hexdigest()}
 row['eligible_for_full_protocol']=row['predicted_acquisition_seconds']<=120 and row['peak_rss_bytes']<=4*2**30
 rows.append(row);print(json.dumps(row),flush=True);del m,c;gc.collect()
(H/'FULL_PROTOCOL_BUDGET.json').write_text(json.dumps(rows,indent=2)+'\n')
