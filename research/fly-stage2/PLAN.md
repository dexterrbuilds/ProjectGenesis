# Stage 2 — prospective protocol, 2026-09-17

Recorded before running any Stage-2 learning model. Stage 1 and Genesis are frozen.
This is an isolated numerical experiment, not a migration or a living-fly claim.
No outcome-driven parameter search, source replacement, or circuit enlargement.

## Biological basis and crosswalk

Hattori et al. (2017), https://doi.org/10.1016/j.cell.2017.04.028:
α′3 MBON odor responses decline selectively with repetition; odor-evoked PPL1-α′3
activity is required. Suppression persists beyond 20 minutes and recovers around
an hour; dopamine without the trained odor can accelerate recovery. The original
MB027B measurements pool α′3 outputs; MB304B targets the corresponding DAN.
These observations do not identify the physiological gain of individual FAFB edges.

Pribbenow et al. (2022), https://elifesciences.org/articles/80445:
postsynaptic α′3 response depression occurs without matching depression in imaged
α′β′ KC arbors. Nicotinic receptor subunits contribute to expression/induction.
Use their 10 × 1-second odor pulses with 6-second gaps. Our plasticity variable is
an effective, contact-specific postsynaptic efficacy, not a measured receptor count.

Li et al. (2020), https://elifesciences.org/articles/62576:
MBON16/17 correspond to α′3ap/α′3m, respectively; MBON17-like cells have related
morphology but different connectivity. MBON13 is the α′2 comparison output.
PPL104 corresponds to PPL1-α′3. VFB confirms individual FAFB identities:
https://www.virtualflybrain.org/blog/2022/01/01/mbon16-vfb_fw031879/
https://www.virtualflybrain.org/blog/2022/01/01/mbon17-vfb_fw008387/
https://www.virtualflybrain.org/term/ppl104-vfb_fw035370/
These are type/morphology crosswalks across specimens, not root-specific functional
recordings. MBON17-like and MBON28 are included as four explicitly ambiguous
surrounding partners; no familiarity plasticity is assigned to them. Rubin & Aso's
updated drivers could not definitively distinguish MBON28 from MBON16/17:
https://elifesciences.org/articles/90523 . Test their removal, not a post hoc expansion.

## Fixed extraction

Adult female FAFB/FlyWire v783, annotations v3.1.0, original checksum-verified files.
Bilateral canonical MBON16/17, PPL104; all α′β′ KCs directly contacting these MBONs;
actual cholinergic ALPN inputs to those KCs; connected APL; MBON13 (α′2 control);
MBON17-like and MBON28 (ambiguity/boundary audit). Bilateral selection is necessary
because observed MBON↔PPL104 connections cross the midline. No strength threshold.
Keep every observed selected-to-selected contact, including minor neuropil rows.
Count all omitted proofread input/output contacts, per cell and role. Unproofread
fragments, gap junctions and volume transmission remain outside this denominator.
No DPM expansion: this short-exposure mechanism does not establish it as necessary.

## Computational model (all numerical parameters are assumptions)

Independent rate model, float64, dt 0.01 s, fast tau 0.05 s, KC threshold 0.15,
eligibility tau 0.5 s. Baseline strengths proportional to contacts divided by ALL
proofread input contacts at each target; omissions are silent, not redistributed.
PN→KC gain 3; KC→MBON/APL gain 1; APL→KC inhibitory gain 1; cholinergic MBON→DAN
gain 0.1; other known cholinergic fast recurrence 0.05. Dopamine has no fast sign.
These conservative, fixed numerical scales reuse conventions, not fitted Stage-1
parameters or a calibration to Stage-2 outcomes. Stage-1 code is never edited.

Plasticity exists only at anatomical KC→canonical α′3 MBON neuropil rows.
Dopamine gate is actual PPL104→that MBON contact-weighted activity; denominator is
intact PPL104 contact total and never changes after lesions. No imposed dopamine,
novelty, reward, familiarity, presentation count or identity labels enter the model.
Effective efficacy m obeys dm/dt = -0.08 * KC_eligibility * DA * m + (1-m)/1800.
Bounds [0.1,1]. Recovery is an explicitly hypothesized phenomenological relaxation,
not a fitted reproduction or a demonstration of the biological recovery mechanism.
No dopamine-only forgetting term: the evidence does not fix its quantitative form.
A zero-threshold DA gate avoids inventing an absolute physiological DA threshold.
All noncanonical KC outputs remain fixed. No baseline conductance renormalization
following any lesion. State persists as per-edge efficacies, rates, eligibility,
logical time and PRNG; no cue-specific table exists in the neural model.

