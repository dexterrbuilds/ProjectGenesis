"""Expanded-context protocols using immutable original kernels and exact cue roots."""
import argparse,hashlib,json,time,resource,os
from pathlib import Path
import numpy as np
from context import H
from class_context import Expanded

def cases(stage,level):
 out=[('primary',q,b,'intact') for q in ('A','B') for b in ((.2,.8) if stage==3 else (.2,))]
 if level==2:
  controls=('silence_dan','freeze_plasticity','matched_control') if stage==3 else (('silence_dan','freeze','matched_dan') if stage==1 else ('silence_dan','freeze','matched_control'))
  out += [('primary','A',b,i) for i in controls for b in ((.2,.8) if stage==3 else (.2,))]
 if level==2:
  variants=('full_normalization','context_half','context_double','glutamate_inhibitory','context_cut') if stage==1 else ('role_normalization','context_half','context_double','glutamate_inhibitory','context_cut')
  out += [(v,'A',b,'intact') for v in variants for b in ((.2,.8) if stage==3 else (.2,))]
 return out

def batch(stage,level):
 begun=time.perf_counter();c=Expanded(stage,level);init=time.perf_counter()-begun;e=c.experiment
 root=H/'class-runs';root.mkdir(exist_ok=True)
 for variant,q,b,intervention in cases(stage,level):
  name=f's{stage}-L{level}-{variant}-{q}-{b}-{intervention}';dest=root/name
  if (dest/'study.json').exists():
   manifest=json.loads((dest/'files.json').read_text());assert all(hashlib.sha256((dest/p).read_bytes()).hexdigest()==h for p,h in manifest.items());continue
  stats={'max_rate':0.,'max_saturated_fraction':0.,'max_context_mean':0.,'max_context_active':0,'finite':True,'step_calls':0,'max_active_added_KCs':0};extensions=[]
  def factory(circuit,*args,**kw):
   names=('params','seed','intervention','target') if stage==1 else (('params','seed','intervention','resource') if stage==3 else ('params','seed','intervention'))
   kw.update(dict(zip(names,args)));m=c.make(**kw,variant=variant);extensions.append(m.extension)
   step=m.step
   added_kc=np.array([i for i,a in enumerate(c.nodes) if i>=c.original.n and a.get('cell_class')=='Kenyon_Cell'],dtype=int)
   def observe(*a):
    step(*a);stats['step_calls']+=1
    if m.tick%10==0:
     stats['finite']=stats['finite'] and bool(np.all(np.isfinite(m.r)))
     stats['max_rate']=max(stats['max_rate'],float(m.r.max()));stats['max_saturated_fraction']=max(stats['max_saturated_fraction'],float(np.mean(m.r>.99)))
     if c.n>c.original.n:
      stats['max_active_added_KCs']=max(stats['max_active_added_KCs'],int(np.count_nonzero(m.r[added_kc]>1e-8)))
      v=m.r[c.original.n:];stats['max_context_mean']=max(stats['max_context_mean'],float(v.mean()));stats['max_context_active']=max(stats['max_context_active'],int(np.count_nonzero(v>1e-8)))
   m.step=observe;return m
  e.Model=factory;kw={'intervention':intervention,'output':dest,'replay':False}
  if stage==1:kw['paired']=q
  elif stage==2:kw['repeated']=q
  else:kw.update(cue=q,body=b)
  start=time.perf_counter();cpu=time.process_time();r=e.one(c,**kw)
  detail={'name':name,'stage':stage,'level':level,'variant':variant,'cue':q,'resource':b,'intervention':intervention,'initialization_seconds':init,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'stability_all_phases':stats,'extension':extensions[0],'source_hashes':{p:hashlib.sha256((H/p).read_bytes()).hexdigest() for p in ('context.py','class_context.py','run_class.py','PLAN.md','CLASS_CONTEXT_AMENDMENT.md')},'frozen_source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (H.parent/f'fly-stage{stage}').glob('*.py')}}
  (dest/'study.json').write_text(json.dumps(detail,indent=2)+'\n')
  (dest/'files.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.iterdir()) if p.is_file() and p.name!='files.json'},sort_keys=True)+'\n')
  effect=r.get('selective_depression',r.get('specificity',r.get('max_plastic_change')))
  print(json.dumps({'name':name,'effect':effect,'wall_seconds':detail['wall_seconds'],'rss':detail['peak_rss_bytes']}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',type=int,required=True);p.add_argument('--level',type=int,required=True);a=p.parse_args();batch(a.stage,a.level)
