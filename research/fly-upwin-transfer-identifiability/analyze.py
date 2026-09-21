"""Descriptive observations and algebraic identifiability witnesses, not a neural simulation.

No optimizer, neural model import, runtime, network access or biological coefficient fit.
Normalized witness values are counterexamples, not acquired observations or transfer estimates.
"""
from common import *
import csv,math,statistics,itertools

def summary(xs):
 return dict(n=len(xs),mean=statistics.mean(xs),min=min(xs),max=max(xs),sample_sem=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else None)

m=load(ROUTE/'MEASUREMENT_AUDIT.json')
acute=next(x for x in m['whole_cell'] if x['file']=='elife-85756-fig4-data2-v3.xlsx')
recall=[]
for c in m['conditioning']:
 paired=c['paired_odor'];control='MCH' if paired=='OCT' else 'OCT';rows=[]
 for r in c['observations']:
  dp=r[paired+'_post_mV']-r[paired+'_pre_mV'];dc=r[control+'_post_mV']-r[control+'_pre_mV']
  rows.append(dict(source_row=r['source_row'],source_label=r['source_label'],animal_id=None,recording_id=None,paired_change_mV=dp,control_change_mV=dc,within_row_difference_of_changes_mV=dp-dc))
 recall.append(dict(file=c['file'],paired_odor=paired,units=c['unit'],window=c['window'],rows=rows,
  paired_change=summary([r['paired_change_mV'] for r in rows]),control_change=summary([r['control_change_mV'] for r in rows]),
  difference_of_changes=summary([r['within_row_difference_of_changes_mV'] for r in rows]),
  uncertainty_scope='SEM is descriptive across source rows, not a new fly-independent CI or causal-transfer estimate.'))
upstream=load(ROUTE/'ALPHA1_CONDITIONING_AUDIT.json')
write('OBSERVATIONS.json',dict(source_files={str(p.relative_to(ROOT)):sha(p) for p in [ROUTE/'MEASUREMENT_AUDIT.json',ROUTE/'ALPHA1_CONDITIONING_AUDIT.json',IDENTITY/'TRANSMISSION.json',STAGE1/'RESULTS.csv']},
 acute=acute,observed_detection_fraction=dict(numerator=4,denominator=17,value=4/17,reported_flies=12,population_interval=None,reason='Finite sample label fraction only; sampling and clustering are not identified.'),
 recall=recall,upstream_conditioning=upstream,
 direct_rate_to_voltage_conversion=None,acute_vs_recall_composition=False,external_population_identity_join=None))

# Read frozen Stage-1 outputs for order only. No Stage-1 code executes.
raw=list(csv.DictReader((STAGE1/'RESULTS.csv').open()))
order=[]
for r in raw:
 if r['run'] in {f'app-{seed}-{cue}-intact' for seed in [1701,1702,1703] for cue in ['A','B']}:
  p=r['paired'];before=float(r[f'baseline_{p}_MBON_app']);after=float(r[f'post_{p}_MBON_app'])
  order.append(dict(run=r['run'],paired_cue=p,paired_post_less_than_pre=after<before,restoration_exact=r['restoration_exact']=='True',
   source='research/fly-stage1/RESULTS.csv',exported_physical_value=None))
write('STAGE1_FIREWALL.json',dict(readonly_order_audit=order,allowed=['existence of a learned difference','modeled mechanism dependence','persistent plastic state','within-model ordering at the same defined readout'],
 not_exported=['physical firing rate','mV','synaptic current','photostimulation equivalence','downstream 50 ms constant','UpWiN gain','receptor sign','behavioral probability'],
 invariant='For a fixed saved scalar r_post < r_pre, strictly increasing re-expression h preserves the order. It does not identify whether physical α1 activity is such a re-expression.',
 not_invariant='Effect-size ratios, differences of changes, population means after arbitrary neuron-wise nonlinear maps, and downstream ordering need extra assumptions.',
 downstream_family_contains=['same order','reversed order','tie'],model_runs=0))

prep=load(ROUTE/'PREPARATION_COMPATIBILITY.json')
domains=prep['preparations']
for d in domains:
 d['source_scope']='Frozen route acquisition: PREPARATION_COMPATIBILITY.json'
