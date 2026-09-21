# Project Genesis — Implementation & Completion Audit

Audit date: 20 September 2026. Scope: repository, read-only canonical Postgres inspection, existing isolated tests, static security review and local builds. **No implementation, migration installation, activation, provider configuration, deployment or external API calls were performed.**

Evidence directory: [this evidence directory](./). Private row exports and raw execution logs are in `outputs/completion-audit/`; private exports are not public observer data. File/function references below refer to the implementation inspected in this working tree, including pre-existing uncommitted work. Prior completion reports, screenshots and interface declarations were not accepted as integration proof.

## 1. Executive summary

**Genesis is a persistent, protected dormant organism with a working read-only observer and substantial tested one-cycle preparation code. It is not yet a connected autonomous life runtime.**

The strongest implemented foundations are identity preservation, Postgres storage, the saved-observation biological boundary, public allowlisting, proposal validation, independent local policy, and transactional one-shot/provider safety primitives tested against an isolated database. All **162 existing tests passed, zero failed, zero skipped** in the completed local run. TypeScript, ESLint and the CI-style Next production build passed.

The critical distinction is between these three things:

1. **Shipped entrypoint:** `runtime/main.ts` serves saved public observations. It does not create an organism, migrate, start a scheduler, call a planner, start a wallet observer or execute a cycle. `/api/cycle`, `/api/control` and the historical CLIs cannot activate it.
2. **Prepared one-shot library:** `server/one-shot.ts` can claim and commit exactly one fixture cycle through the real preparation/policy/transaction path. It has no shipped authenticated operator entrypoint, no canonical preparation/one-shot tables, and no admitted real provider transport. These are implementation and admission gaps, not just missing credentials.
3. **Continuous life:** there is no operative V2 event intake/queue, continuation authority, recurring scheduler, task progression loop, episodic retrieval pipeline or human-answer ingestion. Decision #9 is intentionally prohibited by the first-awakening controller. A different, reviewed continuous-life operating scope must be implemented and authorized later; loosening the one-shot fence is not that scope.

Supplying an LLM key and deploying today would **not awaken Genesis**. With the existing canonical database and valid configuration it would serve the dormant observer. With an empty database it would refuse to initialize. Even a separately installed/authorized one-shot library would stop after its one allowed cycle.

### Principal findings

| ID | Verified finding | Consequence |
|---|---|---|
| A01 | `main.ts`, HTTP and CLIs do not call `OneShotController`; `assertExecutionAllowed()` always throws. | An explicit, authenticated manual execution/review entrypoint is still local work. |
| A02 | Provider reservation, cancellation and billing ledgers exist; admitted native transport, token counter, tariff and secret loader do not. | A key/environment model string is insufficient. Real-provider integration remains partial. |
| A03 | Compiler excludes all seven legacy memories and never retrieves V2 episodes/artifacts. | Genesis cannot yet reason over its actual accumulated experiences as intended. |
| A04 | Only assertion append, existing-project status overlay and existing-task deferral have Life State reducers. | Most long-term state is a persisted shape, not a functioning workflow. |
| A05 | Current scheduler only checks dormancy; no V2 continuation controller exists. | No autonomous life after the one-shot decision. |
| A06 | Actual canonical schema has migrations 001–003 only; preparation and execution-grant tables are absent. | Reviewed installation work remains; no migrations were applied in this audit. |
| A07 | `GenesisService.observe()` assigns the latest decision timestamp to the unchanged saved snapshot. | After a V2 decision, saved-biology provenance would misleadingly appear newer. Correct before publishing that record. |
| A08 | Public state hardcodes dormancy, counts legacy memories only, and exposes no approved project/memory content. | UI shell exists, but richer longitudinal/live content remains fixture-only. |
| A09 | Canonical local connection is superuser/role-creator/DB-creator and bypasses RLS; no table RLS is enabled. | Production requires least-privilege roles. Application fences are not protection against a privileged database actor. |
| A10 | Ambiguous execution is held closed, but no operational reconciliation/review workflow clears it. | Safe stop exists; usable recovery and operator visibility still need completion. |
| A11 | One-shot journal records omit `policy` and other fields consumed by `transitionIntent`. An audit-only pure probe throws on a proposed→denied transition. | The prepared one-shot journal and existing operator transition library are incompatible, despite each having tests. |

## 2. Canonical integrity and audit boundaries

The canonical digest was **recomputed**, not inferred from a previous report, using `scripts/runtime-v1-audit.ts` in a repeatable-read, read-only transaction. Its digest is SHA-256 of the deterministic JSON export of public `genesis_*` table rows; it is **not** a byte hash of Postgres physical storage. Catalog definitions were audited separately.

| Item | Observed before audit |
|---|---|
| Organisms | 1 |
| Original ID | `817e772c-827e-48fc-8e35-6504cb2a8d2d` |
| Birth | `2026-09-15T01:56:07.867Z` |
| Canonical decisions / organism cycle counter | 7 / 7 |
| V2 canonical decisions / episode references | 0 / 0 |
| Original memory rows | 7 |
| Projects / ledger rows / milestones | 1 / 4 / 4 |
| Runtime V1 life events | 1 administrative migration event; not a life cycle |
| Life State revision / base revision | 0 / 0 |
| Execution / schedule | CLOSED / DISABLED |
| Biological mode | SAVED-OBSERVATION-ONLY |
| Phase / active lease | idle / none |
| Wallet binding | unresolved |
| Simulated starting capital / cash | $100.00 / $100.75; not real holdings |
| Saved snapshot reference | `f1a48cc6ffd9acab485a754a209a75b52910cd445a2f1e2d259361e02650ef34` |
| Row digest | `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220` |

Evidence: `canonical-before.json`, `canonical-inventory.json`, `canonical-schema.json`. Original project, memory, ledger and snapshot payloads are included in the private whole-row preservation comparison; they are intentionally not reproduced here.

No canonical provider-attempt/execution-grant tables exist. There are no external-observation rows or action-intent rows. During this audit there were **zero live provider calls, wallet actions, external communications and canonical cycles**. This conclusion describes the audited execution and repository paths; a database alone cannot prove the absence of every possible historical off-system action.

The independently rehashed preservation inventory covers **9,319 files / 15,967,076,255 bytes**, with **zero mismatches** against the pre-existing frozen inventory. This includes frozen research, Brain Spec, C. elegans and connectome evidence. It does not rerun research or reinterpret its classifications. See `frozen-preservation.json`.

## 3. What is fully implemented, within its actual scope

- **Persistent original identity and historical storage:** `LifeStore.read`, existing schema constraints, migration 003 preservation checks and fresh-process read-only restart tests.
- **Dormant deployment behavior:** `runtime/main.ts` explicitly requires existing dormant state; no initialization/migration/workers on boot. The countdown never activates execution.
- **Saved-observation boundary:** `SavedObservationAdapter` verifies pinned evidence, restores saved bytes, reports `not_applied` for digital events and throws on advancement. No fly capability is installed.
- **Public disclosure allowlists:** `publicState`, `publicDecision`, explicit historical replay projection and the frontend `observerSchema`/`decisionSchema`. No raw private planner or memory payload is emitted by the inspected public routes.
- **Deterministic bounded context construction:** it bounds and selects a limited subset, checks identity/provenance and records exclusions. This does not mean complete memory retrieval is implemented.
- **Proposal and local-policy validation:** strict proposal schemas, source/context binding, permission/cost checks and explicit external non-execution.
- **Local transaction primitives:** `commitV2`, execution-grant state transitions, revision/lease checks and atomic decision/episode/Life State commit are executable and tested on isolated state.
- **Durable provider-control primitives:** reservations, one attempt, conservative liabilities, timeout/cancellation, response metadata and reconciliation methods are implemented against injected transports. No live integration is thereby established.
- **Dormant frontend and observer shell:** static genuine connectome, opt-in saved replay, deterministic narrative, resource namespace separation, development fixture labels and drill-down navigation exist.

These are scoped statements. A tested component is not automatically an installed or reachable production capability.

