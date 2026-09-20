# Stage-5 readiness assessment — evidence gaps only

**Question:** Is there sufficient evidence to design a future study of whether the frozen Stage-1 learned signal causally biases downstream biological action-related dynamics?

This assessment identifies candidate evidence and missing links. It chooses no extraction, model, neural equations, stimulus schedule, thresholds, optimization objective or experiment protocol. Stage 5 is not started or authorized by v0.2.

## Current anchor

Stage 1 remains PASS only for persistent dopamine-dependent KC→MBON plasticity in its declared connectome-constrained model. Its appetitive compartment is α1 / MBON07. The negative change in its cue-evoked model response is not itself a preference, movement command or calibrated biological firing change. Its MBON11 aversive counterpart was inconclusive. Consequently an MBON11 pathway is not an equally validated source of learned appetitive action bias.

## Candidate downstream evidence

The strongest targeted literature lead is **MBON-α1 → UpWind Neuron candidates**, including SMP353/SMP354. Aso et al. link α1 memory to wind-oriented locomotion, report direct hemibrain contacts into a subset of those cells, and measure inhibitory α1-evoked responses in **4/17 sampled UpWiNs**. α3 stimulation excites **3/11**. The recordings sample a broad driver population; they do not identify every root's receptor or sign. Imaging, electrical recording and behavior have different observation/preparation scopes. UpWiN recall responses and blocking results motivate a possible learned-response route, not a ready-made Genesis operator. The study uses adult females and figure-specific driver combinations; broad population labeling and possible β1 contributions limit α1-only attribution. [Primary study, Figures 1, 3–5 and methods](https://elifesciences.org/articles/85756)

