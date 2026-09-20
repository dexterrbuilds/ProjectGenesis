"""Read-only transfer of accepted Stage-1 efficacies onto identical anatomical rows.

This is a NEW network context. It does not modify or revalidate the frozen model.
"""
from dataclasses import asdict
import gzip,hashlib,json,platform,resource,time
from pathlib import Path
import numpy as np
from model import Circuit,Model,Parameters,canonical
from experiment import probe
HERE=Path(__file__).resolve().parent

def main():
    start=time.perf_counter();c=Circuit(next((HERE/'artifacts').iterdir()))
    old=next((HERE.parent/'fly-stage1/artifacts').iterdir());oldc=json.loads((old/'circuit.json').read_text())
    oldroles={n['root_id']:n['role'] for n in oldc['nodes']}
    oldplast=[e for e in oldc['edges'] if oldroles[e['source']]=='KC' and oldroles[e['target']] in ('MBON_app','MBON_av')]
    oldev=next((HERE.parent/'fly-stage1/evidence').iterdir())
    # Frozen historical evidential files verified against their existing manifest.
    evidence_manifest=json.loads((oldev/'evidence-manifest.json').read_text())
    rows=[];snapshots={};vectors={};sources={};mapping=[]
    for paired in ('A','B'):
        folder=oldev/f'app-1701-{paired}-intact'
        for filename in ('trained.json.gz','stimuli.json','summary.json'):
            p=folder/filename;h=hashlib.sha256(p.read_bytes()).hexdigest()
            assert h==evidence_manifest['files'][str(p.relative_to(oldev))]
            sources[str(p.relative_to(HERE.parent))]=h
        trained=json.loads(gzip.decompress((folder/'trained.json.gz').read_bytes()))
        accepted=json.loads((folder/'summary.json').read_text())
        assert hashlib.sha256(canonical(trained)).hexdigest()==accepted['trained_hash']
        events=json.loads((folder/'stimuli.json').read_text())['events']
        cues={q:np.array([c.index[root] for root,v in event['currents']]) for q,event in zip(('A','B'),events[:2])}
        values={(e['source'],e['target'],e['neuropil']):(e['synapses'],v) for e,v in zip(oldplast,trained['plastic_multiplier'])
                if oldroles[e['target']]=='MBON_app'}
        for cond in ('intact','silence_dan','silence_mb11','freeze_modulation'):
            for body in (.2,.8):
                for learned in (False,True):
                    m=Model(c,intervention=cond,resource=body)
                    count=0
                    if learned:
                        for j,edge_index in enumerate(m.plastic_edges):
                            e=c.edges[edge_index];key=(e['source'],e['target'],e['neuropil'])
                            if key in values:
                                contacts,value=values[key];assert contacts==e['synapses']
                                m.multiplier[j]=value;count+=1
                        assert count==len(values),'Missing frozen anatomical efficacy rows'
                    if paired=='A' and cond=='intact' and learned and body==.2:
                        mapping=[{'source':k[0],'target':k[1],'neuropil':k[2],'contacts':v[0]} for k,v in sorted(values.items())]
                    state=m.snapshot();out,v=probe(m,state,cues)
                    key=f'{paired}-{cond}-{body}-{int(learned)}'
                    rows.append({'run':key,'paired':paired,'intervention':cond,'resource':body,'learned':learned,
                                 'copied_rows':count,'responses':out})
                    snapshots[key]=gzip.compress(canonical(state),mtime=0)
                    for q,x in v.items():vectors[key+'-'+q]=x
    results={'assay':'same learned anatomical efficacies; new Stage-3 network context',
             'rows':rows,'mapping':mapping,'source_hashes':sources,'circuit':c.manifest_hash,
             'model_sha256':hashlib.sha256((HERE/'model.py').read_bytes()).hexdigest(),
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'performance':{'wall_seconds':time.perf_counter()-start,
                'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)}}
    raw=canonical(results);dest=HERE/'learned-evidence'/hashlib.sha256(raw).hexdigest();dest.mkdir(parents=True,exist_ok=False)
    (dest/'results.json').write_bytes(raw)
    for key,blob in snapshots.items():(dest/f'{key}.json.gz').write_bytes(blob)
    np.savez_compressed(dest/'probe-rates.npz',root_ids=np.array(c.ids),**vectors)
    manifest={'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.iterdir()) if p.is_file()}}
    (dest/'file-manifest.json').write_bytes(canonical(manifest))
    print(json.dumps({'evidence':str(dest),'copied_rows':len(mapping),'performance':results['performance']},indent=2))

if __name__=='__main__':main()
