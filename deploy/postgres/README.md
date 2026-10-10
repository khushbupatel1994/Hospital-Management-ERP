# PostgreSQL production database

Create a dedicated database and least-privilege application user. Do not expose PostgreSQL directly to the public internet.

Example:

```sql
CREATE ROLE erp_app LOGIN PASSWORD 'REPLACE_WITH_A_LONG_RANDOM_SECRET';
CREATE DATABASE hospital_erp OWNER erp_app;
REVOKE ALL ON DATABASE hospital_erp FROM PUBLIC;
```

Use the migration utility in `scripts/migrate_sqlite_to_postgres.py` after reviewing the generated schema and testing on a copy of the data.
