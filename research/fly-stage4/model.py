"""Uncalibrated motion-boundary/point-rate hypothesis. No semantic outputs or plasticity."""
import copy
import math
import numpy as np
from scipy import sparse
from common import digest

DEFAULT = dict(dt=0.005,tau=0.05,gain=1.,lpi_gain=1.,spacing=5.,axis_angle=0.,mirror=1.,normalization='full')


class Movie:
    """Only physical intensity and geometry. Model.step receives samples, never a condition label."""
    def __init__(self, kind, center, dt, seed=17):
        self.kind,self.center,self.dt = kind,np.asarray(center),dt
        self.duration=2.75
        if kind.startswith('approach_'):
            self.lv=float(kind.split('_')[1])/1000
            self.start=self.lv/math.tan(math.radians(2.5))
            self.duration=self.start-self.lv/math.tan(math.radians(30))
        if kind.startswith('grating_'): self.duration=2.
        if kind=='translate': self.duration=4.
        if kind=='small': self.duration=1.25
        self.steps=int(math.ceil((4+self.duration)/dt))+1
        self.permutation=np.random.Generator(np.random.PCG64(seed)).permutation(int(math.ceil(self.duration/dt)))

    def intensity(self, points, t):
        kind=self.kind
        u=float(np.clip(t-2,0,self.duration))
        if kind=='shuffle_time' and 0<t-2<self.duration:
            u=float(self.permutation[min(int((t-2)/self.dt),len(self.permutation)-1)]*self.dt)
        x,y=(points-self.center).T
        if kind=='offset': x=x-40.
        d=5+20*u
        if kind=='recede': d=60-20*u
        if kind.startswith('approach_'): d=math.degrees(2*math.atan(self.lv/(self.start-u)))
        if kind=='blank': return np.full(len(points),.5)
        if kind=='dim': return np.where(x*x+y*y<=30**2, .5*(1-d*d/3600),.5)
        if kind=='translate': inside=(np.abs(x-(-40+20*u))<=5)&(np.abs(y)<=30)
        elif kind.startswith('grating_'):
            angle=math.radians(float(kind.split('_')[1]))
            phase=(x*math.cos(angle)+y*math.sin(angle)-20*u)/20
            inside=(np.cos(2*math.pi*phase)>0)&(np.abs(x)<=25)&(np.abs(y)<=25)
        else: inside=x*x+y*y<=(d/2)**2
        return np.where(inside,1. if kind=='bright' else 0.,.5)


