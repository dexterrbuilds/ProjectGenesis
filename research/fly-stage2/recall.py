"""Fresh-process sensory-only recall. Does not load outcomes or training history."""
import argparse
import gzip
import json
from pathlib import Path
import numpy as np
from model import Circuit,Model,Parameters,canonical
from experiment import probe

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--circuit',type=Path,required=True)
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--snapshot',type=Path,required=True)
    a=p.parse_args()
    c=Circuit(a.circuit)
    config=json.loads(a.config.read_text())
    m=Model(c,Parameters(**config['parameters']),config['seed'],config['intervention'])
    state=json.loads(gzip.decompress(a.snapshot.read_bytes()))
    m.restore(state)
    patterns={k:np.array([c.index[root] for root in roots]) for k,roots in config['patterns'].items()}
    if any(c.roles[i]!='PN' for ids in patterns.values() for i in ids):
        raise ValueError('Sensory inputs only')
    result,_=probe(m,state,patterns)
    print(canonical(result).decode(),end='')