# Explicitly split the behavioral drivers: no assumption of common physiology/neurons.
domains=[d for d in domains if d['id']!='behavior']+[dict(id=f'behavior_{driver}',driver=driver,measurement='assay-specific wind orientation/turning/locomotion',units=['degrees','degrees/s','mm/s'],source_scope='frozen route acquisition; identity study',pool_with_other_driver=False) for driver in ['SS33917','SS33918']]
matrix=[]
for a,b in itertools.combinations([d['id'] for d in domains],2):
 parent=lambda x:'behavior' if x.startswith('behavior_') else x
 pa,pb=parent(a),parent(b)
 if pa==pb:
  status='ASSUMPTION REQUIRED';reason='Related driver-scoped endpoints may be compared; driver populations are not equal and cannot be pooled as one transfer.'
 else:
  old=next(x for x in prep['bridges'] if {x['from'],x['to']}=={pa,pb})
  status=old['classification'];reason=old['reason']
 matrix.append(dict(from_domain=a,to_domain=b,numerical_bridge=status,reason=reason,
  bridge_established=False if status!='DIRECTLY COMPATIBLE' else 'only within the same documented assay/control contrast',
  qualitative_use='May constrain separate domain observations; does not calibrate a common transfer.'))
write('OBSERVATION_MATRIX.json',dict(domains=domains,between_domains=matrix,within_domain=prep['within_assay_direct_bridges'],
 new_joins=[],hypotheses=[dict(id='H-identity',value=None,statement='The sampled physiological and behavioral populations overlap in the required causal targets.'),dict(id='H-state',value=None,statement='A specified order-preserving map connects Stage-1 readout to biological α1 state.'),dict(id='H-exclusion',value=None,statement='Other inputs are held fixed when identifying the α1 contribution.'),dict(id='H-observation',value=None,statement='A common observation map is valid across preparations.')]))

classes=[
 dict(id='C0',name='domain-specific response constraints with unmeasured inputs',form='y_d = F_d(x_d,z_d,t); observation maps and cross-domain correspondence unspecified',status='evidence-admissible parent class',identifies='finite observed responses only',extra_assumptions=[]),
 dict(id='C1',name='sign-only monotone transfer',form='y=f(x), f nonincreasing on declared support',status='conditional subfamily, not selected',identifies='conditional weak order reversal; strict reversal additionally requires nonzero slope and a relevant responder',extra_assumptions=['identity bridge','increasing Stage-1-to-α1 map','constant other inputs','monotonicity over tested support']),
 dict(id='C2',name='linear or saturating monotone refinements',form='b-g*x versus b-A*(1-exp(-x/s))',status='observationally equivalent at sampled endpoints after coordinate convention; no refinement selected',identifies='neither gain nor saturation',extra_assumptions=['C1 assumptions','scale/origin for x','linearity or saturation family']),
 dict(id='C3',name='heterogeneous detection/response mixture',form='observed detection frequency depends on responsiveness, selection and detection sensitivity',status='needed to preserve 4/17 and 13 nonresponders; latent membership not identified',identifies='observed labels, not anatomical responder probability',extra_assumptions=['no iid-cell assumption admitted','detection threshold and sample selection unknown']),
 dict(id='C4',name='latent disinhibition versus alternative input change',form='Δy_d = g_d Δx_d + Δz_d',status='equivalence decomposition, not a fitted physiological model',identifies='no attribution of recall potentiation to α1',extra_assumptions=['restriction of Δz would be new evidence or explicit hypothesis'])]
write('TRANSFER_CLASSES.json',dict(classes=classes,selected_class=None,fitted_parameters=[],bounded_monotone_note='A bound y(1) <= y(x) <= y(0) for x in [0,1] follows only after C1 and support mapping are assumed; not an empirical neural-amplitude bound.'))

