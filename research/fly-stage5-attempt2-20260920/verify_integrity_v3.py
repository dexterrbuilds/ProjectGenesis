"""Read-only hash audit. Never parses Stage-1 summary values or runs neural code."""
from pathlib import Path
import hashlib,json,sys,datetime
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
P=ROOT/'research/fly-stage5-protocol-v0.1'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4194304):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
phase=sys.argv[1];report={'phase':phase,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[],'failures':[],'source_summary_values_read':False}
def check(name,actual,expected):
 ok=actual==expected;report['checks'].append({'check':name,'actual':actual,'expected':expected,'passed':ok})
 if not ok:report['failures'].append(name)
def filecheck(p,h):
 check(str(p.relative_to(ROOT)),sha(p),h)
 report['checks'][-1]['hash_object_type']='FILE HASH'
 report['checks'][-1]['canonical_object']='raw file bytes'
def manifestcheck(p,h):
 filecheck(p,h)
 report['checks'][-1]['hash_object_type']='MANIFEST HASH'
 report['checks'][-1]['canonical_object']='raw bytes of the explicitly pinned manifest; no reserialization'
try:
 candidates=[]
 for p in (ROOT/'research').glob('*/RELEASE.json'):
  d=load(p)
  if d.get('id')=='genesis-stage5-prospective-protocol':candidates.append(str(p.relative_to(ROOT)))
 check('unique_stage5_release',candidates,['research/fly-stage5-protocol-v0.1/RELEASE.json'])
 r=load(P/'RELEASE.json');check('version',r['version'],'0.1.0')
 check('canonical_stage5_content_hash',hashlib.sha256(canonical(r['files'])).hexdigest(),r['content_sha256'])
 report['sealed_stage5_release_hash']=r['content_sha256'];report['release_file_sha256']=sha(P/'RELEASE.json')
 check('sealed_file_inventory',sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()),sorted(list(r['files'])+['RELEASE.json']))
 for p,h in r['files'].items():filecheck(P/p,h)
 check('analysis_code_sha256',sha(P/'prospective_analysis.py'),r['analysis_code_sha256'])
 dep=load(P/'DEPENDENCIES.json')['packages']
 for name,d in dep.items():
  base=ROOT/'research'/name
  if 'release_sha256' in d:filecheck(base/'RELEASE.json',d['release_sha256'])
  if 'content_sha256' in d:
   release=load(base/'RELEASE.json');check(name+' content',hashlib.sha256(canonical(release['files'])).hexdigest(),d['content_sha256'])
   for p,h in release['files'].items():filecheck(base/p,h)
  if name=='genesis-brain-spec-v0.2':
   filecheck(base/'objects'/(d['registry_sha256']+'.json'),d['registry_sha256'])
   package=load(base/'PACKAGE_MANIFEST.json')
   package_hash=hashlib.sha256(canonical({k:v for k,v in package.items() if k!='content_sha256'})).hexdigest()
   check(name+' canonical package content',package_hash,d['package_sha256'])
   report['checks'][-1]['hash_object_type']='PACKAGE-CONTENT HASH'
   report['checks'][-1]['canonical_object']='compact sorted UTF-8 JSON manifest object excluding content_sha256, per owning check.py/check_published'
   check(name+' declared package content',package['content_sha256'],package_hash)
   for p,h in load(base/'PACKAGE_MANIFEST.json')['files'].items():filecheck(base/p,h)
  if name=='fly-stage1':
   em=ROOT/d['evidence_manifest_path'];manifestcheck(em,d['evidence_manifest_sha256'])
   for p,h in load(em)['files'].items():filecheck(em.parent/p,h)
   filecheck(base/'model.py',d['model_sha256'])
   cm=base/'artifacts'/d['circuit_manifest_sha256']/'manifest.json';manifestcheck(cm,d['circuit_manifest_sha256'])
 protected=load(P/'PRESERVATION_MANIFEST.json');check('protected_count',len(protected['files']),9170)
 for p,h in protected['files'].items():filecheck(ROOT/p,h)
 lock=load(P/'STAGE1_INPUT_LOCK.json');check('selected_runs',len(lock['inputs']),28)
 for row in lock['inputs']:
  for a in row['artifacts'].values():filecheck(ROOT/a['path'],a['sha256'])
 if phase.startswith('before'):
  prior=[str(p.relative_to(ROOT)) for p in (ROOT/'research').rglob('*') if 'stage5' in str(p.relative_to(ROOT)).lower() and (p.name in ['RESULTS.json','RESULTS.sha256'] or (p.is_dir() and ('runs' in p.name or 'results' in p.name)))]
  check('no_previous_stage5_result_directory_or_output',prior,[])
 # Preserve attempt 1 and verify its sealed record; never relabel it successful.
 attempt1=ROOT/'research/fly-stage5-preflight-evidence/73105536b60f57079bf5ef556d20c10f7194cba0650e70e77383291506cc7047'
 a1=load(attempt1/'RELEASE.json')
 check('attempt1_content_hash',hashlib.sha256(canonical(a1['files'])).hexdigest(),a1['content_sha256'])
 for p,h in a1['files'].items():
  filecheck(attempt1/p,h)
  filecheck(ROOT/'research/fly-stage5-execution-20260920'/p,h)
 a1status=load(attempt1/'EXECUTION_STATUS.json')
 check('attempt1_zero_units',a1status['evaluated_units'],0)
 check('attempt1_no_execution',a1status['execution_status'],'NOT STARTED')
 check('attempt1_zero_processes',a1status['fresh_process_count'],0)
 check('attempt1_recorded_no_source_value_reads',load(attempt1/'PRESERVATION_AFTER.json')['stage1_summary_values_read'],False)
 check('protocol_release_bytes_equal_attempt1',sha(P/'RELEASE.json'),load(attempt1/'INTEGRITY_BEFORE.json')['release_file_sha256'])
 check('authorized_release_hash',r['content_sha256'],'3fef9c2fad9b7b8be982c699299f957395199d811774041a052237efeb78ec3d')
 for c in report['checks']:
  if 'hash_object_type' not in c and (c['check']=='canonical_stage5_content_hash' or c['check'].endswith(' content')):
   c['hash_object_type']='RELEASE/CONTENT HASH';c['canonical_object']='compact sorted UTF-8 JSON file-hash map per owning release'
 report['attempt1_read_audit_scope']='Verified immutable records, command log and audit scripts; no retrospective OS file-access tracing is claimed.'
 report['passed']=not report['failures']
except Exception as e:
 report['passed']=False;report['failures'].append(type(e).__name__+': '+str(e))
out=HERE/('INTEGRITY_'+phase.upper()+'.json')
if out.exists():raise SystemExit('Refusing to overwrite an integrity record')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['phase','passed','failures']}));print('checks',len(report['checks']))
raise SystemExit(0 if report['passed'] else 1)
