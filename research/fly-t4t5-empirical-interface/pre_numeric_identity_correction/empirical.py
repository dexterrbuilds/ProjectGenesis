"""Empirical lookup/interpolation only. Not a neural or precursor-circuit simulator."""
import json,numpy as np

def descriptor_key(r):return (r['dataset'],r['type'],r['family'],r['frame'],json.dumps(r['descriptor'],sort_keys=True,separators=(',',':')))
def interp_group(r,axis):return (r['recording'],r['type'],r['dataset'],r['polarity'],r['width'],r['duration'] if axis=='offset' else r['offset'])
def interp_stratum(r,axis):return '|'.join(map(str,['E1',r['dataset'],r['type'],r['polarity'],r['width'],axis]))
def template_stratum(r):return '|'.join(map(str,['E2',r['dataset'],r['type'],r['family'],r['polarity'],r['width'] if r['family']=='flash' else 'all_widths']))
def interpolate(q, candidates, axis, Y):
 target=q[axis];values=sorted(set(x[axis] for x in candidates if x[axis]!=target))
 if not values:return None
 near=min(abs(x-target) for x in values);closest=[r['id'] for r in candidates if abs(r[axis]-target)==near];pred0=Y[closest].mean(0)
 lo=[x for x in values if x<target];hi=[x for x in values if x>target]
 if not lo or not hi:return {'nearest':pred0,'linear':None,'reason':'no_strict_bracket'}
 a,b=max(lo),min(hi)
 if (axis=='offset' and b-a>2) or (axis=='duration' and (a<=0 or b/a>4)):return {'nearest':pred0,'linear':None,'reason':'outside_registered_locality'}
 ia=[r['id'] for r in candidates if r[axis]==a];ib=[r['id'] for r in candidates if r[axis]==b];w=(target-a)/(b-a);pred=(1-w)*Y[ia].mean(0)+w*Y[ib].mean(0)
 return {'nearest':pred0,'linear':pred,'bracket':[a,b],'weight':w,'sources':ia+ib}

def errors(y,p):
 e=p-y;return {'mse':float(np.mean(e*e)),'mean_error':float(e.mean()),'max_abs_error':float(np.max(abs(e)))}
