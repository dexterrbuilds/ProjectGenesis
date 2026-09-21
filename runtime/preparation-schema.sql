-- Preparation schema only: not in migration runner and NOT applied to canonical Genesis.
CREATE TABLE genesis_cycle_attempts (
 id TEXT PRIMARY KEY, lease TEXT NOT NULL, cancelled BOOLEAN NOT NULL DEFAULT false,
 status TEXT NOT NULL CHECK(status IN ('preparing','committed')), revision BIGINT NOT NULL
);
CREATE TABLE genesis_provider_grants (id TEXT PRIMARY KEY, record JSONB NOT NULL);
CREATE TABLE genesis_provider_attempts (
 id TEXT PRIMARY KEY, cycle_id TEXT NOT NULL, grant_id TEXT NOT NULL,
 at TIMESTAMPTZ NOT NULL DEFAULT now(), record JSONB NOT NULL
);
