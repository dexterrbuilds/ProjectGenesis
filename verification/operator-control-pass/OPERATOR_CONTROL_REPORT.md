# Project Genesis — Pass 5 Operator, Disclosure & Recovery Foundation

## 1. Summary

Implemented a private, authenticated control plane around the existing one-shot and continuous controllers. This pass adds source-bound disclosure review, context binding, audit records, inspection, stop/revocation, attributed human intake and explicit recovery facts. It does not introduce an execution entrypoint, provider adapter or awakening authority.

The implementation has been tested against disposable PostgreSQL schemas with sanitized history and injected/local planners. The public frontend and frozen research were not redesigned. Canonical Genesis remains dormant. Production installation, actor provisioning, provider integration and actual disclosure decisions remain separate reviewed work.

The current source, prior post-Pass-4 audit and relevant Pass 1–4 reports were inspected before changes. Before the first source edit, the existing read-only canonical exporter confirmed the expected identity and digest. Prior reports were used as evidence, not as a substitute for integration tests.

Main executable evidence:

- `server/operator-auth.ts`, `server/operator-control.ts`, `runtime/operator-cli.ts`.
- `core/v2/disclosure.ts`, `server/disclosure-store.ts`, `server/provider-disclosure.ts`.
- Existing `server/one-shot.ts`, `server/continuous.ts`, `server/commit-v2.ts`, `server/assistance-intake.ts` and `server/provider-control.ts`.
- Prepared `runtime/operator-schema-v1.sql`, `runtime/operator-role-grants.sql`.
- `tests/operator-control.test.ts` plus every pre-existing test file.

The deployment and command reference is [runtime/OPERATOR_CONTROL.md](../../runtime/OPERATOR_CONTROL.md). It is a preparation document, not authorization to install or execute.

## 2. Canonical preservation

The before export was written privately with mode 0600 using `scripts/runtime-v1-audit.ts`, which starts a repeatable-read, read-only transaction and imports no runtime/model code. The after export uses the same procedure. Private exports contain original records and are not copied into this evidence package.

Expected and verified before identity:

- Genesis ID: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Birth: `2026-09-15T01:56:07.867Z`.
- Seven decisions, seven legacy memories, original project/ledger/milestones and saved biological snapshot.
- No canonical V2 episode. The existing administrative migration event is not counted as a life episode.
- Execution CLOSED; schedule disabled; biology SAVED-OBSERVATION-ONLY.
- No one-shot, continuous or operator schema installed canonically; no authority issued.

Canonical row digest before: `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`.

Final read-only comparison: **all canonical rows identical**. Actual after digest: `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`. Details are recorded in `preservation.json`. All canonical rows, not just counts, must be identical for this pass to be classified complete. No repair or restoration is used to force a match.

## 3. Threat model

Untrusted inputs include planner output, stored excerpts, event text, human answers and arbitrary strings claiming to be an issuer/operator. None authenticate a principal or change its capabilities. Public clients have no route into the new control plane. The operator CLI exposes an enumerated command schema, never arbitrary SQL, code, a planner callback, generic unlock or cycle execution.

Trusted boundaries are: externally provisioned high-entropy credentials; a non-secret SQL actor/capability registry provisioned by the migration owner; the private operator application; and PostgreSQL transactions, privileges and triggers. Service roles must not own tables or inherit migration-owner/superuser powers. The local test database owner is used only to create/dispose fixtures and test roles.

A compromised migration owner can disable triggers. A compromised private operator process/DB login can exercise its DB privileges outside this library. This implementation does not claim to sandbox arbitrary trusted-process code. Deployment must protect credentials, process environment, schema ownership, private stdout, network access and backups. Evidence references are operator attestations, not automatically verified external truth.

## 4. Authentication architecture

`OperatorAuthentication` accepts a strict configuration with explicit `production` or `test` mode and up to 20 key records. External configuration stores a SHA-256 credential digest, key ID, actor ID and expiry; SQL stores no credential. Authentication compares fixed-length digests with `timingSafeEqual`. Invalid credentials and unavailable configuration fail generically.

A successfully authenticated principal is frozen and registered in a private WeakMap. A matching actor ID in a newly constructed object is insufficient. Principal lifetime is at most five minutes and never outlives its key. Rotation replaces the key set and invalidates existing principals. Actor enablement and capabilities are reread for each command. Already committed commands remain historical facts.

