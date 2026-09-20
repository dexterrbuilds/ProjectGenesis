"""Anatomy-only crosswalk; no fitting or old outcome inputs."""
from common import *
import csv,gzip,collections
import numpy as np
sys.path.insert(0,str(HERE/'vendor'))
import rdata
ROOT=HERE.parent.parent

def main():
 src=ROOT/'research/fly-stage4/data/column_assignment.csv.gz';ann=ROOT/'outputs/flywire-research/annotations-v3.1.0.tsv'
 with ann.open() as f:annotations={r['root_id']:r for r in csv.DictReader(f,delimiter='\t') if r['cell_type'].startswith(('T4','T5'))}
 with gzip.open(src,'rt') as f:rows=[r for r in csv.DictReader(f) if r['type'] in ['T4a','T4b','T4c','T4d','T5a','T5b','T5c','T5d']]
 new=[]
 for r in rows:
  ar=annotations.get(r['root_id']);new.append({**r,'root_id':str(r['root_id']),'annotation_v3_1_0_type':ar['cell_type'] if ar else None,'type_match':r['type']==ar['cell_type'] if ar else None,'lens_index':None,'retinal_direction':None,'experimental_screen_transform':None})
 with (HERE/'ROOT_COLUMN_CROSSWALK.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(new[0]));w.writeheader();w.writerows(new)
 e=rdata.read_rda(HERE/'data/eyemap.RData');med=rdata.read_rda(HERE/'data/med_ixy.RData')['med_ixy'];mapping=np.asarray(e['eyemap']);directions=np.asarray(e['ucl_rot_sm']);pos=np.asarray(e['med_xyz']);lattice={int(r[0]):r[1:] for r in np.asarray(med)};pairs=[]
 for i,(mi,lens) in enumerate(mapping):
  pairs.append({'Mi1_author_ordinal':int(mi),'lens_author_ordinal':int(lens),'root_id':None,'medulla_lattice_x':int(lattice[int(mi)][0]),'medulla_lattice_y':int(lattice[int(mi)][1]),'med_xyz':pos[i].tolist(),'author_rotated_unit_direction':directions[i].tolist(),'experimental_screen_transform':None})
 write('EYEMAP_LOCAL_MAP.json',{'source_commit':'99d2a43123db636cedb55af9ff31a59657e7d17e','coordinate_frame':'authors anatomy/microCT rotated frame, not electrophysiology screen','entries':pairs})
 conflicts=[r for r in new if r['type_match'] is False];missing=[r for r in new if r['type_match'] is None]
 write('COORDINATE_AUDIT.json',{'sources':{str(src.relative_to(ROOT)):sha(src),str(ann.relative_to(ROOT)):sha(ann),'data/eyemap.RData':sha(HERE/'data/eyemap.RData'),'data/med_ixy.RData':sha(HERE/'data/med_ixy.RData')},'column_assigned_T4T5':len(rows),'by_type_hemisphere':dict(collections.Counter(r['hemisphere']+'_'+r['type'] for r in rows)),'annotation_v3_1_0_T4T5':len(annotations),'type_conflicts':len(conflicts),'roots_missing_from_annotation_T4T5':len(missing),'conflict_examples':conflicts[:10],'eye_map_matched_columns':len(mapping),'medulla_columns':len(med),'microCT_lenses':len(e['lens_ixy']),'unit_vector_norm_range':[float(np.linalg.norm(directions,axis=1).min()),float(np.linalg.norm(directions,axis=1).max())],'auxiliary_boundary_points_excluded':len(e['eyemap_aux'])-len(mapping),'root_to_eye_join':'unresolved; author ordinal is not a FlyWire column ID','eye_to_recording_screen':'unresolved; individual experimental head pose/RF locations absent','chiasm_reflection':'explicit Y sign flip in authors proc_eyemap.R lines 129-131, anatomical not fitted','Stage4_outcomes_used':False,'uncertainty':'discrete identity/frame ambiguity and unquantified specimen/registration error; no fabricated degree confidence interval'})
 print(json.dumps({'root_columns':len(rows),'eye_columns':len(mapping),'conflicts':len(conflicts)}))
if __name__=='__main__':main()