# Counterexamples are symbolic equivalences, with normalized arithmetic checks.
counter=[
 dict(id='CE-sign',property='direct transmission sign',construction='For x=u,z=u: y=-x and y=+x-2z both give y=-u. The direct partial derivative with respect to x is -1 versus +1, while the observed total photostimulation effect agrees.',full_observation_extension='For every observed cell waveform a_i(t), x_i(t)=-u*a_i(t). The same constructions yield u*a_i(t) in both worlds. This is a witness reparameterization, not an inferred α1 waveform or an invented anatomical edge.',scope='Direct sign is not total intervention sign. A negative finite acute response cannot be relabeled positive under the same observation definition.'),
 dict(id='CE-monotonicity',property='monotonicity / local transfer sign',construction='f_c(x)=-x+c*x*(x-1). All c agree at x=0,1. c=4 has derivative 8x-5, negative at 0 and positive near 1.',full_observation_extension='Multiply each observed response a_i(t) by x-c*x*(x-1); endpoints reproduce the entire waveform. Intermediate α1 inputs were not measured.',scope='Normalized endpoint index is not a measured α1 neural coordinate.'),
 dict(id='CE-scale',property='gain and amplitude calibration',construction='x*=k*x and g*=g/k preserve y=g*x for every k>0.',full_observation_extension='Preserves complete time series and all acute observations; source neural-state scale unmeasured.',scope='Known mV units do not identify units or scale of α1 input.'),
 dict(id='CE-saturation',property='saturation and boundedness',construction='f_s(x)=-(1-exp(-x/s))/(1-exp(-1/s)), s>0, and f_linear=-x have the same endpoints; the former saturates and the latter does not.',full_observation_extension='Each observed waveform can be multiplied by the corresponding normalized endpoint function; neither additional dose response nor source state was measured.',scope='Saturation values are normalized mathematical witnesses only.'),
 dict(id='CE-mixture',property='population responder fraction / structural zero',construction='All sampled cells may be physiologically affected but thirteen effects fail detection, or four may have strong transmission while thirteen do not. Unmeasured recording/background variation can preserve the exact same seventeen observed traces.',full_observation_extension='Under an illustrative iid detection model only p*d is estimable: (p,d)=(4/17,1) and (1,4/17) have identical binomial likelihood. That iid model is not justified for the real clustered sample.',scope='4/17 is identified as a label count; biological fraction and nonresponder zero-gain are not.'),
 dict(id='CE-time',property='downstream latency / temporal kernel',construction='Observed LED-to-voltage composite K=H*O. Swapping two factors in convolution leaves K unchanged while assigning different time constants to H. A total delay can likewise be partitioned between opsin/source and target.',full_observation_extension='Even perfect knowledge of a composite trace cannot uniquely factor unmeasured source drive, neural transfer and observation filtering. The present workbook also lacks an original onset event column.',scope='No numerical biological delay or 50 ms target constant inferred. A causal nonnegative delay is an engineering constraint, not measured latency.'),
 dict(id='CE-recall',property='conditioning-dependent transfer / disinhibition',construction='For each observed recall change Δy, Δy=g*Δx+Δz. Worlds g<0 with reduced x, g=0 with Δz=Δy, and g>0 with compensating Δz are indistinguishable because x is not measured in those cells.',full_observation_extension='Set the alternative component per recorded condition, preserving paired and unpaired changes and both reciprocal odor cohorts. Separate upstream conditioning records and behavioral observations remain unchanged in their own domains.',scope='This saturated nuisance construction proves non-identification; it is not a mechanistic fit, identified new pathway, or claim these alternatives are equally likely.'),
 dict(id='CE-sharing',property='one common transfer across acute and recall',construction='A shared g with domain-specific latent inputs and different g_d with adjusted latent inputs give identical observations without a cross-domain joining key.',full_observation_extension='Qualitative calcium suppression is preserved in its own domain; no calcium-to-voltage conversion or behavioral-to-voltage link is supplied.',scope='Neither a common transfer nor its nonexistence is established.'),
 dict(id='CE-order',property='downstream dimensionless order',construction='For x_post<x_pre, f=-x reverses order, f=x preserves it, and f=constant ties it. CE-recall and identity uncertainty allow each for a hypothetical recall target while preserving acute sampled responses.',full_observation_extension='The frozen Stage-1 order itself is unchanged. A strictly increasing recoding of that same scalar preserves order; it supplies no physical identity or transfer direction.',scope='No nonzero signed downstream effect is invariant across the evidence-admissible parent family.'),
 dict(id='CE-statistics',property='identified finite summaries',construction='Try changing transfer, latent gain or target assignment while holding all seventeen labels, eleven paired scalar rows, units and six Stage-1 ordinal records fixed.',full_observation_extension='Counts, arithmetic summaries and saved-scalar inequalities cannot change without changing a fixed observation. Population expectations and causal attributions can change freely.',scope='Counterexample fails for these narrowly defined descriptive estimands; it succeeds for their biological extrapolations.'),
]
write('COUNTEREXAMPLES.json',dict(witnesses=counter,biological_parameter_estimates=False,synthetic_observations=False,neural_runs=0,
 cautions=['Algebraic nuisance terms are non-identification witnesses, not fabricated anatomical partners.','Finite-grid checks illustrate analytic identities, not exhaustive empirical validation.','Consistency does not imply independent support or equal plausibility.']))

