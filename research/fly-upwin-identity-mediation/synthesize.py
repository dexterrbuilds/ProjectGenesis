"""Evidence synthesis only. No neural model, numerical fitting, or database access."""
from common import *
import re

article='https://elifesciences.org/articles/85756'
figures=article+'/figures'
peer=article+'/peer-reviews'
earlier='https://elifesciences.org/articles/79042/peer-reviews'
drivers={x:f'https://splitgal4.janelia.org/cgi-bin/view_splitgal4_imagery.cgi?line={x}' for x in ['SS67249','SS33917','SS33918']}

def mapping(a,b,status,scope,evidence):
 return dict(source_identity=a,target_identity=b,classification=status,scope=scope,evidence=evidence)

maps=[
 mapping('FAFB v783 720575940617302365','MBON07 / MBON-α1','IDENTIFIED','pinned annotation; not a physiological recording',[str(PRIOR.relative_to(ROOT))+'/CROSSWALK.json']),
 mapping('FAFB v783 720575940608236978','SMP353','IDENTIFIED','pinned annotation; not a physiological recording',[str(PRIOR.relative_to(ROOT))+'/CROSSWALK.json']),
 mapping('hemibrain SMP353/SMP354','FAFB SMP353/CB3112 (SMP354 alias)','TYPE-COMPATIBLE','cross-specimen type/annotation correspondence; no physiological identity transfer',[str(PRIOR.relative_to(ROOT))+'/CROSSWALK.json']),
 mapping('SS33917 morphology set','SMP353, SMP354, SMP348, SLP399, SLP400','TYPE-COMPATIBLE','published LM–EM matching of ensemble; does not label recorded responders',[figures+'#fig3s1',figures+'#fig3s2']),
 mapping('SS33918','SS33917-like UpWiN ensemble','TYPE-COMPATIBLE','similar 8–11-neuron expression; exact membership per animal unknown',[figures,drivers['SS33918']]),
 mapping('R64A11-LexA','broad UpWiN population','IDENTIFIED','experimental driver definition only; not a pure SMP353/SMP354 type',[article]),
 mapping('R64A11-LexA recorded responder','SMP353 or SMP354','POSSIBLE','candidate types only; no discriminating cell-linked morphology',[article,earlier]),
 mapping('SS67249 MCFO example','SMP353','TYPE-COMPATIBLE','published morphological resemblance; no mapping of Fig5 cells',[figures+'#fig5s1']),
 mapping('SS67249','SMP354 membership','UNRESOLVED','no independently discriminating per-cell assignment in audited sources',[article,drivers['SS67249']]),
 mapping('SS67249','other/off-target identities','UNRESOLVED','off-target expression reported; identities of recorded cells not supplied',[article]),
 mapping('SS67249 recorded cells','β1-associated cell identity','UNRESOLVED','β1 confound belongs to R58E02-LexA reinforcement; no evidence identifies these recorded cells as β1 cells',[article]),
 mapping('SS67249 Fig5 recording','SS33917/SS33918 behavioral population member','POSSIBLE','overlap motivated by morphology, not a registered recording-to-behavior crosswalk',[article,figures]),
]
write('IDENTITY_CROSSWALK.json',dict(mappings=maps,roots_are_references_only=True,anatomy_ownership=[],
 driver_intersections=[dict(driver=k,AD=a,DBD=d,source=drivers[k]) for k,a,d in [('SS67249','VT040580','R64A11'),('SS33917','VT007746','R64A11'),('SS33918','VT007746','R66B12')]],
 common_hemidriver_does_not_identify_equal_population=True,
 specimens=[dict(specimen_id=s,vfb_id=v,driver=d,recording_link=None,meaning='independent driver morphology specimen, not a Fig4/5 recording identity') for s,v,d in [('20200228_19_A10','VFB_00103h2o','SS67249'),('20200814_31_C3','VFB_00103k1j','SS67249'),('20200228_19_A9','VFB_00103hpc','SS67249'),('20200904_19_F9','VFB_00103hr5','SS33917')]]))

