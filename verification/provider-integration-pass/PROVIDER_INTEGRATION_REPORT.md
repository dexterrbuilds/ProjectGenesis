# Project Genesis — Pass 6: Provider Integration & Reasoning Boundary

## 1. Summary

Implemented a provider-neutral, durable reasoning path around Runtime V1's existing memory, disclosure, one-shot, policy and commit boundaries. The complete request is the accounting object and transport body. Admissions resolve pinned implementation code, rather than accepting a caller's labels as proof. Validated proposals survive process death; uncertain requests retain liability and cannot retry.

**516 tests passed, 0 failed, 0 skipped:** all 446 prior tests plus 70 new provider integration tests. TypeScript, ESLint and the Next.js Webpack production build passed. The final canonical export is identical to the initial export.

This is code integration verified with disposable PostgreSQL fixtures and mocked/injected transports. It does **not** establish compatibility with an unspecified vendor API or validate a production tokenizer/tariff. The implemented HTTPS transport uses the explicitly specified neutral JSON gateway protocol. A reviewed endpoint implementing that protocol can later be admitted without rewriting the organism runtime; a native vendor API using a different protocol requires a reviewed adapter module. No production provider/model/secret/admission was selected, supplied or tested.

## 2. Canonical preservation

The read-only before/after exports both produce:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

Every canonical table and row matches. Organism ID `817e772c-827e-48fc-8e35-6504cb2a8d2d` and birth `2026-09-15T01:56:07.867Z` are unchanged. Seven decisions, seven legacy memories, original project/ledger/milestones/snapshot persist. There are zero V2 episodes; the one existing administrative Life State event is not a V2 cycle. Execution CLOSED, schedule DISABLED, biology SAVED-OBSERVATION-ONLY. No authority, disclosure review, provider admission or attempt schema/record was installed canonically.

Private complete exports remain mode 0600 under `outputs/provider-integration-pass/`; this report package contains only sanitized counts/digests and comparison results. All 9,319 frozen files and seven prior verification packages verified unchanged; see `frozen-preservation.json`. No historical rows were repaired or rewritten.

## 3. Provider architecture

`compileContext` → disclosure manifest → `ReasoningRequest` → `ProviderControl.reasoningPlanner` → `ReasoningControl` → durable reservation → static admitted adapter → immutable receipt → strict Proposal → existing independent policy/intent → `commitV2`.

`OneShotController.admittedReasoningPlanner` binds the stored admission to the original exact grant. The returned planner is admitted by the controller, not by event text. `resumeReceived` reconstructs a preparation from durable receipt without requesting another response; it does not commit automatically. There is no new public API, scheduler, runtime startup path or authority issuer.

## 4. Adapter contract

`server/reasoning/contracts.ts` and `factory.ts` define provider/model identity, adapter version/hash, request format, closed output schema/hash, reasoning settings, timeout, cancellation result, usage categories, request/response IDs, secret reference and rate-card identity. Static implementations: `fixture-v1` and `json-gateway-v1`.

The production transport sends HTTPS JSON with redirect refusal, an AbortSignal and a 64-KiB response bound. It ignores provider headers and never persists arbitrary metadata. Endpoint provenance, DNS/egress/retention policy and conformance to the gateway's ceiling/retry contract still require production review.

## 5. Reasoning request

`server/reasoning/request.ts` defines one immutable representation binding organism/cycle/event, context, disclosure, runtime, constitution, policy, permissions, execution authority, admission, planner contract, output schema, timestamp, timeout, maximum attempts, reservation, complete wire body/hash and accounting evidence. Its digest excludes only its own digest field.

The request is persisted before dispatch. SQL rejects replacement of its contents, context, fence, owner, lease expiry, reservation, admission/model or protocol identity. A changed body, timestamp or binding changes the request identity. Receipt replay independently verifies the stored hash/body and the current compiled context.

## 6. Complete request accounting

`completeWire` is the single serializer used by both accounting and send. It includes versioned instructions, full context, output schema, reasoning configuration, model/planner/admission identity, output and billable-category limits, monetary ceiling, zero retries, empty tools and `store:false`.

The sanitized inspection example has **4,939 context bytes and 19,625 complete request bytes**. Counting only context would omit most of this request. The fixture's independently declared fixed input bound is 12,000 fixture units; this is not a production token measurement. The example worst-case reservation is 8,503 micro-USD using explicitly fictional rates. The inspection makes zero sends and creates no grant, claim or decision.

## 7. Proposal schema

