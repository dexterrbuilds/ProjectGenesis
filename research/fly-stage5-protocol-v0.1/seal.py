"""Seal protocol design only. Never execute the frozen prospective analysis."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
assert not (HERE/'RELEASE.json').exists(),'Do not overwrite a preregistered release.'
validation=json.loads((HERE/'DESIGN_VALIDATION.json').read_text());assert validation['passed']
files={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
h=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
release={'id':'genesis-stage5-prospective-protocol','version':'0.1.0','classification':'STAGE-5 PROTOCOL READY FOR EXECUTION REVIEW','design_authorized':True,'execution_authorized':False,'files':files,'content_sha256':h,'analysis_code_sha256':files['prospective_analysis.py'],'scope':'Protocol design only; no outcomes evaluated; separate execution review required.'}
(HERE/'RELEASE.json').write_text(json.dumps(release,indent=2,ensure_ascii=False)+'\n')
print(h)
