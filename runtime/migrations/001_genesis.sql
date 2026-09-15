CREATE TABLE IF NOT EXISTS genesis_organisms (
  id TEXT PRIMARY KEY,
  state JSONB NOT NULL,
  revision BIGINT NOT NULL DEFAULT 0,
  lease TEXT,
  lease_until TIMESTAMPTZ NOT NULL DEFAULT '-infinity',
  phase TEXT NOT NULL DEFAULT 'idle'
);
CREATE TABLE IF NOT EXISTS genesis_decisions (
  id TEXT PRIMARY KEY,
  cycle BIGINT NOT NULL UNIQUE,
  at TIMESTAMPTZ NOT NULL,
  record JSONB NOT NULL
);
CREATE INDEX IF NOT EXISTS genesis_decisions_at_idx ON genesis_decisions(at);
CREATE TABLE IF NOT EXISTS genesis_memories (
  id TEXT PRIMARY KEY, decision_id TEXT NOT NULL REFERENCES genesis_decisions(id), at TIMESTAMPTZ NOT NULL, record JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS genesis_ledger (
  id TEXT PRIMARY KEY, at TIMESTAMPTZ NOT NULL, record JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS genesis_projects (id TEXT PRIMARY KEY, record JSONB NOT NULL);
CREATE TABLE IF NOT EXISTS genesis_milestones (id TEXT PRIMARY KEY, at TIMESTAMPTZ NOT NULL, record JSONB NOT NULL);
CREATE TABLE IF NOT EXISTS genesis_schedule (
  id TEXT PRIMARY KEY DEFAULT 'genesis', enabled BOOLEAN NOT NULL DEFAULT false,
  remaining_cycles INTEGER CHECK(remaining_cycles IS NULL OR remaining_cycles >= 0),
  next_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), last_heartbeat TIMESTAMPTZ,
  last_error TEXT, updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