The complete JSON Schema is derived from the existing strict Zod contract, including the local LifeChange operation union and bounds. One-shot exposure excludes continuous follow-ups and external/financial tools. Unknown keys/nodes/operations fail; no repair or guessed intent is used. Semantic refinements, provenance/citations, scientific wording and policy are independently validated on the server.

Only an already validated canonical Proposal can be stored as accepted/replayed. Malformed output stores rejection/hash/usage evidence, not arbitrary provider text. Its receipt cannot turn into voluntary abstention or a successful decision.

## 8. Secret boundary

Production `environmentSecrets` resolves only `env:GENESIS_PROVIDER_*` references, with generic failure for absent, malformed or fixture/test-only credentials. Fixture injection is refused outside the dedicated test database/schema. Secrets are transport-header values only; they are excluded from context, attempts, receipts, audit, decisions, Life State, artifacts and diagnostics. Exact secret echo and credential-like response content fail before persistence.

No real key was loaded or supplied. Header/body/error canaries use deliberately fake strings. This is an application boundary, not a claim to defend against a compromised process, database owner or arbitrary encoded exfiltration by an admitted malicious endpoint.

## 9. Admission model

Prepared durable records have PROPOSED → ADMITTED → REVOKED (or PROPOSED → REVOKED) status with append-only payload identity and an authenticated audit reference. `MANAGE_PROVIDER_ADMISSION` guards private propose/admit/revoke operations. Mutation requires an exact current row hash; admission and audit commit atomically.

Factory/counter/schema/instruction hashes are recomputed from repository implementation. Unknown provider/adapter/format/schema/counting identity fails. Runtime, constitution, policy, audience, category definitions/bounds, rate card, secret reference, lifetime and all budgets are bound. A grant separately pins exact admission/provider/model and cannot exceed its own one-shot limits. Admission is not execution authorization.

## 10. Rate-card model

Rate cards declare every billable category, unit, integer rational micro-USD rate, maximum units, evidence reference and canonical hash. BigInt arithmetic rounds each category upward; categories must be unique and complete. Input/output are mandatory boundary categories; other categories are explicitly provider-defined.

Tests exercise input/output/reasoning/request charges with fixture rates. Missing, extra, noninteger, negative, excessive or unknown usage is never zero cost. Such a response leaves the reservation outstanding and blocks commit. No production pricing is provided.

## 11. Counting/budget model

Implemented strategies: conservative UTF-8-byte estimator; reviewed fixed worst case; reported-only (refused for dispatch because it cannot prove an advance bound). No exact tokenizer is claimed. Evidence must cover wrappers/transformations at the proposed endpoint, the admitted wire-size domain, every charge category and enforcement of supplied ceilings.

Complete wire size is independently bounded (at most 256 KiB in this implementation). Request input/output and per-attempt/per-cycle/daily limits all apply. Reservation uses all category maxima, not favorable expected usage. Unknown/in-flight liabilities survive midnight. Existing one-shot monetary/token caps remain unchanged; this pass does not choose a new final budget.

## 12. ProviderControl integration

The existing control surface now exposes `reasoningPlanner`; it delegates to the new request/receipt machinery and shares the existing durable attempt ledger and budget advisory lock. There is one attempt per logical cycle, zero automatic retries and no fallback model/provider. Missing secret, invalid bound or admission fails before send.

Old injected `OneShotController.providerPlanner` remains only for disposable regression fixtures. Production commits require a version-2 receipt. The old `LanguagePlannerV2` HTTP-shaped prototype is not admitted by the production one-shot path.

## 13. Durable response design

`genesis_provider_receipts` stores request/admission identity, provider request/response IDs, response hash, canonical validated Proposal and hash (or rejection), usage, cost and receipt time. It does not store raw provider headers, chain-of-thought or unbounded bodies. Immutable receipt and attempt settlement are one transaction; response IDs cannot silently replace an existing receipt.

A real child process prepared a response and exited before commit; a fresh process/controller reconstructed the identical preparation and committed once without a second send. Replay requires the original still-valid authority/lease, current revision, identical context/disclosure and admitted implementation. Once these fences expire or are revoked, receipt presence does not authorize a commit.

## 14. Worker/dispatch ownership

Attempts persist process owner, original cycle/lease fence and bounded request lease expiry. Dispatch uses a status/owner/expiry compare-and-set. No other process can reuse the attempt to send again. Lease renewal is unnecessary for a bounded ≤25-second call under the existing one-shot lease; no automatic takeover exists.