# All tests below are pure arithmetic on dimensionless witness coordinates.
grid=[0,.25,.5,.75,1]
sign_errors=[abs(-u-(u-2*u)) for u in grid]
curves=[dict(c=c,endpoints=[0.0,-1.0],midpoint=-.5+c*.5*(.5-1),derivative_at_one=-1+c) for c in [-4,0,4]]
saturation=[dict(s=s,at_half=-(1-math.exp(-.5/s))/(1-math.exp(-1/s)),asymptote=-1/(1-math.exp(-1/s))) for s in [.1,1,10]]
scale=[dict(input_scale=k,gain=1/k,output=(1/k)*(k*.5)) for k in [.01,1,100]]
recall_null=[]
for c in recall:
 for r in c['rows']:
  # In Δy = g*Δx+Δz, Δx=-1 is an arbitrary coordinate convention, not Stage1 or spike units.
  for quantity in ['paired_change_mV','control_change_mV']:
   for g in [-2,0,2]:
    dy=r[quantity];z=dy+g
    recall_null.append(dict(file=c['file'],row=r['source_row'],quantity=quantity,arbitrary_g=g,arbitrary_dx=-1,nuisance_residual_not_estimated_biology=z,error=(-g+z)-dy))
kernel=[]
for omega in [.1,1,10]:
 s=complex(0,omega);h1=1/(1+s);h2=1/(1+2*s)
 kernel.append(dict(dimensionless_frequency=omega,swap_error=abs(h1*h2-h2*h1)))
write('DEGENERACY.json',dict(
 arithmetic_tolerance=1e-12,sign_witness_max_error=max(sign_errors),monotonicity_witnesses=curves,saturation_witnesses=saturation,scale_witnesses=scale,
 mixture=dict(observed_detection_fraction=4/17,illustrative_pairs=[[4/17,1],[1,4/17]],products=[4/17,4/17],population_confidence_interval=None),
 recall_nullspace=recall_null,recall_max_error=max(abs(x['error']) for x in recall_null),
 recall_linear_identifiability=dict(n_observed_changes=22,n_equations=22,n_unknowns_if_one_shared_g_and_free_nuisance_per_change=23,jacobian_rank_if_dx_known=22,nullity_at_least=1,explanation='J=[Δx | I]; gain column lies in nuisance span. Real Δx and cross-domain identity are also unknown, making identification no stronger.'),
 convolution_factorization=kernel,
 latent_mediation_bounds=dict(unrestricted_alpha1_attributable_component=['-infinity','+infinity'],under_extra_nonnegative_additive_components_only=[0,1],fraction_bound_is_assumption_not_measurement=True,scope='Formal identification set of the unconstrained decomposition, not a claim that physical membrane voltage is unbounded.'),
 plateau_note='A non-strict monotone transfer may collapse any learned order into a tie; no positive lower slope bound is measured.',
 all_grid_values='mathematical diagnostics, not biological ranges or a Stage5 sweep',selection=None))