The private CLI requires explicit private mode, production auth configuration, an operator DB reference and an external credential. It reads one bounded stdin command and exits. Test authentication is refused by the production CLI; the test principal additionally refuses non-fixture databases/schemas. No production credential or actor has been created.

## 5. Capability model

| Capability | Implemented private surface |
|---|---|
| VIEW_PRIVATE_STATE | Readiness, current private Life State, bounded eligible source preview |
| REVIEW_DISCLOSURE | Catalog, review inspection, append a source/audience-specific decision |
| MANAGE_ONE_SHOT | Inspect/propose/authorize exact grant, revoke/cancel |
| MANAGE_CONTINUOUS | Inspect scopes/queue/resources, propose/authorize exact scope, revoke/cancel event |
| RECORD_HUMAN_RESPONSE | Validated attributed intake, optional explicit local wake enqueue |
| INSPECT_RECOVERY | One-shot inspection, continuous attempt/provider/recovery inspection |
| RESOLVE_RECOVERY | Mark an expired claim ambiguous, append disposition, reconcile liability |
| MANAGE_PROVIDER_ADMISSION | Readiness inspection only; reports PENDING, cannot admit a provider |

Emergency stop requires **both** authority-management capabilities. Holding an inspection capability does not grant control authority. New roles/capabilities cannot be supplied through command payloads, model output or human responses. Proposal and authorization are distinct authenticated commands, even if the same capable operator performs both. Four-eyes approval is not claimed.

## 6. Operator audit journal

`genesis_operator_audit` records stable command ID, authenticated actor, capability, operation, organism, target, previous hash where relevant, requested-command hash, reason reference, result/result hash and exact runtime identity. No raw human answer, memory, credential, provider body or evidence document is stored in the audit payload.

A command transaction locks the organism/control boundary, validates capability and target hash, performs the existing controller operation inside a savepoint, then appends the audit before committing. `transactionBoundPool` keeps trusted controller subtransactions within that outer transaction. A journal failure rolls back the administrative mutation. Review/recovery rows additionally have deferred FKs to their audit record.

Authenticated capability failures are recorded as REFUSED. Unauthenticated calls, malformed envelopes, wrong organism and replayed command IDs are rejected before mutation rather than inventing an actor or duplicate audit. The CLI never asserts success after an uncertain commit. A lost response requires durable inspection, not a different command ID pretending the earlier operation never happened.

UPDATE/DELETE triggers and normal-role privileges protect audit rows. Tests exercise replay refusal, append-only enforcement, write failures and process death mid-reconciliation.

## 7. Disclosure review model

A review binds organism, source type, source identity, content/projection hash, audience, decision, authenticated reviewer, reason reference, created time, optional expiry, schema version and monotonically increasing per-source/audience version.

The independent audiences are INTERNAL_USE, PROVIDER_DISCLOSURE and PUBLIC_DISCLOSURE. Decisions are APPROVED, DENIED, REVOKED or EXPIRED. Expiry at validation time and source mismatch are effective exclusions without editing the stored review. Revocation is a new row. Missing disclosure authority never becomes implicit consent.

The same source ID with changed content cannot inherit approval. A review for source A cannot authorize B. An internal or public approval cannot authorize a provider request. Conversely, explicit approval for one audience does not manufacture approval for another. Installed durable stores ignore ad-hoc review-array overrides passed to the pure compiler.

The catalog hashes the exact retrieval projection or explicitly bounded metadata being reviewed; it does not claim a hash of an unrelated full source package. Provenance remains linked to the original row and review type. Invalid, credential-like or broken-provenance memories still fail the underlying memory eligibility rules even if an approval was attempted.

## 8. Legacy memory review

The seven canonical memories were neither rewritten nor approved. The system can enumerate their identities and projection hashes through authenticated private inspection after a future schema installation. A VIEW_PRIVATE_STATE operator may inspect a bounded eligible legacy excerpt; REVIEW_DISCLOSURE is separately required to decide disclosure. Preview audit rows contain hashes, not excerpt text.

