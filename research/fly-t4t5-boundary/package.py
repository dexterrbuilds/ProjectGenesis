"""Content-address completed study outputs; reference large public source artifacts separately."""
from common import *
exclude_dirs={'vendor','replay','.mpl-cache','__pycache__','Figure2.parts'}
files={}
for p in sorted(HERE.rglob('*')):
 rel=p.relative_to(HERE)
 if not p.is_file() or any(x in exclude_dirs for x in rel.parts) or p.name=='PACKAGE_MANIFEST.json':continue
 if p.suffix in ['.zip','.part','.incoming','.headers']:continue
 if rel.parts[:2]==('data','wholecell') and p.suffix=='.mat':continue
 if p.name.endswith('_LOG.txt'):continue
 if p.name in ['acquisition-resume.log','SUMMARY_LOG.json','POLARITY_SUMMARY_LOG.txt']:continue
 files[str(rel)]=sha(p)
large={}
for name in ['data/Figure2.zip','data/wholecell/singleBarStT4.mat','data/wholecell/singleBarStT5.mat']:
 p=HERE/name;large[name]={'bytes':p.stat().st_size,'sha256':sha(p)}
content=hashlib.sha256(json.dumps({'files':files,'large_sources':large},sort_keys=True,separators=(',',':')).encode()).hexdigest()
write('PACKAGE_MANIFEST.json',{'version':'0.1.0','classification':'PARTIAL VISUAL BOUNDARY CONSTRAINT','content_sha256':content,'files':files,'large_sources':large,'excluded':'vendor/runtime caches, fresh-process duplicate outputs, transport chunks/logs and incomplete duplicate 2019 archive; these are not fitted measurements','brain_spec_registry_sha256':'6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e'})
print(json.dumps({'files':len(files),'large_sources':len(large),'content_sha256':content}))
