"""Phase 10 production-readiness helpers.
Safe defaults; no real credentials are embedded.
"""
from __future__ import annotations
import hashlib
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def sqlite_backup(source: str, destination_dir: str) -> Path:
    src = Path(source)

    if not src.exists():
        raise FileNotFoundError(src)

    out_dir = Path(destination_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dest = out_dir / f"hospital_{utc_stamp()}.sqlite3"

    con = None
    backup_con = None

    try:
        con = sqlite3.connect(src)
        backup_con = sqlite3.connect(dest)

        con.backup(backup_con)

    finally:
        if backup_con is not None:
            backup_con.close()

        if con is not None:
            con.close()

    return dest

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_sqlite(path: str) -> dict:
    con = None

    try:
        con = sqlite3.connect(path)

        integrity_cursor = con.execute('PRAGMA integrity_check')
        integrity = integrity_cursor.fetchone()[0]
        integrity_cursor.close()

        quick_cursor = con.execute('PRAGMA quick_check')
        quick = quick_cursor.fetchone()[0]
        quick_cursor.close()

        return {
            'integrity_check': integrity,
            'quick_check': quick,
            'ok': integrity == 'ok' and quick == 'ok'
        }

    finally:
        if con is not None:
            con.close()

def postgres_dsn_from_env() -> str:
    return os.getenv('DATABASE_URL', 'postgresql://hospital_app:CHANGE_ME@localhost:5432/hospital_erp')


def run_restore_drill(backup_path: str) -> dict:
    """Restore drill for SQLite backups; production PostgreSQL restore remains an ops step."""
    check = verify_sqlite(backup_path)
    return {'backup': str(backup_path), **check}


def command_available(command: str) -> bool:
    return shutil.which(command) is not None


if __name__ == '__main__':
    print('Phase 10 production readiness helper loaded.')
    print('PostgreSQL configured:', postgres_dsn_from_env())
    print('Docker available:', command_available('docker'))
