# Project Genesis — scientific ledger

Genesis is an artificial agent with a connectome-constrained numerical controller. It is not a living worm, a validated emulation of a worm, or evidence of consciousness. The 302-neuron count describes the adult hermaphrodite nervous system, including neurons outside the head.

## 1. Direct biological data

See [data provenance](data/README.md). We retain the OpenWorm neuron names, its broad cell-role annotations, chemical direction, gap-junction adjacency, and serial-section weights from the processed Cook 2019 reconstruction. Connectivity is a composite reconstruction; it is not this software organism's measured physiology. CANL and CANR retain their names even if they are weakly connected. We exclude muscles, glia and other non-neuronal cells and simulate no body mechanics.

## 2. Computational modeling

The implementation is a continuous, leaky, bounded activity model with synchronous Euler updates. Variables are dimensionless activation, not volts, calcium fluorescence, action potentials, or measured firing rates. Raw anatomical edge weights are log-transformed and normalized for numerical stability. Chemical edges default to positive transmission because structural data alone do not identify physiological sign. D-type motor output is modeled inhibitory as a coarse GABA-inspired assumption; AWC→AIY/AIA is assigned inhibitory sign based on the circuit literature. Neither provides a complete receptor/sign model. Gap junctions are symmetric diffusive coupling.

Leak, gains, input amplitudes, adaptation, integration steps and decoder thresholds are engineering parameters, not fitted biological measurements. No random activity is added. A persistent snapshot includes activity, input, adaptation and simulation tick. No synaptic learning, realistic neuromodulation, ion channels or embodied locomotion are claimed.

## 3. Sensory product mappings

The brain never receives language. The agent converts explicit event features into normalized scalar channels. Every mapping below is a **product analogy**, not evidence that a worm understands money, uncertainty, humans or the internet.

| Product channel | Stimulated cells | Biological motivation / limit |
| --- | --- | --- |
| rewardOpportunity | AWA L/R, ASE L/R | Attractive odor / soluble chemical sensing; economic opportunity is our analogy. |
| danger | ASH L/R | Aversive polymodal sensory pathways; financial loss is our analogy. |
| novelty | AWC L/R | Odor removal and local search; arbitrary novelty is not a measured AWC modality. |
| scarcity | AWC L/R, ASK L/R | Food-context/search analogy; no claim that cash depletion is hunger. |
| acquisition | AWA L/R, CEP D/V L/R | Food-associated olfactory/mechanical input analogy; serotonin/dopamine dynamics are not simulated. |
| uncertainty | AWC L/R, ASH L/R, weakly | Engineering mixture of searching and aversive input, no biological uncertainty sensor. |
| social | ASK L/R, URX L/R | Chemosensory and oxygen-context inputs associated with aggregation circuits; human messages are an analogy. |

## 4. Neural decoding and agency

The decoder reads actual simulated downstream cells: AVB/PVC and B-type motor pools (forward), AVA/AVD/AVE and A-type motor pools (reversal), AIB (local search), and AIY (navigation-related interneuron). Their weighted scores select APPROACH, AVOID, RETREAT, EXPLORE or WAIT. These discrete labels, gains and thresholds are our action policy. They are not labels extracted from the anatomical dataset or a validated ethogram. Decoder input excludes event channels: disconnecting the connectome eliminates downstream transmission from a resting state. Safety can block an action, but neither the planner nor guard may relabel the brain's behavior.

Neural visualization uses recorded activation at each integration sample. Node coordinates are a schematic role-based layout, **not anatomical positions**. Edge brightness is computed from the recorded source activation; it is not a measurement of synaptic flux. Replay and current state are labeled separately.

## Sources for circuit motivation

