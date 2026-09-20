# Stage 3 prospective protocol — before any Stage-3 simulation

Freeze Stage 1 PASS and Stage 2 PARTIAL-INCONCLUSIVE, including accepted artifacts,
parameters and reports. New code/data only here; no Genesis imports, cycles or
migration. Scientific failure/inconclusiveness is an allowed result, not a tuning cue.
Literature/root audit: LITERATURE.md. No fitted activity-to-action decoder.

## Extraction decided from anatomy and circuit roles

Bilateral MBON11, MBON18, PPL101, OA-VPM4. Include all actually presynaptic γ and
αβ KCs for MBON11/18 and MBON07. MBON07 supports a separate learned-state transfer
assay using a COPY of accepted Stage-1 plastic efficacies on identical anatomical
rows. MBON14 α3 is a comparator output (not claimed biologically hunger-insensitive).
Actual cholinergic ALPN inputs to selected KCs and hemibrain LHPD2a1/b1 candidates;
connected APL; actual MBON18-connected PD2a1/b1 alias cells and LHCENT1 feedback
partners. PD2 alias membership is ambiguous and separately lesioned. No size target,
no strength threshold and no post-outcome expansion. Include all induced chemical
edges, explicitly zero unresolved physiological effects. Record all omitted inputs
and outputs per population/root and full external-root boundary edges.

## State, inputs, model hypotheses

Independent float64 rate model, dt .01 s, tau .05 s, eligibility tau .5 s. Primary
contact normalization uses all proofread incoming contacts at each target. Omitted
inputs are silent; no tonic compensation. PN→KC gain3, KC→MBON/APL gain1, APL→KC
gain1, GABA MBON11→MBON/other targets gain1; other ACh/GABA recurrence .05. MBON18→LH
and PN→LH gain1, LHCENT1→PN gain.05. DA has no fast sign; MBON07 glutamate targets
have unknown effects here and are zeroed. OA→MBON11 is inhibitory gain1 only on real
OA-VPM4 contacts; other OA fast effects omitted. These are assumptions, not fitted
conductances. Read out MBON11, MBON18, PD2 LH, MBON07, comparator MBON14, PN and KC
activity separately. Do not synthesize a weighted “persistence decision.”

Body variable r in [0,1] follows dr/dt=(resource_input-r)/60 s, initialized low .2
or high .8. PPL101 responsiveness alone is scaled by g(r)=.2+.8r; lower resource
inhibits this pathway, approximating net dNPF-dependent gating direction. r never
directly changes readout, learning rate, motor labels or other neurons. No imposed
PPL101 current: it must obtain neural drive from retained anatomy. The model does
not simulate NPF release/receptors or endocrine starvation.

Local dopamine D at MBON11 is the contact-weighted mean of actual PPL101→MBON11
activity. Acute effective KC→MBON11 transmission is divided by (1+D), an explicitly
hypothesized receptor-mediated transfer, gain1. Experience updates only actual
KC→MBON11 efficacy m via dm/dt=-.08*KC_eligibility*D*m, bounded [.1,1]. No counts,
failure rules or persistent cue scores. Reward-assay MBON07 weights are frozen
copied efficacies, not re-learned or fitted here. Snapshots: rates, eligibility,
per-edge efficacies, body state, clock, PRNG and model/data fingerprint.

Acquisition tests impose .5-current pulses directly at OA-VPM4 (an experimental
boundary stimulation surrogate, NOT a reconstructed gustatory pathway). Control
with OA silenced and input pulse removed. No threat circuit is added. A physical
interruption removes the cue; it is not a neural threat or inferred giving-up signal.

## Primary protocol

Seeds3701/3702/3703. Disjoint equal 5%-of-PN current patterns A/B, amplitude1,
selected without neural-response screening. Same exact PN time series in both body
states, hash checked. Ten 12 s odor/contact trials, starts 0,24,...216 s; total240 s.
The first nine contacts have no acquisition event: the absence of acquisition is
not an injected failure current. Final-trial arms: no acquisition; acquisition
OA pulse224–228 s while cue continues; interruption removes cue224–228 s. Primary
battery is no acquisition across both cues × three seeds × low/high, independent
snapshots (no run-order carryover). Randomize paired execution order deterministically.
Use raw vectors and within-cue comparisons; no thresholds are inside the model.

