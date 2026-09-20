"""Operator counterexamples, not biological activity or a Stage-4 rerun."""
import numpy as np
from common import save

def correlate(c,alpha):
    delayed=c[0].copy();out=[]
    for current in c:
        out.append(max(0.,delayed[0]*current[1]-current[0]*delayed[1]))
        delayed+=alpha*(current-delayed)
    return np.array(out)

def run():
    # Arbitrary algebraic inputs, not any Stage-4 stimulus, trace, parameter search or biological data.
    x=np.linspace(0.,1.,101)
    dark=np.stack([x*.5,x[::-1]*.5],axis=1)
    bright=dark+.5
    on_dark=np.maximum(dark-.5,0);off_bright=np.maximum(.5-bright,0)
    assert np.count_nonzero(on_dark)==np.count_nonzero(off_bright)==0
    # Separable spatial pulse a_i b(t) cancels for any identical linear filter.
    b=np.r_[np.zeros(7),np.ones(19),np.zeros(11)]
    c=b[:,None]*np.array([[.37,.81]])
    residual=float(np.max(correlate(c,.1)))
    assert residual<1e-14
    # A single scalar with nonlinear observation can be supra-additive.
    observation=lambda v:v*v
    separate=observation(1.)+observation(1.);joint=observation(2.)
    assert joint>separate
    # A scalar pooled sum can discard arrangement while a hypothetical local operator distinguishes it.
    a=np.array([2.,0.]);b2=np.array([1.,1.])
    assert a.sum()==b2.sum() and (a*a).sum()!=(b2*b2).sum()
    return {'kind':'mathematical structural restrictions and non-identifiability counterexamples',
        'not_neural_traces':True,'stage4_simulation_runs':0,'fitted_parameters':0,
        'strict_polarity_zero':True,'separable_flash_max_roundoff':residual,
        'nonlinear_scalar_observation':{'separate':separate,'joint':joint,'inference':'supra-additive calcium does not uniquely imply local voltage states'},
        'pooling_information_loss':{'input_A':a.tolist(),'input_B':b2.tolist(),'equal_scalar_sum':float(a.sum()),
            'hypothetical_local_squared_sum_A':float((a*a).sum()),'hypothetical_local_squared_sum_B':float((b2*b2).sum()),
            'inference':'illustrates information loss only; squared local operator has no biological validation'}}

if __name__=='__main__':save('ALGEBRAIC_CHECKS.json',run())