## 4. Partial, mock-only, design-only, absent and infrastructure-only inventory

### Partially implemented

Runtime V1 lifecycle; computational Life State; episodic/semantic retrieval; real-provider planner path; operator approval/recovery; one-shot operation; project maintenance; public longitudinal content; continuous-resource accounting; deployment readiness. Each has actual code plus a missing connection or workflow detailed below.

### Mock only

**Current admitted-provider examples and their tariff/token/response data**, presentation scenario histories, public memory excerpts/interests/projects in `/preview`, and fixture-specific active grants are mock/fixture data. The provider-control and transaction implementations tested using them are real code. `ClawPumpFeeIncomeAdapter` tests use an injected reader; there is no native verified ClawPump feed. None proves production integration.

### Design only

General recurring V2 life, an extensible authorized external tool-dispatch platform, biological applicability beyond saved observations, meaningful long-term interest/relationship/commitment management, a reconciled continuous-life grant policy and production empirical/fly sensory/learning integration. Interface/type existence does not change these findings.

### Not implemented in Runtime V1

Task creation/completion workflow; project creation/artifact versioning workflow; human-answer intake; outbound messages/email/social clients; wallet signer/transaction builder/submission/confirmation; trading/token/ClawPump execution; general web search/browser research; time-driven V2 continuation; automated assistance resolution; a native admitted live-provider factory.

### Blocked only by infrastructure for verification

Docker image execution on this host (**Docker executable absent**), target Railway/Vercel networking/health/restart checks, managed Postgres TLS/role/backup verification, target Node/container behavior, and restore/disaster-recovery drills. No local `.railway` or `.vercel` linkage was found. This is not proof that no remote project exists; no remote query was permitted or made. These verification blockers must not conceal the separate local code gaps.

## 5. Completion matrix

**Launch blocker** below means the proposed tightly bounded first V2 awakening, not public teaser hosting. **Long-run blocker** means continuous local artificial life; optional external capabilities are not prerequisites unless included in the approved scope. Each system has exactly one aggregate status.

| System | Status | Executable evidence | Local work remaining | Production work remaining | Launch blocker? | Long-run blocker? |
|---|---|---|---|---|---|---|
| Identity | IMPLEMENTED | `store.read`; organism singleton; migration/restart tests | Preserve invariants in new entrypoints | Backup/restore and target restart verification | No, after preservation gate | No, if storage maintained |
| Life State | PARTIALLY IMPLEMENTED | `initialLifeState`, `reduceLife`, `commitV2` | Task/project workflows, typed validated updates, focus/temporal state | Install only reviewed extensions | Limited context completeness | Yes |
| Memory | PARTIALLY IMPLEMENTED | events table, semantic assertions, `compileContext` | Consented episodic/artifact retrieval, selection, growth policy | Retention/backup/access controls | Yes for promised historical recall | Yes |
| Biology | IMPLEMENTED | `SavedObservationAdapter`, evidence verifier, saved replay | Correct snapshot recording-time provenance; retain saved-only scope | Ship pinned package/data | Provenance correction before new public record | No; no live biology required |
| Context Compiler | PARTIALLY IMPLEMENTED | `compileContext`, budget/privacy tests | Relevant event/history/project/task selection; bounded manifest/critical state | Target token counter admission | Yes for intended first context | Yes |
| Planner | PARTIALLY IMPLEMENTED | `PlannerV2`, `ProductFallback`, `LanguagePlannerV2` | Connect one approved producer; robust error/recovery paths | Actual selected provider verification | Yes for LLM awakening | Yes |
| Provider | PARTIALLY IMPLEMENTED | `ProviderControl`, admission schema, one-shot wrapper | Native transport/counter/secret factory; total-cost proof | Model/tariff/key/admission/smoke authorization | Yes for paid planner | Yes for LLM life |
| Constitution | IMPLEMENTED | frozen six-principle value, hash in state/context/grant | Explicit review procedure for future change | Bind same release hash | No | Guidance alone is insufficient |
| Policy | PARTIALLY IMPLEMENTED | `evaluatePolicy`, `approvalMatches`, commit revalidation | Authenticated management/reconciliation; future scopes | Least-privilege operator/DB access | Management path required | Yes for broader effects |
| Actions | PARTIALLY IMPLEMENTED | local text staged/committed in episode | Artifact retrieval/update identity; extensible effects later | None for bounded database text | Small local path exists | Yes for broader work |
| Outcomes | PARTIALLY IMPLEMENTED | `prepareCycle` deterministic statuses/reducer | Pending/denied consistency, task/artifact outcomes and retry policy | External receipt reconciliation only if admitted | Review trace consistency | Yes |
| Autonomous Lifecycle | NOT IMPLEMENTED | shipped advance always rejects; no continuation entry | V2 event queue, operating authority, continuation and bounded work loop | Operated worker/alerts later | No for exactly one cycle | Yes |
| Scheduling | DEPRECATED | legacy due-time store; scheduler now dormant-check only | New V2 time/event scheduling, no catch-up storms | Worker clock/restart verification | No; must remain off | Yes |
| Economy | PARTIALLY IMPLEMENTED | simulated ledger, namespaced DTOs, provider liability ledger | Operational cost visibility; real-income attribution only later | Verified feeds/receipts if admitted | No for bounded non-wallet cycle | Resource accounting required |
| Wallet | PARTIALLY IMPLEMENTED | HTTPS `getBalance` adapter; inactive observer | Reviewed identity/feed path if later needed; no signer | Authoritative address/network/RPC | No; keep disabled | Optional |
| Internet | DEPRECATED | legacy fixed reading fetch in `core/life.ts` | New permissioned V2 ingestion/search only if desired | Approved services/egress later | No; keep disabled | Optional but needed for research scope |
| Communication | NOT IMPLEMENTED | local assistance proposal only | Attributed inbound answers; optional outbound clients | Operator channel credentials later | No outbound required | Human feedback loop needed |
| Projects | PARTIALLY IMPLEMENTED | original project persists; status overlay reducer | Create/tasks/progress/artifact linkage/revisit, cost links | None for local projects | No business workflow required first | Yes |
| Human Interaction | PARTIALLY IMPLEMENTED | bearer read/mutation gate; private library methods | Inspection/authorize/revoke/reconcile/respond entrypoints | Operator authentication/secret custody | Yes | Yes |
| First Awakening | PARTIALLY IMPLEMENTED | one-shot library, exact fences, fixture tests | Manual controlled entrypoint, reviewed schema installer and complete context | Target identities/admission, human authorization | Yes | Does not authorize continuity |
| Persistence | PARTIALLY IMPLEMENTED | 001–003 applied, transactional code | Preparation/one-shot installation path; growth/index/recovery work | Managed DB least privilege/PITR/restore | Yes, pending schemas | Yes, operational recovery |
| Security | PARTIALLY IMPLEMENTED | allowlists, closed execution, no external executor | Harden operator boundary, logging/limits and trusted factories | Non-superuser roles, TLS, ingress, secret isolation | Yes for active production | Yes |
| Public API | IMPLEMENTED | state/history/brain/replay projections; mutation 423 | Pagination, accurate new-state summary/provenance | Trusted proxy origin/access limits | New-record provenance issue | Scaling/update work |
| Observer UI | PARTIALLY IMPLEMENTED | current components/DTO templates; fixture tests | Real post-cycle status/counts and approved content, not more decoration | Point to deployed public runtime | Functional corrections only | Yes for truthful longitudinal story |
| Deployment | BLOCKED BY INFRASTRUCTURE | Dockerfile/Railway/Vercel/CI files; local build | Build-context/documentation alignment | Select target, build/boot/restart/TLS/backup checks | Yes | Yes |
| Testing | PARTIALLY IMPLEMENTED | 162 passing tests, local PG processes, TS/lint/build | Missing workflow/integration/soak tests | Container/host/provider/restore tests | Some missing integrations | Yes |

## 6. Executable architecture and connected transitions