`recover()` leaves healthy version-2 reservations/dispatches untouched. Expired unresolved records become unknown with liability retained. Older unleased fixture records retain their existing conservative recovery semantics. Received receipts are not downgraded. Tests cover another worker starting during dispatch and refusing duplicate sends.

## 15. Cancellation semantics

The adapter contract distinguishes SUPPORTED_CONFIRMED, SUPPORTED_UNCONFIRMED, UNSUPPORTED and ALREADY_COMPLETED. The neutral HTTP adapter can abort locally but reports unconfirmed remote cancellation. Fixture adapters exercise confirmed and uncertain cancellation. Neither releases billed liability merely because cancellation was requested or acknowledged.

One-shot provider preparation uses the provider control's own stop/settlement path. A redundant wrapper race was removed for this path so cancellation returns only after durable liability handling is attempted. If the database is unavailable, durable dispatch evidence still prevents retry.

## 16. Error classification

Bounded errors include authentication, rate limit, before/after-dispatch timeout/network categories, provider 5xx, malformed response, schema violation, unknown usage, cancellation uncertainty, configuration and admission mismatch. No raw exception/header/body is emitted in planner errors or public traces. Provider errors escape preparation as `InterruptedCycle`; they do not fabricate a failed or abstaining Decision #8.

A nominal “before dispatch” error reported from inside an invoked transport remains potentially billed. Classification alone never proves no dispatch. Local pre-send failures and actual may-have-sent failures use different durable states; only proven local non-send can record zero cost.

## 17. Disclosure enforcement

Pass-5 reviews are mandatory for this path. Before reservation and immediately before transport, checks validate context hash, current review epoch, source hashes, review versions/expiry, audience and revision. During dispatch, polling detects revocation/expiry and requests cancellation. Current disclosure is checked again on replay and independently at commit.

Tests cover source change, review expiry, review revision change, admission revocation and execution revocation. Already sent data cannot be retracted. Liability survives; stale preparation cannot commit. No canonical memory or project disclosure was approved in this pass.

## 18. First-cycle factual context

The provider context retains immutable ID/name/birth/count, constitution, factual event/time, computational execution/rhythm state, resource namespaces, unresolved wallet status, permission scope, saved-only biological limitations and supported local operations. `Genesis 001` is explicitly labeled a product designation; canonical identity remains the persisted ID/name/birth. No unsupported Experiment 001 identity or autobiographical content is added.

Unreviewed canonical memories/project metadata and private operational details remain excluded. The added designation explanation is provider-only: applying it to local contexts displaced a historical artifact at the existing 12,000-byte bound, which the retained 100-cycle regression test detected. Limiting it to provider context restored the existing local selection without changing tests or budgets.

## 19. Provider instruction contract

Versioned `INSTRUCTIONS` identifies the model as a bounded reasoning component using supplied identity/history/constitution/permissions. It distinguishes uncertainty, past experiences and unverified assertions; rejects invented memories, biological motivations and unsupported external outcomes; treats event/memory/human text as untrusted data; permits abstention/defer/assistance; requires only structured output.

No wealth, business, trading, entertainment, engagement, continuous-operation or personality objective was added. Hidden reasoning is neither requested nor stored. The bounded Proposal rationale remains model output, not a neuronal explanation or chain-of-thought.

## 20. Factory

A static registry resolves exact reviewed code hashes. Caller adapter IDs/hashes cannot nominate arbitrary functions. The production transport is neutral HTTPS JSON; mock transport selection/secret injection/send counters are confined to disposable fixture targets. Environment-selected model names cannot bypass admission or grant binding.

Endpoint/model/protocol conformance still requires a real production review and separately authorized smoke test. Provider-specific adapters may be added later without changing organism policy/intent/commit logic, but are not falsely represented as already implemented.

## 21. Mock adapters

Fixtures use the same adapter interface, serializer, counter, admission, reservation and receipt path as production. Scenarios include valid local reflection, abstain, defer, assistance, malformed JSON, invalid schema, timeout, network loss, 5xx/rate limit, missing/excess/extra usage, confirmed/uncertain cancellation, duplicate response identity, wrong admission and secret echo.

Injected database acknowledgement failures exercise reservation, receipt, reconciliation and final commit independently. HTTP transport tests replace `fetch` in-process and verify exact body and sanitized failures; they make no HTTP request. These are code tests, not provider integration claims.

## 22. One-shot integration

Disposable fixtures start with seven decisions and exact reviewed fixture admission/grant. Success creates at most decision eight, consumes the grant, leaves CLOSED/DISABLED and creates no continuous scope. Duplicate claim/commit is refused. Provider failure creates no decision. Unknown dispatch cannot retry.

