-- Structural release record only. No authority, provider admission, actor or review.
CREATE TABLE genesis_deployment_release (
 id text PRIMARY KEY CHECK(id='deployment-v1'),
 runtime_hash text NOT NULL CHECK(runtime_hash ~ '^[a-f0-9]{64}$'),
 sql_hashes jsonb NOT NULL,
 installed_at timestamptz NOT NULL DEFAULT now()
);
CREATE TRIGGER deployment_release_immutable BEFORE UPDATE OR DELETE ON genesis_deployment_release
 FOR EACH ROW EXECUTE FUNCTION genesis_immutable_event();
-- Runtime V1 execution is grant/scoped only. No normal role can open a generic lock.
ALTER TABLE genesis_life_state ADD CONSTRAINT deployment_execution_closed
 CHECK((record->>'executionLock') IS NOT DISTINCT FROM 'CLOSED');
