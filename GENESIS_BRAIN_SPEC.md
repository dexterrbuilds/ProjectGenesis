# Project Genesis Biological Neural Specification v0.1

**Status: evidence specification for review. No common fly kernel is approved.**

Version: **0.1.0**. This document synthesizes frozen research; it does not introduce a biological experiment, change a model, implement BrainAdapter, or activate Genesis. The C. elegans adapter remains the existing implementation. The Drosophila preparations remain isolated research models.

The machine-readable release is [RELEASE.json](research/genesis-brain-spec-v0.1/RELEASE.json). Its registry SHA-256 is:

`6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e`

The [evidence index](research/genesis-brain-spec-v0.1/EVIDENCE_INDEX.md) lists all 151 entries. The registry contains 27 scoped claims, 25 population views, 19 connection-class views, 65 historical parameter/operator records, 11 capabilities and four quantitative result summaries. It also preserves 25 literature records/collections with preparation and transfer limitations. [Mechanism profiles](research/genesis-brain-spec-v0.1/MECHANISM_PROFILES.json) provide a content-addressed index across these records; they introduce no new physiological assignments.

## 1. What the completed studies establish

| Frozen study | Classification | Permitted conclusion |
|---|---|---|
| [Stage 1](research/fly-stage1/REPORT.md) | **PASS** | Narrow appetitive association is causally implemented in the specified connectome-constrained computational model. The aversive counterpart remains inconclusive. |
| [Stage 2](research/fly-stage2/REPORT.md) | **PARTIAL-INCONCLUSIVE** | A persistent, stimulus-specific model effect exists, but is extremely small and assumption-sensitive. Behavioral familiarity/novelty is unvalidated. |
| [Stage 3](research/fly-stage3/REPORT.md) | **PARTIAL-INCONCLUSIVE** | Small selective resource modulation and local experience effects exist. Persistence, withdrawal and abstention are unestablished. |
| [Boundary/architecture](research/fly-boundary-study/REPORT.md) | **INSUFFICIENT EVIDENCE** | Restoring anatomy does not by itself identify useful functional participation or select an architecture. |
| [Physiology](research/fly-physiology-study/REPORT.md) | **PARTIAL PHYSIOLOGICAL CONSTRAINT** | Some experimental constraints are available; they do not identify a common numerical physiological kernel. |
| [Representation](research/fly-representation-study/REPORT.md) | **INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION** | Local APL responses require more than the tested shared scalar representation. This does not select a representation for all neurons. |

The shortened representation label “INSUFFICIENT EVIDENCE” refers to the last row; the registry retains the full frozen classification. These are historical results, never writable status fields for a later experiment.

### Quantitative limits that must travel with the claims

- **Stage 1:** six counterbalanced primary conditions; mean paired depression **51.12%**, control **8.88%**, selectivity **42.25 percentage points**. Plasticity freeze, PAM11 silencing, removal of the modeled DAN→KC route, and temporally unpaired teaching each remove selectivity while preserving basic sensory response. Snapshot restoration returns baseline; fast reset preserves learning within `1e-10`. Strength shuffling preserves learning: this does **not** establish unique necessity of the exact fly weight distribution.
- **Stage 2:** repeated-cue suppression about **0.001376–0.004555%**, against a **5%** criterion; specificity about **0.001376–0.004266 pp**, against **3 pp**. Persistence in plastic state does not rescue failed magnitude criteria.
- **Stage 3:** MBON11 resource contrast **0.04958433–0.118655429%**, against **10%**; local experience change **0.0238223752–0.0605364741%**, against **5%**. Learned-value × resource interaction is approximately **1.74×10⁻⁶% / 2.27×10⁻⁶%**. OA stimulation suppresses MBON11 but slightly increases MBON18/LH output; it does not demonstrate disengagement.
- **Boundary study:** normalization and transmission assumptions can affect results substantially more than anatomical expansion. Neither the largest network nor the strongest normalization-dependent effect is selected as biological truth.

