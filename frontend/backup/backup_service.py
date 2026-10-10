"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Backup Service
Version : 4.0
===========================================================
"""

import os
import shutil
import sqlite3
from datetime import datetime


class BackupService:

    # ==========================================
    # Create Secure Offline Backup
    # ==========================================

    def create_backup(
        self,
        database_path,
        backup_folder
    ):

        source_conn = None
        backup_conn = None

        try:

            # ------------------------------------------
            # Check Database
            # ------------------------------------------

            if not os.path.exists(database_path):

                return False, "Database not found."

            # ------------------------------------------
            # Create Backup Folder
            # ------------------------------------------

            os.makedirs(
                backup_folder,
                exist_ok=True
            )

            # ------------------------------------------
            # Backup File Name
            # ------------------------------------------

            backup_name = (
                f"hospital_backup_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )

            destination = os.path.join(
                backup_folder,
                backup_name
            )

            # ------------------------------------------
            # SQLite Safe Backup
            # ------------------------------------------

            source_conn = sqlite3.connect(
                database_path
            )

            backup_conn = sqlite3.connect(
                destination
            )

            with backup_conn:

                source_conn.backup(
                    backup_conn
                )

            # ------------------------------------------
            # Verify Backup
            # ------------------------------------------

            if not self.verify_backup(destination):

                try:
                    os.remove(destination)
                except Exception:
                    pass

                return False, "Backup verification failed."

            return True, destination

        except Exception as e:

            return False, f"Backup failed: {e}"

        finally:

            if source_conn is not None:
                source_conn.close()

            if backup_conn is not None:
                backup_conn.close()

    # ==========================================
    # Verify Backup
    # ==========================================

    def verify_backup(
        self,
        backup_file
    ):

        conn = None

        try:

            if not os.path.exists(backup_file):

                return False

            conn = sqlite3.connect(
                backup_file
            )

            cursor = conn.cursor()

            cursor.execute(
                "PRAGMA integrity_check"
            )

            result = cursor.fetchone()

            if result and result[0] == "ok":

                return True

            return False

        except Exception:

            return False

        finally:

            if conn is not None:
                conn.close()

    # ==========================================
    # Restore Backup
    # ==========================================

    def restore_backup(
        self,
        backup_file,
        database_path
    ):

        source_conn = None
        destination_conn = None

        try:

            # ------------------------------------------
            # Check Backup
            # ------------------------------------------

            if not os.path.exists(backup_file):

                return False, "Backup file not found."

            # ------------------------------------------
            # Verify Backup Before Restore
            # ------------------------------------------

            if not self.verify_backup(
                backup_file
            ):

                return False, (
                    "Backup file is corrupted "
                    "or invalid."
                )

            # ------------------------------------------
            # Create Safety Backup
            # ------------------------------------------

            if os.path.exists(database_path):

                safety_name = (
                    f"{database_path}."
                    f"before_restore_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )

                shutil.copy2(
                    database_path,
                    safety_name
                )

            # ------------------------------------------
            # Restore Database
            # ------------------------------------------

            source_conn = sqlite3.connect(
                backup_file
            )

            destination_conn = sqlite3.connect(
                database_path
            )

            with destination_conn:

                source_conn.backup(
                    destination_conn
                )

            # ------------------------------------------
            # Verify Restored Database
            # ------------------------------------------

            if not self.verify_backup(
                database_path
            ):

                return False, (
                    "Restore completed but "
                    "database verification failed."
                )

            return True, (
                "Database restored successfully."
            )

        except Exception as e:

            return False, f"Restore failed: {e}"

        finally:

            if source_conn is not None:
                source_conn.close()

            if destination_conn is not None:
                destination_conn.close()