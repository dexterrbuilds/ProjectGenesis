-- PREPARED / UNAPPLIED. Install after preparation + one-shot schemas, never on boot.
-- Runtime/application roles must not own these tables or have scope authorization_record UPDATE privilege.
CREATE TABLE genesis_continuous_scopes(
 id text PRIMARY KEY,organism_id text NOT NULL REFERENCES genesis_organisms(id),payload jsonb NOT NULL,payload_hash text NOT NULL,
 status text NOT NULL CHECK(status IN ('PROPOSED','AUTHORIZED','REVOKED','EXPIRED','REVIEW_REQUIRED')),
 authorization_record jsonb,revocation_reference text,created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE genesis_runtime_events(
 id text PRIMARY KEY,organism_id text NOT NULL REFERENCES genesis_organisms(id),payload jsonb NOT NULL,payload_hash text NOT NULL,
 dedup_key text NOT NULL,available_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN ('PENDING','CLAIMED','CONSUMED','CANCELLED','EXPIRED','FAILED','AMBIGUOUS')),
 attempts integer NOT NULL DEFAULT 0 CHECK(attempts>=0),cycle_id text UNIQUE,lease text,lease_until timestamptz,
 reason text,UNIQUE(organism_id,dedup_key)
);
CREATE INDEX genesis_due_events ON genesis_runtime_events(available_at,id) WHERE status='PENDING';
CREATE TABLE genesis_continuous_attempts(
 cycle_id text PRIMARY KEY REFERENCES genesis_cycle_attempts(id),event_id text NOT NULL REFERENCES genesis_runtime_events(id),scope_id text NOT NULL REFERENCES genesis_continuous_scopes(id),
 lease text NOT NULL,base_revision bigint NOT NULL,life_revision bigint NOT NULL,at timestamptz NOT NULL DEFAULT now(),
 status text NOT NULL CHECK(status IN ('CLAIMED','COMMITTED','FAILED','CANCELLED','AMBIGUOUS')),
 phase text NOT NULL,resources jsonb NOT NULL,claim_issued_at timestamptz,lease_until timestamptz,reserved_micros bigint NOT NULL DEFAULT 0 CHECK(reserved_micros>=0),cost_micros bigint NOT NULL DEFAULT 0 CHECK(cost_micros>=0),failure text
);
CREATE UNIQUE INDEX genesis_event_single_commit ON genesis_continuous_attempts(event_id) WHERE status='COMMITTED';
CREATE UNIQUE INDEX genesis_scope_single_claim ON genesis_continuous_attempts(scope_id) WHERE status IN ('CLAIMED','AMBIGUOUS');
CREATE INDEX genesis_scope_attempt_window ON genesis_continuous_attempts(scope_id,at);
CREATE TABLE genesis_continuous_journal(id bigserial PRIMARY KEY,event_id text REFERENCES genesis_runtime_events(id),scope_id text REFERENCES genesis_continuous_scopes(id),cycle_id text,at timestamptz NOT NULL DEFAULT now(),transition text NOT NULL,reason text);
CREATE TRIGGER immutable_continuous_journal BEFORE UPDATE OR DELETE ON genesis_continuous_journal FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE FUNCTION genesis_guard_continuous_scope() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 IF NEW.id IS DISTINCT FROM OLD.id OR NEW.organism_id IS DISTINCT FROM OLD.organism_id OR NEW.payload IS DISTINCT FROM OLD.payload OR NEW.payload_hash IS DISTINCT FROM OLD.payload_hash OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN RAISE EXCEPTION 'Immutable continuous scope'; END IF;
 IF NOT (OLD.status='PROPOSED' AND NEW.status IN ('AUTHORIZED','REVOKED','EXPIRED') OR OLD.status='AUTHORIZED' AND NEW.status IN ('REVOKED','EXPIRED','REVIEW_REQUIRED')) THEN RAISE EXCEPTION 'Continuous scope transition'; END IF;
 IF OLD.status<>'PROPOSED' AND NEW.authorization_record IS DISTINCT FROM OLD.authorization_record THEN RAISE EXCEPTION 'Immutable scope authorization_record'; END IF;
 RETURN NEW; END $$;