These are model conditions and responses, not samples of flies or evidence of conscious preference. Exact definitions, intervention matching and unrounded evidence remain in the frozen reports.

## 2. Five categories; no implicit promotion

| Category | Meaning | Example / restriction |
|---|---|---|
| **BIOLOGICAL FACT** | Observed anatomy or experimentally supported observations within a stated preparation | KC cholinergic machinery in tested preparations; a pinned FlyWire contact count. Does not imply root-specific conductance. |
| **EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION** | A limited representation predicts independent biological measurements within its stated observation model | Local APL spatial fluorescence representation. Does not identify APL→KC conductance. |
| **HYPOTHESIS** | A candidate mechanism, sign, representation or transfer requiring evidence | Net positive MBON07→PAM11 transmission; transferable numerical compartment rules. |
| **ENGINEERING ASSUMPTION** | Numerical choices, boundaries, schemas, synthetic stimulation, or facts about a computational implementation | A 50 ms rate time constant; the demonstrated Stage-1 model mechanism; canonical state ownership. Model validation alone does not convert these to experimentally supported physiology. |
| **GENESIS PRODUCT MAPPING** | An interpretation between a digital world and a biological/model quantity | A possible future financial-runway/resource analogy. It is not part of the biological experiments and is not authorized for implementation here. |

Category and evidentiary status are independent fields. An engineering model can pass its computational causal test while its numerical physiology remains unconstrained. A biological fact can have limited preparation compatibility. A population record's fact category describes anatomical membership; its physiological facets explicitly reference separately categorized claims or remain unknown.

### Unknown is not zero

Unknown quantities use a tagged object, for example:

```json
{"state":"unknown","value":null,"reason":"No target-specific receptor measurement","evidence_refs":[]}
```

A historical `boundary_current=0` is a **declared model boundary**, not evidence of physiological silence. A measured zero in an intervention result is a scoped observation. A zero anatomical row count means no retained row in this pinned union, not absence of all chemical, electrical, peptide or volume transmission. Zero and unknown have different meanings throughout the specification.

## 3. Biological identities and ownership

The pinned data describe **adult female FAFB/FlyWire v783**, with annotations **v3.1.0**. The annotation hash, extraction hashes, source table hash and type/root crosswalk are retained in the registry. Root IDs remain decimal **strings**.

| Preparation | Neurons | Directed pairs | Pair/neuropil rows | Anatomical contacts |
|---|---:|---:|---:|---:|
| Stage 1 | 1,054 | 80,423 | 102,889 | 226,143 |
| Stage 2 | 1,172 | 57,804 | 73,715 | 160,848 |
| Stage 3 | 4,563 | 304,192 | 375,699 | 905,536 |

The existing [canonical identity registry](research/fly-representation-study/IDENTITY_SCHEMA.md) is referenced, not copied into a second anatomy owner:

- **5,480** unique biological root identities.
- **449,600** canonical aggregate connection rows, containing **1,056,073** contacts in the **union of extracted rows**. This is not a newly induced union connectome.
- **4,622 KC→MBON07** and **1,053 KC→MBON11** shared rows retain their existing single canonical IDs.
- No root-specific physiological rule is assigned by deduplication.

The source supplies aggregate rows, not individual contact IDs. A row key hashes dataset/version, pinned source hash, pre/post neuron keys and neuropil. A row with ten contacts is not ten invented canonical contact records. Neuropil labels such as `MB_VL` do not individually identify α1, α2, α3 or α′ compartments. Any finer assignment requires separate localization evidence.

One biological neuron may own multiple justified local states. Voltage, calcium, release, biochemical state and receptor modulation are distinct observables/state kinds. A local-state partition is versioned evidence; it is not another neuron. Intracellular coupling is not an EM chemical edge and must not inflate anatomical contact counts.

## 4. Current circuit and physiological boundaries

