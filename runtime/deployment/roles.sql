-- Explicit installer substitutes validated role/schema identifiers only.
-- Additional read-only service role; PUBLIC_OBSERVER receives identity view only.
GRANT USAGE ON SCHEMA :"schema" TO :"reader";
GRANT SELECT ON ALL TABLES IN SCHEMA :"schema" TO :"reader";
GRANT SELECT ON genesis_deployment_release TO :"worker", :"operator";
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA :"schema" FROM PUBLIC;
-- Application functions are trigger functions, including the owner-only continuous
-- admission recorder; ordinary DML triggers still work without EXECUTE grants.
-- Future objects receive no implicit normal-service grants.
ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema" REVOKE ALL ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema" REVOKE ALL ON SEQUENCES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema" REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
