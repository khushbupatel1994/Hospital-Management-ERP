"""SQLite backup helper with timestamped immutable-ish snapshots."""
from pathlib import Path
from datetime import datetime, timezone
import sqlite3, os

def backup_sqlite(source, destination_dir):
    source = Path(source); outdir = Path(destination_dir); outdir.mkdir(parents=True, exist_ok=True)
    if not source.exists(): raise FileNotFoundError(source)
    name = f"hospital_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.db"
    target = outdir / name
    src = sqlite3.connect(source); dst = sqlite3.connect(target)
    try: src.backup(dst)
    finally: dst.close(); src.close()
    os.chmod(target, 0o600)
    return target