| Population / pathway | Supported constraint | Unresolved or prohibited inference |
|---|---|---|
| PN→KC | Coactive claws, sparse nonlinear responses, preparation-specific electrophysiology/calcium evidence | Contact multiplicity is not claw count. No identified dimensionless PN gain or universal sparsity percentage. |
| KC→MBON | Cholinergic machinery and nicotinic receptor dependence in tested targets | No universal contact→conductance conversion or identical target kinetics. Automated transmitter predictions do not override stronger class evidence. |
| KC↔APL | Local inhibitory circuit effects; heterogeneous spatial responses | A single shared scalar fails the audited APL assay, but calcium coefficients are not voltage coupling or inhibitory conductance. |
| PAM11 / α1 / MBON07 | Type-level anatomy; narrow Stage-1 associative mechanism works computationally | Biological eligibility, learning rate, exposure scale and efficacy floor are not identified. Stage-1 PASS does not calibrate them. |
| PPL101 / γ1pedc / MBON11 | Compartment-specific conditioning and state-related experimental observations | Direct DAN→KC and DAN→MBON count-normalized exposure are competing approximations. No common acute/persistent update rule is identified. |
| PPL104 / α′3 / MBON16/17 | Repetition, recovery and postsynaptic receptor evidence in functional studies | Driver membership is not exact root identity. The Stage-2 model does not establish behavioral novelty. α3/MBON14 is not α′3. |
| MBON18, LH, LHCENT | Anatomical paths and specific response observations motivate candidates | Missing inputs/outputs and uncertain aliases limit functional interpretation. No validated downstream pursuit/withdrawal decoder. |
| OA-VPM4→MBON11 | VPM4 activation suppresses MBON11 response in the tested assay | No root-resolved receptor map, universal inhibitory OA sign, dose curve or measured gain of one. |
| dNPF / NO / endocrine pathways | State and memory experiments establish relevant physiological mechanisms | Chemical edge counts do not provide peptide/receptor wiring, diffusion or kinetic parameters. Missing chemical edges do not imply absence. |
| MBON07→PAM11 | Anatomy and NMDA requirement motivate feedback | Direct net excitation remains a hypothesis. Antennal-lobe glutamate/GluCl evidence cannot assign the α1 target sign. |

For every population and connection view, the registry includes root selectors, evidence facets, sign unknowns, representation/locality constraints, timing, normalization, plasticity, parameter and observation limitations, compatibility, interventions, conflicts and wording boundaries. Mechanism profiles connect these views to their scoped claims. They do not use a type name to manufacture receptor or functional-compartment assignments.

### Parameters and observations

The **65** frozen parameter/operator assumptions are imported without changing values or classifications: **39 unconstrained, 16 weakly constrained, 7 product-boundary assumptions and 3 experimentally constrained**. The last three constrain class identity or tested inhibitory sign, not shared numeric gain. “Product-boundary” in the old audit denotes a synthetic preparation/body boundary, not a Genesis financial mapping; its registry category is engineering.

The numerical scale of a model rate is not automatically Hz, current, voltage, calcium fluorescence or transmitter concentration. Hige γ1pedc current depression constrains an integrated effect under that preparation; it does not separately identify learning rate, dopamine dose, eligibility duration and floor. It cannot numerically calibrate α1 appetitive learning by name association.

The global rate time constant, strength normalization, contact-to-efficacy conversion, resource gate, absent transmission delays and unknown modulatory effects remain explicit assumptions. Omitted physiology cannot be silently turned into measured zero transmission.

## 5. Representation: heterogeneous, with no selected common kernel

The representation study's original model-selection criterion remains unchanged.

| Candidate | Evidence position |
|---|---|
| R0: scalar point state | Not universally rejected; inadequate for the tested shared-scalar APL spatial observation model. Scalar electrical state can still coexist with local synaptic plasticity. |
| R1: local/compartment state | Supported for APL spatial response representation at the assay's resolution. Does not establish every neuron's compartment count or multiple voltages. |
| R2: target/receptor-aware effects | Necessary distinctions are supported in particular assays. No complete root-specific receptor/sign/kinetic assignment exists. |
| R3: conductance/biophysics | Some subtype-specific components are measured. Held-out evidence does not establish a common richer kernel or its superiority. |

