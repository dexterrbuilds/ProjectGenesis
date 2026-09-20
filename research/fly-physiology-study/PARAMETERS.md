# Parameter–evidence matrix

Statuses refer to the stated scope: a measured sign does not calibrate its numeric gain. Product-boundary denotes a synthetic external/preparation boundary; no Genesis mapping is introduced. Every declared dataclass field is covered, followed by operator assumptions.

| Stage | Assumption | Frozen value | Classification | Evidence / interpretation |
|---|---|---|---|---|
| 1 | dt | 0.01 | unconstrained | E18: Numerical resolution, not physiology. Convergence is numerical evidence, not a measured 10 ms clock. |
| 1 | tau | 0.05 | unconstrained | E01, E13, E18: Global 50 ms rate relaxation cannot be identified from calcium decay or a different MBON14 membrane constant. |
| 1 | eligibility_tau | 0.5 | weakly constrained | E07, E09: Temporal order matters. No transferable measurement identifies a single 0.5 s exponential in all compartments. |
| 1 | learning_rate | 0.08 | unconstrained | E07, E08, E11: 0.08 multiplies unknown rate, eligibility and DA scales; response depression identifies at most an integrated product. |
| 1 | kc_threshold | 0.15 | weakly constrained | E01, E02, E03: Sparse nonlinear coincidence is supported; dimensionless 0.15 is uncalibrated. |
| 1 | dopamine_threshold | 0.2 | unconstrained | E07, E08, E09: 0.2 rate cutoff is not a measured receptor activation threshold. |
| 1 | pn_gain | 3.0 | unconstrained | E01, E02: 3 depends on rate units, artificial cue amplitude and normalization; EPSPs alone do not identify it. |
| 1 | recurrent_gain | 0.05 | unconstrained | E04, E16: 0.05 is neither an experimentally measured shared conductance nor a receptor-specific gain. |
| 1 | apl_gain | 1.0 | weakly constrained | E05, E06: Inhibitory influence is supported; magnitude 1 and one scalar APL state are not. Local-response fit is non-transferable. |
| 1 | fast_gain | 1.0 | unconstrained | E01, E04: Global multiplicative scale confounded with connection gains; cannot be fitted separately without conventions and observations. |
| 1 | boundary_current | 0.0 | product-boundary assumption | E19: Default zero describes unknown inputs, not measured physiological silence. |
| 1 | boundary_noise | 0.0 | product-boundary assumption | E19: Default zero; missing stochastic input distribution is not determined by omitted contact counts. |
| 1 | min_multiplier | 0.1 | unconstrained | E07: 0.1 is a hard floor, not a measured lower synaptic efficacy. Aggregate 90% depression does not identify this floor. |
| 2 | dt | 0.01 | unconstrained | E18: Numerical resolution, not physiology. Convergence is numerical evidence, not a measured 10 ms clock. |
| 2 | tau | 0.05 | unconstrained | E01, E13, E18: Global 50 ms rate relaxation cannot be identified from calcium decay or a different MBON14 membrane constant. |
| 2 | eligibility_tau | 0.5 | weakly constrained | E07, E09: Temporal order matters. No transferable measurement identifies a single 0.5 s exponential in all compartments. |
| 2 | learning_rate | 0.08 | unconstrained | E07, E08, E11: 0.08 multiplies unknown rate, eligibility and DA scales; response depression identifies at most an integrated product. |
| 2 | kc_threshold | 0.15 | weakly constrained | E01, E02, E03: Sparse nonlinear coincidence is supported; dimensionless 0.15 is uncalibrated. |
| 2 | pn_gain | 3.0 | unconstrained | E01, E02: 3 depends on rate units, artificial cue amplitude and normalization; EPSPs alone do not identify it. |
| 2 | recurrent_gain | 0.05 | unconstrained | E04, E16: 0.05 is neither an experimentally measured shared conductance nor a receptor-specific gain. |
| 2 | feedback_gain | 0.1 | unconstrained | E11, E19: 0.1 MBON-to-DAN scale unmeasured; type-level connectivity is not conductance. |
| 2 | apl_gain | 1.0 | weakly constrained | E05, E06: Inhibitory influence is supported; magnitude 1 and one scalar APL state are not. Local-response fit is non-transferable. |
| 2 | fast_gain | 1.0 | unconstrained | E01, E04: Global multiplicative scale confounded with connection gains; cannot be fitted separately without conventions and observations. |
| 2 | recovery_tau | 1800.0 | weakly constrained | E11, E12: Recovery over minutes/hour constrains timescale loosely; 1800 s and exponential law not identified; other odors matter. |
| 2 | min_multiplier | 0.1 | unconstrained | E07: 0.1 is a hard floor, not a measured lower synaptic efficacy. Aggregate 90% depression does not identify this floor. |
| 2 | normalization | all_inputs | unconstrained | E02, E06: Full proofread input vs retained role mass are numerical assumptions; neither follows from physiological normalization. |
| 3 | dt | 0.01 | unconstrained | E18: Numerical resolution, not physiology. Convergence is numerical evidence, not a measured 10 ms clock. |
| 3 | tau | 0.05 | unconstrained | E01, E13, E18: Global 50 ms rate relaxation cannot be identified from calcium decay or a different MBON14 membrane constant. |
| 3 | eligibility_tau | 0.5 | weakly constrained | E07, E09: Temporal order matters. No transferable measurement identifies a single 0.5 s exponential in all compartments. |
| 3 | body_tau | 60.0 | product-boundary assumption | E13, E14, E15: 60 s converts synthetic resource input into a state. No starvation/peptide concentration kinetics calibrate it. |
| 3 | gate_floor | 0.2 | product-boundary assumption | E14, E15, E20: 0.2 lower bound of a linear synthetic resource→PPL101 gate is not measured. |
| 3 | dopamine_gain | 1.0 | unconstrained | E07, E14: Gain 1 in acute divisor 1/(1+D) has no dose-response or unit mapping. |
| 3 | oa_gain | 1.0 | weakly constrained | E13: VPM4 suppresses MBON11 in tested preparation; magnitude 1 and fast additive inhibitory implementation not established. |
| 3 | learning_rate | 0.08 | unconstrained | E07, E08, E11: 0.08 multiplies unknown rate, eligibility and DA scales; response depression identifies at most an integrated product. |
| 3 | kc_threshold | 0.15 | weakly constrained | E01, E02, E03: Sparse nonlinear coincidence is supported; dimensionless 0.15 is uncalibrated. |
| 3 | pn_gain | 3.0 | unconstrained | E01, E02: 3 depends on rate units, artificial cue amplitude and normalization; EPSPs alone do not identify it. |
| 3 | recurrent_gain | 0.05 | unconstrained | E04, E16: 0.05 is neither an experimentally measured shared conductance nor a receptor-specific gain. |
| 3 | apl_gain | 1.0 | weakly constrained | E05, E06: Inhibitory influence is supported; magnitude 1 and one scalar APL state are not. Local-response fit is non-transferable. |
| 3 | fast_gain | 1.0 | unconstrained | E01, E04: Global multiplicative scale confounded with connection gains; cannot be fitted separately without conventions and observations. |
| 3 | min_multiplier | 0.1 | unconstrained | E07: 0.1 is a hard floor, not a measured lower synaptic efficacy. Aggregate 90% depression does not identify this floor. |
| 3 | normalization | all_inputs | unconstrained | E02, E06: Full proofread input vs retained role mass are numerical assumptions; neither follows from physiological normalization. |
| shared/operator | contact_to_strength | None | unconstrained | E02, E04, E19: Weights proportional to anatomical contacts; per-contact release probability, silent synapses, receptor density, electrotonic location unknown. |
| shared/operator | normalization_stage1 | None | unconstrained | E06: Hardcoded retained presynaptic-role denominator; no physiological calibration. |
| shared/operator | known_cholinergic_KC | None | experimentally constrained | E04: Class-level transmitter identity supported; not every target-specific net effect or numerical gain. |
| shared/operator | APL_GABA_inhibition | None | experimentally constrained | E05, E06: Sign of tested APL→KC inhibitory effect supported; scalar implementation not validated. |
| shared/operator | MBON11_GABA | None | experimentally constrained | E14: Known GABA identity; effective downstream target sign/gain still needs target-specific physiology. |
| shared/operator | MBON07_to_PAM11_positive_sign | None | weakly constrained | E10, E16: NMDA requirement supports hypothesis; direct net excitation not established by source. Frozen code comment is stronger than evidence; left untouched and qualified here. |
| shared/operator | MBON07_other_outputs_zero | None | unconstrained | E10: Computational omission, not proof of no transmission. Stage3 zeros even PAM-related output. |
| shared/operator | DAN_fast_effect_zero | None | unconstrained | E08, E19: Convenience separation of fast and modulatory effects, not measured absence of acute transmission. |
| shared/operator | OA_other_targets_zero | None | unconstrained | E13: Unknown receptor effects omitted, not physiologically absent. |
| shared/operator | DA_locality | None | weakly constrained | E07, E11, E19: Compartmental modulation supported; DAN→KC versus DAN→MBON contact-normalized rate does not identify release/receptor exposure. |
| shared/operator | KC_MBON_APL_gain1 | None | unconstrained | E04, E05: Hardcoded fixed gain lacks synaptic current normalization. |
| shared/operator | MBON11_gain20x_conflict | None | unconstrained | E13, E14: Stage1 recurrent 0.05 vs Stage3 source 1 on many shared outputs; same anatomy does not reconcile strengths. |
| shared/operator | MBON18_PN_to_LH_gain1 | None | unconstrained | E13: Anatomical pathways supported, fixed scale and effective target physiology unknown. |
| shared/operator | clipped_rate_0_1 | None | unconstrained | E07, E11: No Hz/current/calcium observation mapping; a zero lower bound cannot itself express below-baseline fluorescence. |
| shared/operator | point_neurons | None | weakly constrained | E05, E18: Local APL data challenge one globally uniform state; other cell classes require separate checks. |
| shared/operator | plasticity_LTD_only | None | weakly constrained | E07, E08, E09: Narrow pairing protocols support depression; unpaired DAN and reverse timing can have other effects. |
| shared/operator | postsynaptic_multiplier | None | weakly constrained | E12: Receptor evidence supports a possible locus in alpha-prime3, not a complete per-contact rule for all stages. |
| shared/operator | acute_vs_persistent_rule | None | unconstrained | E07, E14: Stage3 acute divisor plus persistent LTD cannot be derived by merging behavior studies and conditioning endpoints. |
| shared/operator | initial_efficacy1 | None | unconstrained | E07: Unit efficacy and zero eligibility at t0 are initialization conventions, not naive-synapse measurements. |
| shared/operator | resource_linear_gate | None | product-boundary assumption | E14, E15, E20: PPL101 desired rate multiplied by 0.2+0.8r; r is not a measured nutrient/hormone state. Direction alone does not identify shape. |
| shared/operator | synthetic_cue_teacher_OA_currents | None | product-boundary assumption | E02, E07, E13: Arbitrary PN cues and dimensionless teacher/OA currents are not odor concentration, spikes or transmitter dose. |
| shared/operator | NO_peptide_receptor_omission | None | unconstrained | E04, E15, E17: Chemical edges do not establish NO/sNPF/dNPF kinetics or receptor graph. Zero omitted action is a model choice. |
| shared/operator | no_transmission_delays | None | unconstrained | E07, E09: Synchronous 10 ms updates do not measure propagation or receptor kinetics. |
| shared/operator | pooling_and_readout | None | product-boundary assumption | E11, E13: Averaging MBON groups and cue-response metrics is an assay choice, not a behavioral motor output. |
