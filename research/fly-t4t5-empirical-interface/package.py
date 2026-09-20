from common import *
import datetime
out=HERE/'PACKAGE_MANIFEST.json';assert not out.exists(),'Refuse to rewrite completed package'
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and '.mpl' not in p.parts and p.name!='PACKAGE_MANIFEST.json'}
payload={'study':'T4/T5 Empirical Sensory Interface Feasibility','version':'0.1.0','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classification':'LIMITED EMPIRICAL INTERFACE SUPPORTED','brain_spec_sha256':read('DEPENDENCIES.json')['registry_sha256'],'files':files}
payload['content_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest();write('PACKAGE_MANIFEST.json',payload)
print(json.dumps({'files':len(files),'content_sha256':payload['content_sha256']}))
