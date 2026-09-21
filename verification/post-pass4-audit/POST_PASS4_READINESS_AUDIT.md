# Project Genesis — Post-Pass-4 System Readiness Audit

## 1. Executive summary

**Genesis has a working, tested local computational-life core. It does not yet have the production connections needed to operate that core as an authenticated, provider-backed organism.** Passes 1–4 substantially closed the original foundation, retrieval, Life State and local event-loop gaps. The next work is not another biological model, a new memory architecture, or simply adding an API key.

The most important remaining work is:

1. A trusted operator surface for narrowly scoped authorization, revocation, inspection, disclosure review and recovery. Library methods accepting operator-reference strings are not authentication.
2. An admitted real-provider implementation, including complete-request counting, billing evidence, secret resolution and structured proposal transport. Existing durable controls are exercised with injected transports, not an installed production adapter.
3. An explicit provider-visible context/disclosure path. The seven legacy memories are still excluded. New operational Life State and continuous events deliberately prohibit provider disclosure. Passing an API key cannot resolve this.
4. A reviewed production installation/role/backup path and target verification. Preparation, one-shot and continuous SQL exist but are not installed canonically. The current local connection is a superuser/table owner, not an acceptable production worker role.
5. A supervised active entrypoint. The shipped service is an observation service; it does not invoke OneShotController or start ContinuousWorker. Continuous authority currently admits **only local deterministic planners**, not paid LLM planning.

Decision #8 remains an isolated one-shot operation. Decision #9+ is now architecturally and executably possible in the **local, separately authorized** continuous controller. It is not an automatic consequence of Decision #8 and is not available from the deployed entrypoint today.

### Audit scope and strength of evidence

This audit read all five requested reports, executable source, tests, SQL and deployment files. It used read-only canonical PostgreSQL transactions and file hashing. It did not run a neural model, create an authority/event, invoke a planner, start a worker, call an HTTP/API endpoint, deploy, or change implementation/schema/canonical records. Only audit documents, sanitized evidence and private integrity exports were written.

The prior Pass-4 result is **387 passed, 0 failed, 0 skipped**. Its report/log manifest verifies; reconstructing its final source snapshot verifies **164 current files with zero mismatches**. This is relevant historical test evidence, not a newly executed integration suite. Integration tests would create disposable authority and start test workers, which this audit expressly does not authorize. Fresh non-emitting TypeScript and non-fixing ESLint checks both passed (exit 0); they are recorded separately below. No fresh build or browser/server session was started; the verified prior Webpack build and browser review are historical evidence only.

All five prior report packages verify against their own content manifests. All **9,319 frozen research files** verify against the existing preservation manifest. The working tree already contains substantial prior uncommitted work; that is not attributed to this audit. See `evidence-verification.json` and `preservation.json` in this directory.

## 2. Canonical integrity

Read-only snapshot method: `scripts/runtime-v1-audit.ts`, `BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY`, sorted complete `genesis_*` rows, SHA-256 of the existing script's JSON serialization. Private exports are mode 0600 under `outputs/post-pass4-audit/`, outside public assets and this sanitized report package.

| Invariant | Verified state |
|---|---|
| Organism | `817e772c-827e-48fc-8e35-6504cb2a8d2d`, one original organism |
| Birth | `2026-09-15T01:56:07.867Z` |
| Decisions / legacy memories | **7 / 7** |
| Canonical V2 episodes | **0**; the one Life State event is administrative |
| Original projects / ledger / milestones | **1 / 4 / 4**, unchanged |
| Execution / schedule | **CLOSED / DISABLED** |
| Biology | **SAVED-OBSERVATION-ONLY**, original snapshot unchanged |
| Continuous authority | **NONE**; continuous tables absent |
| One-shot authority | **NONE**; execution-grant table absent |
| Wallet identity | Unresolved; no wallet capability activated |
| Other database clients at initial export | 0 |

Initial and final row digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

Complete before/after rows match, including identity, birth, history, memories, project, ledger, milestones, saved brain, Life State, lock and schedule. No automatic repair was performed. Provider calls, wallet actions, external communications and biological advancement **during this audit: 0**. No canonical V2/provider/external-effect evidence was added. The repository/database cannot independently prove that no out-of-band actor ever called an external service; these are scoped audit and canonical-state statements, not an external-account audit.

## 3. Architecture trace: executable connections and remaining islands

| Boundary | Executable input → output and persistence | Authorization/failure behavior | Evidence / remaining production work |
|---|---|---|---|
| Event → authority | `RuntimeEvent` strict discriminated schema → immutable `genesis_runtime_events` envelope | Owner/source/dedup/time checks; no permissions in event text | `core/v2/continuous.ts:eventSchema`; `server/continuous.ts:enqueue`; authenticated intake absent |
| Authority → claim | Hashed `ContinuousScope` or `OneShotGrant` → cycle ID, lease, base/Life revisions | Exact runtime/constitution/policy/permission/planner binding, expiry and counts; mixed authorities rejected | `continuous-authority.ts`, `one-shot-authority.ts`; schemas prepared |
| Claim → current state | Locked organism and extension + read-only archive → preparation input | One active owner lease; revision checks; no organism initialization | `ContinuousController.claim/prepare`, `OneShotController.claim/prepare`; PG race/restart tests |
| State → biology | Digital event + saved snapshot reference → NOT_APPLIED observation with null value | Saved adapter cannot advance; commit rejects executed biology | `core/v2/biology.ts`, `server/saved-provenance.ts`; research is evidence only |
| State → memory | Archive + query + audience → bounded `MemorySelection` | Missing consent/provenance excludes optional item; corrupt identity fails | `memory-store.ts`, `core/v2/memory.ts`; review loading absent from controllers |
| Memory → context | Identity/constitution/state/event/selection → text, manifest and content hash | 12,000 UTF-8-byte ceiling; whole optional items dropped; critical overflow fails | `compileContext`; provider operational context intentionally empty |
| Context → planner | `WorkingContext` → strict `Proposal` | Context hash/citations/schema checks; timeout/cancellation; no semantic brain authority | `PlannerV2`, `validateProposal`; real admitted transport missing |
| Planner → policy | Proposal + revision/permission/current state → verdict and payload hash | Reducer preflight; unknown operations/targets and forbidden effects refused outside model | `evaluatePolicy`; not a proof that bounded natural-language text is true |
| Policy → intent | Complete validated `ActionIntent` → journal | Owner, policy payload, approval/reservation fields preserved; terminal transitions refused | `core/v2/intents.ts`, `server/intent-journal.ts`; A11 fixed |
| Intent → local effect | Allowed text/LifeChanges → staged local artifact/state, then DB persistence | No external executor; approval is not execution; denial/abstention/failure distinct | `prepareCycle`, `reduceLife`; no filesystem/shell dispatch |
| Local effect → commit | Prepared decision/state + current fence → next numbered decision, episode, final intent, revised Life State | Recompiles context; rechecks policy, deterministic reducer, permission, lease/revisions and numbering under locks | `commitV2`; atomic local commit, not generic external exactly-once execution |
| Commit → outcome/memory | Bounded recorded outcome + source-bound changes → private episode, artifact versions, state history | No biological learning implied; source evidence is not autonomous fact checking | Passes 1–3 integration tests |
| Outcome → follow-up | Allowed DEFER/typed follow-up/task or commitment review → due event(s) | Depth/delay/effect/event limits and target version; denied/failed proposals do not schedule | `followups`, `ContinuousController.commit`; same transaction as decision/consumption |
| Follow-up → idle/next cycle | Explicitly enabled worker polls due queue → one claim or idle | No eligible work means no planner/decision; scope budget/expiry/revocation applies anew | `ContinuousWorker.tick/run`; no production supervisor/entrypoint |

