# Project Genesis — proposed Brain v1 research specification

**Status:** research and architecture proposal, not an implemented or biologically validated fly model.  
**Research date:** 17 September 2026.  
**Scope:** adult female Drosophila, FAFB/FlyWire materialization 783. The existing C. elegans implementation and organism remain unchanged.

## 1. Recommendation

**Pursue option B conditionally: a bilateral mushroom-body-centered subnetwork, extended with identified sensory, motivational, sleep/arousal and descending circuits. Keep C. elegans as the working reference. Do not migrate to the full fly brain merely to increase neuron count.**

The principal scientific benefit is a plausible place for experience to change neural responses: compartment-specific associative plasticity. The proposed fly system could also support familiarity, state-dependent expression of learned preferences and competing behavioral tendencies. It would not biologically understand money, language, companies or the internet.

A defensible first extraction starts with **6,285 annotated neurons** in a deliberately inclusive associative/input seed. Budget **approximately 8,000–12,000 neurons** after adding state and output circuits and necessary recurrent partners. This is a proposed search range, **not a demonstrated minimum or completed subnetwork census**. The hypothesis that this range is sufficient must survive boundary and ablation tests.

The weakest parts are generalized exploration/exploitation, digital scarcity as hunger, complete sleep dynamics without a body, and abstract action selection. Those must remain explicitly identified modeling/product interpretations. If they require software to dictate the answer while the network merely echoes it, the proposed migration fails its purpose.

### Comparison

| | A. Existing C. elegans | B. Selected adult fly circuitry | C. Full adult fly brain |
|---|---|---|---|
| Anatomical scope | Existing 302 named neurons; 3,709 chemical and 1,091 gap-junction graph edges | Real, individually identified neurons and induced chemical connections; explicit boundaries | Published 139,255 neurons, roughly 50 million chemical synapses; approximately 15.1 million weighted neuron-pair edges |
| Current evidence in Genesis | Working deterministic causal loop and persistent neural state | Proposed; not implemented or validated | Proposed; not implemented or validated |
| Main advantage | Small, inspectable, established baseline | Identified associative plasticity and state-dependent circuits with manageable experimental scope | Retains more brain-internal recurrent pathways and sensory context |
| Main limitation | Current implementation has no modeled synaptic learning and five output labels | Removing inputs/feedback can distort dynamics; needs explicit physiological assumptions | More unknown parameters and greater validation burden; still lacks the complete body and its feedback |
| Best role | Preserve as regression/reference brain | Preferred research direction if staged tests succeed | Offline boundary/reference experiments; consider continuous use only if needed |

The existing implementation's limitations are not claims that real C. elegans cannot learn or regulate internal state. Full-brain counts come from the [wiring publication](https://www.nature.com/articles/s41586-024-07558-y) and [cell-type atlas](https://www.nature.com/articles/s41586-024-07686-5).

## 2. Data, availability and licensing

### What “current FlyWire” means here

