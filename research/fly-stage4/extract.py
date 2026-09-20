"""Outcome-blind anatomy extraction. No neural simulation imports."""
import collections
import csv
import gzip
import json
import time
import resource
import numpy as np
from scipy import sparse
from common import HERE, ROOT, ANATOMY, REGISTRY, sha, save, load, digest


def main():
    started = time.perf_counter()
    registration = load('PREREGISTRATION.json')
    assert sha(HERE/'PROTOCOL.md') == registration['protocol_sha256']
    assert sha(HERE/'DEPENDENCIES.json') == registration['dependencies_sha256']
    for rel, h in json.load(open(ANATOMY/'manifest.json'))['files'].items():
        p = ROOT/rel if (ROOT/rel).exists() else ANATOMY/rel
        assert sha(p) == h, str(p)
    nodes = json.load(open(ANATOMY/'nodes.json'))
    roots = {n['root_id']: i for i, n in enumerate(nodes)}
    columns = list(csv.DictReader(gzip.open(HERE/'data/column_assignment.csv.gz', 'rt')))
    mapped = {}
    conflicts = []
    for c in columns:
        if c['root_id'] not in roots:
            continue
        i = roots[c['root_id']]
        if c['type'] != nodes[i]['cell_type'] or c['hemisphere'] != nodes[i]['side']:
            conflicts.append({'root_id':c['root_id'], 'column_type':c['type'], 'annotation':nodes[i]})
            continue
        p,q = float(c['p']), float(c['q'])
        mapped[i] = dict(c, xy=[float(np.sqrt(3)/2*(q-p)), -(p+q)/2])
    motion = {i for i,n in enumerate(nodes) if n['side']=='right' and n['cell_type'] in
              ['T4a','T4b','T4c','T4d','T5a','T5b','T5c','T5d'] and i in mapped}
    m = sparse.load_npz(ANATOMY/'contacts.npz').tocsc()
    def afferents(targets, allowed):
        return set(m[:,list(targets)].nonzero()[0]) & allowed
    center = np.median([mapped[i]['xy'] for i in sorted(motion)], axis=0)
    ranking = []
    for i,n in enumerate(nodes):
        if n['side']!='right' or n['cell_type']!='LPLC2':
            continue
        inputs = sorted(afferents([i],motion))
        if not inputs:
            continue
        weights = m[inputs,i].toarray().ravel()
        xy = np.average([mapped[j]['xy'] for j in inputs], axis=0, weights=weights)
        ranking.append({'root_id':n['root_id'], 'index':i,'center_xy':xy.tolist(),
                        'center_distance':float(np.linalg.norm(xy-center)), 'mapped_motion_contacts':int(weights.sum())})
    ranking.sort(key=lambda x:(x['center_distance'],x['root_id']))
    selected = ranking[:3]
    targets = {x['index'] for x in selected}
    pre = np.load(ANATOMY/'pre.npy', mmap_mode='r')
    post = np.load(ANATOMY/'post.npy', mmap_mode='r')
    count = np.load(ANATOMY/'count.npy', mmap_mode='r')
    neuropil = np.load(ANATOMY/'neuropil.npy', mmap_mode='r')
    labels = json.load(open(ANATOMY/'neuropil-labels.json'))
    fi,fo = [np.load(ANATOMY/(s+'.npy')) for s in ('full_input','full_output')]
    source_sha = '24f960ae3e7d4f8cd30db3b62e99fb5179cc3d1e76d8c155bfb441e9737d3faf'
    prior_ids = set()
    with gzip.open(ROOT/'research/fly-representation-study/identity-registry.jsonl.gz','rt') as f:
        for line in f:
            prior_ids.add(json.loads(line)['id'])
    levels = {}
    for level,classes in [('L0',{'LPi11'}),('L1',{'LPi11','LPi09'})]:
        allowed = {i for i,n in enumerate(nodes) if n['side']=='right' and n['cell_type'] in classes}
        lpi = afferents(targets,allowed)
        keep = sorted(map(int, targets | lpi | afferents(targets|lpi,motion)))
        local = {g:i for i,g in enumerate(keep)}
        mask = np.zeros(len(nodes),bool); mask[keep]=True
        rows = np.flatnonzero(mask[pre]&mask[post])
        retained_in = np.bincount(post[rows],weights=count[rows],minlength=len(nodes))
        retained_out = np.bincount(pre[rows],weights=count[rows],minlength=len(nodes))
        outnodes=[]
        for i in keep:
            n = dict(nodes[i],global_index=i,canonical_id='FAFB-FlyWire:783:'+nodes[i]['root_id'],
                     full_input_contacts=int(fi[i]),full_output_contacts=int(fo[i]),
                     retained_input_contacts=int(retained_in[i]),retained_output_contacts=int(retained_out[i]),
                     local_state={'representation':'scalar_rate_like','category':'ENGINEERING ASSUMPTION',
                                  'physiological_units':'unknown','compartment_map':'unknown'},
                     column=mapped.get(i), root_receptor_map='unknown')
            outnodes.append(n)
        edges=[]; operators=collections.Counter(); overlaps=0
        for r in rows:
            a,b = int(pre[r]), int(post[r]); at,bt = nodes[a]['cell_type'],nodes[b]['cell_type']
            op,sign = 'unknown_excluded',None
            if a in motion and (b in targets or b in lpi):
                op,sign='class_motion_excitation',1
            elif a in lpi and b in targets:
                op,sign=('LPi11_supported_class_inhibition' if at=='LPi11' else 'LPi09_hypothesized_inhibition'),-1
            npname=labels[int(neuropil[r])]
            cid = digest(['FAFB-FlyWire:783',source_sha,'FAFB-FlyWire:783:'+nodes[a]['root_id'],
                          'FAFB-FlyWire:783:'+nodes[b]['root_id'],npname])
            overlaps+=cid in prior_ids
            edges.append({'id':cid,'pre':local[a],'post':local[b], 'pre_root_id':nodes[a]['root_id'],
                          'post_root_id':nodes[b]['root_id'],'neuropil':npname,'contacts':int(count[r]),
                          'operator':op,'sign':sign,'sign_scope':'class-level conditional model; root-specific receptors unknown',
                          'anatomy_ownership':'reference_existing' if cid in prior_ids else 'unadmitted_extension_reference'})
            operators[op]+=int(count[r])
        boundary={}
        for typ in sorted({n['cell_type'] for n in outnodes}):
            members=[i for i in keep if nodes[i]['cell_type']==typ]
            incoming=np.flatnonzero(np.isin(post,members)&~mask[pre])
            outgoing=np.flatnonzero(np.isin(pre,members)&~mask[post])
            def omitted(indices,side):
                totals=collections.Counter()
                for r in indices:
                    partner=int(pre[r] if side=='input' else post[r])
                    totals[nodes[partner]['cell_type'] or nodes[partner]['cell_class'] or 'untyped']+=int(count[r])
                return [{'type':t,'contacts':n} for t,n in totals.most_common(20)]
            x,y=int(fi[members].sum()),int(fo[members].sum())
            boundary[typ]={'neurons':len(members),'full_input':x,'retained_input':int(retained_in[members].sum()),
                           'input_retention':float(retained_in[members].sum()/x) if x else None,
                           'full_output':y,'retained_output':int(retained_out[members].sum()),
                           'output_retention':float(retained_out[members].sum()/y) if y else None,
                           'omitted_input_contacts':int(count[incoming].sum()),'omitted_output_contacts':int(count[outgoing].sum()),
                           'major_omitted_inputs':omitted(incoming,'input'),'major_omitted_outputs':omitted(outgoing,'output')}
        circuit={'level':level,'nodes':outnodes,'edges':edges,'targets':selected,
                 'boundary':boundary,'counts':{'neurons':len(keep),'directed_pairs':len({(e['pre'],e['post']) for e in edges}),
                 'neuropil_rows':len(edges),'anatomical_contacts':sum(e['contacts'] for e in edges),
                 'operator_contacts':dict(operators),'existing_canonical_rows_referenced':overlaps},
                 'unknown_operator_policy':'retained in anatomy; no numerical current assigned, not known physiological zero'}
        save(f'circuits/{level}.json',circuit)
        levels[level]={'sha256':sha(HERE/f'circuits/{level}.json'),'counts':circuit['counts'],'boundary':boundary}
    # Anatomical feasibility only. No descending activation computed here.
    routes=[]
    for j,n in enumerate(nodes):
        if n['cell_type']=='DNp01':
            ins=m[:,j].tocoo(); bytype=collections.Counter()
            for i,w in zip(ins.row,ins.data): bytype[nodes[i]['cell_type']]+=int(w)
            seed=[{'pre_root_id':nodes[i]['root_id'],'contacts':int(m[i,j])} for i in sorted(targets) if m[i,j]>0]
            routes.append({'root_id':n['root_id'],'side':n['side'],'hemibrain_type':n['hemibrain_type'],
                           'predicted_transmitter':n['top_nt'],'root_specific_sign':'unknown','full_input':int(fi[j]),
                           'LPLC2_contacts':bytype['LPLC2'],'LC4_contacts':bytype['LC4'],'selected_seed_routes':seed,
                           'major_inputs':bytype.most_common(20),'VNC':'outside FAFB; not modeled'})
    save('CROSSWALK.json',{'annotation_version':'v3.1.0','dataset':'FAFB-FlyWire:783',
         'column_sha256':sha(HERE/'data/column_assignment.csv.gz'),'column_conflicts_excluded':conflicts,
         'right_motion_roots_mapped':len(motion),'right_motion_roots_total':sum(n['side']=='right' and n['cell_type'][:2] in ('T4','T5') for n in nodes),
         'selection_ranking':ranking,'selected':selected,'descending_anatomy_only':routes,
         'confidence':{'root_and_type':'high within pinned anatomical annotations, not same animal as physiology',
                       'LPi11_to_LPi4_3':'published type crosswalk; no per-root experimental receptor verification',
                       'LPLC2_function':'class-level experimental correspondence; no measured response for selected roots',
                       'root_hexel':'direct root join, label conflicts excluded',
                       'hexel_retinal_degrees_and_direction':'unresolved; tangent-plane model sensitivity only'}})
    save('CIRCUIT_MANIFEST.json',{'registry_sha256':REGISTRY,'protocol_sha256':sha(HERE/'PROTOCOL.md'),
         'dataset':'FAFB-FlyWire:783','annotation_version':'v3.1.0','source_contacts_sha256':source_sha,
         'annotation_sha256':sha(ROOT/'outputs/flywire-research/annotations-v3.1.0.tsv'),
         'canonical_identity':'SHA256 compact JSON [dataset, source contacts SHA, canonical pre root, canonical post root, neuropil]; aggregated anatomical row, not an individually localized synapse',
         'ownership':'reference-only views; prior registry unchanged; no independent synaptic state',
         'levels':levels,'crosswalk_sha256':sha(HERE/'CROSSWALK.json'),'extractor_sha256':sha(HERE/'extract.py'),
         'wall_seconds':time.perf_counter()-started,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    print(json.dumps({k:v['counts'] for k,v in levels.items()},indent=2))


if __name__=='__main__': main()
