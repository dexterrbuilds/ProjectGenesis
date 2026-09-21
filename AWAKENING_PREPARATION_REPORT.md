# Project Genesis — Awakening Preparation Report

Date: 2026-09-20. This report is not an activation grant.

## Outcome

**AWAKENING PREPARATION COMPLETE — BLOCKERS REMAIN**

The isolated safety harness, provider-control mechanics and observer review are complete. Genesis remains dormant. Docker and the actual target host remain unverified; a live provider model, tariff, tokenizer, transport and authorization have not been admitted. Production orchestration remains deliberately unreachable. The first-awakening mode below is a proposal, not an executable activation configuration.

## 1. Canonical preservation

Read-only repeatable-read database exports before and after this pass have identical rows and the required digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

- Original organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Original birth: `2026-09-15T01:56:07.867Z`.
- One organism; **seven decisions/cycles, seven original memories, one project**.
- Original history, four ledger rows, wallet state and biological snapshot unchanged.
- Runtime V1 extension and its existing migration preserved; no canonical schema change in this pass.
- One existing life-event row; **no canonical V2 episode**.
- Execution **CLOSED**; schedule **DISABLED**, including unchanged schedule metadata/heartbeat.
- No other canonical database client at either audit.

Evidence: [canonical-preservation.json](verification/awakening-preparation/canonical-preservation.json). Full exports remain private, ignored and mode 0600 under `outputs/awakening-preparation/`; they are not public report attachments.

The protected-file audit covers the 9,319 previously recorded research/design/neural/data files. Its final result is in [frozen-preservation.json](verification/awakening-preparation/frozen-preservation.json). No research package, Brain Spec, Stage 1–5 artifact, C. elegans equation or connectome was changed. No Drosophila model or biological consumption rule was installed. The constitution, four memory ownership domains and saved-observation-only applicability boundary remain intact.

## 2. Browser review and presentation corrections

A real in-app browser reviewed the Next.js application on desktop (1280 × 900) and mobile (390 × 844). The development-only `/preview` connected to a separate localhost GET-only fixture. The fixture restored genuine historical frame arrays for manual replay, did not advance a neural model, did not connect to the database and did not contact a provider. Its V2 record is uncommitted, explicitly labeled as a fixture, and cannot be mistaken for canonical decision 8.

| View | Observed result |
|---|---|
| Dormant/countdown | Static real-connectome structural map; no activity implied. Absolute September 29, 07:00 UTC deadline. Countdown cannot unlock runtime. |
| Live | Original birth/history counts, dormant life state, saved biology, closed policy and disabled schedule. Loading schedule now says unknown. |
| Brain | Unknown activity until a saved experience is selected; dated historical replay and manual frame inspection. No automatic neural animation. V2 records are excluded from legacy replay buttons. |
| Life | V1 semantic labels retained only under the historical computational-decoder disclaimer. V2 fixture shows event/life/reasoning/policy/outcome layers; no invented neural decision. |
| Money | SIMULATED ECONOMY distinct from ONCHAIN ECONOMY and ATTRIBUTED REVENUE. Unknown onchain balance and attribution remain null. |
| Memory | Counts and ownership boundaries visible; private memory contents withheld. |
| Science | Saved-only compatibility, unknowns, schematic anatomy limits and unsupported interpretations disclosed. No new fly capability claimed. |

Corrections made: uncommitted V2 label; fixture banner; explicit reasoning-source category and no-external-execution label; unknown schedule while loading; legacy-only replay selection; wrapped mobile navigation now reserves its height instead of overlapping the heading. The corrected mobile Brain view has no horizontal overflow (390 px viewport and document width), and a 32 px gap between navigation and heading.

Screenshots: [desktop dormant](verification/awakening-preparation/browser/desktop-dormant.png), [desktop Life/V2 + legacy](verification/awakening-preparation/browser/desktop-life.png), [desktop Money](verification/awakening-preparation/browser/desktop-money.png), [corrected mobile Brain](verification/awakening-preparation/browser/mobile-brain-corrected.png). Other view screenshots are in [browser evidence](verification/awakening-preparation/browser/). Earlier full-page captures are pre-spacing-correction evidence and may contain browser stitching duplication; the corrected viewport capture is the final mobile layout reference. These are development captures, including the Next development indicator.

