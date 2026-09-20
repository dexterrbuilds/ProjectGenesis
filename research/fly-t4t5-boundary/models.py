"""Conditional voltage approximations. No anatomy, LPLC2, decisions or product state."""
import numpy as np
from scipy.signal import lfilter
import json

def load(path):
 with np.load(path,allow_pickle=False) as z:
  return {**{k:z[k] for k in z.files if k!='metadata'},'metadata':json.loads(str(z['metadata']))}

def features(d,kind,tau=50,delay=0,gamma=0):
 n=len(d['t_ms'])
 if kind=='Z':return np.zeros((n,0))
 xx=d['x_pixels'];s=d['off_occupancy'].astype(float)
 if kind=='B0':
  out=np.zeros((n,1))
  for a,b in zip(d['starts'],d['ends']):
   inp=s[a:b][:,[int(np.where(xx==-1)[0][0]),int(np.where(xx==0)[0][0])]]
   old=np.zeros(2)
   dt=float(d['t_ms'][a+1]-d['t_ms'][a]);stride=int(round(5/dt))
   for j in range(0,len(inp),stride):
    v=inp[j];out[a+j:min(a+j+stride,b),0]=max(0,old[0]*v[1]-v[0]*old[1]);old+=.1*(v-old)
  return out
 basis=np.exp(-.5*((xx[:,None]-np.arange(-6,7,2)[None,:])/2)**2)
 raw=s@basis;taus=[tau] if kind=='B1s' else [20,100];out=np.zeros((n,7*len(taus)))
 for a,b in zip(d['starts'],d['ends']):
  dt=float(d['t_ms'][a+1]-d['t_ms'][a]);lag=int(round(delay/dt))
  for k,tm in enumerate(taus):
   alpha=1-np.exp(-dt/tm);f=lfilter([alpha],[1,-(1-alpha)],raw[a:b],axis=0)
   if lag:f=np.vstack([np.zeros((min(lag,b-a),7)),f[:max(0,b-a-lag)]])
   out[a:b,7*k:7*(k+1)]=f
 if kind=='B1d':out/=1+gamma*np.mean(np.abs(out),axis=1,keepdims=True)
 return out

def moments(d,X):
 g=[];h=[];q=[];dur=[]
 for a,b,m in zip(d['starts'],d['ends'],d['metadata']):
  x=X[a:b];y=d['voltage_mV'][a:b];g.append(x.T@x/len(y));h.append(x.T@y/len(y));q.append(float(y@y/len(y)));dur.append(m['duration_ms'])
 return np.array(g),np.array(h),np.array(q),np.array(dur)

def solve(G,h,lam,kind):
 if not len(h):return np.zeros(0),0.,0
 e,U=np.linalg.eigh(G);e=np.maximum(e,0);pen=lam*np.trace(G)/len(h);inv=np.where(e+pen>max(1e-14,e.max()*1e-12),1/np.maximum(e+pen,1e-300),0)
 beta=U@(inv*(U.T@h))
 if kind=='B0':beta=np.maximum(0,beta)
 edf=float(np.sum(e*inv));rank=int(np.sum(e>max(1e-14,e.max()*1e-10)))
 return beta,edf,rank

def mse(G,h,q,b):return float(max(0,q-2*b@h+b@G@b))

def options():
 yield {'kind':'Z','tau':50,'delay':0,'gamma':0,'lambda':0}
 yield {'kind':'B0','tau':50,'delay':0,'gamma':0,'lambda':0}
 for kind in ['B1s','B1t','B1d']:
  for tau in ([20,50,100] if kind=='B1s' else [50]):
   for delay in [0,10,25,50]:
    for gamma in ([.1,.3,1] if kind=='B1d' else [0]):
     for lam in [0,.01,.1,1,10]:yield {'kind':kind,'tau':tau,'delay':delay,'gamma':gamma,'lambda':lam}
