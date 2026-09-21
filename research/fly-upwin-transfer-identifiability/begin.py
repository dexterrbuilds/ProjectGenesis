from common import *
assert not (HERE/'DEPENDENCIES.json').exists(), 'Do not restart an existing analysis.'
protected=load(IDENTITY/'PRESERVATION_BEFORE.json')
for p in IDENTITY.rglob('*'):
 if p.is_file():protected[str(p.relative_to(ROOT))]=sha(p)
errors=[p for p,h in protected.items() if sha(ROOT/p)!=h]
assert not errors,errors
write('PRESERVATION_BEFORE.json',protected)
pins={}
for name,folder,expected in [('route',ROUTE,'597e6c06bed21fda6ccf62959aacf83fda4aa7adc0f85fcd29453e5ac961f56c'),('identity',IDENTITY,'a2fafc15ff7be4f599c38e332d34bb7d4d573ebf8d90d4d9788c26912d990a56')]:
 r=load(folder/'RELEASE.json');assert r['content_sha256']==expected
 assert hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==expected
 for p,h in r['files'].items():assert sha(folder/p)==h,p
 pins[name]=dict(path=str(folder.relative_to(ROOT)),content_sha256=expected,release_sha256=sha(folder/'RELEASE.json'))
reg='23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88'
assert sha(SPEC/'objects'/f'{reg}.json')==reg
pins['spec']=dict(path=str(SPEC.relative_to(ROOT)),registry_sha256=reg,release_sha256=sha(SPEC/'RELEASE.json'),package_sha256='9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b')
pins['stage1']=dict(path=str(STAGE1.relative_to(ROOT)),classification='PASS (narrow appetitive model)',files={str(p.relative_to(STAGE1)):sha(p) for p in sorted(STAGE1.rglob('*')) if p.is_file()})
write('DEPENDENCIES.json',dict(packages=pins,protected_file_count=len(protected),scientific_inputs_only=list(pins),new_literature_sources=[],evidence_overrides=[],state_ownership=[],stage5_authorized=False))
print(json.dumps(dict(verified=True,protected_files=len(protected))))
