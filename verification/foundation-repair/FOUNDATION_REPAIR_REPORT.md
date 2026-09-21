# Project Genesis — Pass 1 Foundation Repair

## Result and scope

A07, A08, A10 inspection semantics, and A11 are repaired. The original 162 tests and 30 new regression tests pass. TypeScript, ESLint, and the Next.js production build pass. Genesis remains dormant and unchanged. This pass adds no execution authority, provider, retrieval system, scheduler, biological capability, or external effect.

The repository audit was read and its relevant findings confirmed against executable code before editing. The old journal-to-transition probe reproduced the A11 `intent.policy.payloadHash` TypeError. The original audit package still matches every file in its artifact manifest; its historical finding has not been rewritten.

## Canonical integrity

Read-only repeatable audits were performed before modifications and after all implementation, tests, and the build. All canonical rows, not just the count or digest, are identical.

| Property | Before | After |
|---|---|---|
| Organism ID | 817e772c-827e-48fc-8e35-6504cb2a8d2d | unchanged |
| Birth | 2026-09-15T01:56:07.867Z | unchanged |
| Decisions / cycles | 7 / 7 | 7 / 7 |
| Legacy memories | 7 | 7 |
| Projects / ledger entries / milestones | 1 / 4 / 4 | 1 / 4 / 4 |
| Canonical V2 episodes | 0 | 0 |
| Execution | CLOSED | CLOSED |
| Schedule | DISABLED | DISABLED |
| Biology | SAVED-OBSERVATION-ONLY | SAVED-OBSERVATION-ONLY |
| Original brain snapshot | preserved | identical |

Before and after row digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

No canonical migration was applied or required. The existing administrative Life State event is not counted as a V2 episode. Live provider calls, wallet actions, external communications, and canonical life cycles during this pass: **zero**. All write tests used isolated disposable state. The canonical projection check disabled network transport and recorded zero calls.

The 9,319 files in the frozen preservation inventory have zero mismatches. C. elegans equations, connectome, research packages, Brain Spec, constitution, first-awakening mode/permission configuration, and the original history were not changed. Private row dumps remain outside this review package; sanitized evidence is in `canonical-before.json`, `canonical-after.json`, `canonical-public-projection.json`, and `frozen-preservation.json`.

## A11 — canonical intent contract

**Before:** `OneShotController.journal` wrote a reduced JSON record. The operator store accepted an `ActionIntent` and transitions dereferenced policy fields absent from that record. Structural TypeScript typing did not validate the persisted boundary.

**After:** `core/v2/intents.ts` defines one strict runtime-validated contract. Creation, one-shot and isolated journaling, persisted-row reading, operator transitions, reservations, and atomic cycle completion use it. The journal envelope is separately checked against its record and organism ownership.

Required fields include organism identity, proposal, payload hash, complete policy binding, status, attempts, reservation, receipt, and approval. Missing fields, additional unexpected fields, altered payload/policy hashes, wrong ownership, and incompatible approval bindings fail explicitly. No permissive optional chaining or historical repair is used. New creation explicitly records zero attempts/reservation and null receipt/approval because none has occurred; malformed older records do not receive these values by default.

Existing records with incompatible shapes must be reviewed separately. This pass neither migrates them nor invents missing authority. Canonical Genesis currently has no action-intent rows.

`server/intent-journal.ts` owns validated journal conversion and finalization. Finalization occurs in the same fenced transaction as the decision, episode, and Life State update. A changed policy/proposal, already processed intent, or inconsistent episode rolls the transaction back. Operator transitions cannot claim local completion; only cycle commit can do that. Approval remains payload-bound and does not install an external dispatcher.

## Coherent current-scope statuses

| Recorded result | Decision outcome | Committed intent status | Effect interpretation |
|---|---|---|---|
| Voluntary abstention | abstained | abstained | no effect |
| Postponement | deferred | deferred | no effect; no automatic wakeup |
| Policy refusal | denied | denied | no effect |
| Human assistance/approval required | pending | awaiting_approval | no effect; remains pending |
| Permitted local reflection/artifact | local | local_completed | bounded local persistence in commit |
| Permitted computational proposal without a tool | recorded | local_completed | computational record only |
| Planner/provider failure | failed | failed if an intent exists | no voluntary abstention invented |
| Uncommitted cancellation/revocation | no committed episode | cancelled | no effect |
| Ambiguous uncommitted execution | no fabricated outcome | unknown; grant AMBIGUOUS | review required, no retry |

