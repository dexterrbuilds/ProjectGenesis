# Runtime V1 test report

Date: 2026-09-20. All lifecycle/neural verification used isolated fixtures; no canonical cycle, live provider or wallet call.

| Check | Result |
|---|---|
| Full Node test suite, dedicated Postgres URL | **74 passed, 0 failed, 0 skipped** |
| New Runtime V1 unit/contract tests | 39 passed (included above) |
| Isolated Postgres integration tests | 7 passed (included above) |
| Existing fixture/regression tests | 28 passed (included above) |
| `npm run typecheck` | PASS |
| `npm run lint` | PASS, no reported warnings/errors |
| `npm run build -- --webpack` | PASS, production frontend and route build |
| Default `npm run build` (Turbopack) | Host port-binding permission failure, including approved retry; not a pass |
| Standalone Node runtime startup/restart | PASS, two fresh processes on isolated restored state |
| Docker image build | NOT RUN — Docker unavailable |
| Canonical migration backup restoration | PASS; exact baseline digest reproduced in test DB |
| Original-row preservation after canonical migration | PASS |
| Protected file comparison | 9,319 unchanged, 0 missing |
| `git diff --check` | PASS |

## Isolation and coverage

The Postgres suite enforces database name `genesis_runtime_v1_test` and uses disposable schemas. It restores the private verified backup locally; CI without that file creates an isolated synthetic fixture with no neural advancement. CI retains Docker verification and no longer invokes the dormant-disabled demo. Unit providers are injected response/error doubles, not live calls. No canonical runtime process was launched.

Tests cover exact saved snapshot restoration and invalid provenance/version rejection; mocked fail-if-called neural methods; null unavailable/not-applied values; evidence pins and scope refusal; life identity/rhythm; unresolved wallet and rotation refusal; deterministic bounded/private context; protected constitution and invalid biological context; safe product fallback; seven adversarial claims and five forbidden authority fields; citation/context mismatch; permissions/revision/cost and external approval; payload/operation/expiry binding; invalid intent transitions and retries; memory provenance/append-only semantics; computational project abandonment/task deferral; local artifact staging only in an explicit isolated fixture; failed providers without fallback; disallowed provider transport; public DTO redaction; legacy/V2 discrimination; no neural semantic calls in V2; stable JSONB payload identity; and dormant CLI guards.

Postgres tests additionally verify:

1. Exact backup restoration, additive row preservation and library idempotency.
2. Refusal of empty/wrong identity and enabled schedule.
3. Legacy writer and marked-writer rejection while CLOSED.
4. Manual/scheduled/service/API/tick attempts leave the database identical.
5. Direct-runtime public reads expose only allowlisted data and do not write.
6. Intent duplicate/concurrent insertion, persisted payload hashes, revision-checked journal transitions and append-only event rejection.
7. Fresh-process boot/restart does not change any record even when autonomy/public-live flags are set.

## Issues found and corrected before canonical migration

- TypeScript initially scanned an archived test copy. `outputs/` and frozen `research/` are excluded from application type/lint discovery, not altered.
- The restart fixture needed an explicit `NODE_ENV` for Next's environment typing.
- The idempotency test initially hashed new tables as part of the old-only baseline; it now explicitly selects the original table set. The canonical baseline check was not weakened.
- A real JSONB round-trip issue reordered proposal keys and changed naive JSON-string hashes. Payload hashes now use recursively sorted object keys, with ordered arrays preserved. Separate snapshot-byte hashing stays exact. A regression verifies stable identity plus changed-payload rejection.
- Turbopack could not bind a local build-worker port in this host. An approved retry had the same failure. The supported webpack production build passed; no checking was disabled.

## Scope limits

Passing dormant refusal tests is not proof of active in-flight cancellation, real paid-provider crash accounting or external exactly-once effects. Those executors are disabled. Approval, reservation and reconciliation structures/helpers exist; paid dispatch has no reviewed durable budget path. No live provider smoke test or actual Docker build was performed. No browser visual inspection is claimed; UI data contracts/privacy and frontend build were verified.

Historical legacy ablation/decoder tests still pass, but their old semantic enum expectations are not V2 biological capability criteria. No frozen scientific optimization, experiment or replay was run.

Sanitized logs/results are in `verification/runtime-v1/`; full local preparation records and private copies are ignored under `outputs/runtime-v1/`.
