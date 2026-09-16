-- Read-only external evidence; never credited to the simulated USD wallet.
CREATE TABLE IF NOT EXISTS genesis_external_observations (
  id TEXT PRIMARY KEY,
  checked_at TIMESTAMPTZ NOT NULL,
  record JSONB NOT NULL
);