Sanitized fixtures demonstrate independently reviewing a historical memory for internal use, provider disclosure or public-display eligibility. Tests prove that each approval leaves the other audiences unchanged; expiration, revocation and source changes remove eligibility.

This pass therefore removes the infrastructure gap, not the human consent decision. Without future explicit reviews, those canonical memories remain unavailable to provider reasoning. Original identity/birth/history counts and constitution do not depend on approving the private memory text.

## 9. Operational-state disclosure

| Category | Provider/public review classification | Current behavior |
|---|---|---|
| Eligible legacy memories | REVIEWABLE_FOR_PROVIDER / REVIEWABLE_FOR_PUBLIC | Explicit independent review required |
| Bounded legacy project metadata | REVIEWABLE_FOR_PROVIDER / REVIEWABLE_FOR_PUBLIC | Only ID, bounded name, status and work-cycle count; no private project description |
| Pass-3 projects and tasks | INTERNAL_ONLY | Existing private/internal use; review may restrict it |
| Artifacts and immutable versions | INTERNAL_ONLY | No publication/provider elevation |
| Interests, questions, commitments | INTERNAL_ONLY | No automatic disclosure |
| Relationships | INTERNAL_ONLY | No inferred consent, traits or public identity |
| Assistance requests and human answers | INTERNAL_ONLY | Answers remain private untrusted input |
| V2 episodes and semantic assertions | INTERNAL_ONLY | Existing internal provenance rules; no provider/public elevation |
| Current focus | INTERNAL_ONLY | Separately restrictable; denial suppresses the focus field |

These limits intentionally preserve Pass-3 contracts. A later reviewed schema would be needed to transfer private operational material to a real provider. Mandatory factual identity, constitution, permissions and resource namespaces are existing system context, not reviewable private narratives. Other arbitrary Life State fields cannot be promoted by naming them in a review.

## 10. Provider-context manifest

`compileContext` emits a deterministic private disclosure manifest containing audience, installed-store state, review revision, IDs/versions/hashes, source hashes, effective expiry/decision, included categories/sources/reviews, omitted items/reasons and total context bytes.

Omission lists are bounded and explicitly mark clipping. There is no excerpt text, review reason, credential or evidence document in this manifest. Selected historical excerpts remain in the private context only. No public DTO exports the manifest.

Context remains capped at 12,000 UTF-8 bytes, independently of any future tokenizer. Existing memory/operational selection budgets remain intact. The review loader admits at most 256 latest source/audience decisions; overflow fails closed instead of silently discarding a review. Private inspection is capped at 128 KiB. These are engineering bounds, not biological parameters.

Provider context excludes unreviewed legacy memories/project descriptions, private operational records, human answers, relationships and unreviewed environmental text. Merely being public-display eligible no longer silently admits an environment excerpt to a provider. Hypothetical provider permissions do not constitute provider admission.

## 11. Preparation/commit disclosure binding

One-shot and continuous preparation load the memory archive and durable disclosure set with the existing organism transaction lock. Review writers use that lock too. Shared `commitV2` rereads the archive and review interpretation and recompiles the context under the commit fence.

Both context text/hash and manifest bind disclosure authority. Source/review/version/epoch changes, revocation, deletion, effective expiry or installation-state change invalidate preparation. Tests exercise both one-shot and continuous paths; no policy tolerance or result semantics were relaxed.

The binding is conservative: even an unselected review-set change invalidates preparation. This costs liveness but cannot silently broaden disclosure. Actual wall time determines expiry; an old event timestamp cannot restore expired consent.

`ProviderControl` also checks disclosure before reservation and immediately before crossing its dispatch boundary. A changed review prevents even an injected transport from being called. This cannot retract data after a request was already sent; revocation then prevents stale acceptance/commit and may leave unknown liability. No real transport was added.

## 12. First-cycle context inspection

`server/first-context-inspection.ts` operates only in a sanitized fixture database/schema/organism. It opens a read-only transaction, constructs a hypothetical factual input in memory, compiles provider-visible context and returns structural metadata. It calls no planner and creates no event, grant, decision or neural update.

`context-inspection.json` demonstrates identity/name/designation, birth and seven prior decisions; constitution; one explicitly reviewed legacy project metadata record; one reviewed past experience; SIMULATED economy with unresolved on-chain state; saved-only/not-applied biology; factual current input; permission scope; and the available strict local operation names/outcomes.

