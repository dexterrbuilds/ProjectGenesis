"""Build design documents from filenames/manifests, never Stage-5 outcomes or neural execution."""
from pathlib import Path
import json,hashlib,ast
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,x):(HERE/n).write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
assert not (HERE/'RELEASE.json').exists(),'Sealed protocol: create a reviewed amendment, never overwrite.'
E='research/fly-stage1/evidence/4afc692f113981d1ad1a035ba7293e00bb4c8964bc1e87d9b00fab8063037c4b'
M=load(ROOT/E/'evidence-manifest.json')['files']
interventions=['freeze','silence_dan','remove_da_contacts','single_dan','matched_dan','remove_pn_kc','remove_kc_mbon','no_apl','no_recurrence','shuffle_pn_weights','unpaired']
names=[f'app-{s}-{c}-intact' for s in [1701,1702,1703] for c in ['A','B']]+[f'app-1701-{c}-{v}' for v in interventions for c in ['A','B']]
inputs=[]
for name in names:
 artifacts={}
 for file in ['summary.json','initial.json.gz','trained.json.gz','stimuli.json','trace.npz']:
  rel=f'{name}/{file}';assert rel in M
  artifacts[file]={'path':E+'/'+rel,'sha256':M[rel]}
 inputs.append({'run':name,'artifacts':artifacts,'state_fields':['baseline','post','restored','plastic_only'],'cues':['A','B'],'readout':'MBON_app','numeric_values_inspected_for_design':False})
tree=ast.parse((ROOT/'research/fly-stage1/model.py').read_text())
param_class=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Parameters')
parameters={n.target.id:ast.literal_eval(n.value) for n in param_class.body if isinstance(n,ast.AnnAssign)}
write('STAGE1_INPUT_LOCK.json',{'evidence_root':E,'run_count':len(inputs),'inputs':inputs,'frozen_parameters':parameters,'parameter_source':'literal dataclass defaults in pinned model.py; parsed as AST without importing/executing model','readout_definition':'Frozen probe: mean model rate in MBON_app group during second model second of two-second cue-only probe. Averaging order unchanged.','neural_rerun_allowed':False,'snapshot_ownership':'references to original bytes only','stage1_parameter_changes':[],'excluded_runs':'Aversive runs and model-parameter sensitivity arms are preserved, excluded because this protocol fixes the primary appetitive preparation; no exclusion based on Stage5 output.'})