A newly journaled proposal is legitimately `proposed` until commit or closure. It no longer remains proposed after successful local commit. Episode outcome/action fields must agree with decision/policy/action fields. Terminal transitions and duplicate processing are refused. No original historical status was renamed or rewritten.

The existing grant/lease/expected-decision fences remain. The runtime code identity is now `runtime-v1-oneshot-1.0.1`; its hash includes the new execution-affecting contract/journal/provenance modules. Old code identity is not silently reused to authorize altered code. No grant was installed or authorized.

## A07 — saved biological provenance

`server/saved-provenance.ts` resolves the unchanged saved snapshot against an exact historical legacy `brainAfter` record. It uses the earliest exact matching recording and verifies the record timestamp against its database timestamp. It returns the historical decision ID and recording time. A missing match or invalid timestamp returns null; birth, request time, and a later computational decision are never substituted.

`GenesisService.observe`, one-shot preparation, and isolated preparation use this resolver. Saved recording time, observation/request time, latest Genesis activity time, and latest computational decision time are separate fields. Historical replay retains its original record provenance and V2 records remain ineligible for neural replay.

Actual canonical read-only projection:

- Saved biological recording: `2026-09-15T03:31:41.247Z`.
- Latest Genesis activity: `2026-09-15T03:31:41.247Z`.
- Latest computational V2 decision: null.

The equal legacy timestamps today are observed facts, not a coupling in the projection. A regression test commits a computational-only fixture cycle and proves that only Genesis activity advances. It also verifies replay, restart provenance, and zero stimulate/step/decode calls. This lookup is snapshot metadata resolution, not episodic retrieval.

## A08 — authoritative activity and accounting

`server/observation-read.ts` reads a consistent read-only transaction: organism/lease phase, validated Life State, grant/provider state where those tables exist, pending intents, decision timestamps, and actual row counts. Optional preparation tables are inspected without installing them.

Projection priority is review required, current valid active/reasoning claim, pending assistance/approval, then dormant or idle. A stale/expired or inconsistent claim cannot masquerade as live reasoning. CLOSED with no computational cycle remains DORMANT. After a committed computational cycle, an inactive organism can truthfully be IDLE while execution remains CLOSED. Display state grants no execution authority.

Accounting now distinguishes:

- `memoryAccounting.legacyRecords`: original legacy memory records;
- `memoryAccounting.v2Episodes`: persisted episode-kind Life State events, excluding administrative events;
- `memoryAccounting.semanticAssertions`: semantic/self assertions;
- biological plastic state and working context: not included in any of those counts.

The compatibility `counts.memories` field continues to mean legacy records only. The observer labels that meaning explicitly and shows separate episode/assertion counts. No fabricated aggregate was added. Production counts come from persisted records, not the last 20 decisions or bounded episodic-reference list. Canonical counts are 7 / 0 / 0.

## Private trace and A10 ambiguity inspection

`operatorTrace` now includes event metadata, biological applicability/provenance, context manifest/hash, bounded stored rationale, proposal, policy, actual committed-local-effect indicator, outcome, episode identity, recorded changes, and whether review was required at that decision. It does not expose working context or reconstruct hidden reasoning. Current review state is deliberately separate from that historical decision-time flag.

`server/cycle-inspection.ts` provides a private read-only `inspectOneShot` function. It is not a public endpoint or recovery UI. It reports organism/cycle/grant/attempt identity, current durable grant transition and its timestamp, validated intent state, provider attempt identifiers/status, possible dispatch, durable response presence, commit evidence, unresolved liability, integrity problems, retry prohibition, and evidence needed for later reconciliation.

Important limits remain explicit:

