"""Unseal historical outcomes only after all eight null-transfer replays exist."""
import gzip,hashlib,json
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 paths=sorted((H/'replays').glob('*/summary.json'));assert len(paths)==8
 rows=[];by={}
 for p in paths:
  m=load(p.parent/'provenance.json');s=m['stage'];q=m['cue'];b=m['body'];x=load(p)
  if s==1:name=f'app-1701-{q}-intact'
  elif s==2:name=f'primary-2701-{q}'
  else:name=f'primary-3701-{q}-{b}'
  candidates=list((ROOT/f'research/fly-stage{s}/evidence').glob('*/'+name+'/summary.json'));assert len(candidates)==1,(name,candidates)
  oldp=candidates[0];old=load(oldp)
  # State objects are stronger evidence than equality of a pooled scalar readout.
  trained=json.loads(gzip.decompress((p.parent/'trained.json.gz').read_bytes()))
  oldtrained=json.loads(gzip.decompress((oldp.parent/'trained.json.gz').read_bytes()))
  exact=trained==oldtrained
  metrics=['baseline','post','trained_hash','initial_hash']
  if s==1:metrics+=['selective_depression','plastic_only','restored']
  elif s==2:metrics+=['specificity','fast_reset','recovery','restored']
  else:metrics+=['metrics','fast_reset','body_swap_same_weights','restored']
  assert all(x[k]==old[k] for k in metrics),(name,'metric mismatch')
  r={'run':p.parent.name,'historical_path':str(oldp.relative_to(ROOT)),'historical_sha256':sha(oldp),
     'trained_state_exact':exact,'compared_metrics_exact':True,'replay_exact':x['replay_exact'],
     'restoration_exact':x['restoration_exact'],'wall_seconds':m['wall_seconds'],
     'peak_process_rss_bytes':m['peak_process_rss_bytes'],'parameter_changes':{},'calibrated_prediction':False}
  if s==1:r.update(selective_depression_percent=100*x['selective_depression'],paired_depression_percent=100*x['paired_depression'])
  if s==2:r.update(specificity_percent=100*x['specificity'],repeated_depression_percent=100*x['repeated_depression'])
  rows.append(r);by[(s,q,b)]=x
 state=[]
 for q in ('A','B'):
  low=by[(3,q,.2)];high=by[(3,q,.8)]
  # Supplemental descriptive metric: mean of all ten maintained windows; not the frozen trial-10 acceptance metric.
  for group in ['MB11','MB18','LH','PN','KC']:
   a=np.mean([v['maintained'][group] for v in low['metrics']['trials']]);b=np.mean([v['maintained'][group] for v in high['metrics']['trials']])
   state.append({'cue':q,'group':group,'low_resource_mean':float(a),'high_resource_mean':float(b),'contrast_percent_of_high':float(100*(a-b)/max(abs(b),1e-15))})
 out={'calibrated_capability_inference_available':False,'arm':'null-transfer preservation/control; not calibrated validation','runs':rows,'stage3_state_contrasts':state,'transfer_sha256':sha(H/'TRANSFER_FROZEN.json')}
 dest=H/'REPLAY_COMPARISON.json';assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
