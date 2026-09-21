# Project Genesis — Final Pre-Awakening Implementation

Date: 2026-09-20. **No awakening authorization was issued or exercised.**

## 1. Result and preservation

**FINAL PRE-AWAKENING CONTROLS IMPLEMENTED — BLOCKERS REMAIN**

The single-use controller, grant schema, transaction fences, isolated verification and human observer package are implemented. They have not been installed or invoked against canonical Genesis. Existing service/API/CLI execution remains hard-closed.

Before and after read-only canonical exports match row-for-row and have digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

| Preserved item | Final value |
|---|---|
| Original Genesis 001 ID | `817e772c-827e-48fc-8e35-6504cb2a8d2d` |
| Original birth | `2026-09-15T01:56:07.867Z` |
| Organisms | 1 |
| Canonical decisions / cycles | **7 / 7** |
| Original memories / project | **7 / 1**, unchanged |
| Economy, original wallet record, history, saved biological snapshot | Unchanged |
| Execution | **CLOSED** |
| Schedule / schedule metadata | **DISABLED**, unchanged |
| Canonical V2 decisions / episodes | **0 / 0** |
| Canonical tables/migrations/grants added | **0** |
| Live provider calls / wallet actions / Genesis external communications during pass | **0 / 0 / 0** |

Evidence: [canonical-preservation.json](verification/final-pre-awakening/canonical-preservation.json). Private exports remain ignored files with restricted permissions; no private database payload is attached to this report.

The 9,345-file preservation audit found **zero mismatches**: 9,319 previously protected research/design/neural/data files plus the preceding preparation report and its evidence files. [Audit](verification/final-pre-awakening/preservation-files.json). Brain Spec, frozen research, Stage 1–5, C. elegans equations/connectome and original biological state remain unchanged. No Drosophila runtime, biological interpretation or new scientific capability was introduced.

## 2. One-shot authorization primitive

Implementation:

- [one-shot-spec.ts](server/one-shot-spec.ts): strict grant/mode validation and content identities.
- [one-shot.ts](server/one-shot.ts): propose, authorize, claim, check, prepare, journal, commit, revoke/cancel, failure handling and expired-claim recovery.
- [one-shot-authority.ts](server/one-shot-authority.ts): transaction-time identity/state/schedule checks.
- [one-shot-schema.sql](runtime/one-shot-schema.sql): durable grant table, unresolved-claim uniqueness, immutable payload/claim/authorization, terminal-state and deletion guards, grant-aware database writer fence.
- [commit-v2.ts](server/commit-v2.ts): shared atomic commit with one-shot revalidation.

Each payload binds grant ID; existing organism; exact runtime code/environment identity; constitution version/hash; policy version/hash; mode version/hash; neutral event schema version/hash; exact permission manifest/hash; maximum one cycle; planner/provider/model/admission identities; one provider attempt; cost/input/output ceilings; allowed local effects and explicit prohibitions; issuer/evidence reference; issuance/expiry; original and Life State revisions; expected prior decision count **7**.

`PROPOSED` is not authority. `authorize` requires a separate record matching the exact payload hash, issuer and evidence reference. The internal authorization function is a privileged operator operation, not a public endpoint or a cryptographic identity provider. A future trusted operator must verify the authorization evidence before calling it. This pass creates only test grants and does not supply a canonical grant or authorization document.

The runtime identity hashes a specified code/config/dependency-lock map together with Node version, operating system and architecture. The current local identity is in [identities.json](verification/final-pre-awakening/identities.json). A Linux/Node24 target must resolve its own identity before an operator authorizes a target-specific grant; a local identity cannot silently authorize another runtime.

## 3. State machine and single-consumer semantics

| From | Allowed transitions | Meaning |
|---|---|---|
| PROPOSED | AUTHORIZED, REVOKED, EXPIRED | No cycle authority yet |
| AUTHORIZED | CLAIMED, REVOKED, EXPIRED | A valid, unexpired, explicitly authorized payload may be claimed once |
| CLAIMED | CONSUMED, REVOKED, FAILED, AMBIGUOUS | No second claimant or restart reuse |
| CONSUMED / REVOKED / FAILED / EXPIRED / AMBIGUOUS | None in this release | Cannot be reset, edited into authority or deleted through ordinary grant writes |

A consumed grant records the terminal computational result: abstention, deferment, pending local assistance, local artifact/reflection, denial or planner failure. Known cancellation/revocation before commit terminates the grant without a decision. A failed orchestration before commit is FAILED unless a provider outcome is unresolved, in which case it is AMBIGUOUS. These are execution/accounting states, not biological claims.

