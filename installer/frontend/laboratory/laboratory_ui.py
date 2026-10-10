"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class LaboratoryUI:

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
            text="🧪 Laboratory Management",
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
            placeholder_text="Search Test..."
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
        self.body.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT
        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420,
            height=650      # height देना जरूरी है
        )

        self.left.pack(
            side="left",
            fill="both",    # y की जगह both
            expand=False,
            padx=(0,10),
            pady=5
        )

        # RIGHT
        self.right = ctk.CTkFrame(self.body)

        self.right.pack(
            side="left",
            fill="both",
            expand=True,
            pady=5
        )
        # ==========================================
        # Laboratory Test Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Laboratory Test Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # ==========================================
        # Test ID
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Test ID"
        ).pack(anchor="w", padx=20)

        self.test_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Test ID",
            state="disabled"
        )

        self.test_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Test Name
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Test Name"
        ).pack(anchor="w", padx=20)

        self.test_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Test Name"
        )

        self.test_name.pack(
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
                "Pathology",
                "Biochemistry",
                "Microbiology",
                "Hematology",
                "Radiology",
                "Cardiology",
                "General"
            ]
        )

        self.department.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Sample Type
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Sample Type"
        ).pack(anchor="w", padx=20)

        self.sample_type = ctk.CTkComboBox(
            self.left,
            values=[
                "Blood",
                "Urine",
                "Stool",
                "Sputum",
                "Saliva",
                "Serum",
                "Plasma",
                "X-Ray",
                "ECG",
                "Others"
            ]
        )

        self.sample_type.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Test Fee
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Test Fee"
        ).pack(anchor="w", padx=20)

        self.test_fee = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.test_fee.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Normal Range
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Normal Range"
        ).pack(anchor="w", padx=20)

        self.normal_range = ctk.CTkEntry(
            self.left,
            placeholder_text="Example: 4.5 - 11.0"
        )

        self.normal_range.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values

        self.department.set("Pathology")
        self.sample_type.set("Blood")

        # ==========================================
        # Patient
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Patient"
        ).pack(anchor="w", padx=20)

        self.patient = ctk.CTkComboBox(
            self.left,
            values=[]
        )

        self.patient.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Doctor
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Doctor"
        ).pack(anchor="w", padx=20)

        self.doctor = ctk.CTkComboBox(
            self.left,
            values=[]
        )

        self.doctor.pack(
            fill="x",
            padx=20,
            pady=5
        )
        # ==========================================
        # Mobile
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Mobile"
        ).pack(anchor="w", padx=20)

        self.mobile = ctk.CTkEntry(
            self.left,
            placeholder_text="Mobile Number"
        )

        self.mobile.pack(
            fill="x",
            padx=20,
            pady=5
        )
        # ==========================================
        # Age
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Age"
        ).pack(anchor="w", padx=20)

        self.age = ctk.CTkEntry(
            self.left,
            placeholder_text="Age"
        )

        self.age.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Gender
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Gender"
        ).pack(anchor="w", padx=20)

        self.gender = ctk.CTkComboBox(
            self.left,
            values=[
                "Male",
                "Female",
                "Other"
            ]
        )

        self.gender.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Test Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Test Date"
        ).pack(anchor="w", padx=20)

        self.test_date = DateEntry(
            self.left,
            width=20,
            date_pattern="dd-mm-yyyy"
        )

        self.test_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Test Result
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Test Result"
        ).pack(anchor="w", padx=20)

        self.test_result = ctk.CTkTextbox(
            self.left,
            height=80
        )

        self.test_result.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Status
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Status"
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Pending",
                "In Progress",
                "Completed",
                "Cancelled"
            ]
        )

        self.status.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Remarks
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Remarks"
        ).pack(anchor="w", padx=20)

        self.remarks = ctk.CTkTextbox(
            self.left,
            height=70
        )

        self.remarks.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Status

        self.status.set("Pending")

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
            pady=15
        )

        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Add"
        )

        self.add_btn.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.update_btn = ctk.CTkButton(
            self.button_frame,
            text="Update"
        )

        self.update_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete"
        )

        self.delete_btn.grid(
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
        # Laboratory Test List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Laboratory Test List",
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

        columns = (
            "ID",
            "Test ID",
            "Test Name",
            "Patient",
            "Doctor",
            "Department",
            "Fee",
            "Status"
        )

        self.laboratory_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.laboratory_table.yview
        )

        for col in columns:

            self.laboratory_table.heading(
                col,
                text=col
            )

        self.laboratory_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.laboratory_table.column(
            "Test ID",
            width=120,
            anchor="center"
        )

        self.laboratory_table.column(
            "Test Name",
            width=220
        )

        self.laboratory_table.column(
            "Patient",
            width=180
        )

        self.laboratory_table.column(
            "Doctor",
            width=180
        )

        self.laboratory_table.column(
            "Department",
            width=140,
            anchor="center"
        )

        self.laboratory_table.column(
            "Fee",
            width=100,
            anchor="e"
        )

        self.laboratory_table.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.laboratory_table.pack(
            fill="both",
            expand=True
        )