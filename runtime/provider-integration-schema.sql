-- PREPARED / UNAPPLIED. Requires operator-schema-v1 and its preceding schemas.
CREATE TABLE genesis_provider_admissions (
 id text PRIMARY KEY, organism_id text NOT NULL REFERENCES genesis_organisms(id), payload jsonb NOT NULL,
 payload_hash text NOT NULL, status text NOT NULL CHECK(status IN ('PROPOSED','ADMITTED','REVOKED')),
 audit_id text NOT NULL REFERENCES genesis_operator_audit(id) DEFERRABLE INITIALLY DEFERRED,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE genesis_provider_receipts (
 attempt_id text PRIMARY KEY REFERENCES genesis_provider_attempts(id), provider text NOT NULL,
 response_id text NOT NULL, request_hash text NOT NULL, admission_hash text NOT NULL,
 record jsonb NOT NULL, received_at timestamptz NOT NULL DEFAULT now(), UNIQUE(provider,response_id)
);
CREATE TRIGGER immutable_provider_receipt BEFORE UPDATE OR DELETE ON genesis_provider_receipts FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE TRIGGER immutable_provider_admission_delete BEFORE DELETE ON genesis_provider_admissions FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE FUNCTION genesis_guard_provider_admission() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 IF NEW.payload IS DISTINCT FROM OLD.payload OR NEW.payload_hash IS DISTINCT FROM OLD.payload_hash OR NEW.id<>OLD.id OR NEW.organism_id<>OLD.organism_id OR NEW.created_at<>OLD.created_at OR NEW.audit_id=OLD.audit_id
 OR NOT (OLD.status='PROPOSED' AND NEW.status IN ('ADMITTED','REVOKED') OR OLD.status='ADMITTED' AND NEW.status='REVOKED') THEN RAISE EXCEPTION 'Immutable admission or invalid transition'; END IF;
 RETURN NEW; END $$;
CREATE TRIGGER provider_admission_guard BEFORE UPDATE ON genesis_provider_admissions FOR EACH ROW EXECUTE FUNCTION genesis_guard_provider_admission();
CREATE FUNCTION genesis_guard_reasoning_attempt() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
 IF OLD.record->>'protocolVersion'='2' AND (
 NEW.cycle_id<>OLD.cycle_id OR NEW.grant_id<>OLD.grant_id OR NEW.id<>OLD.id
 OR NEW.record->'protocolVersion' IS DISTINCT FROM OLD.record->'protocolVersion'
 OR NEW.record->'reservedMicros' IS DISTINCT FROM OLD.record->'reservedMicros'
 OR NEW.record->'admissionHash' IS DISTINCT FROM OLD.record->'admissionHash'
 OR NEW.record->'contextHash' IS DISTINCT FROM OLD.record->'contextHash'
 OR NEW.record->'model' IS DISTINCT FROM OLD.record->'model'
 OR NEW.record->'request' IS DISTINCT FROM OLD.record->'request'
 OR NEW.record->'context' IS DISTINCT FROM OLD.record->'context'
 OR NEW.record->'fence' IS DISTINCT FROM OLD.record->'fence'
 OR NEW.record->'owner' IS DISTINCT FROM OLD.record->'owner'
 OR NEW.record->'leaseUntil' IS DISTINCT FROM OLD.record->'leaseUntil'
 OR (OLD.record->>'status' IN ('received','not_sent','reconciled') AND NEW.record->>'status' IS DISTINCT FROM OLD.record->>'status')
 OR (OLD.record->>'status'='unknown' AND NEW.record->>'status' NOT IN ('unknown','reconciled'))
 ) THEN RAISE EXCEPTION 'Immutable reasoning request/ownership or terminal attempt'; END IF;
 RETURN NEW; END $$;
CREATE TRIGGER reasoning_attempt_guard BEFORE UPDATE ON genesis_provider_attempts FOR EACH ROW EXECUTE FUNCTION genesis_guard_reasoning_attempt();
-- Reviewed deployment grants SELECT admissions/receipts to worker; INSERT receipts;
-- existing attempt privileges retained. Operator: SELECT receipts, INSERT admissions,
-- UPDATE(status,audit_id) admissions. No runtime admission writes. No PUBLIC grants.

CREATE TRIGGER immutable_reasoning_attempt_delete BEFORE DELETE ON genesis_provider_attempts FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
CREATE INDEX provider_admissions_status ON genesis_provider_admissions(organism_id,status);
