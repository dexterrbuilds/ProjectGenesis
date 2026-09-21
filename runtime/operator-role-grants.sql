-- PREPARED, NOT INSTALLED. MIGRATION_OWNER supplies existing NOLOGIN group roles
-- using psql variables schema, observer, worker, operator. Never run on boot.
-- Login roles must be non-owner/NOSUPERUSER/NOCREATEROLE/NOCREATEDB/NOBYPASSRLS,
-- members of exactly one group; worker/observer must not inherit operator/owner.
-- New dedicated schema only: owner must audit pre-existing PUBLIC privileges.
REVOKE ALL ON SCHEMA :"schema" FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA :"schema" FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA :"schema" FROM PUBLIC;
GRANT USAGE ON SCHEMA :"schema" TO :"observer", :"worker", :"operator";
GRANT SELECT ON genesis_public_identity TO :"observer";
-- Worker needs source data for private context and execution, not actor/control writes.
GRANT SELECT ON genesis_organisms,genesis_schedule,genesis_decisions,genesis_memories,genesis_projects,genesis_ledger,genesis_milestones,genesis_life_state,genesis_life_events,genesis_action_intents,genesis_external_observations,genesis_cycle_attempts,genesis_provider_grants,genesis_provider_attempts,genesis_execution_grants,genesis_continuous_scopes,genesis_runtime_events,genesis_continuous_attempts,genesis_continuous_journal,genesis_control_state,genesis_disclosure_reviews TO :"worker";
-- PostgreSQL row-share locking requires UPDATE on at least one column. Only heartbeat
-- metadata is writable; enabled/due-time/remaining-cycle authority stays inaccessible.
GRANT UPDATE(last_heartbeat) ON genesis_schedule TO :"worker";
GRANT UPDATE(state,revision,lease,lease_until,phase) ON genesis_organisms TO :"worker";
GRANT UPDATE(record,revision) ON genesis_life_state TO :"worker";
GRANT INSERT ON genesis_decisions,genesis_life_events,genesis_action_intents,genesis_cycle_attempts,genesis_provider_attempts,genesis_runtime_events,genesis_continuous_attempts,genesis_continuous_journal TO :"worker";
GRANT UPDATE ON genesis_action_intents,genesis_cycle_attempts,genesis_provider_attempts,genesis_runtime_events,genesis_continuous_attempts TO :"worker";
GRANT UPDATE(status,cycle_id,lease,result,updated_at) ON genesis_execution_grants TO :"worker";
GRANT UPDATE(status,revocation_reference) ON genesis_continuous_scopes TO :"worker";
GRANT USAGE ON SEQUENCE genesis_continuous_journal_id_seq TO :"worker";
-- Private control process is trusted to enforce per-actor capabilities; no SQL input API.
GRANT SELECT ON ALL TABLES IN SCHEMA :"schema" TO :"operator";
GRANT UPDATE(lease,lease_until,phase) ON genesis_organisms TO :"operator";
GRANT UPDATE(record,revision) ON genesis_life_state TO :"operator";
GRANT UPDATE(review_revision) ON genesis_control_state TO :"operator";
GRANT INSERT ON genesis_operator_audit,genesis_disclosure_reviews,genesis_recovery_dispositions,genesis_execution_grants,genesis_continuous_scopes,genesis_life_events,genesis_runtime_events,genesis_continuous_journal TO :"operator";
GRANT UPDATE(status,authorization_record,result,updated_at) ON genesis_execution_grants TO :"operator";
GRANT UPDATE(status,authorization_record,revocation_reference) ON genesis_continuous_scopes TO :"operator";
GRANT UPDATE ON genesis_cycle_attempts,genesis_provider_attempts,genesis_runtime_events,genesis_continuous_attempts,genesis_action_intents TO :"operator";
GRANT USAGE ON SEQUENCE genesis_continuous_journal_id_seq TO :"operator";
-- No actor INSERT/UPDATE, schedule UPDATE, historical UPDATE/DELETE, schema CREATE,
-- TRUNCATE, trigger disabling or ownership is granted to normal roles.

-- Admission proof is owner-written by a restricted trigger; workers may inspect only.
GRANT SELECT ON genesis_continuous_admissions TO :"worker";
REVOKE INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER ON genesis_continuous_admissions FROM :"worker", :"operator", :"observer";
