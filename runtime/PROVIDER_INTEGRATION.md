# Reasoning boundary v2 — prepared, not enabled

No canonical admission, schema installation, execution grant, provider secret or smoke authorization is supplied by this release.

## Entry points and ownership

- `OneShotController.admittedReasoningPlanner(fence, options)` resolves an already ADMITTED database record through `ProviderControl.reasoningPlanner` and the pinned factory. It does not issue a grant or open execution.
- `ReasoningRequest` binds the complete serialized body, current context/disclosure, organism/event/cycle, authority, runtime, policy, constitution, schema, permission, cost reservation and timestamp.
- `OneShotController.resumeReceived(fence)` reconstructs a prepared decision from a canonical durable receipt. It neither dispatches nor commits. The original claim, lease, runtime, state and disclosure must still be valid. Expired/revoked claims remain stopped for operator review.
- `CONTINUOUS_LOCAL_V1` remains deterministic and unpaid. A paid continuous mode is not implemented or admitted.
- Legacy injected `providerPlanner` is restricted to disposable test databases. `LanguagePlannerV2` remains a historical injected prototype, not a production route.

## Trusted adapter protocol

The static factory registers `fixture-v1` and `json-gateway-v1`. The latter is a real HTTPS JSON transport implementation, **not an adapter for an asserted vendor API**. A prospective endpoint must independently implement the reviewed `genesis-json-envelope-v1` protocol. Native vendor APIs need a reviewed adapter if they do not implement it; that does not require changing organism orchestration. No such vendor or hosted gateway was selected in this pass.

Request body is exactly `completeWire(admission, context)` as UTF-8 JSON. It contains version/model/planner/admission identity, versioned instructions, the bounded context string and hash, full closed output schema, reasoning settings, output ceiling, per-category billable-unit ceilings, monetary ceiling, zero retries, no tools, and `store:false`. The authenticated header is transport-only. Do not log headers. No redirect follows an admission endpoint.

The endpoint must enforce admitted ceilings, prohibit hidden reasoning content, perform zero automatic retries/fallbacks, and return exactly:

```ts
{
 responseId: string,
 requestId: string | null, // null is explicitly unavailable, not invented
 admissionHash: string,
 model: string,
 structured: Proposal | string, // JSON string parsed once; never repaired
 usage: Record<string, number> | null
}
```

Every admitted billable category must be present in known usage. Extra/missing categories, excess usage, unknown usage and response collisions stop the cycle. No provider-specific headers or full response bodies are persisted. The response stream is capped at 64 KiB. Only the canonical validated Proposal, identities, hashes, time, usage, validation result and cost are stored. Invalid bodies get rejection metadata/hash rather than raw text.

The adapter endpoint is trusted configuration, never an event/model-selected URL. HTTPS only; no userinfo/query/fragment, IP literals, localhost or `.local`/`.internal` targets. Production target review must additionally verify DNS/egress restrictions, endpoint ownership, retention policy and gateway implementation. These are deployment prerequisites, not demonstrated network properties.

## Accounting and assumptions

Categories use exact integer rational micro-USD rates and per-category upward rounding. Worst-case reservation covers **all** category maxima. Existing one-shot grant limits still bound admission; the generic admission does not decide a new global budget.

`FIXED_WORST_CASE` and `CONSERVATIVE_ESTIMATOR` require operator-reviewed evidence for the bound over the admitted wire-size domain. UTF-8 bytes are an estimator, not a measured tokenizer result. Fixed bounds are assertions requiring independent evidence; fixture bounds do not validate a production tokenizer. Gateway wrappers or transformations not represented in this body must be covered by the reviewed bound. `PROVIDER_REPORTED_ONLY` cannot establish a pre-dispatch ceiling and is refused. No exact tokenizer implementation is claimed.

The instruction/schema/wrapper bytes are included before admission checks. Transport sends the identical string. If a real endpoint cannot prove and enforce the admitted category bounds, **do not admit it**.

## Secrets

Production references: `env:GENESIS_PROVIDER_<NAME>`. Values load only at dispatch, never from SQL/context. Fixture references/resolvers/callbacks are rejected outside `genesis_runtime_v1_test` / `awakening_test_*`. Resolver errors are generic; secret echo is rejected before any response persistence. No key exists in this release.

