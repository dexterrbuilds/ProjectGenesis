# Runtime V1 preservation report

Date: 2026-09-20. Canonical audit was read-only before and after the explicitly authorized additive migration. The runtime was not started against canonical Genesis.

## Database identity

| Quantity | Verified value |
|---|---|
| BEFORE_DATABASE_DIGEST | `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312` |
| AFTER_DATABASE_DIGEST | `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220` |
| ORIGINAL_ROW_PRESERVATION_RESULT | All original records identical |
| Organism | Same original ID/birth; one organism |
| Original decisions / cycles | 7 / 7 |
| Original memories / projects | 7 / 1 |
| Original ledger / milestones | 4 / 4 |
| Schedule | Every original field identical; enabled=false |
| Execution lock | CLOSED |
| Wallet identity extension | unresolved; original wallet state unchanged |
| Active lease / other clients at migration check | None / 0 |

These are SHA-256 hashes of the audit's deterministic table/row JSON representation, not PostgreSQL physical-file digests. The whole-database digest legitimately changed through additive schema/rows; whole-database byte preservation is not claimed.

All nine original table row sets compare identically after excluding only the new `003` schema-migration row. This includes organisms, decisions, memories, projects, ledger, milestones, schedule, external observations, and the two original migration rows. The migration independently compared original rows before committing while holding write-excluding table locks.

Serialized saved brain bytes compare exactly before/after: **13,219 bytes**, SHA-256 `f1a48cc6ffd9acab485a754a209a75b52910cd445a2f1e2d259361e02650ef34`. No new parent snapshot or model state was generated for Genesis. The extension references this snapshot; it does not install fly research memory.

## Authorized delta

- Three new tables: `genesis_life_state`, `genesis_life_events`, `genesis_action_intents`.
- One CLOSED life-state extension referencing the existing organism.
- One administrative migration event, explicitly not a life experience.
- One `genesis_migrations` row, version `003`.
- Zero action intents, zero new decisions, zero new memories, zero financial entries.
- Database triggers fence legacy writers and enforce append-only histories.

## File preservation

**9,319 protected files** were hashed against the opening inventory: zero changed, zero missing. The inventory covers all existing research files, both Brain Specs, Stages 1–5, route/identity/physiology/representation/sensory studies, C. elegans implementation, data, legacy contracts, brain tests and approved design. No new files were added to a research package. Existing untracked research packages were retained, not committed or rewritten by this task.

The C. elegans file hash remains `0ee044fcd922e4916340a6c7083903a310ae3af7998d07c2eefc910169806fec`; the connectome remains `1b8bc920fe1899b1bf8350acec84539d34ffe7f4d5351a4d5627fb786344babe`.

## Verification records

Private, ignored local evidence lives in `outputs/runtime-v1/`: `PRIVATE_BASELINE_BACKUP.json`, `PRIVATE_CANONICAL_AFTER.json`, `CANONICAL_MIGRATION.json`, `MIGRATION_DRY_RUN.json`, `PRESERVATION_RESULT.json`, `FROZEN_BEFORE.json`, and `FROZEN_AFTER.json`. Private exports use mode 0600 and must not be published. A sanitized verification subset accompanies this report in `verification/runtime-v1/`.

The backup was restored only into disposable schemas of `genesis_runtime_v1_test`; its reconstructed baseline digest matched exactly. Canonical state was never used for lifecycle tests. Legacy neural computation ran only in isolated tests; no new canonical simulation, stimulus, cycle or activation occurred. Provider tests used doubles. No live provider, wallet/RPC, signing, financial, browser/internet tool or external communication action occurred.

Historical research packages that recorded the old canonical digest remain untouched. Their historical digest is evidence of their own execution state, not an instruction to undo this authorized migration.