Claiming locks the original organism, extension and grant in a transaction. It verifies seven existing decisions and seven recorded cycles, exact revisions, CLOSED global state and disabled schedule. It assigns a fixed logical cycle ID derived from the grant and a fresh lease. A unique cycle-attempt ID and unique unresolved organism claim prevent duplicate or competing consumption.

The shared commit rechecks grant status/lease/expiry, runtime/evidence identities, exact revisions, count, factual event, reconstructed context hash, planner identity, policy verdict and local-effect scope. Decision 8, its private episode, Life State changes, grant consumption and lease release commit atomically. A second grant in this first-awakening mode also expects seven prior decisions and therefore cannot create decision 9.

**The global execution lock never becomes OPEN.** Scoped authority is explicitly supplied to context/policy preparation and checked again in the database transaction. Setting a boolean OPEN is not a substitute. The generic service, HTTP endpoints, scheduler and legacy CLI do not consume one-shot grants, even if environment flags or request bodies name one.

## 4. Database fence and migration boundary

The old database fence correctly rejects every CLOSED-state original-row write, including a new one-shot lease. The prepared migration replaces that function on isolated copies with a narrower grant-aware fence. It requires a CLAIMED grant, transaction-bound grant/lease identifiers, matching authorization payload reference, the original organism, unexpired scope, CLOSED extension and disabled schedule.

For original tables it admits only the bound organism lease/phase/cycle update and the matching V2 decision 8 insertion. Original organism fields other than computational activity/cycle remain protected; other original-table writes, including schedule, ledger, wallet/history edits, are refused. Existing append-only decision/event protections remain in place.

This is a security-sensitive writer-fence change, **not a purely structural migration**. Consequently it was **not applied to canonical Genesis**. Future deployment must separately review and explicitly install the prior preparation tables plus this one-shot schema/fence on a verified backup/copy before any canonical installation. Neither script is run by boot, Next.js or the migration-on-start path. `installFixtureSchema` refuses anything other than the dedicated test database/schema.

The production Dockerfile includes the new server/config imports, but this does not start a controller or authorize a grant. Database-owner administrative access remains trusted; this design is not protection against a malicious superuser rewriting functions or tables.

## 5. Crash, cancellation and reconciliation

- Crash **before claim** leaves AUTHORIZED with zero consumption. A later explicit invocation may claim it; no scheduler retries it.
- Crash **after claim**, before commit or after the durable intent leaves CLAIMED, no additional committed decision and no fabricated receipt.
- Once an unresolved lease expires, explicit recovery marks it **AMBIGUOUS** and cancels the stale attempt. Another grant for that organism is refused while ambiguity exists.
- Recovery does not reopen execution or retry a paid request. There is no automatic AMBIGUOUS → AUTHORIZED transition or reconciliation shortcut.
- Revocation before/after claim and cancellation during planning/before commit prevent commit. A bounded planner deadline and authority polling also reject a planner that never resolves; no late result can commit. Stale revision/lease or changed context fails closed.
- A remote timeout is not evidence of non-billing. Outstanding provider reservations remain liabilities. An ambiguous provider result prevents normal one-shot completion and requires review.
- A crash after the database transaction commits can be resolved by reading the already consumed grant and its decision; invocation cannot produce another cycle.

Reconciliation requires operator review of durable grant/attempt/decision/provider evidence. This release deliberately contains no command that guesses a result or clears an ambiguous execution grant. A reviewed remedy/new authorization is required. External irreversible executors remain absent; no exactly-once external-effect guarantee is claimed.

## 6. Verification

**150 tests passed, zero failures, zero skips**: the prior 110 tests plus 40 one-shot cases. TypeScript, ESLint and Next.js webpack production build pass. [Logs and identities](verification/final-pre-awakening/).

All active tests use sanitized fixture identity, unique `awakening_test_*` schemas in `genesis_runtime_v1_test`, no canonical credentials, mock providers and local effects only. The ordinary V1 tests still exercise compatibility in their own isolated schemas. One-shot tests keep their fixture global lock CLOSED throughout normal execution.

