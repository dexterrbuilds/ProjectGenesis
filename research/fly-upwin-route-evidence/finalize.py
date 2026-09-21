"""Freeze acquisition/report package only, never amend Brain Spec."""
from common import *
import zipfile,subprocess,os,time
assert not (HERE/'RELEASE.json').exists(),'Already frozen'
urls={
'article.html':'https://elifesciences.org/articles/85756','article-text.txt':None,'figures.html':'https://elifesciences.org/articles/85756/figures','elife-79042.html':'https://elifesciences.org/articles/79042','elife-79042-figures.html':'https://elifesciences.org/articles/79042/figures','frontiers-1822122.html':'https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2026.1822122/full','elife-85756-fig3-figsupp1-v3.jpg':'https://iiif.elifesciences.org/lax:85756%2Felife-85756-fig3-figsupp1-v3.tif/full/1234,/0/default.jpg'}
rows=[]
for p in sorted((HERE/'sources').rglob('*')):
 if not p.is_file() or p.name.startswith('elife-85756-') and p.suffix=='.xlsx':continue
 u=urls.get(p.name)
 if p.name.startswith('elife-79042-') and p.suffix in ['.zip','.xlsx']:u='https://cdn.elifesciences.org/articles/79042/'+p.name
 row={'path':str(p.relative_to(HERE)),'sha256':sha(p),'bytes':p.stat().st_size,'url':u,'source_scope':'authoritative original' if u else 'HTML-derived text or byte-preserved embedded archive member; parent provenance below'}
 if p.suffix in ['.zip','.xlsx']:
  with zipfile.ZipFile(p) as z:row['zip_crc_verified']=z.testzip() is None
 if p.parent.name=='79042-alpha1':row['parent_archive']='sources/elife-79042-fig3-figsupp2-data1-v2.zip';row['member_path']='79042_Figure_3-figuresupplement2_source_data/'+p.name
 rows.append(row)
write('AUXILIARY_SOURCES.json',{'files':rows,'acquisition_limits':'Author-hosted summarized figure values do not constitute full raw trial/image/trajectory datasets. Missing metadata never inferred.','license_scope':'eLife article Creative Commons Attribution; original source workbook attribution preserved; frontiers article consulted for anatomical hypothesis only','resumed_download':'79042 fig3-data1 initial timeout after22347776 of51284239 bytes; completed by HTTP resume and ZIP CRC verification'})
start=time.perf_counter();r=subprocess.run([PYTHON,str(HERE/'validate.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(HERE/'TEST_LOG.txt').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
write('VERIFICATION.json',{'valid':True,'tests':15,'adversarial_test_families':5,'protected_files':len(load(HERE/'FROZEN_BEFORE.json')),'changed_protected_files':[],'canonical_sha256':load(HERE/'CANONICAL_AFTER.json')['sha256'],'canonical_cycles':7,'schedule_enabled':False,'neural_runs':0,'model_fits':0,'stage5_protocol_created':False,'source_workbooks':36,'source_cells':sum(s['actual_populated_cells'] for w in load(HERE/'WORKBOOK_INVENTORY.json') for s in w['sheets']),'elapsed_validation_seconds':time.perf_counter()-start,'at_utc':now()})
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='RELEASE.json'}
write('RELEASE.json',{'id':'alpha1-upwin-route-evidence-acquisition','version':'1.0.0','classification':load(HERE/'READINESS.json')['classification'],'spec_registry_sha256':SPEC_SHA,'spec_package_sha256':PACKAGE_SHA,'files':files,'content_sha256':hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'total_bytes':sum((HERE/f).stat().st_size for f in files),'scope':'evidence only; no capability admission or Stage5 authorization'})
print(json.dumps({'valid':True,'content_sha256':load(HERE/'RELEASE.json')['content_sha256'],'files':len(files)}))