The local loop is connected: tests cover request → wait → attributed answer → wake → recall → resolution, task continuation, artifact revision and 100 committed cycles. The important disconnected islands are **production control-plane access**, **real provider transport/admission**, **durable disclosure review → context loading**, **ambiguity reconciliation → legal lifecycle resolution**, and **worker library → production service supervision**.

## 4. Identity and continuity

Identity is owned by PostgreSQL, not an LLM session. `genesis_organisms` retains UUID/birth/saved brain; unique decision IDs/cycle numbers and transactional increments retain numbering. `genesis_life_state`, append-only episodes, immutable original decisions/memories, operational histories and artifact versions retain computational continuity. One-shot/continuous SQL prevents rewriting protected original identity/brain and keeps the legacy schedule disabled.

| Situation | Evidence and limit |
|---|---|
| Normal runtime restart / reconnect | Existing state is read, never recreated; fresh-controller/PG tests recover state, focus and artifacts |
| Local worker crash | Durable claims/leases, process-exit tests and bounded local recovery prevent duplicate committed events |
| Application redeploy | Same intact DB preserves rows by design; no target redeploy was performed |
| Different Node/platform/build | Grant/scope hashes include exact source and runtime identity; stale authority fails closed. Mac-issued identities cannot simply be reused on Linux/Node 24 |
| Deployment rollback | Incompatible writers are fenced; no tested automated schema/app rollback procedure or authority renewal |
| Database replacement/restore | Continuity requires restoring the same complete database and verifying it. Empty DB is not a replacement Genesis. No automatic reinitialization occurs at runtime boot |
| Restore older backup after a billed request/commit | Local snapshot may forget authority consumption or liability. Runtime hashes do not detect all historical rollback. Requires stopped writers, external/provider reconciliation, fresh review and invalidation of stale authority |

Persistence tests are not production disaster-recovery verification. A tested backup/restore and rollback runbook is still required.

## 5. Memory

The Pass-2 retrieval implementation remains present and connected to both preparation and commit revalidation:

- Legacy memories, bounded decision/episode projections and attributed inputs are discovered by `readMemoryArchive`. Raw planner response/prompt/rationale and neural arrays are not retrieved as memory.
- `retrieveMemory` distinguishes past experience, unverified semantic assertion, prior artifact and temporary working context. Biological snapshot state remains a separate owner.
- Relevance is deterministic structured/lexical ranking, not embeddings: explicit reference, task/project/subject association, lexical overlap, pending/current state and recency with stable ties. Direct older references can outrank recent irrelevant records.
- Default selection limits are 3 episodes, 3 assertions, 1 artifact, 4,500 serialized bytes and 600-byte excerpts, subordinate to the final context ceiling. Source-resolution/supersession/contradiction handling excludes broken references instead of inventing provenance.
- Artifact recall prefers current versions and permits explicit historical-version references. Restart tests recover actual committed fixture history.
- Database discovery takes at most 10,000+1 rows per category; clipping is reported. Beyond that window, an old referenced source can be unavailable. This is not an unlimited indexed archive.

### The seven canonical legacy memories

The read-only inventory confirms **7 discovered records and 0 containing disclosure/consent/visibility evidence**. No review store has been added. Current retrieval therefore continues to exclude all seven; the verified Pass-2 diagnostic is consistent with unchanged canonical rows and current code. Their private contents were not included in this report.

| Operator choice, not made here | Consequence |
|---|---|
| Keep excluded | Acceptable for a narrowly factual first cycle that is explicitly not claimed to recall prior experiences. Identity/birth/count persist; autobiographical reasoning is limited |
| Approve selected internal use only | Enables eligible local reasoning when review is correctly loaded; does not authorize external-provider disclosure or public display |
| Approve selected provider disclosure | Requires scoped source-hash-bound review and production plumbing; could supply useful history to the selected provider without public disclosure |
| Approve public display | Separate decision and projection work; neither necessary nor implied by reasoning admission |

Thus exclusion is **not a persistent-identity blocker**. Historical context is optional for a minimal abstaining/reflective first decision. Operator review is required before claiming that Decision #8 can use its original private experiences, and a provider-context acceptance review is a launch prerequisite for the intended LLM cycle. This audit does not make those consent decisions.

Growth evidence remains fixture-scoped: Pass 2 selected three items at 10/100/1,000 episodes; context sizes were 8,391/8,412/8,433 bytes. The 1,000-episode retrieval measured about 86 ms locally. It establishes bounded selection in that fixture, not constant memory use or production throughput.

## 6. Operational Life State

`core/v2/operations.ts`, `life-state.ts`, `operational-context.ts`, `server/assistance-intake.ts` and `commit-v2.ts` provide real validated workflows, not only interfaces.

| Structure | What can persist and be recalled internally | Limit |
|---|---|---|
| Projects | Create, update summary/status, abandon, resume, complete; stable ID and history | Original legacy project remains separate; no migration into an operational project |
| Tasks | Create, active/deferred/completed/cancelled/reopened transitions, project ownership and evidence | Dates are scheduling inputs only under continuous scope; no external work executor |
| Artifacts | Database text, stable logical ID, immutable versions, current pointer, source episode, associations | No filesystem execution/publication; current and historical recall are bounded |
| Interests | Add/update/retire sourced computational topics | No inferred neural motivation |
| Questions | Create/resolve/close/reopen; resolution requires a source | No autonomous truth verification or web research |
| Commitments | Internal scoped commitments, fulfillment/cancellation/review history | No legal/financial obligations or commitments on another person's behalf |
| Relationships | Minimal sourced reference/context, private disclosure, unknown consent default | No social inference/enrichment; no public or provider disclosure by default |
| Assistance | Request, attributed untrusted response, resolution/cancellation; optional atomic wake | Authenticated intake/delivery/operator workflow absent; no outbound communication |
| Focus | Existing project/task/assistance, idle/none; restart persistence | No autonomous authority or emotion |

Policy validates strict operations, unknown fields, identity collisions, source existence, expected state revision and target version. Deterministic reducers and commit revalidation prevent arbitrary JSON patching and silent concurrent overwrite. History records source events and hashes; text itself remains untrusted. Operational actions can affect future **internal** memory/context today. They cannot thereby cause real-world effects or override disclosure.

JSON growth is an engineering limitation, not evidence of an immediate one-cycle launch failure. Pass-3 fixtures with 20/100/300 tasks used 74,141/128,518/264,918 bytes of state while context stayed about 6.9 KB, with explicit omissions. State/history/artifact versions are still read, cloned and rewritten; archive/manifest sizes grow. Start with small reviewed limits; measure before increasing the horizon. Normalization/indexing/retention becomes important for sustained use, not a reason to rewrite this architecture before Decision #8.

## 7. Continuous life

**Code:** implemented and locally verified for `CONTINUOUS_LOCAL_V1`. **Installation/activation:** absent canonically. **Paid-provider continuous life:** not implemented.

Verified mechanisms include immutable private typed events, due ordering, dedup conflict rejection, transactional claims, one logical organism writer, revision/lease checks, claim-count/window limits, one concurrent cycle, event attempt/backoff limits, continuation depth/root-rate/follow-up limits, target obsolescence, atomic event consumption/child creation and abortable idle polling. Claims, including failed attempts, count against ceilings. Unresolved provider liabilities are not erased at midnight.

The event vocabulary includes manual events, time wake, continuation, task/commitment/project/question/assistance review, human response and a recovery shape. The existence of a recovery event type is not an automatic generator or authenticated intake route. No periodic reflection/job scheduler is implicitly installed.