class Model:
    def __init__(self,circuit,params=None,intervention='intact',seed=17):
        self.c=circuit; self.p=DEFAULT | (params or {})
        self.rng=np.random.Generator(np.random.PCG64(seed))
        self.neurons=circuit['nodes']; self.n=len(self.neurons)
        self.motion=np.array([i for i,n in enumerate(self.neurons) if n['cell_type'][:2] in ('T4','T5')],dtype=int)
        self.outputs=np.array([i for i,n in enumerate(self.neurons) if n['cell_type']=='LPLC2'],dtype=int)
        self.on=np.array([self.neurons[i]['cell_type'].startswith('T4') for i in self.motion])
        xy=np.array([self.neurons[i]['column']['xy'] for i in self.motion])*self.p['spacing']
        xy[:,0]*=self.p['mirror']
        axes={'a':0,'b':math.pi,'c':math.pi/2,'d':-math.pi/2}
        ang=np.array([axes[self.neurons[i]['cell_type'][-1]] for i in self.motion])+math.radians(self.p['axis_angle'])
        dirs=np.stack([np.cos(ang),np.sin(ang)],axis=1)*self.p['spacing']/2
        self.points=np.concatenate([xy-dirs,xy+dirs])
        self.rates=np.zeros(self.n); self.delay=np.zeros((2,len(self.motion)))
        self.step_index=0; self.initialized=False
        self.lesioned=[]
        rows=[e for e in circuit['edges'] if e['sign'] is not None]
        den=np.array([max(1,n['full_input_contacts']) for n in self.neurons],dtype=float)
        if self.p['normalization']=='retained':
            den=np.maximum(1,np.bincount([e['post'] for e in rows],weights=[e['contacts'] for e in rows],minlength=self.n))
        route=[j for j,e in enumerate(rows) if e['pre'] in self.motion and e['post'] in self.outputs]
        offroute=[j for j,e in enumerate(rows) if e['pre'] in self.motion and e['post'] not in self.outputs]
        removed=set(); changed_pre={}
        if intervention=='route_remove': removed=set(route)
        if intervention=='matched_route':
            ranked=sorted(offroute,key=lambda j:(-rows[j]['contacts'],rows[j]['id']))
            removed=set(ranked[:len(route)])
        if intervention=='lpi_remove': removed={j for j,e in enumerate(rows) if e['sign']==-1 and self.neurons[e['pre']]['cell_type']=='LPi11'}
        if intervention=='shuffle_space':
            # Counterfactual preserves contact counts/targets and source subtype; never anatomical evidence.
            for typ in sorted({self.neurons[i]['cell_type'] for i in self.motion}):
                eligible=sorted({rows[j]['pre'] for j in route if self.neurons[rows[j]['pre']]['cell_type']==typ})
                perm=self.rng.permutation(eligible)
                translation=dict(zip(eligible,map(int,perm)))
                for j in route:
                    if rows[j]['pre'] in translation: changed_pre[j]=translation[rows[j]['pre']]
        if intervention in ('sensory_lesion','matched_sensory'):
            direct={rows[j]['pre'] for j in route}
            strength={i:sum(rows[j]['contacts'] for j in route if rows[j]['pre']==i) for i in direct}
            candidates=sorted(direct,key=lambda i:(-strength[i],self.neurons[i]['root_id']))
            control=set(self.motion)-direct
            pairs=[]
            for i in candidates:
                matches=sorted([k for k in control if self.neurons[k]['cell_type']==self.neurons[i]['cell_type']],key=lambda k:self.neurons[k]['root_id'])
                if matches:
                    k=matches[0]; pairs.append((i,k)); control.remove(k)
                if len(pairs)==8: break
            self.lesioned=[p[0 if intervention=='sensory_lesion' else 1] for p in pairs]
        if intervention=='output_silence': self.lesioned=list(self.outputs)
        a,b,w=[],[],[]
        for j,e in enumerate(rows):
            if j in removed: continue
            a.append(e['post']); b.append(changed_pre.get(j,e['pre']))
            w.append(e['contacts']/den[e['post']]*e['sign']*self.p['gain']*(self.p['lpi_gain'] if e['sign']==-1 else 1))
        self.weights=sparse.csr_matrix((w,(a,b)),shape=(self.n,self.n))
        self.audit={'kind':intervention,'removed_rows':len(removed),'removed_contacts':sum(rows[j]['contacts'] for j in removed),
                    'route_rows':len(route),'route_contacts':sum(rows[j]['contacts'] for j in route),
                    'permuted_rows':len(changed_pre),'lesioned_root_ids':[self.neurons[i]['root_id'] for i in self.lesioned],
                    'normalization_recomputed_after_intervention':False}
        self.identity=digest({'root_ids':[n['root_id'] for n in self.neurons],'params':self.p,
                              'weights':list(zip(a,b,w)),'intervention':self.audit})

    def snapshot(self):
        return {'model_identity':self.identity,'rates':self.rates.tolist(),'motion_delay':self.delay.tolist(),'step_index':self.step_index,
                'clock_seconds':self.step_index*self.p['dt'],'initialized':self.initialized,
                'prng':copy.deepcopy(self.rng.bit_generator.state)}

    def restore(self,s):
        assert s['model_identity']==self.identity, 'Snapshot/model mismatch'
        self.rates=np.asarray(s['rates'],float).copy(); self.delay=np.asarray(s['motion_delay'],float).copy()
        self.step_index=s['step_index']; self.initialized=s['initialized']
        assert abs(s['clock_seconds']-self.step_index*self.p['dt'])<1e-12
        self.rng.bit_generator.state=copy.deepcopy(s['prng'])

    def step(self,intensity):
        c=np.maximum((intensity.reshape(2,-1)-.5)*np.where(self.on,1.,-1.),0)
        if not self.initialized: self.delay=c.copy(); self.initialized=True
        # Delayed near-site contrast × far-site contrast minus the mirror direction.
        motion=np.maximum(self.delay[0]*c[1]-c[0]*self.delay[1],0)
        drive=self.weights@self.rates
        drive[self.motion]+=motion
        new=self.rates+(self.p['dt']/self.p['tau'])*(np.maximum(drive,0)-self.rates)
        new[self.lesioned]=0
        self.rates=new
        self.delay+=(self.p['dt']/self.p['tau'])*(c-self.delay)
        self.step_index+=1
        return self.rates,motion


def trial(circuit,target_root,kind='expand',params=None,intervention='intact',seed=17,full=False):
    model=Model(circuit,params,intervention,seed)
    center=np.array(next(x['center_xy'] for x in circuit['targets'] if x['root_id']==target_root))*model.p['spacing']
    center[0]*=model.p['mirror']
    movie=Movie(kind,center,model.p['dt'],seed)
    target=next(i for i,n in enumerate(model.neurons) if n['root_id']==target_root)
    read=np.zeros((movie.steps,5)); allstate=np.zeros((movie.steps,model.n)) if full else None
    input_trace=np.zeros((movie.steps,len(model.motion))) if full else None
    for k in range(movie.steps):
        t=model.step_index*model.p['dt']
        rates,motion=model.step(movie.intensity(model.points,t))
        read[k]=[t+model.p['dt'],rates[target],float(rates[model.motion].sum()),float(motion.sum()),float(rates.max())]
        if full: allstate[k]=rates; input_trace[k]=motion
    active=(read[:,0]>=2)&(read[:,0]<=2+movie.duration+.5)
    indices=np.flatnonzero(active); peakidx=indices[np.argmax(read[active,1])]
    metric={'target_root_id':target_root,'stimulus':kind,'params':model.p,'intervention':model.audit,'seed':seed,
            'peak':float(read[peakidx,1]),'integral':float(np.trapezoid(read[active,1],read[active,0])),
            'peak_time_after_onset_s':float(read[peakidx,0]-2),'sensory_peak_sum':float(read[:,2].max()),
            'motion_peak_sum':float(read[:,3].max()),'network_peak':float(read[:,4].max()),
            'finite':bool(np.isfinite(read).all()),'duration_s':float(read[-1,0]),'final_step':model.step_index}
    return metric,read,allstate,input_trace,model.snapshot()
