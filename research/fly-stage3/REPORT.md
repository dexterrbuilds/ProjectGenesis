# Stage 3 — resource-state modulation and persistence

**Final classification: PARTIAL-INCONCLUSIVE. Stop for review.**

This preparation demonstrates a small, selective, anatomy-dependent resource effect
and a persistent local experience effect. It **does not establish persistence,
withdrawal or voluntary abstention**. All six primary cue/seed pairs miss the
prospective 10% MBON11 resource threshold and the joint 5% experience thresholds.
MBON11 low/high contrast is 0.04958433%–0.118655429%; low-resource
trial-dependent MBON11 decline is 0.0238223752%–0.0605364741%.
LH experience change is only 2.14946356e-06%–1.77687783e-05%.

The assumed inhibitory MBON11→MBON18 path also creates competing readout directions.
No sign-flipped, thresholded or fitted decision decoder was introduced to turn these
signals into “continue” or “give up.” The stronger learned-value × resource-state
claim is unsupported at the preregistered magnitude. No parameters, anatomical
selection, thresholds or neural equations were adjusted after the main battery began.

## Frozen prior work and scope

[FROZEN_BEFORE.json](FROZEN_BEFORE.json) records 1,025 files spanning both research
stages and Genesis core/data/runtime/server. [PRESERVATION.json](PRESERVATION.json)
records the final comparison. Stage-1 essential tests pass 10/10; Stage-2 tests pass 9/9;
both primary trained-state hashes reproduced exactly before Stage 3 implementation.
Stage 1 remains **PASS**, Stage 2 remains **PARTIAL-INCONCLUSIVE**. Their models,
parameters, accepted results, reports, extractions and manifests were untouched.
The C. elegans adapter/connectome and the canonical organism/database remain
unchanged, with seven life cycles. No canonical cycle, migration or activation ran.

## BIOLOGICAL FACT

Experimental and crosswalk evidence is independently audited with authoritative
links in [LITERATURE.md](LITERATURE.md). It supports state-dependent MB computations
and identifies candidate PPL101/MBON11/MBON18/OA-VPM4 pathways, but not a universal
monotonic persistence readout. In particular, the original tracking experiments
explicitly leave MBON interaction and behavior relationships unresolved.
[Sayin et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6839618/).