An allowed completed proposal may create no follow-up. An abstention may leave the queue empty indefinitely. Focus and unfinished tasks alone do not invoke reasoning. Human response wake requires explicit intake authorization and an enabled scoped worker. Expired local claims may retry within limits; ambiguous dispatch does not.

The current scope requires `LOCAL_DETERMINISTIC`, provider/model null, `llm:false`, zero permitted provider attempts and explicit prohibition of live providers. `ProductFallback` just abstains. The capable planners in long-run tests are injected fixtures. Arbitrary injected JavaScript is trusted code, not a sandbox; a production planner factory must supply reviewed implementations, not accept code from events.

Historical integrated evidence: 100 cycles committed decisions 8–107, 100 episodes, 101 events, zero duplicate decisions/events, 11 artifact versions, ten idle ticks and one budget-blocked pending event. Maximum context was 11,143 bytes; state 35,561 bytes. These are local deterministic fixtures, not proof of independent LLM project behavior, paid operation or production durability.

**What still stops life after #8:** no production active entrypoint/supervisor, no installed continuous SQL/scope/intake, no production operator controls, and no admitted continuous provider path. A valid local scope plus a deliberately enabled reviewed local worker can progress after #8 once installed; an API key cannot provide that scope or alter its local-only rules.

## 8. First awakening

`GENESIS_FIRST_AWAKENING_V1` remains version 1.0.0, `NOT_AUTHORIZED`; current code identity is `runtime-v1-oneshot-1.0.4`. Prepared configuration permits one cycle, expected prior count seven, one provider attempt, no automatic retry, 12,000 input/1,200 output token ceilings, $0.05 maximum, 25-second planner/provider timeout and 60-second lease. No provider/model is admitted.

The grant binds exact organism, runtime/environment, constitution, policy, mode, event, permission hash, revisions/count, planner/provider/model/admission, allowed/forbidden effects, issuer/reference and expiry. Claiming uses durable locks and a single unresolved-grant constraint. Shared-code changes retained the one-shot SQL branch, tested again after continuous-schema installation in disposable state.

With a properly installed environment, authenticated invocation and valid grant:

1. Claim checks actual seven decisions/revisions and creates one lease/attempt without opening global execution.
2. It builds a strict factual event, saved-only non-applied biological observation, bounded context and one admitted planner attempt.
3. Schema/policy/reducer checks produce a local proposal, abstention, deferral, assistance request, denial or recorded failure. No external executor exists.
4. Commit rechecks the binding and atomically records at most Decision #8 and one V2 episode, changes permitted Life State, finalizes intent, clears lease and consumes authority.
5. Execution stays CLOSED; schedule stays disabled. A one-shot DEFER is a recorded intention, **not** a continuous wake. No automatic Decision #9.

Known precommit failures close the attempt; interrupted/ambiguous work stays review-required. Reconciliation is not an automatic retry. Installing schema alone never creates a grant/event/cycle. The present boot/API/CLI does not expose this sequence, so a valid record alone would not execute it.

## 9. Exactly what the first cycle would know

This is a source-level assessment, not an instantiated canonical event or simulated decision.

| Category | Current compiler/provider-visible reality |
|---|---|
| Identity/birth/history | UUID, birth and cycle count. Human-readable “Genesis 001” identity/name is not included in `critical.identity` |
| Constitution | Six versioned principles and scientific/permission instructions |
| Current event/time | Factual awakening envelope, wall time, elapsed time and prior-history metadata when legitimately constructed |
| Current computational state | Revision, CLOSED lock, rhythm and permission scope; legacy task/commitment subsets (currently empty) |
| Original project | Legacy project ID only; title, purpose, current summary and work are not included through that path |
| Original memories | None eligible under current no-review state |
| V2 episodes/semantic assertions | None canonically; future records subject to audience disclosure and bounded retrieval |
| Operational projects/tasks/focus | None canonically. Future private operational entries are excluded from a provider context |
| Biology | NOT_APPLIED, null neural value, saved snapshot provenance/limitations; no neural action instruction |
| Economy | Simulated cash 10,075 cents; explicitly separate null onchain/attributed-revenue values |
| Wallet | Unresolved status in factual envelope; no balance/control authority |
| Tools/operations | `local_reflection`, `local_artifact`, permissions and proposal contract. The HTTP prototype does not supply the full operational LifeChange schema to a model |
| Private/public data | No private historical text automatically sent. Critical identity/constitution/event metadata is still provider input if LLM is admitted |

A minimal factual abstention/reflection is coherent; rich autobiographical/project continuity is not currently supported in that provider input. Before authorizing the intended first LLM cycle, approve a concrete context-category/disclosure manifest and verify it includes enough identity and authorized history to meet the chosen scope. Do not silently add private history. Also review whether grant identifiers and the event's authorization-reference string should be included in the provider envelope; references are not secret proof by definition, but current code forwards them, so they must be safe references rather than raw operator evidence.

## 10. Provider / reasoning

| Layer | Current reality | Remaining work |
|---|---|---|
| Planner contract | Executable strict `PlannerV2`/proposal schema, context binding, local policy, bounded stored rationale | Supply full allowed structured-output contract in an admitted provider adapter; no hidden reasoning required |
| Local planner | `ProductFallback` abstains deterministically | Does not implement unscripted project planning |
| HTTP prototype | `LanguagePlannerV2` contains a Responses-style request but default transport throws `DURABLE_PROVIDER_CONTROL_REQUIRED` | Not a production-admitted adapter; no provider choice made by this audit |
| Durable provider boundary | `ProviderControl.reserve/dispatch/recover/reconcile`, injected counter/transport, identity/revision/context checks, reservations, bounded attempts, timeout/cancel polling, usage and unknown-liability records | Real end-to-end request/usage/cancellation behavior remains unverified |
| One-shot admission | `providerPlanner` checks reviewed admission identity and marks returned planner as admitted | Trusted factory must actually select pinned code; matching caller-supplied identity/hash strings alone are not attestation |
| Model selection | Pending | Exact model and supported structured output/billable usage categories |
| Secret configuration | Secret reference schema; no complete production secret resolver | Least-privilege loading, no client/log leakage, rotation |
| Pricing/counting | No selected rate card/tokenizer. Integer-microunit tariff contract and worst-case reservation exist | Count complete wire request, including instructions/schema/tool overhead; conservatively cover every billed category; prove ceiling before dispatch |
| Production smoke test | Not performed | Separately authorized bounded transport/count/usage/cancellation/reconciliation test before a Genesis call |

The injected counter presently receives `context.text`; the separate HTTP prototype adds instructions and a contract suffix. Joining them without complete-request accounting would not prove the token/cost ceiling. $0.05 is a configured hard ceiling under admitted rate/count assumptions, not verified pricing for an unspecified model. There is no implicit fallback after a real-provider failure.

Timeout/revocation after dispatch conservatively retains an unknown liability. A durably received response stores identity/usage/proposal **hash**, not a restartable complete proposal body. A process death after receipt but before commit cannot simply replay that proposal. `recover()` marks reserved/dispatching attempts unknown without per-healthy-worker lease discrimination: production orchestration must not call it indiscriminately against other active requests.

## 11. Operator control

Existing bearer validation protects current HTTP mutations, which still refuse execution. It is not a management API for the new libraries. No authenticated grant/scope/review/response/recovery route or CLI exists. References/issuer strings passed to methods validate attribution and binding, not caller identity.

