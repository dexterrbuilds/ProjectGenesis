"""Read-only parameter and annotation audit. No Stage result tables are read."""
import ast,csv,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 inventory=json.loads((H/'PARAMETER_INVENTORY.json').read_text())
 specs={
 'dt':('unconstrained','Numerical resolution, not physiology. Convergence is numerical evidence, not a measured 10 ms clock.','E18'),
 'tau':('unconstrained','Global 50 ms rate relaxation cannot be identified from calcium decay or a different MBON14 membrane constant.','E01,E13,E18'),
 'eligibility_tau':('weakly constrained','Temporal order matters. No transferable measurement identifies a single 0.5 s exponential in all compartments.','E07,E09'),
 'learning_rate':('unconstrained','0.08 multiplies unknown rate, eligibility and DA scales; response depression identifies at most an integrated product.','E07,E08,E11'),
 'kc_threshold':('weakly constrained','Sparse nonlinear coincidence is supported; dimensionless 0.15 is uncalibrated.','E01,E02,E03'),
 'dopamine_threshold':('unconstrained','0.2 rate cutoff is not a measured receptor activation threshold.','E07,E08,E09'),
 'pn_gain':('unconstrained','3 depends on rate units, artificial cue amplitude and normalization; EPSPs alone do not identify it.','E01,E02'),
 'recurrent_gain':('unconstrained','0.05 is neither an experimentally measured shared conductance nor a receptor-specific gain.','E04,E16'),
 'apl_gain':('weakly constrained','Inhibitory influence is supported; magnitude 1 and one scalar APL state are not. Local-response fit is non-transferable.','E05,E06'),
 'fast_gain':('unconstrained','Global multiplicative scale confounded with connection gains; cannot be fitted separately without conventions and observations.','E01,E04'),
 'boundary_current':('product-boundary assumption','Default zero describes unknown inputs, not measured physiological silence.','E19'),
 'boundary_noise':('product-boundary assumption','Default zero; missing stochastic input distribution is not determined by omitted contact counts.','E19'),
 'min_multiplier':('unconstrained','0.1 is a hard floor, not a measured lower synaptic efficacy. Aggregate 90% depression does not identify this floor.','E07'),
 'feedback_gain':('unconstrained','0.1 MBON-to-DAN scale unmeasured; type-level connectivity is not conductance.','E11,E19'),
 'recovery_tau':('weakly constrained','Recovery over minutes/hour constrains timescale loosely; 1800 s and exponential law not identified; other odors matter.','E11,E12'),
 'normalization':('unconstrained','Full proofread input vs retained role mass are numerical assumptions; neither follows from physiological normalization.','E02,E06'),
 'body_tau':('product-boundary assumption','60 s converts synthetic resource input into a state. No starvation/peptide concentration kinetics calibrate it.','E13,E14,E15'),
 'gate_floor':('product-boundary assumption','0.2 lower bound of a linear synthetic resource→PPL101 gate is not measured.','E14,E15,E20'),
 'dopamine_gain':('unconstrained','Gain 1 in acute divisor 1/(1+D) has no dose-response or unit mapping.','E07,E14'),
 'oa_gain':('weakly constrained','VPM4 suppresses MBON11 in tested preparation; magnitude 1 and fast additive inhibitory implementation not established.','E13')}
 rows=[]
 for stage,params in inventory.items():
  source=ROOT/f'research/fly-stage{stage}/model.py'
  tree=ast.parse(source.read_text());c=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='Parameters')
  actual={x.target.id:ast.literal_eval(x.value) for x in c.body if isinstance(x,ast.AnnAssign)}
  assert actual==params
  for name,value in params.items():
   status,note,evidence=specs[name]
   rows.append(dict(stage=int(stage),name=name,value=value,status=status,note=note,evidence=evidence.split(','),source=f'research/fly-stage{stage}/model.py'))
 extras=[
 ('contact_to_strength','unconstrained','Weights proportional to anatomical contacts; per-contact release probability, silent synapses, receptor density, electrotonic location unknown.','E02,E04,E19'),
 ('normalization_stage1','unconstrained','Hardcoded retained presynaptic-role denominator; no physiological calibration.','E06'),
 ('known_cholinergic_KC','experimentally constrained','Class-level transmitter identity supported; not every target-specific net effect or numerical gain.','E04'),
 ('APL_GABA_inhibition','experimentally constrained','Sign of tested APL→KC inhibitory effect supported; scalar implementation not validated.','E05,E06'),
 ('MBON11_GABA','experimentally constrained','Known GABA identity; effective downstream target sign/gain still needs target-specific physiology.','E14'),
 ('MBON07_to_PAM11_positive_sign','weakly constrained','NMDA requirement supports hypothesis; direct net excitation not established by source. Frozen code comment is stronger than evidence; left untouched and qualified here.','E10,E16'),
 ('MBON07_other_outputs_zero','unconstrained','Computational omission, not proof of no transmission. Stage3 zeros even PAM-related output.','E10'),
 ('DAN_fast_effect_zero','unconstrained','Convenience separation of fast and modulatory effects, not measured absence of acute transmission.','E08,E19'),
 ('OA_other_targets_zero','unconstrained','Unknown receptor effects omitted, not physiologically absent.','E13'),
 ('DA_locality','weakly constrained','Compartmental modulation supported; DAN→KC versus DAN→MBON contact-normalized rate does not identify release/receptor exposure.','E07,E11,E19'),
 ('KC_MBON_APL_gain1','unconstrained','Hardcoded fixed gain lacks synaptic current normalization.','E04,E05'),
 ('MBON11_gain20x_conflict','unconstrained','Stage1 recurrent 0.05 vs Stage3 source 1 on many shared outputs; same anatomy does not reconcile strengths.','E13,E14'),
 ('MBON18_PN_to_LH_gain1','unconstrained','Anatomical pathways supported, fixed scale and effective target physiology unknown.','E13'),
 ('clipped_rate_0_1','unconstrained','No Hz/current/calcium observation mapping; a zero lower bound cannot itself express below-baseline fluorescence.','E07,E11'),
 ('point_neurons','weakly constrained','Local APL data challenge one globally uniform state; other cell classes require separate checks.','E05,E18'),
 ('plasticity_LTD_only','weakly constrained','Narrow pairing protocols support depression; unpaired DAN and reverse timing can have other effects.','E07,E08,E09'),
 ('postsynaptic_multiplier','weakly constrained','Receptor evidence supports a possible locus in alpha-prime3, not a complete per-contact rule for all stages.','E12'),
 ('acute_vs_persistent_rule','unconstrained','Stage3 acute divisor plus persistent LTD cannot be derived by merging behavior studies and conditioning endpoints.','E07,E14'),
 ('initial_efficacy1','unconstrained','Unit efficacy and zero eligibility at t0 are initialization conventions, not naive-synapse measurements.','E07'),
 ('resource_linear_gate','product-boundary assumption','PPL101 desired rate multiplied by 0.2+0.8r; r is not a measured nutrient/hormone state. Direction alone does not identify shape.','E14,E15,E20'),
 ('synthetic_cue_teacher_OA_currents','product-boundary assumption','Arbitrary PN cues and dimensionless teacher/OA currents are not odor concentration, spikes or transmitter dose.','E02,E07,E13'),
 ('NO_peptide_receptor_omission','unconstrained','Chemical edges do not establish NO/sNPF/dNPF kinetics or receptor graph. Zero omitted action is a model choice.','E04,E15,E17'),
 ('no_transmission_delays','unconstrained','Synchronous 10 ms updates do not measure propagation or receptor kinetics.','E07,E09'),
 ('pooling_and_readout','product-boundary assumption','Averaging MBON groups and cue-response metrics is an assay choice, not a behavioral motor output.','E11,E13')]
 for name,status,note,ev in extras:rows.append(dict(stage='shared/operator',name=name,value=None,status=status,note=note,evidence=ev.split(','),source='frozen models and protocols'))
 (H/'PARAMETER_EVIDENCE.json').write_text(json.dumps(rows,indent=2)+'\n')
 md=['# Parameter–evidence matrix','', 'Statuses refer to the stated scope: a measured sign does not calibrate its numeric gain. Product-boundary denotes a synthetic external/preparation boundary; no Genesis mapping is introduced. Every declared dataclass field is covered, followed by operator assumptions.','', '| Stage | Assumption | Frozen value | Classification | Evidence / interpretation |','|---|---|---|---|---|']
 for r in rows:md.append(f"| {r['stage']} | {r['name']} | {r['value']} | {r['status']} | {', '.join(r['evidence'])}: {r['note']} |")
 (H/'PARAMETERS.md').write_text('\n'.join(md)+'\n')
 # Annotation join uses root-ID strings, never numeric coercion.
 anno=ROOT/'outputs/flywire-research/annotations-v3.1.0.tsv'
 byid={r['root_id']:r for r in csv.DictReader(anno.open(),delimiter='\t')}
 selected={}; hashes={}
 types={'APL','PAM11','PPL101','PPL104','MBON07','MBON11','MBON18','MBON16','MBON17','MBON17-like','MBON28','OA-VPM4'}
 for s in (1,2,3):
  p=next((ROOT/f'research/fly-stage{s}/artifacts').glob('*/circuit.json'));hashes[str(p.relative_to(ROOT))]=sha(p)
  for n in json.loads(p.read_text())['nodes']:
   if n['cell_type'] not in types:continue
   a=byid[n['root_id']];assert a['cell_type']==n['cell_type']
   v=selected.setdefault(n['root_id'],{'root_id':n['root_id'],'stages':[],**{k:a[k] for k in ('cell_type','hemibrain_type','side','fbbt_id','vfb_id','known_nt','top_nt','matching_notes')}});v['stages'].append(s)
 out={'dataset':'FAFB/FlyWire v783 adult female','annotations':'v3.1.0','annotation_sha256':sha(anno),'circuit_hashes':hashes,'identity_level':'annotation/type crosswalk, not individual physiological equivalence','rows':list(selected.values())}
 (H/'CROSSWALK.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Audited',len(rows),'parameter/operator entries;',len(selected),'named root IDs')
if __name__=='__main__':main()
