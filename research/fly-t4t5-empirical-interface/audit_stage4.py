"""Post-freeze static stimulus audit. No imports/execution of Stage 4 or LPLC2."""
from common import *
import ast,datetime
freeze=read('INTERFACE_FREEZE.json')
for n,h in freeze['files'].items():assert sha(HERE/n)==h,n
source=ROOT/'research/fly-stage4/model.py';run=ROOT/'research/fly-stage4/run.py'
# Parse source as text only. Extract physical Movie and stimulus-name list.
tree=ast.parse(source.read_text());movie=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Movie')
run_tree=ast.parse(run.read_text());primary=next(ast.literal_eval(n.value) for n in run_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PRIMARY' for t in n.targets))
rows=[]
for kind in primary:
 reasons=['No source-screen/head/retinal transform into the catalog RF/PD pixel frame','No measured full physical tuple for this stimulus','Somatic voltage cannot be converted to root-specific terminal output']
 if kind.startswith('grating_'):family='2-D angular drifting grating';detail='20 degree period; 20 degree/s phase motion; 50 by 50 degree aperture; orientations 0/90/180/270; 2 s duration';reasons.append('Catalog gratings have finite literal source-pixel patterns; a family-name match is not a physical-tuple match')
 elif kind.startswith('approach_'):family='angular approach disc';detail='l/v '+kind.split('_')[1]+' ms; diameter 5 to 60 degrees from 2 atan(l/v / time-to-collision)';reasons.append('No approach/expanding-disc voltage family measured')
 elif kind=='translate':family='2-D angular moving rectangle';detail='10 by 60 degrees; x center -40 to 40 degrees at 20 degree/s for 4 s';reasons.append('Measured source-pixel bars do not identify this 2-D angular trajectory')
 elif kind=='dim':family='area-matched dimming';detail='60 degree circular aperture; intensity .5*(1-diameter^2/3600)';reasons.append('No matching gradual luminance-control family')
 elif kind=='blank':family='constant gray';detail='intensity .5';reasons.append('Baseline-subtracted zero is not an independently measured blank-stimulus waveform')
 else:
  family='angular disc';detail={'expand':'dark diameter 5 to 60 degrees at 20 degree/s','recede':'dark diameter 60 to 5 degrees at 20 degree/s','bright':'bright diameter 5 to 60 degrees at 20 degree/s','small':'dark diameter 5 to 30 degrees','offset':'dark expanding disc center shifted 40 degrees','shuffle_time':'temporally permuted expanding-disc samples'}.get(kind,kind)
  reasons.append('No matching 2-D curved-edge/expansion/recession/time-permutation family')
 rows.append({'source_condition':kind,'physical_family':family,'physical_description':detail,'support':'OUT OF DISTRIBUTION / UNKNOWN','reasons':reasons})
write('STAGE4_SUPPORT_AUDIT.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'interface_freeze_sha256':sha(HERE/'INTERFACE_FREEZE.json'),'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [source,run]},'source_scope':'Static AST/text only: Movie physical stimulus class and PRIMARY names. No trial/model execution, response outputs or model scores.','primary_conditions':rows,'in_domain_count':0,'count':len(rows),'interface_modified_after_audit':False,'Stage4_runs':0,'LPLC2_runs':0})
write('STAGE4_SOURCE_EXCERPT.json',{'physical_movie_source':ast.get_source_segment(source.read_text(),movie),'PRIMARY':primary})
print('Static audit:',len(rows),'conditions; all UNKNOWN; zero simulations.')