- The current grant row is the last durable grant transition, not a manufactured full transition history.
- Existing provider rows do not record separate dispatch/response timestamps; those fields remain null. Reservation time is labeled as reservation time.
- Missing/invalid cost evidence remains null, never zero.
- A malformed historical intent is flagged without repair or field invention.
- Missing response evidence does not prove that dispatch never occurred.
- Decision/episode/grant disagreement requires review.
- Inspection cannot reopen execution, resolve ambiguity, or retry.

## Public disclosure and presentation

Public DTOs remain explicit allowlists. No intent, approval, provider body, private episode text, operator evidence, raw context, secret reference, or hidden reasoning was added. Only status/count/timestamp metadata is projected. Deterministic translations distinguish abstention, denial, pending help, recorded computational changes, active reasoning, and review-required state. Assistance copy does not claim perpetual pending status from an old historical entry. Existing saved-only and legacy-label disclaimers remain.

Presentation changes are limited to these corrected semantics and accounting. Dormant/countdown behavior and the larger observer design are unchanged. Tests use private-data canaries and confirm unsupported planner text cannot become public narration.

## Files changed

New:

- `core/v2/intents.ts`
- `server/intent-journal.ts`
- `server/saved-provenance.ts`
- `server/observation-read.ts`
- `server/cycle-inspection.ts`
- `tests/foundation-repair.test.ts`

Modified:

- `core/v2/contracts.ts`, `biology.ts`, `cycle.ts`, `policy.ts`, `public.ts`
- `server/life-store-v1.ts`, `commit-v2.ts`, `one-shot.ts`, `one-shot-spec.ts`, `isolated-cycle.ts`
- `runtime/service.ts`
- `lib/observer-presentation.ts`, `observer-fixtures.ts`
- `components/live-observation.tsx`
- `tests/support/active-fixture.ts`

The fixture helper supplies structural legacy metadata and its existing saved snapshot to noncanonical fixtures so tests exercise real provenance resolution. It does not execute a neural model or change canonical history. `source-changes.json` records changes relative to this pass's starting working tree rather than conflating previous uncommitted work.

## Verification

| Check | Result |
|---|---|
| Complete existing suite plus regressions | 192 passed; 0 failed; 0 skipped |
| New regression coverage | 30 tests |
| TypeScript after production build | PASS |
| ESLint | PASS |
| Next.js production build, `npm run build -- --webpack` | PASS |
| Canonical before/after complete-row comparison | identical |
| Frozen preservation inventory | 9,319 files, zero mismatches |
| Prior completion-audit artifact manifest | zero mismatches |

The verified local Webpack route was used. Default Turbopack was not rerun; its prior host-environment failure is not represented as a pass. The production build emits a Node `module.register()` deprecation warning but completes successfully.

Regression coverage includes actual one-shot journal → operator-store transition; approval binding and disabled execution; denial/defer/local/approval-required statuses; terminal and duplicate refusal; malformed/missing policy, reservation, approval, ownership and payload; atomic rollback on episode disagreement; cancellation/failure/ambiguity closure; provenance across computational commit/restart/replay; missing provenance; authoritative activity; separate memory namespaces; private/public canaries; inspection with unknown liability; stale/cancelled claims; and no new activation/effect entrypoint. Existing concurrency, one-shot, provider-mock, policy, persistence, and scientific tests remain in the full suite. No mock transport is represented as a live-provider verification.

Full logs are `tests.txt`, `typecheck.txt`, `lint.txt`, and `build.txt`. `verification.json` summarizes commands/results.

## Deliberately deferred

**DEFERRED TO PASS 2:** memory retrieval / usable historical recall. No episodic search, semantic retrieval, embeddings, summarization, ranking, or long-term context selection was added.

**DEFERRED TO LATER PASSES:** Life State workflows; continuous-life controller; operator UI/control and reviewed ambiguity reconciliation; real provider; production migrations; deployment; wallet/internet/communication capabilities.

Prepared one-shot/provider infrastructure remains uninstalled in canonical Genesis. No Decision #8, awakening event, grant authorization, scheduler activation, biological advancement, or external action occurred. This repair is not an awakening readiness approval.

FOUNDATION REPAIR COMPLETE — READY FOR PASS 2
