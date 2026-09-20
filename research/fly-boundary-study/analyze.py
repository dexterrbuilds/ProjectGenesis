"""Derive quantitative tables from sealed runs. No simulation or fitting."""
import csv,gzip,hashlib,json
from pathlib import Path
import numpy as np
from context import H

def pct_effect(before,after):return None if abs(before)<1e-12 else 1-after/before

def main():
 rows=[];runs={}
 for p in sorted((H/'runs').iterdir())+sorted((H/'class-runs').iterdir()):
  if not (p/'study.json').exists():raise ValueError('Incomplete run '+str(p))
  files=json.loads((p/'files.json').read_text());assert all(hashlib.sha256((p/f).read_bytes()).hexdigest()==v for f,v in files.items())
  meta=json.loads((p/'study.json').read_text());r=json.loads((p/'summary.json').read_text());s=meta['stage'];q=meta['cue'];g='MBON_app' if s==1 else ('MBON' if s==2 else 'MB11')
  def group(phase,cue,key):
   rr=r[phase][cue];return rr[key] if s==1 else rr['groups'][key]
  rr={k:meta[k] for k in ('name','stage','level','variant','cue','resource','intervention','wall_seconds','cpu_seconds','peak_rss_bytes')}
  rr['family']='class_consistent' if p.parent.name=='class-runs' else 'generic'
  rr.update(baseline=group('baseline',q,g),post=group('post',q,g),effect=r.get('selective_depression',r.get('specificity')),max_plastic_change=r['max_plastic_change'],restoration_exact=r['restoration_exact'],max_rate=meta['stability_all_phases']['max_rate'],saturated_fraction=meta['stability_all_phases']['max_saturated_fraction'],max_context_active=meta['stability_all_phases']['max_context_active'])
  rr['baseline_sensory']={key:group('baseline',q,key) for key in ('PN','KC')}
  rr['sensory_change']={key:pct_effect(group('baseline',q,key),group('post',q,key)) for key in ('PN','KC')}
  rr['reset_delta']=(max(abs(r['post'][cue][key]-r['plastic_only'][cue][key]) for cue in r['post'] for key in r['post'][cue])
                     if s==1 else r.get('fast_reset_max_rate_delta',r.get('reset_max_rate_delta')))
  rr['reset_delta_scope']='original population means' if s==1 else 'all modeled neuron probe rates'
  if s==3:
   tt=r['metrics']['trials'];rr['experience']={key:tt[9]['maintained'][key]/tt[0]['maintained'][key]-1 if tt[0]['maintained'][key]>1e-12 else None for key in ('MB11','MB18','LH','PN','KC')}
   rr['last']=tt[9]['maintained'];rr['first']=tt[0]['maintained']
  rows.append(rr);runs[rr['family']+'/'+meta['name']]=(r,meta,p)
 comparisons=[]
 for row in rows:
  if row['stage']!=3 or row['resource']!=.2:continue
  high=next(x for x in rows if all(x[k]==row[k] for k in ('family','stage','level','variant','cue','intervention')) and x['resource']==.8)
  comparisons.append({k:row[k] for k in ('family','level','variant','cue','intervention')}|{'contrast':{g:row['last'][g]/high['last'][g]-1 if abs(high['last'][g])>1e-12 else None for g in row['last']},'experience_low':row['experience'],'experience_high':high['experience']})
 preservation=[]
 for s in (1,2,3):
  saved=next((H.parent/f'fly-stage{s}'/'evidence').iterdir())
  for q in ('A','B'):
   for body in ((.2,.8) if s==3 else (.2,)):
    name=f's{s}-L0-primary-{q}-{body}-intact';r,meta,p=runs['generic/'+name]
    pattern=f'app-1701-{q}-intact' if s==1 else (f'primary-2701-{q}' if s==2 else f'primary-3701-{q}-{body}')
    candidates=[saved/pattern]
    if not candidates[0].exists():
     candidates=[]
     for d in saved.iterdir():
      if not d.is_dir() or not (d/'summary.json').exists():continue
      rr=json.loads((d/'summary.json').read_text())
      if s==1 and rr.get('seed')==1701 and rr.get('paired')==q and rr.get('intervention')=='intact' and rr.get('target')=='app' and not rr.get('unpaired_teaching'):candidates.append(d)
    assert len(candidates)==1,(s,q,candidates)
    original=json.loads(gzip.decompress((candidates[0]/'trained.json.gz').read_bytes()));new=json.loads(gzip.decompress((p/'trained.json.gz').read_bytes()))
    equal={k:original[k]==new[k] for k in ('rate','eligibility','plastic_multiplier','tick','prng')}
    assert all(equal.values()),(name,equal)
    preservation.append({'run':name,'trained_neural_plastic_clock_PRNG_exact':True,'fingerprints_differ_by_design':True})
 benchmark=[json.loads(p.read_text()) for p in sorted((H/'benchmarks').glob('*/result.json'))]
 result={'runs':rows,'stage3_comparisons':comparisons,'L0_frozen_reproduction':preservation,'benchmarks':benchmark,'protocol_budget':json.loads((H/'FULL_PROTOCOL_BUDGET.json').read_text())}
 (H/'ANALYSIS.json').write_text(json.dumps(result,indent=2)+'\n')
 with (H/'TRAJECTORIES.csv').open('w',newline='') as f:
  fields=['family','stage','level','variant','cue','resource','intervention','baseline','post','effect','max_plastic_change','wall_seconds','peak_rss_bytes'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
 print(json.dumps({'conditions':len(rows),'exact_L0_reproductions':len(preservation),'all_restores':all(r['restoration_exact'] for r in rows),'max_rate':max(r['max_rate'] for r in rows)},indent=2))
if __name__=='__main__':main()
