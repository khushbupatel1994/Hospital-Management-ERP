"""Phase 6 server-first module gateway.
Only approved tables/fields are exposed through the API.
"""
import sqlite3
from datetime import datetime, timezone
from typing import Any

MODULES = {
    "patients": {
        "table": "patients",
        "read_roles": {"Super Admin", "Admin", "Doctor", "Nurse", "Receptionist"},
        "write_roles": {"Super Admin", "Admin", "Doctor", "Receptionist"},
        "fields": ["id", "patient_id", "registration_no", "patient_name", "name", "gender", "dob", "age", "blood_group", "mobile", "email", "address", "city", "state", "pin_code", "aadhaar", "disease", "doctor", "department", "patient_type", "assigned_doctor", "registration_date", "status", "father_husband_name", "created_at"],
    },
    "doctors": {
        "table": "doctors",
        "read_roles": {"Super Admin", "Admin", "Doctor", "Nurse", "Receptionist"},
        "write_roles": {"Super Admin", "Admin"},
        "fields": ["id", "doctor_id", "doctor_code", "full_name", "name", "gender", "department", "specialization", "qualification", "experience", "mobile", "phone", "email", "consultation_fee", "opd_timing", "available_days", "available_time", "joining_date", "status", "created_at"],
    },
    "appointments": {
        "table": "appointments",
        "read_roles": {"Super Admin", "Admin", "Doctor", "Nurse", "Receptionist"},
        "write_roles": {"Super Admin", "Admin", "Doctor", "Receptionist"},
        "fields": ["id", "appointment_id", "patient_id", "doctor_id", "patient_name", "doctor_name", "department", "appointment_date", "appointment_time", "visit_type", "token_no", "token_number", "purpose", "status", "remarks", "created_at"],
    },
    "laboratory": {
        "table": "lab_tests",
        "read_roles": {"Super Admin", "Admin", "Doctor", "Nurse", "Laboratory"},
        "write_roles": {"Super Admin", "Admin", "Laboratory"},
        "fields": ["id", "test_id", "patient_id", "patient_name", "test_name", "status", "result", "test_date", "created_at"],
    },
    "pharmacy": {
        "table": "medicines",
        "read_roles": {"Super Admin", "Admin", "Doctor", "Pharmacist"},
        "write_roles": {"Super Admin", "Admin", "Pharmacist"},
        "fields": ["id", "medicine_id", "name", "category", "stock_quantity", "minimum_stock", "expiry_date", "price", "status", "created_at"],
    },
    "inventory": {
        "table": "inventory",
        "read_roles": {"Super Admin", "Admin", "Pharmacist", "Store"},
        "write_roles": {"Super Admin", "Admin", "Store"},
        "fields": ["id", "item_id", "item_name", "category", "stock_quantity", "minimum_stock", "expiry_date", "status", "created_at"],
    },
    "billing": {
        "table": "billing",
        "read_roles": {"Super Admin", "Admin", "Accounts", "Receptionist"},
        "write_roles": {"Super Admin", "Admin", "Accounts"},
        "fields": ["id", "bill_id", "bill_no", "patient", "patient_name", "doctor", "doctor_name", "bill_date", "consultation_fee", "medicine_charges", "lab_charges", "total_amount", "paid_amount", "payment_status", "created_at"],
    },
}


