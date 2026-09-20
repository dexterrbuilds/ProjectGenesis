# Representation, observation and precursor assessment

## Evidence categories

**BIOLOGICAL FACT / observations:** the independent whole-cell experiments provide graded somatic T4/T5 voltages in response to localized flashes and motion. Their measurement/preparation provenance is in SOURCE_DATA_AUDIT.md. ON/OFF pathway names do not imply an identically zero response to every nonpreferred contrast in every assay. The anatomy supplies neuron identities and column assignments, not a complete physiological input operator.

**EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION:** the completed comparison supports only the narrow statement that some flash-trained, compact signed space/time response models predict portions of these T5 voltage responses better than a zero-response reference. It does not validate their parameters as membrane/synaptic constants or establish a general T4/T5 boundary. No candidate reaches this study's general acceptance scope.

**HYPOTHESIS:** a richer compact nonlinear input/output model may account for broad stimulus families; an explicit precursor model may ultimately improve causal explanation. Neither is established as necessary by the present results. Published compact excitatory/inhibitory models are relevant counterexamples to the assertion that failures of these particular basis models require explicit precursor neurons.

**ENGINEERING ASSUMPTION:** Gaussian spatial bases, fixed filter grids, common delay grid, ridge penalty, one-standard-error rule, mean-trace loss, 5 ms baseline discretization, and phenomenological divisive compression. They were registered before fitting and are not identified biological conductances. The baseline minimum-norm coefficient zero is an algorithmic convention for an unidentifiable gain; its true physiological value is unknown.

**GENESIS PRODUCT MAPPING:** none.

## Candidate accounting

| Candidate | Dynamic variables / coefficients | Tested role | Limitation |
|---|---|---|---|
| B0 frozen boundary algebra | Two delayed physical contrast samples; one nonnegative voltage gain | Structural baseline | Static flashes cannot identify gain; opposite-polarity/signed voltage and generic stationary responses are excluded by construction. Numerical zero-gain motion scores are not calibrated neural predictions. |
| B1s | Seven spatial basis outputs × one exponential; seven signed coefficients | Small compact RF/flicker-responsive approximation | Fitted only to T5 OFF flashes. Its spatial basis is not an anatomical compartment or seven neurons. |
| B1t | Seven basis outputs × two exponentials; 14 signed coefficients | Multiple temporal components | Filter constants are a registered grid, not identified cell-specific physiology. |
| B1d | B1t plus a selected divisive-compression coefficient | Compact nonlinearity | Denominator is phenomenological; not identified receptor/conductance or gain control circuit. |
| Separate ON/OFF model B2 | Not instantiated | Would require independent polarity calibration and compatible held-out data | T4 polarity descriptions are not T5 parameter identification. No cross-type constant transfer. |
| Explicit Mi/Tm/CT1 | Not instantiated | Causal precursor necessity question | No paired controlled comparison establishes necessity. |

## Observation-model boundaries

The loss is in baseline-subtracted **mV**. It is not firing rate, synaptic release or ΔF/F. Whole-cell current injection, soma recording and authors' trial filtering constrain interpretation. Voltage-to-calcium rectification, indicator kinetics, dendrite-to-soma filtering, calcium saturation and transmitter release remain unknown. No free observation nonlinearity is fit to make voltage match a different assay.

The physiological studies' PD/ND metrics also differ in denominator and observation type; they are not pooled as one universal DSI. The compact dataset's local axis is conditioned on author localization, not a screen transform learned here. Predicted errors are computed on the supplied trace means, not on independently held-out raw trials. Noise ceilings and trial-level uncertainty cannot be inferred from the compact files.

## Identifiability

See IDENTIFIABILITY.json and TRAINING_PROFILE.json for every recording's grid profile, selected coefficients, fold stability, effective degrees of freedom and design spectrum. A predictive coefficient can be regularized without being physiologically identified. Delay and filter shape can trade off; spatial bases overlap; flash-only training leaves motion-specific nonlinearities poorly tested until family holdout. A low inner-fold error does not license a unique membrane time constant, causal sign map or precursor architecture.

No fly bootstrap or time-sample confidence interval is presented. The four duration folds provide a model-selection heuristic and sensitivity profile, not four independent animals. Selection was completed before scoring apparent motion/moving bars/gratings. Strong held-out failures remain unchanged; candidates are not re-ranked on those outcomes.

## Do explicit precursors become necessary?

**Not established.** The flash-selected compact family fails important held-out stimulus families. That demonstrates limited generalization of the registered candidates. It does not exclude all compact nonlinear/state-dependent boundaries, nor demonstrate that an explicit Mi/Tm/CT1 architecture captures the missing computation under equivalent held-out tests.

Independent anatomy/physiology nominates Mi1/Tm3 and Mi4/Mi9/CT1-related inputs for T4, and Tm1/Tm2/Tm4/Tm9/CT1-related inputs for T5; their exact minimal causal set depends on the assay, cell subtype, synaptic location, receptor signs and preparation. Contact counts alone do not identify those operators. This study neither extracts that network nor selects a minimum neuron count.

A necessity claim would require a preregistered compact-versus-precursor comparison on the same independent stimulus/observation data, with comparable parameter accounting, held-out flies/families and precursor-specific perturbation evidence. Poor fit by an intentionally bounded candidate set is insufficient. No large precursor network is recommended as an automatic next step.
