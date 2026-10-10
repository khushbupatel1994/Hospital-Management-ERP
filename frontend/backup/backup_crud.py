"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Backup CRUD
Version : 4.0
===========================================================
"""

from database.database import Database
from datetime import datetime
import os


class BackupCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_backup_history_table()
        self.add_action_column()

    # ==========================================
    # Check Database Connection
    # ==========================================

    def check_database(self):

        try:

            self.cursor.execute(
                "SELECT 1"
            )

            return True

        except Exception:

            return False

    # ==========================================
    # Get Database Path
    # ==========================================

    def get_database_path(self):

        return self.db_path

    # ==========================================
    # Create Backup History Table
    # ==========================================

    def create_backup_history_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            backup_file TEXT NOT NULL,

            backup_path TEXT NOT NULL,

            backup_date TEXT NOT NULL,

            backup_size INTEGER DEFAULT 0,

            action TEXT DEFAULT 'BACKUP',

            backup_type TEXT DEFAULT 'Offline',

            status TEXT DEFAULT 'Success',

            created_by TEXT,

            remarks TEXT

        )
        """)

        self.commit()

    # ==========================================
    # Add Missing Action Column
    # ==========================================

    def add_action_column(self):

        try:

            self.cursor.execute(
                "ALTER TABLE backup_history ADD COLUMN action TEXT DEFAULT 'BACKUP'"
            )

            self.commit()

        except Exception:
            pass

    # ==========================================
    # Save Backup History
    # ==========================================

    def add_backup_history(
        self,
        backup_file,
        backup_path,
        backup_size,
        backup_type="Offline",
        status="Success",
        created_by="System",
        remarks=""
    ):

        try:

            self.cursor.execute("""
            INSERT INTO backup_history(
                backup_file,
                backup_path,
                backup_date,
                backup_size,
                backup_type,
                status,
                created_by,
                remarks
            )
            VALUES(?,?,?,?,?,?,?,?)
            """, (

                backup_file,

                backup_path,

                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                backup_size,

                backup_type,

                status,

                created_by,

                remarks

            ))

            self.commit()

            return True

        except Exception as e:

            print(
                "Backup History Error:",
                e
            )

            return False

    # ==========================================
    # Get Backup History
    # ==========================================

    def get_backup_history(self):

        try:

            self.cursor.execute("""
            SELECT
              id,
              backup_file,
              backup_path,
              backup_date,
              backup_size,
              action,
              backup_type,
              status
              FROM backup_history
            ORDER BY id DESC
            """)

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Get Backup History Error:",
                e
            )

            return []

    # ==========================================
    # Delete Backup History
    # ==========================================

    def delete_backup_history(
        self,
        history_id
    ):

        try:

            self.cursor.execute(
                """
                DELETE FROM backup_history
                WHERE id=?
                """,
                (history_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print(
                "Delete Backup History Error:",
                e
            )

            return False

    # ==========================================
    # Clear Backup History
    # ==========================================

    def clear_backup_history(self):

        try:

            self.cursor.execute(
                "DELETE FROM backup_history"
            )

            self.commit()

            return True

        except Exception as e:

            print(
                "Clear Backup History Error:",
                e
            )

            return False

        

    # ==========================================
    # Add Restore History
    # ==========================================

    def add_restore_history(
        self,
        backup_file,
        created_by="System"
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO backup_history(
                    backup_file,
                    backup_path,
                    backup_date,
                    backup_size,
                    action,
                    backup_type,
                    status,
                    created_by,
                    remarks
                )
                VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (

                    backup_file,

                    "",

                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                    0,

                    "RESTORE",

                    "Offline",

                    "Success",

                    created_by,

                    "Database restored successfully"

                )
            )

            self.commit()

            return True

        except Exception as e:

            print(
                "Restore History Error:",
                e
            )

            return False