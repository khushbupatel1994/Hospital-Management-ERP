"""Local readiness checks for demo and pre-production validation."""
import os
import sqlite3
from config.paths import DATABASE_DIR


class SystemHealth:
    REQUIRED_TABLES = {"users", "patients", "doctors", "appointments", "billing"}

    def check(self):
        db = os.path.join(DATABASE_DIR, "hospital.db")
        result = {"database": False, "tables": False, "api_configured": False, "issues": []}
        try:
            conn = sqlite3.connect(db)
            result["database"] = True
            rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            tables = {r[0] for r in rows}
            missing = sorted(self.REQUIRED_TABLES - tables)
            result["tables"] = not missing
            if missing: result["issues"].append("Missing tables: " + ", ".join(missing))
            conn.close()
        except Exception as e:
            result["issues"].append(f"Database check failed: {e}")
        if os.getenv("OPENAI_API_KEY") and os.getenv("HOSPITAL_AI_MODEL"):
            result["api_configured"] = True
        else:
            result["issues"].append("Live AI is not configured; offline AI mode is active.")
        return result
