"""Execution recorder only. Does not import or alter the sealed analysis."""
from pathlib import Path
import sys,os,subprocess,json,datetime,time,hashlib,resource
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'research/fly-stage5-protocol-v0.1'
n=sys.argv[1];assert n in ['1','2']
assert json.loads((H/'PREFLIGHT_GATE.json').read_text())['passed']
assert json.loads((H/'AUTHORIZATION_VERIFICATION.json').read_text())['AUTHORIZATION_HASH_MATCH']
a=H/'AUTHORIZATION.json';out=R/'research/fly-stage5-runs'/('attempt-2-process-'+n)
record=H/('PROCESS_'+n+'.json');assert not out.exists() and not record.exists()
if n=='2':
 # Check only execution status. Never reads process-1 scientific output.
 assert json.loads((H/'PROCESS_1.json').read_text())['exit_code']==0
cmd=[sys.executable,str(P/'prospective_analysis.py'),'--authorization',str(a),'--output',str(out)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
p=subprocess.run(cmd,cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'),capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat();elapsed=time.monotonic()-t
for kind,data in [('stdout',p.stdout),('stderr',p.stderr)]:
 dest=H/('PROCESS_'+n+'.'+kind+'.txt');assert not dest.exists();dest.write_bytes(data)
u=resource.getrusage(resource.RUSAGE_CHILDREN)
d={'attempt_id':'genesis-stage5-attempt-2-20260920','process':int(n),'argv':cmd,'cwd':str(R),'start_utc':start,'end_utc':end,'wall_seconds':elapsed,'exit_code':p.returncode,'env_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},'child_user_cpu_seconds':u.ru_utime,'child_system_cpu_seconds':u.ru_stime,'child_maxrss_native_units':u.ru_maxrss,'maxrss_units':'bytes on this Darwin host','stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'authorization_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'sealed_analysis_sha256':hashlib.sha256((P/'prospective_analysis.py').read_bytes()).hexdigest(),'output_directory':str(out),'scientific_output_not_inspected_by_recorder':True,'other_process_scientific_output_consumed':False}
record.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'process':n,'exit_code':p.returncode,'wall_seconds':elapsed,'stderr':p.stderr.decode()}))
raise SystemExit(p.returncode)