| Control | Library/data exists? | Authenticated usable interface / audit limitations | Required by |
|---|---|---|---|
| One-shot propose/authorize/claim/revoke/cancel | Yes | No trusted production entrypoint; grant stores exact authorization, but operator identity must be verified externally | First awakening |
| Continuous propose/authorize/revoke | Yes | No authenticated interface; durable scope/journal do not themselves authenticate caller | Continuous life |
| Event intake/queue cancellation | Yes | Trusted references only; no production intake service | Continuous life |
| Human answer intake | Yes, transaction + provenance + optional wake | No authenticated operator interface/answer inbox; answer remains untrusted, private | Before relying on assistance feedback |
| Disclosure review | Typed hash-bound `MemoryReview` input exists | No durable reviewed-record store/load path in preparation and commit; no operational provider promotion mechanism | First provider-context review; richer recall thereafter |
| Ambiguity inspection | `inspectOneShotCycle`, intent/provider records, trace | Private function only; continuous equivalent assembled from tables, not a complete control surface | First awakening |
| Provider cost reconciliation | Ledger method exists | No authenticated workflow; not grant/event reconciliation | First paid attempt |
| Cycle/grant ambiguity reconciliation | Stop/inspection exists | No admitted transition out of terminal AMBIGUOUS grant/event/attempt or REVIEW_REQUIRED scope; no audited resolution operation | Recovery readiness before active operation |
| Emergency stop | One-shot revoke and continuous revoke/cancel methods | Generic CLOSED is already normal active scoped state; setting it again does not revoke scope. Operator must revoke correct authority and stop worker | First/continuous as applicable |
| Resource/queue inspection | Queryable attempts/events; `resources()` | No operator dashboard/CLI, alarms or reason-specific idle view | Continuous life |
| Provider admission | Validated schema and binding | No authenticated admission registry/factory | First real-provider cycle |

A permanently stopped, inspected ambiguity is a safe outcome for an initial one-shot trial; it need not be reopened to count as safely handled. However, resuming after an ambiguous result requires a separately reviewed legal resolution path, not a direct database status edit. The existing inability to resume is an operational recovery gap, not evidence that an ambiguous cycle currently executes twice. A full graphical operator UI is optional initially. A small authenticated, narrowly scoped CLI/service with durable actor attribution, safe private inspection, tested revoke/reconciliation and no generic unlock is sufficient in principle. A manually improvised database edit is not that system.

## 12. Disclosure and consent

Public display, private internal use, provider disclosure and operator-only evidence are distinct. The current implementation correctly fails closed for missing legacy consent, private operational records and unresolvable source chains.

Important gaps are integration gaps rather than permission to relax the rules:

- `compileContext` accepts optional reviews, but `OneShotController.prepare`, continuous preparation and commit recompilation do not load a durable reviewed set. Adding reviews at preparation only would make recompiled context/hash disagree at commit.
- Operational records, human responses, versioned artifacts and all current continuous events explicitly have provider/public=false. Some are hardcoded internal-only by candidate construction; a legacy MemoryReview alone does not admit them.
- `life.environment` items are admitted using public visibility and credential filtering, not a separate provider-review flag. Legacy critical task fields also bypass the new operational selector. These collections are empty canonically today. They need an explicit provider-boundary review before populated provider use; “public” is not necessarily consent to every provider.
- Credential-pattern filtering is useful defense-in-depth, not proof that arbitrary text is non-sensitive.

A basic provider context can contain constitution/factual identity/time/permissions without the seven private memories. Whether that is enough for the approved first-cycle goal is a human scope decision. **Provider disclosure review is a first-awakening prerequisite; automatic disclosure of all private memory is neither required nor allowed.** No reviews were created here.

## 13. Database and migrations

Fresh read-only catalog evidence is in `database-catalog.json`.

### Installed canonical schema

12 tables; migrations 001/002/003 recorded; 14 indexes; 20 constraints; 30 trigger event rows (multi-event triggers counted separately):

`genesis_organisms`, `genesis_decisions`, `genesis_memories`, `genesis_ledger`, `genesis_projects`, `genesis_milestones`, `genesis_schedule`, `genesis_external_observations`, `genesis_migrations`, `genesis_life_state`, `genesis_life_events`, `genesis_action_intents`.

Unique decision cycle/ID constraints, original-memory decision FK, Life State/event/intent organism ownership FKs, append-only history triggers and the Runtime V1 writer fence are installed. Most extension-field validation remains application-level JSON validation.

### Prepared but uninstalled

| SQL | Tables / security changes |
|---|---|
| `runtime/preparation-schema.sql` | Cycle attempts, provider grants, provider attempts |
| `runtime/one-shot-schema.sql` | Execution grants; immutable/transition guards; unique unresolved claim; replaces OPEN-style writer function with closed-state one-shot fence |
| `runtime/continuous-schema.sql` | Continuous scopes, events, attempts, journal; due/window/unique indexes, FKs/immutable/transition guards; adds separate continuous writer branch while retaining one-shot branch |

There is no canonical grant, provider attempt or continuous event table today. Do not label their application code missing merely because it is uninstalled.

### Required production order

1. Select target and fixed application/SQL identities; quiesce writers. Backup the actual original database and verify restore/integrity in an isolated copy. Never seed a replacement organism.
2. Restore/preserve existing 001–003 state. For this canonical database those versions are already applied. `npm run db:migrate` covers only 001/002; the separate Runtime V1 migration is not a general bootstrap replacement.
3. Review role grants and transactionally install **preparation SQL → one-shot SQL** with an audited version ledger/preflight. Verify zero new authority/events/decisions and closed lock/disabled schedule.
4. Continuous SQL depends on those schemas; install only under separate structural authorization, before continuous activation. Its presence must not enable the worker or issue a scope.
5. Verify least-privilege application behavior, trigger assumptions, fresh restart and current runtime hashes on the actual target. Authorizations come later.

Fixture installers deliberately refuse production DB/schema names. Prepared SQL is not a production idempotent migration runner, and `CREATE OR REPLACE` writer functions change security semantics. Installation/rollback tooling, manifest tracking and an operator runbook remain local work before production installation.

The audited connection has superuser, create-role, create-DB and bypass-RLS privileges and owns every canonical table. RLS is not enabled. This local setup is **not production least privilege**. Separate migration owner, private operator, worker and public observer database identities/permissions are required. Session markers are cooperative writer fences, not authentication against an owner who can modify tables/functions/triggers. No production grants/roles were installed or verified.

Transactions use row locks under normal PostgreSQL transactions; coherent public/audit reads use repeatable-read/read-only snapshots. Provider budgets use a transaction advisory lock. The runtime pool is capped at eight connections per process; aggregate limits must include worker/operator/replicas. Provider tables lack some cycle/time lookup indexes/FKs; episode discovery scans/sorts and growing JSON remain future scaling costs. No PITR/backup supervision, event-rebuild utility or restored-ledger reconciliation is installed.

## 14. Deployment

| Component | Actual configuration | Remaining verification/work |
|---|---|---|
| Observer | Next.js 16.3.4, Vercel config, stateless fixed-route runtime proxy | Target project/domain, environment, TLS, runtime reachability, public disclosure/traffic tests |
| Observation service | `runtime/main.ts`; Node HTTP, PG pool, graceful server close, `/healthz`; no boot migrations/init/worker | Production target/service/secrets/networking and actual container execution |
| Active one-shot runner | Trusted library only | Authenticated command/service adapter and lifecycle logging; no generic `/api/cycle` unlock |
| Continuous worker | Explicit disabled-by-default library | Supervised process entry, signal handling, fault/backoff policy, readiness/metrics, authority selection |
| Database | Local PostgreSQL with original state | Durable production target, roles, backups/PITR/restore, migration process and connection budget |
| Provider | Pending config only | Admitted factory/transport/counting/billing/secret/smoke test |
| Operator | Libraries and private projections | Authenticated restricted control surface and durable audit trail |

