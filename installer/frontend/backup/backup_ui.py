"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Backup UI
Version : 3.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk

class BackupUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Create Widgets
    # ==========================================

    def create_widgets(self):

        self.main_frame = ctk.CTkFrame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Database Backup & Restore",
            font=("Arial", 24, "bold")
        )

        self.title_label.pack(
            pady=20
        )

        # ==========================================
        # Backup Folder
        # ==========================================

        self.path_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.path_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            self.path_frame,
            text="Backup Folder"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.backup_path = ctk.CTkEntry(
            self.path_frame,
            width=450
        )

        self.backup_path.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse"
        )

        self.browse_btn.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # ==========================================
        # Buttons
        # ==========================================

        self.button_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.button_frame.pack(
            pady=20
        )

        self.backup_btn = ctk.CTkButton(
            self.button_frame,
            text="Create Backup",
            width=180
        )

        self.backup_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        self.restore_btn = ctk.CTkButton(
            self.button_frame,
            text="Restore Backup",
            width=180
        )

        self.restore_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        self.verify_backup_btn = ctk.CTkButton(
            self.button_frame,
            text="Verify Backup",
            width=180
        )

        self.verify_backup_btn.grid(
            row=0,
            column=2,
            padx=10
        )

        self.delete_backup_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete Backup",
            width=180
        )

        self.delete_backup_btn.grid(
            row=0,
            column=3,
            padx=10
        )

        # ==========================================
        # Status
        # ==========================================

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Status : Ready",
            font=("Arial", 14)
        )

        self.status_label.pack(
            pady=10
        )

        # ==========================================
        # Backup History
        # ==========================================

        self.history_title = ctk.CTkLabel(
            self.main_frame,
            text="Backup History",
            font=("Arial", 20, "bold")
        )

        self.history_title.pack(
            pady=10
        )

        # ==========================================
        # History Search
        # ==========================================

        self.history_search_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.history_search_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.history_search_entry = ctk.CTkEntry(
            self.history_search_frame,
            width=420,
            placeholder_text="Search backup history by file, path, date, or status..."
        )

        self.history_search_entry.pack(
            side="left",
            padx=(10, 8),
            pady=8
        )

        self.search_history_btn = ctk.CTkButton(
            self.history_search_frame,
            text="Search",
            width=120
        )

        self.search_history_btn.pack(
            side="left",
            padx=8,
            pady=8
        )

        self.clear_history_search_btn = ctk.CTkButton(
            self.history_search_frame,
            text="Clear Search",
            width=120
        )

        self.clear_history_search_btn.pack(
            side="left",
            padx=8,
            pady=8
        )

        self.history_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Action",
            "File Name",
            "Backup Path",
            "Date",
            "Size",
            "Type",
            "Status"
        )

        self.history_table = ttk.Treeview(
            self.history_frame,
            columns=columns,
            show="headings",
            height=8
        )

        column_widths = {
            "ID": 60,
            "Action": 100,
            "File Name": 210,
            "Backup Path": 330,
            "Date": 150,
            "Size": 85,
            "Type": 100,
            "Status": 100,
        }

        for col in columns:
            self.history_table.heading(
                col,
                text=col
            )

            self.history_table.column(
                col,
                width=column_widths[col],
                minwidth=60
            )

        self.history_table.pack(
            fill="both",
            expand=True,
            side="top"
        )

        # The full backup location can be longer than the available window
        # width, especially on smaller screens.
        self.history_scrollbar = ttk.Scrollbar(
            self.history_frame,
            orient="horizontal",
            command=self.history_table.xview
        )

        self.history_table.configure(
            xscrollcommand=self.history_scrollbar.set
        )

        self.history_scrollbar.pack(
            fill="x",
            side="bottom"
        )

        # Refresh Button
        self.refresh_history_btn = ctk.CTkButton(
            self.main_frame,
            text="Refresh History"
        )

        self.refresh_history_btn.pack(
            pady=10
        )
