"""Fresh-process null-transfer replay. No reads of historical outcomes."""
import argparse,hashlib,json,sys,time,resource,platform
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',type=int,choices=[1,2,3],required=True);p.add_argument('--cue',choices=['A','B'],required=True);p.add_argument('--body',type=float,default=.2);a=p.parse_args()
 decision=json.loads((H/'TRANSFER_FROZEN.json').read_text())
 assert decision['stage_parameter_changes']=={} and not decision['calibrated_neural_kernel_exported']
 for f,h in decision['frozen_inputs'].items():assert sha(H/f)==h,f
 source=ROOT/f'research/fly-stage{a.stage}';sys.path.insert(0,str(source))
 from model import Circuit
 from experiment import one
 c=Circuit(next((source/'artifacts').glob('*/manifest.json')).parent)
 name=f's{a.stage}-{a.cue}'+(f'-{a.body}' if a.stage==3 else '')
 dest=H/'replays'/name
 kw={'output':dest,'replay':True,'dense':True}
 if a.stage==1:kw.update(seed=1701,paired=a.cue,target='app')
 elif a.stage==2:kw.update(seed=2701,repeated=a.cue)
 else:kw.update(seed=3701,cue=a.cue,body=a.body)
 start=time.perf_counter();r=one(c,**kw)
 meta={'arm':'null-transfer, unchanged physiological assumptions','transfer_sha256':sha(H/'TRANSFER_FROZEN.json'),
       'stage':a.stage,'cue':a.cue,'body':a.body if a.stage==3 else None,
       'source_hashes':{str(x.relative_to(ROOT)):sha(x) for x in [source/'model.py',source/'experiment.py',source/'PLAN.md']},
       'worker_sha256':sha(Path(__file__)),'manifest':c.manifest_hash,
       'wall_seconds':time.perf_counter()-start,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024),
       'python':platform.python_version(),'calibrated_prediction':False}
 (dest/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
 (dest/'files.json').write_text(json.dumps({x.name:sha(x) for x in dest.iterdir() if x.is_file()},indent=2)+'\n')
 print(json.dumps({'run':name,'wall_seconds':meta['wall_seconds'],'replay_exact':r.get('replay_exact')}),flush=True)
if __name__=='__main__':main()
