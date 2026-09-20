"""Read-only evidence/release checks; no neural execution."""
from governance import *
import argparse

def check_content():
 r=registry();check_registry(r,load(HERE/'ADMISSION_REVIEWS.json'))
 check_capabilities(load(HERE/'CAPABILITY_REGISTRY.json'));check_identity(load(HERE/'CANONICAL_IDENTITY_REFERENCES.json'));check_sensory(load(HERE/'SENSORY_BOUNDARY_CONTRACT.json'))
 expected={'stage4':'Gate A NOT SUPPORTED for frozen model; Gate B NOT TESTED','diagnostic':'PARTIAL MECHANISTIC CONSTRAINT — MORE DATA REQUIRED','boundary':'PARTIAL VISUAL BOUNDARY CONSTRAINT','empirical':'LIMITED EMPIRICAL INTERFACE SUPPORTED'}
 lineage=load(HERE/'RESEARCH_LINEAGE.json')
 require({x['id']:x['classification'] for x in lineage['nodes']}==expected,'Frozen classification changed')
 for n in lineage['nodes']:require(n['package']['content_sha256']==PACKAGES[n['id']][1],'Lineage dependency mismatch')
 readiness=load(HERE/'STAGE5_READINESS.json')
 require(readiness['classification']=='PARTIAL READINESS — TARGETED EVIDENCE REQUIRED','Unreviewed readiness promotion')
 require(not readiness['experiment_authorized'] and not readiness['protocol_designed'] and readiness['neural_runs']==0,'Stage 5 authorized/designed/executed')
 require(all(p.get('sign',{'state':'unknown','value':None})['state']=='unknown' for p in readiness['candidate_pathways']),'Candidate root sign silently assigned')
 a=load(HERE/'CANONICAL_BEFORE.json');b=load(HERE/'CANONICAL_AFTER.json');require(a==b,'Canonical Genesis state changed')
 require(b['tableRowCounts']['genesis_decisions']==7 and all(not s['enabled'] for s in b['schedule']),'Canonical preservation invariant')
 packages=verify_packages()
 preserved=load(HERE/'PRESERVATION_BEFORE.json')
 for name,h in preserved.items():require(sha(ROOT/name)==h,'Protected artifact changed: '+name)
 return {'valid':True,'v01_byte_preserved':True,'verified_packages':packages,'protected_files':len(preserved),'registry_sha256':digest(r),'inherited_entries':151,'appended_claims':11,'canonical_database_sha256':b['sha256'],'canonical_cycles':7,'schedule_enabled':False,'neural_runs':0,'stage5_authorized':False}

def check_published():
 release=load(HERE/'RELEASE.json');require(release['version']=='0.2.0','Release version')
 require(release['parent']['registry_sha256']==BASE_SHA,'Parent mismatch')
 require(sha(ROOT/release['parent']['release_path'])==release['parent']['release_file_sha256'],'Historical release bytes changed')
 require(sha(HERE/release['registry']['path'])==release['registry']['sha256']==digest(registry()),'Release registry mismatch')
 for ref in release['components'].values():require(sha(HERE/ref['path'])==ref['sha256'],'Release component changed')
 m=load(HERE/'PACKAGE_MANIFEST.json');require(digest({k:v for k,v in m.items() if k!='content_sha256'})==m['content_sha256'],'Package content address')
 for path,h in m['files'].items():require(sha(HERE/path)==h,'Release package file changed: '+path)
 return {'published_package_valid':True,'version':release['version'],'registry_sha256':release['registry']['sha256'],'package_sha256':m['content_sha256'],'files':len(m['files'])}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--package-only',action='store_true');a=p.parse_args()
 result={} if a.package_only else check_content()
 result.update(check_published());print(json.dumps(result,indent=2))
