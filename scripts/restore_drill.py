import sys
from production_readiness import run_restore_drill
if len(sys.argv) != 2:
    raise SystemExit('Usage: python scripts/restore_drill.py BACKUP_FILE')
print(run_restore_drill(sys.argv[1]))
