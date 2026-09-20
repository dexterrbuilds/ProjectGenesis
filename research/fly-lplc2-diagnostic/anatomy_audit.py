"""Static audit of frozen anatomy; no neural update, extraction, or model selection."""
from collections import Counter
import numpy as np
from common import HERE, ROOT, STAGE4, save, sha
import json

def run():
    base=ROOT/'research/fly-boundary-study/anatomy'
    nodes=json.loads((base/'nodes.json').read_text())
    pre=np.load(base/'pre.npy',mmap_mode='r');post=np.load(base/'post.npy',mmap_mode='r')
    count=np.load(base/'count.npy',mmap_mode='r')
    neuropil=np.load(base/'neuropil.npy',mmap_mode='r')
    labels=json.loads((base/'neuropil-labels.json').read_text())
    out={'scope':'read-only anatomical rows and unchanged Stage-4 coordinates; no response metrics',
         'source_contacts_sha256':'24f960ae3e7d4f8cd30db3b62e99fb5179cc3d1e76d8c155bfb441e9737d3faf',
         'levels':{}}
    for level in ('L0','L1'):
        path=STAGE4/f'circuits/{level}.json';c=json.loads(path.read_text());ns=c['nodes']
        selected={n['global_index'] for n in ns};groups={}
        for typ in sorted({n['cell_type'] for n in ns}):
            ids={n['global_index'] for n in ns if n['cell_type']==typ}
            edges=[e for e in c['edges'] if ns[e['post']]['cell_type']==typ]
            effective=sum(e['contacts'] for e in edges if e['sign'] is not None)
            full=c['boundary'][typ]['full_input']
            omitted=Counter();omitted_neuropil=Counter();missing_roots=set()
            inds=np.flatnonzero(np.isin(post,list(ids)))
            for j in inds:
                i=int(pre[j])
                if i not in selected:
                    omitted[nodes[i]['cell_type'] or '<unknown>']+=int(count[j])
                    omitted_neuropil[labels[int(neuropil[j])]]+=int(count[j]);missing_roots.add(nodes[i]['root_id'])
            retained=sum(e['contacts'] for e in edges)
            assert full==retained+sum(omitted.values())
            groups[typ]={'neurons':len(ids),'full_input_contacts':full,'retained_input_contacts':retained,
                'effective_input_contacts':effective,'effective_input_fraction':effective/full,
                'retained_unknown_operator_contacts':retained-effective,
                'omitted_input_contacts':sum(omitted.values()),'omitted_input_root_count':len(missing_roots),
                'omitted_by_type':dict(omitted.most_common()),'omitted_by_neuropil':dict(omitted_neuropil),
                'full_output_contacts':c['boundary'][typ]['full_output'],
                'output_retention':c['boundary'][typ]['output_retention']}
        geo=[]
        dirs={'a':(1.,0.),'b':(-1.,0.),'c':(0.,1.),'d':(0.,-1.)}
        for target in c['targets']:
            center=np.array(target['center_xy']); bytype=[]
            for typ in sorted(t for t in groups if t.startswith(('T4','T5'))):
                es=[e for e in c['edges'] if e['post_root_id']==target['root_id'] and ns[e['pre']]['cell_type']==typ]
                if not es:continue
                weights=np.array([e['contacts'] for e in es]); xy=np.array([ns[e['pre']]['column']['xy'] for e in es])
                centroid=np.average(xy,axis=0,weights=weights);radial=xy-center
                norm=np.linalg.norm(radial,axis=1);valid=norm>1e-12
                projection=radial@np.array(dirs[typ[-1]])
                bytype.append({'type':typ,'contacts':int(weights.sum()),'roots':len({e['pre_root_id'] for e in es}),
                    'centroid_grid_xy':centroid.tolist(),'centroid_from_center_grid_xy':(centroid-center).tolist(),
                    'mean_outward_alignment_assumed_grid':float(np.average(projection[valid]/norm[valid],weights=weights[valid])) if valid.any() else None})
            geo.append({'root_id':target['root_id'],'center_grid_xy':target['center_xy'],'afferents':bytype,
                'interpretation':'uncalibrated grid summary, NOT measured retinal direction or LPLC2 receptive-field centre'})
        n=len(ns);m=sum(n['cell_type'].startswith(('T4','T5')) for n in ns)
        out['levels'][level]={'frozen_circuit_sha256':sha(path),'counts':c['counts'],'populations':groups,
            'geometry':geo,'scalar_state_budget':{'neurons':n,'motion_cells':m,'rate_and_delay_float64_values':n+2*m,
                'bytes':8*(n+2*m),'excluded':'sparse operator, traces, Python overhead; not measured RAM'},
            'preserved_boundaries':c['boundary']}
    return out

if __name__=='__main__':
    out=run();save('ANATOMY_AUDIT.json',out)
    for l,v in out['levels'].items():
        print(l,{t:(p['effective_input_contacts'],p['full_input_contacts'],p['effective_input_fraction']) for t,p in v['populations'].items() if t in ('LPLC2','LPi09','LPi11')})
