from common import *
from models import *
import time,resource

def main():
 start=time.perf_counter();access=firewall('fit');allfits=[];profile=[]
 for cell in range(1,18):
  path=HERE/f'processed/cell_{cell:02d}_train.npz';d=load(path);rows=[];cache={}
  for opt in options():
   key=tuple(opt[k] for k in ['kind','tau','delay','gamma'])
   if key not in cache:
    X=features(d,**{k:opt[k] for k in ['kind','tau','delay','gamma']});cache[key]=moments(d,X)
   g,h,q,dur=cache[key];G=g.mean(0);H=h.mean(0);Q=q.mean();errs=[];foldbeta=[]
   for held in sorted(set(dur)):
    tr=dur!=held;te=~tr;b,_,_=solve(g[tr].mean(0),h[tr].mean(0),opt['lambda'],opt['kind']);errs.append(mse(g[te].mean(0),h[te].mean(0),q[te].mean(),b));foldbeta.append(b.tolist())
   b,edf,rank=solve(G,H,opt['lambda'],opt['kind']);ev=np.linalg.eigvalsh(G) if len(H) else np.array([])
   rows.append({**opt,'cv_mse_mV2':float(np.mean(errs)),'cv_fold_mse_mV2':errs,'cv_fold_se_heuristic':float(np.std(errs,ddof=1)/np.sqrt(len(errs))),'coefs':b.tolist(),'effective_dof':edf,'raw_coefficients':len(b),'rank':rank,'spectrum':ev.tolist(),'condition_positive_subspace':float(ev[-1]/ev[ev>max(1e-14,ev[-1]*1e-10)][0]) if rank else None,'training_mse_mV2':mse(G,H,Q,b),'fold_coefficients':foldbeta})
  best=min(rows,key=lambda x:x['cv_mse_mV2']);cut=best['cv_mse_mV2']+best['cv_fold_se_heuristic'];eligible=[x for x in rows if x['cv_mse_mV2']<=cut]
  selected=min(eligible,key=lambda x:(x['effective_dof']+(x['kind']=='B1d'),x['cv_mse_mV2']))
  bykind={k:min([x for x in rows if x['kind']==k],key=lambda x:x['cv_mse_mV2']) for k in ['Z','B0','B1s','B1t','B1d']}
  allfits.append({'recording':cell,'train_sha256':sha(path),'selected':selected,'candidate_fits':bykind,'competitive_ranges':{k:sorted(set(x[k] for x in eligible)) for k in ['kind','tau','delay','gamma','lambda']},'selection_cutoff_mV2':cut})
  profile.append({'recording':cell,'options':rows});print(json.dumps({'recording':cell,'selected':selected['kind'],'inner_mse':selected['cv_mse_mV2']}),flush=True)
 write('FITS.json',{'protocol_sha256':sha(HERE/'CONDITIONAL_PROTOCOL.md'),'model_sha256':sha(HERE/'models.py'),'fits':allfits,'scope':'conditional flash-trained voltage only; no fly or T4 validation'})
 write('TRAINING_PROFILE.json',profile)
 write('FIT_FREEZE.json',{'fits_sha256':sha(HERE/'FITS.json'),'model_sha256':sha(HERE/'models.py'),'protocol_sha256':sha(HERE/'CONDITIONAL_PROTOCOL.md'),'test_outcomes_used':False,'wall_seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
 write('FIT_ACCESS.json',sorted(set(access)))
if __name__=='__main__':main()
