# Pass-7 readiness update — additive Pass 7.1 evidence

This update preserves the original Pass-7 report, failed test logs and artifact manifest unchanged.

The failing regression now reports its real reason: **`Continuous stale claim`**. A detailed trace confirms valid attempt/event bindings but an actual event lease **7 ms expired** at the rejecting check. The injected before-claim crash creates no attempt or lease; the second tick claims normally. No stale recovery timestamp or inherited planner timer was demonstrated.

Fifty isolated unchanged-limit executions produced **45 passes and 5 failures**. Seven new boundary tests and all 17 deployment-critical tests passed. Dormant E2E, TypeScript and lint passed. Canonical digest remains `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`; Genesis still has seven decisions and zero V2 episodes, with execution CLOSED and schedule DISABLED.

**No runtime correction was applied.** The investigation establishes legitimate lease expiry during normal preparation/checks but does not establish an implementation violation that can safely be corrected within the existing contract. The original `COMMITTED` assertion, 250 ms lease, 100 ms timeout and all fences remain unchanged.

The isolated-stability gate was not met, so no new complete-suite or Webpack promotion result is claimed. The prior 532-pass/1-fail full-suite result remains historical evidence. Docker is unavailable; container execution remains unverified.

See [SHORT_LEASE_RECOVERY_REPORT.md](SHORT_LEASE_RECOVERY_REPORT.md) and its separately hashed `short-lease-evidence` package. No deployment, authority, provider call, canonical migration or awakening is authorized by these results.

SHORT-LEASE RECOVERY REMAINS UNRESOLVED — PASS 7 NOT READY
