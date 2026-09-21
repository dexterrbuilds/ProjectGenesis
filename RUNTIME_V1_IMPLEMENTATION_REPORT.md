# Runtime V1 implementation report

Date: 2026-09-20. Scope: reviewed Runtime V1 implementation and isolated verification; no awakening.

**Disposition: RUNTIME V1 IMPLEMENTED — BLOCKERS REMAIN.** The dormant observation runtime and isolated V2 preparation path are implemented. Paid reasoning, external execution and canonical life execution remain disabled. This is not a new biological experiment or capability admission.

## Modules added

| Module | Implemented responsibility |
|---|---|
| `core/v2/contracts.ts` | Versioned observation adapter/envelopes, LifeStateV1, four memory domains, PlannerV2, proposals, policy/approvals/intents, DecisionV2 |
| `core/v2/biology.ts` | Pinned evidence-package verification, compatible exact saved-state restoration, saved observations, explicit `not_applied`, refusal to advance |
| `core/v2/identity.ts` | Pinned six-principle constitution; extension initialization without new birth; unresolved/operator-reviewed existing wallet binding; canonical payload hashing |
| `core/v2/life-state.ts` | Deterministic sourced assertions, project lifecycle and deferred-task changes; episode references; protected ownership |
| `core/v2/context.ts` | Bounded context with critical constraints, permission/evidence provenance, disclosure limits and deterministic selection manifest |
| `core/v2/planner.ts` | Strict proposal contract, product abstention fallback, injected-transport language adapter, no implicit fallback on provider failure |
| `core/v2/policy.ts` | Independent validation, payload-bound approvals, state-transition rules, bounded reservation helper and ambiguous-retry rejection |
| `core/v2/cycle.ts` | Isolated preparation of the layered trace, local artifact/non-execution, episode and proposed extension update |
| `core/v2/public.ts` | Allowlisted public projections; exact legacy disclaimer; V1/V2 discrimination |
| `server/life-store-v1.ts` | Existing-life checks, hard-closed service grant, guarded transactional commit, durable intent journal/revision transitions |
| `runtime/migrations/003_runtime_v1.sql`, `runtime/migrate-v1.ts` | Three additive tables, append-only enforcement, legacy-writer fence and transactional preservation checks |
| `scripts/runtime-v1-*.ts` | Private read-only audit, dedicated test-DB provisioning, explicit baseline-specific migration |
| `app/api/replay/route.ts` | Stateless proxy for genuine historical frames |
| `tests/runtime-v1.test.ts` | 39 new contract/safety/privacy/compatibility tests |

## Existing modules changed

`runtime/main.ts`, `service.ts`, `http.ts`, and `scheduler.ts` now expose dormant observation and refuse production execution. Startup no longer migrates/initializes or starts mutating workers. `server/store.ts` adds only a connection accessor; legacy methods remain and are fenced after migration.

The Live/Brain/Life/Money/Memory observer, scientific-limits page and brain missing-data label now distinguish saved biology, computational life, reasoning and policy. Private text is withheld. Replay uses only saved compatible frames and a manual slider. The dormant/countdown page and logo remain intact.

CLI `life`, `demo` and `check:llm` refuse execution. Docker copies the extension store and pinned evidence package. CI uses the dedicated test DB, removes the now-disabled demo invocation, and uses the verified webpack build. TypeScript/lint exclude archived outputs and frozen research vendor content; research is checked by file hashes, not rewritten to satisfy application lint.

`README.md`, `ARCHITECTURE.md`, `DEPLOYMENT.md` and `.env.example` now document the actual dormant mode. The approved design and historical scientific reports were not edited.

## Implemented semantics

- **Biology:** SAVED-OBSERVATION-ONLY. No `decodeBehavior`, `step`, or semantic `stimulate` call in V2 orchestration. The C. elegans constructor/restore validates state only. Missing/not-applied values remain null. Physical calibration remains unknown. No fly learning operator is installed.
- **Life:** an extension of Genesis 001, not a replacement aggregate. Existing birth, rhythm, memories, projects, economy and snapshot survive. Newly introduced interests, relationships, commitments and assertions start empty, not fabricated.
- **Memory:** biological snapshot ownership is opaque to the planner; episodic archive is append-only; semantic assertions are unverified and source-bound; working context is temporary. Old memories are not truncated or rewritten.
- **Planning:** product-level PROPOSAL/DEFER/ABSTAIN/REQUEST_ASSISTANCE; no biological behavior enum. Strict shape/citation validation rejects authority patches and the tested unsupported claims. Language-provider failures remain failures. No real provider call occurred.
- **Policy:** independent of neural output and planner narrative. Unknown tools/effects, stale revisions, inappropriate permissions, changed/expired approvals and excessive costs fail closed. External intent names cannot dispatch.
- **Intents:** unique durable IDs, stable JSON payload hashes, optimistic revisions plus row locks, approval/reconciliation fields and append-only administrative transitions. Production reservations and dispatch are refused. Exactly-once delivery/billing is not claimed.
- **Execution:** the extension is CLOSED and service execution always refuses in this release even if an operator edits that flag. No environment key, countdown or endpoint carries an activation grant. HTTP controls and CLI entry points are blocked.
- **Economics:** preserved simulated cents; chain balance and attributed revenue unknown and separate. Wallet binding unresolved, no new address or signer. No real economic or communication effect.

## Validation and canonical result

74/74 tests passed: 39 V1 unit tests, seven isolated Postgres tests, 28 existing fixture/regression tests. TypeScript and lint pass. Next production build passes with webpack. Standalone runtime starts and restarts against isolated copied state without mutation. Docker is unavailable; its build is not claimed.

The authorized canonical migration was applied only after backup restoration and isolated verification. Original rows compare exactly; only three tables, writer/immutability protections and three administrative/extension rows were added. There are still seven decisions and no new life episode. See [preservation](RUNTIME_V1_PRESERVATION_REPORT.md) and [migration](RUNTIME_V1_MIGRATION_REPORT.md).

## Limits and blockers

1. Actual Docker build/target-host verification remains outstanding.
2. The existing wallet's authoritative public address/provenance is unresolved. Wallet-specific activation is blocked; unresolved is not zero.
3. No activation grant exists. This release cannot be unlocked by API or flags. Future operational authorization must name its scope.
4. Paid-provider durable reservation, crash/reconciliation and revocation at execution time are not validated as an active service. The language adapter is tested only with injected transport. Enable no paid provider until these controls are completed and reviewed.
5. External message/financial executors are absent. The intent journal is infrastructure, not an executable financial approval flow. There is no receiver/network-specific financial payload schema in this dormant release.
6. Guarded prepared-commit code is unreachable in this release; dormant locking tests do not establish active concurrent-cycle/cancellation safety. This remains an activation review requirement.
7. Claim-pattern rejection is defense in depth, not a universal semantic classifier. Public DTOs therefore exclude arbitrary planner rationale and private content. No human/browser visual review was claimed in this pass.
8. Saved observations do not demonstrate biological participation in new life decisions. Any such mode needs separate evidence, consumption rules and authorization.

No frozen study, Brain Spec, neural equation, canonical life cycle, wallet action or external communication was changed or executed. Stop for review.
