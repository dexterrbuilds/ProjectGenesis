from common import *
from interface import *
import time,resource,platform
start=time.perf_counter();api=EmpiricalInterface();init=time.perf_counter()-start
r=api.rows[0];q={k:r[k] for k in ['dataset','type','family','frame','observation','units','recording','descriptor']}
times=[]
for i in range(300):
 t=time.perf_counter();out=api.query(q);times.append(time.perf_counter()-t)
start=time.perf_counter();m=next(m for m in read('PREDICTION_METRICS.json') if m['stratum']=='E1|2021_T5_flash|T5|0.0|1.0|duration');r=api.rows[m['id']];partial=EmpiricalInterface([x for x in api.rows if x['id']!=r['id']]);q={k:r[k] for k in ['dataset','type','family','frame','observation','units','recording','descriptor']}
it=[]
for i in range(100):
 t=time.perf_counter();o=partial.query(q);assert o['status']=='ESTIMATE';it.append(time.perf_counter()-t)
names=['atlas/records.json','atlas/waveforms.npz','VALIDATION_RESULTS.json','UNCERTAINTY.json','interface.py','empirical.py','common.py']
write('INTERFACE_BENCHMARK.json',{'host':platform.platform(),'machine':platform.machine(),'python':platform.python_version(),'initialization_seconds':init,'measured_query_median_ms':float(np.median(times)*1000),'measured_query_p95_ms':float(np.quantile(times,.95)*1000),'interpolation_query_median_ms':float(np.median(it)*1000),'interpolation_query_p95_ms':float(np.quantile(it,.95)*1000),'peak_process_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'RAM_scope':'whole Python process including two catalog instances and measurement metrics; macOS ru_maxrss bytes','catalog_arrays_bytes':api.Y.nbytes+api.time.nbytes,'runtime_files_bytes':sum((HERE/n).stat().st_size for n in names),'cpu_scope':'single Python process; no neural-time or real-time neural-substrate claim','query_replicates':{'exact':300,'interpolation':100}})
print(read('INTERFACE_BENCHMARK.json'))