write('TRANSMISSION.json',dict(
 presynaptic=dict(population='MBON-α1',transmitter='glutamate',scope='type-level evidence; inherited frozen source audit',source=article),
 observed=dict(driver='R64A11-LexA',quantity='baseline-subtracted membrane voltage',units='mV',responders=4,tested_neurons=17,reported_flies=12,sign='negative response in four sampled cells after α1 photostimulation',source=article+'#fig4'),
 target_specific=[dict(type=t,receptor=None,sign=None,paired_recording=None,localization=None,identified_target_perturbation=None) for t in ['SMP353','SMP354']],
 scope='No target-specific receptor/sign evidence identified in searched sources. This is not proof of absence of such physiology.',
 inhibitory_synaptic_current_measured=False,monosynaptic_transmission_isolated=False,
 independent_replications_added=0,
 earlier_caption=dict(source=earlier,wording='SMP353/354',same_alpha1_counts=[4,17,12],interpretation='Earlier presentation of the same result, not independently identified cells or replication.',alpha3_earlier_counts=[2,6,4],alpha3_final_counts=[3,11,7]),
 receptor_search=dict(categories=['paired recording','target-specific transcriptomics','receptor localization','synapse-local receptor','identified-target physiology','receptor perturbation'],result='No independently target-resolved positive result located',excluded_inferences=['glutamate implies inhibition','general fly GluCl evidence specifies SMP353 receptors','anatomical shunting hypothesis measures receptor function','simulation using SMP354 establishes its physiology']),
 parameters_fitted=[]))

links=[
 dict(id='alpha1-stimulation-to-sampled-voltage',classification='SUPPORTED',intervention='MB310C-driven α1 photostimulation',observation='negative somatic voltage response in 4/17 broadly labeled cells',phase='acute physiology, not learning',scope='sampled R64A11 cells',source=article+'#fig4',does_not_establish='target type, receptor, monosynaptic sign or mediation'),
 dict(id='alpha1-alpha3-population-interaction',classification='SUPPORTED',intervention='α1 and α3 coactivation versus α3 activation',observation='suppression of population calcium response',phase='dissected-brain physiology',scope='population ROI; not a cell-resolved current-clamp assay',source=article+'#fig4',does_not_establish='α1 inhibition during learned recall'),
 dict(id='conditioning-to-ss67249-response',classification='SUPPORTED',intervention='odor paired with R58E02-LexA DAN activation',observation='paired odor depolarization increases; reciprocal odor training',phase='conditioning followed by recall measurement',scope='11 source rows in two cohorts; same-row pre/post measurements',source=article+'#fig5',does_not_establish='α1-specific mediation; β1 reinforcement also possible'),
 dict(id='alpha1-learning-to-upwin-recall',classification='UNRESOLVED',intervention=None,observation=None,phase='link between separately measured preparations',scope='no joint α1-state/identified-UpWiN measurement resolved',source=peer,does_not_establish='disinhibition; reviewer request not satisfied by a new direct α1 inhibition assay'),
 dict(id='upwin-activation-to-wind-oriented-movement',classification='SUPPORTED',intervention='SS33917/SS33918 activation',observation='wind-related turning and locomotion; airflow/arista/control comparisons',phase='acute expression',scope='driver populations',source=article+'#fig6',does_not_establish='individual SMP353/SMP354 causality or a continuous voltage-to-behavior conversion'),
 dict(id='chronic-blockade',classification='PARTIAL',intervention='TNT',observation='reduced learned behavior including upwind component',phase='chronic across acquisition/consolidation/recall/expression',scope='UpWiN-driver populations',source=article+'#fig7',does_not_establish='recall-specific mediation'),
 dict(id='acute-blockade-binary-memory',classification='SUPPORTED',intervention='temperature-restricted shibire',observation='binary memory performance impairment',phase='recall-period test',scope='endpoint-specific, temperature-dependent preparation',source=article+'#fig7',does_not_establish='upwind mediation'),
 dict(id='acute-blockade-upwind',classification='CONTRADICTED',intervention='shibire at restrictive temperature',observation='required control upwind behavior absent',phase='recall-period test',scope='claim of successful validation of this endpoint is contradicted; biological role not disproven',source=article+'#fig7',does_not_establish='a validated upwind endpoint'),
 dict(id='complete-mediated-chain',classification='UNRESOLVED',intervention=None,observation=None,phase='acquisition through expression',scope='no joined identified preparation found',source=peer,does_not_establish='α1 change is necessary/sufficient for recall-related UpWiN change and ensuing steering'),
]
write('MEDIATION.json',dict(links=links,numerical_composition=False,prior_proof_not_required_for_future_hypothesis_test=True,
 phase_boundaries=dict(acquisition='formation during pairing',consolidation='post-training stabilization; not isolated by chronic TNT',recall='odor-evoked retrieval',expression='neural-to-movement contribution; not interchangeable with memory score'),
 peer_review_resolution='Authors allowed α3/other input alternatives and removed disinhibition wording; no new direct α1-inhibition-to-UpWiN experiment supplied in this response.',
 missing_evidence_is_not_evidence_of_no_route=True))

