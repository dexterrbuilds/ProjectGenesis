"""Read-only preservation/evidence verification; never reruns completed simulations."""
import ast,hashlib,json,re,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 frozen=json.loads((H/'FROZEN_BEFORE.json').read_text());changes=[p for p,h in frozen.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h];assert not changes,changes
 resumed=json.loads((H/'RESUME_COMPLETED_HASHES.json').read_text());assert all(sha(H/p)==h for p,h in resumed.items())
 for p,h in json.loads((H/'anatomy/manifest.json').read_text())['files'].items():assert sha(H/'anatomy'/p)==h,p
 from run import cases as generic_cases
 from run_class import cases as class_cases
 counts={}
 for family,fun,levels in [('runs',generic_cases,range(4)),('class-runs',class_cases,(1,2,3))]:
  count=0
  for l in levels:
   for s in (1,2,3):
    for v,q,b,i in fun(s,l):
     p=H/family/f's{s}-L{l}-{v}-{q}-{b}-{i}'
     files=json.loads((p/'files.json').read_text())
     for f,h in files.items():assert sha(p/f)==h,(p,f)
     meta=json.loads((p/'study.json').read_text())
     for f,h in meta['source_hashes'].items():assert sha(H/f)==h,(p,f)
     for f,h in meta['frozen_source_hashes'].items():assert sha(Path(f))==h,(p,f)
     count+=1
  counts[family]=count
 before=json.loads((H/'CANONICAL_BEFORE.json').read_text());after=json.loads((H/'CANONICAL_AFTER.json').read_text());assert before==after
 assert after['tableRowCounts']['genesis_decisions']==7 and after['schedule'][0]['enabled'] is False
 tests={}
 for name,n in [('stage1-tests-before',10),('stage2-tests-before',9),('stage3-tests-before',11),('study-tests',8)]:
  p=ROOT/'outputs/fly-boundary-study'/f'{name}.log';log=p.read_text();assert f'Ran {n} tests' in log and log.rstrip().endswith('OK');tests[name]={'passed':n,'log_sha256':sha(p)}
 for p in H.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
 a=json.loads((H/'ANALYSIS.json').read_text());assert len(a['runs'])==sum(counts.values())==156;assert len(a['L0_frozen_reproduction'])==8
 assert all(r['restoration_exact'] for r in a['runs'])
 out={'protected_files':len(frozen),'all_protected_files_unchanged':True,'resumed_evidence_files_unchanged':len(resumed),'completed_verified_conditions':counts,'canonical_before':before,'canonical_after':after,'tests_previously_completed_not_repeated':tests,'L0_exact_trained_state_reproductions':8,'all_156_snapshot_restores_exact':True,'stage1':'PASS','stage2':'PARTIAL-INCONCLUSIVE','stage3':'PARTIAL-INCONCLUSIVE','architecture_recommendation':'INSUFFICIENT EVIDENCE','canonical_cycles_executed':0,'integration_performed':False,'new_behavioral_capabilities':[]}
 (H/'PRESERVATION.json').write_text(json.dumps(out,indent=2)+'\n')
 logs=H/'verification';logs.mkdir(exist_ok=True)
 for p in (ROOT/'outputs/fly-boundary-study').glob('*.log'):shutil.copyfile(p,logs/p.name)
 print(json.dumps({'frozen_files_verified':len(frozen),'resumed_evidence_files_verified':len(resumed),'conditions':counts,'canonical_unchanged':True,'disabled_schedule':True,'tests':tests},indent=2))
if __name__=='__main__':main()