The peptide evidence supports a direction of motivational modulation, not a chemical
edge-count-derived receptor graph. Source neurons, peptide dose, receptor location,
co-transmission and compensatory physiology are not established by this extraction.
[Krashes et al., 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2780032/),
[Tsao et al., 2018](https://elifesciences.org/articles/35264),
[2024 compensatory reinforcement study](https://pubmed.ncbi.nlm.nih.gov/38795709/).

## Circuit and provenance

Adult female FAFB/FlyWire materialization 783, annotationv3.1.0; source checksums and
licensing inherited from the audited original cache. Root IDs are strings, never
JavaScript numbers. The model is new and isolated. More KCs are needed here than
Stage 2 because the target compartments involve γ and αβ populations. Neuron count
was not an objective and no post-result expansion occurred.

- **4,563 neurons; 304,192 directed pairs; 375,699 pair/neuropil rows;
  905,536 anatomical contacts.**
- 4,214 KCs,317 cholinergic ALPNs, two each MBON11/MBON18/PPL101/OA-VPM4/APL/LHCENT1,
  four each MBON07/MBON14, 12 MBON18-connected PD2a1/b1 alias candidates.
- Experience plasticity: **4,203 KC→MBON11 pairs, 5,278 efficacy variables,
  18,268 contacts**. Value context: 3,619 KC→MBON07 pairs, 9,407 efficacy variables,
  22,625 contacts. Value variables do not learn in Stage 3.
- Of the value variables, exactly **4,622** receive copied historical efficacies in
  the transfer assay, with source/target/neuropil/contact count checked against the
  original Stage 1 anatomy. No new synapse or teaching event is inserted.
- Overlap: 1,041 Stage 1 roots;268 Stage 2 roots; **3,374 additional to their union**.
- Omitted: **597,746 incoming and 1,012,673 outgoing proofread contacts**. Boundary
  artifacts contain every external root/contact row and per-class/type aggregates.

| Population | Neurons | Retained input | Omitted input | Input % | Retained output | Omitted output | Output % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APL | 2 | 96169 | 35943 | 72.7935388% | 80846 | 29938 | 72.9762421% |
| CONTROL | 4 | 20786 | 1761 | 92.1896483% | 972 | 6164 | 13.6210762% |
| DAN | 2 | 14479 | 6286 | 69.7279075% | 4402 | 783 | 84.8987464% |
| KC | 4214 | 693392 | 105216 | 86.8250756% | 486978 | 266494 | 64.6312006% |
| LH | 12 | 1992 | 5423 | 26.8644639% | 71 | 6362 | 1.10368413% |
| LHCENT | 2 | 2760 | 13855 | 16.6114956% | 2791 | 9808 | 22.1525518% |
| MB11 | 2 | 19523 | 1030 | 94.9885661% | 2877 | 3963 | 42.0614035% |
| MB18 | 2 | 10359 | 1592 | 86.678939% | 1324 | 5522 | 19.3397604% |
| OA | 2 | 206 | 4605 | 4.28185408% | 174 | 4116 | 4.05594406% |
| PN | 317 | 22366 | 419321 | 5.06376688% | 323823 | 675504 | 32.404108% |
| VALUE | 4 | 23504 | 2714 | 89.6483332% | 1278 | 4019 | 24.1268643% |

### Actual contacts on the proposed causal paths

| Path | Contacts |
| --- | --- |
| DAN->MB11 | 894 |
| KC->DAN | 13889 |
| LH->DAN | 0 |
| MB11->MB18 | 36 |
| MB11->VALUE | 241 |
| MB18->LH | 92 |
| OA->MB11 | 47 |

OA→MBON11 is highly asymmetric:45 contacts from left-labelled OA to right-labelled
MBON11 and 2 in the other direction; cell-side labels are not axonal territorial
boundaries. MBON11→MBON18 totals 36 and MBON18→PD2 totals 92: neither is a giant relay.
The PD2 alias population has only 26.86% retained input, LHCENT1 only 16.61%, and OA
only 4.28%. This prevents a complete natural acquisition/pursuit claim. Direct OA
current bypasses those missing afferents; it must not be presented as their recovery.

All current CB cell types, hemibrain aliases, sides, known and predicted transmitters,
FBbt/VFB IDs and ambiguity notes are retained. PD2 alias membership is not exact
functional-driver membership; only 12/16 annotated alias candidates have observed
MBON18 input and are selected. No NPF-named neuron was invented as a peptide source.
KCs use experimentally established cholinergic identity despite problematic automatic
transmitter predictions. LHCENT1 is modeled inhibitory, consistent with its GABA
annotation. Unresolved MBON07 glutamatergic outputs and non-MBON11 OA fast effects
are numerically zeroed, while their anatomical rows remain in the extraction.

Compartment localization remains coarse:16,494/18,268 experience-plastic contacts
carry MB_PED labels; remaining neuropil labels are fully enumerated in the anatomy
audit. Neither these region labels nor cell names prove molecular receptor placement.

## COMPUTATIONAL MODEL — what was assumed

[PLAN.md](PLAN.md) fixes parameters, thresholds and comparisons before simulations.
Float64 rate dynamics use dt 10 ms, fast tau 50 ms, KC threshold0.15, and eligibility
500 ms. Weights are proportional to contacts, normalized by **all proofread input**
at each target. Omitted inputs are silent. Conductances, gains and time constants
are not measured for this specimen.

A body-boundary variable obeys `dr/dt=(resource_input-r)/60 s`, initialized 0.2/0.8.
Only PPL101 responsiveness receives `g(r)=0.2+0.8r`. Lower resource reduces this
pathway's responsiveness. This is a directional dNPF-related approximation, **not
biological starvation, molecular NPF release or a persistence input**. There is no
PPL101 tonic injection. Its activity depends on retained neuronal inputs.

On observed KC→MBON11 rows, acute transmission is divided by `1+D`, where D is
contact-weighted activity from real PPL101→MBON11 contacts. Efficacy follows
`dm/dt=−0.08×KC_eligibility×D×m`, bounded 0.1–1. These transfer functions are hypotheses.
Resource state does not directly set output, activity thresholds or learning rate.
OA stimulation inhibits MBON11 only through real OA→MBON11 contacts. No other OA
sign, receptor distribution or unobserved route is invented.

Persistent state contains rates, eligibility, per-edge efficacy, body state, clock,
PRNG and fingerprints. It contains no cue count, reward score, task appraisal,
continue/give-up flag or prose memory. The input stream contains numeric sensory
currents/timing, a bounded resource input, and specified OA currents in surrogate
acquisition arms. There is no LLM, database or product dependency.

## Protocol, baseline and resource counterbalancing

Seeds 3701/3702/3703; equal-cardinality disjoint A/B PN patterns (16 roots each), fixed
amplitude 1. Both resource conditions have **identical hashed sensory schedules**.
Twelve primary conditions run independently in seeded randomized order. Baseline
probes use disposable snapshot copies to avoid contaminating actual acquisition.

Ten12 s contact periods start0, 24,…,216 s, total240 s. Early contacts yield no
acquisition; absence of reward is not converted to a failure current or stop rule.
Primary readouts are raw dimensionless population rates during2–10 s after onset;
additional onset, tail, post-offset and single-neuron data are saved. These are not
spike frequencies, measured fly speed or motor decisions.

| Seed / cue | MBON11 low first → last | MBON11 high first → last | MBON18 low first → last | LH low first → last |
| --- | --- | --- | --- | --- |
| 3701 / A | 0.0185810500423 → 0.0185761921372 | 0.0185775437643 → 0.0185662082732 | 0.00878602417871 → 0.00878603766682 | 0.00107941096657 → 0.00107941115836 |
| 3701 / B | 0.0162877842757 → 0.0162839041386 | 0.0162848879514 → 0.0162758338755 | 0.00962700113043 → 0.00962701447509 | 0.0038573724069 → 0.00385737258309 |
| 3702 / A | 0.0162651918627 → 0.0162600626984 | 0.0162619352602 → 0.016249967642 | 0.00959356763466 → 0.00959358685568 | 0.00645262966658 → 0.00645262991418 |
| 3702 / B | 0.0323726397531 → 0.0323530424985 | 0.0323604259459 → 0.0323146993532 | 0.0272535873971 → 0.0272536572108 | 0.0424665268141 → 0.0424665277269 |
| 3703 / A | 0.0255035799845 → 0.025494861321 | 0.025497718744 → 0.0254773734507 | 0.0133524608369 → 0.0133524824325 | 0.00603615783454 → 0.00603615815531 |
| 3703 / B | 0.0232282846617 → 0.0232207094492 | 0.0232229715862 → 0.023205295219 | 0.0126372716276 → 0.0126372917387 | 0.00752668279254 → 0.00752668308 |

Relative resource contrast is `low/high−1`; experience is `trial10/trial1−1`.
Positive MBON11 resource contrast is the literature-direction test. Positive LH
experience change is an explicit candidate hypothesis, not an established universal
pursuit decoder.

| Seed / cue | MBON11 low (late) | MBON11 high (late) | Low/high contrast | MBON11 experience (low) | LH experience (low) | LH low/high contrast |
| --- | --- | --- | --- | --- | --- | --- |
| 3701 / A | 0.0185761921372 | 0.0185662082732 | 0.0537743834% | -0.0261444054% | 1.77687783e-05% | -3.65247617e-05% |
| 3701 / B | 0.0162839041386 | 0.0162758338755 | 0.04958433% | -0.0238223752% | 4.56771425e-06% | -9.47137959e-06% |
| 3702 / A | 0.0162600626984 | 0.016249967642 | 0.0621235473% | -0.0315346069% | 3.8372008e-06% | -7.52513846e-06% |
| 3702 / B | 0.0323530424985 | 0.0323146993532 | 0.118655429% | -0.0605364741% | 2.14946356e-06% | -4.19309018e-06% |
| 3703 / A | 0.025494861321 | 0.0254773734507 | 0.0686407895% | -0.0341860376% | 5.31423685e-06% | -1.07151061e-05% |
| 3703 / B | 0.0232207094492 | 0.023205295219 | 0.0664254863% | -0.0326120183% | 3.819207e-06% | -7.81752429e-06% |

The raw state effect is selective: PN/KC responses are nearly unchanged, not globally
amplified. But it is small and downstream state effects have the opposite sign.
Maintained responses remain throughout unrewarded cue periods; simply responding
to a maintained sensory current is not evidence of autonomous pursuit.

## Intervention battery

All conditions start with intact-normalization denominators; lesion weights are
zeroed afterwards, never renormalized. Percentage reduction is relative to intact
MBON11 resource contrast for the same cue. Undefined means the required baseline
is absent; it is not counted as selective learning success.

| Condition | Resource contrast MBON11 | Contrast reduction | LH resource contrast | Largest PN/KC lesion change |
| --- | --- | --- | --- | --- |
| control-silence_dan-A | 0% | 100% | 0% | 2.39124265e-07% |
| control-silence_dan-B | 0% | 100% | 0% | 2.68365504e-06% |
| control-silence_mb11-A | undefined | undefined | 0% | 0.00079522125% |
| control-silence_mb11-B | undefined | undefined | 0% | 0.00836525354% |
| control-silence_mb18-A | 0.0537744779% | -0.000175764225% | 1.4656844e-06% | 0.000654169943% |
| control-silence_mb18-B | 0.0495845106% | -0.000364276295% | 2.30629826e-07% | 0.000732589196% |
| control-silence_oa-A | 0.0537736366% | 0.00138882026% | -3.65245275e-05% | 2.63399746e-08% |
| control-silence_oa-B | 0.0495841113% | 0.000441090929% | -9.47135874e-06% | 1.19910526e-08% |
| control-remove_da_gate-A | 0% | 100% | 0% | 2.39124265e-07% |
| control-remove_da_gate-B | 0% | 100% | 0% | 2.68365504e-06% |
| control-freeze_modulation-A | 0% | 100% | 0% | 6.83230805e-08% |
| control-freeze_modulation-B | 0% | 100% | 0% | 7.6675557e-07% |
| control-freeze_plasticity-A | 0.0170807784% | 68.236217% | -1.16360022e-05% | 2.33999375e-08% |
| control-freeze_plasticity-B | 0.0161518418% | 67.4255116% | -3.0734346e-06% | 2.58272526e-07% |
| control-matched_control-A | 0.0537745724% | -0.00035148625% | -3.6523492e-05% | 7.75963516e-05% |
| control-matched_control-B | 0.0495848009% | -0.000949721051% | -9.47097326e-06% | 0.000125862779% |
| control-remove_pn_kc-A | undefined | undefined | 0% | 100% |
| control-remove_pn_kc-B | undefined | undefined | 0% | 100% |
| control-remove_mb11_mb18-A | 0.0537743834% | -1.12850751e-07% | 1.27627302e-06% | 3.858727e-06% |
| control-remove_mb11_mb18-B | 0.04958433% | -1.09221365e-07% | 2.19653939e-07% | 4.12852268e-06% |
| control-remove_mb18_lh-A | 0.0537743834% | 3.90208421e-08% | 1.45273422e-06% | 3.8839707e-07% |
| control-remove_mb18_lh-B | 0.04958433% | 1.35239264e-08% | 2.92783064e-07% | 3.0743984e-07% |
| control-shuffle_pn_weights-A | 0.0535903735% | 0.342188741% | -3.73777459e-05% | 2.74636875% |
| control-shuffle_pn_weights-B | 0.041356146% | 16.5943232% | -6.40827773e-06% | 14.6240854% |
| control-no_apl-A | 0.0550085271% | -2.29504023% | -3.94955115e-05% | 0.9160773% |
| control-no_apl-B | 0.0508381434% | -2.52864843% | -1.00747353e-05% | 0.87132093% |
| control-no_lh_feedback-A | 0.0537743819% | 2.84212095e-06% | -3.72661085e-05% | 2.31743377e-05% |
| control-no_lh_feedback-B | 0.049584319% | 2.21688012e-05% | -9.62218187e-06% | 7.65083968e-05% |
| control-global_gain-A | -99.0212025% | 184241.958% | -82.9012522% | 98.5670314% |
| control-global_gain-B | -99.1847732% | 200132.497% | -81.9474679% | 98.836665% |

PPL101 silencing, local dopamine-gate removal and frozen resource modulation test
the causal route. Frozen plasticity separately tests experience, and MBON11/18
lesions test candidate downstream transmission. The MBON14 matched lesion uses one
cell per hemisphere and is matched in count, not centrality. MBON14 is not claimed
biologically independent of hunger; it is outside the particular modeled direct gate.
PN→KC removal destroys sensory drive, so it cannot count as selective persistence
loss. PN strength shuffling changes weights only on existing anatomical rows and
never fabricates topology. A surviving shuffled effect shows dependence on a motif,
not unique necessity of the exact biological weight distribution.

The global-gain negative control deliberately applies the resource factor throughout
the network. Its sensory changes disqualify it; the evaluator does not call it
motivational selectivity. No tonic-current rescue or post-outcome weight scaling was
introduced. Boundary lesions silence/remove only observed pathways.

## Acquisition, interruption and abstention limits

Acquisition-surrogate arms apply OA current 0.5 from 224–228 s while the PN cue continues.
This is experimental direct-neuron stimulation, not natural taste transduction.
Suppression below is `1−acquisition/control`; a negative value means activation.

| Cue / resource | MBON11 suppression | MBON18 suppression | LH suppression | MBON11 suppression with OA silenced |
| --- | --- | --- | --- | --- |
| A / 0.2 | 5.50854579% | -0.0261575884% | -0.00323454996% | 0% |
| A / 0.8 | 5.51236275% | -0.0261620429% | -0.00323506593% | 0% |
| B / 0.2 | 6.28406918% | -0.0236311038% | -0.000895498191% | 0% |
| B / 0.8 | 6.28803642% | -0.0236353965% | -0.000895640634% | 0% |

OA suppresses MBON11 by 5.5–6.3%, but slightly increases MBON18/LH output. It therefore
fails the joint 20% pursuit-candidate suppression criterion. OA silencing removes
its modeled MBON11 effect but does not resolve the contradictory downstream readout.
This does not establish disengagement. Physical cue interruption removes the sensory
input and consequently neural responses; it is not a threat mechanism or learned
withdrawal. Sham remains silent: absence of activity is not an autonomous abstention
decision. No threat, competing-action policy or motor circuit was added.

## Persistence vs decay, adaptation and imposed drive

| Primary low-resource condition | MBON11 post-offset/maintained | LH post-offset/maintained | Seconds above 25/50/75% in final12 s | Ten vs single final cue MBON11 |
| --- | --- | --- | --- | --- |
| primary-3701-A | 1.46763121e-17% | 5.10142831e-17% | 11.8 / 11.8 / 11.7 | -0.0261444054% |
| primary-3701-B | 1.45389913e-17% | 1.98835902e-17% | 11.8 / 11.8 / 11.7 | -0.0238223752% |
| primary-3702-A | 1.53843819e-17% | 1.55558082e-17% | 11.8 / 11.8 / 11.7 | seeds 3702/3: not scheduled |
| primary-3702-B | 1.51962532e-17% | 1.23937125e-17% | 11.8 / 11.8 / 11.8 | seeds 3702/3: not scheduled |
| primary-3703-A | 1.4933352e-17% | 2.29411811e-17% | 11.8 / 11.8 / 11.7 | seeds 3702/3: not scheduled |
| primary-3703-B | 1.47708012e-17% | 1.93744564e-17% | 11.8 / 11.8 / 11.7 | seeds 3702/3: not scheduled |

Measured post-offset activity is tiny compared with maintained-cue activity; there
is no demonstrated long autonomous after-discharge. The 25/50/75% duration sweep
illustrates maintained cue following and cannot rescue failed raw experience metrics.
Single-last-contact controls match total elapsed time; the small ten-vs-single
change reflects efficacy history, not just more elapsed simulation time. Fast tau
half/double tests are reported below and do not turn slower decay into persistence.

No sensory-adaptation variable exists in this model. PN/KC preservation and plasticity
freeze distinguish the recorded effect from global sensory fatigue within this
implementation, not from every possible real-fly adaptation mechanism. Resource
input alone generates zero neural activity in sham and analytic body-state tests.
There is no externally imposed tonic neural drive in primary conditions.

## Snapshot, reset and replay

All original snapshots restore the saved baselines. All 12 primary acquisitions
replay bit-identically, and 36 clean-environment fresh-process recalls reproduce
trained/fast-reset/original readouts exactly. Fast reset retains body and plastic
state; largest primary recall difference is **6.93889e-18**, below 1e−10.
Cue-only recall after reset retains a MBON11 decrease of
0.0264690018%–0.067260738% from baseline. Thus a genuine modeled
neural/plastic history effect exists even though persistence acceptance fails.

Body-swap probes separately retain the same efficacies while changing current body
state. They do not turn that resource value into an external decision. Body dynamics
are validated against the 60 s relaxation equation; primary high/low assays start at
steady resource levels and do not simulate metabolic starvation or energy spending.
No cross-platform bitwise guarantee is made;1e−10 is the compatible-environment
numerical tolerance, not a timestep-convergence assertion.

### Plastic-state and body-swap measurements

| Condition | Changed efficacy rows (>1e-12) | Largest efficacy decrease | Reset recall / baseline − 1 | Body swap / reset recall − 1 |
| --- | --- | --- | --- | --- |
| primary-3701-A-0.2 | 709 | 0.00115520087234 | -0.0290489665% | -0.0173834225% |
| primary-3701-A-0.8 | 709 | 0.00269424902185 | -0.0677948214% | 0.0173923076% |
| primary-3701-B-0.2 | 601 | 0.000760075841408 | -0.0264690018% | -0.0164272428% |
| primary-3701-B-0.8 | 601 | 0.0017731295466 | -0.0617739263% | 0.0164350071% |
| primary-3702-A-0.2 | 596 | 0.00103805128744 | -0.0350378897% | -0.0182289842% |
| primary-3702-A-0.8 | 596 | 0.00242125254182 | -0.081766745% | 0.0182391845% |
| primary-3702-B-0.2 | 1135 | 0.00190345984724 | -0.067260738% | -0.0342950562% |
| primary-3702-B-0.8 | 1135 | 0.00443878106815 | -0.156993535% | 0.0343323284% |
| primary-3703-A-0.2 | 930 | 0.00121507416659 | -0.0379838612% | -0.0210396886% |
| primary-3703-A-0.8 | 930 | 0.00283413560025 | -0.0886550398% | 0.0210542651% |
| primary-3703-B-0.2 | 872 | 0.00110575725768 | -0.0362349992% | -0.021019846% |
| primary-3703-B-0.8 | 872 | 0.00257923232367 | -0.0845700471% | 0.0210332378% |

Efficacy decrease is an absolute change from the initial multiplier of 1. The body-swap column holds the trained weights fixed and changes the current resource boundary to the opposite level. It measures the acute component; it does not recondition the model.

## Learned association × current state

| Paired cue / intervention | Low naive | Low trained | High naive | High trained | Mixed difference | Relative interaction |
| --- | --- | --- | --- | --- | --- | --- |
| A / intact | 0.0053344293044 | 0.00273011607351 | 0.00533443994 | 0.00273012666382 | 4.52948000287e-11 | 1.73922241e-06% |
| A / silence_dan | 0.00533442132725 | 0.00273010813033 | 0.00533442132725 | 0.00273010813033 | 0 | 0% |
| A / silence_mb11 | 0.00540431883652 | 0.00279970802341 | 0.00540431883652 | 0.00279970802341 | 0 | 0% |
| A / freeze_modulation | 0.00533443462229 | 0.00273012136875 | 0.00533443462229 | 0.00273012136875 | 0 | 0% |
| B / intact | 0.0141000443431 | 0.0077849678706 | 0.0141000676185 | 0.00778499100252 | 1.43507735209e-10 | 2.2724623e-06% |
| B / silence_dan | 0.0141000268852 | 0.00778495052029 | 0.0141000268852 | 0.00778495052029 | 0 | 0% |
| B / silence_mb11 | 0.0142238268426 | 0.00790799095957 | 0.0142238268426 | 0.00790799095957 | 0 | 0% |
| B / freeze_modulation | 0.0141000559811 | 0.00778497943682 | 0.0141000559811 | 0.00778497943682 | 0 | 0% |

The four VALUE neurons' mean response is shown; only the two original Stage 1 output
roots have imported training. The assay preserves a large learned-response difference
in this new context. However, the normalized mixed difference is only approximately
1.74e−6% (cueA) /2.27e−6% (cueB), far below 5%. It disappears under the PPL101/MBON11/
frozen-modulation controls but is near numerical-tolerance scale in absolute units.
The stronger claim is therefore **unsupported**, not evidence of useful value-state
multiplication. Resource effects largely add to, rather than modulate, the learned
response difference. No permanent preference field or new Stage 1 learning was used.

This is a test of transferred efficacies in a **new network context**, not a change
to Stage 1 or proof of physiological transfer between brains. The broader appetite
network and peptide/body inputs are incomplete. A lack of strong interaction here
does not show that biological reward memory is state-independent.

## Parameter and boundary sensitivity

| Variant | MBON11 state contrast | MBON11 trial change low | LH trial change low | PN contrast | KC contrast |
| --- | --- | --- | --- | --- | --- |
| sensitivity-half_dt | 0.0537397708% | -0.0261227019% | 1.77540263e-05% | 3.67773367e-08% | -3.60476582e-07% |
| sensitivity-tau_half | 0.0538727611% | -0.0261957747% | 1.78037483e-05% | 3.68799213e-08% | -3.60443464e-07% |
| sensitivity-tau_double | 0.0535552584% | -0.0260259235% | 1.76881674e-05% | 3.66279895e-08% | -3.61084806e-07% |
| sensitivity-eta_half | 0.0354237877% | -0.0130725831% | 8.88469538e-06% | 2.4231106e-08% | -2.41975739e-07% |
| sensitivity-eta_double | 0.0904983328% | -0.052285766% | 3.55351058e-05% | 6.19316154e-08% | -5.98210881e-07% |
| sensitivity-floor01 | 0.0604945858% | -0.0203337838% | 1.38200726e-05% | 4.14010826e-08% | -4.05773659e-07% |
| sensitivity-floor04 | 0.0403329138% | -0.0377669396% | 2.56663403e-05% | 2.76009438e-08% | -2.7054432e-07% |
| sensitivity-da_half | 0.0452160607% | -0.0261414643% | 1.77679105e-05% | 3.09682502e-08% | -2.99009351e-07% |
| sensitivity-da_double | 0.0708973684% | -0.0261502873% | 1.77705132e-05% | 4.84657425e-08% | -4.84084706e-07% |
| sensitivity-gain 075 | 0.0207168365% | -0.00888153457% | 1.95866041e-06% | 3.16562332e-09% | -3.11001724e-07% |
| sensitivity-gain 125 | 0.0945640487% | -0.049490221% | 6.9347505e-05% | 1.83817739e-07% | 3.6314695e-06% |
| sensitivity-oa_half | 0.0542239236% | -0.68977236% | 0.000397228624% | 3.6858494e-08% | -3.61646812e-07% |
| sensitivity-oa_double | 0.0556116664% | -2.680687% | 0.00153560861% | 3.70314668e-08% | -3.64489838e-07% |
| sensitivity-retained | 0.0970146215% | -0.0489752883% | 4.51178926e-05% | 2.86690147e-06% | 6.2317979e-06% |
| sensitivity-roles | 7.37956296e-07% | -4.98120312e-07% | 2.21123808e-07% | 2.65262923e-08% | 9.09586184e-08% |

All variants were scheduled before the main outcomes. Retained-total and
retained-role normalizations are optimistic alternative assumptions, not replacements
for the all-input primary. No induced current compensates for omitted input.
OA-gain variants use the acquisition arm; other variants use the unrewarded arm.
Full threshold-free effects and sensitivity are reported even if their sign changes,
baselines vanish or large gains saturate activity. No variant can retroactively
replace the failed primary criteria.

For cue A, modest unrewarded variants retain the resource-effect direction, but span 0.0207–0.0946%, still below 10%. Retained-total normalization gives 0.0970%; retained-role normalization nearly abolishes the effect (7.38e−7%). Thus direction alone does not establish robust magnitude. Removing APL increases the primary contrast by approximately 2.3–2.5% relative; removing LH feedback changes it negligibly. These controls cannot establish that unknown omitted inputs would be harmless.

## Prespecified acceptance audit

| Prospective criterion | Result |
| --- | --- |
| LH_experience_increase_at_least_5pct | **not met** |
| MB11_experience_decrease_at_least_5pct | **not met** |
| MB11_state_contrast_at_least_10pct | **not met** |
| OA_lesion_removes_MB11_suppression_80pct | met |
| PN_KC_state_preserved_5pct | met |
| acquisition_MB11_and_LH_suppression_at_least_20pct | **not met** |
| all_36_fresh_recalls_exact | met |
| all_nonzero_baselines | met |
| all_primary_replays_exact | met |
| all_primary_resets_1e_10 | met |
| all_restores_exact | met |
| all_sensory_inputs_matched | met |
| global_gain_negative_control_detected | met |
| matched_preserves_75pct | met |
| mechanism_reduction_80pct_sensory_preserved | met |
| modest_sensitivity_state_direction | met |
| no_cue_sham_zero | met |
| plasticity_freeze_removes_experience_80pct | met |
| remove_mb11_mb18_reduces_LH_interaction_80pct | met |
| remove_mb18_lh_reduces_LH_interaction_80pct | met |
| silence_mb11_reduces_LH_interaction_80pct | met |
| silence_mb18_reduces_LH_interaction_80pct | met |

The evaluator also reports stricter diagnostic checks: exact-zero sham instead of the prospectively allowed <1% response, and 80% downstream interaction reduction where the plan required a reduction without a numeric cutoff. Both stricter checks pass; neither changes the classification. The four failed magnitude criteria above are explicitly prospective.

The classification reflects the joint criteria, not the fact that tests execute.
Selective pathway effects alone are insufficient to establish persistence or a
coherent disengagement readout.

## Performance, execution and genuine artifacts

The 122-condition battery plus12 full primary replays used
**2700.07 s total elapsed wall time** including the checkpoint transition.
The first 93 complete serial conditions were preserved
byte-for-byte; the remaining 29 ran with four local workers
in 682.60 s. Only orchestration changed; the exact neural
model, protocols and parameters stayed fixed. Completed-run hashes are included.
Each acquisition advances 240 simulated seconds, including quiet/contact intervals;
this is not a claim of continuous autonomous motor behavior.

Measured peak worker RSS: **317.30 MiB**; coordinator peak:
261.09 MiB. The conservative concurrent-process
upper bound is 1530.28 MiB, computed from per-process
peaks, **not a sampled combined peak**. Serial-worker peak was not captured before
checkpointing. The learned-state assay took 10.29 s and
396.38 MiB peak RSS. Hardware/environment metadata is
saved with evidence; these are local measurements, not cloud service guarantees.

- [Circuit manifest](artifacts/28cc6285ba4b40077db73952bacee75d0938f2f80021aaf89c214524797b2a52/manifest.json)
- [Anatomical audit](anatomy-audit/63cec86fd34013c3c30be4e844b53514fe2039389cebad46746338b09605b83e/anatomy.json)
- [All 122 condition records](evidence/07ac1e4903fcfdd4a911653a17046acb2f3b5042360eb8972d9f7c5891e605bd/results.json)
- [Acceptance evaluation](evaluations/5d6d99ceb97fbaddc96d314a646a8ac3a76d7bc55a0bc362e47778b2eff34ead/evaluation.json)
- [Learned-state evidence](learned-evidence/be21a04961294190b6a8248fe184bd5c328ad62189ce43e1b8e0cff836dbc2d6/results.json)
- [Comparison CSV](RESULTS.csv)
- [Reproduction instructions](README.md)

Actual group activity is sampled every 100 ms; two dense runs save individual neurons
and all efficacies every 1 s. Snapshots/integration use float64; dense traces use
float32. Per-neuron probe arrays and all initial/trained/reset states are saved.
There is no fabricated activity or visualization. Artifacts are content-addressed
and checked on load; hash immutability is not filesystem write-once protection.

Implementation checks pass 11/11. Scientific acceptance is separately reported above.
Source licensing remains the inherited caveat: Zenodo metadata CC-BY4.0, FlyWire
site/VFB guidance CC-BY-NC4.0, annotation terms not independently resolved. This
work is isolated local research, not commercial data publication or deployment.

## Review decision and remaining uncertainty

This experiment has no validated mapping to continue pursuing, disengage or choose
inactivity. Missing LH/OA inputs, cross-specimen driver aliases, unknown receptor
transfer functions, omitted nitric oxide/peptide physiology, simple point-neuron
APL, fixed synthetic cues and absent descending/VNC/body control are substantive
limits. Cell-type-gated efficacy is not verified subcellular receptor anatomy.
The resource variable is a declared computational boundary, not biological hunger.

**GENESIS MAPPING: none. Stage 1 remains PASS; Stage 2 remains PARTIAL-INCONCLUSIVE.**
Stage 3 ends here with **PARTIAL-INCONCLUSIVE**. No further circuit expansion,
threat/sleep/arousal experiment, BrainAdapter migration or Genesis integration is
performed. Further investigation requires a separate review of these results.