In the frozen APL Figure 4 validation, shared-scalar MSE was **5.796135**; local zero-transfer MSE **0.007750565**; local shared-coupling **0.00831429**; directional coupling **0.00701383**. Figure 3's separate assay gave **1.444396**, **0.040157** and **0.036414** for shared-scalar, local zero-transfer and local shared-coupling respectively. These support locality, but coupling does not clear the **20%** material-improvement criterion over the local zero-transfer alternative. The shared coupling interval includes zero.

**Do not infer a nonzero coupling constant from the locality result.** Conversely, Figure 7's different spatial profiles prevent declaring universal biological disconnection. Do not transfer any fitted fluorescence coefficient to APL→KC conductance.

### Excluded temporal validation

The [MBON source audit](research/fly-representation-study/MBON_SOURCE_AUDIT.md) remains binding. The supplementary workbook's raw tau mean is **16.9825 ms**, versus reported **14.48 ms**, and a row matches original training values without resolved provenance. This is an unresolved discrepancy, not proof of duplication. The workbook is excluded from clean held-out validation until authoritative clarification. It cannot select a temporal model through a renamed evidence entry.

## 6. Shared physiological rules are not composable

The 4,622/1,053 shared rows remain single anatomical identities, with **unresolved physiological composition**. The [frozen conflict report](research/fly-boundary-study/UNIFIED_MODEL_CONFLICTS.md) and [physiology assessment](research/fly-physiology-study/UNIFIED_PHYSIOLOGY.md) identify:

- DAN→KC exposure in Stage 1 versus DAN→MBON11 exposure in Stage 3.
- A Stage-1 dopamine threshold versus different Stage-3 gating.
- No acute Stage-1 divisor versus Stage-3 `1/(1+D)` gating.
- Retained-role versus all-proofread-input normalization.
- MBON11 output gain **0.05 versus 1** on relevant shared outputs.
- Assumed positive MBON07 feedback versus omitted outputs in Stage 3.
- Active MBON07 learning versus frozen transferred efficacy.
- Independent eligibility/plastic states and clocks; no justified merged update law.

Alternative frozen preparations may retain separate experiment snapshots. They may not be composed as two simultaneous owners of one connection's efficacy in one model. Anatomy references can be shared freely; physiological ownership cannot. A new result must independently reconcile the required operator and state meanings. Adding software scores or combining incompatible update equations does not accomplish this.

## 7. Capability registry

| Capability | Current evidence status |
|---|---|
| Associative appetitive learning | **Validated narrowly within the Stage-1 computational model** |
| Familiarity/novelty | Candidate mechanism; behavioral interpretation unsupported |
| Resource-state modulation | Modeled causal modulation exists; persistence/withdrawal unsupported |
| Persistence | Unsupported |
| Withdrawal/disengagement | Unsupported |
| Voluntary abstention | Unsupported; silence is not a decision |
| General curiosity | Unsupported |
| Threat behavior | Not yet tested; the aversive-learning counterpart is not a threat-behavior assay |
| Sleep | Not yet tested |
| Arousal | Not yet tested |
| Consciousness/sentience | Unsupported and outside current evidence |

No approved decoder maps these unestablished capabilities onto digital actions. Unknown activity remains unknown activity.

## 8. Versioning, provenance and admission of future evidence

The registry and neuron annotation index are SHA-256 addressed under `research/genesis-brain-spec-v0.1/objects/`. Each entry has its own hash. Sources include path, hash, kind and section, with primary-source URLs and preparation details in the literature records. `SPEC_MANIFEST.json` pins the completed specification package, including this document and the supplemental profile object. SHA-256 detects content changes; it is not a digital signature or a filesystem write lock.

