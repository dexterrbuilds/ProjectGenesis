"""Analytical identifiability/compatibility tests, never synthetic biological data."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from fit import save
H=Path(__file__).resolve().parent
def equivalent_voltage(C,g,axial,t):
 A=np.array([[-(g+axial)/C,axial/C],[axial/C,-(g+axial)/C]])
 # Uniformly driven common mode makes coupling unobservable at any time.
 return np.array([(np.eye(2)-expm(A*v))@np.ones(2)/g for v in t])
def main():
 t=np.linspace(0,.1,101);tau=.016056
 # These are mathematical counterexamples, NOT measured traces or fitted physiology.
 v0=equivalent_voltage(1.,1/tau,0.,t)
 errors=[float(np.max(abs(equivalent_voltage(1.,1/tau,a,t)-v0))) for a in [1.,10.,100.,1000.]]
 # An endpoint identifies integrated hazard, not which pathway generated it.
 eta=np.logspace(-4,1,101);exposure=-np.log(.1)/eta
 # At fixed observed tau, C and g may scale together indefinitely.
 scales=np.logspace(-3,3,101);tau_profile=(scales*1.)/(scales/tau)
 # Recovery times need a measurement threshold to identify exponential tau.
 # Sensitivity thresholds explicitly hypothetical; not fitted to a source figure.
 recovery=[]
 for remaining in [.01,.05,.1]:
  recovery.append({'assumed_remaining_fraction_at_1h':remaining,'implied_tau_s':float(-3600/np.log(remaining))})
 out={'status':'analytical compatibility and non-identifiability, not held-out neural fits',
  'temporal':{'mbon14_training_mean_tau_ms':tau*1000,'uniform_drive_two_compartment_scalar_max_abs_errors':errors,
   'capacitance_leak_joint_scaling_tau_max_error_seconds':float(np.max(abs(tau_profile-tau))),
   'meaning':'One fitted time constant cannot identify compartment number, coupling or separate C/g. Full localized voltage transients could discriminate; common-mode examples demonstrate non-uniqueness only.'},
  'conditioning':{'Hige_gamma1_remaining_fraction':.1,'integrated_hazard':float(-np.log(.1)),
   'eta_exposure_endpoint_max_error':float(np.max(abs(np.exp(-eta*exposure)-.1))),
   'identifiable_rank':1,'unknown_factors':2,
   'LTD_only_positive_eligibility_can_potentiate':False,
   'Handler_gamma4_forward_seconds':.5,'Handler_gamma4_backward_seconds':-1.2,
   'compatibility':'Observed opposite plasticity directions reject a universal monotonic LTD-only law in that assay. Does not identify a receptor map, doses or time constants in alpha1/gamma1pedc.',
   'global_equal_modulation_can_express_compartment_different_changes':False,
   'scope':'Only global identical-effect modulation is contradicted. A common signal with independently evidenced target-specific receptors remains logically possible.'},
  'recovery_threshold_sensitivity':recovery,
  'KC_sparsity':'A sparse activated fraction can be matched by many thresholds/input-gains/inhibitory strengths and detection criteria; no identifiable representation from an unpaired population fraction.',
  'R3_alpha_beta_core_KC_measured_constraints':{'A_current_half_activation_mV':-20.3,'half_activation_SEM_mV':1.6,
    'A_current_half_inactivation_mV':-72.9,'half_inactivation_SEM_mV':1.2,'inactivation_tau_at_plus50mV_ms':37.2,'tau_SEM_ms':2.4,
    'source':'Groschner et al. 2018 Figure 3 / S4; male 6–24h in-vivo patch clamp',
    'missing':'full independently held-out I/V and time trajectories; conductance density, activation/inactivation slopes and kinetic functions for a complete kernel; crosswalk to FAFB KC subtype roots'},
  'new_neural_fits':0,'new_stage_replays':0,'kernel_exported':False}
 save(H/'TEMPORAL_CONDITIONING.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
