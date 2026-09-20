"""Verify preservation without opening runtime or running canonical life cycles."""
import argparse,ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 frozen=load(H/'FROZEN_BEFORE.json');resumed=load(H/'RESUMED_HASHES.json')
 for f,d in frozen.items():assert sha(ROOT/f)==d,f
 for f,d in resumed.items():assert sha(H/f)==d,f
 for f in ['CALIBRATION_FROZEN.json','IDENTIFICATION_FROZEN.json']:
  for name,d in load(H/f)['source_hashes'].items():assert sha(H/name)==d,(f,name)
 for name,d in load(H/'TRANSFER_FROZEN.json')['frozen_inputs'].items():assert sha(H/name)==d,name
 before=load(H/'CANONICAL_BEFORE.json');after=load(H/'CANONICAL_AFTER.json');assert before==after
 assert after['tableRowCounts']['genesis_decisions']==7 and after['schedule'][0]['enabled'] is False
 comparison=load(H/'REPLAY_COMPARISON.json');assert len(comparison['runs'])==8
 assert all(x['trained_state_exact'] and x['replay_exact'] and x['restoration_exact'] for x in comparison['runs'])
 for p in (H/'replays').glob('*/files.json'):
  for f,d in load(p).items():assert sha(p.parent/f)==d,(p,f)
 tests={}
 for name,n in [('stage1',10),('stage2',9),('stage3',11),('study-tests',8)]:
  p=H/'verification'/f'{name}.txt';s=p.read_text();assert f'Ran {n} tests' in s and s.rstrip().endswith('OK');tests[name]={'tests':n,'sha256':sha(p)}
 for p in H.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
 audit={'previous_files_unchanged':len(frozen),'interrupted_study_files_unchanged':len(resumed),
   'tests':tests,'canonical_before':before,'canonical_after':after,'canonical_cycles_run':0,
   'same_historical_states':8,'same_replay_states':8,'snapshot_restores_exact':8,
   'neural_parameter_changes':{},'calibrated_kernel_exported':False,'stage4_started':False,
   'prior_classifications_unchanged':{'Stage1':'PASS','Stage2':'PARTIAL-INCONCLUSIVE','Stage3':'PARTIAL-INCONCLUSIVE','Architecture':'INSUFFICIENT EVIDENCE'},
   'classification':'PARTIAL PHYSIOLOGICAL CONSTRAINT'}
 if a.check:
  assert load(H/'PRESERVATION.json')==audit
  m=load(H/'STUDY_MANIFEST.json')
  for f,d in m['files'].items():assert sha(H/f)==d,f
  print(json.dumps({'verified_files':len(m['files']),'previous_files':len(frozen),'classification':audit['classification']}))
 else:
  assert not (H/'STUDY_MANIFEST.json').exists(),'Refuse to replace completed manifest'
  (H/'PRESERVATION.json').write_text(json.dumps(audit,indent=2)+'\n')
  m={'classification':audit['classification'],'frozen_calibration_sha256':sha(H/'CALIBRATION_FROZEN.json'),
     'files':{str(p.relative_to(H)):sha(p) for p in sorted(H.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='STUDY_MANIFEST.json'}}
  (H/'STUDY_MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'files':len(m['files']),'bytes':sum((H/f).stat().st_size for f in m['files']),'prior_files_verified':len(frozen),'classification':audit['classification']}))
if __name__=='__main__':main()
