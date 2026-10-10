"""Cloud Secure Hospital ERP - Enterprise API gateway."""

import os
import sqlite3
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import bcrypt
import jwt

from fastapi import (
    FastAPI,
    HTTPException,
    Header,
    Depends,
    Response,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel, Field

from server.module_gateway import (
    MODULES,
    list_records,
    create_record,
    update_record,
    delete_record,
)

from enterprise.audit import record as audit_record
from enterprise_phase8.security import REVOCATIONS, new_jti
from enterprise_phase8.health import database_health, environment_health
from enterprise_phase8.metrics import METRICS
from enterprise_phase8.backup import backup_sqlite


# ============================================================
# CONFIGURATION
# ============================================================

BASE = Path(__file__).resolve().parents[1]

DB = Path(
    os.getenv(
        "HOSPITAL_DB",
        BASE / "database" / "hospital.db"
    )
)

API_KEY = os.getenv("ERP_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "ERP_API_KEY environment variable is required."
    )

JWT_SECRET = os.getenv("ERP_JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "ERP_JWT_SECRET environment variable is required."
    )

if len(JWT_SECRET) < 32:
    raise RuntimeError(
        "ERP_JWT_SECRET must be at least 32 characters."
    )

JWT_ALG = "HS256"

JWT_MINUTES = int(
    os.getenv("ERP_JWT_MINUTES", "30")
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Cloud Secure Hospital ERP API",
    version="7.0"
)

security = HTTPBearer(auto_error=False)

_failed = {}

# ============================================================
# RENDER DEMO DATABASE INITIALIZATION
# ============================================================

def initialize_demo_database():
    DB.parent.mkdir(parents=True, exist_ok=True)

    # Always create/open the exact database configured for this API.
    with sqlite3.connect(DB) as con:
        con.execute("PRAGMA foreign_keys = ON")

        # Users table is required for API login.
        con.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT,
                mobile TEXT,
                email TEXT,
                security_question TEXT,
                security_answer TEXT,
                status TEXT DEFAULT 'Active',
                last_login TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                failed_attempts INTEGER DEFAULT 0,
                account_locked INTEGER DEFAULT 0
            )
        """)

        existing = con.execute(
            "SELECT id FROM users WHERE username=? COLLATE NOCASE",
            ("admin",)
        ).fetchone()

        if not existing:
            password_hash = bcrypt.hashpw(
                b"admin123",
                bcrypt.gensalt()
            ).decode("utf-8")

            con.execute("""
                INSERT INTO users(
                    employee_id,
                    full_name,
                    username,
                    password,
                    role,
                    department,
                    mobile,
                    email,
                    security_question,
                    security_answer,
                    status
                )
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """, (
                "EMP001",
                "Administrator",
                "admin",
                password_hash,
                "Super Admin",
                "Administration",
                "9876543210",
                "admin@hospital.com",
                "What is your favourite color?",
                "Blue",
                "Active"
            ))

        con.commit()

    # Try to initialize the existing ERP tables too.
    try:
        import config.paths as app_paths
        app_paths.DATABASE_DIR = str(DB.parent)

        from database.database import Database
        db = Database()
        db.connect()
        db.close()

    except Exception as exc:
        print(f"⚠ ERP core-table initialization warning: {exc}")

    print(f"✅ Render demo database ready: {DB}")
    print("✅ Demo login: admin / admin123")

initialize_demo_database()


# ============================================================
# REQUEST MODELS
# ============================================================

class LoginRequest(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=100
    )

    password: str = Field(
        min_length=1,
        max_length=200
    )


class AIRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class RecordRequest(BaseModel):
    data: dict = Field(default_factory=dict)


class NotificationRead(BaseModel):
    last_event_id: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=100)


# ============================================================
# API KEY AUTHENTICATION
# ============================================================

def require_api_key(
    x_api_key: Optional[str] = Header(default=None)
):
    if (
        not API_KEY
        or API_KEY == "CHANGE-ME"
        or x_api_key != API_KEY
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized API client"
        )


# ============================================================
# JWT AUTHENTICATION
# ============================================================

def require_token(
    credentials: Optional[
        HTTPAuthorizationCredentials
    ] = Depends(security)
):
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Bearer token required"
        )

    try:
        claims = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALG]
        )

        if (
            claims.get("jti")
            and REVOCATIONS.is_revoked(
                claims["jti"]
            )
        ):
            raise HTTPException(
                status_code=401,
                detail="Session revoked"
            )

        return claims

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session"
        )


# ============================================================
# ROLE AUTHENTICATION
# ============================================================

def require_roles(*roles):

    def checker(
        claims=Depends(require_token)
    ):
        if claims.get("role") not in roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permission"
            )

        return claims

    return checker


# ============================================================
# DATABASE HELPERS
# ============================================================

def query_count(
    table: str,
    where: str = "",
    params=()
) -> int:

    allowed = {
        "patients",
        "doctors",
        "appointments",
        "lab_tests",
        "pharmacy",
        "inventory",
        "ipd",
        "opd",
    }

    if table not in allowed:
        raise ValueError("Invalid table")

    if not DB.exists():
        return 0

    with sqlite3.connect(DB) as con:
        row = con.execute(
            f"SELECT COUNT(*) FROM {table} {where}",
            params
        ).fetchone()

        return int(row[0] or 0)


def query_sum(
    table: str,
    column: str
) -> float:

    allowed = {
        "billing": {"total_amount"},
    }

    if table not in allowed or column not in allowed[table]:
        raise ValueError("Invalid sum target")

    if not DB.exists():
        return 0.0

    with sqlite3.connect(DB) as con:

        row = con.execute(
            f"SELECT COALESCE(SUM({column}), 0) FROM {table}"
        ).fetchone()

        return float(row[0] or 0)


def find_user(username: str):

    if not DB.exists():
        return None

    with sqlite3.connect(DB) as con:

        con.row_factory = sqlite3.Row

        return con.execute(
            """
            SELECT
                id,
                full_name,
                username,
                password,
                role,
                department,
                status,
                account_locked
            FROM users
            WHERE username=?
            COLLATE NOCASE
            LIMIT 1
            """,
            (username.strip(),)
        ).fetchone()


def safe_user(row):

    return {
        "id": row["id"],
        "name": row["full_name"],
        "username": row["username"],
        "role": row["role"],
        "department": row["department"],
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "hospital-erp-api",
        "version": "7.0",
        "database": DB.exists(),
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ============================================================
# LOGIN
# ============================================================

@app.post(
    "/api/v1/auth/login",
    response_model=LoginResponse,
    dependencies=[Depends(require_api_key)]
)
def login(req: LoginRequest):

    now = time.time()

    key = req.username.lower()

    attempts = [
        t
        for t in _failed.get(key, [])
        if now - t < 900
    ]

    if len(attempts) >= 5:

        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again later."
        )

    row = find_user(req.username)

    valid = bool(
        row
        and row["status"] == "Active"
        and not row["account_locked"]
        and bcrypt.checkpw(
            req.password.encode(),
            row["password"].encode()
        )
    )

    if not valid:

        attempts.append(now)

        _failed[key] = attempts

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    _failed.pop(key, None)

    if JWT_SECRET.startswith("CHANGE-ME"):

        raise HTTPException(
            status_code=500,
            detail="Server JWT secret is not configured"
        )

    now_dt = datetime.now(timezone.utc)

    exp = now_dt + timedelta(
        minutes=JWT_MINUTES
    )

    token = jwt.encode(
        {
            "sub": str(row["id"]),
            "username": row["username"],
            "role": row["role"],
            "jti": new_jti(),
            "iat": now_dt,
            "exp": exp,
        },
        JWT_SECRET,
        algorithm=JWT_ALG,
    )

    return LoginResponse(
        access_token=token,
        expires_in=JWT_MINUTES * 60,
        user=safe_user(row)
    )


# ============================================================
# CURRENT USER
# ============================================================

@app.get("/api/v1/me")
def me(
    claims=Depends(require_token)
):

    return {
        "user_id": claims.get("sub"),
        "username": claims.get("username"),
        "role": claims.get("role"),
    }


# ============================================================
# SUMMARY
# ============================================================

@app.get("/api/v1/summary")
def summary(
    claims=Depends(require_token)
):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return {
        "patients": query_count("patients"),

        "doctors": query_count("doctors"),

        "appointments": query_count(
            "appointments"
        ),

        "today_appointments": query_count(
            "appointments",
            "WHERE appointment_date LIKE ?",
            (today + "%",)
        ),

        "pending_lab_tests": query_count(
            "lab_tests",
            "WHERE LOWER(COALESCE(status,''))='pending'"
        ),

        "active_ipd": query_count(
            "ipd",
            "WHERE LOWER(COALESCE(status,'')) IN ('active','admitted')"
        ),

        "low_medicines": query_count(
            "pharmacy", "WHERE COALESCE(quantity,0) <= COALESCE(minimum_stock,0)"
        ),

        "low_inventory": query_count(
            "inventory",
            "WHERE COALESCE(stock_quantity,0) <= COALESCE(minimum_stock,0)"
        ),

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ============================================================
# ADMIN SECURITY
# ============================================================

@app.get("/api/v1/admin/security")
def security_summary(
    claims=Depends(
        require_roles(
            "Super Admin",
            "Admin"
        )
    )
):

    return {
        "failed_login_window": 900,
        "max_attempts": 5,
        "jwt_minutes": JWT_MINUTES,
        "database_present": DB.exists(),
    }


# ============================================================
# AI ASSISTANT
# ============================================================

@app.post("/api/v1/ai/assistant")
def ai_assistant(
    req: AIRequest,
    claims=Depends(require_token)
):

    q = req.question.lower()

    if "patient" in q:

        answer = (
            f"There are currently "
            f"{query_count('patients')} "
            f"patient records."
        )

    elif "doctor" in q:

        answer = (
            f"There are currently "
            f"{query_count('doctors')} "
            f"doctor records."
        )

    elif "appointment" in q:

        answer = (
            f"There are currently "
            f"{query_count('appointments')} "
            f"appointment records."
        )

    elif "lab" in q:

        pending_lab_where = (
            "WHERE LOWER(COALESCE(status,''))='pending'"
        )

        answer = (
            f"There are currently "
            f"{query_count('lab_tests', pending_lab_where)} "
            f"pending lab tests."
        )

    elif "medicine" in q or "stock" in q:

        answer = (
            f"There are "
            f"{query_count('pharmacy', 'WHERE COALESCE(quantity,0) <= COALESCE(minimum_stock,0)')} "
            f"medicines at or below minimum stock."
        )

    else:

        answer = (
            "I can currently answer approved "
            "hospital summary questions."
        )

    return {
        "answer": answer,
        "safe_mode": True,
        "role": claims.get("role"),
    }


# ============================================================
# MODULES
# ============================================================

@app.get("/api/v1/modules")
def modules(
    claims=Depends(require_token)
):

    role = claims.get("role")

    return {
        "modules": {
            name: {
                "read": role in cfg["read_roles"],
                "write": role in cfg["write_roles"],
            }
            for name, cfg in MODULES.items()
        }
    }


@app.get("/api/v1/modules/{module}/records")
def module_records(
    module: str,
    limit: int = 50,
    offset: int = 0,
    search: str = "",
    claims=Depends(require_token)
):

    if module not in MODULES:

        raise HTTPException(
            status_code=404,
            detail="Unknown module"
        )

    try:

        result = list_records(
            DB,
            module,
            claims.get("role"),
            limit,
            offset,
            search,
        )

        audit_record(
            "module.read",
            claims.get("username"),
            claims.get("role"),
            True,
            {
                "module": module,
                "count": len(result["items"]),
            },
        )

        return result

    except PermissionError as e:

        audit_record(
            "module.read.denied",
            claims.get("username"),
            claims.get("role"),
            False,
            {"module": module},
        )

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


@app.post("/api/v1/modules/{module}/records")
def module_create(
    module: str,
    req: RecordRequest,
    claims=Depends(require_token)
):

    if module not in MODULES:

        raise HTTPException(
            status_code=404,
            detail="Unknown module"
        )

    try:

        rid = create_record(
            DB,
            module,
            claims.get("role"),
            req.data
        )

        audit_record(
            "module.create",
            claims.get("username"),
            claims.get("role"),
            True,
            {
                "module": module,
                "record_id": rid,
            },
        )

        return {
            "ok": True,
            "id": rid
        }

    except PermissionError as e:

        audit_record(
            "module.create.denied",
            claims.get("username"),
            claims.get("role"),
            False,
            {"module": module},
        )

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    except (ValueError, sqlite3.Error) as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.put("/api/v1/modules/{module}/records/{record_id}")
def module_update(
    module: str,
    record_id: int,
    req: RecordRequest,
    claims=Depends(require_token)
):

    if module not in MODULES:

        raise HTTPException(
            status_code=404,
            detail="Unknown module"
        )

    try:

        ok = update_record(
            DB,
            module,
            claims.get("role"),
            record_id,
            req.data
        )

        audit_record(
            "module.update",
            claims.get("username"),
            claims.get("role"),
            ok,
            {
                "module": module,
                "record_id": record_id,
            },
        )

        return {
            "ok": ok
        }

    except PermissionError as e:

        audit_record(
            "module.update.denied",
            claims.get("username"),
            claims.get("role"),
            False,
            {
                "module": module,
                "record_id": record_id,
            },
        )

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    except (ValueError, sqlite3.Error) as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.delete("/api/v1/modules/{module}/records/{record_id}")
def module_delete(
    module: str,
    record_id: int,
    claims=Depends(require_token)
):

    if module not in MODULES:

        raise HTTPException(
            status_code=404,
            detail="Unknown module"
        )

    try:

        ok = delete_record(
            DB,
            module,
            claims.get("role"),
            record_id
        )

        audit_record(
            "module.delete",
            claims.get("username"),
            claims.get("role"),
            ok,
            {
                "module": module,
                "record_id": record_id,
            },
        )

        return {
            "ok": ok
        }

    except PermissionError as e:

        audit_record(
            "module.delete.denied",
            claims.get("username"),
            claims.get("role"),
            False,
            {
                "module": module,
                "record_id": record_id,
            },
        )

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    except sqlite3.Error as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ============================================================
# ENTERPRISE DASHBOARD
# ============================================================

@app.get("/api/v1/dashboard/enterprise")
def enterprise_dashboard(
    claims=Depends(require_token)
):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return {
        "patients": query_count("patients"),

        "doctors": query_count("doctors"),

        "appointments": query_count("appointments"),

        "appointments_today": query_count(
            "appointments",
            "WHERE appointment_date LIKE ?",
            (today + "%",)
        ),

        "appointments_pending": query_count(
            "appointments",
            "WHERE LOWER(COALESCE(status,''))='pending'"
        ),

        "lab_pending": query_count(
            "lab_tests",
            "WHERE LOWER(COALESCE(status,''))='pending'"
        ),

        "low_medicines": query_count(
            "pharmacy", "WHERE COALESCE(quantity,0) <= COALESCE(minimum_stock,0)"
        ),

        "low_inventory": query_count(
            "inventory",
            "WHERE COALESCE(stock_quantity,0) <= COALESCE(minimum_stock,0)"
        ),

        "opd": query_count("opd"),

        "active_ipd": query_count(
            "ipd",
            "WHERE LOWER(COALESCE(status,'')) IN ('active','admitted')"
        ),

        "revenue": query_sum(
            "billing",
            "total_amount"
        ),

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ============================================================
# REALTIME
# ============================================================

from server.realtime import (
    publish as publish_event,
    since as events_since
)


@app.get("/api/v1/notifications")
def notifications(
    last_event_id: int = 0,
    limit: int = 50,
    claims=Depends(require_token)
):

    limit = max(
        1,
        min(limit, 100)
    )

    return {
        "events": events_since(
            last_event_id,
            limit
        ),
        "server_time": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ============================================================
# ENTERPRISE HEALTH
# ============================================================

@app.get("/api/v1/enterprise/health")
def enterprise_health(
    claims=Depends(require_token)
):

    if claims.get("role") not in {
        "Super Admin",
        "Admin"
    }:

        raise HTTPException(
            status_code=403,
            detail="Admin permission required"
        )

    return {
        "api": "ok",
        "database": DB.exists(),
        "database_path": str(DB),
        "server_time": datetime.now(
            timezone.utc
        ).isoformat(),
        "version": "7.0",
    }


@app.post("/api/v1/session/logout")
def logout(
    claims=Depends(require_token)
):

    if claims.get("jti") and claims.get("exp"):

        REVOCATIONS.revoke(
            claims["jti"],
            int(claims["exp"])
        )

    audit_record(
        "session.logout",
        claims.get("username"),
        claims.get("role"),
        True,
        {}
    )

    return {
        "ok": True
    }


@app.get("/api/v1/notifications/bootstrap")
def bootstrap_notifications(
    claims=Depends(require_token)
):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    alerts = []

    pending = query_count(
        "appointments",
        "WHERE LOWER(COALESCE(status,''))='pending'"
    )

    lab = query_count(
        "lab_tests",
        "WHERE LOWER(COALESCE(status,''))='pending'"
    )

    meds = query_count(
        "pharmacy", "WHERE COALESCE(quantity,0) <= COALESCE(minimum_stock,0)"
    )

    if pending:

        alerts.append({
            "type": "appointment",
            "severity": "info",
            "title": "Pending appointments",
            "message": f"{pending} appointments are pending.",
        })

    if lab:

        alerts.append({
            "type": "laboratory",
            "severity": "warning",
            "title": "Pending lab tests",
            "message": f"{lab} lab tests are pending.",
        })

    if meds:

        alerts.append({
            "type": "pharmacy",
            "severity": "warning",
            "title": "Low medicine stock",
            "message": f"{meds} medicines are at or below minimum stock.",
        })

    return {
        "date": today,
        "alerts": alerts,
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ============================================================
# PHASE 8
# ============================================================

@app.get("/api/v1/enterprise/health/deep")
def deep_health(
    claims=Depends(
        require_roles(
            "Super Admin",
            "Admin"
        )
    )
):

    return {
        "database": database_health(DB),
        "environment": environment_health(),
        "metrics": METRICS.snapshot(),
    }


@app.post("/api/v1/admin/backup")
def create_backup(
    claims=Depends(
        require_roles("Super Admin")
    )
):

    target = backup_sqlite(
        DB,
        os.getenv(
            "ERP_BACKUP_DIR",
            str(BASE / "backups")
        )
    )

    audit_record(
        "database.backup",
        claims.get("username"),
        claims.get("role"),
        True,
        {
            "file": target.name
        },
    )

    return {
        "ok": True,
        "backup": target.name
    }


# ============================================================
# METRICS
# ============================================================

@app.get("/metrics")
def prometheus_metrics():

    snap = METRICS.snapshot()

    lines = [
        "# HELP hospital_erp_requests_total Total tracked application requests",
        "# TYPE hospital_erp_requests_total counter",
    ]

    lines.append(
        f"hospital_erp_requests_total "
        f"{snap.get('requests', 0)}"
    )

    lines += [
        "# HELP hospital_erp_errors_total Total tracked application errors",
        "# TYPE hospital_erp_errors_total counter",
    ]

    lines.append(
        f"hospital_erp_errors_total "
        f"{snap.get('errors', 0)}"
    )

    return Response(
        content="\n".join(lines) + "\n",
        media_type="text/plain; version=0.0.4"
    )
