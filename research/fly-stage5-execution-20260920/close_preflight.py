"""Close a failed preflight; never executes prospective analysis or reads source values."""
from pathlib import Path
import json,hashlib,datetime,platform,sys,os
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;P=ROOT/'research/fly-stage5-protocol-v0.1'
def load(p):return json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4194304):h.update(b)
 return h.hexdigest()
def write(n,d):
 p=HERE/n
 if p.exists():raise RuntimeError('Refusing overwrite: '+n)
 p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
r=load(P/'RELEASE.json');protected=load(P/'PRESERVATION_MANIFEST.json')['files']
failures=[p for p,h in protected.items() if sha(ROOT/p)!=h]
failures += ['protocol/'+p for p,h in r['files'].items() if sha(P/p)!=h]
before=load(HERE/'INTEGRITY_BEFORE.json')
if sha(P/'RELEASE.json')!=before['release_file_sha256']:failures.append('protocol RELEASE.json')
a=load(HERE/'CANONICAL_BEFORE.json');b=load(HERE/'CANONICAL_AFTER.json')
if a!=b or b!=load(P/'CANONICAL_AFTER.json'):failures.append('canonical database audit')
write('PRESERVATION_AFTER.json',{'passed':not failures,'failures':failures,'protected_file_count':len(protected),'sealed_protocol_artifacts':len(r['files']),'release_file_unchanged':sha(P/'RELEASE.json')==before['release_file_sha256'],'canonical_before_equals_after':a==b,'canonical_matches_frozen':b==load(P/'CANONICAL_AFTER.json'),'canonical_database_sha256':b['sha256'],'decisions':b['tableRowCounts']['genesis_decisions'],'schedule':b['schedule'],'neural_runs':0,'stage5_analysis_processes':0,'stage1_summary_values_read':False,'runtime_actions':0,'wallet_actions':0,'brain_adapter_modified':False})
write('ENVIRONMENT.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_version':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'machine':platform.machine(),'cpu_count':os.cpu_count(),'bytecode_disabled':os.environ.get('PYTHONDONTWRITEBYTECODE'),'environment_secrets_recorded':False})
write('PREFLIGHT_ERROR_EXPLANATION.json',{'error_owner':'new auxiliary preflight checker; not sealed prospective_analysis.py','incorrect_operation':'Compared SHA256(PACKAGE_MANIFEST.json bytes) to DEPENDENCIES.json package_sha256. These identify different objects.','actual_raw_manifest_sha256':'e961f9105e0101ab110503386b158d3548acf62962ea23c885caa4d1ae64869c','pinned_package_content_sha256':'9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b','authoritative_definition':'research/genesis-brain-spec-v0.2/check.py check_published(): digest(manifest excluding content_sha256)','authoritative_verifier_observed':{'command':['python3','research/genesis-brain-spec-v0.2/check.py','--package-only'],'PYTHONDONTWRITEBYTECODE':'1','exit_code':0,'stdout':{'published_package_valid':True,'version':'0.2.0','registry_sha256':'23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88','package_sha256':'9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b','files':32}},'conclusion':'Auxiliary comparison error; no actual dependency or sealed-file corruption established. Initial failed record and erroneous checker retained without overwrite. Execution remains stopped under user stop-on-failed-check requirement.','sealed_protocol_repaired':False,'authorization_written':False,'analysis_executed':False})
write('EXECUTION_STATUS.json',{'sealed_stage5_release_hash':r['content_sha256'],'authorization_referenced_hash':None,'authorization_hash_match':'NOT VERIFIED — record not created before stop','pre_execution_integrity':'STOPPED — auxiliary checker error; 17/17 sealed static tests passed; all actual protected/sealed file comparisons passed','execution_status':'NOT STARTED','fresh_process_count':0,'reproducibility':'NOT TESTED','planned_units':224,'evaluated_units':0,'planned_runs':28,'families':['E','Z','P','R','WP','WR','H','U','N'],'source_dependence_gates':{'P':'UNASSESSABLE','R':'UNASSESSABLE'},'scientific_classifications':None,'scientific_interpretation_permitted':False,'null_compatibility_result':None,'transfer_sensitivity_result':None,'robust_invariants_established':[],'failure':'Auxiliary preflight compared a package content hash against a raw manifest file hash. No scientific run or failed biological control occurred.','preservation_passed':not failures,'next_step_automatic':False})
print(json.dumps({'preservation_passed':not failures,'protected_files':len(protected),'stage5_executed':False}))
