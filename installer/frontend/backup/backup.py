"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Backup Controller
Version : 3.0
===========================================================
"""

import os
from tkinter import filedialog, messagebox
from frontend.backup.backup_crud import BackupCRUD
from frontend.backup.backup_ui import BackupUI
from frontend.backup.backup_service import BackupService


class Backup(BackupUI):

    def __init__(self, root):
        
        self.crud = BackupCRUD()

        super().__init__(root)

        self.service = BackupService()

        self.bind_events()
        self.load_backup_history()

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.browse_btn.configure(
            command=self.browse_folder
        )

        self.backup_btn.configure(
            command=self.create_backup
        )

        self.restore_btn.configure(
            command=self.restore_backup
        )


        self.refresh_history_btn.configure(
            command=self.load_backup_history
        )

        self.search_history_btn.configure(
            command=self.search_backup_history
        )

        self.clear_history_search_btn.configure(
            command=self.clear_backup_history_search
        )

        self.history_search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_backup_history()
        )

        self.delete_backup_btn.configure(
            command=self.delete_backup
        )

        self.verify_backup_btn.configure(
            command=self.verify_backup
        )
    # ==========================================
    # Browse Folder
    # ==========================================

    def browse_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.backup_path.delete(0, "end")

            self.backup_path.insert(0, folder)

    # ==========================================
    # Create Backup
    # ==========================================

    def create_backup(self):

        backup_folder = self.backup_path.get().strip()

        if not backup_folder:

            messagebox.showerror(
                "Error",
                "Please select a backup folder."
            )

            return

        # Use the same database file as the rest of the application.  The
        # application keeps its writable database in LOCALAPPDATA, so a
        # project-relative path would otherwise back up the bundled seed DB.
        database_path = self.crud.get_database_path()

        success, message = self.service.create_backup(
            database_path,
            backup_folder
        )

        if success:

            # ==========================================
            # Get Backup File Information
            # ==========================================

            backup_file = message

            backup_name = os.path.basename(
                backup_file
            )

            backup_size = os.path.getsize(
                backup_file
            )

            # ==========================================
            # Save Backup History
            # ==========================================

            history_saved = self.crud.add_backup_history(

                backup_file=backup_name,

                backup_path=backup_file,

                backup_size=backup_size,

                backup_type="Offline",

                status="Success",

                created_by="System",

                remarks="Backup verified successfully"

            )

            # ==========================================
            # Update UI
            # ==========================================

            self.status_label.configure(
                text="Status : Backup Created Successfully"
            )

            if history_saved:

                messagebox.showinfo(
                    "Success",
                    "Backup created and history saved successfully.\n\n"
                    f"Backup:\n{backup_file}"
                )

            else:

                messagebox.showwarning(
                    "Backup Created",
                    "Backup created successfully, "
                    "but backup history could not be saved.\n\n"
                    f"Backup:\n{backup_file}"
                )

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # ==========================================
    # Load Backup History
    # ==========================================

    def load_backup_history(self):

        try:
            rows = self.crud.get_backup_history()

            self.display_backup_history(rows)

        except Exception as e:

            print(
                "Backup History Error:",
                e
            )

    # ==========================================
    # Display Backup History
    # ==========================================

    def display_backup_history(self, rows):

        for item in self.history_table.get_children():

            self.history_table.delete(item)

        for row in rows:

            backup_id = row[0]
            file_name = row[1]
            backup_path = row[2]
            backup_date = row[3]
            backup_size = row[4]
            action = row[5]
            backup_type = row[6]
            status = row[7]

            # Convert Bytes to MB

            size_mb = round(
                (backup_size or 0) / (1024 * 1024),
                2
            )

            self.history_table.insert(
                "",
                "end",
                values=(
                    backup_id,
                    action,
                    file_name,
                    backup_path,
                    backup_date,
                    f"{size_mb} MB",
                    backup_type,
                    status
                )
            )

    # ==========================================
    # Search Backup History
    # ==========================================

    def search_backup_history(self):

        keyword = self.history_search_entry.get().strip().casefold()
        rows = self.crud.get_backup_history()

        if keyword:
            rows = [
                row for row in rows
                if any(keyword in str(value).casefold() for value in row)
            ]

        self.display_backup_history(rows)

    # ==========================================
    # Clear Backup History Search
    # ==========================================

    def clear_backup_history_search(self):

        self.history_search_entry.delete(0, "end")
        self.load_backup_history()

    # ==========================================
    # Restore Backup
    # ==========================================

    def restore_backup(self):

        backup_file = filedialog.askopenfilename(

            title="Select Backup File",

            filetypes=[
                ("Database Files", "*.db")
            ]

        )

        if not backup_file:
            return

        confirm = messagebox.askyesno(
            "Confirm Restore",
            "Are you sure you want to restore this backup?\n\n"
            "Current database will be replaced."
        )

        if not confirm:
            return

        # Close the history connection before replacing the database.  Keeping
        # it open can lock the file on Windows and leaves the UI connected to
        # the pre-restore database.
        database_path = self.crud.get_database_path()
        self.crud.close()

        success, message = self.service.restore_backup(
            backup_file,
            database_path
        )

        # Restore the history connection whether the operation succeeded or
        # failed, so the backup screen remains usable.
        self.crud.connect()

        if success:

            self.status_label.configure(
                text="Status : Database Restored"
            )

            self.crud.add_restore_history(
                os.path.basename(backup_file)
            )

            self.load_backup_history()

            messagebox.showinfo(
                "Success",
                message
            )

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # ==========================================
    # Delete Backup
    # ==========================================

    def delete_backup(self):

        selected = self.history_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select backup history."
            )

            return

        values = self.history_table.item(
            selected,
            "values"
        )

        if len(values) < 3:
            messagebox.showerror(
                "Error",
                "Invalid backup history record."
            )
            return

        history_id = values[0]
        action = values[1]
        file_name = values[2]

        # ==========================================
        # Find Backup File Path
        # ==========================================

        backup_path = None

        rows = self.crud.get_backup_history()

        for row in rows:

            if row[0] == int(history_id):

                backup_path = row[2]
                break

        # A restore entry is an audit record rather than a backup owned by the
        # application.  It has no physical file to remove.
        if action == "RESTORE":
            confirm = messagebox.askyesno(
                "Delete Restore History",
                "This is a restore history record; no backup file will be "
                "deleted.\n\nRemove this history record?"
            )

            if confirm and self.crud.delete_backup_history(history_id):
                messagebox.showinfo(
                    "Success",
                    "Restore history deleted successfully."
                )
                self.load_backup_history()

            return

        if not backup_path or not os.path.exists(backup_path):
            confirm = messagebox.askyesno(
                "Backup File Missing",
                "The backup file no longer exists at its saved path.\n\n"
                "Remove the history record?"
            )

            if confirm and self.crud.delete_backup_history(history_id):
                messagebox.showinfo(
                    "Success",
                    "Missing backup history deleted successfully."
                )
                self.load_backup_history()

            return

        # ==========================================
        # Delete Physical Backup File
        # ==========================================

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this backup file?\n\n"
            f"File: {file_name}\n"
            f"Path: {backup_path}"
        )

        if not confirm:
            return

        os.remove(backup_path)

        if self.crud.delete_backup_history(history_id):
            messagebox.showinfo(
                "Success",
                "Backup deleted successfully."
            )
            self.load_backup_history()
        else:
            messagebox.showerror(
                "Error",
                "Failed to delete backup history."
            )
    # ==========================================
    # Verify Backup
    # ==========================================

    def verify_backup(self):
        backup_file = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[
                ("Database Files", "*.db")
            ]
        )

        if not backup_file:
            return

        # Verify Backup
        success = self.service.verify_backup(
            backup_file
        )

        if success:
            self.status_label.configure(
                text="Status : Backup Verified"
            )

            messagebox.showinfo(
                "Backup Verification",
                "Backup file is valid and healthy."
            )

        else:
            self.status_label.configure(
                text="Status : Backup Corrupted"
            )

            messagebox.showerror(
                "Backup Verification",
                "Backup file is corrupted or invalid."
            )