rows=[
 ('sample-label-fraction','Finite R64A11 reported responder fraction','IDENTIFIED','4/17 (13 nonresponders); 12 reported flies','Fixed sample labels, not a population sampling estimate','CE-statistics'),
 ('acute-observed-sign','Finite sampled acute response direction','QUALITATIVELY CONSTRAINED','negative somatic Vm response in four reported cells','Only this protocol and sampled subset; not receptor/direct-transfer sign','CE-sign'),
 ('transfer-sign','Hypothetical α1-state→target transfer sign','NON-IDENTIFIABLE',None,'Input scale, operating state, mediation and target membership unresolved','CE-sign'),
 ('monotonicity','Monotonicity across neural input states','NON-IDENTIFIABLE',None,'Single protocol response is not a neural-state dose-response curve','CE-monotonicity'),
 ('population-fraction','Biological responder probability or mixture membership','NON-IDENTIFIABLE',None,'Selection/detection/clustering unknown; nonresponders not zero edges','CE-mixture'),
 ('recorded-amplitude','Finite recorded voltage amplitudes/summaries','IDENTIFIED','See OBSERVATIONS.json; mV with preserved windows','Not a gain or unobserved output bound; trace extrema not used as stimulus-aligned peaks','CE-statistics'),
 ('gain','Absolute α1→UpWiN gain / amplitude scale','NON-IDENTIFIABLE',None,'Known output units do not identify input units','CE-scale'),
 ('conditional-bounds','Intermediate output under assumed endpoint-monotonic map','BOUNDED','Between the two endpoints only under C1 and known support ordering','Conditional mathematical bound; not admitted biological bound','CE-monotonicity'),
 ('latency','Downstream neural latency','NON-IDENTIFIABLE',None,'Original event onset/source activity/observation delays unavailable','CE-time'),
 ('kernel','Neural time constant or temporal kernel','NON-IDENTIFIABLE',None,'LED composite cannot identify its physiological factors; no 50 ms transfer','CE-time'),
 ('saturation','Saturation / asymptotic output','NON-IDENTIFIABLE',None,'No identified neural-input sweep','CE-saturation'),
 ('observed-heterogeneity','Detected heterogeneous acute response labels','IDENTIFIED','four responders versus thirteen nonresponders','Observation heterogeneity only; true gain/subtype/detection sources not identified','CE-statistics'),
 ('latent-heterogeneity','Mechanistic heterogeneity','NON-IDENTIFIABLE',None,'Threshold/detection/noise/selection can mimic type/gain mixtures','CE-mixture'),
 ('recall-summary','Finite SS67249 paired-row changes and controls','IDENTIFIED','Both cohorts retain increased paired-odor means; source values preserved','No population transfer estimate or mediation attribution','CE-statistics'),
 ('conditioning-modulation','Conditioning-dependent α1→UpWiN transfer change','NON-IDENTIFIABLE',None,'Changed input and changed transfer cannot be separated','CE-recall'),
 ('common-transfer','One transfer explaining both acute and recall','NON-IDENTIFIABLE',None,'Distinct populations; shared and separate functions both compatible','CE-sharing'),
 ('disinhibition','α1 disinhibition as cause of recall change','NON-IDENTIFIABLE',None,'Alternative input changes preserve all separate observations','CE-recall'),
 ('stage1-order','Same saved Stage-1 readout post/pre order','IDENTIFIED','six intact counterbalanced runs have paired post < pre','Only this dimensionless scalar; no physical transfer or cross-cue ranking assertion','CE-statistics'),
 ('downstream-order','Transferred physical response order','NON-IDENTIFIABLE',None,'Full family allows order preservation, reversal and ties','CE-order'),
 ('calcium','Population calcium interaction','QUALITATIVELY CONSTRAINED','α1 coactivation suppresses α3-evoked population signal in its assay','Cannot convert to mV or constrain a recorded target receptor','CE-sharing'),
 ('behavior','Driver-scoped downstream intervention relationship','QUALITATIVELY CONSTRAINED','Separate wind-oriented movement findings with recorded control limits','No voltage-to-movement gain/probability; chronic and acute limits retained','CE-sharing'),
]
write('IDENTIFIABILITY.json',dict(quantities=[dict(id=i,quantity=q,classification=c,identified_value=v,scope=s,counterexample_test=ce) for i,q,c,v,s,ce in rows],
 all_IDENTIFIED_claims_have_counterexample_attempt=True,classification_is_not_capability_admission=True))

