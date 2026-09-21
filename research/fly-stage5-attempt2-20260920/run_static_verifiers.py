"""Only existing read-only release methods and sealed static tests. No model execution."""
from pathlib import Path
import subprocess,sys,os,json,datetime,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
py='/Users/mac/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
assert Path(py).is_file()
commands=[
 ('brain-spec-package',[sys.executable,'research/genesis-brain-spec-v0.2/check.py','--package-only']),
 ('route-release',[py,'research/fly-upwin-route-evidence/validate.py','Audit.test_15_release_if_present']),
 ('identity-release',[sys.executable,'research/fly-upwin-identity-mediation/validate.py','Audit.test_18_release_if_published']),
 ('identifiability-release',[sys.executable,'research/fly-upwin-transfer-identifiability/validate.py','Audit.test_19_release_if_sealed']),
 ('sealed-static-suite',[sys.executable,'research/fly-stage5-protocol-v0.1/validate_design.py'])]
records=[]
for name,cmd in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
 end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for kind,data in [('stdout',p.stdout),('stderr',p.stderr)]:
  dest=HERE/(name+'.'+kind+'.txt');assert not dest.exists();dest.write_bytes(data)
 record={'name':name,'argv':cmd,'cwd':str(ROOT),'start_utc':start,'end_utc':end,'exit_code':p.returncode,'env_override':{'PYTHONDONTWRITEBYTECODE':'1'},'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
 records.append(record);print(name,p.returncode,flush=True)
 if p.returncode:break
out=HERE/'AUTHORITATIVE_VERIFICATION.json';assert not out.exists()
out.write_text(json.dumps({'records':records,'passed':len(records)==len(commands) and all(r['exit_code']==0 for r in records),'source_summary_values_read':False,'stage1_verification':'All evidence payload and selected source hashes via corrected checker; no Stage-1 computational test executed.'},indent=2)+'\n')
raise SystemExit(0 if len(records)==len(commands) and all(r['exit_code']==0 for r in records) else 1)
