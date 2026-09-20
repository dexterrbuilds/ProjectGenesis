"""Anatomical audit, no neural trials or circuit enlargement."""
import collections,hashlib,json
from pathlib import Path
from model import Circuit,Model,canonical
HERE=Path(__file__).resolve().parent
c=Circuit(next((HERE/'artifacts').iterdir()));m=Model(c)
roles={};matrix=collections.Counter();pathways={}
for g,ids in c.groups.items():
    b=c.boundary['per_neuron'];s={k:sum(b[c.ids[int(i)]][k] for i in ids) for k in
                               ('retained_input','omitted_input','retained_output','omitted_output')}
    s['input_retention']=s['retained_input']/(s['retained_input']+s['omitted_input'])
    s['output_retention']=s['retained_output']/(s['retained_output']+s['omitted_output'])
    roles[g]=s
for e,i,j in zip(c.edges,c.pre,c.post):matrix[c.roles[i]+'->'+c.roles[j]]+=e['synapses']
for a,b in [('MB11','MB18'),('MB18','LH'),('OA','MB11'),('DAN','MB11'),('MB11','VALUE'),('LH','DAN'),('KC','DAN')]:
    edges=[e for e,i,j in zip(c.edges,c.pre,c.post) if c.roles[i]==a and c.roles[j]==b]
    pairs=collections.Counter();regions=collections.Counter()
    for e in edges:pairs[e['source'],e['target']]+=e['synapses'];regions[e['neuropil']]+=e['synapses']
    pathways[a+'->'+b]={'contacts':sum(pairs.values()),'pairs':[{'source':a,'target':b,'contacts':n} for (a,b),n in sorted(pairs.items())],
                       'neuropils':dict(regions)}
plastic={}
for name,mask in [('experience',m.learnable),('value',~m.learnable)]:
    rows=m.plastic_edges[mask];regions=collections.Counter()
    for i in rows:regions[c.edges[i]['neuropil']]+=c.edges[i]['synapses']
    plastic[name]={'rows':len(rows),'pairs':len(set(zip(c.pre[rows],c.post[rows]))),'contacts':int(c.count[rows].sum()),'neuropils':dict(regions)}
old_roots={}
for n in (1,2):
    old=json.loads(next((HERE.parent/f'fly-stage{n}/artifacts').glob('*/circuit.json')).read_text())
    old_roots[str(n)]={x['root_id'] for x in old['nodes']}
result={'circuit':c.manifest_hash,'counts':c.manifest['counts'],'roles':roles,'pathways':pathways,'plastic':plastic,
        'matrix':dict(matrix),'overlap':{k:len(v & set(c.ids)) for k,v in old_roots.items()},
        'additional_to_union':len(set(c.ids)-set.union(*old_roots.values())),
        'identities':[n for n in c.nodes if n['role'] not in ('PN','KC')],
        'top_omitted_inputs':{g:sorted([x for x in c.boundary['by_external_class_type_transmitter'] if x['inside_role']==g and x['direction']=='omitted_input'],key=lambda x:-x['synapses'])[:12] for g in c.groups},
        'model_effects':{'nonzero_fast_rows':int((m.weights!=0).sum()),'zero_fast_rows':int((m.weights==0).sum())}}
raw=canonical(result);dest=HERE/'anatomy-audit'/hashlib.sha256(raw).hexdigest();dest.mkdir(parents=True,exist_ok=True)
p=dest/'anatomy.json'
if p.exists():assert p.read_bytes()==raw
else:p.write_bytes(raw)
print(json.dumps({'anatomy':str(p),'overlap':result['overlap'],'additional':result['additional_to_union'],'plastic':plastic},indent=2))
