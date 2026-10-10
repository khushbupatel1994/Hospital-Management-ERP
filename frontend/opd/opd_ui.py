"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : OPD Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class OPDUI:

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
            text="🏥 OPD Management",
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
            placeholder_text="Search OPD..."
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

        self.body = ctk.CTkFrame(
            self.main
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420,
            fg_color="transparent"
        )

        self.left.pack(
         side="left",
         fill="both",
         expand=True,
         padx=(0, 10),
         pady=10
        )
        self.right = ctk.CTkFrame(
            self.body
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # OPD Form
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="OPD Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # OPD ID
        ctk.CTkLabel(
            self.left,
            text="OPD ID"
        ).pack(anchor="w", padx=20)

        self.opd_id = ctk.CTkEntry(
            self.left,
            placeholder_text="OPD ID",
            state="disabled"
        )

        self.opd_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Patient
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

        # Doctor
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

        # Department
        ctk.CTkLabel(
            self.left,
            text="Department"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            values=[
                "General Medicine",
                "Cardiology",
                "Neurology",
                "Orthopedics",
                "Pediatrics",
                "Gynecology",
                "Dermatology",
                "ENT"
            ]
        )

        self.department.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Visit Date
        ctk.CTkLabel(
            self.left,
            text="Visit Date"
        ).pack(anchor="w", padx=20)

        self.visit_date = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            width=22
        )

        self.visit_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Visit Time
        ctk.CTkLabel(
            self.left,
            text="Visit Time"
        ).pack(anchor="w", padx=20)

        self.visit_time = ctk.CTkEntry(
            self.left,
            placeholder_text="10:30 AM"
        )

        self.visit_time.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Status
        ctk.CTkLabel(
            self.left,
            text="Status"
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Open",
                "Closed"
            ]
        )

        self.status.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values
        self.department.set("General Medicine")
        self.status.set("Open")

        # ==========================================
        # Chief Complaint
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Chief Complaint"
        ).pack(anchor="w", padx=20)

        self.chief_complaint = ctk.CTkTextbox(
            self.left,
            height=60
        )

        self.chief_complaint.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Diagnosis
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Diagnosis"
        ).pack(anchor="w", padx=20)

        self.diagnosis = ctk.CTkTextbox(
            self.left,
            height=60
        )

        self.diagnosis.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Prescription
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Prescription"
        ).pack(anchor="w", padx=20)

        self.prescription = ctk.CTkTextbox(
            self.left,
            height=80
        )

        self.prescription.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Follow-up Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Follow-up Date"
        ).pack(anchor="w", padx=20)

        self.followup_date = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            width=22
        )

        self.followup_date.pack(
            fill="x",
            padx=20,
            pady=5
        )
        # ==========================================
        # Notes
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Notes"
        ).pack(anchor="w", padx=20)

        self.notes = ctk.CTkTextbox(
            self.left,
            height=70
        )

        self.notes.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

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
            text="Add",
            width=100,
            height=40
        )

        self.add_btn.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.update_btn = ctk.CTkButton(
            self.button_frame,
            text="Update",
            width=100,
            height=40
        )

        self.update_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete",
            width=100,
            height=40

        )

        self.delete_btn.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            width=100,
            height=40
        )

        self.clear_btn.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # ==========================================
        # OPD List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="OPD List",
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

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )
        self.scroll_x = ctk.CTkScrollbar(
            self.table_frame,
            orientation="horizontal"
        )

        self.scroll_x.pack(
            side="bottom",
            fill="x"
        )

        columns = (
            "ID",
            "OPD ID",
            "Patient",
            "Doctor",
            "Department",
            "Visit Date",
            "Visit Time",
            "Status"
        )

        self.opd_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )
        self.scroll_x.configure(
           command=self.opd_table.xview
        )
        self.scroll_y.configure(
            command=self.opd_table.yview
        )

        for col in columns:
            self.opd_table.heading(col, text=col)
            self.opd_table.column(col, anchor="center")

        self.opd_table.column("ID", width=60, anchor="center")
        self.opd_table.column("OPD ID", width=100, anchor="center")
        self.opd_table.column("Patient", width=180)
        self.opd_table.column("Doctor", width=180)
        self.opd_table.column("Department", width=150)
        self.opd_table.column("Visit Date", width=110, anchor="center")
        self.opd_table.column("Visit Time", width=100, anchor="center")
        self.opd_table.column("Status", width=90, anchor="center")

        self.opd_table.pack(
            fill="both",
            expand=True
        )

       