It contains no private canonical contents and is not a simulated Decision #8. The output also identifies the categories still excluded. The provider would not know the private operational descriptions merely because they exist in Life State. No output scripts what Genesis should decide.

## 13. One-shot controls

The operator boundary wraps existing proposal, exact authorization, inspection, revocation/cancellation and expired-claim inspection logic. The proposal issuer must match the authenticated actor; the authorization command binds the already-stored row/payload hash. Attribution references alone never authenticate.

Fixture integration proves prior count 7 → exactly one decision 8, consumed grant, no decision 9, execution CLOSED, disabled schedule and saved-only biology. No continuous scope is automatically created. A revoked in-flight authority cannot commit.

No generic OPEN operation exists. The active-cycle entrypoint still requires separate future work/review; this CLI manages authority only. Canonical grant tables remain uninstalled and no canonical grant is proposed or authorized.

## 14. Continuous controls

Separate authenticated operations manage the existing continuous scopes. Private queue inspection includes bounded pending/terminal event metadata, attempts, scope payload hashes and actual resource accounting. Cancellation and revocation preserve existing event/lease/budget rules. Recovery-only operators can inspect a continuous ambiguous attempt without gaining scope-management privileges.

Pass-4 compatibility tests retain deduplication, leases, numbering, idle/defer, revocation, budgets, bounded follow-ups, restart and crash checks. The complete prior suite includes its isolated 100-cycle test. No canonical worker, event, scope or recurring schedule is started.

## 15. Emergency stop

Emergency stop revokes all proposed/active one-shot grants and proposed/active continuous scopes, invalidates their stale claims and preserves pending events. Repeating stop does not delete evidence or reopen execution. Terminal ambiguous records remain stopped.

A targeted test exposed a relevant distinction: revoking a one-shot with a possible provider dispatch must not simply mark it REVOKED and remove the unresolved-claim barrier. This pass changes that path to AMBIGUOUS and preserves unknown intent/liability. This is a fail-closed correction, not an automatic recovery route.

No separately supervised worker exists in this entrypoint to signal. The response reports that fact explicitly. Existing worker phase/poll/commit checks enforce durable revocation. Process supervision/signaling remains deployment work.

## 16. Human-response intake

`human_response` requires RECORD_HUMAN_RESPONSE and delegates to the existing validated intake inside the operator transaction. It requires an existing request and original provenance, matching organism/revision, explicit respondent attribution, time, bounded text and the strict private/internal-only disclosure shape.

A response appends an administrative input and moves the request to answered, not resolved. It neither executes its content nor grants permissions. Duplicate identity, stale state or wrong capability is refused. The audit records a command hash, not the answer. Wake enqueue is an explicit boolean and defaults to no wake; even an enqueued event cannot execute without separately valid authority.

No message was sent. No external messaging client was introduced.

## 17. Ambiguity/recovery

Recovery dispositions append authenticated administrative facts: CONFIRMED_NO_EXTERNAL_EFFECT, CONFIRMED_EXTERNAL_EFFECT_WITHOUT_LOCAL_COMMIT, CONFIRMED_LOCAL_COMMIT or UNRESOLVED_REMAIN_STOPPED. Each binds target state/hash and evidence reference/hash. Existing grant/event/history is not rewritten into a more convenient outcome.

Confirmed local commit requires matching V2 decision/episode identity, ownership and source linkage. Contradictory/incomplete commit evidence refuses confirmation. An expired uncommitted claim can be explicitly marked AMBIGUOUS; it is not rerun. Continuous inspection reports attempt/event/commit evidence and provider accounting independently.

Even a successful reconciliation does not reopen a terminal authority, requeue an ambiguous event or permit the same claim to run again. Future clearance of such historical barriers, if justified, requires another reviewed mechanism. This pass prefers a retained stop over an invented retry.

## 18. Provider liability reconciliation

A RESOLVE_RECOVERY operator can record externally established NOT_EXECUTED, BILLED or UNKNOWN facts against an owned unresolved attempt. Known costs and optional usage/response identity are explicit. Unknown stays null and retains reservation liability; it never becomes zero merely because the request timed out.

