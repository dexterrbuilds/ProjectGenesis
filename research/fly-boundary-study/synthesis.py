"""Additional aggregate comparisons from sealed experiments, without new simulation."""
import json,hashlib
from pathlib import Path
import numpy as np
from context import H

def main():
 a=json.loads((H/'ANALYSIS.json').read_text());rr=a['runs'];cc=a['stage3_comparisons'];rows=[];controls=[];participation=[];diagnostics=[]
 def find(stage,level,cue,family,variant='primary',intervention='intact'):
  seq=cc if stage==3 else rr
  return next(x for x in seq if x.get('stage',3)==stage and x['level']==level and x['cue']==cue and x['family']==family and x['variant']==variant and x['intervention']==intervention)
 def metric(x,stage):return x['contrast']['MB11'] if stage==3 else x['effect']
 for stage in (1,2,3):
  for q in ('A','B'):
   base=metric(find(stage,0,q,'generic'),stage)
   for level in (1,2,3):
    g=metric(find(stage,level,q,'generic'),stage);c=metric(find(stage,level,q,'class_consistent'),stage)
    rows.append({'stage':stage,'cue':q,'level':level,'original':base,'generic':g,'class_consistent':c,'class_minus_generic_percentage_points':100*(c-g),'class_vs_generic_relative_change':c/g-1,'class_vs_original_relative_change':c/base-1,'generic_vs_original_relative_change':g/base-1})
  for fam in ('generic','class_consistent'):
   base=find(stage,2,'A',fam);b=metric(base,stage)
   ints=('silence_dan','freeze_plasticity','matched_control') if stage==3 else (('silence_dan','freeze','matched_dan') if stage==1 else ('silence_dan','freeze','matched_control'))
   for intervention in ints:
    x=find(stage,2,'A',fam,intervention=intervention);v=metric(x,stage)
    controls.append({'stage':stage,'family':fam,'intervention':intervention,'effect':v,'intact_effect':b,'effect_reduction':None if v is None else 1-v/b,'experience_low':x.get('experience_low')})
 for family in ('runs','class-runs'):
  for p in sorted((H/family).iterdir()):
   if not (p/'study.json').exists():continue
   m=json.loads((p/'study.json').read_text());r=json.loads((p/'summary.json').read_text());state=m['stability_all_phases']
   participation.append({'family':family,'run':p.name,**state,'extension':m['extension'],'wall_seconds':m['wall_seconds'],'cpu_seconds':m['cpu_seconds'],'peak_rss_bytes':m['peak_rss_bytes']})
   if m['variant']!='primary' or m['intervention']!='intact':continue
   z=np.load(p/'trace.npz');names=z['group_names'].tolist();rates=z['group_rates'];t=z['seconds']
   diagnostics.append({'family':family,'run':p.name,'dopamine_sampled_peak':{g:float(rates[:,j].max()) for j,g in enumerate(names) if 'DAN' in g},'final_second_max':{g:float(rates[t>=t[-1]-1,j].max()) for j,g in enumerate(names)},'mean_plastic_multiplier_end':float(z['mean_learnable_multiplier'][-1]) if 'mean_learnable_multiplier' in z else None})
 storage={name:sum(p.stat().st_size for p in (H/name).rglob('*') if p.is_file()) for name in ('anatomy','runs','class-runs','benchmarks')}
 out={'effect_family_comparison':rows,'L2_intervention_comparison':controls,'participation_and_stability':participation,'trace_diagnostics':diagnostics,'storage_bytes':storage,'notes':['Active-context thresholds >1e-8 are numerical diagnostics, not behavior labels.','Participation maxima include acquisition and disposable probes; not simultaneous whole-brain motor activity.','Generic added KCs are analytically silent because .05 maximum incoming drive <.15 threshold; class-consistent added-KC counts are measured.','Stage3 comparison metric is resource contrast, while freeze primarily tests experience; acute modulation can remain.']}
 (H/'SYNTHESIS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'L3_comparison':[x for x in rows if x['level']==3],'storage_bytes':storage,'all_finite':all(x['finite'] for x in participation),'max_class_added_KCs':max(x.get('max_active_added_KCs',0) for x in participation)},indent=2))
if __name__=='__main__':main()
