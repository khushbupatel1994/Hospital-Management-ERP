"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Login CRUD
Version : 3.0
===========================================================
"""

from datetime import datetime

from database.database import Database
from backend.security.security import Security


class LoginCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_users_table()

        self.upgrade_users_table()

        self.create_login_history_table()

        self.create_default_admin()
        self.login_history_id = None

    # =====================================================
    # Create Users Table
    # =====================================================

    def create_users_table(self):

        self.cursor.execute("""
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

        self.commit()

    # =====================================================
    # Upgrade Users Table
    # =====================================================

    def upgrade_users_table(self):

        self.cursor.execute(
            "PRAGMA table_info(users)"
        )

        columns = [
            column[1]
            for column in self.cursor.fetchall()
        ]

        if "failed_attempts" not in columns:

            self.cursor.execute(
                """
                ALTER TABLE users
                ADD COLUMN failed_attempts
                INTEGER DEFAULT 0
                """
            )

        if "account_locked" not in columns:

            self.cursor.execute(
                """
                ALTER TABLE users
                ADD COLUMN account_locked
                INTEGER DEFAULT 0
                """
            )

        self.commit()

    # =====================================================
    # Create Login History Table
    # =====================================================

    def create_login_history_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            role TEXT,

            login_time TEXT,

            logout_time TEXT,

            status TEXT,

            ip_address TEXT

        )
        """)

        self.commit()

    # =====================================================
    # Default Admin
    # =====================================================

    def create_default_admin(self):

        self.cursor.execute(
            "SELECT id FROM users WHERE username=?",
            ("admin",)
        )

        if self.cursor.fetchone():
            return

        password = Security.hash_password("admin123")

        self.cursor.execute("""
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
        """,
        (

            "EMP001",

            "Administrator",

            "admin",

            password,

            "Super Admin",

            "Administration",

            "9876543210",

            "admin@hospital.com",

            "What is your favourite color?",

            "Blue",

            "Active"

        ))

        self.commit()

        print("✅ Default Admin Created")

    # =====================================================
    # Login
    # =====================================================

    def login(self, username, password):

        self.cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = self.cursor.fetchone()

        if user is None:

            return None

        # -----------------------------
        # Account Locked
        # -----------------------------

        if user[15] == 1:

            print("❌ Account Locked")

            return "LOCKED"

        # -----------------------------
        # Password Verify
        # -----------------------------

        if Security.verify_password(
            password,
            user[4]
        ):

            self.cursor.execute(
                """
                UPDATE users
                SET
                    last_login=?,
                    failed_attempts=0
                WHERE id=?
                """,
                (
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),
                    user[0]
                )
            )

            self.commit()

            self.login_history_id = self.log_login_history(
                user,
                "Success"
            )

            return user

        # -----------------------------
        # Wrong Password
        # -----------------------------

        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts =
                failed_attempts + 1
            WHERE id=?
            """,
            (
                user[0],
            )
        )

        self.commit()

        self.cursor.execute(
            """
            SELECT failed_attempts
            FROM users
            WHERE id=?
            """,
            (
                user[0],
            )
        )

        attempts = self.cursor.fetchone()[0]

        if attempts >= 5:

            self.cursor.execute(
                """
                UPDATE users
                SET account_locked=1
                WHERE id=?
                """,
                (
                    user[0],
                )
            )

            self.commit()

            print("🔒 Account Locked")

        self.log_login_history(
            user,
            "Failed"
        )

        return None

    # =====================================================
    # Login History
    # =====================================================

    def log_login_history(
        self,
        user,
        status="Success"
    ):

        self.cursor.execute(
            """
            INSERT INTO login_history(

                username,

                role,

                login_time,

                logout_time,

                status,

                ip_address

            )
            VALUES(?,?,?,?,?,?)
            """,
            (

                user[3],

                user[5],

                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                "",

                status,

                "127.0.0.1"

            )
        )

        self.commit()

        history_id = self.cursor.lastrowid
        print("✅ Login History Saved")
        return history_id

    # =====================================================
    # Logout
    # =====================================================

    def logout(self, history_id=None, username=None):
        """Mark the active successful login session as logged out."""
        try:
            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            if history_id:
                self.cursor.execute(
                    """UPDATE login_history
                       SET logout_time=?, status='Success'
                       WHERE id=? AND (logout_time IS NULL OR logout_time='')""",
                    (now, history_id)
                )
            elif username:
                self.cursor.execute(
                    """UPDATE login_history
                       SET logout_time=?, status='Success'
                       WHERE id=(SELECT id FROM login_history
                                 WHERE username=? AND status='Success'
                                   AND (logout_time IS NULL OR logout_time='')
                                 ORDER BY id DESC LIMIT 1)""",
                    (now, username)
                )
            self.commit()
            return True
        except Exception as e:
            print("Logout History Error:", e)
            return False

    # =====================================================
    # Forgot User ID
    # =====================================================

    def forgot_user_id(
        self,
        mobile,
        email
    ):

        self.cursor.execute(
            """
            SELECT username
            FROM users
            WHERE
                mobile=?
                AND email=?
            """,
            (
                mobile,
                email
            )
        )

        return self.cursor.fetchone()

    # =====================================================
    # Verify Security Question
    # =====================================================

    def verify_security(
        self,
        username,
        question,
        answer
    ):

        self.cursor.execute(
            """
            SELECT id
            FROM users
            WHERE
                username=?
                AND security_question=?
                AND security_answer=?
            """,
            (
                username,
                question,
                answer
            )
        )

        return self.cursor.fetchone()

    # =====================================================
    # Update Password
    # =====================================================

    def update_password(
        self,
        username,
        new_password
    ):

        new_password = Security.hash_password(
            new_password
        )

        self.cursor.execute(
            """
            UPDATE users
            SET password=?
            WHERE username=?
            """,
            (
                new_password,
                username
            )
        )

        self.commit()

        print("✅ Password Updated")

        return True

    # =====================================================
    # Unlock User Account
    # =====================================================

    def unlock_account(
        self,
        username
    ):

        self.cursor.execute(
            """
            UPDATE users
            SET
                failed_attempts=0,
                account_locked=0
            WHERE username=?
            """,
            (
                username,
            )
        )

        self.commit()

        print("✅ Account Unlocked")

        return True

    # =====================================================
    # Reset Failed Attempts
    # =====================================================

    def reset_failed_attempts(
        self,
        username
    ):

        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts=0
            WHERE username=?
            """,
            (
                username,
            )
        )

        self.commit()

        return True

    # =====================================================
    # Get User Details
    # =====================================================

    def get_user(
        self,
        username
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (
                username,
            )
        )

        return self.cursor.fetchone()

    # =====================================================
    # Get Login History
    # =====================================================

    def get_login_history(self):

        self.cursor.execute(
            """
            SELECT
                username,
                role,
                login_time,
                logout_time,
                status,
                ip_address
            FROM login_history
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    # =====================================================
    # Get All Users
    # =====================================================

    def get_all_users(self):

        self.cursor.execute(
            """
            SELECT
                id,
                employee_id,
                full_name,
                username,
                role,
                department,
                mobile,
                email,
                status,
                account_locked
            FROM users
            ORDER BY full_name
            """
        )

        return self.cursor.fetchall()

    # =====================================================
    # Close Database
    # =====================================================

    def close_connection(self):

        self.close()
    