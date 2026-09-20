"""Final immutable research manifest and preservation checks, no runtime access."""
import argparse,ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent.parent
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(4*1024*1024),b''):h.update(c)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 prior=load(H/'FROZEN_BEFORE.json');resumed=load(H/'RESUMED_HASHES.json')
 for path,d in prior.items():assert sha(ROOT/path)==d,path
 for path,d in resumed.items():assert sha(H/path)==d,path
 before=load(H/'CANONICAL_BEFORE.json');after=load(H/'CANONICAL_AFTER.json');assert before==after
 old=load(H.parent/'fly-physiology-study/CANONICAL_AFTER.json');assert before['sha256']==old['sha256']
 assert before['tableRowCounts']['genesis_decisions']==7 and before['schedule'][0]['enabled'] is False
 for f in H.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
 tests={}
 for name,n in [('stage1',10),('stage2',9),('stage3',11),('frozen-physiology',8),('study-tests',10)]:
  f=H/'verification'/f'{name}.txt';s=f.read_text();assert f'Ran {n} tests' in s and s.rstrip().endswith('OK'),name
  tests[name]={'passed':n,'sha256':sha(f)}
 fit=load(H/'FIT_FROZEN.json')
 for f,d in fit['source_hashes'].items():assert sha(H/f)==d,f
 for source in load(H/'data/challenges.json')['sources']:assert sha(H/'data'/source['file'])==source['sha256']
 assert load(H/'VALIDATION.json')['fit_sha256']==sha(H/'FIT_FROZEN.json')
 benches=list((H/'benchmarks').glob('*/result.json'));assert len(benches)==15
 for f in benches:
  r=load(f);assert r['replay_exact'] and r['all_finite'] and r['updates']==100
  assert r['code_sha256']==sha(H/'benchmark.py') and r['specification_sha256']==sha(H/'REPRESENTATIONS.md')
 assert load(H/'IDENTITY_AUDIT.json')['registry_sha256']==sha(H/'identity-registry.jsonl.gz')
 audit={'protected_files_unchanged':len(prior),'interrupted_files_unchanged':len(resumed),'tests':tests,
  'canonical_hash_unchanged':before['sha256'],'canonical_decisions':7,'schedule_enabled':False,
  'canonical_cycles_run':0,'new_stage_probe_replays':0,'kernel_exported':False,'benchmark_exact_replays':15,
  'prior_research_changed':False,'genesis_integration':False,'stage4':False,
  'classification':load(H/'SUMMARY.json')['classification']}
 if args.check:
  assert load(H/'PRESERVATION.json')==audit
  m=load(H/'STUDY_MANIFEST.json')
  for f,d in m['files'].items():assert sha(H/f)==d,f
  current={str(f.relative_to(H)) for f in H.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='STUDY_MANIFEST.json'}
  assert current==set(m['files']),'Unmanifested/missing file'
  print(json.dumps({'files_verified':len(m['files']),**audit}));return
 assert not (H/'STUDY_MANIFEST.json').exists(),'Refuse replacing completed manifest'
 (H/'PRESERVATION.json').write_text(json.dumps(audit,indent=2)+'\n')
 files={str(f.relative_to(H)):sha(f) for f in sorted(H.rglob('*')) if f.is_file() and '__pycache__' not in f.parts and f.name!='STUDY_MANIFEST.json'}
 m={'classification':audit['classification'],'files':files,'bytes':sum((H/f).stat().st_size for f in files)}
 (H/'STUDY_MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');print(json.dumps({'files':len(files),'bytes':m['bytes'],**audit}))
if __name__=='__main__':main()
