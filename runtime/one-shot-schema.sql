-- Explicit additive preparation only. Not registered for boot or canonical migration.
CREATE TABLE IF NOT EXISTS genesis_execution_grants (
 id text PRIMARY KEY,
 payload jsonb NOT NULL,
 payload_hash text NOT NULL,
 status text NOT NULL CHECK(status IN ('PROPOSED','AUTHORIZED','CLAIMED','CONSUMED','EXPIRED','REVOKED','FAILED','AMBIGUOUS')),
 authorization_record jsonb,
 cycle_id text UNIQUE,
 lease text,
 result text,
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS genesis_one_unresolved_claim
 ON genesis_execution_grants ((payload->>'organismId')) WHERE status IN ('CLAIMED','AMBIGUOUS');
-- Reviewed deployment must explicitly replace the old OPEN-based writer fence.
-- This draft is installed ONLY on isolated copies in this pass.
CREATE OR REPLACE FUNCTION genesis_require_v2_writer() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE g genesis_execution_grants%ROWTYPE; o jsonb;
BEGIN
 SELECT * INTO g FROM genesis_execution_grants WHERE id=current_setting('genesis.oneshot_grant',true);
 SELECT state INTO o FROM genesis_organisms WHERE id='genesis';
 IF current_setting('genesis.writer_version',true) IS DISTINCT FROM 'runtime-v1'
 OR g.id IS NULL OR g.status<>'CLAIMED' OR g.lease IS DISTINCT FROM current_setting('genesis.oneshot_lease',true)
 OR g.authorization_record->>'payloadHash' IS DISTINCT FROM g.payload_hash
 OR g.payload->>'organismId' IS DISTINCT FROM o->>'id'
 OR (g.payload->>'expectedDecisionCount')::int<>7 OR (g.payload->>'maximumCycles')::int<>1
 OR (g.payload->>'expiresAt')::timestamptz<=now()
 OR NOT EXISTS(SELECT 1 FROM genesis_life_state WHERE organism_id='genesis' AND record->>'executionLock'='CLOSED')
 OR NOT EXISTS(SELECT 1 FROM genesis_schedule WHERE id='genesis' AND enabled=false) THEN
  RAISE EXCEPTION 'Valid single-use closed-state grant required';
 END IF;
 IF TG_TABLE_NAME='genesis_organisms' AND TG_OP='UPDATE' THEN
  IF (OLD.state->>'cycles')::int<>7 OR (NEW.state->>'cycles')::int NOT IN (7,8)
  OR NEW.state - 'cycles' - 'activity' IS DISTINCT FROM OLD.state - 'cycles' - 'activity'
  OR OLD.revision<>(g.payload->>'stateRevision')::bigint
  OR NEW.revision NOT IN (OLD.revision,OLD.revision+1) THEN RAISE EXCEPTION 'Protected one-shot organism state'; END IF;
 ELSIF TG_TABLE_NAME='genesis_decisions' AND TG_OP='INSERT' THEN
  IF NEW.id IS DISTINCT FROM g.cycle_id OR NEW.cycle<>8 OR (o->>'cycles')::int<>7
  OR (NEW.record->>'schemaVersion')::int<>2 THEN RAISE EXCEPTION 'One-shot decision identity'; END IF;
 ELSE RAISE EXCEPTION 'Effect/table outside first-awakening grant';
 END IF;
 RETURN NEW;
END $$;
CREATE OR REPLACE FUNCTION genesis_guard_grant_transition() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.id IS DISTINCT FROM OLD.id OR NEW.payload IS DISTINCT FROM OLD.payload
 OR NEW.payload_hash IS DISTINCT FROM OLD.payload_hash THEN RAISE EXCEPTION 'Grant payload immutable'; END IF;
 IF NOT ((OLD.status='PROPOSED' AND NEW.status IN ('AUTHORIZED','REVOKED','EXPIRED'))
 OR (OLD.status='AUTHORIZED' AND NEW.status IN ('CLAIMED','REVOKED','EXPIRED'))
 OR (OLD.status='CLAIMED' AND NEW.status IN ('CONSUMED','REVOKED','FAILED','AMBIGUOUS'))) THEN
  RAISE EXCEPTION 'Grant transition/reuse forbidden';
 END IF;
 IF OLD.status<>'PROPOSED' AND NEW.authorization_record IS DISTINCT FROM OLD.authorization_record THEN RAISE EXCEPTION 'Authorization immutable'; END IF;
 IF OLD.status='CLAIMED' AND (NEW.lease IS DISTINCT FROM OLD.lease OR NEW.cycle_id IS DISTINCT FROM OLD.cycle_id) THEN RAISE EXCEPTION 'Claim immutable'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER one_shot_grant_transition BEFORE UPDATE ON genesis_execution_grants FOR EACH ROW EXECUTE FUNCTION genesis_guard_grant_transition();
CREATE TRIGGER immutable_execution_grants BEFORE DELETE ON genesis_execution_grants FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
