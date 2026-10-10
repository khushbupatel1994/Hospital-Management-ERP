"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Reports Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class ReportsUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Create Widgets
    # ==========================================

    def create_widgets(self):

        self.main = ctk.CTkFrame(
            self.root,
            corner_radius=10
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Header
        # ==========================================

        self.header = ctk.CTkFrame(
            self.main,
            height=70
        )

        self.header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header,
            text="📊 Reports Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

        # ==========================================
        # Search
        # ==========================================

        self.search_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        self.search_frame.pack(
            side="right",
            padx=20
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=250,
            placeholder_text="Search Report..."
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100
        )

        self.search_btn.pack(
            side="left",
            padx=5
        )

        # ==========================================
        # Body
        # ==========================================

        self.body = ctk.CTkFrame(self.main)
        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Left Scrollable Frame
        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420,
            corner_radius=10
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # Right Frame
        self.right = ctk.CTkFrame(self.body)
        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )
        # ==========================================
        # Report Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Report Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # ==========================================
        # Report Type
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Report Type"
        ).pack(anchor="w", padx=20)

        self.report_type = ctk.CTkComboBox(
            self.left,
            values=[
                "Patient Report",
                "Doctor Report",
                "Appointment Report",
                "OPD Report",
                "IPD Report",
                "Billing Report",
                "Pharmacy Report",
                "Laboratory Report",
                "Inventory Report",
                "Accounts Report"
            ]
        )

        self.report_type.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # From Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="From Date"
        ).pack(anchor="w", padx=20)

        self.from_date = DateEntry(
            self.left,
            width=20,
            date_pattern="dd-mm-yyyy",
            background="#1F6AA5",
            foreground="white",
            borderwidth=2
        )

        self.from_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # To Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="To Date"
        ).pack(anchor="w", padx=20)

        self.to_date = DateEntry(
            self.left,
            width=20,
            date_pattern="dd-mm-yyyy",
            background="#1F6AA5",
            foreground="white",
            borderwidth=2
        )

        self.to_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Department
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Department"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            values=[
                "All Departments",
                "Reception",
                "OPD",
                "IPD",
                "Pharmacy",
                "Laboratory",
                "Inventory",
                "Accounts"
            ]
        )

        self.department.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Export Format
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Export Format"
        ).pack(anchor="w", padx=20)

        self.export_format = ctk.CTkComboBox(
            self.left,
            values=[
                "Screen Preview",
                "PDF",
                "Excel",
                "CSV"
            ]
        )

        self.export_format.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values

        self.report_type.set("Patient Report")
        self.department.set("All Departments")
        self.export_format.set("Screen Preview")

        # ==========================================
        # Buttons
        # ==========================================

        self.button_frame = ctk.CTkFrame(
            self.left,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.generate_btn = ctk.CTkButton(
            self.button_frame,
            text="Generate Report"
        )

        self.generate_btn.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.export_btn = ctk.CTkButton(
            self.button_frame,
            text="Export"
        )

        self.export_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.print_btn = ctk.CTkButton(
            self.button_frame,
            text="Print"
        )

        self.print_btn.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear"
        )

        self.clear_btn.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # ==========================================
        # Report Preview
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Report Preview",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=10
        )

        self.table_frame = ctk.CTkFrame(
            self.right
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Scrollbar
        # ==========================================

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # Treeview
        # ==========================================

        self.report_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.report_table.yview
        )

        self.report_table.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # Treeview Style
        # ==========================================

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#1F6AA5")],
            foreground=[("selected", "white")]
        )

        # ==========================================
        # Column Stretch
        # ==========================================
        # Default columns
        self.report_table["columns"] = ()

        # ==========================================
        # Report Summary
        # ==========================================

        self.summary_frame = ctk.CTkFrame(
          self.right,
          height=50
        )

        self.summary_frame.pack(
          fill="x",
           padx=10,
           pady=(0, 10)
        )

        self.summary_frame.pack_propagate(False)

        self.total_records = ctk.CTkLabel(
         self.summary_frame,
         text="Total Records : 0",
         font=("Segoe UI", 12, "bold")
        )

        self.total_records.pack(
         side="left",
          padx=20
        )

        self.total_amount = ctk.CTkLabel(
         self.summary_frame,
         text="Total Amount : ₹0.00",
          font=("Segoe UI", 12, "bold")
       )

        self.total_amount.pack(
         side="right",
         padx=20
        )

        # ==========================================
        # Default Focus
        # ==========================================

        self.search_entry.focus()

        # ==========================================
        # End of Reports UI
        # ==========================================