-- Additive only. No original organism/history/schedule row is rewritten.
CREATE TABLE genesis_life_state (
 organism_id TEXT PRIMARY KEY REFERENCES genesis_organisms(id),
 schema_version INTEGER NOT NULL CHECK(schema_version=1),
 revision BIGINT NOT NULL DEFAULT 0, record JSONB NOT NULL,
 CHECK (record->>'executionLock' IN ('CLOSED','OPEN'))
);
CREATE TABLE genesis_life_events (
 id TEXT PRIMARY KEY, organism_id TEXT NOT NULL REFERENCES genesis_organisms(id),
 at TIMESTAMPTZ NOT NULL, record JSONB NOT NULL
);
CREATE TABLE genesis_action_intents (
 id TEXT PRIMARY KEY, organism_id TEXT NOT NULL REFERENCES genesis_organisms(id),
 revision BIGINT NOT NULL DEFAULT 0, payload_hash TEXT NOT NULL, record JSONB NOT NULL
);
-- Old application writers lack this versioned transaction marker. CLOSED also
-- blocks marked writers. No application route/CLI in this release can unlock it.
CREATE FUNCTION genesis_require_v2_writer() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF current_setting('genesis.writer_version',true) IS DISTINCT FROM 'runtime-v1'
    OR NOT EXISTS (SELECT 1 FROM genesis_life_state WHERE organism_id='genesis' AND record->>'executionLock'='OPEN') THEN
  RAISE EXCEPTION 'Genesis execution locked or incompatible writer';
 END IF;
 IF TG_TABLE_NAME='genesis_organisms' AND TG_OP='UPDATE' THEN
  IF NEW.state->'id' IS DISTINCT FROM OLD.state->'id' OR NEW.state->'bornAt' IS DISTINCT FROM OLD.state->'bornAt'
    OR NEW.state->'brain' IS DISTINCT FROM OLD.state->'brain' THEN
   RAISE EXCEPTION 'Protected identity/birth/saved brain cannot change';
  END IF;
 END IF;
 IF TG_OP='DELETE' THEN RETURN OLD; END IF;
 RETURN NEW;
END $$;
DO $$ DECLARE t text; BEGIN
 FOREACH t IN ARRAY ARRAY['genesis_organisms','genesis_decisions','genesis_memories','genesis_ledger','genesis_projects','genesis_milestones','genesis_schedule','genesis_external_observations'] LOOP
  EXECUTE format('CREATE TRIGGER runtime_v1_writer_fence BEFORE INSERT OR UPDATE OR DELETE ON %I FOR EACH ROW EXECUTE FUNCTION genesis_require_v2_writer()',t);
 END LOOP;
END $$;
CREATE FUNCTION genesis_immutable_event() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'Append-only event'; END $$;
CREATE TRIGGER immutable_life_events BEFORE UPDATE OR DELETE ON genesis_life_events FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE TRIGGER immutable_decisions BEFORE UPDATE OR DELETE ON genesis_decisions FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE TRIGGER immutable_memories BEFORE UPDATE OR DELETE ON genesis_memories FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