Agent browser review is complete. Final human/operator acceptance of the screenshots and disclosure scope remains pending; this report does not claim a human has already approved them.

## 3. Privacy and trace ownership

Public projection is an explicit allowlist. It withholds private memories, project/artifact contents, raw working context, planner rationale, pending payloads, approval details, credentials and operator identity. The public reasoning source is a category, not the provider response body. Historical labels are wrapped at projection time; their source records remain untouched.

Seeded private rationale/memory/approval markers were absent from rendered fixture views and actual public HTTP responses through the Next proxy. State/history/brain response field lists and sizes are recorded in [public-response-review.json](verification/awakening-preparation/public-response-review.json). The browser blocked direct navigation to JSON, so those response bodies were separately read by a local HTTP client; this is not a claim of browser network-panel inspection. Existing public projection and context privacy tests also pass.

`operatorTrace` is a private projection helper only: bounded stored rationale (maximum 2,000 characters), provenance/context manifest and decision stages. It does not export hidden provider reasoning or raw working context. No operator trace HTTP endpoint was added; any future endpoint must authenticate independently. Public observations continue to show statuses instead of private rationale or unpublished artifact text.

## 4. Docker verification

**DOCKER_VERIFICATION = BLOCKED_BY_ENVIRONMENT**

Neither Docker nor Podman is available on PATH; the usual Docker application/Homebrew/local executable locations were also absent. No image build, container boot, container restart, Node 24 container test or target-platform result is claimed.

The Dockerfile now includes the extracted shared `server/commit-v2.ts` import. Intended target remains `node:24-bookworm-slim`, non-root `node`, `CMD ["node", "runtime/main.ts"]`. Local verification used Node v26.1.0, which does not substitute for the Node 24/container gate.

The existing standalone Node boot/restart test runs against an isolated database, verifies unchanged state and closed execution, and passes in the full suite. It does not start canonical Genesis. A future Docker test must use the isolated copy, explicitly pre-migrate it, verify no boot initialization/migration/worker/heartbeat/cycle, restart, and compare identity/state. No container may be pointed at the canonical database for this check.

## 5. Target-host readiness

Repository configuration was inspected; no deployment was performed.

| Setting | Intended configuration / verification |
|---|---|
| Build | Railway Dockerfile builder; `npm ci --omit=dev` in runtime image |
| Start | Docker CMD `node runtime/main.ts`; no startup migration command |
| Health | `/healthz`, 120-second Railway health timeout; requires dormant extension |
| Restart | `ON_FAILURE`, maximum 10 retries |
| Storage | Postgres required; no filesystem/in-memory fallback |
| Migration | Explicit reviewed command; boot only reads an existing original organism and V1 extension |
| Execution | Service/CLI/API remain hard closed even if environment flags request activity |
| Workers | No scheduler, heartbeat, wallet observer or external observer started by boot |
| Provider | No production provider construction/dispatch; credentials alone do not grant authority |
| Signing | No signing/external executor installed |
| Exposure | Public allowlisted GET observations; mutation requests require bearer authorization/origin checks and still hit the closed gate; no unlock route |
| Secrets | Required database URL and operator token remain server-only; no values included here or in screenshots |

A read-only Railway status request returned **No linked project found**. No project was linked or guessed. Consequently remote service/region/platform, actual build overrides, secret values/presence, private networking and deployed health cannot be attested. Operator must identify the intended Railway project/environment/service before target-host verification.

Legacy environment configuration fields remain parsed for compatibility; they cannot enable workers or authorize a model in this build. Future provider selection must use the reviewed durable grant, not `OPENAI_MODEL`. The separate frontend still builds independently for Vercel. No GPT Sites runtime/hosting integration was added.

## 6. Existing wallet identity

**WALLET_IDENTITY = UNRESOLVED**

The original simulated wallet record is preserved. Repository configuration references are placeholders/tests; local operator environment has no configured Solana public address/network/RPC identity. There is no linked deployment record establishing ownership. No address was guessed, generated, inferred from transactions or bound to Genesis.

Required operator input: the **existing** Solana public address, network (`devnet` or `mainnet-beta`), and an authoritative operator-controlled ownership/provenance reference identifying it as Genesis 001's wallet. No private key is required or requested. A reviewed binding would record organism ID, chain, network, address, source/reference, verification method, effective timestamp and proposed/verified status. No binding record with a fabricated address was created.

