"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : User CRUD
Version : 2.0
===========================================================
"""

from database.database import Database
from backend.security.security import Security


class UserCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_user_table()
        self.upgrade_user_table()

    # ==========================================
    # Create User Table
    # ==========================================

    def create_user_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id TEXT UNIQUE,

            full_name TEXT NOT NULL,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT,

            department TEXT,

            mobile TEXT,

            email TEXT,

            status TEXT DEFAULT 'Active',

            last_login TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Upgrade User Table
    # ==========================================

    def upgrade_user_table(self):

        self.cursor.execute(
            "PRAGMA table_info(users)"
        )

        columns = [
            column[1]
            for column in self.cursor.fetchall()
        ]

        if "security_question" not in columns:

            self.cursor.execute("""
                ALTER TABLE users
                ADD COLUMN security_question TEXT
            """)

            print("✅ Security Question Column Added")

        if "security_answer" not in columns:

            self.cursor.execute("""
                ALTER TABLE users
                ADD COLUMN security_answer TEXT
            """)

            print("✅ Security Answer Column Added")

        self.commit()

    # ==========================================
    # Check Duplicate User
    # ==========================================

    def check_duplicate(self, employee_id, username):

        self.cursor.execute("""
            SELECT id
            FROM users
            WHERE employee_id=? OR username=?
        """, (
            employee_id,
            username
        ))

        return self.cursor.fetchone()
    # ==========================================
    # Add User
    # ==========================================

    def add_user(
        self,
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
    ):

        try:

            # Password Hash
            hashed_password = Security.hash_password(
                password
            )

            self.cursor.execute("""
                INSERT INTO users
                (
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
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                employee_id,
                full_name,
                username,
                hashed_password,
                role,
                department,
                mobile,
                email,
                security_question,
                security_answer,
                status
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add User Error :", e)

            return False

    # ==========================================
    # Load All Users
    # ==========================================

    def load_users(self):

        self.cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                username,
                role,
                department,
                mobile,
                status
            FROM users
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Search User
    # ==========================================

    def search_user(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                username,
                role,
                department,
                mobile,
                status
            FROM users
            WHERE
                employee_id LIKE :keyword
                OR full_name LIKE :keyword
                OR username LIKE :keyword
                OR role LIKE :keyword
                OR department LIKE :keyword
                OR mobile LIKE :keyword
                OR email LIKE :keyword
                OR status LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Update User
    # ==========================================

    def update_user(
        self,
        user_id,
        employee_id,
        full_name,
        username,
        role,
        department,
        mobile,
        email,
        security_question,
        security_answer,
        status
    ):

        try:

            self.cursor.execute("""
                UPDATE users
                SET
                    employee_id = ?,
                    full_name = ?,
                    username = ?,
                    role = ?,
                    department = ?,
                    mobile = ?,
                    email = ?,
                    security_question = ?,
                    security_answer = ?,
                    status = ?
                WHERE id = ?
            """, (
                employee_id,
                full_name,
                username,
                role,
                department,
                mobile,
                email,
                security_question,
                security_answer,
                status,
                user_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update User Error:", e)

            return False

    # ==========================================
    # Delete User
    # ==========================================

    def delete_user(self, user_id):

        try:

            self.cursor.execute(
                "DELETE FROM users WHERE id=?",
                (user_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete User Error:", e)

            return False

    
