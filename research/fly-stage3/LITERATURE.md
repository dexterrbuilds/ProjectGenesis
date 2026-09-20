# Stage-3 crosswalk and evidence audit — 2026-09-17

## BIOLOGICAL FACT

**Sayin et al. 2019**: hungry flies sustain odor tracking without acquisition.
MBON11/MVP2 (MB112C), MBON18/α2sc (MB080C) and PPL1-γ1pedc contribute; OA-VPM4
(MB113C) suppresses MBON11 and tracking. MB22B labels VPM3 plus VPM4, so it is not
VPM4-specific. MBON11 peduncular responses decline with trials. MBON18 has onset
and offset responses, with no significant trial-number effect in that imaging assay.
The authors explicitly note tension between an inhibitory MBON11→MBON18 connection
and some behavioral/earlier imaging results. Their reduced model uses recurrence
and fitted transforms; this does not establish a FlyWire-root-specific motor decoder.
Our experiment does not reuse those fitted activity-to-running transforms.
https://pmc.ncbi.nlm.nih.gov/articles/PMC6839618/ (doi:10.1016/j.neuron.2019.07.028)

**Krashes et al. 2009**: dNPF-neuron activation promotes appetitive memory expression
in fed flies; dNPF receptor in a dopaminergic population is implicated. Blocking
that population releases expression, activation suppresses it. This is not a
connectomic map of peptide source cells or a concentration-response curve.
https://pmc.ncbi.nlm.nih.gov/articles/PMC2780032/ (doi:10.1016/j.cell.2009.08.035)

**Tsao et al. 2018**: PPL1-γ1pedc signaling and MBON-γ1pedc>αβ participate in food
seeking; hunger inhibits this DAN pathway and enhances the corresponding MBON odor
response. DAMB signaling and receptor knockdowns support modulation; the authors
explicitly leave precise upstream peptide neurons and receptor localization open.
Different MBONs change in different directions. No universal brain activity gain
or universal dopamine reward signal follows from these results.
https://elifesciences.org/articles/35264

**2024 reinforcement study**: chronic hunger can preserve/enhance aversive learning
through AKH-dependent input compensation despite motivational inhibition of DANs.
Thus the isolated resource gate below cannot describe all PPL101 functions, shock
processing or hunger compensation. None of these extra hormone pathways is invented.
https://pubmed.ncbi.nlm.nih.gov/38795709/ (doi:10.1016/j.neuron.2024.04.035)

**Dolan et al. 2018; Bates et al. 2020**: MBON-α2sc has LH partners integrating learned
and olfactory input; PD2a1/b1 and LHCENT1 are relevant convergence/feedback candidates.
https://pmc.ncbi.nlm.nih.gov/articles/PMC6226615/
https://pmc.ncbi.nlm.nih.gov/articles/PMC7443706/

**Li et al. 2020**: the MB network includes feedforward inhibition and deprivation-
sensitive configurations; volume peptide/amine modulation is not fully specified
by its chemical connectome. These omissions must remain explicit.
https://elifesciences.org/articles/62576

## Root-level crosswalk, not functional recordings of each root

v783 plus v3.1.0 annotations (pinned source hashes in manifest):

| Literature/type | Roots (strings) | Ontology |
| --- | --- | --- |
| PPL1-γ1pedc / MP1 → PPL101 | `720575940617691170`, `720575940621040737` | FBbt_00100243 |
| MVP2 / γ1pedc>αβ → MBON11 | `720575940617749538`, `720575940623201833` | FBbt_00100246 |
| α2sc → MBON18 | `720575940624539284`, `720575940622997453` | FBbt_00110101 |
| OA-VPM4 | `720575940636574388`, `720575940625264457` | FBbt_00110152 |

VFB corroborates the MBON roots and the shared OA-VPM4 ontology linking the original
FAFB tracing to current annotations:
https://www.virtualflybrain.org/term/mbon11-vfb_fw035279/
https://www.virtualflybrain.org/blog/2022/01/01/mbon18-vfb_fw036312/
https://api.virtualflybrain.org/docs/tutorials/apis/connectome/1_discovery/

PD2a1/b1 **are not current cell_type labels**. Select their hemibrain_type aliases
LHPD2a1/LHPD2b1, preserving divergent current CB classes individually. Treat this
one-to-many mapping as uncertain, not as exact driver membership. VFB independently
links CB2977 to LHPD2a1 at root `720575940615975474`:
https://www.virtualflybrain.org/term/lhpd2a1-vfb_fw017867/

PPL101 annotation also records nitric oxide co-transmission. Neither its kinetics
nor a peptide/receptor graph can be read from edge counts; these are omitted. No
NPF-named neuron is selected by name and declared a causal peptide source.

## COMPUTATIONAL MODEL / GENESIS MAPPING

Resource-to-PPL101 modulation is a **body-boundary approximation** supported only
in direction, not in dose, time scale or exact source. It is not biological starvation.
The model's local dopamine response, OA sign and strength assumptions are tested,
not inferred from transmitter labels alone. See PLAN.md before interpreting outputs.
**GENESIS MAPPING: none.** No financial, task-quality or decision inputs are used.