Pin **FAFB connectivity 783** separately from **annotation release v3.1.0**. Annotation updates change cell-type names and cross-dataset matches without being a new acquisition of this brain. The [official annotation repository](https://github.com/flyconnectome/flywire_annotations) includes synonyms, hemibrain labels, transmitter predictions and sex-related annotations. Use these fields, not name matching alone, to associate a functional study with a FlyWire root.

FAFB is one adult female **brain**, not its whole nervous system. Peripheral physiology, much of the ventral nerve cord (VNC), muscles, endocrine organs and natural sensory feedback are outside this model. Newer whole-CNS datasets are also available in the [current Codex catalogue](https://codex.flywire.ai/); that does not justify silently importing neurons from another animal or sex into FAFB.

The 2024 atlas reported 8,453 types and approximately one-third of hemibrain types could not be reliably reidentified. A matching type label is therefore evidence to inspect, not a guarantee of identical physiology. Strong connections are generally more reproducible across brains, but weak connections are not necessarily unimportant. [Schlegel et al., 2024](https://www.nature.com/articles/s41586-024-07686-5)

### Licensing findings

- The [FlyWire connectivity deposit, version 783.0](https://zenodo.org/records/10676866), explicitly declares **CC BY 4.0**, confirmed in its [machine-readable record](https://zenodo.org/api/records/10676866). Preserve attribution, version and transformation notices with future derived connectivity artifacts.
- This does **not** automatically establish the license of every annotation supplement, EM image, skeleton or software repository. I did not locate an unambiguous standalone license for the current v3.1.0 annotation repository during this review. Resolve that before redistributing its complete table or a production derivative; retain provenance now.
- The [published full-brain model's code](https://github.com/philshiu/Drosophila_brain_model) uses MIT licensing. Its code license is separate from the data license. No model code is incorporated in this task.

### What was actually counted

I downloaded the public [v3.1.0 annotation TSV](https://github.com/flyconnectome/flywire_annotations/blob/v3.1.0/supplemental_files/Supplemental_file1_neuron_annotations.tsv) and counted rows, without modifying Genesis's connectome. It contains **139,248 unique root IDs**, seven fewer than the published 139,255. The cause of that difference was not established. Reconcile the missing/extra ID sets against the pinned connectivity inventory before making a production manifest; do not silently drop unmatched neurons.

All counts below are bilateral, exact counts in that table, and **annotation counts rather than claims of experimentally verified function**.

| Selection | Count | Interpretation / reliability limit |
|---|---:|---|
| `cell_class == Kenyon_Cell` | 5,177 | Includes α/β, α′/β′ and γ subclasses; retain individual neurons |
| `cell_class == MBON` | 96 | Includes some compound/ambiguous labels; not 96 equally characterized neurons |
| `cell_type` starts with `PAM` | 307 | Compartment and functional assignment still need review |
| `cell_type` starts with `PPL1` | 16 | PPL101–108; excludes dopamine neurons named under other classes |
| `APL`, `DPM` | 2 each | Identified broad MB neurons; point-neuron approximations require care |
| `cell_class == ALPN` | 685 | Broad antennal-lobe projection-neuron seed; not all are interchangeable odor inputs |
| `cell_class == ALLN` | 429 | Available local antennal-lobe circuitry, optional if starting downstream at PNs |
| `cell_class == LHLN` | 514 | Available local lateral-horn population, not a requirement to include every cell |
| `MBON11`, `MBON16`, `MBON17`, `MBON18` | 2 each | Useful identified output classes |
| `PPL101`, `PPL104` | 2 each | Useful identified dopamine classes |
| `ER5`, `ER3d`, `ExR1`, `ExR3`, `hDeltaK` | 21, 47, 4, 2, 31 | Candidate sleep/state circuit components, with functional crosswalks |
| `FB6A`, `FB6H`, `FB7B` | 4, 2, 2 | Named state-circuit candidates; not all FB6/FB7 neurons have the same role |
| `OA-VPM3`, `OA-VPM4` | 2 each | Distinct octopamine populations; not one global arousal signal |
| `LC4`, `LPLC2`, `DNp01` | 104, 210, 2 | Looming-related inputs and giant-fiber output candidates |
| `EPG` plus `EPGt`; `PEN_a`, `PEN_b`; `PEG`; `Delta7` | 51; 20, 22; 20; 42 | Optional spatial-navigation circuitry |
| `FC2A/B/C`; `PFL1/2/3` | 85; 50 | Optional spatial goal/steering circuitry, not abstract planning |

The **6,285-neuron seed** is the union of the first six rows: 5,177 + 96 + 307 + 16 + 2 + 2 + 685. It is deliberately conservative about retaining the MB, not an assertion that all these neurons are necessary.

Reproducibility: annotation file SHA-256 `9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be`. Count exact `cell_class` or `cell_type` values as stated; do not sum overlapping rows. Root IDs must remain **strings**, since their integer values exceed JavaScript's safe integer range.

### Connectivity is not yet a functional model

The [783 deposit](https://zenodo.org/records/10676866) provides a roughly 852 MB proofread connection table, including neuropil and synapse counts, and a much larger synapse-location table. A connection-table row can be a pre/post/neuropil group, not a unique neuron pair. Raw synapse detections also include cells outside the proofread brain inventory. Keep these denominators distinct.

**The edge table was not extracted in this research task. No exact subnetwork edge or synapse count is claimed.** The annotation census alone cannot provide those counts.

Predicted transmitter labels do not specify receptor distribution, synaptic conductance, all co-transmission or peptide signaling. Electrical connections are not a complete part of this chemical connectome. Assigning every glutamatergic connection one sign, or every dopamine connection “reward,” would be unjustified. [Network statistics and transmitter methods](https://www.nature.com/articles/s41586-024-07968-y)

## 3. Proposed circuits and the three layers of interpretation

**BIOLOGICAL FACT** below means experimentally supported circuit evidence or observed anatomy. **COMPUTATIONAL MODEL** is a proposed approximation, not a claim that the parameters were measured in FAFB. **GENESIS MAPPING** is a product choice and never a claim about a fly's conceptual understanding.

### 3.1 Associative value, preference and aversion — required

**BIOLOGICAL FACT.** Mushroom-body Kenyon cells provide distributed sensory representations to compartment-specific MBONs; dopamine modulates plasticity in these compartments. MBON output patterns influence learned approach/avoidance. The circuit includes recurrent and inter-compartment pathways, including MBON–DAN feedback. [Adult MB anatomy](https://elifesciences.org/articles/62576), [MBON valence experiments](https://elifesciences.org/articles/4580)

**COMPUTATIONAL MODEL.** Retain bilateral KCs, MBONs, PAM/PPL1 DANs, APL and DPM with actual PN→KC, KC→MBON and recurrent connections. Use compartment-local dopamine and plasticity, rather than a single scalar value unit. Keep uncertain MBON classes explicitly marked. Include verified additional MB input neurons during boundary closure.

**GENESIS MAPPING.** A stable cue identifies an opportunity, task context or outcome-associated situation. Experience changes the cue's subsequent neural valuation. “Preference for this context” is defensible as an analogy; “the fly understands this business” is not.

### 3.2 Reward and punishment — required, compartment-specific

**BIOLOGICAL FACT.** Dopamine populations have distinct learning functions. Their effects depend on timing and compartment; PPL1/PAM are not a universal punishment/reward binary. Recent work directly demonstrates interactions between short- and long-term reinforcement pathways. [Cell-specific learning rules](https://pubmed.ncbi.nlm.nih.gov/27441388/), [2024 reinforcement study](https://www.nature.com/articles/s41586-024-07819-w)

**COMPUTATIONAL MODEL.** Start with separately validated appetitive and aversive conditioning pathways. Model phasic dopamine and tonic state modulation separately. Use natural-stimulus input pathways where crosswalks are secure; otherwise label direct DAN current as a boundary stimulation model, comparable to experimental perturbation, not simulated taste transduction.

**GENESIS MAPPING.** Verified resource acquisition can supply an appetitive teaching event; a verified loss or harmful outcome an aversive event. An opportunity is a predictive cue, not reward already received. The LLM cannot declare its own success, edit teaching signals or label its favored plan rewarding.

### 3.3 Novelty, familiarity and exploration/exploitation — partly supported

**BIOLOGICAL FACT.** α′3 MBON responses distinguish novel from repeated odors through dopamine-dependent plasticity. The documented effect is stimulus-specific familiarity, not an abstract curiosity algorithm. Candidate class crosswalk: MBON16/17 and PPL104, to be confirmed against the pinned root manifest. [Hattori et al., 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806120/), [adult MBON crosswalk table](https://pmc.ncbi.nlm.nih.gov/articles/PMC9984194/)

**COMPUTATIONAL MODEL.** Preserve α′3 circuitry and its local habituation/recovery dynamics. Read familiarity alongside learned cue value, threat, arousal and commitment. Test competition between unfamiliar and familiar rewarded cues; do not insert an external epsilon-greedy exploration policy and call it biology.

**GENESIS MAPPING.** Elevated unfamiliar-cue response may permit examining a new context. A familiar positively valued context may favor continuing established work. The tradeoff is a product-level readout of several neural signals; there is no verified “explore the internet” circuit. Semantic novelty is not established by an odor-like cue code.

### 3.4 Scarcity, resource seeking and persistence — required with a body boundary

**BIOLOGICAL FACT.** Hunger-dependent dNPF signaling changes expression of appetitive memory through dopamine pathways. PPL101 participates in motivational gating as well as aversive reinforcement. MBON11 (γ1pedc→α/β), MBON18 (α2sc) and OA-VPM4 participate in persistence versus withdrawal from food-odor pursuit. Hungry flies can persist despite unsuccessful pursuit; failure does not simply mean disengagement. [Krashes et al., 2009](https://doi.org/10.1016/j.cell.2009.08.035), [PPL101 hunger/reinforcement study](https://pubmed.ncbi.nlm.nih.gov/38795709/), [Sayin et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6839618/)

**COMPUTATIONAL MODEL.** Use a slow resource-state variable to modulate the identified motivational pathway; separately model ongoing cue contact, phasic reinforcement and interruption signals. Retain PPL101/MBON11/MBON18 and OA-VPM4 partners. dNPF source/receptor assignments require literature crosswalks: peptide effects cannot be inferred from chemical edge counts or an `NPF` name search alone.

**GENESIS MAPPING.** Operational resource runway is an external analogue of resource availability. It is not glucose, starvation or suffering. Ongoing productive task contact can sustain engagement; acquisition, danger and competing demands can interrupt it. Insolvency safeguards remain software safety constraints, not artificial pain or punishment escalation.

### 3.5 Learned/innate convergence and action selection — required, modest claims

**BIOLOGICAL FACT.** PD2a1/PD2b1 lateral-horn neurons integrate olfactory and learned-pathway input, including MBONα2sc. Descending commands operate through interacting populations. Brain walk-OFF populations can inhibit walking-related outputs; motor stopping is distinct from sleep. [Dolan et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6226615/), [descending networks](https://www.nature.com/articles/s41586-024-07523-9), [context-specific halting](https://www.nature.com/articles/s41586-024-07854-7)

**COMPUTATIONAL MODEL.** Include anatomically verified MBON/LH convergence and selected downstream descending/halting pathways. PD2a1/b1, FG/BB and walking-output aliases require paper-to-root mapping; these are named extraction targets, not a completed manifest. Preserve competition and abstention. Do not invent missing inhibitory edges to manufacture a winner-take-all circuit.

**GENESIS MAPPING.** Neural outputs can select engagement, interruption or withholding within a predefined set of digital affordances. A descending locomotion signal is a proxy for engagement, not “write code.” VNC muscle-control cells such as BRK are outside the FAFB brain and are not silently appended.

### 3.6 Threat and avoidance — required as a bounded sensory channel

**BIOLOGICAL FACT.** LC4 and LPLC2 provide looming-related signals to giant-fiber/DNp01 escape circuitry. The biological pathway operates in a visual and motor body. [Ache et al., 2019](https://doi.org/10.1016/j.cub.2019.01.079)

**COMPUTATIONAL MODEL.** Include 104 LC4, 210 LPLC2 and two DNp01 candidates plus audited intermediate/feedback partners. Starting with feature currents at LC4/LPLC2 omits upstream visual computation: it models an escape-related response to imposed evidence, not detection of looming objects from pixels. A rate model supports escape propensity, not millisecond-accurate takeoff or the complete giant-fiber electrical/motor pathway.

**GENESIS MAPPING.** A verified urgent hazard can be translated to increasing threat intensity/urgency. Cybersecurity risk is not a predator; this is explicitly an analogy. Hard safety blocks apply regardless of neural response, and cannot be counted as successful biological avoidance.

### 3.7 Arousal — required, with sex and receptor qualifications

**BIOLOGICAL FACT.** OA-VPM3 links MB/CX circuitry to wake regulation, but a 2026 study found stronger effects in males and weaker, more variable effects in females. OA-VPM4 has a different behavioral role. Neither finding supports a universal octopamine “motivation level.” [Reyes et al., 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13122709/)

**COMPUTATIONAL MODEL.** Include the two OA-VPM3 neurons as qualified candidates, alongside identified dopamine/state circuits. Fit a range of receptor-dependent gain effects and test female-compatible response ranges. Record uncertainty rather than importing a male effect size into the female connectome.

**GENESIS MAPPING.** Arousal may affect responsiveness and permitted activity cadence. It does not represent consciousness, excitement about profits or an LLM-assigned emotion.

### 3.8 Sleep, rest, wake and circadian phase — required, highest modeling risk

**BIOLOGICAL FACT.** Identified CX state pathways include ER5, ExR1/helicon, ExR3 and hDeltaK, connected with recurrent dorsal fan-shaped-body networks. FB6A and dopamine classes FB6H/FB7B are candidate components. Much upstream/downstream function remains unresolved. [Hulse et al., 2021](https://elifesciences.org/articles/66039)

Older dFB conclusions require caution: common 23E10 drivers can include VNC cells, and refined work finds heterogeneous transmitters, including cholinergic/glutamatergic populations, rather than a uniform GABAergic sleep switch. [Jones et al., 2025](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003014)

A FlyWire-specific clock study identifies approximately 240 clock neurons, extending older estimates. DPM neurons also link MB inhibition, sleep and memory consolidation. [Reinhard et al., 2024](https://doi.org/10.1038/s41467-024-54694-0), [Haynes et al., 2015](https://elifesciences.org/articles/03868)

**COMPUTATIONAL MODEL.** Extract the named CX populations and necessary recurrent FB/ring partners; add clock neurons using the clock study's supplementary identities, including s-LNv/l-LNv, LNd and DN groups. Couple their rates to phenomenological homeostatic and circadian variables. Exact peptide/receptor and dFB crosswalks remain admission requirements. For example, older `FB6C_b` is not a literal current `cell_type`; substituting all `FB6C` would be unjustified.

**GENESIS MAPPING.** Low engagement alone is “idle,” not sleep. Call a state **modeled sleep** only after demonstrating reduced responsiveness, reversibility, raised arousal threshold and homeostatic rebound. Rest can restrict tool use while state dynamics continue. Wall-clock downtime and an operator pause are not biological sleep.

### 3.9 Spatial goal persistence — optional, exclude initially without navigation

**BIOLOGICAL FACT.** EPG heading-related activity and FC2/PFL pathways support transformations from allocentric goals to steering commands. This is evidence about navigation, not a general executive or business-planning center. [Goal-to-steering experiments](https://www.nature.com/articles/s41586-023-07006-3)

**COMPUTATIONAL MODEL.** Add EPG/EPGt, PEN, PEG, Delta7, FC2 and PFL populations only if the digital body has an explicit spatial environment with measured heading/motion feedback. Some cells may separately be needed as boundary partners for state circuits; that does not grant them an abstract planning interpretation.

**GENESIS MAPPING.** Do not put “business A” at 90 degrees and “business B” at 180 degrees and call the resulting ring activity biologically grounded abstract choice. Optional virtual navigation can be a scientific test environment, not a requirement for Genesis's public life.

### 3.10 Social/environmental responses — defer dedicated social drives

**BIOLOGICAL FACT.** FAFB is female; sex-specific cell identity and cross-dataset differences require explicit treatment. Male courtship results are not automatically applicable to this brain. [Annotation release and dimorphism fields](https://github.com/flyconnectome/flywire_annotations)

**COMPUTATIONAL MODEL.** No dedicated social-emotion subsystem in the minimum proposal. Treat externally sourced cues through the same sensory, familiarity and learned-value pathways until a particular adult female social circuit and its receptors are justified.

**GENESIS MAPPING.** A human message can be a new or previously reinforced cue. Its sender is not a fly pheromone, and neither trust nor loneliness is established by this model. Communication remains a constrained digital action, not proof of biological sociability.

## 4. Selecting a subnetwork without manufacturing its behavior

The smallest *demonstrated* circuit is not knowable from the literature and label table alone. Use this staged selection:

1. **Associative seed:** the 6,285 neurons above. Preserve bilateral identities and real recurrence. Candidate modality-specific input neurons missing from that seed must be audited before interpreting otherwise silent KCs.
2. **State/output seed:** named persistence, threat, sleep/arousal, clock, LH and descending classes. Resolve root IDs against functional figures/supplements, morphology and synonyms. Record ambiguous assignments, including functional driver lines spanning multiple types.
3. **Boundary closure:** measure retained versus omitted incoming/outgoing synapse mass per neuron, class, neuropil and transmitter. Add recurrent partners and known low-count modulatory paths based on those measurements and literature. One-hop expansion alone is not a scientific criterion; two hops can approach the whole brain.
4. **Compare nested extractions:** seed, expanded circuit, and larger-context reference. Keep the same parameters and stimulus protocols. Verify learned preferences, sleep transitions and intervention effects do not depend on an arbitrary cut.
5. **Minimize only after validation:** remove groups and repeat the battery. A smaller model that reproduces more of the prespecified evidence is preferable to a large uncalibrated one.

**Planning envelope, not extraction results:** 8–12k neurons; provision for **0.2–1.5 million unique directed neuron-pair edges**. This wide edge range is an engineering allowance, not an empirical estimate from measured subnetwork connectivity. Exact anatomical synapse counts remain unknown until extraction. Preserve separate compartment/neuropil groups where collapsing them would destroy the modeled mechanism.

Removing the remaining brain can remove tonic drive, inhibition, shared input, sensory adaptation and state-dependent feedback. A network may then become silent or unstable for reasons unrelated to the animal. Boundary current/noise models are permissible **computational approximations**, but must be recorded and tested. Do not add a hidden “explore” current to repair an undesirable Genesis choice.

Acceptance thresholds for retained mass should be declared in advance, but no universal percentage proves completeness. A low-mass peptide pathway may matter more than many fast synapses. Do not discard every connection below five synapses by default. Compare thresholds 1/3/5/10 and degree/strength-matched controls, documenting changes. Keep baseline weight scaling fixed during ablations; automatic renormalization could hide the lesion.

## 5. Simulation and neural learning specification

### Dynamics

**Proposed implementation approach:** sparse continuous-rate dynamics, one identified neuron per primary unit, with explicit local compartments where required. Use native/compiled numeric arrays behind the adapter; avoid millions of JavaScript edge objects in the hot loop.

Conceptual model, not fitted parameters:

```text
tau_i * dr_i/dt = -r_i + phi_i(sum_j g_ij * r_j + input_i - adaptation_i)
g_ij = fixed anatomical baseline_ij * receptor effect_ij * plastic multiplier_ij
```

- Start at a fixed **5 ms integration step**, with fast time constants in a provisional 10–100 ms range. Validate smaller steps and fitted time constants; these values are engineering starting points, not measured values for all fly neurons.
- Separate fast transmission, adaptation, dopamine/octopamine modulation and slower homeostatic variables. Do not give all neuromodulators instantaneous excitatory effects.
- Map synapse count to baseline strength with declared class-level scaling. Retain raw anatomical counts. Receptor evidence overrides an over-simple transmitter-sign lookup; unresolved effects require sensitivity analysis.
- Include local KC terminal/plasticity compartments and spatially limited APL activity. APL is non-spiking and its inhibition is locally structured, so one global inhibitory scalar is an especially consequential approximation. [Amin et al., 2020](https://elifesciences.org/articles/56954)
- Parameter sharing by cell class controls the number of free parameters. Fit to fly conditioning, perturbation and response data, not desired Genesis outcomes or business profitability.

A simplified full-brain leaky-integrate-and-fire model has already predicted selected sensorimotor responses, establishing that connectome-constrained simulation can be useful. It does not validate all internal states or biological real-time performance for this proposal. [Shiu et al., 2024](https://www.nature.com/articles/s41586-024-07763-9)

Use a spiking/LIF submodel later only where spike timing is necessary for a prespecified experiment. Hodgkin–Huxley dynamics for every neuron would add unsupported parameter detail, not automatically improve fidelity.

### Plasticity that changes the neural organism

**BIOLOGICAL FACT.** Dopamine-dependent changes at KC→MBON synapses provide a supported associative-learning mechanism. Timing and cell type affect the direction and persistence of learning. [Hige et al., 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/), [Aso and Rubin, 2016](https://pubmed.ncbi.nlm.nih.gov/27441388/)

**COMPUTATIONAL MODEL.** Use a compartment-local three-factor rule: recent presynaptic KC activity, a local eligibility state, and the appropriate dopamine signal. One schematic form is:

```text
d eligibility_ij/dt = -eligibility_ij/tau_e + local_coactivity_ij
d multiplier_ij/dt = eta_c * F_c(eligibility_ij, dopamine_c, timing)
                    - slow_relaxation_c
```

`F_c` must be fitted to the selected compartment's paired/unpaired and timing experiments; its sign is not a global “reward strengthens everything” rule. Bound multipliers, preserve the anatomical baseline and never create unobserved edges. Begin with short-term associative change and measured familiarity recovery. Add a slower consolidation state only after separate retention experiments; do not claim a molecular account of long-term memory.

DPM participation supports investigating consolidation, but sleep need not make every memory stronger: appetitive memory can use sleep-dependent or sleep-independent pathways depending on feeding conditions. [Food availability and consolidation](https://www.nature.com/articles/s41586-020-2997-y)

**GENESIS MAPPING.** A later encounter with the same cue must evoke different neural activity and preference after training, even with the LLM disabled and prose memories unavailable. Neural plasticity stores learned cue associations; database memory still stores language, facts and episodes. Those are distinct kinds of memory.

Do not stretch a seconds-scale eligibility trace across a multihour business outcome and claim fly-like credit assignment. Represent logged intermediate contact and immediate outcomes, or explicitly label any longer task-credit mechanism as a separate product model. Persist plastic weights, eligibility, adaptation and modulatory state, not just final output labels.

## 6. Time, sleep and continuity

Use three explicit time scales:

| Scale | Proposed update | Interpretation |
|---|---|---|
| Neural | Fixed 5 ms logical steps initially | Fast rate dynamics and transient responses |
| Modulatory/homeostatic | Seconds to minutes, integrated against elapsed logical time | Modeled resource availability, adaptation and sleep pressure |
| Circadian | Approximately daily phase, with explicit entrainment input | Phenomenological clock coupled to identified clock neurons |

The slow variables are **computational approximations of physiology absent from the static connectome**. Their influence on neural excitability must be bidirectional where modeled and causally testable. A scheduler that simply says “sleep at midnight” is not a biological sleep circuit.

Maintain a timestamped input stream and a deterministic logical clock. A live worker maps wall time to logical time; offline tests replay recorded elapsed intervals. While resting, neural/state evolution continues; it is not conditioned on browser visits or LLM requests. Long quiet periods may use validated multirate integration, but must not freeze state until the next tool action.

On downtime, restore the last checkpoint and apply a declared recovery policy. Bounded slow-state catch-up can be an approximation; it must not fabricate fast neural activity, actions or experiences during the outage. Log the gap. Operator pause freezes logical execution unless an explicitly configured policy says otherwise; never retroactively convert pause into sleep.

## 7. Sensory encoder and digital body

The current seven scalar channels are useful product features, but insufficient as a fly sensory interface. Proposed future input packets contain stable cue identity, modality/boundary, intensity, onset/duration, provenance and elapsed time.

| Input | Biological boundary | Computational encoding | Genesis interpretation |
|---|---|---|---|
| Reidentifiable cue | Real ALPN populations and their downstream wiring | Fixed, logged cue-to-population codebook; repeated cues reproduce the same input | A context/task can become familiar and acquire value |
| Appetitive outcome | Audited reward pathway; initially compartment-specific DAN boundary stimulation | Phasic current, distinct from anticipation | Independently verified acquisition/success |
| Aversive outcome | Audited aversive pathway/DAN boundary | Separately calibrated event with explicit magnitude cap | Verified loss/harm, not LLM dissatisfaction |
| Resource availability | Literature-supported motivational modulation | Slow body-state input; peptide effects modeled separately from chemical edges | Resource runway; not simulated starvation |
| Urgent threat | LC4/LPLC2 input boundary | Intensity and urgency of imposed threat evidence | Operational hazard analogy |
| Contact/completion/interruption | Audited persistence and acquisition pathways | Timestamped progress/contact and outcome signals | Continue, finish or interrupt current activity |
| Environmental phase/activity | Clock and state-circuit boundary | Declared day/night/elapsed-time input and activity feedback | Continuous life rhythm |

All rows are **product analogies**, not statements that digital stimuli naturally activate these cells. Inputs imposed downstream must be displayed as such. Stable cue coding preserves stimulus identity, but does not give the fly semantic understanding. Counterbalance the codebook in tests to expose arbitrary innate biases from the chosen PN patterns.

Do not directly inject a “novelty = 1” command into an output neuron to manufacture curiosity. Repetition/familiarity should arise from presentation history and neural plasticity. Likewise, uncertainty is not automatically a fly uncertainty neuron: use ambiguous/conflicting cues experimentally, and label any numerical confidence as a model readout.

## 8. Rich outputs with a subordinate LLM

The output should be a **continuous, evidence-bearing state plus constrained affordances**, not another five-label classifier.

Proposed fields, all versioned model readouts:

- Candidate-specific learned attraction/aversion and familiarity response.
- Engagement and persistence; interruption/withdrawal evidence.
- Threat-response drive and action-suppression evidence.
- Arousal, modeled sleep pressure, wake/rest/sleep regime and circadian phase.
- Permitted candidate IDs, permitted action families, commitment horizon and abstention.
- Contributing root IDs, compartments, activity windows, readout coefficients and sensitivity/uncertainty metadata.

“Exploration preference” is derived from unfamiliar-cue responses competing with learned values under the current state. It is not a newly named biological neuron. Readout thresholds and the translation from descending signals to digital engagement are **GENESIS MAPPINGS**, fixed and logged.

The environment/tool registry should enumerate feasible candidate affordances before reasoning. Present their cues through a balanced, reproducible protocol. The neural system supplies relative preferences and permitted families; an explicit decoder translates them to enforceable constraints. Avoid an LLM choosing the candidate shortlist in a way that predetermines the neural choice.

The LLM may implement “research,” “read,” “work,” “draft a service,” “reflect,” or “communicate” only within that authorization. If several actions remain equally permitted, it may choose among them and must record that residual choice. Reject attempts to override candidate, state, budgets or abstention. Financial and physical safety gates remain independent and can veto an action; log such vetoes separately from neural decisions.

Reading a book is not a biological fact. Its **product mapping** is an available information-gathering action. Reflection is not automatically synaptic consolidation. Business creation is a digital affordance assembled by reasoning, not a fly drive. If the neural state changes but practically every action remains allowed, the constraint layer is too permissive.

## 9. Validation: prove causality and test biological claims separately

Preregister protocols and expected directions before fitting. A graph ablation changing an output only proves dependence, not biological validity. Require both causal dependence and agreement with specific experimental findings.

| Experiment | Intervention and expected discriminating result |
|---|---|
| Integrity/replay | Pinned root/edge/annotation hashes, fixed ordered updates, explicit PRNG state; identical snapshot + timed inputs reproduces neural and plastic state within declared numeric tolerances |
| Wiring controls | Remove edges, shuffle destinations preserving degree/strength, permute labels; compare tasks with intact model while holding encoder/decoder fixed |
| Associative conditioning | Counterbalanced cues with paired vs unpaired appetitive/aversive outcomes; preference changes after paired training and not equivalently in controls |
| Plasticity necessity | Freeze KC→MBON plasticity or perturb relevant DAN compartment; learned preference change is selectively reduced while basic sensory responses remain |
| Neural memory | Disable the LLM and hide prose memory; learned preference persists; restore pretraining plastic state and test loss of the learned effect |
| Novelty/familiarity | Repeat one cue, introduce another, test recovery; perturb α′3 mechanism to distinguish stimulus-specific familiarity from global fatigue |
| Motivation/persistence | Compare resource states and maintained cue contact; perturb PPL101, MBON11/18 or OA-VPM4 using the published odor-pursuit paradigm before digital analogies |
| Threat | Vary looming-like feature inputs; perturb LC4/LPLC2/DNp01; reduction of the chosen escape readout without erasing unrelated learned preference |
| Sleep | Compare spontaneous quiescence with reduced responsiveness, strong-stimulus awakening, deprivation/rebound and phase shifts; perturb state vs clock components separately |
| Specificity | Matched-size control lesions, dose sweeps, restoration/rescue, left/right comparisons and unfamiliar held-out cues |
| Boundary robustness | Nested subnetworks and omitted-input perturbations; direction of major results survives plausible external drive and parameter ranges |
| Timing/model robustness | Smaller integration steps, alternate parameter samples and rate/LIF comparison where relevant; do not select only the convenient parameter set |
| LLM subordination | Adversarial planner suggestions, reordered wording and a fixed planner; prohibited actions stay rejected and circuit perturbation still changes permitted behavior |
| Idle and continuity | No obligation to act each cycle; identical logged time across restart reproduces state; browser absence does not alter logical simulation |

Do not require every lesion to eliminate every behavior. Selective effects, rescue and preserved unrelated function are stronger evidence. Sleep consolidation, social claims and generalized exploration stay outside the advertised capabilities until their specific tests pass.

## 10. CPU, RAM and continuous operation

These are **analytical planning estimates, not benchmarks**. They exclude LLM inference and database service memory. No cloud pricing or real-time performance has been measured in this task.

| Configuration | Initial provisioning hypothesis | Numeric workload at 5 ms steps |
|---|---|---|
| Existing worm | Existing runtime; marginal neural workload is small | 4,800 anatomical edges per update; retain current timing/model |
| Proposed 8–12k fly subnetwork | Start benchmarking on 2–4 dedicated vCPU, 4–8 GB RAM | At 0.2–1.5M edges, approximately 40–300M edge accumulations/second |
| Full 139k fly graph | Benchmark 8–16 dedicated vCPU, 16–32 GB RAM; evaluate acceleration only if needed | At 15.1M edges, approximately 3.02B edge accumulations/second |

For a basic sparse matrix, 32-bit index + 32-bit weight costs approximately **8 bytes/edge** before row pointers and additional state: 1.6–12 MB for the subnetwork allowance, about 121 MB for the full pair graph. Plastic multipliers, eligibility, compartment groups, transmitter-specific operators, checkpoints and temporary arrays multiply this. Language object overhead can be much worse. Large input files do not imply that their entire uncompressed content must remain resident.

The full graph's lower-bound edge read traffic alone is approximately **24 GB/s** at 200 Hz; actual work includes indexing, state access and nonlinear updates. Shared cloud CPUs may not sustain the required throughput. A full model at 10–50 Hz is cheaper but is a different temporal approximation requiring validation. A GPU is neither automatically necessary nor automatically sufficient.

For a production claim, benchmark the extracted model at the selected time step, including plasticity, checkpoints and simultaneous API load. Require headroom and stable wall-time lag over a 24-hour run. If 5 ms updates cannot keep up, report the simulated/wall-time ratio; do not silently skip integration steps.

**Trace storage can dominate cost.** Uncompressed float32 activity at 10 Hz is about 34.6 GB/day for 10k neurons, and about 481 GB/day for 139,255 neurons, before metadata. Save sparse events, checkpoints, compact summaries and selected genuine decision windows. Reconstruct replay only from recorded inputs/checkpoints under the pinned model, clearly labeled as replay. Never synthesize visual activity.

## 11. Migration design — future work only

### What is already compatible

The current `BrainAdapter` exposes `initialize`, `stimulate`, `step`, `decodeBehavior`, `getState` and `snapshot`. Organism identity, wallet, memory, businesses and life history are separate from `BrainSnapshot`. That separation is the right foundation.

### What is not a drop-in replacement

The current `Stimulus` fixes seven channels and `BehavioralOutput.behavior` fixes five behaviors. The planning context consumes those constraints. Rich fly semantics cannot honestly be added just by swapping the class name, or by hiding a new contract in `scores`.

Propose a **future additive, versioned BrainAdapter V2**, preserving the lifecycle method names:

| Method / addition | Proposed responsibility |
|---|---|
| Capabilities/schema description | Declare supported input packets, output dimensions, timing units and trace encoding; no fly assumptions in the organism |
| `initialize(snapshot?)` | Restore only a compatible adapter/data/model version; reject incompatible state |
| `stimulate(packet)` | Structured, timestamped sensory/boundary input; return exact neuron/compartment stimulation provenance |
| `step(...)` | Explicit logical duration or fixed-step count with declared time base |
| `decodeBehavior()` | Rich neural state, candidate constraints, abstention and inspectable evidence |
| `getState()` | Typed state/trace view suitable for compact transport; root IDs remain strings |
| `snapshot()` | Adapter/model/data hashes, neural/slow/plastic state, PRNG and logical clock; immutable scientific provenance |

A separate legacy wrapper would expose the existing worm's seven-channel/five-behavior semantics unchanged. The future fly planner boundary consumes V2 constraints. Neither adapter knows what a wallet or business is. Safety and digital affordance translation belong outside the neural implementation, with versioned mappings and tests.

### Safe future sequence

1. Freeze the accepted C. elegans adapter, scientific documentation and organism records. Keep historical adapter IDs intact; do not relabel old worm decisions as fly decisions.
2. Create an independent research model and immutable extraction manifest after licensing/crosswalk checks. Run synthetic fly-task validation with no Genesis writes or external actions.
3. Shadow-replay recorded digital events with the proposed encoder. Compare sensitivity and constraints without changing the live organism or claiming equivalent worm/fly state.
4. Only after scientific and operational acceptance, add the versioned adapter/planner interface and persistence support in a separately authorized implementation task.
5. At an explicitly authorized migration, archive the last worm snapshot, record a brain-lineage event, and initialize the fly from a documented baseline. **There is no justified mapping from 302 worm membrane states into fly neuron states.** Preserve identity, birth, age, seven existing cycles, money, memories and businesses unchanged.
6. Keep rollback possible with the archived worm snapshot and an honest history of the interval. Do not erase the organism's experiences to make rollback look seamless.

## 12. Decision gates and limitations

Proceed with B only when the following are demonstrated:

- Licensing/provenance and the seven-ID annotation discrepancy are resolved for the actual extraction.
- Every advertised circuit has a reviewed root-ID manifest; ambiguity is recorded, not guessed away.
- Learned neural preference works without an LLM or prose-memory lookup.
- Circuit lesions have selective, reproducible effects beyond generic network disruption.
- State/behavior survives plausible boundary and parameter variations.
- Sleep claims meet behavioral criteria; otherwise expose only modeled rest/arousal.
- Neural outputs materially constrain available digital actions, with observable intervention effects.
- Continuous runtime meets measured timing and storage budgets.

If only associative learning passes, ship a clearly described **fly associative-drive model**, not a complete biological-life simulation. If removing the surrounding brain reverses core effects, expand the subnetwork; if expansion and calibration do not solve the problem, keep C. elegans and reconsider the claim. A full connectome does not supply missing physiology, endocrine state, learning rules, embodiment or semantic understanding by itself.

No result here establishes sentience, a faithful living fly, or a biological basis for entrepreneurship. The defensible goal is narrower and testable: **real anatomy constrains a transparent neural model; experience alters its state; its outputs causally constrain Genesis's digital behavior.**

### Task preservation record

This task added research documentation only. It did not implement a fly adapter, run organism cycles, alter planner/persistence code, replace connectome data or modify the original scientific documentation.

Unchanged files checked during research:

- `core/brain/celegans.ts`: SHA-256 `0ee044fcd922e4916340a6c7083903a310ae3af7998d07c2eefc910169806fec`
- `data/connectome.json`: SHA-256 `1b8bc920fe1899b1bf8350acec84539d34ffe7f4d5351a4d5627fb786344babe`

The annotation census and license metadata were inspected in an ignored local research cache. No downloaded fly data was incorporated into Genesis's runtime.
