import sys
from production_readiness import sqlite_backup, sha256_file, verify_sqlite

if len(sys.argv) != 3:
    raise SystemExit('Usage: python scripts/backup_sqlite.py DATABASE_PATH BACKUP_DIR')
backup = sqlite_backup(sys.argv[1], sys.argv[2])
print('Backup:', backup)
print('SHA256:', sha256_file(str(backup)))
print('Verification:', verify_sqlite(str(backup)))
