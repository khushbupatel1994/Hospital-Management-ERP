"""Conservative SQLite -> PostgreSQL data migration helper.
Review generated schema/data in a staging environment before production use.
"""
import os, re, sqlite3
from pathlib import Path
import psycopg

SQLITE = Path(os.getenv("SQLITE_DB", "database/hospital.db"))
PG = os.environ["POSTGRES_DSN"]

def pg_type(sql_type: str) -> str:
    t = (sql_type or "").upper()
    if "INT" in t: return "BIGINT"
    if any(x in t for x in ("REAL", "FLOA", "DOUB")): return "DOUBLE PRECISION"
    if any(x in t for x in ("BLOB",)): return "BYTEA"
    if "BOOL" in t: return "BOOLEAN"
    if "DATE" in t or "TIME" in t: return "TIMESTAMPTZ" if "TIME" in t else "DATE"
    return "TEXT"

def qident(s: str) -> str:
    return '"' + s.replace('"', '""') + '"'

with sqlite3.connect(SQLITE) as src, psycopg.connect(PG) as dst:
    tables = [r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    with dst.cursor() as cur:
        for table in tables:
            cols = src.execute(f"PRAGMA table_info({qident(table)})").fetchall()
            defs = []
            for _, name, typ, notnull, default, pk in cols:
                d = f"{qident(name)} {pg_type(typ)}"
                if pk and len([c for c in cols if c[5]]) == 1: d += " PRIMARY KEY"
                if notnull and not pk: d += " NOT NULL"
                defs.append(d)
            cur.execute(f"CREATE TABLE IF NOT EXISTS {qident(table)} ({', '.join(defs)})")
            rows = src.execute(f"SELECT * FROM {qident(table)}").fetchall()
            if not rows: continue
            placeholders = ",".join(["%s"] * len(cols))
            names = ",".join(qident(c[1]) for c in cols)
            cur.executemany(f"INSERT INTO {qident(table)} ({names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING", rows)
    dst.commit()
print(f"Migrated {len(tables)} tables from {SQLITE} to PostgreSQL")