| Required case | Result |
|---|---|
| Valid cycle, abstention, defer, local reflection/artifact, local assistance | One fixture V2 decision, count 7 → 8, grant CONSUMED, lock CLOSED, schedule disabled |
| Policy denial | No local effect; terminal DENIED result, consumed once |
| Planner failure | One explicit computational failure record, no fallback; grant consumed |
| Mock provider success | One durable reservation/request; one cycle at most |
| Mock provider timeout | AMBIGUOUS; no automatic retry or invented success |
| Cancellation / revocation before claim, after claim, during planning, before commit | No committed additional decision |
| Expiry | EXPIRED durably; no claim |
| Wrong organism/runtime/policy/constitution/mode/permission/state revision/expected count/authorization reference | Rejected |
| Wrong Life State revision | Rejected |
| Two claimants and two committers | One successful claimant, one successful commit |
| Duplicate invocation / attempted second first-awakening grant | Cannot produce decision 9 |
| Fresh-process crash before claim | Still seven; one later explicit claim works |
| Fresh-process crash after claim / before commit / after intent | Still seven; expired recovery AMBIGUOUS, replacement grant blocked |
| Restart | No fabricated episode/outcome; no grant reopening |
| Unadmitted planner / over-limit token count | No provider transport call |
| Scheduler / authenticated API / CLI / enabling environment flags | Cannot consume the available grant; seven decisions preserved |
| Generic OPEN / ordinary writer marker | Insufficient authority |
| Grant payload rewrite, terminal reauthorization, deletion | Database rejection |
| Context altered before commit | Rejected; no extra decision |

Initial fixture tests identified a reserved SQL column name and the existing CLOSED writer fence; these were corrected in the new isolated implementation. A later full run exceeded the existing standalone-server readiness deadline while a large file audit/build overlapped it. The failure log is retained; after that workload finished, the full suite passed without changing its startup tolerance. No frozen research or canonical repair occurred.

## 7. Finalized first-awakening mode and neutral event

Mode: [config/first-awakening-v1.json](config/first-awakening-v1.json), validated by the strict executable `modeSchema`.

- ID: `GENESIS_FIRST_AWAKENING_V1`
- Version: **1.0.0**
- Canonical JSON SHA-256: `cc16b326232479bb0679ffdc82b4d4a687873977e48e08ced44cc10d8f8f3ee0`
- Status remains **NOT_AUTHORIZED**. A separate payload-bound grant supplies authority; the mode file never becomes a generic enable switch.

Neutral event: [JSON schema](config/first-awakening-event.schema.json) and matching strict [runtime validator](server/awakening-event.ts).

- Schema version: **1**
- JSON-schema file SHA-256: `179acfee77f40c944c003e91d4a85611fb5d88e8dd4d9f95f769ea5e40101b20`

The event contains only the activation reference, timestamp, existing identity/birth, last saved event time and elapsed wall time, constitution identity, seven prior cycles, `not_applied` biology, wallet identity status, approved context references and permission hash. It is included in the private context and episode provenance, not treated as a biological stimulus. There is no motivational variable or desired outcome. The context supplies factual projects/tasks/resources and permissions under existing disclosure rules. No canonical event was instantiated.

Allowed after a future separately authorized grant: inspect approved identity/birth/history metadata, constitution, computational Life State, project/task/resource state, wall time, permission state and historical saved provenance; reason once; abstain, defer, request assistance locally, reflect locally or persist one bounded local artifact and permitted Life State changes. There is one proposal/artifact slot per cycle, not arbitrary filesystem execution. Existing private legacy memory text remains undisclosed; only memory content already permitted by the source-aware context compiler can be included. This pass grants no blanket memory disclosure.

Disabled: biological advancement/stimulation/stepping, fly runtime, wallet RPC/signing, transfers/trading/token launch/ClawPump, purchases/hiring, external messages/social posting, internet/research/browser automation, arbitrary shell or filesystem execution, unadmitted APIs, scheduler and a second cycle. A request for assistance is a local pending record, not a sent message.

The four memory domains and constitution remain intact. Product-level abstention/reflection is not a neural output or scientific capability claim.

## 8. Provider admission and cost

**PROVIDER_ADMISSION = PENDING**

No exact provider or model is admitted. [provider-admission.pending.json](config/provider-admission.pending.json) preserves nulls for missing evidence; [provider-admission.ts](server/provider-admission.ts) specifies the strict admission contract.

Required before admitting a paid planner:

1. Named provider and exact model; no environment-selected override.
2. Reviewed API transport ID/code hash and compatible response/usage interpretation.
3. Tokenizer/counting method ID and evidence covering the complete request representation, including any transport-added overhead.
4. Hashed rate-card evidence covering all billable usage; no invented rates or omitted fee classes.
5. Input/output token bounds, per-attempt/per-cycle/day ceilings, timeout and zero automatic retries.
6. Server-side secret reference, not a key inside the grant/context/report.
7. Admission hash bound into the execution grant. Dispatch then binds grant hash, context hash, revisions and attempt identity in durable records.