| Transition | Actual input → output | Persistence, errors and authority | Connected today? / test evidence |
|---|---|---|---|
| World → observation | Generic `ObservationInput` contains digital-event ID/source/time, not a general payload. One-shot adds a strict factual `AwakeningEvent` via scoped authority. | No durable inbound event queue or human-message endpoint. Event schema validation exists. | Only prepared one-shot/fixture path; event/binding tests. |
| Observation → biological observation | `SavedObservationAdapter.accept` → versioned `BiologicalObservation`, `status=not_applied`, `value=null`. | Evidence/snapshot hashes checked; no stimulate/step; invalid input throws. Original saved brain remains owned by organism. | Connected to `prepareCycle`; explicit forbidden-method tests. |
| Biological observation + Life State → context | `compileContext` → `WorkingContext` text/hash/selection manifest. | Pure; critical overflow throws; permission/provenance checks. No biological interpretation update is fabricated. | Connected to preparation; deterministic/privacy/budget tests. |
| Context → planner → proposal | `PlannerV2.propose` → strict `Proposal`. | Context/source/scientific wording validation. Fallback abstains; provider errors become failed preparation or ambiguous grant. | Injected provider/fallback connected in fixtures; live factory missing. |
| Proposal → policy | `evaluatePolicy` → ALLOW/DENY/DEFER/REQUIRE_HUMAN_APPROVAL and payload hash. | Outside LLM; revisions/permissions/cost checked. Grant commit recomputes context/policy. | Executable tested. No general public approval route. |
| Policy → local action/non-execution | Only permitted `local_reflection`/`local_artifact` text is staged. | No shell, filesystem executor, internet or external effect. Assistance stays local. | Connected to pure preparation and atomic commit, not shipped HTTP cycle. |
| Result → episode/Life State | `reduceLife` plus `DecisionV2` and private episode. | Assertions/status/defer changes only on ALLOW. Invalid change references throw; no repair/fallback. | Connected in `prepareCycle`; narrower than an outcome-learning engine. |
| Prepared result → durable decision | `commitV2` under transaction and `CycleFence` → numbered decision, episode, Life State/base revisions, grant terminal state. | Row locks, lease/cancellation/revision/identity checks; all-or-nothing rollback; duplicate cycle/IDs rejected. | Tested real PG fixture; schemas not canonical, no active production entrypoint. |
| Committed outcome → next world event | No V2 producer. Legacy `liveCycle` once generated nextEvent but is no longer runtime authority. | No continuation permission, queue or next wake time update. | **Missing.** |

The complete **local one-shot preparation-and-commit chain** exists inside a library. The **deployed runtime lifecycle** and **outcome-to-next-event loop** do not. HTTP/CLI flags deliberately cannot connect these islands implicitly.

## 7. Identity, state continuity and restart behavior

`genesis_organisms` stores the original UUID/birth/brain/economic JSON plus revision, phase and lease. Decisions have a unique numeric cycle; Life State is owned through the organism foreign key and repeats the UUID. Grants bind both the identity and expected revisions. `commitV2` changes only base cycle/activity and extension state, preserving birth/brain/economy. Historical events/decisions have append-only guards.

- **Normal restart:** tested by fresh standalone Node processes against isolated restored state; both boots remain read-only, CLOSED and schedule-disabled.
- **Crash before/after claim or before commit/after intent:** tested in separate child processes. Claimed work is not silently reused; expired claims become AMBIGUOUS; committed duplicates are rejected.
- **Database reconnect/outage:** a pool and error listener exist; transactions fail/rollback. No explicit outage/reconnect injection test, retry coordinator or active-cycle recovery daemon exists. Do not treat normal restart tests as outage proof.
- **Redeploy:** persistence is external Postgres and boot refuses an empty/replacement organism. Actual Railway redeploy/network behavior was not tested. Runtime grant identity includes Node version/platform/architecture and source files, so target changes require a correctly matched grant rather than reuse of a laptop identity.
- **Indefinite continuity:** identity can persist independently of LLM sessions. Useful continuity additionally requires retrieval, bounded growing state, backups and a continuation loop. Those are incomplete.

## 8. Life State: stored fields versus real workflows

All new arrays are currently empty; `canonical-inventory.json` records counts. Persisted does not imply writable through an approved workflow. Life State is private except explicitly projected counts/status.

| Field | Actual storage/update/provenance/validation |
|---|---|
| Projects | Original project in base JSON and `genesis_projects`; `projectLife` is a status/reason/source overlay for an **already existing** project. Strict reducer; no V2 create workflow. |
| Tasks / unfinished work | `tasks` persists ID/status/reviewAt/source. Reducer can defer an existing task, cannot create or finish one. Canonical tasks are empty. |
| Resources | Legacy simulated ledger persists; context computes cash. Wallet identity remains unresolved. Operational provider ledger is separate and unapplied canonically. |
| Interests / open questions | Arrays of assertion-shaped values; no dedicated runtime reducer/write path. Fixture display is not an update workflow. |
| Commitments | ID/source/status/dueAt persisted shape; compiler includes limited fields; no creation/fulfilment workflow. |
| Relationships | ID/source/consent persisted shape; no admitted write, retrieval or interaction lifecycle. |
| Preferences | No supported V2 preference state/biological preference authority. Semantic beliefs must not be relabeled neural preference. |
| Goals | Constitution is durable guidance. Legacy `drives` remain historical product text, not a V2 goal-progress engine. |
| Semantic/self memory | Strict planner-authored assertions, source IDs, confidence, unverified flag, supersession/contradiction references. Append only by reducer; no fact-checking engine. |
| Environment | ID/text/source/visibility/time persisted shape; compiler selects public items. No ingestion endpoint. |
| Pending decisions | Array present; preparation/assistance journaling does not populate a usable pending-decision management workflow. |
| Current focus/rhythm | Legacy rhythm preserved; V1 starts dormant. No dynamic focus/rest/wake reducer. Base activity becomes generic “Computational life event recorded.” |
| Temporal/history | Episode IDs and biological-observation IDs append per prepared cycle; at/revision/source recorded. No due-time execution. |

`reduceLife` rejects unknown project/task IDs, duplicate assertion IDs and unrecognized source/history references. It does not deduplicate semantically repeated claims or maintain a prioritized task list. Direct database writers remain trusted; `LifeExtensionStore.read` checks schema version/constitution hash rather than validating every stored field against a complete runtime schema.

## 9. Four memory ownership boundaries

| Memory | What persists | Retrieval / writes / limits | Assessment |
|---|---|---|---|
| Biological-model memory | Original saved neural snapshot; independent frozen fly research plastic state remains research | Saved adapter restore/view only. Digital events do not update it. | Implemented for current saved-only scope; no current biological learning. |
| Episodic memory | Seven original memory rows and decisions; future V2 private `genesis_life_events` episode with proposal/policy/error and optional text artifact; full decision elsewhere | Atomic one-shot commit works in fixtures. No context retrieval of legacy memory or V2 episodes; all legacy memories explicitly excluded for lack of consent. | Storage works; usable recall incomplete. |
| Semantic/self memory | Identity/constitution plus `semanticMemory` assertions in Life State | Source-bound append/supersession references. Compiler includes assertions only when **all source IDs are already selected**. No external verification. | Narrow self-belief mechanism; broad retrieval unresolved. |
| Working context | Temporary serialized context plus persisted hash/selection manifest | Pure deterministic compiler; raw full context is not stored in public DTOs. Byte budget, whole-excerpt dropping. | Implemented bounded subset; not all intended inputs. |

A subtle retrieval limitation: assertions referencing a past event-specific biological observation will generally not have that source in a later cycle's selected IDs. They may remain stored but never be selected again. There is no source-resolution query to fix that bridge.

### Growth assessment (inspection, not invented load benchmarks)