CREATE TRIGGER continuous_scope_transition BEFORE UPDATE ON genesis_continuous_scopes FOR EACH ROW EXECUTE FUNCTION genesis_guard_continuous_scope();
CREATE TRIGGER immutable_continuous_scope BEFORE DELETE ON genesis_continuous_scopes FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE FUNCTION genesis_guard_runtime_event() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 IF NEW.id IS DISTINCT FROM OLD.id OR NEW.organism_id IS DISTINCT FROM OLD.organism_id OR NEW.payload IS DISTINCT FROM OLD.payload OR NEW.payload_hash IS DISTINCT FROM OLD.payload_hash OR NEW.dedup_key IS DISTINCT FROM OLD.dedup_key THEN RAISE EXCEPTION 'Immutable event envelope'; END IF;
 IF NOT (OLD.status='PENDING' AND NEW.status IN ('CLAIMED','CANCELLED','EXPIRED','FAILED') OR OLD.status='CLAIMED' AND NEW.status IN ('PENDING','CONSUMED','FAILED','CANCELLED','AMBIGUOUS')) THEN RAISE EXCEPTION 'Event transition'; END IF;
 RETURN NEW; END $$;
CREATE TRIGGER runtime_event_transition BEFORE UPDATE ON genesis_runtime_events FOR EACH ROW EXECUTE FUNCTION genesis_guard_runtime_event();
CREATE TRIGGER immutable_runtime_event BEFORE DELETE ON genesis_runtime_events FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();

-- Private transaction proof, written only by the decision admission trigger.
-- Not an authority flag, not renewable, and never reused in another transaction.
CREATE TABLE genesis_continuous_admissions(
 cycle_id text PRIMARY KEY REFERENCES genesis_continuous_attempts(cycle_id),
 transaction_id xid8 NOT NULL, lease text NOT NULL, event_id text NOT NULL,
 admitted_at timestamptz NOT NULL, lease_until timestamptz NOT NULL,
 CHECK(admitted_at<lease_until)
);
REVOKE ALL ON genesis_continuous_admissions FROM PUBLIC;
CREATE TRIGGER immutable_continuous_admission BEFORE UPDATE OR DELETE ON genesis_continuous_admissions FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE FUNCTION genesis_admit_continuous_decision() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE o genesis_organisms%ROWTYPE; l genesis_life_state%ROWTYPE;
 a genesis_continuous_attempts%ROWTYPE; e genesis_runtime_events%ROWTYPE; s genesis_continuous_scopes%ROWTYPE;
 attempt genesis_cycle_attempts%ROWTYPE; t timestamptz; disclosure_until timestamptz; schedule_enabled boolean; binding jsonb; epoch bigint; r record; v jsonb;
