"""Read-only verification of this study and all frozen predecessor files."""
from common import *
import datetime,subprocess

def verify():
 checks={}
 for lock in ['PRIMARY_RESULT_LOCK.json','INTERFACE_FREEZE.json']:
  for n,h in read(lock)['files'].items():assert sha(HERE/n)==h,(lock,n)
  checks[lock]=True
 for n,h in read('NUMERIC_IDENTITY_CORRECTION.json')['old_files'].items():assert sha(HERE/'pre_numeric_identity_correction'/n)==h,n
 checks['initial_results_preserved']=True
 for n,h in read('SOURCE_INPUTS.json').items():assert sha(ROOT/n)==h,n
 checks['source_inputs_preserved']=True
 assert sha(HERE/'PROTOCOL.md')==read('REGISTRATION.json')['protocol_sha256']
 checks['preregistered_rules_unchanged']=True
 assert read('CANONICAL_BEFORE.json')==read('CANONICAL_AFTER.json')
 assert read('CANONICAL_AFTER.json')['tableRowCounts']['genesis_decisions']==7
 assert all(not x['enabled'] for x in read('CANONICAL_AFTER.json')['schedule'])
 checks['canonical_state_unchanged']=True
 frozen=read('FROZEN_BEFORE.json')
 failures=[n for n,h in frozen.items() if not (ROOT/n).is_file() or sha(ROOT/n)!=h]
 assert not failures,failures
 checks['protected_files']=len(frozen)
 assert set(read('ESTIMATOR_ACCESS.json'))=={'COVERAGE_ATLAS.json','atlas/records.json','atlas/waveforms.npz'}
 checks['estimator_input_firewall']=True
 a=read('STAGE4_SUPPORT_AUDIT.json');freeze=read('INTERFACE_FREEZE.json')
 assert a['interface_freeze_sha256']==sha(HERE/'INTERFACE_FREEZE.json')
 assert datetime.datetime.fromisoformat(a['at_utc'])>datetime.datetime.fromisoformat(freeze['at_utc'])
 assert a['Stage4_runs']==a['LPLC2_runs']==a['in_domain_count']==0 and a['count']==16
 checks['static_audit_after_freeze']=True
 replay=read('REPRODUCTION.json');assert all(replay['identical_json'].values()) and all(replay['identical_arrays'].values())
 checks['fresh_process_exact_replay']=True
 if (HERE/'PACKAGE_MANIFEST.json').exists():
  manifest=read('PACKAGE_MANIFEST.json');payload={k:v for k,v in manifest.items() if k!='content_sha256'}
  assert hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()==manifest['content_sha256']
  for n,h in manifest['files'].items():assert sha(HERE/n)==h,n
  checks['package_valid']=True
 return checks

if __name__=='__main__':print(json.dumps(verify(),indent=2))