An experiment must declare the exact release digest and hashes of every evidence entry it uses. Its manifest accepts reference-only anatomy views and explicit unvalidated assumptions. It cannot write a capability status, override a classification, or silently assign a supported physiological sign. The example manifest is a **preflight example only**, with no executable experiment.

### Evidence updates are append-only

1. Retain every frozen entry and historical study classification byte-for-byte.
2. Add a new scoped claim with a new ID and explicit `supersedes` records containing old entry IDs, hashes and reasons.
3. Supply newly admitted, content-pinned independent evidence and a separate review record binding the new entry hash, preparation scope, reviewer, UTC time and rationale.
4. Validate the candidate as a new version. Old sources renamed under new IDs do not qualify as new evidence.
5. Publish a separately reviewed release. A future result does not rewrite what the earlier study concluded.

The validator cannot authenticate a person or adjudicate the truth of arbitrary scientific prose. The positive supersession test uses explicitly synthetic **test-only** evidence to test the contract; it is not admitted research. Human scientific review and control of release publication remain essential. No review/admission can itself authorize Stage 4 or Genesis integration.

### Required rejections

Checks reject unsupported capability/pathway promotion, category laundering, known sign without scoped provenance, unknown→zero substitution, stale/missing dependencies, numeric roots, duplicate canonical ownership, conflicting shared-rule assignment, product/hidden-answer inputs, renamed old evidence, and edits to frozen classifications. Rehashed adversarial fixtures exercise semantic rules rather than merely breaking a checksum.

## 9. Proposed heterogeneous runtime interface — documentation only

This is a future **research** interface proposal. It is not implemented and does not change `BrainAdapter`, current neural models or storage.

```ts
type EvidenceRef = { id: string; sha256: string };
type NeuronId = string;      // dataset/version + decimal FlyWire root string
type RowId = string;         // existing canonical aggregate-connection hash
type LocalStateId = string; // neuron + partition version + region + state kind
type EvidenceValue<T> =
  | { state: "unknown"; reason: string }
  | { state: "constrained"; value: T; units: string; evidence: EvidenceRef[] }
  | { state: "model-boundary"; value: T; units: string; assumption: EvidenceRef };

interface NeuronIdentity {
  id: NeuronId;
  rootId: string;
  annotationEvidence: EvidenceRef[];
}
interface LocalStateDefinition {
  id: LocalStateId;
  owner: NeuronId;
  partitionVersion: string;
  anatomicalRegion: EvidenceValue<string>;
  kind: "electrical" | "calcium" | "release" | "modulatory" | "biochemical";
  units: string;
  representationEvidence: EvidenceRef[];
}
interface ConnectionAssignment {
  row: RowId;                       // reference, never a copied anatomy owner
  preLocal: EvidenceValue<LocalStateId>;
  postLocal: EvidenceValue<LocalStateId>;
  transmissionOperator: EvidenceValue<EvidenceRef>;
  plasticityOperator: EvidenceValue<EvidenceRef>;
  stateOwner: string;               // unique per row/model-instance/state kind
}
interface ResearchSnapshot {
  evidenceRelease: string;
  anatomyHash: string;
  partitionHash: string;
  operatorHashes: string[];
  observationHashes: string[];
  logicalTime: number;
  prngState: unknown;
  neuralState: unknown;
  localModulatoryState: unknown;
  synapticPlasticState: unknown;
  bodyBoundaryState: unknown;       // explicitly modeled, never relabeled physiology
}
interface ProposedResearchKernel {
  initialize(specification: unknown): Promise<void>;
  stimulate(timestampedPhysicalOrDeclaredBoundaryInput: unknown): void;
  step(elapsedSimulationTime: number): void;
  observe(observationModel: EvidenceRef): unknown;
  getState(): ResearchSnapshot;
  snapshot(): ResearchSnapshot;
  restore(snapshot: ResearchSnapshot): void;
}
```