Dockerfile uses `node:24-bookworm-slim`, production dependencies, non-root Node user, port 3001 and dormant runtime command. It includes required code/config/anatomy/Brain Spec assets, not an active control process. Railway specifies Docker build, `/healthz`, 120-second health timeout and ON_FAILURE with ten restarts. Vercel specifies Next build. CI declares Node 24, disposable Postgres, type/lint/tests/Webpack build and Docker build; a workflow file is not evidence those remote jobs ran.

**DOCKER_VERIFICATION = BLOCKED_BY_ENVIRONMENT:** Docker executable is unavailable locally. No install attempted. **TARGET_HOST_VERIFICATION = BLOCKED_PENDING_OPERATOR_TARGET:** no intended local Railway/Vercel project/service linkage was found. Remote infrastructure was not queried. The operator must identify project/environment/service/database, frontend target/domain and intended network/secrets ownership; this audit neither guesses nor creates them.

Vercel can host the public Next app/proxy; a supervised continuous process needs persistent compute (Railway or equivalent). Observation/operator/worker processes can share a deployment if roles and shutdown/authority are explicit; separate services are not scientifically required. Serverless requests must not become the continuous worker.

Required configuration categories: `DATABASE_URL`, runtime host/port, strong operator authentication, allowed origins, public runtime URL, public-mode presentation, and later reviewed active-entry/authority/provider secret references. Old model/environment flags do not confer admission. Provider/wallet/biological/external activity stays disabled by default. `/healthz` currently asserts CLOSED and reports workers OFF; that is truthful for this shipped service, not a ready-made future worker health/queue monitor.

Production Node/platform/source hashes must be calculated on the deployed immutable build before grants/scopes are issued. The historical local Webpack build passed; default Turbopack host restrictions were not retested or treated as a code defect.

## 15. Launch-focused security findings

| Finding | Timing / consequence | Current containment |
|---|---|---|
| S1: No authenticated narrow control plane | **CRITICAL BEFORE FIRST AWAKENING** for issuance/revoke/private inspection; extend before continuous life | No public issuance route exists today; dormant endpoints refuse |
| S2: Local DB credentials own/bypass all protections | **CRITICAL BEFORE FIRST AWAKENING** in production | Local audit only; no active deployment authorized |
| S3: No admitted complete real-provider path | **CRITICAL BEFORE FIRST PAID AWAKENING**: actual implementation identity, full billability, secrets, cancellation and error sanitization | Provider OFF; mocks cannot authorize a real request |
| S4: Provider-visible context/disclosure not operationally reviewed/loaded | **CRITICAL BEFORE FIRST PROVIDER CYCLE**; especially richer recall/continuous life | Private operational/legacy data fail closed today; empty legacy collections avoid noted bypass exposure |
| S5: Ambiguity stops but lacks authenticated legal resolution workflow | **CRITICAL RECOVERY PREREQUISITE** for active operation; safety currently achieved by remaining stopped | No automatic retry/reopen; unknown costs retained |
| S6: Rollback/restore can reintroduce historical authority/erase receipts | **CRITICAL BEFORE PRODUCTION ACTIVATION** recovery policy | Exact runtime hashes fence incompatible code, but do not prove monotonic disaster recovery |
| S7: No active worker supervision/meaningful live health | **CRITICAL BEFORE CONTINUOUS LIFE** | Worker not imported at boot; disabled by default |
| S8: Public availability/log hardening | **IMPORTANT BEFORE PUBLIC TRAFFIC / AFTER SMALL CONTROLLED LAUNCH** depending exposure | Generic HTTP errors, size/time bounds; no application rate limiter; DB error message goes to stderr |

Public DTOs are explicit allowlists (`core/v2/public.ts`); browser parsing strips extra fields. The public inventory is `/api/state` (identity/status/counts/namespaced funds/redacted history/saved metadata), `/api/history` (redacted decisions), `/api/brain` (structural graph), `/api/replay` (explicit saved legacy measurements), and `/healthz` (dormant health). Next proxies these fixed routes; development-only preview routes return sanitized fixtures. No memory-content, operator-trace, queue, approval or provider-response endpoint is exposed. Public routes never return operatorTrace/raw intents/episodes/provider bodies. Request proxy endpoint is fixed, redirects refused, and browser URLs cannot choose an arbitrary fetch target; server-configured base URL must still be trusted. No general HTTP tool exists, so this is not proof that later internet tools are SSRF-safe.

Human answers/memory are untrusted data. Source references do not validate instruction truth. Strict schema, independent policy, revision binding and absent external executors contain prompt injection's effect scope. Scientific/credential regexes cannot prove semantic safety or completeness. Constitution principles guide reasoning; enforceable policy is a separate, narrower boundary.

One-shot and continuous planners are supplied by trusted code. A string-matching planner identity does not sandbox a malicious JavaScript callback. Production factory/role/egress controls must preserve that trust boundary. No attacker-facing arbitrary callback loader is currently installed.

This is a source/catalog/evidence audit, not a live penetration test. No vulnerabilities were patched.

## 16. Public observer

Implemented: dormant landing, optional live observer, saved structural C. elegans visualization, explicit historical replay, redacted V2/legacy timelines, separate resource namespaces, memory accounting, responsive/detail views and deterministic copy. `/api/state` derives dormant/reasoning/active/idle/waiting/review-required from durable facts; Pass-1 hardcoded dormancy is repaired. No current event makes decorative neurons fire.

| Surface | Real source and limit |
|---|---|
| State/activity/feed | `readObservation` → `publicState/publicDecision`; latest 20 decisions; meaningful V2 statuses supported |
| Brain/replay | Genuine structural graph; explicit legacy saved frame allowlist; V2 does not generate replay |
| Memory | Separate legacy/episode/assertion counts; no approved excerpts canonically |
| Projects/interests/tasks | Real legacy project count only. Rich detail examples are development fixtures; no newly approved operational-public projection |
| Money | Simulated balance, unresolved/null onchain, null verified revenue; never sum namespaces |
| Private operator trace | Function only, no public endpoint |
| Preview | Development-gated fixture paths; prominently noncanonical/not awakened |

Remaining source-visible issues: header says “Observing saved records” for all nondormant states despite the more accurate main activity text; custom continuous local planner identities become “FAILED OR OTHER PLANNER”; `local_saved` copy calls both reflection and artifact a text artifact; “Why this happened” can refer to the latest completed event while a new cycle is active; the Brain technical explanation mentions fixture-specific missing timestamps even outside a fixture. These are truthful-layer/presentation cleanup targets, not evidence of neural action control. Project count still refers only to preserved legacy projects and must not be marketed as all operational projects.

The current product can display a safe redacted Decision #8 and current waiting/review state. Missing public project descriptions/private memory excerpts are intentional privacy boundaries, not reason to expose more state. Rich project/task/public-content disclosure and full paginated life history are later work. Public UI polish is not the principal awakening blocker. No fresh browser/API review was performed under this audit's no-calls/no-server restriction; historical screenshots are not claimed as current live verification.

## 17. Economy

