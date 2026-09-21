-- PREPARED / UNAPPLIED. Requires 003, preparation, one-shot, continuous schemas.
-- Credentials live outside SQL. Actors are provisioned only by MIGRATION_OWNER.
CREATE TABLE genesis_operator_actors (
 id text PRIMARY KEY, enabled boolean NOT NULL, capabilities text[] NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 CHECK(capabilities <@ ARRAY['VIEW_PRIVATE_STATE','REVIEW_DISCLOSURE','MANAGE_ONE_SHOT','MANAGE_CONTINUOUS','RECORD_HUMAN_RESPONSE','INSPECT_RECOVERY','RESOLVE_RECOVERY','MANAGE_PROVIDER_ADMISSION']::text[])
);
CREATE TABLE genesis_control_state (
 organism_id text PRIMARY KEY REFERENCES genesis_organisms(id),
 schema_version integer NOT NULL CHECK(schema_version=1), review_revision bigint NOT NULL DEFAULT 0 CHECK(review_revision>=0)
);
INSERT INTO genesis_control_state(organism_id,schema_version) SELECT id,1 FROM genesis_organisms;
CREATE TABLE genesis_operator_audit (
 id text PRIMARY KEY,at timestamptz NOT NULL DEFAULT now(),actor_id text NOT NULL REFERENCES genesis_operator_actors(id),
 capability text NOT NULL,operation text NOT NULL,organism_id text NOT NULL REFERENCES genesis_organisms(id),
 target_id text,previous_hash text,requested_hash text NOT NULL,reason_reference text NOT NULL,
 result text NOT NULL CHECK(result IN ('SUCCEEDED','REFUSED')),result_hash text,runtime_hash text NOT NULL
);
CREATE TABLE genesis_disclosure_reviews (
 id text PRIMARY KEY,organism_id text NOT NULL REFERENCES genesis_organisms(id),source_type text NOT NULL,source_id text NOT NULL,
 source_hash text NOT NULL CHECK(source_hash ~ '^[a-f0-9]{64}$'),audience text NOT NULL CHECK(audience IN ('INTERNAL_USE','PROVIDER_DISCLOSURE','PUBLIC_DISCLOSURE')),
 version integer NOT NULL CHECK(version>0),schema_version integer NOT NULL CHECK(schema_version=1),
 decision text NOT NULL CHECK(decision IN ('APPROVED','DENIED','REVOKED','EXPIRED')),
 reviewer_id text NOT NULL REFERENCES genesis_operator_actors(id),reason_reference text NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),expires_at timestamptz,
 UNIQUE(organism_id,source_type,source_id,audience,version),CHECK(expires_at IS NULL OR expires_at>created_at)
);
CREATE INDEX genesis_disclosure_latest ON genesis_disclosure_reviews(organism_id,source_type,source_id,audience,version DESC);
CREATE TABLE genesis_recovery_dispositions (
 id text PRIMARY KEY,organism_id text NOT NULL REFERENCES genesis_organisms(id),actor_id text NOT NULL REFERENCES genesis_operator_actors(id),
 target_type text NOT NULL CHECK(target_type IN ('one_shot','continuous','provider')),target_id text NOT NULL,
 previous_hash text NOT NULL,disposition text NOT NULL,reference text NOT NULL,facts jsonb NOT NULL,at timestamptz NOT NULL DEFAULT now(),
 CHECK(disposition IN ('CONFIRMED_NO_EXTERNAL_EFFECT','CONFIRMED_EXTERNAL_EFFECT_WITHOUT_LOCAL_COMMIT','CONFIRMED_LOCAL_COMMIT','UNRESOLVED_REMAIN_STOPPED','PROVIDER_NOT_EXECUTED','PROVIDER_BILLED','PROVIDER_UNKNOWN'))
);
CREATE INDEX genesis_recovery_target ON genesis_recovery_dispositions(target_type,target_id,at);
CREATE TRIGGER immutable_operator_audit BEFORE UPDATE OR DELETE ON genesis_operator_audit FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE TRIGGER immutable_disclosure_reviews BEFORE UPDATE OR DELETE ON genesis_disclosure_reviews FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE TRIGGER immutable_recovery_dispositions BEFORE UPDATE OR DELETE ON genesis_recovery_dispositions FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE FUNCTION genesis_require_control_privilege() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 -- Runtime column UPDATE rights for consuming claims must not authorize a proposed authority.
 IF NEW.status='AUTHORIZED' AND NOT has_table_privilege(current_user,'genesis_operator_audit','INSERT') THEN
  RAISE EXCEPTION 'Private operator role required';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER private_grant_authorization BEFORE UPDATE ON genesis_execution_grants FOR EACH ROW EXECUTE FUNCTION genesis_require_control_privilege();
CREATE TRIGGER private_scope_authorization BEFORE UPDATE ON genesis_continuous_scopes FOR EACH ROW EXECUTE FUNCTION genesis_require_control_privilege();
ALTER TABLE genesis_disclosure_reviews ADD COLUMN audit_id text NOT NULL REFERENCES genesis_operator_audit(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE genesis_recovery_dispositions ADD COLUMN audit_id text NOT NULL REFERENCES genesis_operator_audit(id) DEFERRABLE INITIALLY DEFERRED;
CREATE FUNCTION genesis_guard_review_insert() RETURNS trigger LANGUAGE plpgsql AS $$ DECLARE previous integer; BEGIN
 PERFORM 1 FROM genesis_organisms WHERE id=NEW.organism_id FOR UPDATE;
 PERFORM 1 FROM genesis_control_state WHERE organism_id=NEW.organism_id FOR UPDATE;
 SELECT coalesce(max(version),0) INTO previous FROM genesis_disclosure_reviews WHERE organism_id=NEW.organism_id AND source_type=NEW.source_type AND source_id=NEW.source_id AND audience=NEW.audience;
 IF NEW.version<>previous+1 OR NEW.decision='REVOKED' AND previous=0 THEN RAISE EXCEPTION 'Review version conflict'; END IF;
 UPDATE genesis_control_state SET review_revision=review_revision+1 WHERE organism_id=NEW.organism_id;
 RETURN NEW; END $$;
CREATE TRIGGER disclosure_insert_guard BEFORE INSERT ON genesis_disclosure_reviews FOR EACH ROW EXECUTE FUNCTION genesis_guard_review_insert();
CREATE FUNCTION genesis_guard_private_input() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 IF NEW.record->'record'->>'type'='human_response' AND NOT has_table_privilege(current_user,'genesis_operator_audit','INSERT') THEN RAISE EXCEPTION 'Private intake role required'; END IF;
 RETURN NEW; END $$;
CREATE TRIGGER private_human_response BEFORE INSERT ON genesis_life_events FOR EACH ROW EXECUTE FUNCTION genesis_guard_private_input();
-- This narrow view contains no raw Life State or private historical content.
CREATE VIEW genesis_public_identity AS SELECT state->>'id' AS organism_id,state->>'name' AS name,state->>'bornAt' AS born_at,(state->>'cycles')::integer AS decisions FROM genesis_organisms;