Crash/receipt replay, revoked disclosure/admission/authority, source changes, expiry, duplicate response IDs, excessive cost/unknown usage and lost commit acknowledgement are tested. A commit whose acknowledgement is lost remains one committed decision, not a reason to create decision nine. No canonical cycle was run.

## 23. Continuous compatibility

`CONTINUOUS_LOCAL_V1` remains local deterministic, `llm:false`, zero provider attempts/cost and no paid adapter selection. Existing continuous tests, including the unchanged 100-cycle lifecycle/recall test, pass. No paid scope, new scheduler mode or continuation authority was added.

The ReasoningRequest/fence interface is reusable by a future independently specified paid mode; this release does not admit such a mode. Shared code changes alter runtime hashes, so later grants must be issued against this exact reviewed runtime rather than old hash labels.

## 24. Operator integration

Existing private authenticated CLI/library gains admission propose/admit/revoke/inspect and bounded attempt/receipt inspection, using existing MANAGE_PROVIDER_ADMISSION / INSPECT_RECOVERY capabilities. The same actor rechecks, exact target hashes, transactional audit and secret-free diagnostics apply. No GUI or public mutation route was added.

Inspection exposes owner/lease/status, request/admission hashes, usage/reservation/cost, bounded errors/cancellation, response identity and receipt validation/proposal hash. It does not expose raw context, provider body or secret. Existing reconciliation records billing evidence without retry or reopening authority.

## 25. Future smoke-test command

`runtime/provider-smoke.ts` is prepared **and was not executed**. It requires explicit private production authentication, enabled capable actor, separately admitted compatible tiny-output configuration, exact authorization/admission/wire hashes, expiry and monetary limit, external credential, and an owner-only private journal directory.

It uses only a fixed sanitized non-Genesis context; creates no decision/authority/schema/DB mutation; creates an exclusive fsynced 0600 journal before one send; bounds output to ≤128; and records billing evidence separately. Reusing authorization identity refuses. Fixture/test-only production credentials refuse. Stopped/ambiguous requests remain review-required. See `runtime/PROVIDER_INTEGRATION.md` for prerequisites, fields and command. Live transport/token/usage/cancellation tests are deliberately deferred.

## 26. Privacy/secret canaries

Secret echo and unknown error tests verify fake credential strings do not enter attempts, receipts, audit, decisions, Life State or recovery tables. Receipt allowlists exclude headers/raw body. Existing public projection/private-memory/provider-canary tests all remain in the full passing suite. Inspection outputs do not include context or proposal body. No raw canonical memory, human answer or operator credential is included in this evidence directory.

The fixture inspector reports hashes/counts/references only. No actual secrets were available to persist. This does not claim that a future operator can skip endpoint/disclosure/security review.

## 27. Failure behavior

| Boundary | Verified behavior |
|---|---|
| Before reservation / missing secret | No send, no new decision |
| Reservation durable, acknowledgement lost | No automatic dispatch/retry; reserved/unknown liability retained |
| Healthy request / second worker | Recovery leaves it active; second send refused |
| Request may have left process / 5xx / timeout | Unknown liability, no retry, seven decisions |
| Response received but not durable | Existing dispatch evidence requires reconciliation; cannot replay an absent receipt |
| Receipt durable / process exits | Canonical validated proposal reconstructs under original live fences |
| Invalid proposal | Rejected receipt, no repaired output or fabricated abstention |
| Missing/excess/extra billable usage | Unknown cost, full reservation retained, commit refused |
| Admission/authority/disclosure revoked | Subsequent acceptance/replay/commit refused |
| Receipt commit acknowledgement lost | Receipt remains recoverable; no second request |
| Final cycle commit acknowledgement lost | One decision/consumed grant; duplicate commit refused |
| Reconciliation acknowledgement lost | Durable reconciled state remains terminal; no reopening |
| Response identity collision | Existing receipt preserved; new outcome unknown and stopped |

Some crash locations are injected transaction-acknowledgement failures; one receipt/process-exit and a separate replay use actual fresh OS processes. This is not a production chaos/network/host-loss certification. Validation occurs before the atomic receipt insert, so no raw “received but unvalidated” body is trusted after restart.

## 28. Schema