def _table_name(con, module):
    """Return the configured table, with a compatibility fallback."""
    configured = MODULES[module]["table"]
    tables = {
        row[0]
        for row in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if configured in tables:
        return configured
    if module == "pharmacy" and "pharmacy" in tables:
        return "pharmacy"
    return configured


def _available_fields(con, module, table):
    columns = {
        row[1]
        for row in con.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    }
    return [field for field in MODULES[module]["fields"] if field in columns]


def list_records(db_path, module, role, limit=50, offset=0, search=""):
    cfg = MODULES[module]
    if role not in cfg["read_roles"]:
        raise PermissionError("Read permission denied")
    limit = max(1, min(int(limit), 100))
    offset = max(0, int(offset))
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        table = _table_name(con, module)
        fields = _available_fields(con, module, table)
        if not fields:
            raise ValueError(f"No approved fields are available for module: {module}")
        params = []
        where = ""
        if search:
            candidates = [f for f in fields if f not in {"id", "created_at"}]
            if candidates:
                clauses = [f"CAST({f} AS TEXT) LIKE ?" for f in candidates]
                where = "WHERE " + " OR ".join(clauses)
                params.extend([f"%{search}%"] * len(clauses))
        total = con.execute(f"SELECT COUNT(*) FROM {table} {where}", params).fetchone()[0]
        order_by = "id DESC" if "id" in fields else "rowid DESC"
        rows = con.execute(
            f"SELECT {', '.join(fields)} FROM {table} {where} "
            f"ORDER BY {order_by} LIMIT ? OFFSET ?",
            params + [limit, offset],
        ).fetchall()
    return {"module": module, "items": [dict(r) for r in rows], "total": int(total), "limit": limit, "offset": offset}


def create_record(db_path, module, role, payload: dict[str, Any]):
    cfg = MODULES[module]

    if role not in cfg["write_roles"]:
        raise PermissionError("Write permission denied")

    with sqlite3.connect(db_path) as con:
        table = _table_name(con, module)
        available = set(_available_fields(con, module, table))
        allowed = available - {"id", "created_at"}
        clean = {k: v for k, v in payload.items() if k in allowed}
        if not clean:
            raise ValueError("No approved fields supplied")

        # -------------------------------------------------
        # Patient IDs are generated centrally by the server.
        # BEGIN IMMEDIATE serializes writers so two clients
        # cannot receive the same next ID.
        # -------------------------------------------------

        if module == "patients" and {"patient_id", "registration_no"}.issubset(available):

            con.execute("BEGIN IMMEDIATE")

            # -----------------------------
            # Generate next Patient ID
            # -----------------------------

            patient_rows = con.execute(
                "SELECT patient_id FROM patients "
                "WHERE patient_id LIKE 'PT%'"
            ).fetchall()

            max_patient_number = 0

            for row in patient_rows:

                value = str(row[0] or "").strip().upper()

                if value.startswith("PT"):

                    try:
                        number = int(value[2:])

                        if number > max_patient_number:
                            max_patient_number = number

                    except (TypeError, ValueError):
                        pass

            next_patient_number = max_patient_number + 1

            while True:

                generated_patient_id = (
                    f"PT{next_patient_number:06d}"
                )

                exists = con.execute(
                    "SELECT 1 FROM patients "
                    "WHERE patient_id=? LIMIT 1",
                    (generated_patient_id,)
                ).fetchone()

                if not exists:
                    break

                next_patient_number += 1

            # -----------------------------
            # Generate next Registration No
            # -----------------------------

            year = datetime.now().strftime("%Y")

            registration_rows = con.execute(
                "SELECT registration_no FROM patients"
            ).fetchall()

            max_registration_number = 0

            for row in registration_rows:

                value = str(row[0] or "").strip().upper()

                if value.startswith("REG"):

                    try:
                        number = int(value[-6:])

                        if number > max_registration_number:
                            max_registration_number = number

                    except (TypeError, ValueError):
                        pass

            next_registration_number = (
                max_registration_number + 1
            )

            while True:

                generated_registration_no = (
                    f"REG{year}{next_registration_number:06d}"
                )

                exists = con.execute(
                    "SELECT 1 FROM patients "
                    "WHERE registration_no=? LIMIT 1",
                    (generated_registration_no,)
                ).fetchone()

                if not exists:
                    break

                next_registration_number += 1

            clean["patient_id"] = generated_patient_id
            clean["registration_no"] = generated_registration_no

        cols = list(clean)

        marks = ", ".join(
            "?" for _ in cols
        )

        cur = con.execute(
            f"INSERT INTO {table} "
            f"({', '.join(cols)}) "
            f"VALUES ({marks})",
            [clean[c] for c in cols]
        )

        con.commit()

        return int(cur.lastrowid)


def update_record(db_path, module, role, record_id: int, payload: dict[str, Any]):
    cfg = MODULES[module]
    if role not in cfg["write_roles"]:
        raise PermissionError("Write permission denied")
    with sqlite3.connect(db_path) as con:
        table = _table_name(con, module)
        allowed = set(_available_fields(con, module, table)) - {"id", "created_at"}
        clean = {k: v for k, v in payload.items() if k in allowed}
        if not clean:
            raise ValueError("No approved fields supplied")
        sets = ", ".join(f"{c}=?" for c in clean)
        cur = con.execute(f"UPDATE {table} SET {sets} WHERE id=?", [clean[c] for c in clean] + [record_id])
        con.commit()
        return cur.rowcount == 1


def delete_record(db_path, module, role, record_id: int):
    cfg = MODULES[module]
    if role not in cfg["write_roles"]:
        raise PermissionError("Delete permission denied")
    # Hard delete is deliberately limited to administrative records. Clinical records should be deactivated.
    if module in {"patients", "doctors", "laboratory", "billing"}:
        raise PermissionError("Hard delete is disabled for protected clinical/financial records")
    with sqlite3.connect(db_path) as con:
        table = _table_name(con, module)
        cur = con.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        con.commit()
        return cur.rowcount == 1