## Protocol and predeclared comparisons

Seeds 2701, 2702, 2703; A/B reversal for each. Equal cardinality, disjoint PN current
patterns sampled without looking at responses (5% of available PNs, amplitude 1).
Baseline probes run from disposable copies of the initial snapshot: they cannot
familiarize the actual preparation. Ten 1 s pulses, starts 0,7,...,63 s; stop at
70 s. No teaching input. Probe each cue independently for 1 s, mean last 0.5 s;
retain raw per-neuron rates and within-probe plasticity, not only normalized scores.
Readout: canonical α′3 MBON mean. Depression D=1-post/baseline; specificity D_A-D_B.
Baseline >1e-8 required. Also compare each MBON, PN/KC and α′2 responses.

Essential controls in both cue directions: freeze all plasticity; silence both
PPL104; remove PPL104→MBON modulation contacts; cut canonical MBON→PPL104 fast
feedback; silence two MBON13 (matched two-neuron, different-compartment lesion);
remove PN→KC; remove KC→canonical MBON; shuffle PN→KC weights ONLY over existing
contacts at each KC; remove APL; remove four ambiguous partners; one-pulse control;
sham with zero presentations. Matched lesions are matched in count, not anatomical
centrality or transmitter. Sensory specificity is assessed at PN/KC as well as MBON.

Restore original snapshot; separately clear fast rates/eligibility and keep m;
compare cue-only recall. Exact deterministic replay from serialized initial state
and numeric timestamped currents. Fresh-process recall must not load training
labels, prose, results, or episodic records. Compatibility tolerance 1e-10; expect
bit identity on this pinned environment. Save genuine sampled rates and plasticity.

Recovery probes at 0,300,1200,3600 s after fast reset, using exact zero-activity
relaxation of m. Explicitly an isolated silent-preparation recovery assay; not a
claim that an intact awake fly has zero internal activity. Validate the analytic
idle update against direct integration. Recovery is measured, but positive recovery
under this rule is not independent evidence for its biological correctness.

One-factor sensitivity (both cues, seed2701): eta×0.5/2; all fast gains×0.75/1.25;
KC threshold 0.10/0.20; feedback gain 0/0.2; dt 0.005; recovery tau 900/3600 s;
APL gain 0.5/2. Boundary brackets: normalize by retained total inputs; separately
normalize per retained presynaptic role (Stage-1-like). These optimistic brackets
must not replace the conservative full-input primary. No tonic/noisy external
currents to compensate for omissions. These tests cannot bound arbitrary missing
odor-driven inputs: severe DAN boundary loss limits any positive conclusion.

## Reward/familiarity distinction

The selected α′3 circuit is not an established appetitive teaching circuit. Do not
label PPL104 injection as reward. Compare to the frozen Stage-1 α1 model in a
separate assay: a 2×2 of prior sensory exposure (0 vs 10 pulses) and identical cue
presentation with/without its PAM11 teaching current, counterbalanced A/B. Retain
Stage-1 model/parameters unchanged; all new outputs stay in Stage 2. Compare
unreinforced α1 plasticity to Stage-2 α′3 plasticity. This tests separate mechanisms
in separate preparations, NOT orthogonality/coupling in one brain. Reinforcement
also presents the cue: call the arm low-exposure, not literally unseen+reinforced.
Do not invent cross-compartment connections. Biological interactions remain open.

## Decision rule

A narrow modeled familiarity PASS requires every primary cue/seed to have D_paired
≥0.05, specificity ≥0.03, unseen depression ≤0.02, neural-state recall after fast
reset, original restoration and replay within tolerance. Mechanism disruptions
must reduce specificity ≥80% while PN/KC responses stay within 10%; matched lesion
must preserve ≥75% of intact specificity. Baseline activity alone is not learning.
Sensitivity must preserve direction without relying on optimistic boundary
normalization. Report all effects, including tiny ones and failed comparisons.

PARTIAL-INCONCLUSIVE if a persistent local effect exists but is too small,
parameter/boundary dependent, or physiological identity/drive is insufficiently
constrained. FAIL if state/causal dependence is absent or the implementation cannot
satisfy the memory criterion. A complete neural behavioral/sensory fly model is
not claimed even for PASS. GENESIS MAPPING: none. Stop after Stage 2 review.