A zero billed amount is not proof of non-dispatch. No-effect confirmation requires a not-sent record or an explicit not-executed reconciliation, not just cost zero. Billed/response evidence and absence of local commit are separately required for external-effect-without-local-commit confirmation. Costs beyond the existing reservation refuse normal reconciliation and require investigation.

Accounting updates and appended recovery/audit records share one transaction. A fresh child process killed after its accounting update but before the recovery/audit commit leaves the original unknown accounting and no partial administrative fact. The restarted inspector still reports review required. No provider was contacted to obtain these fixture facts.

## 19. Role separation

The prepared SQL profile was applied only to disposable schemas with randomly named NOLOGIN roles; roles and schemas were removed afterward. Tests prove:

- PUBLIC_OBSERVER can read the narrow identity view, but cannot read raw memories/reviews or mutate.
- RUNTIME_WORKER cannot insert authority/reviews/audit/actors or update authorization records/schedule enablement. A status-only authorization attempt is also refused by a DB trigger. Direct human-response insertion is refused.
- PRIVATE_OPERATOR can perform authenticated inspection/authorization/revocation but cannot update/delete historical rows, overwrite organism identity, modify actors or disable triggers.
- An actual local one-shot fixture succeeds under the restricted worker role and cannot run a second cycle.

PostgreSQL `FOR SHARE` requires an UPDATE privilege on at least one schedule column. The worker receives heartbeat-column permission only; it cannot enable the schedule, change due times or remaining-cycle authority. This was verified without weakening the existing row lock. No canonical heartbeat was written.

This is a tested prepared privilege profile, not a claim that production roles, TLS or identity provisioning are installed. The complete observer must continue through allowlisted service projections; the SQL identity view is deliberately insufficient for private history. Future provider-grant provisioning needs a separately reviewed non-owner path.

## 20. Schema

Five new tables are prepared: operator actors, control-state/review epoch, operator audit, disclosure reviews and recovery dispositions. The schema includes organism/actor ownership FKs, append-only guards, deferred audit FKs, review version sequencing, indexes, authorization-role guards, private intake guard and the public identity view.

No credentials live in these tables. Actor provisioning is reserved for the migration owner, not an operator command. New SQL is not registered in a boot migration runner. Installation order and role template are documented, but no canonical table, role, migration or authority was added.

The existing authority models, constitution, first-awakening mode and biological equations were retained. Runtime content identities were advanced to bind the changed compiler/control/SQL implementation; historical reviewed runtime identities were not silently reused.

## 21. Privacy

Public DTO implementations remain explicit allowlists and were not broadened. Canary tests cover credential material, actor/review references, private memory, human answers, relationships and context/control metadata. Existing public decision identifiers remain identifiers; no grant/scope payload, review reason or provider reconciliation record is exported.

New private source previews are bounded and capability-gated. Review hashes/manifests contain no raw private contents. Recovery inspection exports bounded request/accounting identity, not raw provider bodies or hidden reasoning. The evidence package contains sanitized fixture structure and test results, not original private memories, answers, operator evidence contents or credentials.

## 22. Failure behavior

| Boundary | Verified behavior |
|---|---|
| Missing/invalid authentication | Refuse before control mutation; generic CLI error |
| Wrong capability/target hash | Refuse; authenticated capability refusal audited |
| After proposal, before authorization | Durable PROPOSED only; no invocation |
| After authorization, before invocation | No automatic claim/cycle/worker |
| Audit/review DB write failure | Roll back administrative changes; never return success |
| Review committed before preparation | New controller reads it durably |
| Review revoked/expired/removed after preparation | Commit fails closed |
| Operator revokes an in-flight cycle | Stale commit refused |
| Possible provider dispatch during stop | AMBIGUOUS; liability preserved |
| Reconciliation process dies midway | Accounting/recovery/audit transaction rolls back |
| Unknown provider liability | Null/unknown retained; no retry |
| Two operators race same version/authority | One mutation wins; stale request refused |
| Duplicate command identity | No duplicate administrative mutation |

The first parallel full-suite run had two failures in existing short-deadline continuous-life tests under host contention. Their deadlines/assertions were not weakened. A serial full-suite run passed; both the parallel output and final serial output are retained, rather than discarding the initial result.

## 23. Tests/build