This blocks wallet-specific operation only. A first cycle with wallet RPC/signing/economics disabled can proceed through review without resolving it.

## 7. Provider controls

Implemented `server/provider-control.ts` and isolated durable grant/attempt tables. Nothing is enabled in production; the tables were installed only in test schemas.

| Requirement | Implemented behavior |
|---|---|
| Permission/model | Context execution + LLM permission and an enabled, unexpired, reviewed exact-model grant; empty/invalid grants refused |
| Cost/token bounds | Reviewed compatible counter on the complete submitted text; max input/output tokens; integer micro-USD reservation before dispatch; per-call, cumulative per-cycle and UTC-day ceilings |
| Budget concurrency | Transaction/advisory lock serializes reservations; liabilities count across model grants; unresolved liabilities survive midnight |
| Attempt identity | Unique durable attempt ID, cycle/lease/revision binding, context hash, grant hash and counter provenance |
| Dispatch | Rechecks authority and bindings before transport; output token limit conveyed to injected transport |
| Timeout/revocation | Abort signal and bounded timeout; authority/grant monitoring during request and recheck before accepting response |
| Retry | No automatic retry; total attempt limit; unresolved/in-flight attempt blocks retry; no implicit fallback after real-provider failure |
| Ambiguity | Timeout/disconnect/crash leaves unknown liability, not zero cost or fabricated success |
| Reconciliation | Explicit operator/reference plus bounded cost required; unknown outcome never becomes a fabricated proposal |
| Response provenance | Model, request/response IDs, context/proposal hashes, returned usage and accounted cost; raw exceptions and response bodies not logged |
| Proposal authority | Provider output still passes proposal validation, policy and the lease/revision/lock commit fence |

Accounting tests use an explicitly invented **TEST ONLY** tariff and exact mock token counter. They do not validate a real provider's pricing, tokenizer, billing or cancellation semantics. A local abort cannot prove a remote request was not billed. Recovery is a conservative explicit maintenance operation, not an automatically running worker; it must be used after exclusive shutdown of request processing and converts in-flight reservations to unknown. Charges above a reservation require investigation, not truncation to the budget.

