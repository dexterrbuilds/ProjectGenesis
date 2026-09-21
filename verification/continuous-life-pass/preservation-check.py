"""Read-only research/prior-package and canonical before/after comparison. No model imports."""
import hashlib,json
from pathlib import Path

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
base=Path('verification/continuous-life-pass')
frozen=json.load(open('outputs/awakening-preparation/FROZEN_BEFORE.json'))
failures=[p for p,h in frozen.items() if not Path(p).is_file() or sha(p)!=h]
prior={}
for name in ['completion-audit','foundation-repair','memory-pass','life-state-pass']:
 root=Path('verification')/name
 manifest=json.load(open(root/'ARTIFACT_MANIFEST.json'))
 prior[name]=[p for p,h in manifest['files'].items() if not (root/p).is_file() or sha(root/p)!=h]
before=json.load(open('outputs/continuous-life-pass/PRIVATE_BEFORE.json'))
after=json.load(open('outputs/continuous-life-pass/PRIVATE_POST_TEST.json'))
expected='4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220'
rows=after['rows'];o=rows['genesis_organisms'][0]['state'];life=rows['genesis_life_state'][0]['record']
result={'frozenFilesChecked':len(frozen),'frozenMismatches':failures,'priorPackages':prior,'beforeDigest':before['sha256'],'afterDigest':after['sha256'],'allCanonicalRowsIdentical':before['rows']==rows,'expectedDigestMatch':after['sha256']==expected,'organismId':o['id'],'bornAt':o['bornAt'],'decisions':len(rows['genesis_decisions']),'legacyMemories':len(rows['genesis_memories']),'canonicalV2Episodes':sum(r['record'].get('kind')=='episode' for r in rows['genesis_life_events']),'execution':life['executionLock'],'scheduleEnabled':rows['genesis_schedule'][0]['enabled'],'biology':life['biologicalContext']['mode'],'newContinuousTablesInstalled':any(k.startswith('genesis_continuous') or k=='genesis_runtime_events' for k in rows),'canonicalTableCounts':{k:len(v) for k,v in rows.items()}}
(base/'preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
if failures or any(prior.values()) or not result['allCanonicalRowsIdentical'] or not result['expectedDigestMatch'] or result['newContinuousTablesInstalled']:raise SystemExit(1)