General MBON behavior-linked studies motivate convergence rather than an automatic command-neuron interpretation. They do not establish that the particular frozen α1 model controls action. [Aso et al. 2014](https://doi.org/10.7554/eLife.04580) Trans-Tango mapping provides downstream anatomical candidates, but tracing is not target-specific receptor evidence or measured transfer dynamics. [Scaplen et al. 2021](https://doi.org/10.7554/eLife.63379)

### Existing pinned anatomy leads — no new extraction

| Candidate | Already frozen evidence | What it does not establish |
|---|---|---|
| MBON07 → SMP353 | Boundary-study `INTEGRATION.json` records MBON07 root `720575940617302365` → SMP353 root `720575940608236978`, **11 contacts**, as one segment of a separately audited anatomical path. | This is not an audited recording/driver/hemibrain→FAFB functional crosswalk, a receptor map, or a demonstrated motor path. |
| MBON07 → LH-associated convergence candidates | Frozen `S1_MBON_app_L0_output` includes LHAD1b5 roots `720575940620067823` (59 omitted-output contacts), `720575940613953703` (55), and `720575940621943187` (55); LHAD1k1 `720575940622358604` (30). These counts are aggregated for the Stage-1 appetitive source population, not necessarily one presynaptic root. | Neither their name nor their contact mass proves action selection; downstream function and source-specific row attribution remain to be audited. |
| MBON07 ↔ reward/recurrent pathways | Stage 1 and the architecture study already show feedback/other anatomical routes, including PAM11-related circuitry. | Reward feedback or second-order learning circuitry is not a motor endpoint. Shortest paths are not physiological propagation. |
| MBON11/other MBON convergence | Anatomically relevant as context, with shared state-rule conflicts already recorded. | Stage-1 aversive inconclusiveness and Stage-3 tiny modeled effects do not validate learned appetitive action selection through this route. |

Evidence source: the unchanged [architecture-study integration artifact](../fly-boundary-study/INTEGRATION.json). Numeric rows are referenced, not copied into a new canonical anatomy owner. No particular descending neuron is admitted as a verified Stage-1 action endpoint. SMP354 has a literature lead; its required FAFB root crosswalk has not been established in this synthesis.

## Required evidence before prospective design

| Requirement | Present basis | Targeted missing evidence |
|---|---|---|
| Anatomical pathway | Pinned α1 output and named downstream candidates | Complete source-root→target-root mapping, direction, neuropil/local sites, contacts, recurrence and boundary retention; audited hemibrain/FAFB and driver identities; actual paths onward to independently action-related populations |
| Physiology and sign | Preparation-specific inhibitory responses exist for a subset of α1 downstream targets | Which candidate roots/compartments correspond to those measured cells; receptor/sign evidence and confidence per target; electrical transfer magnitude, delay and state dependence. Glutamate identity alone cannot establish excitation or inhibition. No blanket GluCl assignment. |
| Learned-signal transfer | Stage-1 plastic state causally changes its own MBON response | Compatible biological before/after α1 and downstream recordings; independent constraints on conversion from model activity to recorded electrical/fluorescence quantity; no tuning to maximize action bias |
| Behavioral evidence | Published conditioning, heading, turning and locomotion assays | Accessible trial/fly identities, genotype/preparation and state controls, matched cue/learning conditions, neural/behavioral timing and uncertainty; independently held-out relationships rather than a software threshold on an arbitrary rate |
| Observation mapping | Distinct voltage/calcium/behavior source measurements exist | Valid compartment, baseline and indicator mapping for each comparison. A lack of visible calcium inhibition cannot be equated with no electrical inhibition. Neural units must not silently become movement probability. |
| Context and embodiment | Wind-oriented behavior is a concrete biological assay | Measured wind/directional/contextual and baseline inputs relevant to the route. Disinhibition needs supported background/excitatory context; arbitrary tonic current cannot be added to manufacture the effect. |
| Causal intervention | Literature provides manipulation leads; Stage 1 provides local learning controls | Evidence that altering the proposed route changes the appropriate downstream quantity while preserving upstream learning and unrelated sensory responsiveness; matched interventions and timing/context specificity. These are evidentiary requirements, not a selected Stage-5 battery. |
| Unified state ownership | Canonical rows and conflicts are identified | One defensible state/update rule for every included shared row. Preserve 4,622 KC→MBON07 and 1,053 KC→MBON11 identities; no parallel independent owners or silent averaging of incompatible rules. |

Useful published measurement leads are Figure 4 whole-cell and population-imaging source workbooks, Figure 5 conditioning response data, and Figure 1/behavioral trajectory data from the primary UpWiN study. Their accessibility is not equivalent to a clean validated dataset. Cell/fly identities, exclusions, waveform definitions, independent replication and any duplicate-recording/mean discrepancies must be audited before calibration or prospective acceptance criteria. This task did not download/process them or fit any coefficient. No numerical threshold is selected here.

## Neural action bias versus software interpretation

A future neural-action-bias claim would require a measured downstream variable whose change is carried through the biological connectivity and supported transmission mechanism, with a preparation-compatible independently established relationship to a narrow action-related quantity. The cue must carry the same physical input before and after learning. Intervention on the route must affect the downstream change without erasing the upstream learned signal or all sensory activity. Observation decoding must be fixed independently of the desired outcome and must not store cue preference or choose an action on behalf of the circuit.

A signed MBON score, custom weighted sum, threshold crossing named APPROACH, maximum across separately modeled stage scores, or an LLM choosing from that score cannot establish this claim. A genuine downstream neural bias would still not establish general action selection, voluntary choice, persistence, avoidance, consciousness or Genesis behavior.

## Stage-1 assumptions that cannot silently transfer

The 50 ms scalar time constant, contact normalization, shared gains/signs, point APL, synthetic PN/DAN currents, 500 ms eligibility, LTD rate/floor, compartment/contact-based dopamine exposure and response readout were scoped computational assumptions. Their Stage-1 success does not calibrate those quantities for a downstream target. In particular, Stage-1 MBON07→PAM11 transmission assumptions and other-output zero boundaries are not physiological evidence for inhibition, excitation or absence of downstream signaling. Contact counts are not conductance; a route previously omitted or assigned no operator has unknown physiology rather than zero physiology.

Stage 3 did not validate persistence; its learned-value×resource interaction near 10^-6% is not useful action-integration evidence. The boundary study's sensitivity to normalization and the unresolved shared KC→MBON07/11 update rules remain constraints. Neither the empirical visual interface nor the APL calibration fills these gaps.

## Decision

There is a specific independently motivated α1-to-downstream candidate and a frozen associative-model anchor. That is enough to justify targeted evidence acquisition, but the root crosswalk, physiological mapping, background inputs and action observation are not sufficiently established to declare readiness now. The next authorization should address those missing links before a protocol is designed. No Stage-5 experiment is specified or begun.

**PARTIAL READINESS — TARGETED EVIDENCE REQUIRED**