| Scale | Expected behavior from present code |
|---|---|
| 10 cycles | Storage capacity is not a concern; the principal problem is missing episodic recall/workflow. One-shot code itself will not reach this count. |
| 100 cycles | `episodicRefs`, observation IDs, semantic assertions and decision/event rows grow without pruning. Public history remains a latest-20 view rather than complete accessible history. |
| 1,000 cycles | Entire Life State JSON is read/cloned/written, semantic/environment selection scans arrays, and context manifests list rejected IDs. Critical tasks/commitments are not bounded individually; exceeding the context budget rejects the whole cycle. |
| 10,000 cycles | Unbounded JSON write amplification, ever-growing event/intent/provider tables, no retention/archival/search plan or long-run benchmark. No relevant provider-attempt time/cycle indexes in the draft schema. Public latest history still loads full decision JSON internally. |

Genesis does **not** inject all history into its prompt. It also does **not** yet perform adequate retrieval. Both distinctions matter. Legacy `liveCycle` truncated its in-organism memory to 80, but that deprecated path is not the V2 retention policy.

## 10. Biological core and scientific boundaries

- Real C. elegans equations/302-neuron data remain in `core/brain/celegans.ts` and `data/connectome.json`; frozen hashes match. Existing isolated scientific tests execute these models, but canonical runtime never stimulates/steps them.
- Runtime restoration instantiates the C. elegans class to initialize a saved snapshot and read state. It does not call `stimulate`, `step` or `decodeBehavior`. Tests replace those methods with throwing spies and still pass.
- Fly studies remain in `research/`; only the pinned Brain Spec evidence package is consumed at runtime. Stage-1 associative learning is research-only; no failed/inconclusive branch is installed.
- Historical `APPROACH / AVOID / EXPLORE / RETREAT / WAIT` still exist in the original contracts, policy, planner, sensory and `core/life.ts` paths. They are **deprecated runtime authority**, not deleted history. Production service ignores old constructor planner/brain arguments and rejects advance before those paths can run. Historical CLIs throw before execution.
- Old code contains phrases such as “retained its neural impulse,” direct semantic-to-action mappings, simulated service-income rules and digital danger/novelty stimuli. These are real legacy implementation, **not permitted current production claims**. Reusing that loop would violate the current boundary.
- Current public narrative disclaims historical labels and saved replay. The main remaining provenance defect is `observe()` using `history[0].at` for the unchanged snapshot. The initial seven-decision state is consistent, but a new computational-only decision cannot supply a new recording time for old biology.

There is no need to install more neuroscience to complete the admitted computational life. This audit recommends no capability promotion or biological migration.

## 11. Context, planner and provider audit

### Context compiler

`compileContext` orders mandatory constitution/identity/Life State/biology/permissions/tools first, then environment sorted by ID, then eligible semantic assertions in stored order. It uses UTF-8 byte length as a conservative engineering bound, not an admitted model tokenizer. Whole optional excerpts are dropped; oversized mandatory content fails clearly. A manifest records selected/dropped IDs and reasons. Context hash and state revision are bound into proposals and grants.

Included: UUID/birth/cycle count, constitution, limited rhythm, project IDs, full current task list, limited commitments, simulated cash, null onchain/revenue, non-applied biology/provenance, permission set and one-shot factual event when supplied. Missing: actual episodic retrieval, project names/artifacts/status overlays in ordinary critical context, relationships/interests/open questions, priority/ranking by relevance, deadlines that cause wakeup, memory disclosure management and structured general-world event payloads. Source visibility/credential-like text is filtered, but a regex is not a full sensitive-data classifier.

The budget protects request size, not all host memory/manifest growth. `ProviderControl` currently passes `context.text` to its injected counter, while the separate `LanguagePlannerV2` request adds instructions and a proposal-contract suffix. A future bridge must count the complete provider request, including this overhead; blindly joining those components would not establish the token/cost ceiling. There is no LLM context summarizer or hidden second narrator. Stale state is rechecked at one-shot commit; ordinary read-only public reads use multiple queries rather than a coherent multi-table snapshot.

### Planner

A provider-neutral `PlannerV2` interface and strict `proposalSchema` exist. `ProductFallback` deterministically abstains; it is not an autonomous project strategist. `validateProposal` rejects unknown enums/extra fields, unauthorized citations, mismatched context and certain prohibited biological wording. It does not prove a rationale true or fully enforce constitutional intent.

`LanguagePlannerV2` contains a Responses-style HTTP request implementation but its default transport throws `DURABLE_PROVIDER_CONTROL_REQUIRED`; it is not installed by the runtime or joined to the admitted durable provider path. It requests JSON and then validates locally; there is no production end-to-end provider result/usage proof. Old `core/planner.ts` is not a substitute: it belongs to the deprecated semantic-brain pipeline.

### Durable provider controls

`ProviderControl.reserve/dispatch/recover/reconcile` and `OneShotController.providerPlanner` implement:

- context/revision/grant/model binding, durable reservation before dispatch and atomic budget reservation;
- one attempt, no paid retry/fallback, input/output ceilings, per-call/cycle/day ceilings;
- unknown liabilities retained across midnight, cancellation/timeout and post-response authority check;
- response identity/usage/proposal hash and bounded diagnostic codes; no raw provider body published;
- ambiguous-result stop and manual reconciliation evidence.

What is **not supplied** is an admitted actual provider/model, verified transport implementation factory, model-compatible complete-request token counter, rate card, verified treatment of every billable usage category, secret resolver or live transport smoke result. `config/provider-admission.pending.json` explicitly says PENDING. The schema takes positive integer microdollars/token; fractional tariffs need an explicitly justified representation or conservative bound, not invented rounding/pricing. $0.05 is an enforced configured ceiling under supplied tariff assumptions, not a verified quotation for an unspecified model.

Transport IDs/code hashes and counting provenance are checked against caller-supplied admission objects. The future trusted factory must actually select the pinned implementation; passing a matching string is not independent code attestation. `recover()` marks all in-flight reservations unknown: it must not be called indiscriminately while healthy workers are active. No daemon/operator route currently operates these recovery methods.

## 12. Constitution versus enforceable policy

`core/v2/identity.ts` defines frozen **v1.0.0** guidance: Continuity; Learning and honesty; Useful contribution; Sustainable existence; Human agency and safety; Freedom to reconsider. Its canonical hash is stored in Life State, included in context and bound in grants. A changed hash fails the existing context/store checks. There is no runtime “rewrite constitution” tool or authorized amendment workflow.

The principles are **constitutional guidance**. An LLM can produce unhelpful, false or repetitive permitted text despite them. The enforced policy is narrower: proposal schema, source references, local-effect allowlist, lock/grant/revision binding, budgets, approval state and absence of external executors. Scientific wording regexes reject some forbidden statements but cannot establish semantic honesty. No claim is made that a textual constitution is a complete safety system.

## 13. Policy and action/tool reality

Effects below refer to current Runtime V1, not what an old research/demo function can be manually imported to do.

| Action/capability | Action status | Actual enforcement and result |
|---|---|---|
| Local reflection | LOCAL ONLY | On ALLOW, text is staged in private episode and committed; no private filesystem process. |
| Local artifact | LOCAL ONLY | Same database-backed text save, bounded proposal text. No standalone file, update/version retrieval API or publication. |
| Abstain / defer | IMPLEMENTED | Structured proposal/episode persists on authorized fixture commit; defer does not schedule a wake. Production invocation remains disabled. |
| Human assistance | LOCAL ONLY | Local request/pending record only; no message delivery or answer ingestion. |
| Existing project status | LOCAL ONLY | Reducer changes overlay for known original project; no project creation. |
| Semantic assertion | LOCAL ONLY | Validated sourced unverified claim persisted in extension. |
| Filesystem / shell | NOT IMPLEMENTED | No V2 dispatcher/tool; first mode expressly forbids them. |
| Internet/search/browser/research | DISABLED | No V2 executor. Old fixed-URL reading helper is deprecated, not installed. |
| External API other than admitted LLM | NOT IMPLEMENTED | No admitted tool/dispatcher. |
| External message / social/email | NOT IMPLEMENTED | Proposal can require human review; no effect executor exists, even if approved. |
| Wallet read | DISABLED | Real balance adapter exists but no active worker/admission. |
| Signing/transfers/trading/purchases/hiring/token launch | NOT IMPLEMENTED | Financial proposal type does not implement transaction construction or execution. |
| Scheduling / automatic next cycle | DISABLED | No active V2 scheduler. Grant explicitly forbids a second cycle. |
| Biological advancement | DISABLED | Saved adapter throws; compiler refuses non-null/applied biology. |

