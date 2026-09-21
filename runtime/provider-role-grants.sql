-- PREPARED / UNAPPLIED. Apply after provider-integration-schema.sql and reviewed
-- operator-role-grants.sql with the SAME schema/worker/operator variables.
REVOKE ALL ON genesis_provider_admissions,genesis_provider_receipts FROM PUBLIC;
GRANT SELECT ON genesis_provider_admissions,genesis_provider_receipts TO :"worker", :"operator";
GRANT INSERT ON genesis_provider_receipts TO :"worker";
GRANT INSERT ON genesis_provider_admissions TO :"operator";
GRANT UPDATE(status,audit_id) ON genesis_provider_admissions TO :"operator";
-- No admission mutation/actor mutation/secret table/receipt mutation is granted
-- to worker. No new observer privileges. No permission to execute a cycle.