- **Simulated:** original four ledger entries and $100.75 simulated cash remain stored. This is development money, not bank/wallet holdings or earned real revenue. Current local V2 effects do not run old simulated business-income rules.
- **Onchain:** wallet identity unresolved, no observed balance supplied to current DTO. `SolanaReadOnlyWallet` can perform a bounded HTTPS finalized `getBalance` in separately invoked code; it is not started/admitted by current runtime. No signing, transfer, trading, token creation or transaction confirmation execution is installed.
- **Attributed revenue:** null/no verified source. Injected fee-income adapter contracts do not establish live ClawPump attribution or working financial control. Incoming transactions are not earnings.
- **Operational costs:** prepared provider reservation/usage ledger is separate from simulated cash; no actual canonical provider costs. No infrastructure invoice import, real runway or business/project income accounting is connected.

Genesis may honestly display simulated resources, unresolved wallet observation and no verified earnings. Wallet identity/signing is optional for the first local cycle and should remain disabled. Future economic autonomy is a separate implementation/admission/security project, not missing glue to enable during awakening.

## 18. Biology

Current production facade is **SAVED-OBSERVATION-ONLY**. `SavedObservationAdapter.accept` returns NOT_APPLIED, null value, unchanged snapshot hashes and no runtime capabilities. `advance` throws. Compilation and commit reject applied/non-null/new neural state. The actual historical recording time is resolved independently of latest computational activity. C. elegans source/equations and frozen fly research remain preserved.

Historical decoder labels remain in deprecated code/history and are explicitly disclaimed in public projection. Current service refuses old advance/CLI paths; no decoder label can authorize a current tool. Stage-1 associative learning is a frozen research capability, not a production planner mechanism. Stage-5 conditional orders do not establish biological transmission/action selection. No fly runtime is installed. The observer draws static structure until a user explicitly requests saved data; no ordinary reasoning cycle creates firing.

No material new biological overclaim was found in the active projection paths inspected. Legacy model/planner prose elsewhere must remain unreachable/deprecated rather than be reused as current biological claims.

## 19. Long-run reality

With the database/schema/operator/provider/grant prerequisites completed **and a trusted active invocation wired**, one-shot execution produces at most #8, consumes authority and stops. Merely deploying this repository with a valid record does not invoke the library.

Later, an installed separately authorized local scope plus supervised reviewed local worker and admitted event(s) can run #9+, process due follow-ups and answers, update private projects/tasks/artifacts, then idle. The legacy schedule remains disabled. It continues only while work is due and scope/budgets allow; it does not promise constant thinking. A real LLM-driven continuing organism needs an explicitly reviewed extension of the local-only scope/provider/disclosure integration. That must not be smuggled through a matching planner identity.

| Horizon / risk | Mitigated now | Remaining limit |
|---|---|---|
| First day: duplicate/racing cycles | Row locks, leases, unique identities, atomic commit, source revisions | Target network/process behavior and actual role permissions unverified |
| Provider outage/charged lost response | One attempt, reservations, timeout, unknown liability and stop | Real transport/reconciliation/control path absent |
| Event storm/repeated deferral | Count/window/root/depth/follow-up/attempt limits, due filtering, obsolete target cancellation | Limits require reviewed production values; no event-capacity quota or queue alarm |
| Repeated assistance/reflection/stuck project | Explicit IDs, pending requests, no automatic assistance polling; scope bounds total cycles | Distinct duplicate-meaning requests/reflections are not semantically deduplicated; no guaranteed progress/utility |
| Seven/thirty days | Expiry, revocation, rolling counts, bounded local recovery | Renewal/monitoring/maintenance not implemented; no guarantee of uninterrupted activity |
| 1,000+ cycles | Bounded context and deterministic retrieval tested synthetically | Growing JSON/state history, archive scans, manifest/decision/event/intent/provider storage, no retention/PITR operator tooling |
| 10,000+ archived items | Discovery limit explicitly marked incomplete | Old explicit sources may fall outside scanned window; indexed deep source lookup needed before relying on them |
| Stale external observations | No live ingestion currently active | Future freshness/attribution/egress design remains separate |

JSON growth does not block the first controlled cycle. Unbounded storage, queue/backlog behavior and operational monitoring need staged limits and measurement before claiming continuous 30-day readiness.

## 20. Failure reality

Statuses below separate historical local tests from unperformed production verification.

| Failure | Classification | What actually happens / gap |
|---|---|---|
| Local process crash before claim | SAFE / TESTED | No claim/effect created; original event still eligible |
| One-shot dies after claim before provider request | REQUIRES OPERATOR RECONCILIATION | Claim expiry becomes AMBIGUOUS conservatively; no automatic second attempt |
| Continuous local process dies before commit | SAFE / TESTED | Local transaction effects absent; expired claim retried only within declared limits, fresh fence |
| Process dies during provider request | REQUIRES OPERATOR RECONCILIATION | Unknown whether paid/received; retain liability, no paid retry |
| Process dies after durable provider receipt, before commit | REQUIRES OPERATOR RECONCILIATION | Receipt metadata/hash not a persisted reusable proposal; do not fabricate decision |
| DB error during atomic local commit | SAFE BY DESIGN BUT NOT PRODUCTION-VERIFIED | PG transaction is atomic; lost acknowledgement requires inspecting durable decision/event/grant, not assuming rollback |
| Provider timeout or charged response lost | REQUIRES OPERATOR RECONCILIATION | Mock tests prove unknown-cost stop; actual vendor cancellation/billing not tested |
| Provider malformed output | SAFE BY DESIGN BUT NOT PRODUCTION-VERIFIED | Validation refuses action; durable charge may remain recorded; no fallback. Mock path covered |
| Worker restart with expired local claim | SAFE / TESTED | Fresh-process tests recover within attempt/backoff limits; terminal events do not recommit |
| Operator revokes during local reasoning | SAFE / TESTED | Subsequent checks/commit refuse; fixture tests verify. Authenticated production control still needed |
| Scope expires / wrong runtime / stale revision | SAFE / TESTED | Authority/commit refused; does not reopen execution |
| Deployment rollback/schema mismatch | SAFE BY DESIGN BUT NOT PRODUCTION-VERIFIED | Exact hashes and absent-table/trigger checks fail closed on supported paths; no production compatibility/rollback runbook |
| Database restored from older backup and worker restarted without review | UNSAFE / BLOCKER | Could lose receipts/consumption, expose stale authorization and forget liability; restore must be quiesced and reconciled before admission |
| Observer unavailable | SAFE BY DESIGN BUT NOT PRODUCTION-VERIFIED | Observer has no execution authority; saved DB remains authoritative. Private stop/monitoring must work independently |
| Worker loop DB/claim/recovery throws outside per-cycle catch | SAFE BY DESIGN BUT NOT PRODUCTION-VERIFIED | `run()` rejects/stops rather than fabricating success; production supervisor/backoff/alerting missing |

“SAFE / TESTED” means the specified local fixture semantics were exercised in the verified prior suite, not that this audit replayed them or verified production failures. Ambiguous states are intentionally safe stops but are not a complete operational recovery workflow.

## 21. Completion matrix

Each row has exactly one subsystem status. “First” means the intended provider-backed, strictly local Decision #8; continuous means the later intended reasoning organism, distinguishing current local-only loop where relevant.

