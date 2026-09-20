"""Correct numerical identity only; source records/waveforms remain unchanged."""
from common import *
from empirical import canonical_numbers,descriptor_key
import collections
rows=read('atlas/records.json'); atlas=read('COVERAGE_ATLAS.json')
for g in atlas['groups']:
 rr=[r for r in rows if (r['dataset'],r['type'],r['family'])==(g['dataset'],g['type'],g['family'])]
 tuples=collections.defaultdict(set)
 for r in rr:tuples[descriptor_key(r)].add(r['recording'])
 g['unique_descriptor_tuples']=len(tuples)
 g['tuple_recording_count_range']=[min(map(len,tuples.values())),max(map(len,tuples.values()))]
 for k,v in g['dimensions'].items():
  vals={json.dumps(canonical_numbers(r['descriptor'][k]),sort_keys=True) for r in rr}
  v.update(unique_values=[json.loads(x) for x in sorted(vals)],n_unique=len(vals))
atlas['numerical_identity']='Integral floats and signed zero canonicalized; no physical descriptor removed.'
write('COVERAGE_ATLAS.json',atlas)
