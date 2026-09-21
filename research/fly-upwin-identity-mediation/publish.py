"""Seal this evidence package after validation; never admit evidence into Brain Spec."""
from common import *
assert not (HERE/'RELEASE.json').exists(), 'Release already sealed; do not overwrite.'
assert load(HERE/'VALIDATION.json')['passed']
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
write('RELEASE.json',dict(id='alpha1-upwin-identity-and-mediation-resolution',version='1.0.0',
 classification=load(HERE/'READINESS.json')['classification'],dependencies=load(HERE/'DEPENDENCIES.json'),
 files=files,content_sha256=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 total_bytes=sum((HERE/p).stat().st_size for p in files),scope='Evidence resolution only; unadmitted; Stage5 unauthorized.'))
print(load(HERE/'RELEASE.json')['content_sha256'])
