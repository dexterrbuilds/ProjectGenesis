"""ZIP metadata/identity audit of frozen sources; no re-fitting or waveform reconstruction."""
from common import *
import zipfile,xml.etree.ElementTree as ET
records=[]
for stem in ['fig4-data1','fig4-data2','fig4-data3','fig5-data1','fig5-data2','fig5-data3','fig5-figsupp2-data1','fig5-figsupp2-data2','fig5-figsupp2-data3']:
 p=PRIOR/'sources'/f'elife-85756-{stem}-v3.xlsx'
 with zipfile.ZipFile(p) as z:
  names=z.namelist();meta={}
  for n in ['docProps/core.xml','docProps/app.xml']:
   if n in names:meta[n]={e.tag.split('}')[-1]:e.text for e in ET.fromstring(z.read(n)).iter() if e.text and e.text.strip()}
  artifact_names=[n for n in names if any(s in n.lower() for s in ['comment','drawing','media/','embedding','externalLink','customxml','person'])]
  records.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'archive_members':names,'document_properties':meta,'candidate_morphology_or_identity_parts':artifact_names,'interpretation':'Document creator/save time/software properties are not animal or cell identities. No acquisition timestamp may be inferred from save date.'})
m=load(PRIOR/'MEASUREMENT_AUDIT.json');alpha=next(w for w in m['whole_cell'] if 'fig4-data2' in w['file']);responders=[]
for t in alpha['traces']:
 if t['paper_responder']:responders.append({'source_workbook':alpha['file'],'source_column':t['column'],'source_label':t['source_label'],'waveform_numeric_sha256':t['numeric_sha256'],'published_response':'inhibitory voltage response to alpha1 optostimulation','driver':'R64A11-LexA','mapping_classification':'UNRESOLVED','identified_cell_type':None,'identified_FlyWire_root':None,'recording_to_morphology_link':None,'reason':'No per-recording identifier joins the column to deposited microscopy specimens; connectivity is not an identifier.'})
recall=[]
for c in m['conditioning']:
 for o in c['observations']:recall.append({'source_workbook':c['file'],'row':o['source_row'],'source_label':o['source_label'],'pre_post_pairing':'same published scalar row; author reports neuron-level repeated measurements','external_recording_id':None,'fly_id':None,'mapping_classification':'UNRESOLVED','cell_type':None,'root':None,'morphology_link':None})
write('SOURCE_IDENTITY_AUDIT.json',{'archives':records,'four_responders':responders,'recall_records':recall,'prior_numeric_results_unchanged':True,'individuals_inferred_from_row_order':False})
print('Audited',len(records),'ZIP metadata inventories; four responder locators; recall rows',len(recall))
