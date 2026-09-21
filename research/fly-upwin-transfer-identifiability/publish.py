from common import *
assert not (HERE/'RELEASE.json').exists(),'Do not overwrite a sealed release.'
assert load(HERE/'VALIDATION.json')['passed']
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
write('RELEASE.json',dict(id='alpha1-upwin-minimal-transfer-identifiability',version='1.0.0',files=files,content_sha256=content_hash(files),
 classification=load(HERE/'DESIGN_SUFFICIENCY.json')['classification'],scope='Conditional identifiability analysis only; Stage5 unauthorized; no biological parameter fit or evidence admission.',
 dependencies=load(HERE/'DEPENDENCIES.json'),total_bytes=sum((HERE/f).stat().st_size for f in files)))
print(load(HERE/'RELEASE.json')['content_sha256'])