There is a small typed proposal vocabulary and an intent journal, **not yet a general extensible executable tool registry**. Absence of an executor is an effective current boundary, but not a reusable authorization design for arbitrarily adding future tools.

`approvalMatches` checks payload identity, tool, expiry, approver and policy; present recipient/network/asset requirements are null. That is not a usable financial recipient authorization. `recordIntentTransition` refuses reservation/dispatch/success in this release. There is no browser approval button or private approval API.

**Verified integration defect:** `OneShotController.journal` writes a reduced record without `organismId`, `policy`, `reservedMicros` or `approval`. `LifeExtensionStore.recordIntentTransition` passes such records to `transitionIntent`, which immediately accesses `intent.policy.payloadHash`. A pure, no-database audit probe reproduces a TypeError on proposed→denied; see `intent-compatibility.json`. Existing tests cover complete draft intents and one-shot persistence separately, not this cross-component handoff. The journal must not be described as an operational approval workflow. No code was changed.

Local effect idempotency comes from unique cycle/decision/event IDs and atomic transactions. Pending intent status can remain `proposed` after a permitted local text commit; the commit does not finalize the intent journal. No external receipt/rollback framework is implemented. “Local saved” means text in Postgres, not completion of a broader task.

## 14. Outcomes, projects and human feedback

`prepareCycle` classifies failures/local saves/defer/pending/abstention deterministically. It persists allowed planner-supplied LifeChanges; it does not independently infer task progress from observed external outcomes. The biological model is not trained.

A useful narrow path exists: permitted local text + sourced assertion/project-status change → episode and extension commit. Limits:

- A proposal requiring approval never runs an external action. REQUEST_ASSISTANCE is `pending`; a generic external proposal requiring approval can retain an `abstained` outcome while the policy says approval is required. These fields need consistent operational semantics before broader tools.
- Invalid reducer references throw outside the planner/validation catch. One-shot handles this by failure/closure, not a fabricated successful life event. Tests do not establish a recovery dialogue.
- No task creation/completion, new-project creation, artifact revision history, project-income/expense attribution or abandonment/revisit controller exists. Existing project can be marked abandoned/active, but nothing decides when to revisit or supplies its artifact to later context.
- Human assistance text is recorded privately. There is no properly attributed answer event, inbox, relationship/commitment update, notification delivery or assistance deduplication.
- `operatorTrace` exists as a private projection function but no authenticated runtime endpoint serves it. Library approval/revoke/reconcile functions rely on a trusted caller; a management interface still needs authentication, audit records and secret-safe presentation.

Thus experience storage exists, while the practical feedback/learning loop is incomplete. It would be misleading to claim the organism already learns from all its life merely because it writes an episode.

## 15. Autonomous lifecycle and time after Decision #8

**First-awakening safety and long-run autonomy are different systems.**

After a successfully committed one-shot cycle: cycle becomes 8; a V2 decision and private episode are stored; Life State revision increments; base phase returns idle and lease clears; grant becomes CONSUMED; execution remains CLOSED and schedule remains disabled. Brain/economy/birth remain unchanged. There is no automatic next event or wakeup. A second invocation fails; even a new first-awakening grant is rejected because both the hardcoded expectation and SQL fence require seven prior decisions.

Current answers:

| Question | Actual answer |
|---|---|
| Return to idle? | Yes, transaction sets base phase idle; rhythm remains dormant unless separately modeled. |
| Receive another general event? | No admitted persistent intake/queue/consumer. |
| Decide when to wake? | Can store DEFER timestamp; no scheduler consumes it. |
| Resume unfinished work? | No operational task/retrieval loop. |
| React to time? | One-shot factual event includes wall time; no time-event producer. |
| React to external observations? | Dormant wallet poller is not started; no V2 observation bridge. |
| Computational rest? | Abstention/deferral records exist; no sleep/wake policy or biology claim. |
| Survive restart? | Saved identity/decisions survive tested local process restart; active recovery is manual/library-only. |
| Continue to #9 safely? | Not with this controller or shipped runtime. |

Legacy schedule table stores enabled/next time/interval/remaining/budget data and old store functions implement some due-time logic. They are fenced off; `LifeScheduler.tick` only asserts dormancy. No delayed-task queue, recurring reflection, deadline system, polling workflow or durable V2 wake-time management is connected. `GENESIS_INTERVAL_MS` and `GENESIS_MAX_DAILY_CYCLES` do not create a V2 operating policy.

## 16. Economy, wallet, internet and communications

### Economic namespaces

- **SIMULATED:** integer-cent ledger with idempotent entries, validation, reserve/expense limits and historical income/P&L categories. Current $100.75 is development money. The old `work` tool manufactured explicitly simulated income every third work unit; that deprecated rule is not current business income.
- **ONCHAIN:** unresolved identity and null balance in public DTO. `SolanaReadOnlyWallet` implements HTTPS JSON-RPC `getBalance` at finalized commitment with timeout and integer handling. No signing, token enumeration, transaction history, submission or confirmation tracker. Configuration does not prove address ownership/network; current main does not instantiate polling.
- **ATTRIBUTED REVENUE:** null, no verified feed. An incoming transfer cannot become earnings. `ClawPumpFeeIncomeAdapter` requires an injected verified-reader contract, validates receipt shapes, but does not implement the authoritative source, signature/attribution verification or a durable complete ingestion workflow.
- **OPERATIONAL:** prepared provider reservation/usage costs, separate from simulated cash. There is no compute/infrastructure expense import or funded-real-runway calculation. This audit added none.

Namespace separation is explicit in present DTOs and policy. Risks come from future ingestion and attribution, not an observed current sum of incompatible balances. There is no canonical real economic execution.

### Internet and communication

`core/life.ts` has an old read-only fetch helper limited to hardcoded readings, HTTPS source choices, no redirects and bounded body reading. It is not a V2 tool, and is not general search or browser research. Current source provenance for those old readings does not create future ingestion permissions. No public arbitrary URL fetch endpoint was found.

There are no X/email/Telegram/Discord clients or inbound message routes in the inspected executable product. Assistance is local recordkeeping only. A safe later internet/message feature needs independent permissions, egress/SSRF protections, untrusted-content handling, per-effect idempotency, observation provenance and human consent. None is necessary for the first non-network local cycle.

## 17. First-awakening controller: actual state machine and gaps

`OneShotController`, `one-shot-authority.ts`, `commit-v2.ts` and `one-shot-schema.sql` implement the durable single-consumer mechanism. Payload binds organism/runtime/constitution/policy/mode/event/permission hashes, revision/count, planner/model/admission, allowed/forbidden effects, one cycle, one attempt, budgets, issuance/expiry and operator evidence.

| State | Implemented behavior |
|---|---|
| PROPOSED | Validated immutable payload inserted; no execution. |
| AUTHORIZED | Matching payload/issuer/reference recorded by trusted library call; no public/operator entrypoint yet. |
| CLAIMED | Transaction locks base, extension and grant, verifies actual count 7 and revisions, creates one lease/attempt. Unique unresolved-claim index. |
| CONSUMED | Atomic commit records decision 8/episode/state and terminal result; includes abstain/defer/local/denied/planner-failure outcomes as applicable. |
| REVOKED | Pre/postclaim revocation/cancellation invalidates work; stale workers cannot commit. |
| EXPIRED | Expired unclaimed authorization becomes terminal; not an unlock. |
| FAILED | Pre-commit known failure closes the attempt; no automatic retry. |
| AMBIGUOUS | Expired claimed/crashed or unresolved-provider work stops for review. No automatic reopening or replacement grant. |

Tests exercise normal local outcomes, denial, mismatched identities/hashes/counts/revisions, two workers, duplicate commit/invocation, second grant, expiry, cancellation, stale state, durable intent crash, fresh-process restart, mock timeout/budget and API/CLI/environment/scheduler bypass refusal.

