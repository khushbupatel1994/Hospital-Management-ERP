"""SQLite database bootstrap used by the desktop client and local API.

The repository historically referenced ``database.database.Database`` from
many modules, but the package was missing from the uploaded repository.  This
module keeps the local/desktop storage contract intact and creates the shared
ERP schema on first use.  Production deployments should use the PostgreSQL
migration path documented under ``deploy/postgres``.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path


class Database:
    """Small connection wrapper with idempotent schema initialization."""

    def __init__(self) -> None:
        default_dir = Path(os.getenv("LOCALAPPDATA", Path.home())) / "Cloud Secure Hospital ERP" / "database"
        configured = os.getenv("HOSPITAL_DB")
        self.db_path = Path(configured) if configured else default_dir / "hospital.db"
        self.db_path = self.db_path.expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def connect(self) -> sqlite3.Connection:
        if self.conn is not None:
            return self.conn

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.initialize_database()
        return self.conn

    def initialize_database(self) -> None:
        if self.conn is None:
            return

        schema = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE,
            full_name TEXT NOT NULL DEFAULT '',
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL DEFAULT '',
            role TEXT NOT NULL DEFAULT 'Receptionist',
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
        );
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            login_time TEXT DEFAULT CURRENT_TIMESTAMP,
            logout_time TEXT,
            status TEXT
        );
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id TEXT UNIQUE,
            doctor_code TEXT UNIQUE,
            full_name TEXT,
            name TEXT,
            gender TEXT,
            department TEXT,
            specialization TEXT,
            qualification TEXT,
            experience INTEGER DEFAULT 0,
            mobile TEXT,
            phone TEXT,
            email TEXT,
            consultation_fee REAL DEFAULT 0,
            opd_timing TEXT,
            available_days TEXT,
            available_time TEXT,
            joining_date TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE,
            registration_no TEXT UNIQUE,
            patient_code TEXT UNIQUE,
            patient_name TEXT,
            name TEXT,
            gender TEXT,
            dob TEXT,
            age INTEGER,
            blood_group TEXT,
            mobile TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            pin_code TEXT,
            pincode TEXT,
            aadhaar TEXT,
            disease TEXT,
            emergency_contact TEXT,
            doctor TEXT,
            department TEXT,
            patient_type TEXT,
            assigned_doctor INTEGER,
            registration_date TEXT,
            registration_time TEXT,
            registration_day TEXT,
            father_husband_name TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id TEXT UNIQUE,
            patient_id INTEGER,
            doctor_id INTEGER,
            patient_name TEXT,
            doctor_name TEXT,
            department TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            visit_type TEXT,
            token_no TEXT,
            token_number INTEGER,
            purpose TEXT,
            disease TEXT,
            father_husband_name TEXT,
            status TEXT DEFAULT 'Pending',
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT UNIQUE,
            bill_no TEXT UNIQUE,
            patient TEXT,
            patient_name TEXT,
            doctor TEXT,
            doctor_name TEXT,
            bill_date TEXT,
            consultation_fee REAL DEFAULT 0,
            consultation REAL DEFAULT 0,
            medicine_charges REAL DEFAULT 0,
            medicine_charge REAL DEFAULT 0,
            lab_charges REAL DEFAULT 0,
            lab_charge REAL DEFAULT 0,
            room_charge REAL DEFAULT 0,
            other_charges REAL DEFAULT 0,
            other_charge REAL DEFAULT 0,
            discount REAL DEFAULT 0,
            tax REAL DEFAULT 0,
            gst REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            total REAL DEFAULT 0,
            payment_mode TEXT,
            payment_method TEXT,
            bill_status TEXT,
            payment_status TEXT,
            advance REAL DEFAULT 0,
            due REAL DEFAULT 0,
            remarks TEXT,
            created_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS pharmacy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_code TEXT UNIQUE,
            medicine_id TEXT UNIQUE,
            medicine_name TEXT,
            name TEXT,
            category TEXT,
            batch_number TEXT,
            supplier TEXT,
            quantity INTEGER DEFAULT 0,
            stock_quantity INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 10,
            price REAL DEFAULT 0,
            expiry_date TEXT,
            status TEXT DEFAULT 'Available',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id TEXT UNIQUE,
            medicine_code TEXT UNIQUE,
            name TEXT,
            medicine_name TEXT,
            category TEXT,
            stock_quantity INTEGER DEFAULT 0,
            quantity INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 10,
            price REAL DEFAULT 0,
            expiry_date TEXT,
            status TEXT DEFAULT 'Available',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS lab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT UNIQUE,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_id INTEGER,
            patient_name TEXT,
            test_name TEXT,
            result TEXT,
            remarks TEXT,
            report_date TEXT,
            test_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT UNIQUE,
            item_name TEXT,
            category TEXT,
            supplier TEXT,
            batch_no TEXT,
            purchase_price REAL DEFAULT 0,
            selling_price REAL DEFAULT 0,
            stock_quantity INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 0,
            unit TEXT,
            gst REAL DEFAULT 0,
            expiry_date TEXT,
            remarks TEXT,
            status TEXT DEFAULT 'Available',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            transaction_date TEXT,
            transaction_type TEXT,
            category TEXT,
            amount REAL DEFAULT 0,
            payment_mode TEXT,
            description TEXT,
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE,
            full_name TEXT,
            department TEXT,
            designation TEXT,
            mobile TEXT,
            email TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS opd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opd_id TEXT UNIQUE,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            department TEXT,
            visit_date TEXT,
            visit_time TEXT,
            chief_complaint TEXT,
            diagnosis TEXT,
            prescription TEXT,
            followup_date TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS ipd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_id TEXT UNIQUE,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            ward TEXT,
            bed_no TEXT,
            admission_date TEXT,
            discharge_date TEXT,
            diagnosis TEXT,
            treatment TEXT,
            daily_charges REAL DEFAULT 0,
            status TEXT DEFAULT 'Admitted',
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE,
            setting_value TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS backup_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_path TEXT,
            backup_time TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            created_by TEXT
        );
        """
        self.conn.executescript(schema)
        self.conn.commit()

    def commit(self) -> None:
        if self.conn is not None:
            self.conn.commit()

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None
