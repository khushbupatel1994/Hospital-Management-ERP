from datetime import datetime, timezone
from pathlib import Path
import sqlite3, os

def database_health(db_path):
    p = Path(db_path)

    result = {
        "present": p.exists(),
        "path": str(p),
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

    if not p.exists():
        result["ok"] = False
        return result

    con = None

    try:
        con = sqlite3.connect(p)
        con.execute("PRAGMA integrity_check").fetchone()
        result["ok"] = True

    except sqlite3.Error as e:
        result["ok"] = False
        result["error"] = str(e)

    finally:
        if con is not None:
            con.close()

    return result

def environment_health():
    return {"python": os.sys.version.split()[0], "pid": os.getpid(), "time": datetime.now(timezone.utc).isoformat()}