Not established by those tests: real provider cancellation/billing, target-host process termination, storage/network partition recovery, authenticated grant issuance, actual migration deployment, or a human-operated ambiguous-grant resolution procedure. `recoverExpired` and provider `reconcile` are methods, not an operational recovery service. The execution-grant state machine has no admitted transition out of AMBIGUOUS; resolution cannot be improvised as a retry.

The mode is executable validated configuration, version **GENESIS_FIRST_AWAKENING_V1 / 1.0.0**, still **NOT_AUTHORIZED**. The neutral event schema rejects extra fields and carries factual identity/time/history/scope with biology NOT_APPLIED. No canonical event/grant was created here. Maximum configured cost remains **$0.05**, one paid attempt, ≤12,000 input/1,200 output tokens, zero automatic retries; actual model cost/counting evidence is pending.

## 18. Database and persistence audit

### Applied canonical schema

Catalog inspection confirms 12 `genesis_*` tables, migrations **001, 002, 003**, 14 indexes, append-only/writer functions and triggers. See the full read-only catalog export, including constraints/functions rather than merely SQL source.

- `genesis_organisms`, `genesis_decisions`, `genesis_memories`, `genesis_ledger`, `genesis_projects`, `genesis_milestones`, `genesis_schedule`, `genesis_external_observations`, `genesis_migrations`.
- `genesis_life_state`, `genesis_life_events`, `genesis_action_intents` added by Runtime V1.
- Unique cycle and ID constraints; memory→decision FK; extension/event/intent ownership FKs; append-only historical protections; guarded old writers.

### Prepared but unapplied

`runtime/preparation-schema.sql`: `genesis_cycle_attempts`, `genesis_provider_grants`, `genesis_provider_attempts`.

`runtime/one-shot-schema.sql`: `genesis_execution_grants`, transition/delete guards, partial unique unresolved-claim index, and **replacement** of the old OPEN-based writer function with a closed-state one-shot fence. Although additive in data intent, it changes a security function; it is not merely adding harmless empty tables.

No listed preparation table is canonical. `npm run db:migrate` only installs 001/002. Migration 003 uses a separate reviewed migration path. Preparation/one-shot schemas are installed by guarded fixture helpers, not a production idempotent installer. A new deploy cannot safely infer the intended schema from the generic migrate command.

### Persistence limits

Atomic commit and conflicting-writer rejection have real PG tests. Provider budgets use an advisory transaction lock; grant claims lock rows. These are valuable properties. Draft provider tables lack broader FKs and workload indexes. Most Life State constraints are application JSON validation, not relational enforcement. There is no automatic backup, PITR management, retention/archiving, corruption detection daemon or restore runbook exercised against a production host.

The canonical connection's inspected role has `rolsuper`, `rolcreatedb`, `rolcreaterole`, `rolbypassrls` true. All canonical table RLS flags are false. This is a local development setup, **not acceptable evidence of production least privilege**. SQL session markers are application fencing, not authentication against an actor who holds those credentials or can bypass triggers. Separate schema-owner/migration and runtime roles are required before active production.

## 19. Security and public/private data

### Verified current protections

- Constant-time hashed bearer comparison, minimum configured operator secret length and origin check for mutation requests; public mutation paths still return CLOSED/not-authorized.
- Frontend never imports the database/planner into the observer. Dormant proxy refuses reads/mutations; development preview is impossible in production via its flag alone.
- Public state exposes identity/counts/namespaced resources/saved metadata and redacted history. `publicDecision` V2 has only bounded enums/statuses/provenance; legacy labels are allowlisted and disclaimed.
- Historical replay exposes timestamp/model/ticks/activity/stimulation only; no plans/prompts/private event content. Replay rejects V2 records as a source of new neural frames.
- No arbitrary tool URL, shell, wallet signer or external dispatcher is installed. Prompts cannot create a tool implementation or overcome the execution fence.
- Provider-control errors are scrubbed to bounded codes; raw response text is not public. Context marks selected excerpts as untrusted; model proposals still face independent schema/policy checks.

### DTO inventory

| Public surface | Authoritative source / disclosure |
|---|---|
| `/api/state` | `GenesisService.observe` → `publicState` + `publicDecision`; saved-biology metadata only. |
| `/api/history` list/detail | `publicDecision`; no raw record returned. List currently lacks exposed pagination. |
| `/api/brain` | Static `data/connectome.json` nodes/edges. |
| `/api/replay?id=` | Explicit saved legacy frame projection in `GenesisService.replay`. |
| `/healthz` | Fixed lock/worker result after DB dormancy check; no secret. |
| Next API proxy | Fixed runtime endpoint, query forwarding, no server secret injection in production, no redirects, generic failure. Trusts upstream JSON; no additional server-side DTO schema. |
| `/preview` / preview API | Development-gated fixtures/static anatomy/sanitized saved frame; no canonical query. |
| Observer components | `readObservation` strips unrecognized fields before copy/JSX. Scientific graph uses a separate structural projection. |
| Private operator trace | Function only, no public API; bounded stored rationale, not hidden chain-of-thought. |

No public private-memory/planner/approval/credential leak was found in the inspected routes and tested canaries. This is a scoped source/test result, not a penetration-test guarantee. Raw private exports under `outputs/` are outside Next `public/` and mode 0600.

### Security-critical and operational launch blockers

1. **Least-privilege DB access:** do not deploy the current superuser credentials. Validate permissions with the actual migrations/fences and separate owner account.
2. **Trusted operator entrypoint:** authenticate authorization/revocation/reconciliation independently of payload strings. Existing class methods assume the caller is trusted. Provide private inspection and durable authorization evidence without a generic unlock.
3. **Admitted provider factory and total billability:** pin real implementation/model/counting/tariff, prove all billed input/output categories fit, bind to one grant. No production key or generic environment string substitutes for this.
4. **Target recovery and secrets:** target TLS, private DB reachability, secrets isolation/rotation, backup/restore, ambiguous-provider review and stopped-cycle inspection remain unverified.
5. **Public availability controls:** no application rate limiting; state reads reconstruct a saved brain and synchronously verify evidence on every request, loading up to 20 full historical decision rows internally. Add/load-test suitable cache/request limits before significant traffic. Next proxy reads the full request body before its 2,000-character check; runtime itself limits 8 KiB. This is an availability hardening gap, not observed activation bypass.
6. **Logging boundary:** runtime logs raw database `e.message` to operator stderr. Sanitize/review platform logging and access; no claim that arbitrary future provider/library errors are safe merely because public handlers are generic.

No arbitrary external ingestion currently exists, so current prompt injection cannot execute arbitrary shell/financial actions. Safe later browsing cannot be inferred from that absence. No software patch was made to resolve any finding.

## 20. Public observer reality

The redesigned observer is real code: one Live view, static genuine connectome, chronological redacted moments, simulated-resource summary, memory/project counts and detail navigation; saved neural replay is explicit and loaded on demand. Polling stops while the document is hidden; the canvas is memoized and does not continuously fabricate firing. CSS/semantic labels include reduced-motion, keyboard and responsive provisions.

What is real versus preview-only:

- **Real now:** original age/identity, seven historical records, simulated cash/counts, static structural brain and selected genuine saved replay. Production countdown stays primary unless public presentation mode is explicitly changed.
- **Real once a V2 row exists:** enum-based abstain/defer/help/local-save/denial/failure summaries can render it. No provider text becomes public copy.
- **Fixture only:** rich example memories, interests, project descriptions/questions and illustrative varied V2 activity scenarios. Actual backend emits no such free text, deliberately.
- **Incomplete:** live phase/current-activity reporting (`publicState` is always DORMANT), V2 episode count (`o.memory.length` stays seven), full timeline pagination, approved public-memory/project disclosures and meaningful changes. Observer Life uses the latest 20 state-history entries; “show more” only expands that array. It does not fetch the full historical archive.
- **Scientific correction needed before new record:** unchanged snapshot timestamp is derived from latest decision as described in A07.