- Cook et al. (2019), [whole-animal connectivity](https://doi.org/10.1038/s41586-019-1352-7).
- Chalasani et al. (2007), [Dissecting a circuit for olfactory behaviour](https://www.nature.com/articles/nature06292): AWC odor removal, AIB activation and AIY inhibition.
- Bargmann (2006), [Chemosensation in C. elegans](https://www.ncbi.nlm.nih.gov/books/NBK19746/): sensory modalities and navigation circuits.
- WormAtlas, [AVD](https://www.wormatlas.org/neurons/Individual%20Neurons/AVDmainframe.htm): reversal-associated interneuron and A-type motor circuit.
- Macosko et al. (2009), [A hub-and-spoke circuit drives pheromone attraction and social behaviour](https://doi.org/10.1038/nature07886): aggregation circuit motivation, not human social cognition.

## Validation scope

Decoder v1 calibration: `forward = mean(AVB,PVC) + 0.4 mean(DB,VB) + 0.3 mean(AIY)`; `reverse = mean(AVA,AVD,AVE) + 0.4 mean(DA,VA)`; `search = 0.8 mean(AIB)`. WAIT if all three are below 0.008. Reversal wins if greater than 1.02 × forward and greater than search; reversal above 0.07 becomes RETREAT, otherwise AVOID. Otherwise search greater than forward becomes EXPLORE; the remaining active cases become APPROACH. These thresholds were calibrated against three demo stimuli at 80 steps from rest, explicitly an engineering calibration rather than biological validation. Initial 1.2 × reversal dominance failed to distinguish the danger case; lowering it to 1.02 exposes the modest modeled reversal preference. Persisted history can change the result for the same subsequent stimulus.

Exact dynamics: chemical weights `sign × log(1+w) / max(1, sumIncomingLogWeights)`, chemical gain 0.85. Electrical weight `log(1+w) / max(1, totalGapLogWeightAtEitherEndpoint)`, gain 0.25, symmetric diffusive current. Each step computes `target = clamp(tanh(input + chemical + gap - 0.12 adaptation), 0, 1)`, then `activity += 0.15(target-activity)`, `adaptation += 0.008(oldActivity-adaptation)`, and `input *= 0.995`. All updates are synchronous. One cycle integrates 80 steps and stores frames every 4 steps, including the initial frame. Between decisions the neural state persists; no implicit reset or time-to-tick conversion is used.

Tests establish determinism, data integrity, finite bounded dynamics, snapshot replay, causal dependence on connectivity, action constraints, and persistence/economic invariants. They do not establish biological fidelity. Decoder behavior depends on engineering choices; a connectivity ablation demonstrates material use of the graph, not that this is the unique or correct biological model.

## Demo world, distinct from the brain

Successful reading currently produces `rewardOpportunity=1` as an explicit development-world rule. A saved draft produces opportunity 0.9 / novelty 0.1. Work produces either acquisition 0.8 / opportunity 0.4 on simulated revenue or opportunity 0.75 / uncertainty 0.1 otherwise. Failed actions produce danger 0.7 / uncertainty 0.5. Rest/reflect reintroduces novelty 0.35. These are product rules, not learned biology. The local planner rotates among permitted reading activities and develops a saved project; it is explicitly deterministic. A live language planner is optional and cannot change the decoded impulse.

## Continuous life and product identity

Project Genesis’s birth time and immutable organism ID describe software continuity. Age is wall-clock time since that record, not neural developmental age. Memories, projects, milestones and simulated finances belong to the organism and persist through storage migrations and explicit brain replacement. They do not arise directly from anatomical data.

A product-level energy budget decreases by 0.13 after active actions and recovers by 0.20 on rest, idle or reflection. Recovery latches at energy ≤0.20 and clears at ≥0.80. This is an explicit scheduling/planning device, not measured metabolism, sleep or neural fatigue. Every behavioral allowlist permits `idle`: leaving an impulse unacted upon preserves its decoded label. The local planner uses it during recovery; the LLM receives the same context and constraints. Idle creates a saved experience without an external action or expense. Its next event contains no invented reward. Resting actions double the schedule interval. Wall-clock pauses do not generate missing neural samples.

The Postgres runtime, birth timeline, planner configuration and deployment changes do not modify the neural equations, anatomical dataset or original deterministic/ablation tests. The website reads saved frames from the persistent runtime. Neither a browser animation nor a service heartbeat is neural activity. The language planner supplies an action rationale, not a scientific explanation of neuronal causation; the actual causal evidence is the stimulus, saved activation, readout values and ablation tests.
