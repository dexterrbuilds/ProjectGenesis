"""Read-only package/preservation audit. No simulation or database connection."""
import argparse
import json
from common import HERE, ROOT, REGISTRY, load, sha, digest


def validate(package=False):
    before=load('FROZEN_BEFORE.json')
    changed=[p for p,h in before.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    assert not changed,changed
    for p,h in load('MODEL_FREEZE.json')['files'].items():assert sha(HERE/p)==h,p
    prereg=load('PREREGISTRATION.json')
    assert sha(HERE/'PROTOCOL.md')==prereg['protocol_sha256']
    for name,h in prereg['sources_at_registration'].items():assert sha(HERE/'data'/name)==h,name
    assert load('DEPENDENCIES.json')['registry_sha256']==REGISTRY
    release=ROOT/'research/genesis-brain-spec-v0.1/objects'/f'{REGISTRY}.json'
    assert sha(release)==REGISTRY
    for path,h in load('DEPENDENCIES.json')['dependencies'].items():
        e=next(e for e in json.loads(release.read_text())['entries'] if e['id']==path)
        assert digest(e)==h,path
    beforedb,afterdb=load('CANONICAL_BEFORE.json'),load('CANONICAL_AFTER.json')
    assert beforedb==afterdb
    assert afterdb['tableRowCounts']['genesis_decisions']==7
    assert all(s['enabled'] is False for s in afterdb['schedule'])
    row_ids={};source=load('CIRCUIT_MANIFEST.json')['source_contacts_sha256']
    for level in ['L0','L1']:
        c=load(f'circuits/{level}.json')
        assert len(c['nodes'])==len({n['root_id'] for n in c['nodes']})
        for e in c['edges']:
            assert isinstance(e['pre_root_id'],str) and isinstance(e['post_root_id'],str)
            cid=digest(['FAFB-FlyWire:783',source,'FAFB-FlyWire:783:'+e['pre_root_id'],'FAFB-FlyWire:783:'+e['post_root_id'],e['neuropil']])
            assert e['id']==cid
            value=(e['pre_root_id'],e['post_root_id'],e['neuropil'],e['contacts'])
            assert row_ids.setdefault(cid,value)==value
            if e['operator']=='unknown_excluded':assert e['sign'] is None
    results=load('RESULTS.json')
    for r in results:assert sha(HERE/r['trace_path'])==r['trace_sha256']
    assert len(results)==len(load('TASKS.json'))==846
    for r in load('RELIABILITY.json'):
        fresh=load(r['fresh_process_result_path'])
        assert fresh['readout_sha256']==r['readout_sha256']
        assert fresh['snapshot_sha256']==r['snapshot_sha256']
        assert r['restored_tail_max_abs']<=1e-12
    update=load('CANDIDATE_EVIDENCE_UPDATE.json')
    assert update['status']=='UNADMITTED' and update['base_registry_sha256']==REGISTRY
    assert update['capability_promotions']==[] and update['supersedes']==[]
    assert update['gate_b']=='NOT TESTED'
    if package:
        m=load('PACKAGE_MANIFEST.json')
        assert digest(m['files'])==m['content_sha256']
        for p,h in m['files'].items():assert sha(HERE/p)==h,p
    return {'valid':True,'protected_prior_files':len(before),'protected_changes':changed,
            'registry_sha256':REGISTRY,'database_sha256':afterdb['sha256'],
            'canonical_cycles':7,'schedule_enabled':False,'new_canonical_cycles':0,
            'new_unique_reference_rows':len(row_ids),'trials_verified':len(results),
            'gate_a':load('ANALYSIS.json')['gate_a'],'gate_b':'NOT TESTED',
            'BrainAdapter_modified':False,'previous_study_classifications_changed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--package',action='store_true');args=p.parse_args()
    print(json.dumps(validate(args.package),indent=2))