The UI can display Decision #8 in recent history without pretending its neurons fired. It cannot yet show the complete promised evolving life. No UI redesign or new screenshots were produced in this audit. Existing screenshot reports were treated as historical review material, not fresh functionality proof. Current tests check DTO/template behavior and source-level responsive/accessibility provisions; they are not browser layout or screen-reader automation.

## 21. Tests and build verification

Completed existing suite command:

```text
node --env-file=outputs/runtime-v1/test-db.env --test tests/*.test.ts
162 tests; 162 passed; 0 failed; 0 skipped; 0 cancelled; 0 todo
reported duration: 6,214.331041 ms
```

Dedicated database enforcement and disposable schemas prevent canonical writes. Some Postgres preservation tests restore a previously saved private baseline into isolated schemas; active-cycle/one-shot tests use sanitized fixtures and injected transports. A prior existing test also rewrites its dry-run evidence file under `outputs/runtime-v1/`; it does not apply a canonical migration. Old neural tests run isolated models only.

| Area | Existing meaningful coverage | Important limits |
|---|---|---|
| Neural/legacy | `brain`, `life`, `planner`, `identity`, `store`, `economy` tests; determinism/ablation/legacy constraints | Passing legacy tests does not admit legacy loop to V2. SQLite test is compatibility evidence, not production Postgres. |
| Current boundaries | `runtime-v1.test.ts`: saved-state no-step, context/privacy, proposal/policy/reducer, no semantic authority | No complete memory/task/relationship workflow to test. |
| Real local PG | `postgres.test.ts`: restored backup, additive migration, writer fences, private public projection, fresh runtime boot/restart | No target-host/partition/PITR/restricted-role verification. |
| Active preparation | `awakening-active.test.ts`: cancellation, stale revisions/leases, races, crash before commit/after intent, mock provider budgets/ambiguity | Injected transport, non-effectful local actions. |
| One-shot | `one-shot.test.ts`: state transitions, hash fences, two-worker/duplicate/decision-nine refusal, crash/restart/revocation, mock provider | No native admitted live-provider or installed operator command. |
| Observer | `observer-presentation.test.ts`, `awakening.test.ts`: allowlist canaries, namespace separation, copy, fixture gate, static/saved biology, countdown | Mostly pure/source-inspection tests; no browser automation in this audit. |

TypeScript and ESLint completed successfully. `npm run build -- --webpack` completed successfully, matching CI's build invocation. The Vercel/default `npm run build` (Turbopack) was also attempted, including an elevated retry. Both were blocked by the environment while a CSS/PostCSS worker tried to bind a local port (`Operation not permitted`). Default-target verification remains **BLOCKED_BY_ENVIRONMENT**; it is not a demonstrated source-code failure. The successful Webpack build must not be represented as a successful default Turbopack invocation.

Verification interruptions are preserved rather than hidden:

- The first test attempt was denied localhost access by the sandbox (`EPERM 127.0.0.1:6544`). The authorized local-only rerun completed all 162 tests. This was not a code fix.
- An initial concurrent typecheck/build invocation raced on generated `.next/types` files. After build completion, serial TypeScript passed; no implementation changed. Logs retain both attempts. Future verification should not run those two commands concurrently in the same build directory.
- The default Turbopack build retained the same worker-port permission failure after an elevated retry. No third workaround or implementation change was attempted.

Missing meaningful tests include consented recall across cycles, task creation/completion and repeated project work, human-answer ingestion, long-run event scheduling, admitted real transport/full-request billing, network partitions, backup restoration on the target, restart after an actual provider request, traffic load and long-duration growth. Mocks passing are not production integration.

## 22. Deployment: local evidence versus target obligations

| Item | Verified locally | Still requires target environment |
|---|---|---|
| Frontend | Next 16.3.4 / React 19; `vercel.json`, separate proxy, production bundle | Actual Vercel routing/environment/ingress, intended domain and runtime URL; no DB/LLM keys in frontend |
| Runtime | Node native TypeScript entrypoint, read-only local process boot/restart tests | Railway service/container startup, TLS, port/health/restart behavior |
| Node | Local v26.1.0 arm64 Darwin; package requires ≥22.18 | Docker/CI specify Node24 Linux; actual image compatibility and grant identity must be checked there |
| Docker | Actual Dockerfile audited: Node24, production dependencies, non-root, port3001, CMD `node runtime/main.ts` | **BLOCKED_BY_ENVIRONMENT**: executable unavailable; no build/boot/restart claim |
| Railway | `railway.json`: Dockerfile builder, `/healthz`, 120-second health timeout, ON_FAILURE/max10 | **BLOCKED_PENDING_OPERATOR_TARGET** locally; operator must identify/link intended project/service/environment. No guessed target |
| Postgres | Local catalog/state and isolated transaction tests | Managed Postgres/Supabase endpoint, TLS/roles/pooling/backups/recovery |
| Migrations | Explicit 001/002 command, separately guarded003; pending schemas identified | Reviewed manual installation with preservation audit; never boot migrations |
| Defaults | Lock CLOSED; disabled schedule required; no worker/provider/wallet start | Confirm exact deployed environment and target boot—not only example values |
| Provider/wallet flags | Legacy env fields parsed; not permission to run them | Admit provider separately; wallet remains disabled/unresolved |
| CI | Workflow declares tests/type/lint/build/Docker on Node24/Postgres16 | No remote CI result queried; workflow text is not a successful run |

`.dockerignore` excludes env files, private outputs, node_modules and Git, but not the full research tree. Only Brain Spec v0.2 is copied into the runtime image, yet the local Docker context can include roughly 16 GB of research; production source/build-context handling needs review. The image does not include all operator scripts/tests, so a future laptop-only command cannot be assumed available inside it.

No GPT Sites runtime/deployment is required by the shipped entrypoints or dependencies. A historical `.sites-runtime` ignore entry is not a hosting dependency. No production resources were created, linked, queried or deployed during this audit.

## 23. Long-run failure modes

These are architectural/code-path projections, not fabricated soak measurements. Today the dormant process does not autonomously accumulate cycles.

| Horizon/risk | Existing mitigation | Work still needed before continuous operation |
|---|---|---|
| 24h: repeated cycles/provider failures | One-shot cap, leases, no retry, unknown liability | Continuous-life budgets/event dedup/backoff; no current recurring authority |
| 24h: stale work/cancellation | Revision/lease/lock checks and atomic commit | Operator recovery visibility; real transport cancellation cannot retract a request already sent |
| 7d: repeated assistance/reflection | Individual proposal schema only | Semantic task/assistance dedup, unanswered-question handling, bounded idle policy; do not force productive action |
| 7d: stuck projects | Existing status overlay and task defer | Task creation/progress/revisit, failure/reminder handling, artifact retrieval |
| 7d: stale external observations | No current observer/external effects | If enabled, trustworthy freshness; wallet poller error retains old balance while updating row check time—do not mistake check time for observation time |
| 30d: provider reservation/recovery | Unknown costs retained, no automatic retry | Supervised reconciliation, status-specific retention/indexes, total-cost aggregation without namespace mixing |
| 30d: DB/log growth | Append-only history and bounded public projection | Retention/archive/log rotation/backup capacity; complete history retrieval |
| 1,000 cycles: context/JSON growth | Bounded serialized context, optional excerpt drops | Bound critical tasks and manifest growth; indexed retrieval; avoid rewriting all accumulated references each cycle |
| Many viewers | Hidden-tab polling pause; static canvas; replay on demand | Cache verified immutable evidence/structural data, avoid loading full historical traces for state summaries, rate/traffic tests |
| Restart/redeploy | Existing-state-only boot, row persistence | Target failover/outage tests, controlled recovery worker, no blanket in-flight recovery while healthy workers operate |
| Runaway spending | Zero active provider; one-shot reservation/cost caps | Actual tariff/usage completeness; reviewed longer-run daily caps and credential-side limits |
| Corruption/privileged mutation | Hashes, revisions, current SQL writer guards | Least privilege, immutable audit/backup integrity and restore drill; superuser can defeat guards |

