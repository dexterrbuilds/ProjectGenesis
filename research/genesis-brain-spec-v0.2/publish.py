"""Publish local immutable specification artifacts after governance/preservation checks."""
from common import *
import os,sys,subprocess
from check import check_content,check_published
assert not (HERE/'RELEASE.json').exists(),'Do not overwrite published release'
proc=subprocess.run([sys.executable,str(HERE/'test_governance.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(HERE/'TEST_LOG.txt').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stderr
verified=check_content();verified.update(at_utc=now(),governance_tests=12,test_exit_code=proc.returncode);write('VERIFICATION.json',verified)
names=['ADMISSION_REVIEWS.json','APPEND_ONLY_DIFF.json','CAPABILITY_REGISTRY.json','CANONICAL_IDENTITY_REFERENCES.json','RESEARCH_LINEAGE.json','SENSORY_BOUNDARY_CONTRACT.json','STAGE5_READINESS.json','RELEASE_GOVERNANCE.json','REVIEW_AUTHORIZATION.md','GENESIS_BRAIN_SPEC.md','SENSORY_BOUNDARY_CONCEPT.md','STAGE5_READINESS.md','LITERATURE_READINESS_AUDIT.json','DEPENDENCY_VERIFICATION.json','VERIFICATION.json']
release={'version':'0.2.0','published_at_utc':now(),'publication':'local repository evidence release; no external deployment','registry':load(HERE/'REGISTRY_POINTER.json'),'parent':{'version':'0.1.0','registry_sha256':BASE_SHA,'release_path':'research/genesis-brain-spec-v0.1/RELEASE.json','release_file_sha256':sha(BASE/'RELEASE.json')},'inherited_artifact_base':'research/genesis-brain-spec-v0.1','components':{n:{'path':n,'sha256':sha(HERE/n)} for n in names},'new_biological_capabilities':0,'runtime_implementation':False,'Stage5_authorized':False}
write('RELEASE.json',release)
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE_MANIFEST.json'}
package={'version':'0.2.0','registry_sha256':release['registry']['sha256'],'parent_registry_sha256':BASE_SHA,'files':files};package['content_sha256']=digest(package);write('PACKAGE_MANIFEST.json',package)
print(json.dumps(check_published(),indent=2))