requirements=[
 ('defensible source identity','SUPPORTED','Pinned MBON07/α1 anatomy and type evidence; Stage-1 rate remains model-specific.'),
 ('defensible downstream target identity','PARTIAL','Anatomical candidates and broad driver definitions available; four responders and 11 recall rows have no resolved type/root identity.'),
 ('directional anatomy','SUPPORTED','Frozen starting-root pair has 11 contacts; cross-specimen driver/type bridges remain qualified.'),
 ('target-scoped physiological sign','PARTIAL','Negative voltage in four sampled R64A11 cells; SMP353/SMP354-specific sign/receptor unresolved.'),
 ('measurable downstream neural variable','SUPPORTED','Somatic voltage in mV and separately population fluorescence; no interchange or inferred current.'),
 ('conditioning-compatible evidence','PARTIAL','SS67249 recall measurements are real; R58E02 β1 contribution and cross-driver identity unresolved.'),
 ('independently action-related variable','SUPPORTED','Driver activation affects wind-related turning/locomotion; no action label or voltage-to-behavior calibration.'),
 ('causal intervention evidence','PARTIAL','Acute activation and chronic blockade informative; route-specific recall mediation not isolated.'),
 ('preparation compatibility','PARTIAL','Cross-animal type comparison legitimate in principle; specific recorded-to-behavioral population correspondence remains unresolved.'),
 ('raw data for thresholds and held-out validation','PARTIAL','Cell-averaged traces and paired scalar rows available; trial identities/morphology linkage/raw tracks not recovered. Cannot declare fly-held-out validation.'),
]
write('READINESS.json',dict(classification='PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED',
 requirements=[dict(id=i+1,requirement=n,classification=c,reason=r) for i,(n,c,r) in enumerate(requirements)],
 resolutions=[
 dict(resolution='individual-root',design_justified=False,status='UNRESOLVED',reason='Physiological recordings are not mapped to roots; exact root propagation cannot be asserted.',permitted_claim='pinned anatomical route only'),
 dict(resolution='cell-type',design_justified=False,status='PARTIAL',reason='Morphology motivates SMP353/SMP354, but responders and recall cells are not independently typed; their sign and conditioning mediation cannot yet be assigned to that type.',permitted_claim='type-compatible candidate anatomy with explicitly unresolved physiology'),
 dict(resolution='driver-population',design_justified=False,status='PARTIAL',reason='Each driver defines valid assays, but R64A11 physiology, stochastic SS67249 recall and SS33917/18 movement are not one identified population. A standalone population-level biological experiment is defensible; the requested modeled α1→target→recall→action-bias chain is not yet sufficiently specified.',permitted_claim='separate driver-scoped neural and behavioral findings, not root/type propagation')],
 root_identity_is_not_universal_prerequisite=True,
 complete_prior_mediation_proof_is_not_prerequisite=True,
 reasons_beyond_missing_root_identity=['unregistered cross-driver target correspondence','β1/α3 alternative routes not isolated','no observation-compatible link from Stage-1 activity to sampled physiology','no joint mediation dataset or suitable linked raw records'],
 minimum_evidence_gaps=['recording-to-morphology or independently typed target correspondence','compatible α1-specific perturbation/recall evidence in the same identified target population','trial/animal identifiers and appropriate behavioral/physiological controls for prospective criteria'],
 stage5_authorized=False,stage5_protocol=None,neural_runs=0,fitted_parameters=[],decoder=None,capability_promotions=[],canonical_writes=0))

