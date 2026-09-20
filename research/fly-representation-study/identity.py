"""Identity-only audit of frozen anatomy. No physiological update rules."""
import hashlib,json,gzip
from pathlib import Path
H=Path(__file__).resolve().parent
DATASET='FAFB-FlyWire:783';SOURCE='24f960ae3e7d4f8cd30db3b62e99fb5179cc3d1e76d8c155bfb441e9737d3faf'
def neuron_key(root):
 if not isinstance(root,str) or not root.isdecimal():raise ValueError('Root must be a decimal string')
 return DATASET+':'+root
def row_key(edge):
 # Aggregate row identity, not a fabricated individual anatomical contact ID.
 key=[DATASET,SOURCE,neuron_key(edge['source']),neuron_key(edge['target']),edge['neuropil']]
 return hashlib.sha256(json.dumps(key,separators=(',',':')).encode()).hexdigest()
def insert(registry,edge,stage):
 key=row_key(edge)
 if key in registry:
  if registry[key]['anatomical_contacts']!=edge['synapses']:raise ValueError('Conflicting contact count for canonical row')
  registry[key]['preparations'].append(stage)
 else:registry[key]={'id':key,'pre':neuron_key(edge['source']),'post':neuron_key(edge['target']),
  'neuropil':edge['neuropil'],'anatomical_contacts':edge['synapses'],'preparations':[stage],
  'physiology_rule':None,'functional_compartment':None}
 return key
def main():
 out=H/'IDENTITY_AUDIT.json';assert not out.exists()
 registry={};roots=set();circuits={};sources={}
 for stage in (1,2,3):
  path=next((H.parent/f'fly-stage{stage}'/'artifacts').glob('*/circuit.json'));c=json.loads(path.read_text());circuits[stage]=c
  sources[str(path.relative_to(H.parent.parent))]=hashlib.sha256(path.read_bytes()).hexdigest()
  for n in c['nodes']:roots.add(neuron_key(n['root_id']))
  for edge in c['edges']:insert(registry,edge,stage)
 def targeted(stage,group):
  c=circuits[stage];kc=set(c['groups']['KC']);mb=set(c['groups'][group])
  return {row_key(e) for e in c['edges'] if e['source'] in kc and e['target'] in mb}
 shared={name:sorted(targeted(1,a)&targeted(3,b)) for name,a,b in [('KC_MBON07','MBON_app','VALUE'),('KC_MBON11','MBON_av','MB11')]}
 assert len(shared['KC_MBON07'])==4622 and len(shared['KC_MBON11'])==1053
 with gzip.GzipFile(filename=str(H/'identity-registry.jsonl.gz'),mode='wb',mtime=0) as stream:
  for key in sorted(registry):stream.write((json.dumps(registry[key],separators=(',',':'))+'\n').encode())
 (H/'shared-row-ids.json').write_text(json.dumps(shared,indent=2)+'\n')
 r={'dataset':DATASET,'source_sha256':SOURCE,'roots':len(roots),'unique_aggregate_rows':len(registry),
  'summed_preparation_rows':sum(len(c['edges']) for c in circuits.values()),
  'contacts_in_union_of_extracted_rows':sum(r['anatomical_contacts'] for r in registry.values()),
  'shared_rows':{k:len(v) for k,v in shared.items()},'conflicting_contact_counts':0,'physiology_rules_assigned':0,
  'source_hashes':sources,'registry_sha256':hashlib.sha256((H/'identity-registry.jsonl.gz').read_bytes()).hexdigest(),
  'meaning':'Union of existing extraction rows, not induced union connectome; identity schema only. No neural model created.'}
 out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
