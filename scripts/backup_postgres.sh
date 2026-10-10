#!/usr/bin/env bash
set -euo pipefail
: "${PGHOST:?PGHOST required}"; : "${PGUSER:?PGUSER required}"; : "${PGDATABASE:?PGDATABASE required}"
BACKUP_DIR="${BACKUP_DIR:-./backups/postgres}"
mkdir -p "$BACKUP_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
pg_dump --format=custom --no-owner --file="$BACKUP_DIR/hospital_erp_${STAMP}.dump" "$PGDATABASE"
find "$BACKUP_DIR" -type f -name '*.dump' -mtime +30 -delete