Primary windows: mean rate2–10 s after each onset, tail8–10 s, first1 s, baseline
before cue, 2 s after offset, and final acquisition window224–228 s. Measure trial10
vs1 responses, PN/KC/comparator changes, late-vs-early cue activity, post-offset
activity decay and duration above 25/50/75% of trial1 amplitude. Activity maintained
only because an unchanged cue is present is NOT evidence of experience-dependent
persistence. Slow decay alone also cannot satisfy acceptance.

Pre/post 2 s cue-only probes from disposable copies of snapshots, same body state;
fast reset of rates/eligibility while keeping efficacies and body; restore original;
swap body state with unchanged learned weights; fresh-process replay and recall.

## Primary acceptance, fixed before outcomes

All six cue/seed comparisons must have: nonzero MBON11/LH baseline (>1e-8); low-vs-
high MBON11 response ≥10% during maintained late cues (direction supported by hunger
response experiments); no >5% PN/KC changes; and an experience-dependent change
≥5% in MBON11 response plus ≥5% in PD2 downstream maintained-cue response, not only
offset decay. MBON11 trial response is expected to decline, not increase; increased
PD2 sustained engagement is a model hypothesis, not a verified universal mapping.
A claim of pursuit remains conditional on this raw multivariate pattern and circuit
interventions. Contradictory MBON18/PD2 effects or a sign-flipped decoder cannot be
silently resolved into a behavioral success.

PPL101 or modulation removal must reduce the resource contrast ≥80%, preserving
PN/KC within5%; frozen plasticity must remove ≥80% of experience-dependent change;
matched two-cell control lesions preserve ≥75% of intact contrast. MBON11/18 and
relevant-edge lesions must reduce the downstream interaction; report if they have
the opposite sign. Acquisition must suppress the relevant raw pursuit-candidate
responses ≥20% during maintained cue, and OA silencing must remove ≥80% of that
suppression. These are operational thresholds, not estimates of fly psychophysics.
No-cue activity must remain below1% of cue response in both states. Reset/restore/
replay tolerances1e-10; fresh-process same-environment bit identity expected.

Sensitivity must preserve direction across the declared modest ranges. No PASS
based only on optimistic boundary normalization. Declare PARTIAL-INCONCLUSIVE for
selective neural effects failing these joint thresholds, unresolved phenotype sign,
or ungrounded boundary/decoder assumptions; FAIL for no causal/selective state or
experience effect or integrity failure. A threshold-free metric accompanies every
categorical criterion. No model is tuned after the battery.

## Controls (seed3701, both cues and resource states unless stated)

Silence PPL101, MBON11, MBON18, OA-VPM4; remove dopamine gate; freeze resource
modulation at g(.5); freeze plasticity; matched two MBON14 cells (one per hemisphere,
lowest root ID; not matched centrality); remove PN→KC; remove MBON11→MBON18; remove
MBON18→PD2; shuffle strengths ONLY among existing PN→KC rows at each KC. No lesion
renormalization. No APL, no PD2/LHCENT1 feedback partners as boundary checks.
No-cue sham; single last cue after equal elapsed time as history control; last-trial
acquisition with/without OA; cue interruption (not threat).

Sensitivity, seed3701 cueA both states: dt .005; tau .025/.1; learning rate .04/.16;
state-gate floor .1/.4; dopamine gate gain .5/2; all fast gains .75/1.25; OA gain .5/2;
all-proofread vs retained-total vs retained-role normalization. A separate global-
gain negative control applies g(r) to ALL desired rates instead of PPL101: it must
be flagged by PN/KC specificity checks, not accepted as motivation. No imposed tonic
current variant is needed: sham plus decay/reset directly test its absence. Threshold
sweeps cannot rescue failed raw response effects. Report full parameter grid.

## Frozen learned-value transfer (stronger, optional claim)

Import only the accepted Stage-1 KC→MBON07 efficacy rows, matching source root,
target root and neuropil; check anatomical contact count equality, reject mismatch.
Do not import its fast state or reward labels into the neural model. Use its saved
numeric cue patterns; compare naive/trained copies at both body states, after the
same sensory probe. No new Stage-1 training. Report mixed difference:
(trained−naive)_low − (trained−naive)_high, raw and normalized. Compare PPL101 and
MBON11 lesions. This is a new Stage-3 network context, NOT another acceptance of
Stage-1 behavioral interpretation. If no ≥5% modulation of learned expression,
report the stronger claim unsupported. No financial/product mapping.