These `unknown` TypeScript payloads mark unresolved interface design, not arrays to initialize to zero. A future concrete schema must define units, dimensions, tolerances and ownership before execution. A compiler/validator would reject an unknown required transmission operator, unsupported partition, duplicate owner or conflicting shared rule. Unknown physiology may be represented as unknown; it must not become an executable invented constant.

DAN electrical activity, compartment modulation, local eligibility and persistent efficacy need separate semantics. Modulatory fields and intracellular coupling must have their own justified identities without becoming fabricated anatomical edges. Observations must declare whether they are rates, currents, spikes, fluorescence or release, and any conversion assumptions. A behavioral decoder would require separate validation; none is supplied here.

The interface permits later adaptation behind a generic BrainAdapter while leaving organism identity, memories and economics outside the neural kernel. That compatibility is a design aim, not authorization to integrate it.

## 10. What a future Stage 4 may assume—and must establish

**Stage 4 is not authorized or started by this specification.** When separately requested, it may rely on:

1. The pinned anatomy, root strings and canonical row identities, within their annotation/crosswalk uncertainty.
2. The narrow Stage-1 computational causal result, including its intervention and topology limitations.
3. The failed/partial Stage-2/3 interpretations and the unresolved architecture/physiology conclusions as constraints.
4. Local APL response representation for the audited assays, without inferred nonzero coupling or conductance.
5. Experimental compartment, transmitter/receptor and timing observations only within their audited preparations.

It must independently establish:

- **Capability and scope:** an operational neural/behavioral claim, independently justified circuit/root crosswalk and preparation compatibility. No output may be named persistence, curiosity, threat, sleep or arousal solely from a cell label or activity threshold.
- **Mechanism and physiology:** an appropriate observation model; parameter/sign/normalization evidence and explicit unknowns; eligible local targets; boundary losses and model uncertainty. No synthetic tonic rescue attributed to anatomy.
- **Causal acceptance:** preregistered thresholds before outcomes, appropriate counterbalancing, mechanism and matched controls, preserved unrelated responsiveness, deterministic replay and sensitivity. Anatomy, boundary drive, normalization and parameter changes must be separated.
- **State ownership:** if learning is claimed, persistent neural/plastic state must explain the result after fast reset and without external answers; pre-exposure restoration must reverse it. If composition is claimed, reconcile shared operators independently before assigning one physiological state owner.
- **Independent biological prediction:** held-out data where available; exclusions and preparation differences preserved. Genesis capability magnitudes cannot be physiological fitting objectives. No pseudo-calibrated replay.
- **Evidence governance:** release/entry dependencies pinned; new claims admitted explicitly. Prior studies remain frozen even if a later supported mechanism disagrees.

No numerical acceptance thresholds for an unspecified new capability are invented here. They belong in its prospective protocol. No LLM, product-state input, wallet, runtime integration or automatic life-cycle activation follows from passing a registry check.

## 11. Computation and preservation

The existing [scaling study](research/fly-representation-study/SCALING.md) measures its own documented recurrences. Full-reference R0/R1/R2 throughput was approximately **35.1 / 22.9 / 13.7 updates/s**, with R2 peak about **1,040.2 MiB**. These are not calibrated physiological benchmarks; multiple local/plastic variables invalidate blanket extrapolation from the older scalar benchmark. No new neural benchmark or model run was performed for this specification.

The specification verifies **3,848 protected files**, preserves the pre-interruption specification artifacts and references the existing canonical identity archive. A repeatable-read, read-only Postgres audit checks the unchanged canonical snapshot, seven decisions/life cycles and disabled schedule. The [completion audit](research/genesis-brain-spec-v0.1/VERIFICATION.json) records actual checks and test results.

This is local research infrastructure. Frozen source audits retain an unresolved upstream CC-BY/CC-BY-NC/annotation licensing discrepancy; this specification does not grant data redistribution rights.

**Stop for review. No new capability, common neural kernel, Stage 4 or Genesis integration is approved.**