| System | Status | Evidence | Local code work remaining | Production work remaining | First blocker? | Continuous blocker? | Post-launch work? |
|---|---|---|---|---|---|---|---|
| Identity | IMPLEMENTED AND VERIFIED | Store, writer guards, canonical/restart evidence | None for current identity | Restore/redeploy proof | Restore prerequisite | Yes: operational continuity proof | Recovery drills |
| Persistence transaction core | IMPLEMENTED AND VERIFIED | `commitV2`, PG race/crash tests | Production-compatible migration/role integration separately below | Storage/network fault verification | Prerequisite | Prerequisite | Growth/retention |
| Biology | IMPLEMENTED AND VERIFIED | Saved adapter, context/commit guards, frozen hashes | None; keep saved-only | Verify assets in image | No new biology needed | No new biology needed | Maintain provenance |
| Memory retrieval | IMPLEMENTED AND VERIFIED | Pass-2/3 tests, archive and retriever | Disclosure integration separately below; eventual deep-source indexing | Read/load behavior at target | No for restricted context | Disclosure for LLM recall | Index/retention |
| Operational Life State | IMPLEMENTED AND VERIFIED | Strict operations/reducers, fixture continuity | Legacy project/provider-context review, not a workflow rewrite | Validate persisted target behavior | Scope-dependent context | Provider disclosure | Growth limits |
| Context compiler | PARTIALLY IMPLEMENTED | `compileContext`, bounded manifest | Review loading, complete provider-context identity/legacy-project scope, explicit disclosure for remaining paths | Approved payload inspection | Yes for intended reviewed LLM context | Yes | Retrieval tuning only with evidence |
| Planner contract | IMPLEMENTED AND VERIFIED | Strict schema/policy, injected tests | Expose complete contract through admitted adapter | Validate vendor output support | Adapter prerequisite | Adapter prerequisite | Quality evaluation |
| Provider abstraction | IMPLEMENTED BUT NOT PRODUCTION-VERIFIED | `ProviderControl`, injected usage/cancel/unknown tests | Trusted real factory and complete request accounting integration | Billing/cancel/failure smoke | Yes, integration | Yes | Usage monitoring |
| Real provider | NOT IMPLEMENTED | Pending config; HTTP prototype not admitted | Transport/secret/count/rate/output wiring | Model/rate evidence, secret, smoke | Yes if LLM | Yes if LLM | Model updates reviewed |
| Policy | IMPLEMENTED AND VERIFIED | `evaluatePolicy`, independent reducer and fence tests | Typed future paid-continuous permissions; no external tool authority now | Role/egress proof | Current local scope adequate | Paid extension required | Future tools separately |
| Intent | IMPLEMENTED AND VERIFIED | A11 integration/finalization tests | Control/reconciliation surface separately | Operator integration | Control prerequisite | Control prerequisite | External effects not implied |
| Local effects | IMPLEMENTED AND VERIFIED | DB reflection/artifact/change commit | None for supported local scope | Target persistence proof | No new executor needed | Local-only adequate | Publication later |
| Event model | IMPLEMENTED AND VERIFIED | Strict envelopes/follow-ups/answer tests | Authenticated ingress integration | Target intake/config | No for one-shot | Yes: integration | Quotas/observability |
| Durable queue | IMPLEMENTED AND VERIFIED | Due/dedup/leases/atomic follow-up tests | Supervision/inspection integration | Install schema and exercise target | No | Yes: installation/integration | Backlog maintenance |
| Continuous authority | IMPLEMENTED AND VERIFIED | `CONTINUOUS_LOCAL_V1`, guards/tests | Paid-provider extension only if intended; operator surface | Scope review/issuance after #8 | No | Yes | Renew/review limits |
| First-awakening authority | IMPLEMENTED AND VERIFIED | OneShotController, SQL seven-to-eight tests | Trusted invocation/inspection/recovery | Install, pin target release, reviewed grant | Yes: integration/authorization | Cannot authorize #9 | None automatically |
| Human assistance storage | IMPLEMENTED AND VERIFIED | `recordHumanResponse`, wake/resolution tests | Authenticated intake and answer visibility | Operator access | Needed if assistance is usable, not for abstention alone | Yes for human loop | Outbound optional |
| Operator control | PARTIALLY IMPLEMENTED | Methods, bearer refusal, private trace | Authenticated narrow interface, actor audit, stop/inspect/reconcile | Identity/role/secrets/runbooks | Yes | Yes | GUI optional |
| Disclosure review | PARTIALLY IMPLEMENTED | Typed MemoryReview, fail-closed audiences | Durable reviews/load/revalidation; operational provider admission | Human category/item review | Yes for provider scope | Yes for useful paid continuity | Public publishing separate |
| Economy | PARTIALLY IMPLEMENTED | Original simulated ledger, separate DTO/usage namespaces | No real accounting source needed initially | None for simulated-only display | No | No for local life | Real accounting later |
| Wallet | PARTIALLY IMPLEMENTED | Read-only adapter; unresolved identity; no signer | No work required for disabled wallet | No binding/calls authorized | No | No for non-wallet life | Separate safe admission |
| Public observer | IMPLEMENTED BUT NOT PRODUCTION-VERIFIED | DTOs, UI and prior canary/browser evidence | Small truthful-copy/projection corrections; optional content display | Live target/private canaries/load | Not principal blocker | Operational status validation | Pagination/polish |
| Applied database schema | IMPLEMENTED AND VERIFIED | Fresh catalog, digest, migrations 001–003 | Do not rewrite canonical history | Verified restore to target | Prepared additions needed | Prepared additions needed | Maintenance |
| Preparation/one-shot/continuous schemas | PREPARED BUT UNINSTALLED | SQL files and fixture installers/tests | Reviewed installer/version/rollback/role procedure | Authorized install in correct order | Prep+one-shot required | Continuous required | Schema evolution |
| Deployment | PARTIALLY IMPLEMENTED | Docker/Railway/Vercel/CI files; dormant main | Active entrypoint, supervision, schema readiness | Target binding/container/secrets/network | Yes | Yes | Resilience drills |
| Monitoring | PARTIALLY IMPLEMENTED | Dormant health, private resource queries, journal | Worker/queue/ambiguity/liability status and alarms | Private monitoring retention/access | Minimal private status required | Yes | Capacity metrics |
| Recovery | PARTIALLY IMPLEMENTED | Local retry and ambiguity inspection | Legal authenticated reconciliation; restore/rollback controls | Backup/restore and vendor reconciliation drills | Yes for operational readiness | Yes | PITR exercises |
| Security | PARTIALLY IMPLEMENTED | DTOs, guards, no external executors | Control/admission/disclosure/role integration | Least privilege, TLS/secrets/egress | Yes | Yes | Availability hardening |
| Internet | NOT IMPLEMENTED | No V2 executor; old helper unreachable | None for initial scope | Keep disabled | No | No for local life | Separate future capability |
| External communications | NOT IMPLEMENTED | No clients/dispatcher; assistance local only | None for initial scope | Keep disabled | No | No for local life | Separate future capability |
| Legacy semantic-brain runtime | DEPRECATED | Old loop/CLIs fenced, labels disclaimed | Never reconnect as authority | None | No | No | Preserve historical evidence |
| Sophisticated continuous planner | MOCK / FIXTURE ONLY | Long-run injected fixture planners; fallback abstains | Real admitted planning connection | Controlled evidence of useful operation | Not needed for bare local test | Yes for intended LLM life | Quality, repetition/progress review |

## 22. Readiness classifications

| Area | Classification | Concrete reason |
|---|---|---|
| CODE READINESS | NOT READY — LOCAL WORK REMAINS | Production operator/provider/disclosure/recovery/active-entry connections missing; local core is substantial and tested |
| DATABASE READINESS | NOT READY — PRODUCTION WORK REMAINS | Original data intact; prepared schemas uninstalled; target roles/restore required, installer preparation also needed |
| DEPLOYMENT READINESS | BLOCKED | Intended target unspecified locally; Docker unavailable; no active service supervision |
| PROVIDER READINESS | NOT READY — LOCAL WORK REMAINS | No admitted real transport/factory/counting/billing/secret path; model choice and smoke follow |
| OPERATOR READINESS | NOT READY — LOCAL WORK REMAINS | Trusted methods exist without authenticated control/reconciliation/disclosure workflow |
| FIRST-AWAKENING READINESS | NOT READY — LOCAL WORK REMAINS | One-shot core works; cannot safely substitute key/config for missing integrations and reviews |
| CONTINUOUS-LIFE READINESS | NOT READY — LOCAL WORK REMAINS | Local controller works; production worker/operator/installation missing; paid planning expressly not admitted |
| PUBLIC-OBSERVER READINESS | READY WITH VERIFIED PREREQUISITES | Redacted local interface can show #8; requires verified target connection/disclosure and current status checks; richer private content is optional |

