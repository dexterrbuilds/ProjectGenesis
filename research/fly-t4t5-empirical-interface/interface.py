"""Isolated empirical voltage catalog. No neural simulator or Genesis adapter."""
from common import HERE,read
from empirical import descriptor_key,interp_group,interp_stratum,template_stratum,interpolate
import numpy as np

OBS='mean_baseline_subtracted_somatic_voltage'
def unknown(reason,support='OUT OF DISTRIBUTION / UNKNOWN'):
 return {'status':'UNKNOWN','support':support,'reason':reason,'voltage_mV':None}

class EmpiricalInterface:
 def __init__(self,rows=None):
  self.rows=read('atlas/records.json') if rows is None else rows
  with np.load(HERE/'atlas/waveforms.npz',allow_pickle=False) as z:self.Y=z['voltage_mV'];self.time=z['time_ms']
  self.stats={s['stratum']:s for s in read('VALIDATION_RESULTS.json')['strata']}
  self.envelopes=read('UNCERTAINTY.json')['envelopes']
  self.exact={}
  for r in self.rows:self.exact.setdefault(descriptor_key(r),[]).append(r)
 def query(self,q):
  required={'dataset','type','family','frame','observation','units','descriptor'}
  optional={'recording','mode','horizon_ms','FlyWire_root','subtype','column','fly_id'}
  if not isinstance(q,dict) or not required<=q.keys() or set(q)-required-optional:return unknown('Missing or unsupported request field')
  if any(q.get(k) is not None for k in ['FlyWire_root','subtype','column','fly_id']):return unknown('Physiology-to-identity crosswalk not identified')
  if q['observation']!=OBS or q['units']!='mV':return unknown('Observation conversion not identified')
  if q.get('horizon_ms',500)!=500:return unknown('Only the registered 0–500 ms waveform is exported')
  if q.get('mode','individual') not in ['individual','class_template']:return unknown('Unsupported export mode')
  if not isinstance(q['descriptor'],dict):return unknown('Descriptor must be a complete physical tuple')
  pool=[r for r in self.rows if all(r[k]==q[k] for k in ['dataset','type','family','frame'])]
  if not pool:return unknown('No compatible source/family/frame')
  if set(q['descriptor'])!=set(pool[0]['descriptor']):return unknown('Missing or extra physical descriptor')
  try:key=descriptor_key(q)
  except (TypeError,ValueError):return unknown('Invalid physical descriptor')
  exact=self.exact.get(key,[])
  if q.get('mode')=='class_template':
   if q.get('recording') is not None:return unknown('Class template cannot assert an individual recording')
   recs=sorted({r['recording'] for r in exact})
   if len(recs)<4:return unknown('Fewer than four exact recordings; no eligible leave-one-recording-out comparison')
   st=template_stratum(exact[0]);stat=self.stats[st]
   if not stat['meets_registered_criteria']:return unknown('Conditional template comparison failed or underpowered','WEAKLY SUPPORTED')
   y=np.mean([self.Y[[r['id'] for r in exact if r['recording']==k]].mean(0) for k in recs],axis=0)
   return self.export(y,exact,'WEAKLY SUPPORTED','CLASS TEMPLATE',st,None)
  rec=q.get('recording')
  if rec is None:return unknown('Individual response requires a named source recording','WEAKLY SUPPORTED')
  exact=[r for r in exact if r['recording']==rec]
  if exact:return self.export(self.Y[[r['id'] for r in exact]].mean(0),exact,'DIRECTLY MEASURED','MEASURED',None,rec)
  if q['family']!='flash':return unknown('No exact recording-condition match; cross-family/trajectory inference unsupported')
  d=q['descriptor']
  if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and np.isfinite(x) for x in d.values()):return unknown('Non-finite or nonnumeric flash descriptor')
  target=dict(q,recording=rec,polarity=d['contrast_value'],width=d['width_pixels'],duration=d['duration_ms'],offset=d['offset_pixels'])
  for axis,field in [('offset','offset_pixels'),('duration','duration_ms')]:
   st=interp_stratum(target,axis)
   # Input numeric spellings cannot change stratum identity.
   target.update(polarity=float(target['polarity']),width=float(target['width']));st=interp_stratum(target,axis)
   stat=self.stats.get(st)
   if not stat or not stat['meets_registered_criteria']:continue
   tested={r[axis] for r in pool if r['polarity']==target['polarity'] and r['width']==target['width']}
   if target[axis] not in tested:continue
   candidates=[r for r in pool if interp_group(r,axis)==interp_group(target,axis)]
   out=interpolate(target,candidates,axis,self.Y)
   if out and out.get('linear') is not None:
    sources=[r for r in candidates if r['id'] in out['sources']]
    result=self.export(out['linear'],sources,'INTERPOLATION-SUPPORTED','ESTIMATE',st,rec)
    result['bracket']=out['bracket'];result['weight']=out['weight'];result['axis']=axis
    return result
  return unknown('No validated one-axis bracket for the requested condition','WEAKLY SUPPORTED')
 def export(self,y,sources,support,status,stratum,recording):
  env=[e for e in self.envelopes if e['stratum']==stratum and e['recording']==recording]
  band=env[0]['half_width_mV'] if env else None
  return {'status':status,'support':support,'observation':OBS,'units':'mV','time_ms':self.time.tolist(),'voltage_mV':y.tolist(),'source_ids':[r['id'] for r in sources],'source_recordings':sorted({r['recording'] for r in sources}),'stratum':stratum,'uncertainty':{'half_width_mV':band,'bounded':band is not None,'population_guarantee':False,'source_trial_noise_identified':False},'root_assignment':None,'mechanistic_simulation':False}