Final validation: **446 passed, 0 failed, 0 skipped**, including all 387 baseline tests and 59 new tests. TypeScript, ESLint and the Webpack production build passed. Machine-readable counts and command statuses are in `checks.json`; full outputs accompany this report. The expected baseline of 387 tests is retained, with new operator/auth/disclosure/recovery/role/privacy coverage.

Validation runs:

- Full Node suite with the dedicated `genesis_runtime_v1_test` URL only. Canonical `.env` was not loaded into tests. Final route uses `--test-concurrency=1` so independent files do not compete against the existing millisecond lease/deadline fixtures.
- TypeScript `--noEmit --incremental false`.
- ESLint over the repository.
- Next.js production build through the verified Webpack route, without a runtime launch.
- Read-only final canonical row export and frozen-package/file hashing.

Fixture mock-provider accounting is not a live-provider call. Existing neural tests run disposable test models; no canonical biological state is advanced. No production integration result is inferred from mocks or localhost PostgreSQL tests.

## 24. Files changed

New source files:

- `core/v2/disclosure.ts`.
- `server/operator-auth.ts`, `server/operator-control.ts`, `server/operator-transaction.ts`.
- `server/disclosure-store.ts`, `server/provider-disclosure.ts`, `server/first-context-inspection.ts`.
- `runtime/operator-cli.ts`, `runtime/operator-schema-v1.sql`, `runtime/operator-role-grants.sql`, `runtime/OPERATOR_CONTROL.md`.
- `tests/operator-control.test.ts`.

Modified existing source:

- `core/v2/contracts.ts`, `core/v2/context.ts`, `core/v2/operational-context.ts`, `core/v2/memory.ts`, `core/v2/cycle.ts`.
- `server/commit-v2.ts`, `server/one-shot.ts`, `server/continuous.ts`, `server/provider-control.ts`.
- `server/one-shot-spec.ts`, `server/continuous-spec.ts` for explicit runtime identity changes.

This report/evidence directory and private pass outputs are additive. `source-changes.json` lists hashes against the actual start-of-pass source snapshot, avoiding attribution of earlier uncommitted work to this pass. No prior test file, frontend implementation, frozen research file or historical report was edited. Verification also confirmed **9,319 frozen files** and all six prior audit/report packages unchanged; see `frozen-preservation.json`.

## 25. Known limitations

- No production schema/role/IAM/network/backup verification has occurred. The private CLI is deliberately not a UI or public API.
- Operator evidence is authenticated attribution, not independent verification of an external billing claim. Costs/usage must be reviewed before entry.
- Recovery records cannot automatically clear terminal barriers. There is no retry/reopen command.
- The review catalog/inspection bounds are conservative and may refuse at larger scale. JSON Life State/archive growth issues from earlier passes remain.
- Operational relationships, human answers, V2 episodes and Pass-3 records remain internal-only. This can constrain a future provider's useful context; it is not a reason to bypass disclosure.
- Public approval records eligibility but does not publish a memory/artifact or change public endpoints.
- Revocation cannot retract an already-sent provider request. Unknown liability remains an explicit stop.
- Role protection assumes non-owner, non-superuser, non-inherited service credentials and trusted schema search paths. Table owners are not confined by these application controls.
- Existing very short test deadlines can fail under heavy parallel load; serial verification preserves those exact assertions.

## 26. Deferred work

Provider integration/model selection/tokenizer/rate-card admission/secret configuration/live smoke test are deferred. So are production migrations/roles, deployment, supervised process control, operator UI, human canonical disclosure decisions, authorized first awakening, continuous activation, wallet/internet/external communications and any future recovery-clearance authority.

No Brain Spec/research capability update is proposed. No second organism, new biological capability, semantic neural drive or product mapping was introduced.

## 27. Final state

The final preservation evidence confirms: seven canonical decisions; zero canonical V2 episodes; execution CLOSED; schedule DISABLED; biology SAVED-OBSERVATION-ONLY; no canonical one-shot/continuous authority or disclosure reviews; no live provider call, wallet action or external communication during this pass.

This pass prepares controls; it does not authorize using them against canonical Genesis. Stop for review after the evidence package is finalized.

OPERATOR CONTROL PASS COMPLETE — READY FOR PROVIDER-INTEGRATION REVIEW