### Test evidence

Verified prior suite: **387/387 passed, zero failed/skipped**, including 61 Pass-4 tests and retained foundation/memory/Life State/one-shot/provider/privacy suites. Current 164-file final Pass-4 snapshot and all prior evidence-package files match. Prior TypeScript, ESLint and Next Webpack build logs pass. Fresh audit static-check results are recorded in `checks.json`; no fresh integration tests, production build, Docker execution or browser/API calls are claimed.

Coverage includes wrong identities/hash/revisions, two workers, terminal/duplicate refusal, crashes at durable boundaries, restart, revocation, due/obsolete events, backoff/depth/root/count limits, unknown liabilities, 100 local cycles, bounded recall and disclosure canaries. Missing production evidence: real provider transport/billing/cancellation, authenticated operator use, non-owner roles, target deploy/rollback, actual network partitions, production backup restore and sustained traffic. A mocked transport proves enforcement around that mock, not the behavior of an unimplemented real adapter.

## 23. Ordered remaining work

This is a new plan derived from current code; no step is authorized by this audit.

| Pass | Purpose / why now | Local or production | Dependencies | What it unblocks | Must remain disabled |
|---|---|---|---|---|---|
| 1. Narrow operator and recovery foundation | Authenticated actor-bound grant/scope/inspection/revoke/intake controls; explicit legal ambiguity resolution without automatic retry; durable source-hash disclosure reviews. Controls must exist before credentials or active authority are introduced | Local code + isolated tests | Current strict contracts and terminal-state semantics; reviewed resolution design | Safe private administration, consent decisions and recovery | Canonical execution/authority, provider calls, scheduler, wallet/network tools |
| 2. Approved first-cycle context and provider integration | Review minimal identity/history/project categories; load identical reviews at prepare/commit; keep private defaults; implement trusted real adapter/factory, full structured schema, complete-request counting and usage/cost handling | Local code/mocks; operator selects later model/evidence | Pass 1 review path; existing provider ceilings/fences | Coherent, auditable provider-ready one-shot | Live calls, canonical migration/authorization, paid continuous scope |
| 3. Production installation and deployment preparation | Versioned reviewed SQL installation, roles, schema-readiness/rollback checks; one-shot operator runner; target-ready private monitoring. Build/verify container when environment permits | Local first, then named target | Stable Pass 1–2 release; target information | Deployable dormant system with inspectable controls | Genesis cycles, all grants/scopes, external tools |
| 4. Target/backup/least-privilege verification and provider admission | Verify isolated restore and authorized structural installation, Node/build identity, TLS/network/roles; configure reviewed secret; separately authorized bounded non-Genesis provider smoke; rate/token evidence | Production/operator | Named target, reviewed installation, selected provider/model and consent scope | Concrete awakening review package | Canonical planner invocation, Decision #8, continuous worker, wallet/internet/messaging |
| 5. First-awakening authorization and exactly one cycle | Fresh integrity, reviewed context/cost, exact target-hashed grant, human authorization, one invocation, postcommit review | Production, separately authorized | All first-awakening blockers closed | Decision #8 only | Decision #9, paid retry/fallback, continuous authority, all external effects |
| 6. Continuous-life integration/admission | Supervised worker, queue/resource/stop/recovery controls and renewed scope review. Decide whether initial continuous mode is genuinely local-only or add separately reviewed paid-provider/disclosure/budget support | Local isolated implementation then production | Reviewed #8; operator/backup controls; real-provider evidence if used | Safely bounded #9+ with event-driven idle/wake | Unadmitted external effects, biology, wallet, internet, communication |
| 7. Measured growth and optional capabilities | Archive/index/retention, context and event capacity, public approved projects, optional external tools only under new scopes | Local + measured production | Evidence from limited operation | Longer useful operation | Anything not separately admitted |

The next task should be **operator/control, disclosure and recovery integration**, not another UI redesign or an API-key-only pass. Provider adapter work is the next dependency; infrastructure target identification can happen in parallel as an operator decision, without issuing authority. A large operator dashboard is not required. Do not merge first-awakening authority with continuous authority to reduce the work.

## 24. Product reality check

**What is Genesis today?** One preserved dormant organism with seven historical decisions, a saved C. elegans model, an additive computational-life database and a substantial tested local runtime library. Production boot serves observations only.

**What can it actually do in fixtures?** Claim bounded authority, retrieve eligible internal memory, validate proposals, record abstention/defer/help/reflection, maintain projects/tasks/private artifacts and other operational state, accept attributed answers, consume due events, continue across cycles/restarts, and stop on budgets/revocation/ambiguity. Sophisticated fixture planning is supplied by test code, not evidence of an autonomous production LLM.

**What can it not do today?** Invoke an admitted real-provider canonical cycle through shipped entrypoints; receive authenticated operational control/consent through a usable interface; automatically continue canonically; publish/message/browse/trade/sign/pay; acquire new biological computation or use fly research as action authority.

**What if someone only added an API key?** Nothing awakens. No provider is admitted, no grant or scope is created, the runtime remains observational and the HTTP mutation paths refuse. Inconsistent legacy config may instead reject startup. An API key is not execution authority.

**Minimum missing system for a safe Decision #8?** A small authenticated one-shot control/inspection/recovery path, approved coherent disclosure-bound context, a real admitted provider path if LLM reasoning is desired, plus verified prepared-schema installation, production roles/backup and exact release-bound human authorization. Existing one-shot mathematical/transaction fences do not need replacement. A deterministic abstaining first cycle would not need a paid provider, but would not demonstrate live LLM reasoning and still needs control/infrastructure authorization.

**Minimum missing system for safe #9+?** Separately installed/authorized continuous schema/scope, authenticated events and stop/inspection, supervised worker/recovery and verified target. Current local-only loop can then run reviewed local planners. Intended real-LLM continuous life additionally needs explicit paid-planner scope/admission/disclosure integration; the current scope forbids it.

**Optional for initial awakening?** Wallet identity, onchain balance, web research, external messaging, business activity, embeddings, richer public memories/projects, GUI control polish, all-seven-memory disclosure and more neuroscience. None should be smuggled into the launch-critical path.

**What should wait?** Automatic continuous activation until #8 is reviewed; economic/internet/communication effects; biological advancement; capability promotion; speculative scaling rewrites before measured limits. Limited continuous integration may be developed separately, but never auto-enabled by the first grant.

## 25. Final recommendation

Retain the current architecture and frozen research. Complete the production connections around the working local core, beginning with trusted operator/disclosure/recovery controls, then provider and deployment integration. The local event loop is real; the current production organism still cannot operate it merely by receiving a key or a deployment restart.

Final canonical verification: **7 decisions; 0 V2 episodes; execution CLOSED; schedule DISABLED; SAVED-OBSERVATION-ONLY; no continuous authority; no provider calls, wallet actions or external communications during the audit.** Actual final digest: `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`. All canonical rows and audited implementation files remain unchanged. No implementation, installation, authority or awakening was performed.

LOCAL IMPLEMENTATION WORK REMAINS BEFORE PRODUCTION