families=[
 {'id':'E','partition':'EVIDENCE-ADMISSIBLE FAMILY','definition':'Union of every below qualitative branch, arbitrary cross-domain compatibility and arbitrary finite nuisance differences. No physiological numerical bounds.','symbolic_coverage':'all signs, flat/zero, heterogeneous mixtures, nonmonotone and context-dependent maps; explicit full-family nuisance','positive_claim_limit':'No universal nonzero direction follows solely from this family.'},
 {'id':'Z','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'f(x)=constant; nuisance contrast held equal (ν=0).','operator':'zero','nuisance':'matched','scope':'null transfer branch; not no anatomical contacts'},
 {'id':'P','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'Any strictly increasing scalar f; same f in a contrast; ν=0.','operator':'increasing','nuisance':'matched','scope':'source-to-output order preserved by assumption'},
 {'id':'R','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'Any strictly decreasing scalar f; same f in a contrast; ν=0.','operator':'decreasing','nuisance':'matched','scope':'source-to-output order reversed by assumption'},
 {'id':'WP','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'Any weakly increasing f, including local/full plateaus; ν=0.','operator':'weak_increasing','nuisance':'matched','scope':'flat/saturated nulls retained'},
 {'id':'WR','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'Any weakly decreasing f, including local/full plateaus; ν=0.','operator':'weak_decreasing','nuisance':'matched','scope':'flat/saturated nulls retained'},
 {'id':'H','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'A fixed mixture of responsive or flat components receiving this same abstract scalar, nonnegative weights summing to one, signs and membership unrestricted, responsive mass q in [0,1]; ν=0.','operator':'heterogeneous','nuisance':'matched','scope':'q not assigned 4/17; no physical cell count/root ownership; no independence assumption'},
 {'id':'U','partition':'RESTRICTED CONDITIONAL FAMILY','definition':'Any deterministic scalar f including nonmonotone functions; same f across each contrast; ν=0.','operator':'arbitrary','nuisance':'matched','scope':'local sign may differ from acute-protocol sign'},
 {'id':'N','partition':'EVIDENCE-ADMISSIBLE FAMILY','definition':'For each of Z/P/R/WP/WR/H/U, allow arbitrary finite nuisance contrast ν, including cue/history/learning-dependent alternatives and exact cancellation.','operator':'arbitrary','nuisance':'unrestricted','scope':'no inequality bound from existing data; union represents broad uncertainty, not an executable biological mechanism'}]
write('TRANSFER_FAMILIES.json',{'families':families,'selected_family':None,'biological_parameter_estimates':{},'physical_output_units':None,'engineering_numerical_sweep':None,'family_id_not_a_capability':True})
write('ASSUMPTION_PARTITIONS.json',{'EVIDENCE-ADMISSIBLE FAMILY':['Includes all unresolved qualitative alternatives; non-admitted mechanisms are hypotheses, not claimed facts.','Nuisance may vary with cue, history and preparation. No joint observation identifies it.','R64A11 acute-response constraints apply only in their domain; Z/P/R for a hypothetical Stage1-linked target do not erase those observations.'],
 'RESTRICTED CONDITIONAL FAMILY':['H-state: Stage1 saved scalar is used as an abstract ordered input, not calibrated biological α1 state.','H-identity: target is an abstract population-associated variable, not an identified driver or FlyWire root.','H-context: a matched-context contrast uses the same scalar f and equal nuisance in both terms. This is not measured physiology.','Monotonicity, strictness, scalar sufficiency and shared-map assumptions apply only to their named branches.','Mixture members receive the same abstract scalar; no root-specific rates or unobserved covariances are inferred.'],
 'ENGINEERING SENSITIVITY RANGE':['No numerical gain, time, q or saturation grid is used. Analytic sets cover the declared mathematical domains.','Decimal parsing preserves stored decimal tokens. Nonzero input differences within 1e-12 model units are conservatively sign-ambiguous; this is computational precision policy, not biology.'],
 'unknown_bridges':['biological source scale and ordering','recorded-population identity correspondence','direct receptor/transmission sign','latency/kernel','source-to-voltage observation map','cue/history-dependent alternative input','population heterogeneity weights'],
 'no_post_execution_pruning':True})
write('NUISANCE_SPEC.json',{'definition':'ν = z_condition − z_reference, an unidentified abstract nuisance contrast; not an anatomical neuron or injected current.','full_domain':'all finite real ν for each marginal contrast; no finite evidence-derived bound','shared_state_consistency':'z is indexed by run/cue/source state. Contrasts sharing a state share that latent value. Marginal sign sets do not assert every Cartesian-product sign combination is jointly realizable.','matched_context_restriction':'ν=0 because the two counterfactual terms hold nuisance equal, not because biology has zero alternative input','learning_dependent_nuisance_retained':True,'full_family_source_dependence_not_identified':True,'nuisance_fit':False,'unit':'abstract dimensionless output coordinate; no mV interpretation'})

write('ESTIMANDS.json',{'unit':'ordinal sets over {-1,0,+1}, not neural firing/voltage or action states','input':'x_{run,cue,state}=saved summary[state][cue][MBON_app]','output_name':'conditional downstream order set',
 'contrasts':[
 {'id':'response_change','left':'post','right':'baseline','definition':'S_D={sign(f(x_left)-f(x_right)+ν): (f,ν) in declared domain D}.'},
 {'id':'restoration_check','left':'restored','right':'baseline','definition':'same S_D, comparing archived restored response with original baseline'},
 {'id':'plastic_state_retention','left':'plastic_only','right':'baseline','definition':'same S_D after archived fast-state reset preserving plastic state'},
 {'id':'learned_state_comparison','left':'post','right':'restored','definition':'Full nuisance family remains unconditioned; ν=0 subfamilies are matched-context mathematical learned-state comparisons.'}],
 'evaluation_unit':'run × cue × contrast × family, never select only the trained cue or favorable seed',
 'joint_inference':'Only marginal per-contrast identification sets are computed. No Cartesian-product joint neural state or probability is inferred. Strict monotone control profiles hold for any common fixed map, without fitting one.',
 'secondary':['per-run paired and control cue sign-set profiles','matched-seed intervention profiles','conditional mechanism-dependence gate defined in CONTROL_MATRIX.json'],
 'not_estimands':['absolute mV','firing rate','latency','movement probability','heading prediction','semantic action label','new weighted combination of biological roots'],
 'normalization':'none; use the frozen readout; no across-run, cue, or post-outcome rescaling','no_pooled_crosscue_rank':True})

write('POPULATION_RESOLUTION.json',{'biological_resolution':'hypothetical population/type-associated interpretation only; not experimentally identified common population','executable_resolution':'abstract saved Stage1 group readout → mathematical ordinal set','separate_domains':['Stage1 dimensionless MBON_app','MB319C/MB043 biological α1 spike counts','R64A11-LexA acute somatic voltage','R64A11 population GCaMP6s','SS67249 recall voltage','SS33917 behavior','SS33918 behavior','FAFB anatomical roots'],
 'root_assignment':None,'root_context_only':['720575940617302365','720575940608236978'],'driver_membership_assignment':None,'biological_transfer_established':False,'observation_conversions':[]})
matrix=load(ROOT/'research/fly-upwin-transfer-identifiability/OBSERVATION_MATRIX.json')
write('OBSERVATION_COMPATIBILITY.json',{'source':'research/fly-upwin-transfer-identifiability/OBSERVATION_MATRIX.json','source_sha256':sha(ROOT/'research/fly-upwin-transfer-identifiability/OBSERVATION_MATRIX.json'),'matrix':matrix,'execution_use':'Context and scientific wording only. No recorded physical values enter Stage5 calculations.'})

controls=[
 ('intact','three seeds × both paired identities','baseline/post/restored/plastic_only','reference learned-state contrasts, no favorable-run selection'),
 ('freeze','seed1701 × A/B','baseline/post','block Stage1 plastic updates; a downstream difference need not vanish under unmatched nuisance'),
 ('silence_dan','seed1701 × A/B','baseline/post','disable modeled teaching pathway; not a biological target perturbation'),
 ('remove_da_contacts','seed1701 × A/B','baseline/post','disable modeled dopamine contact operator; no renormalization'),
 ('single_dan','seed1701 × A/B','baseline/post','one relevant DAN lesion; compare matched_dan, not all-DAN versus one-cell lesion'),
 ('matched_dan','seed1701 × A/B','baseline/post','one opposite-compartment DAN chosen anatomically in frozen Stage1; comparator, not guaranteed biologically unrelated'),
 ('remove_pn_kc','seed1701 × A/B','baseline/post','sensory-route disruption control; global responsiveness loss not learning specificity'),
 ('remove_kc_mbon','seed1701 × A/B','baseline/post','output-route disruption control; a loss here alone not mechanism-specific'),
 ('no_apl','seed1701 × A/B','baseline/post','frozen context control, do not retune'),
 ('no_recurrence','seed1701 × A/B','baseline/post','frozen recurrence control, no new circuit closure'),
 ('shuffle_pn_weights','seed1701 × A/B','baseline/post','frozen connectivity control; retain original verdict and topology limits'),
 ('unpaired','seed1701 × A/B','baseline/post','unpaired teaching timing control; do not relabel as paired')]
write('CONTROL_MATRIX.json',{'controls':[dict(id=i,coverage=c,fields=f,purpose=p) for i,c,f,p in controls],
 'within_run':['restored pre-training snapshot versus baseline','plastic-only fast-state reset versus baseline','both cues, including unpaired cue'],
 'comparison_rule':'Same cue and seed, same family and contrast; compare full sign-set profiles. Do not subtract effect magnitudes under arbitrary monotone maps.',
 'source_dependence_gate':{'scope':'restricted P/R matched-context only, no claim of biological mediation','requirements':['all six intact paired-cue response_change and plastic_state_retention sets exclude zero','all six intact restoration_check sets equal {0}','freeze, silence_dan, remove_da_contacts and unpaired paired-cue response_change at seed1701 equal {0}','PN and KC source baseline/post readouts for intact/freeze/silence_dan/remove_da_contacts/unpaired are present and unchanged to engineering 1e-12 model units','all source restoration_exact flags true and required original replay flags true'],
 'verdicts':['SATISFIED UNDER DECLARED CONDITIONAL FAMILY','NOT SATISFIED','UNASSESSABLE'],
 'unpaired_cue_requirement':'Report all unpaired-cue sets and original source responses. No invented zero-response or selective-effect threshold; this gate cannot establish strict cue-exclusive downstream change.',
 'matched_lesion_requirement':'Report single_dan versus matched_dan profiles separately; no guarantee of complete ablation or unrelatedness.'},
 'replicate_scope':'3 fixed primary seeds, 2 cue assignments; controls only seed1701. Not 28 independent biological replicates.',
 'replay':'Use saved Stage1 replay/restoration metadata and immutable snapshots. Future mathematical reanalysis must reproduce canonically serialized output byte-for-byte. No neural replay in this protocol.'})

write('ROBUSTNESS_DEFINITIONS.json',{'sign_alphabet':[-1,0,1],
 'analytic_rules':['For exactly equal scalar inputs and ν=0, every deterministic fixed scalar f yields equality.','For ordered inputs, strict increasing/decreasing maps preserve/reverse strict order; weak maps add zero.','Arbitrary fixed f or unrestricted-sign heterogeneous mixtures can preserve, reverse or erase distinct scalar order.','Unrestricted ν permits cancellation or either sign even for equal scalar inputs.','Known input scale cannot be inferred from invariant order; no magnitude or temporal claim follows.'],
 'numerics':{'mode':'Decimal arithmetic over frozen decimal tokens','epsilon':'0.000000000001','exact_equal':'{0} source order; exact stored equality only','small_nonzero':'source sign set {-1,0,+1}, flagged numerical ambiguity, never rounded to established zero','larger_nonzero':'stored sign, marked a model-artifact comparison'},
 'validity':'Analytic invariance over the declared mathematical family, not physiological validation. Finite examples never certify an unbounded family.',
 'nontractable':'Any extension not covered by the frozen analytic rules must be UNINTERPRETABLE until separately preregistered; do not fall back to a favorable grid.',
 'robust_atomic_claim':'For a specified contrast and family, the output sign set is a singleton; or an explicitly set-valued claim is proven for all family members. Do not relabel union breadth as one fixed neural outcome.'})
write('RESULT_CLASSIFICATION.json',{'unit':'per run/cue/contrast plus study-wide coverage flags','multi_label':True,
 'labels':{
 'ROBUST ACROSS DECLARED EVIDENCE-ADMISSIBLE FAMILY':'A predeclared atomic sign conclusion holds for every member of E/N (singleton full-family sign set). A robust zero remains a null result, not a positive capability.',
 'ROBUST ONLY UNDER RESTRICTED CONDITIONAL FAMILY':'At least one restricted family yields a singleton while full E/N does not; list exactly which restrictions and whether the singleton is zero. Always carry transfer-sensitive/null flags where applicable.',
 'TRANSFER-SENSITIVE / NON-ROBUST':'The full admissible set has more than one sign, or compatible restricted families disagree; include concrete witnesses.',
 'NULL-COMPATIBLE':'Zero belongs to the full admissible set; this is not proof that the true biological effect is zero.',
 'UNINTERPRETABLE':'Integrity/schema/unit/identity gate fails, source evidence does not support requested contrast, classification cannot be evaluated, or a nonpreregistered operator is required.'},
 'precedence':'UNINTERPRETABLE blocks substantive classification; otherwise labels coexist. Never reduce all branches to a single positive score.',
 'study_summary':'Report every unit and family, all counterbalanced rows, gate coverage and counts. Overall presence of transfer sensitivity/nulls cannot be hidden by restricted-family singletons.',
 'acceptance':'A complete integrity-preserving analysis returning any valid nonrobust/null conclusion is scientifically completed. No biological-capability PASS threshold exists.',
 'positive_terms_prohibited':['biological α1→UpWiN propagation validated','general action selection','voluntary action','Genesis behavior'],
 'structural_limit':'The full-family signed-singleton category may be analytically unattainable with unrestricted nuisance. Never remove a branch to make this label attainable. Set-valued uncertainty statements must be distinguished from a unique neural output.',
 'design_status':'STAGE-5 PROTOCOL READY FOR EXECUTION REVIEW','execution_result':None})
write('COUNTEREXAMPLE_REGISTRY.json',{'source':'research/fly-upwin-transfer-identifiability/COUNTEREXAMPLES.json','entries':[
 {'claim':'learned signal has nonzero downstream effect','adversary':'Z or a local plateau; or ν exactly cancels f(left)-f(right)','required_downgrade':'conditional nonzero only'},
 {'claim':'direction is determined','adversary':'P versus R; or unrestricted ν reverses either','required_downgrade':'conditional direction only'},
 {'claim':'same sign under monotonic map means biological inhibition','adversary':'earlier CE-sign: opposite direct sign plus covarying unmeasured input','required_downgrade':'assumed function orientation, not receptor evidence'},
 {'claim':'all target cells express learning','adversary':'H with zero responsive mass or mixed signs/cancellation','required_downgrade':'no target population fraction identified'},
 {'claim':'learning causes recall-related downstream change','adversary':'N varies with cue/history independently of Stage1 state; alternatively nuisance cancels real model influence','required_downgrade':'matched-context mathematical dependence only'},
 {'claim':'cue-selective magnitude is invariant','adversary':'nonlinear increasing f changes differences-of-differences and effect ratios','required_downgrade':'do not compute a universal magnitude ranking'},
 {'claim':'restored equality establishes physiological reset','adversary':'same scalar with different hidden context under N','required_downgrade':'saved-model reset plus matched-map equality only'},
 {'claim':'action-related kinematics follow','adversary':'no identified observation map; behavioral domains remain separate','required_downgrade':'no kinematic prediction allowed'}],
 'execution_requirement':'Emit the counterexample references and applicable analytic family alternatives beside every restricted positive conclusion; no new fitting.'})
write('PARAMETER_PROVENANCE.json',{'parameters':[
 {'name':'seeds','value':[1701,1702,1703],'category':'FROZEN MODEL DESIGN','source':'research/fly-stage1/experiment.py:SEEDS','biological_parameter':False},
 {'name':'cue labels','value':['A','B'],'category':'FROZEN COUNTERBALANCING','source':'research/fly-stage1/experiment.py','semantic_input_to_transfer':False},
 {'name':'readout','value':'MBON_app mean in frozen probe','category':'FROZEN MODEL OBSERVATION','source':'research/fly-stage1/experiment.py:probe','biological_parameter':False},
 {'name':'epsilon','value':'1e-12 model units','category':'ENGINEERING PRECISION POLICY','source':'Prospectively declared here, consistent with prior algebraic verification tolerance; not a physical detection threshold.'},
 {'name':'decimal precision','value':50,'category':'ENGINEERING ARITHMETIC POLICY','source':'Prospectively declared storage/roundoff handling; no biological interpretation.'},
 {'name':'gain','value':None,'coverage':'no finite bound; strict order families quantify over every allowed monotone map'},
 {'name':'responder mass q','value':None,'coverage':'all [0,1] in H, including endpoints; not estimated from 4/17'},
 {'name':'saturation/plateau','value':None,'coverage':'all weak monotone maps and constant branch; no lower slope bound'},
 {'name':'nuisance difference','value':None,'coverage':'all finite reals in N/E; matched-context equality only in conditional families'},
 {'name':'latency/kernel','value':None,'coverage':'not an estimand; no temporal neural model'},
 {'name':'physical observation conversion','value':None,'coverage':'prohibited without independently identified mapping'}],
 'engineering_grid':None,'physiological_confidence_interval':None,'post_outcome_normalization':False})
write('BLINDING_FIREWALL.json',{'design_authorized':True,'execution_authorized':False,'design_inspected':['frozen source code','filenames/manifests/hashes','prior identifiability specifications','previously reviewed Stage1 conclusions'],
 'not_inspected':['Stage5 outputs','new downstream parameter evaluations','new neural simulations'],
 'current_validation':'Static schema/hash/AST and governance tests only; no import or call of prospective_analysis.py.',
 'future_gate':'Separate explicit user authorization naming this exact release hash; read-only sealed protocol plus external authorization record; analysis output must be in a separate empty run directory.',
 'post_freeze':'No edits to family definitions, assumptions, code, priors, readout, numeric tolerance, controls or normalization after outcome access. Amendments require a new version and renewed review.',
 'forbidden_inputs':['LLM reasoning/planner','wallet/economy/business state','physical threat/product concepts','new behavioral outputs used for fitting'],
 'neural_model_execution':False,'biological_parameter_fit':False})
write('EXECUTION_AUTHORIZATION_CHECKLIST.json',{'status':'AWAITING SEPARATE USER REVIEW','authorization_granted':False,
 'before_execution':['Review this release hash and all conditional-scope limits.','Obtain explicit user authorization for archived-data mathematical analysis only.','Record reviewed release hash and authorization outside sealed protocol.','Verify every dependency, snapshot, source summary and protocol hash.','Confirm canonical state unchanged and scheduler disabled without activating runtime.','Prepare a separate empty output directory; deny writes to canonical and frozen research.','Verify all families, nuisance branches, controls and both cues are included.','Keep physical observation values and behavioral outputs out of calculations.','Perform two fresh-process mathematical analyses for byte-identical replay only after authorization.','Report all branches and counterexamples; no capability admission.'],
 'not_authorized_even_by_this_design':['neural model runs','Genesis integration','BrainAdapter changes','parameter fitting','new anatomical extraction','Stage6 or new capability'],
 'reviewer_decision':None})
write('PREREGISTRATION.json',{'version':'0.1.0','type':'prospective protocol; archived data reanalysis','design_authorized':True,'execution_authorized':False,
 'primary_question':'Which, if any, ordinal downstream conclusions are invariant across declared transfer uncertainty when using a frozen learned model signal?',
 'planned_run_count':len(inputs),'family_ids':[f['id'] for f in families],'contrast_ids':['response_change','restoration_check','plastic_state_retention','learned_state_comparison'],
 'planned_units_formula':'28 source runs × 2 cues × 4 contrasts; every unit reports every family. These are design counts, not results.',
 'selection':'Fixed primary appetitive runs and all original primary causal controls; no sampling or optimizing against Stage5 outcomes.',
 'normalization':'none','new_training':False,'outcome_values':None,'stopping_rule':'Stop after the complete fixed analysis/verification battery, regardless of signs, nulls, or failures; no adaptive enlargement.',
 'failure_handling':'Missing/corrupt/mismatched inputs stop before analysis. Nonfinite/invalid source schemas or required original restoration/replay failure are UNINTERPRETABLE; do not impute, regenerate, drop, or retune.',
 'scope':'abstract population-associated order; neither identified UpWiN voltage nor action behavior'})
print(json.dumps({'design_documents_written':True,'planned_source_runs':len(inputs),'source_summary_values_loaded':False,'stage5_executed':False}))