## 24. First-awakening and long-run readiness

**First awakening is not ready for activation today.** Remaining requirements are more than human authorization: connect a private manual one-shot entrypoint, make pending schema installation/recovery reviewable, supply the intended permitted history/context, correct saved-snapshot provenance, implement/admit a real provider if LLM reasoning is desired, verify the target and least-privilege persistence, and then authorize the exact release/grant.

A deterministic first cycle can avoid paid-provider selection, but the present fallback only abstains, and it does not eliminate entrypoint/schema/context/operational requirements. It must not be presented as a real-LLM awakening.

**Long-run autonomous life is not implemented.** The three-layer direction is coherent and preservation/safety primitives are useful; missing work is largely connecting and extending product lifecycle, retrieval, task/event and operator systems. No neuroscience expansion, wallet signer or trading system is required to begin meaningful continuous local life.

## 25. One ordered remaining-work plan

This is a plan only. Nothing below was implemented or authorized by this audit. A first-cycle blocker is distinguished from later continuous-life work; optional financial/internet/social features need not delay a local non-effectful start.

### PHASE A — LOCAL CODE COMPLETION

1. **Finish private operator execution/inspection.** Provide a reviewed, authenticated, manually invoked one-shot entrypoint using the existing controller, exact grant/release binding, safe preflight, private trace, terminal/ambiguous result inspection and no generic unlock. Test the actual intended invocation, not only internal methods.
2. **Prepare a production installation path.** Package pending preparation/one-shot SQL with explicit version/precondition/idempotency checks, backups and isolated restore/rollback verification. Preserve old rows and review the writer-function replacement. Do not apply to canonical as incidental boot work.
3. **Complete first-context recall.** Establish approved memory disclosure rules; retrieve a bounded relevant selection of original/V2 episodes and artifacts with provenance, identity/history/project context. Resolve stored assertion sources across cycles. Do not send every private memory indiscriminately.
4. **Correct functional provenance/trace inconsistencies.** Bind saved biology to its original recording; distinguish current/last activity; make episode counts accurate; reconcile the incompatible one-shot/operator intent record shapes and keep pending/denied/local statuses coherent; provide appropriate private artifact retrieval. No frozen record rewrite.
5. **Implement the admitted-provider integration seam.** Native transport, complete-request token-count contract, bounded structured response/usage parsing, cancellation, trusted implementation registry and secret-reference loading through existing durable reservations. Test with protocol-shaped mock responses. Leave it disabled pending Phase C.
6. **Finish operational safety tests and least-privilege compatibility.** Test command authorization, restricted DB role, stale grants, crash-after-commit observation, context/reference failures, explicit recovery and no repeated paid attempt. Harden body/log limits where necessary for public hosting.
7. **Complete local groundwork for continuous life in fixtures, separately from one-shot authority.** Versioned event intake/queue/dedup, meaningful task/project/artifact operations, attributed human answers, bounded memory selection/state, future delayed wakes/budgets/backoff and idle behavior. Define the reviewed operating scope; test many local non-effectful cycles without opening canonical execution. This work can be done locally and must not be hidden as “deployment.” It is a long-run blocker, not a reason to weaken the first-cycle fence.
8. **Repeat tests/build and prepare deployment artifact/runbook.** Limit build context, align runtime Node/build commands, document exact pending migrations and grant identity calculation. Preserve auditability of all prior research.

### PHASE B — PRODUCTION INFRASTRUCTURE

9. Operator identifies intended Vercel frontend, Railway service/environment and managed Postgres target. Configure private DB access/TLS and separate migration/runtime roles; provision secret storage without activating a provider.
10. Build the actual non-root runtime container when Docker/target builder is available; boot/restart against an isolated copy first. Prove no auto-initialization/migration/heartbeat/worker and preservation. Verify health/restart/shutdown and exact target release identity.
11. Verify backups/PITR and an actual restore drill, ingress/access limits, operator logging/monitoring and frontend public-only proxy. Deploy dormant/read-only configuration only; no cycle or grant implied.

### PHASE C — PROVIDER & SECRETS

12. Select exact provider/model and independently verify tariff, tokenizer/counting and all billable request/response categories. Admit transport/code identity and total ≤$0.05, ≤one attempt configuration; refuse if proof does not fit.
13. Install runtime-only secret reference. Conduct a separately authorized isolated transport smoke test, usage/cancellation/error audit and target egress check. No canonical call; no silent fallback model or retry. Freeze admission and bind its hash into the future grant.

### PHASE D — AWAKENING PREPARATION

14. Re-audit canonical digest/counts/identity/birth/snapshot, frozen research and installed target identities. Explicitly review/apply necessary schema changes as a separate authorized step, with row preservation and lock/schedule still CLOSED/DISABLED.
15. Finish human public/private observer review and operator reconciliation procedures. Prepare exact factual event and one-shot grant bound to expected seven decisions, runtime/constitution/policy/mode/permissions/provider and resource ceilings. Obtain explicit human authorization; mere preparation is not authorization.

### PHASE E — FIRST AWAKENING

16. Only after separate execution authorization, manually consume one grant for **at most Decision #8**. Allow abstention/deferral/local output/help; do not script success. Keep biological processing non-applied, scheduler/wallet/internet/external messages off. Preserve provider liabilities and stop for review on ambiguity.
17. Verify commit/identity/history/provenance/costs/public projection and consumed/closed authority. Review the recorded cycle before any continuation. Do not automatically request or create another grant.

### PHASE F — POST-AWAKENING AUTONOMY

18. Review the separate bounded continuous-life controller/event/memory/task/human-feedback work from Phase A against the first-cycle evidence. Authorize a new operating scope with capped cycles/cost, emergency stop, idempotent wakes and restart/reconciliation controls. Never repurpose the first-awakening grant to create #9.
19. Begin only the separately authorized small continuous-local scope, with operator observation and measured growth/recovery. Increase capabilities individually after end-to-end verification. Browsing/communication/wallet/income integrations are optional later scopes, not assumptions of current “life.”

## 26. Product reality check

**If a real LLM key were supplied and this repository deployed today:** Genesis would display its dormant countdown or its saved observer depending on presentation configuration. Its real structural brain and seven saved records could be viewed. The runtime would retain one original identity. It would make no canonical decision, provider call, wallet action, public post or new project. An empty database would not silently create Genesis 002. A key with incompatible legacy environment configuration could even fail configuration validation; a correct key does not grant execution.

**If the prepared one-shot library were properly installed, connected and separately authorized:** it could perform one reasoned/abstaining computational cycle, persist a private episode and approved bounded text/assertion/existing-project-status changes, then stop. The current deterministic fallback would abstain. The real-provider path still needs implementation/admission. “Create artifact” means database text, not publishing a website or running code.

**After the first successful V2 cycle:** it would return to idle with the grant consumed and execution closed. No next event, wake or Decision #9 would occur. It would not yet continue living autonomously. The missing loop is bounded event/time intake → relevant retained context → authorized planning → permitted local work → reliable outcome/project/task/memory update → future event, with durable operating authority and human recovery.

## 27. Final recommendation

Preserve the accepted scientific boundary and existing safety infrastructure. Complete the local lifecycle and integration gaps instead of calling the repository code-complete or treating deployment/key configuration as the remaining work. A protected dormant observer is operationally real; the prepared one-shot engine is substantial; continuous artificial life remains unfinished.

The audit's final preservation and exact command results are recorded in [VERIFICATION_SUMMARY.md](VERIFICATION_SUMMARY.md). Final read-only verification found the same canonical digest, all rows identical, seven decisions, CLOSED execution, DISABLED schedule, SAVED-OBSERVATION-ONLY biology and zero canonical V2 cycles. All 200 protected source/config/data/document files matched their audit-start hashes, and all 9,319 frozen-inventory files matched. Live provider calls, wallet actions and external communications during the audit were zero. No reported gap was repaired during this audit. No activation is authorized by this document.

ARCHITECTURE COMPLETE — IMPLEMENTATION WORK REMAINS