write('DESIGN_SUFFICIENCY.json',dict(
 classification='STAGE-5 DESIGN POSSIBLE UNDER EXPLICIT TRANSFER UNCERTAINTY',
 scope='Only a prospective conditional model/partial-identification study. No claim that a biological α1→UpWiN transfer, physical voltage prediction, or nonzero downstream bias is established.',
 prior_route_readiness_unchanged=True,stage5_authorized=False,stage5_protocol=None,
 calibrated_transfer_required=dict(for_conditional_order_and_sensitivity_questions=False,for_absolute_voltage_or_physiological_timing_prediction=True,for_unconditional_biological_signed_effect='Requires additional identifying evidence; calibration alone would not resolve identity/mediation.'),
 alternatives=[
  dict(kind='ordinal neural comparison',status='model-local only unless bridge assumed',requirement='use a defined neural scalar and invariant order, not a semantic preference or population-mean rank invented by a decoder'),
  dict(kind='sign/order change',status='conditional',requirement='explicit order-preserving source map, fixed other inputs, declared transfer sign and non-flat range; retain opposite-sign/null branches as unresolved alternatives'),
  dict(kind='experimentally bounded population perturbation',status='narrow assay endpoint only',requirement='observed photostimulation/recorded mV envelopes are not bounds on hidden α1 activity or a new target population'),
  dict(kind='parameter-swept unknown families',status='conditional sensitivity analysis possible',requirement='family-level analytic uncertainty first; every finite sweep range is an engineering coverage choice unless independently bounded; no parameter selected using downstream outcomes')],
 unknowns=['source-state scale and origin','source-to-Stage1 order map','target composition and cross-driver overlap','direct and total transfer sign outside observed acute protocol','monotonicity and operating range','gain','responder selection/detection probability','latency','kernel and observation filters','saturation and lower slope bound','conditioning-dependent gain versus input change','latent alternative-input contribution','voltage-to-downstream observation mapping'],
 minimum_information=['precise resolution and neural estimand','explicit observation domain with units and known support','declared identity/state/exclusion/observation bridges','admissible transfer families with null/opposite-sign alternatives','evidence-bounded versus assumed parameters separated','criterion stated as conditional or invariant before outputs are examined'],
 governance=['Freeze evidence hashes, estimand, model-family definitions and bridge assumptions before downstream results are accessible.','Keep parameter-choice personnel/process blind to downstream result values; freeze code/config hashes before unblinding.','If new measurement fitting becomes authorized, fit only independent physiological observations and keep Stage1/Stage5 outputs inaccessible to that process.','Predeclare family partitions and handling of unbounded nuisance ranges; do not call a finite arbitrary grid full-family coverage.','Retain all branches, failures and nulls; report conditional identification sets instead of choosing the branch with strongest output.','Any new evidence that removes a branch requires separately versioned review, not a post-outcome adjustment.'],
 full_family_invariants=['frozen upstream model difference remains an upstream fact','observed domain-specific summaries are retained','no guaranteed nonzero signed downstream effect follows'],
 conditional_invariants=['Strictly increasing source recoding preserves the order of the same scalar.','A fixed nonincreasing target map reverses weak order, possibly to equality; strict change requires responsiveness and non-flat range.','Any downstream claim must hold for every admissible nuisance/bridge choice in the declared subfamily, or be reported as conditional/partially identified.'],
 uninterpretable_if=['unknown gain/time constant taken from Stage1','4/17 used as universal cell-type/root responsiveness','calcium/spikes/model rates converted to mV without an observation map','cross-driver records joined by row order','only nonzero negative-transfer branches retained without declaring this assumption','effect-positive parameters selected after unblinding','monotone transfer sign presented as discovered sign','finite sensitivity grid presented as full admissible-family robustness','behavioral controls or recall mediation limitations erased'],
 no_positive_biological_result_guaranteed=True,new_biological_capabilities=[],physical_parameters_fitted=[]))
print(json.dumps(dict(stage1_order_records=len(order),recall_rows=sum(len(c['rows']) for c in recall),
 reciprocal_mean_difference_of_changes=[c['difference_of_changes']['mean'] for c in recall],sign_error=max(sign_errors),recall_error=max(abs(x['error']) for x in recall_null))))