`providerPlanner` verifies the supplied reviewed transport and counter identities, creates a scoped budget record, and uses the existing durable reservation/timeout/usage/reconciliation controls. The controller refuses an arbitrary injected planner for an LLM-enabled grant; that planner must have been constructed through its provider-admission path. Native network transport and secret resolution remain uninstalled, because no real model/tariff/counting method has been selected. Mock identities and rates used by tests are labeled TEST ONLY and are not admissions.

Hard first-cycle external ceiling remains **$0.05 total (50,000 micro-USD)**, maximum **one attempt**, **12,000 input / 1,200 output tokens**. These are ceilings, not targets. Automatic retries: **0**. Timeout ceiling: **25 seconds**, within the proposed **60-second lease**. If counting and verified pricing cannot establish a reservation within the grant, dispatch is refused. No second paid model or implicit paid fallback is available. Unknown liabilities are retained across restart and midnight.

Current integer micro-USD tariff representation accepts only configurations it can safely represent. A fractional or more complicated tariff must not be rounded optimistically; admission must refuse unless a reviewed conservative accounting representation is justified. No $0.05 feasibility claim is made for an unselected real model.

## 9. Human review and infrastructure

Human package: [HUMAN_OBSERVER_REVIEW.md](verification/final-pre-awakening/HUMAN_OBSERVER_REVIEW.md).

It includes final desktop/mobile screenshots of the dormant landing, Live, Brain, Life, Money, Memory, scientific limits and the uncommitted V2 fixture. Fixture labels explicitly state **NOT CANONICAL / NOT AWAKENED / DEVELOPMENT FIXTURE**. The checklist asks for approval/rejection of scientific wording, biological presentation, privacy/disclosure, clarity, mobile layout and causal trace. **HUMAN_OBSERVER_REVIEW = PENDING**. Preparing or viewing this package is not approval.

**DOCKER_VERIFICATION = BLOCKED_BY_ENVIRONMENT**. Docker/Podman and the standard executable locations remain unavailable. Nothing was installed. No actual image/Node24/container result is claimed; local checks used Node v26.1.0. The independent Next build and isolated standalone Node boot/restart pass.

**TARGET_HOST_VERIFICATION = BLOCKED_PENDING_OPERATOR_TARGET**. Read-only Railway status again returned no linked project. No project was created, guessed or linked. Operator must identify the existing Railway project ID/name, environment and runtime service, then explicitly authorize or perform the intended link/read-only verification. Target build/start/platform overrides, secrets/networking and health still require inspection before deployment. Any eventual image check must use an isolated pre-migrated copy, never canonical Genesis as a smoke-test database.

**WALLET_IDENTITY = UNRESOLVED**. No address was created, inferred or bound. Every wallet capability is disabled. This is not a blocker for the proposed non-wallet first cycle.

## 10. Remaining blockers and exact change scope

Remaining blockers:

- Human observer and implementation review.
- Docker/target-host verification and target-specific runtime identity resolution.
- Separate approval of the grant/preparation schema and writer-fence migration; none applied to canonical state.
- Provider/model/transport/token-counter/rate-card admission if real LLM reasoning is selected.
- Explicit operator authorization record for exactly one reviewed grant, issued only after the above prerequisites for its chosen mode are satisfied.

Implemented files: new `server/one-shot*.ts`, `server/awakening-event.ts`, `server/provider-admission.ts`, `runtime/one-shot-schema.sql`, final mode/pending-admission JSON, one-shot tests and support fixtures, this report and separate verification package. Updated `server/commit-v2.ts` for scoped revalidation; `core/v2/context.ts`, `cycle.ts` and `contracts.ts` for explicit temporary grant authority; Docker import/config copying; and the observer fixture banner. No frozen scientific files, biological core, BrainAdapter, canonical schema/records, constitution or policy rules were changed.

The scoped path is deliberately a privileged internal controller. No public unlock, authorization, execution or retry endpoint was added. Existing canonical runtime boot, scheduler, API and CLI remain closed. This is an implementation for review, not permission to invoke it against Genesis.

## 11. Final state

```
DECISIONS = 7
EXECUTION = CLOSED
SCHEDULE = DISABLED
BIOLOGY = SAVED-OBSERVATION-ONLY
CANONICAL V2 CYCLES = 0
LIVE PROVIDER CALLS DURING PASS = 0
WALLET ACTIONS = 0
EXTERNAL COMMUNICATIONS = 0
```

**FINAL PRE-AWAKENING CONTROLS IMPLEMENTED — BLOCKERS REMAIN**
