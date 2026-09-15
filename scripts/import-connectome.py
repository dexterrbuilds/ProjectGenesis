"""Reproducible, offline extraction from pinned OpenWorm files; no upstream code execution."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/source'
values = {}
for node in ast.parse((RAW / 'Cells.py').read_text()).body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        try:
            values[node.targets[0].id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            pass
names = sorted(values['PREFERRED_HERM_NEURON_NAMES'])
assert len(names) == len(set(names)) == 302
raw = json.loads((RAW / 'Cook2019HermReader.json').read_text())
idx = {n: i for i, n in enumerate(raw['nodes'])}
assert all(n in idx for n in names)
def role(n):
    for prefix, label in [('PHARYNGEAL_', 'pharyngeal'), ('SENSORY_NEURONS_', 'sensory'), ('INTERNEURONS_', 'interneuron')]:
        if any(n in v for k, v in values.items() if k.startswith(prefix) and isinstance(v, list)):
            return label
    if n in ['CANL', 'CANR']:
        return 'unknown'
    return 'motor'
edges = []
for key, kind in [('Generic_CS', 'chemical'), ('Generic_GJ', 'gap')]:
    matrix = raw['connections'][key]
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            w = matrix[idx[a]][idx[b]]
            if kind == 'gap':
                assert w == matrix[idx[b]][idx[a]], (a, b, 'asymmetric gap')
                if j <= i:
                    continue
            if w:
                assert w > 0 and int(w) == w
                edges.append({'source': a, 'target': b, 'weight': int(w), 'kind': kind})
result = {
    'provenance': {
        'dataset': 'OpenWorm processed Cook et al. 2019 hermaphrodite (July 2020 corrected matrices)',
        'repository': 'https://github.com/openworm/ConnectomeToolbox',
        'commit': 'b9c0b4a7bc2ccf47d3ce7aac624e1b3e2ea86254',
        'license': 'MIT (OpenWorm distribution; see data/README.md)',
        'weightMeaning': 'EM serial-section counts, NOT measured conductance or synapse counts',
        'sourceSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(RAW.iterdir())},
        'excludedNonNeuronalNodes': len(raw['nodes']) - len(names),
    },
    'neurons': [{'id': n, 'role': role(n)} for n in names],
    'edges': edges,
}
out = ROOT / 'data/connectome.json'
out.write_text(json.dumps(result, separators=(',', ':')) + '\n')
print(json.dumps({'neurons': len(names), 'chemicalEdges': sum(e['kind'] == 'chemical' for e in edges), 'gapPairs': sum(e['kind'] == 'gap' for e in edges), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}, indent=2))