BEGIN
 IF coalesce(current_setting('genesis.continuous_cycle',true),'')='' THEN RETURN NEW; END IF;
 -- All cooperating paths serialize first on organism. No callback or network work here.
 SELECT * INTO o FROM genesis_organisms WHERE id='genesis' FOR UPDATE;
 SELECT * INTO l FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE;
 SELECT * INTO a FROM genesis_continuous_attempts WHERE cycle_id=NEW.id FOR UPDATE;
 SELECT * INTO s FROM genesis_continuous_scopes WHERE id=a.scope_id FOR UPDATE;
 SELECT enabled INTO schedule_enabled FROM genesis_schedule WHERE id='genesis' FOR UPDATE;
 SELECT * INTO e FROM genesis_runtime_events WHERE id=a.event_id FOR UPDATE;
 SELECT * INTO attempt FROM genesis_cycle_attempts WHERE id=NEW.id FOR UPDATE;
 binding:=NEW.record#>'{lifeContext,contextManifest,disclosure,binding}';
 IF to_regclass('genesis_control_state') IS NOT NULL THEN
  EXECUTE 'SELECT review_revision FROM genesis_control_state WHERE organism_id=''genesis'' FOR UPDATE' INTO epoch;
  IF binding IS NULL OR binding->>'installed' IS DISTINCT FROM 'true' OR (binding->>'revision')::bigint IS DISTINCT FROM epoch THEN RAISE EXCEPTION 'DISCLOSURE_INVALID'; END IF;
 ELSE
  IF binding->>'installed' IS DISTINCT FROM 'false' THEN RAISE EXCEPTION 'DISCLOSURE_INVALID'; END IF;
 END IF;
 IF a.cycle_id IS NULL OR a.status<>'CLAIMED' OR e.status<>'CLAIMED' OR e.cycle_id IS DISTINCT FROM a.cycle_id
 OR a.cycle_id IS DISTINCT FROM current_setting('genesis.continuous_cycle',true)
 OR a.lease IS DISTINCT FROM current_setting('genesis.continuous_lease',true)
 OR e.lease IS DISTINCT FROM a.lease OR o.lease IS DISTINCT FROM a.lease
 OR attempt.lease IS DISTINCT FROM a.lease OR attempt.status<>'preparing'
 OR o.lease_until IS DISTINCT FROM e.lease_until OR a.lease_until IS DISTINCT FROM e.lease_until
 OR NEW.record->>'organismId' IS DISTINCT FROM o.state->>'id'
 OR e.payload->>'organismId' IS DISTINCT FROM o.state->>'id'
 OR s.payload->>'organismId' IS DISTINCT FROM o.state->>'id'
 THEN RAISE EXCEPTION 'OWNERSHIP_MISMATCH'; END IF;
 IF attempt.cancelled THEN RAISE EXCEPTION 'CANCELLED'; END IF;
 IF o.revision<>a.base_revision OR l.revision<>a.life_revision OR (NEW.record#>>'{lifeContext,revision}')::bigint IS DISTINCT FROM a.life_revision THEN RAISE EXCEPTION 'REVISION_STALE'; END IF;
 IF s.status<>'AUTHORIZED' OR s.authorization_record->>'payloadHash' IS DISTINCT FROM s.payload_hash
 OR s.authorization_record->>'issuer' IS DISTINCT FROM s.payload->>'issuer'
 OR s.authorization_record->>'reference' IS DISTINCT FROM s.payload->>'authorizationReference'

 OR l.record->>'executionLock' IS DISTINCT FROM 'CLOSED' OR schedule_enabled IS DISTINCT FROM false
 OR l.record#>>'{biologicalContext,mode}' IS DISTINCT FROM 'SAVED-OBSERVATION-ONLY'
 OR l.record->>'constitutionHash' IS DISTINCT FROM s.payload->>'constitutionHash'

 OR NEW.record#>>'{memory,episode,record,continuousAuthority,scopeId}' IS DISTINCT FROM s.id
 OR NEW.record#>>'{memory,episode,record,continuousAuthority,permissionHash}' IS DISTINCT FROM s.payload->>'permissionHash'
 THEN RAISE EXCEPTION 'SCOPE_INVALID'; END IF;
 IF epoch IS NOT NULL THEN
  -- The context was recompiled under the organism lock. Recheck review membership,
  -- versions and time-dependent effective status without an archive/context scan.
  FOR r IN EXECUTE 'SELECT DISTINCT ON(source_type,source_id,audience) * FROM genesis_disclosure_reviews WHERE organism_id=''genesis'' ORDER BY source_type,source_id,audience,version DESC LIMIT 257' LOOP
   SELECT value INTO v FROM jsonb_array_elements(binding->'reviews') WHERE value->>'id'=r.id;
   IF v IS NULL OR (v->>'version')::integer IS DISTINCT FROM r.version OR v->>'sourceHash' IS DISTINCT FROM r.source_hash
    OR v->>'audience' IS DISTINCT FROM r.audience OR v->>'sourceId' IS DISTINCT FROM r.source_id

   THEN RAISE EXCEPTION 'DISCLOSURE_INVALID'; END IF;
   IF v->>'effective' NOT IN ('EXPIRED','STALE_SOURCE') THEN disclosure_until:=least(disclosure_until,r.expires_at); END IF;
  END LOOP;
 END IF;
 IF EXISTS(SELECT 1 FROM genesis_provider_attempts WHERE cycle_id=NEW.id AND record->>'status' IN ('reserved','dispatching','unknown')) THEN RAISE EXCEPTION 'PROVIDER_AMBIGUITY'; END IF;
 -- Final time sample after all validation; from here only atomic local writes remain.
 t:=clock_timestamp();
 IF e.lease_until IS NULL OR t>=e.lease_until THEN RAISE EXCEPTION USING MESSAGE='LEASE_EXPIRED_BEFORE_ADMISSION',DETAIL=json_build_object('admitted',false,'databaseTime',t,'deadline',e.lease_until,'marginMs',extract(epoch FROM(e.lease_until-t))*1000)::text; END IF;
 IF t<(s.payload->>'issuedAt')::timestamptz OR t>=(s.payload->>'expiresAt')::timestamptz OR (e.payload->>'expiresAt' IS NOT NULL AND t>=(e.payload->>'expiresAt')::timestamptz) THEN RAISE EXCEPTION 'SCOPE_INVALID'; END IF;
 IF disclosure_until IS NOT NULL AND t>=disclosure_until THEN RAISE EXCEPTION 'DISCLOSURE_INVALID'; END IF;
 INSERT INTO genesis_continuous_admissions(cycle_id,transaction_id,lease,event_id,admitted_at,lease_until)
 VALUES(a.cycle_id,pg_current_xact_id(),a.lease,e.id,t,e.lease_until);
 RETURN NEW;
END $$;
-- Pin the definer's namespace; no caller-controlled search_path or temp shadowing.
DO $$ BEGIN EXECUTE format('ALTER FUNCTION genesis_admit_continuous_decision() SET search_path TO %I, pg_catalog, pg_temp',current_schema()); END $$;
REVOKE ALL ON FUNCTION genesis_admit_continuous_decision() FROM PUBLIC;
CREATE TRIGGER aaa_continuous_admission BEFORE INSERT ON genesis_decisions FOR EACH ROW EXECUTE FUNCTION genesis_admit_continuous_decision();

-- The single-use branch below is retained verbatim. No OPEN fallback.
CREATE OR REPLACE FUNCTION genesis_require_v2_writer() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE admitted boolean; g genesis_execution_grants%ROWTYPE; o jsonb; a genesis_continuous_attempts%ROWTYPE; s genesis_continuous_scopes%ROWTYPE; e genesis_runtime_events%ROWTYPE;
BEGIN

 IF current_setting('genesis.continuous_cycle',true) IS NOT NULL AND current_setting('genesis.continuous_cycle',true)<>'' THEN
  IF coalesce(current_setting('genesis.oneshot_grant',true),'')<>'' THEN RAISE EXCEPTION 'Mixed authority'; END IF;
  SELECT * INTO a FROM genesis_continuous_attempts WHERE cycle_id=current_setting('genesis.continuous_cycle',true);
  SELECT * INTO s FROM genesis_continuous_scopes WHERE id=a.scope_id;
  SELECT * INTO e FROM genesis_runtime_events WHERE id=a.event_id;
  SELECT state INTO o FROM genesis_organisms WHERE id='genesis';
  IF current_setting('genesis.writer_version',true) IS DISTINCT FROM 'runtime-v1' OR a.cycle_id IS NULL OR a.status<>'CLAIMED' OR a.lease IS DISTINCT FROM current_setting('genesis.continuous_lease',true) OR e.status<>'CLAIMED' OR e.cycle_id IS DISTINCT FROM a.cycle_id OR s.payload->>'organismId' IS DISTINCT FROM o->>'id'
   OR NOT EXISTS(SELECT 1 FROM genesis_life_state WHERE organism_id='genesis' AND record->>'executionLock'='CLOSED') OR EXISTS(SELECT 1 FROM genesis_schedule WHERE enabled) THEN RAISE EXCEPTION 'Continuous writer fence'; END IF;
  -- Expired/revoked claims may release only their own metadata. Never an organism effect.
  IF TG_TABLE_NAME='genesis_organisms' AND TG_OP='UPDATE' THEN
   IF NEW.state IS NOT DISTINCT FROM OLD.state AND NEW.revision=OLD.revision AND NEW.lease IS NULL AND OLD.lease=a.lease THEN RETURN NEW; END IF;
  END IF;
  SELECT EXISTS(SELECT 1 FROM genesis_continuous_admissions WHERE cycle_id=a.cycle_id AND lease=a.lease AND event_id=e.id AND transaction_id=pg_current_xact_id()) INTO admitted;
  IF NOT admitted AND (s.status<>'AUTHORIZED' OR s.authorization_record->>'payloadHash' IS DISTINCT FROM s.payload_hash OR (s.payload->>'expiresAt')::timestamptz<=clock_timestamp()) THEN RAISE EXCEPTION 'Continuous scope inactive'; END IF;
  IF TG_TABLE_NAME='genesis_organisms' AND TG_OP='UPDATE' THEN
   IF NEW.state IS DISTINCT FROM OLD.state AND NOT admitted THEN RAISE EXCEPTION 'CONTINUOUS_ADMISSION_REQUIRED'; END IF;
   IF NEW.state - 'cycles' - 'activity' IS DISTINCT FROM OLD.state - 'cycles' - 'activity' OR OLD.revision<>a.base_revision OR NEW.revision NOT IN (OLD.revision,OLD.revision+1) OR (NEW.state->>'cycles')::int NOT IN ((OLD.state->>'cycles')::int,(OLD.state->>'cycles')::int+1) THEN RAISE EXCEPTION 'Protected continuous state'; END IF;
  ELSIF TG_TABLE_NAME='genesis_decisions' AND TG_OP='INSERT' THEN
   IF NEW.id IS DISTINCT FROM a.cycle_id OR NEW.cycle<>(o->>'cycles')::int+1 OR (NEW.record->>'schemaVersion')::int<>2 OR NOT admitted THEN RAISE EXCEPTION 'Continuous decision fence'; END IF;
  ELSE RAISE EXCEPTION 'No external/table effects in continuous scope'; END IF;
  RETURN NEW;
 END IF;
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

-- Additional local write tables share the same admission proof when executing a
-- continuous transaction. Administrative intake/claim/cleanup is not a life effect.
CREATE FUNCTION genesis_require_continuous_admission() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE cycle text:=current_setting('genesis.continuous_cycle',true);
BEGIN
 IF coalesce(cycle,'')='' THEN RETURN NEW; END IF;
 IF TG_TABLE_NAME='genesis_runtime_events' AND TG_OP='UPDATE' THEN IF NEW.status<>'CONSUMED' THEN RETURN NEW; END IF; END IF;
 IF TG_TABLE_NAME='genesis_continuous_attempts' THEN IF NEW.status<>'COMMITTED' THEN RETURN NEW; END IF; END IF;
 IF NOT EXISTS(SELECT 1 FROM genesis_continuous_admissions WHERE cycle_id=cycle AND lease=current_setting('genesis.continuous_lease',true) AND transaction_id=pg_current_xact_id()) THEN RAISE EXCEPTION 'CONTINUOUS_ADMISSION_REQUIRED'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER continuous_life_admission BEFORE UPDATE ON genesis_life_state FOR EACH ROW EXECUTE FUNCTION genesis_require_continuous_admission();
CREATE TRIGGER continuous_episode_admission BEFORE INSERT ON genesis_life_events FOR EACH ROW EXECUTE FUNCTION genesis_require_continuous_admission();
CREATE TRIGGER continuous_intent_admission BEFORE INSERT OR UPDATE ON genesis_action_intents FOR EACH ROW EXECUTE FUNCTION genesis_require_continuous_admission();
CREATE TRIGGER continuous_event_admission BEFORE INSERT OR UPDATE ON genesis_runtime_events FOR EACH ROW EXECUTE FUNCTION genesis_require_continuous_admission();
CREATE TRIGGER continuous_attempt_admission BEFORE UPDATE ON genesis_continuous_attempts FOR EACH ROW EXECUTE FUNCTION genesis_require_continuous_admission();
