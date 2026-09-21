// Runtime V1 dormant release: no CLI can grant execution authority.
throw new Error('GENESIS_EXECUTION_NOT_AUTHORIZED_IN_THIS_RELEASE');
// Provider contract tests use injected transports in tests/runtime-v1.test.ts.
// Live provider calls require a reviewed budget/reservation and activation grant.
export {};