## Admission and operator controls

The existing authenticated private operator CLI gains:

- `propose_provider`: strict version-2 admission, actual implementation hashes, source reference; creates PROPOSED only.
- `admit_provider` / `revoke_provider`: exact current row hash, existing actor capability `MANAGE_PROVIDER_ADMISSION`, atomic audit.
- `inspect_provider`: private configuration/secret reference only.
- `inspect_provider_attempt`: private owner/lease, request/admission hashes, receipt validation, usage, liability; no context/proposal body.

Admission cannot authorize execution. The later one-shot grant must bind exact admission/provider/model/runtime and limits. Current actor capabilities, authority, review epoch, source hashes, review versions/expiry and context are checked immediately before dispatch. Commit independently recompiles current context and checks the durable admitted receipt. Admission/review revocation cannot retract already-sent bytes; it blocks subsequent acceptance/commit.

## Durable states and crashes

Reservation precedes dispatch. Provider owner + original cycle fence/lease + bounded request lease expiry are immutable. No lease takeover or retry. A second recovery process leaves healthy attempts alone. Expired in-flight records become UNKNOWN with liability retained (even reserved-only cases are conservatively stopped).

Valid receipt and billing state commit atomically. If acknowledgement is lost, the durable receipt can be inspected/replayed under valid fences. If receipt durability is unknown, do not send again. Received malformed proposals never become abstentions. Timeout/cancellation/5xx do not prove zero billing. Cancellation reports SUPPORTED_CONFIRMED / SUPPORTED_UNCONFIRMED / UNSUPPORTED / ALREADY_COMPLETED, and even confirmation does not imply zero cost. Generic transport currently reports unconfirmed cancellation.

A receipt with unknown cost cannot commit or replay. Operator reconciliation records billing evidence; it does not grant new execution authority, retry, or automatically resume an ambiguous cycle.

## Schema installation (future, separately reviewed)

Existing base → Runtime V1 migration 003 → preparation → one-shot → continuous → operator v1 → `provider-integration-schema.sql` → reviewed role grants → `provider-role-grants.sql`.

The new prepared schema contains immutable admissions and receipts, a request/ownership guard on the existing attempt table, and indexes. There is no secret table, duplicate budget ledger, boot installer, automatic actor provisioning or public endpoint. Runtime worker may read admissions and insert receipts; it may not admit providers. Operator mutations are capability-authenticated and audited. Owners/superusers remain trusted migration principals and must not run the application. Backup/restore and target-role verification remain deployment work.

## Fixture inspection

`inspectFixtureAdmission` is pure: given a fixture admission, already compiled fixture context, fence and timestamp, returns request/admission/implementation hashes, wire bytes, reservation, billable categories, assumptions and secret **reference**. It cannot resolve secrets or call the network. The tests exercise the same serializer, counter and factory used by the HTTPS transport.

## Future smoke command — NOT RUN

`node runtime/provider-smoke.ts` is a separate manual command, not imported by runtime boot or public routes. It requires all of:

- `GENESIS_PRIVATE_OPERATOR_MODE=enabled`;
- production `GENESIS_OPERATOR_AUTH_FILE`, externally supplied operator credential and private operator database connection;
- enabled actor with `MANAGE_PROVIDER_ADMISSION`;
- separately ADMITTED, compatible non-fixture admission with output ceiling ≤128;
- `GENESIS_SMOKE_AUTHORIZATION_FILE` matching `authSchema` in the command (purpose/id/actor/admission hash/wire hash/maximum micros/expiry/reference);
- existing owner-only directory `GENESIS_SMOKE_JOURNAL_DIRECTORY`;
- externally resolved production credential.

It uses a fixed sanitized fictitious context, no Genesis context or authority. Authorization ID owns an exclusive 0600 journal created and fsynced before sending. Existing ID refuses. There is at most one send. Journal tracks the separately authorized reservation, request/response identity and billing evidence. No organism/database writes occur. Never delete/reuse a stopped journal to retry. Ambiguity remains review-required. The command's source was inspected, but **it was not executed** in this pass. Live transport/token/usage/cancellation validation remains a later explicit authorization.
