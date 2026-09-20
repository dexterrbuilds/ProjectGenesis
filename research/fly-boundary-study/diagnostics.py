"""Read saved real traces for modulation and decay diagnostics; never runs a model."""
import json
from pathlib import Path
import numpy as np
from context import H
rows=[]
for d in sorted((H/'runs').iterdir()):
 if not (d/'study.json').exists():continue
 m=json.loads((d/'study.json').read_text())
 if m['variant']!='primary' or m['intervention']!='intact':continue
 r=json.loads((d/'summary.json').read_text());z=np.load(d/'trace.npz');names=z['group_names'].tolist();rr=z['group_rates'];time=z['seconds']
 modulation=[g for g in names if 'DAN' in g];mod={g:{'peak_sampled':float(rr[:,names.index(g)].max()),'mean_sampled':float(rr[:,names.index(g)].mean())} for g in modulation}
 tail=rr[time>=time[-1]-1].max(axis=0)
 rows.append({'run':d.name,'stage':m['stage'],'level':m['level'],'cue':m['cue'],'resource':m['resource'],'modulator_activity':mod,'final_second_max':dict(zip(names,map(float,tail))),'max_plastic_change':r['max_plastic_change']})
(H/'TRACE_DIAGNOSTICS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps({'primary_traces':len(rows)}))
