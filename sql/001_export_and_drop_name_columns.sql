-- Migration helper: Export and drop name columns
-- IMPORTANT: Run the export script first to create `user_mapping.csv`.
-- 1) Backup your DB (run locally where `mysqldump` is configured):
--    mysqldump -u <user> -p <database_name> > zeitschriften_db_backup_$(date +%Y%m%d_%H%M%S).sql

-- 2) Optionally create a full table backup (non-destructive):
--    CREATE TABLE benutzer_backup AS SELECT * FROM benutzer;

-- 3) After verifying the CSV export, drop the firstname/name columns:
-- Note: Adjust column names if your schema differs.
ALTER TABLE benutzer
  DROP COLUMN firstname,
  DROP COLUMN name;

-- 4) Verify table structure:
--    DESCRIBE benutzer;

-- Rollback (if you kept benutzer_backup):
--    DROP TABLE benutzer;
--    RENAME TABLE benutzer_backup TO benutzer;
