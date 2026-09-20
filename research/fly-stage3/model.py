"""Stage-3 resource-boundary hypothesis, not a persistence decision maker.
BIOLOGY: pinned anatomy; tested population-level modulatory directions.
MODEL: rate/efficacy dynamics and phenomenological body-to-PPL101 regulation.
GENESIS MAPPING: none. No application, peptide graph, cue scores or decision inputs.
"""
import copy
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix

MODEL_VERSION = "fly-stage3-resource-gate-1"

def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()

@dataclass(frozen=True)
class Parameters:
    dt: float = .01
    tau: float = .05
    eligibility_tau: float = .5
    body_tau: float = 60.
    gate_floor: float = .2
    dopamine_gain: float = 1.
    oa_gain: float = 1.
    learning_rate: float = .08
    kc_threshold: float = .15
    pn_gain: float = 3.
    recurrent_gain: float = .05
    apl_gain: float = 1.
    fast_gain: float = 1.
    min_multiplier: float = .1
    normalization: str = 'all_inputs'

class Circuit:
    def __init__(self, directory):
        self.directory = Path(directory)
        raw = (self.directory/"manifest.json").read_bytes()
        self.manifest_hash = hashlib.sha256(raw).hexdigest()
        if self.directory.name != self.manifest_hash:
            raise ValueError("Manifest content address mismatch")
        self.manifest = json.loads(raw)
        for name, spec in self.manifest["artifacts"].items():
            if hashlib.sha256((self.directory/name).read_bytes()).hexdigest() != spec["sha256"]:
                raise ValueError("Artifact checksum mismatch: "+name)
        c = json.loads((self.directory/"circuit.json").read_text())
        self.nodes, self.edges = c['nodes'], c['edges']
        self.ids = [n['root_id'] for n in self.nodes]
        if len(set(self.ids)) != len(self.ids) or any(type(i) is not str for i in self.ids):
            raise ValueError("Invalid roots")
        self.n = len(self.ids)
        self.index = {i: k for k, i in enumerate(self.ids)}
        self.roles = np.array([n['role'] for n in self.nodes])
        self.groups = {g: np.array([self.index[i] for i in ids], dtype=int) for g, ids in c['groups'].items()}
        self.pre = np.array([self.index[e['source']] for e in self.edges])
        self.post = np.array([self.index[e['target']] for e in self.edges])
        self.count = np.array([e['synapses'] for e in self.edges], dtype=float)
        self.boundary = json.loads((self.directory/'boundary.json').read_text())
        self.full_input = np.array([sum(self.boundary['per_neuron'][r][k] for k in
            ('retained_input','omitted_input')) for r in self.ids], dtype=float)


