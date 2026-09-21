from common import *
import subprocess,os
assert not (HERE/'FROZEN_BEFORE.json').exists()
old=load(SPEC/'PRESERVATION_BEFORE.json')
for p in SPEC.rglob('*'):
 if p.is_file():old[str(p.relative_to(ROOT))]=sha(p)
for p,h in old.items():assert sha(ROOT/p)==h,p
write('FROZEN_BEFORE.json',old)
p=subprocess.run([str(ROOT/'.local/fly-stage1-venv/bin/python'),str(SPEC/'check.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));assert p.returncode==0,p.stderr
v=json.loads(p.stdout);assert v['registry_sha256']==SPEC_SHA and v['package_sha256']==PACKAGE_SHA
write('SPEC_VALIDATION.json',v)
r=load(SPEC/'objects'/f'{SPEC_SHA}.json');ids=['plasticity.appetitive-model','connection.KC.MBON07','connection.KC.MBON11','representation.heterogeneous','anatomy.pinned','crosswalk.type','visual.empirical.observation']
write('DEPENDENCIES.json',{'id':'alpha1.upwin.route.evidence-acquisition','registry_sha256':SPEC_SHA,'package_sha256':PACKAGE_SHA,'dependencies':{i:r['entry_hashes'][i] for i in ids},'evidence_overrides':[],'capability_promotions':[],'result_claims':[],'state_ownership':[],'input_channels':[],'stage5_authorized':False,'neural_runs':0,'fitting':False})
write('DEPENDENCY_LOCK.json',{'at_utc':now(),'protected_files':len(old),'spec_registry_sha256':SPEC_SHA,'spec_package_sha256':PACKAGE_SHA,'canonical_expected_sha256':'3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312'})
print('Pinned v0.2; protected files:',len(old))
