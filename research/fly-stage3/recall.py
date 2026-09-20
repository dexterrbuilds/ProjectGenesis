"""Clean-process sensory-only recall from neural/body/plastic state, not training prose."""
import argparse,gzip,json
from pathlib import Path
import numpy as np
from model import Circuit,Model,Parameters,canonical
from experiment import probe
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--circuit',type=Path,required=True)
    p.add_argument('--config',type=Path,required=True);p.add_argument('--snapshot',type=Path,required=True)
    a=p.parse_args();c=Circuit(a.circuit);config=json.loads(a.config.read_text())
    m=Model(c,Parameters(**config['parameters']),config['seed'],config['intervention'],config['resource'])
    state=json.loads(gzip.decompress(a.snapshot.read_bytes()));m.restore(state)
    cues={q:np.array([c.index[r] for r in roots]) for q,roots in config['patterns'].items()}
    if any(c.roles[i]!='PN' for ids in cues.values() for i in ids):raise ValueError('Sensory roots only')
    result,_=probe(m,state,cues);print(canonical(result).decode(),end='')