class Model:
    def __init__(self,circuit,params=Parameters(),seed=3701,intervention='intact',resource=.2):
        nums=[v for v in asdict(params).values() if isinstance(v,(int,float))]
        if (not np.all(np.isfinite(nums)) or min(nums)<0 or params.dt<=0 or
            params.dt>min(params.tau,params.eligibility_tau,params.body_tau) or not 0<=resource<=1
            or not 0<=params.gate_floor<=1 or not 0<=params.min_multiplier<=1):
            raise ValueError('Invalid parameters')
        if params.normalization not in ('all_inputs','retained_inputs','retained_roles'):
            raise ValueError('Unknown normalization')
        accepted=('intact','silence_dan','silence_mb11','silence_mb18','silence_oa','remove_da_gate',
                  'freeze_modulation','freeze_plasticity','matched_control','remove_pn_kc',
                  'remove_mb11_mb18','remove_mb18_lh','shuffle_pn_weights','no_apl','no_lh_feedback','global_gain')
        if intervention not in accepted:
            raise ValueError('Unknown intervention')
        self.c,self.p,self.intervention=circuit,params,intervention
        self.rng=np.random.Generator(np.random.PCG64(seed))
        self.r=np.zeros(circuit.n);self.eligibility=np.zeros(circuit.n)
        self.body=float(resource);self.tick=0
        self.pre,self.post=circuit.pre,circuit.post
        src,dst=circuit.roles[self.pre],circuit.roles[self.post]
        self.plastic_edges=np.flatnonzero((src=='KC') & np.isin(dst,['MB11','VALUE']))
        self.plastic_pre,self.plastic_post=self.pre[self.plastic_edges],self.post[self.plastic_edges]
        self.learnable=dst[self.plastic_edges]=='MB11'
        self.multiplier=np.ones(len(self.plastic_edges))
        if params.normalization=='all_inputs':
            denom=circuit.full_input[self.post]
        elif params.normalization=='retained_inputs':
            denom=np.bincount(self.post,weights=circuit.count,minlength=circuit.n)[self.post]
        else:
            denom=np.zeros(len(self.pre))
            for role in sorted(set(src)):
                mask=src==role
                d=np.bincount(self.post[mask],weights=circuit.count[mask],minlength=circuit.n)
                denom[mask]=d[self.post[mask]]
        weights=circuit.count/np.maximum(1,denom)
        gain=np.full(len(weights),params.recurrent_gain)
        gain[(src=='PN')&(dst=='KC')]=params.pn_gain
        gain[(src=='KC') & np.isin(dst,['MB11','MB18','VALUE','CONTROL','APL'])]=1
        gain[(src=='APL')&(dst=='KC')]=params.apl_gain
        gain[src=='MB11']=1
        gain[np.isin(src,['MB18','PN']) & (dst=='LH')]=1
        sign=np.ones(len(weights))
        sign[np.isin(src,['APL','MB11','LHCENT'])]=-1
        # VALUE glutamate and other OA effects have unresolved signs: retain anatomy, zero fast effect.
        sign[np.isin(src,['DAN','VALUE','OA'])]=0
        oa=(src=='OA')&(dst=='MB11')
        sign[oa]=-1;gain[oa]=params.oa_gain
        weights*=gain*sign*params.fast_gain
        da=(src=='DAN')&(dst=='MB11')
        den=np.bincount(self.post[da],weights=circuit.count[da],minlength=circuit.n)
        val=circuit.count[da]/np.maximum(1,den[self.post[da]])
        if intervention=='remove_da_gate':val.fill(0)
        self.da=csr_matrix((val,(self.post[da],self.pre[da])),shape=(circuit.n,circuit.n))
        self.lesion=np.array([],dtype=int)
        g={'silence_dan':'DAN','silence_mb11':'MB11','silence_mb18':'MB18','silence_oa':'OA','no_apl':'APL'}.get(intervention)
        if g:self.lesion=circuit.groups[g]
        if intervention=='matched_control':
            ids=circuit.groups['CONTROL']
            self.lesion=np.array([next(i for i in ids if circuit.nodes[i]['side']==side) for side in ('left','right')])
        if intervention=='remove_pn_kc':weights[(src=='PN')&(dst=='KC')]=0
        if intervention=='remove_mb11_mb18':weights[(src=='MB11')&(dst=='MB18')]=0
        if intervention=='remove_mb18_lh':weights[(src=='MB18')&(dst=='LH')]=0
        if intervention=='no_lh_feedback':weights[np.isin(src,['LH','LHCENT'])]=0
        if intervention=='shuffle_pn_weights':
            for k in circuit.groups['KC']:
                ids=np.flatnonzero((src=='PN')&(self.post==k))
                weights[ids]=self.rng.permutation(weights[ids])
        self.weights=weights.copy();self.plastic_baseline=weights[self.plastic_edges].copy()
        weights[self.plastic_edges]=0
        self.fixed=csr_matrix((weights,(self.post,self.pre)),shape=(circuit.n,circuit.n))
        self.threshold=np.where(circuit.roles=='KC',params.kc_threshold,0.)
        self.fingerprint=hashlib.sha256(canonical({'model':MODEL_VERSION,
            'source':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'circuit':circuit.manifest_hash,
            'parameters':asdict(params),'intervention':intervention,
            'weights':hashlib.sha256(self.weights.tobytes()).hexdigest()})).hexdigest()

    def step(self,currents,resource_input):
        if currents.shape!=(self.c.n,) or not np.all(np.isfinite(currents)) or not 0<=resource_input<=1:
            raise ValueError('Finite numeric currents and bounded body-boundary input required')
        self.body += (resource_input-self.body)*(1-np.exp(-self.p.dt/self.p.body_tau))
        d=self.da@self.r
        factor=np.ones(len(self.plastic_edges))
        factor[self.learnable]=1/(1+self.p.dopamine_gain*d[self.plastic_post[self.learnable]])
        drive=self.fixed@self.r+np.bincount(self.plastic_post,weights=
            self.plastic_baseline*self.multiplier*factor*self.r[self.plastic_pre],minlength=self.c.n)
        desired=np.clip(drive+currents-self.threshold,0,1)
        body=.5 if self.intervention=='freeze_modulation' else self.body
        g=self.p.gate_floor+(1-self.p.gate_floor)*body
        if self.intervention=='global_gain':desired*=g
        else:desired[self.c.groups['DAN']]*=g
        self.r+=self.p.dt/self.p.tau*(desired-self.r)
        self.r[self.lesion]=0
        self.eligibility+=self.p.dt/self.p.eligibility_tau*(self.r-self.eligibility)
        if self.intervention!='freeze_plasticity':
            dopamine=self.da@self.r
            ids=self.learnable
            self.multiplier[ids]*=np.exp(-self.p.learning_rate*self.p.dt*
                self.eligibility[self.plastic_pre[ids]]*dopamine[self.plastic_post[ids]])
            np.maximum(self.multiplier,self.p.min_multiplier,out=self.multiplier)
        self.tick+=1

    def reset_fast_state(self):
        self.r.fill(0);self.eligibility.fill(0)

    def snapshot(self):
        return {'model':MODEL_VERSION,'fingerprint':self.fingerprint,'manifest':self.c.manifest_hash,
                'rate':self.r.tolist(),'eligibility':self.eligibility.tolist(),'plastic_multiplier':self.multiplier.tolist(),
                'body':self.body,'tick':self.tick,'prng':copy.deepcopy(self.rng.bit_generator.state)}

    def restore(self,s):
        if s['fingerprint']!=self.fingerprint or s['manifest']!=self.c.manifest_hash:
            raise ValueError('Incompatible snapshot')
        arrays=[np.asarray(s[k],dtype=float) for k in ('rate','eligibility','plastic_multiplier')]
        if (any(a.shape!=b.shape for a,b in zip(arrays,(self.r,self.eligibility,self.multiplier))) or
            any(not np.all(np.isfinite(a)) or np.any(a<0) or np.any(a>1) for a in arrays) or
            np.any(arrays[2]<self.p.min_multiplier) or not 0<=s['body']<=1 or type(s['tick']) is not int or s['tick']<0):
            raise ValueError('Invalid neural state')
        self.r,self.eligibility,self.multiplier=(a.copy() for a in arrays)
        self.body=float(s['body']);self.tick=s['tick'];self.rng.bit_generator.state=copy.deepcopy(s['prng'])

    def state_hash(self):
        return hashlib.sha256(canonical(self.snapshot())).hexdigest()
