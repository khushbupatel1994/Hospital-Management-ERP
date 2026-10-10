import os
import sqlite3
from config.paths import DATABASE_DIR, APP_DATA_DIR

REQUIRED_TABLES = {
    "users", "patients", "doctors", "appointments", "billing",
    "laboratory", "inventory", "pharmacy"
}


def check():
    db = os.path.join(DATABASE_DIR, "hospital.db")
    result = {"app_data": os.path.isdir(APP_DATA_DIR), "database": False, "tables": False, "integrity": False}
    if not os.path.exists(db):
        return result
    try:
        conn = sqlite3.connect(db)
        result["database"] = True
        result["integrity"] = conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        result["tables"] = REQUIRED_TABLES.issubset(tables)
        conn.close()
    except Exception:
        pass
    return result