The existing `LanguagePlannerV2` no longer defaults to unrestricted network fetch: absent an injected transport it fails with `DURABLE_PROVIDER_CONTROL_REQUIRED`. No native paid transport or grant is wired into boot. Real enablement still requires reviewing a model, tokenizer, rate card (including any additional billable usage), secret handling and transport mapping. Official [Responses API reference](https://developers.openai.com/api/reference/typescript/resources/responses/methods/create) documents output-token limits/usage; it does not identify a cost-safe model/tariff for Genesis by itself.

**Live provider calls during this pass: zero. External provider cost: $0.00.**

## 8. Active-cycle safety harness

`server/isolated-cycle.ts` accepts only database `genesis_runtime_v1_test`, schema names beginning `awakening_test_`, and an organism ID beginning `fixture-`. Test setup rejects canonical `DATABASE_URL`; spawned crash processes receive only the dedicated test connection and fixture metadata. Each test owns and drops its schema. The sanitized fixture contains no canonical secrets/private prose. All planning is deterministic or an injected mock; no wallet RPC, internet, communication or financial executor is used.

The harness exercises the actual V2 context/compiler/prepareCycle/policy/local-effect preparation and the shared atomic commit helper now referenced by production's still-unreachable `commitPrepared` method. It does not substitute a fake commit result. Draft supporting tables are not registered as a canonical migration or boot action.

**110 tests passed, zero failures, zero skips**: 74 prior tests plus 36 new active/provider cases. TypeScript, ESLint and the Next.js webpack production build pass. Logs are in [verification/awakening-preparation](verification/awakening-preparation/).

| Scenario | Quantitative/observable outcome |
|---|---|
| Normal local reflection; local artifact | Fixture decision count 7 → 8; one atomic episode; artifact only in permitted local life state |
| Abstain / defer / assistance | Non-execution recorded; defer stays deferred; assistance stays a local approval request |
| External proposal | Approval-required intent remains awaiting approval; zero dispatches |
| Policy denial | No local artifact saved; denied action remains unexecuted |
| Planner failure | Failure record, null proposal; no fallback |
| Cancellation before/during planning or before commit | Rejected; fixture remains at seven decisions |
| Execution lock closes while pending | Commit/check rejected; no eighth fixture decision |
| Stale revision / stale lease | Commit rejected; no life event added |
| Two workers racing | Exactly one lease claimant; losing worker cannot proceed |
| Duplicate commit | Second commit rejected; exactly one additional fixture decision |
| Process crash before commit | Child exits 77; seven decisions, zero V2 episodes |
| Process crash after durable intent | Child exits 77; one non-executed intent persists, zero V2 episodes; restart fabricates no success |
| Restart after stale crashed cycle | Same logical cycle ID cannot be reused; only a new explicitly chosen ID can claim after expiry |
| Stale/cancelled provider dispatch | Zero transport invocations |
| Approval payload mismatch | Approval rejected |
| Provider timeout/ambiguous/revoked/cancelled/usage mismatch | Unknown outcome and retained cost liability; no automatic retry |
| Token/model/budget/permission failures | Zero transport invocations |
| Budget race | Exactly one durable reservation |
| Second grant attempting daily-budget bypass | Zero second-cycle transport calls; first unknown liability retained |
| Invalid expiry / wrong cycle / changed context | Refused before transport; unrelated reserved attempt left intact |

No claim of exactly-once irreversible external effects is made. External dispatchers remain absent. The crash-after-intent test demonstrates the durable pre-effect boundary and honest restart status; it cannot validate an executor that does not exist. The lease/revision fence is transactional for local commit. Provider cancellation is cooperative with a final authority recheck; it cannot revoke an already received remote request.

During implementation, a syntax error in newly added test code temporarily stopped validation; it was corrected and the complete suite rerun. Those intermediate logs remain in ignored preparation outputs. No canonical mutation or frozen scientific defect was involved.

## 9. Proposed first-awakening mode

[config/first-awakening-v1.proposed.json](config/first-awakening-v1.proposed.json) defines **GENESIS_FIRST_AWAKENING_V1**, status `PROPOSED_NOT_AUTHORIZED`. All enable switches remain false. It is not read by the runtime as an activation instruction.

Proposed scope after separate review and authorization:

- Exactly one manually initiated computational cycle; scheduler remains disabled.
- Read approved identity, original history metadata, constitution, eligible episodic/semantic memories, current time, project/task/resource state and permissions.
- Biological applicability `not_applied`; saved observation reference may be shown as historical provenance only.
- Authorized planner may propose abstention, deferment, local reflection, a safe local artifact or a locally recorded request for human assistance. No scripted outcome or narrative.
- Local artifacts are bounded records in Life State; no shell, publishing or external filesystem execution is implied.
- After the one authorized cycle: execution CLOSED and schedule DISABLED. This one-shot activation/relocking path is **not implemented/enabled by this pass** and needs separately reviewed implementation/authorization before use.

Disabled: biological advancement; wallet RPC/signing/transfers; trading/token launch/ClawPump; purchases/hiring; external messages/posts; browser automation; internet/research access; arbitrary shell; external effectful tools.

Proposed external ceiling: **$0.05 total**, at most one provider attempt, also capped at $0.05 for the cycle/day. Proposed token bounds: 12,000 input, 1,200 output; request timeout 25 seconds within a proposed 60-second lease. These are operational caps, not a model price quote. Reservation must refuse if the eventual reviewed tariff/counter cannot fit them. Model allowlist is empty and pricing/token-counter evidence is null until reviewed. Deterministic planning has zero external provider cost. This report authorizes neither route.

## 10. Neutral event and observability

[config/first-awakening-event.schema.json](config/first-awakening-event.schema.json) specifies a strict factual event envelope; **no event instance was emitted**.

Fields: schema/event IDs; explicit activation authorization reference; observed time; existing organism ID/birth; last recorded life-event time; elapsed wall time (nullable); constitution hash; seven cycles before; `biologicalStatus: not_applied`; wallet binding status; approved context references; permission-manifest hash.

Elapsed time since the last record is not proof of biological sleep or a measured continuous subjective experience. The compiler must preserve that distinction. Context references supply capabilities, unavailable operations, unresolved wallet status, projects/tasks and separate resource namespaces; they must not inject reward, danger, scarcity, curiosity, hunger or another hidden biological objective. This schema does not override the existing context compiler or become a biological stimulus.

Proposed eventual trace:

`AWAKENING EVENT → BIOLOGICAL: NOT_APPLIED / HISTORICAL SAVED STATE → COMPUTATIONAL LIFE CONTEXT → PLANNER SOURCE → PROPOSAL / ABSTENTION → POLICY → LOCAL ACTION OR NON-EXECUTION → OUTCOME → MEMORY / LIFE-STATE CHANGE`

Public: statuses, bounded source categories and appropriately reviewed outcomes; no private payloads. Operator: authenticated provenance/context manifest, bounded stored rationale and proposal/policy/outcome details. Neither exposes hidden provider reasoning. Simulated accounting, observed onchain facts and attributed revenue remain separate; incoming funds alone never establish revenue.

## 11. Readiness gates reassessed

| # | Existing gate | Current status |
|---|---|---|
| 1 | Reviewed implementation, constitution, policy, named mode | **PARTIAL** — preparation implemented; proposed named mode and operator review pending; no constitution change |
| 2 | Migration and preserved identity/history/wallet/snapshot | **PASS** — exact canonical digest and row equality; no preparation migration applied |
| 3 | Default-closed execution and disabled schedule | **PASS** — canonical CLOSED/DISABLED; boot/restart/environment cannot awaken it |
| 4 | Evidence integrity and honest capabilities | **PASS for saved-only mode** — frozen files retained; no new biological claim/operator |
| 5 | Memory/context provenance/privacy | **PASS for current tested scope** — public allowlist, private-canary checks, bounded private helper; future operator endpoint not implemented |
| 6 | Policy/approval/idempotency/crash/cost | **PASS in isolated local/mock harness; PARTIAL for live use** — native transport/admitted tariff/counter/grant and reviewed production one-shot path still required |
| 7 | Authoritative wallet binding | **UNRESOLVED** — blocks wallet capabilities, not proposed non-wallet first cycle |
| 8 | Public labels/DTOs/traces | **Agent browser and automated review complete; HUMAN REVIEW PENDING** |
| 9 | Independent infrastructure/build/restore | **PARTIAL** — tests/build/Node restart pass; Docker environment blocked and Railway target unlinked |
| 10 | Separate authorization for named awakening | **NOT AUTHORIZED** — no unlock or first cycle occurred |

Remaining blockers are explicit: human review; Docker/Node24 image verification; identification and read-only verification of intended Railway deployment; separate review of production preparation-schema migration and one-shot orchestration; admission of a real provider transport/model/tokenizer/tariff/grant if a paid planner is chosen; and final named-mode authorization. No missing wallet identity needs to be worked around for a non-wallet cycle.

## 12. Exact implementation scope in this pass

New files:

- `server/provider-control.ts`: grant/reservation/attempt/timeout/reconciliation control.
- `server/commit-v2.ts`: shared fenced local commit.
- `server/isolated-cycle.ts`: dedicated test-only orchestration harness.
- `runtime/preparation-schema.sql`: three draft supporting tables, test-only installation.
- `tests/awakening-active.test.ts`: 36 active/provider cases.
- `tests/support/active-fixture.ts`, `crash-worker.ts`, `observer-fixture.ts`: isolated test/review tools.
- `tests/fixtures/genesis-dormant-sanitized.json`: sanitized copy with saved brain state, not a new canonical organism.
- Two proposed files under `config/first-awakening*`.
- This report and separate sanitized evidence under `verification/awakening-preparation/`.

Modified files:

- `server/life-store-v1.ts`: delegates unreachable prepared commit to shared fence.
- `Dockerfile`: includes shared commit import.
- `core/v2/planner.ts`: disables implicit native provider fetch.
- `core/v2/public.ts`: safe reasoning-source category and private bounded trace helper.
- `components/live-observation.tsx`: truthful fixture/V2/loading/replay presentation.
- `app/globals.css`: mobile navigation spacing.

Other dirty files predate this pass and are not claimed as new preparation work. Previous Runtime V1 reports and frozen research conclusions remain historical records.

## Final confirmation

Genesis 001 remains unchanged, with **seven canonical decisions**, **CLOSED execution**, **DISABLED schedule**, **SAVED-OBSERVATION-ONLY biology**, no live provider call, no external executor, no wallet action, no new neural advancement and no canonical V2 cycle. The observer/test servers are temporary review tools, not autonomous Genesis workers.

**AWAKENING PREPARATION COMPLETE — BLOCKERS REMAIN**
