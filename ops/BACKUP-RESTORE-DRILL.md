# Backup & Restore Drill

## Objective
Prove that backups are usable, not merely that backup files exist.

## Procedure
1. Create a fresh production-like backup.
2. Copy it to isolated recovery storage.
3. Restore into a separate test environment.
4. Run database integrity checks.
5. Compare key record counts and application health.
6. Execute critical UAT workflows against the restored environment.
7. Record restore duration and data-loss window.
8. Document failures and corrective actions.

Never perform a restore drill by overwriting the live production database.
