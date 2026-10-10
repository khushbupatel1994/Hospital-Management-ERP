"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : IPD Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class IPDUI:

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
            text="🏥 IPD Management",
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
            placeholder_text="Search Admission..."
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
            width=420
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=False,
            padx=(0, 10)
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
        # IPD Admission Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="IPD Admission Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # ==========================================
        # Admission ID
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Admission ID"
        ).pack(anchor="w", padx=20)

        self.admission_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Admission ID",
            state="readonly"
        )

        self.admission_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

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
        # Ward
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Ward"
        ).pack(anchor="w", padx=20)

        self.ward = ctk.CTkComboBox(
            self.left,
            values=[
                "General Ward",
                "Semi Private",
                "Private",
                "ICU",
                "NICU",
                "PICU",
                "Emergency"
            ]
        )

        self.ward.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Bed Number
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Bed Number"
        ).pack(anchor="w", padx=20)

        self.bed_no = ctk.CTkComboBox(
            self.left,
            values=[
                "Bed-001",
                "Bed-002",
                "Bed-003",
                "Bed-004",
                "Bed-005",
                "Bed-006",
                "Bed-007",
                "Bed-008",
                "Bed-009",
                "Bed-010"
            ]
        )

        self.bed_no.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.bed_no.set("Bed-001")

        # ==========================================
        # Admission Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Admission Date"
        ).pack(anchor="w", padx=20)

        self.admission_date = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            font=("Segoe UI", 11),
            width=18
        )

        self.admission_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Expected Discharge Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Expected Discharge Date"
        ).pack(anchor="w", padx=20)

        self.discharge_date = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            font=("Segoe UI", 11),
            width=18
        )

        self.discharge_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Value

        self.ward.set("General Ward")

        # ==========================================
        # Diagnosis
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Diagnosis"
        ).pack(anchor="w", padx=20)

        self.diagnosis = ctk.CTkTextbox(
            self.left,
            height=70
        )

        self.diagnosis.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Treatment Plan
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Treatment Plan"
        ).pack(anchor="w", padx=20)

        self.treatment = ctk.CTkTextbox(
            self.left,
            height=70
        )

        self.treatment.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Daily Charges
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Daily Charges"
        ).pack(anchor="w", padx=20)

        self.daily_charges = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.daily_charges.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Admission Status
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Admission Status"
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Admitted",
                "Under Treatment",
                "Recovered",
                "Discharged",
                "Referred"
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

        self.status.set("Admitted")

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
    # IPD Admission List
    # ==========================================

        ctk.CTkLabel(
            self.right,
            text="IPD Admission List",
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
        # Horizontal Scrollbar
        self.scroll_x = ctk.CTkScrollbar(
            self.table_frame,
            orientation="horizontal"
        )

        self.scroll_x.pack(
            side="bottom",
            fill="x"
        )

        # ==========================================
        # Treeview
        # ==========================================

        columns = (
            "ID",
            "Admission ID",
            "Patient",
            "Doctor",
            "Ward",
            "Bed",
            "Admission Date",
            "Status"
        )

        self.ipd_table = ttk.Treeview(
           self.table_frame,
           columns=columns,
           show="headings",
          yscrollcommand=self.scroll_y.set,
          xscrollcommand=self.scroll_x.set
        )

        self.scroll_y.configure(
            command=self.ipd_table.yview
        )
        self.scroll_x.configure(
           command=self.ipd_table.xview
        )

        for col in columns:

            self.ipd_table.heading(
                col,
                text=col
            )

        self.ipd_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.ipd_table.column(
            "Admission ID",
            width=130,
            anchor="center"
        )

        self.ipd_table.column(
            "Patient",
            width=180
        )

        self.ipd_table.column(
            "Doctor",
            width=180
        )

        self.ipd_table.column(
            "Ward",
            width=140,
            anchor="center"
        )

        self.ipd_table.column(
            "Bed",
            width=90,
            anchor="center"
        )

        self.ipd_table.column(
            "Admission Date",
            width=130,
            anchor="center"
        )

        self.ipd_table.column(
            "Status",
            width=130,
            anchor="center"
        )

        self.ipd_table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )
      