Prepared/unapplied `runtime/provider-integration-schema.sql` adds `genesis_provider_admissions`, `genesis_provider_receipts`, immutable admission/receipt guards and immutable request/ownership guards on the existing attempt table. No duplicated cost ledger or secret table. `runtime/provider-role-grants.sql` is a separate prepared least-privilege extension; no role changes were applied canonically.

Fixture installers enforce the dedicated database/schema. Production installation order follows operator v1 and its prerequisites; backup/restore, least-privilege role execution and target schema/Node identity verification remain separate deployment preparation. Runtime/observer startup does not migrate.

## 29. Tests/build

Final commands and results are recorded in `checks.json` and accompanying logs:

- Full Node suite, serial disposable PostgreSQL: **516 passed; 0 failed; 0 skipped**.
- New provider tests: **70 passed**.
- TypeScript `--noEmit --incremental false`: passed.
- ESLint: passed, no warnings.
- Next.js production Webpack build: passed (existing Node DEP0205 deprecation warning only).
- Canonical read-only exports: exact row/digest match.

All original 446 tests remain byte-identical; no assertions/deadlines were relaxed. The first full run was 505/506 with one genuine local-context regression, preserved in `full-tests-initial.txt`. The provider-only correction passed the unchanged focused 100-cycle test and final full suite. Serial testing avoids known cross-file timing contention; no default Turbopack workaround was introduced.

## 30. Files changed

Existing application changes are limited to:

- `core/v2/context.ts`: provider-only product-designation provenance.
- `server/provider-control.ts`: new reasoning path, lease-aware recovery.
- `server/one-shot.ts`: exact durable admission, interrupted failure path, durable receipt recovery; legacy transport restricted to fixtures.
- `server/commit-v2.ts`: current admission/receipt/proposal check inside commit.
- `server/operator-control.ts`: authenticated admission/attempt inspection and lifecycle.
- `server/one-shot-spec.ts`: pinned new dependencies; runtime version `runtime-v1-oneshot-1.0.6`.

New reasoning contracts/factory/request/control/store/inspection modules, two prepared SQL files, the inert smoke command, integration documentation, provider tests/fixture helpers and this evidence package are listed with hashes in `source-changes.json` / `source-hashes.json`. Existing frontend, scientific code, original test files and canonical schema are untouched.

## 31. Known limitations

- A neutral JSON gateway adapter is implemented, not verified native vendor protocol support. A concrete target must prove gateway contract conformance or receive a separately reviewed adapter.
- No actual tokenizer, tariff, billing telemetry, endpoint, cancellation guarantee or provider retention setting was verified. Fixed/byte bounds require production evidence; reported-only counting refuses.
- Recovery cannot reuse an expired/revoked original claim. Unknown billing remains stopped even if an operator later records a cost; no hidden resumption is introduced.
- The short request lease has no renewal/takeover. Database availability and production statement/connection timeouts must be verified on the intended host.
- Prepared SQL/role profile is not installed on canonical Genesis; deployed least-privilege role tests and restore/redeploy drills remain production prerequisites.
- Unreviewed legacy memory and private operational content remain unavailable to a provider. No disclosure decision was made to make a fixture look richer.
- Long-run memory/Life State growth and paid continuous operation are outside this pass.

## 32. Deferred production work

Review this implementation; select a concrete provider/model/protocol; verify all usage categories/tariffs/counting and category ceilings; verify target endpoint/privacy/egress; provision external secret and actor credentials; install reviewed schemas/least-privilege roles on the reviewed target; review context disclosure; authorize and perform the separate sanitized smoke test; pin resulting exact runtime/admission; then separately review any execution grant.

No key alone enables Genesis. No model was selected, no smoke executed, no deployment performed, no awakening authorized. Paid continuous life requires a future distinct reviewed mode; it is not silently unlocked by a provider admission.

## 33. Final state

CANONICAL DECISIONS = 7  
LEGACY MEMORIES = 7  
CANONICAL V2 EPISODES = 0  
EXECUTION = CLOSED  
SCHEDULE = DISABLED  
BIOLOGY = SAVED-OBSERVATION-ONLY  
ONE-SHOT AUTHORITY = NONE  
CONTINUOUS AUTHORITY = NONE  
CANONICAL DISCLOSURE REVIEWS = NONE  
CANONICAL PROVIDER ADMISSIONS / ATTEMPTS = NONE  
LIVE PROVIDER CALLS = 0  
WALLET ACTIONS = 0  
EXTERNAL COMMUNICATIONS = 0

No further pass or activation was started.

PROVIDER INTEGRATION PASS COMPLETE — READY FOR DEPLOYMENT-PREPARATION REVIEW