queries=['"UpWiN" "dataset" recordings morphology','"SMP353" "receptor"','"85756" "zenodo" OR "figshare" OR "dryad" OR "github"','"SMP354" "GluCl" electrophysiology','"SMP353" "transcriptomics" receptor','"SS67249" recording morphology data','"Neural circuit mechanisms for transforming" "data" repository raw','site:zenodo.org "85756"','site:figshare.com "wind-oriented" Aso','site:datadryad.org "UpWiN"','"SMP353" paired recordings receptor localization']
write('SEARCH_AUDIT.json',dict(queries=queries,search_date='2026-09-20',scope='Public indexed literature and original publisher/driver-resource records; not an exhaustive search of private or unindexed data.',
 repositories=dict(publisher='Final source workbooks already frozen; all 36 original accepted-manuscript workbooks recovered and byte-identical to final files.',microscopy='FlyLight primary driver pages and VFB registered specimens acquired; no recording linkage found. Original Fig5 morphology PDF visually inspected; MCFO cell#1–3 are not electrophysiological row identifiers.',neuronbridge='Landing application acquired; no cell-specific recording identifier available for a registered physiology match. No claim of exhaustive internal search.',indexed_deposits='No additional trial/morphology/identity deposit located by the documented title/DOI/type searches.',github='Original article links FlyTracker, NeuTu and VVD_Viewer software; these links are not a deposit of Fig4/5 trials or persistent behavioral tracks.'),
 original_software_links=['https://github.com/kristinbranson/FlyTracker','https://github.com/janelia-flyem/NeuTu','https://github.com/takashi310/VVD_Viewer'],
 rejected_shortcuts=['Earlier SMP353/354 caption is not independent cell identification','Reviews and downstream computational models are not independent physiology','Whole-brain GluCl expression or anatomical shunting proposals do not identify the target receptor','A movie overlay is not a deposited machine-readable track with persistent identities'],
 author_contact=False,unknowns_not_zero=True))

urls=load(HERE/'URLS.json')
write('SOURCE_MANIFEST.json',dict(originals=[dict(key=k,url=u,path='sources/'+k+'.html',sha256=sha(HERE/'sources'/f'{k}.html'),bytes=(HERE/'sources'/f'{k}.html').stat().st_size) for k,u in urls.items()],
 reused_originals='Referenced via frozen route-study release; no originals modified or new trials synthesized.',
 license='Publisher content attributed to original authors (eLife CC BY); FlyLight/VFB metadata attributed to Janelia/VFB. Preserve source-specific license statements. No license inferred for unrelated software.',
 parser_note='HTML originals retained byte-for-byte. Derived plain text uses replacement for undecodable bytes; consult originals for authoritative encoding.',
 ancillary_files=[dict(path=str(p.relative_to(HERE)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted((HERE/'sources').rglob('*')) if p.is_file() and p.suffix not in ['.html','.txt','.json']]))
