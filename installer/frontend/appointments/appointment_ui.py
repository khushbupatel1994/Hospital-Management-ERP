"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Appointment Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class AppointmentUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    def create_widgets(self):

        # ==========================================
        # Main Frame
        # ==========================================

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
            text="📅 Appointment Management",
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
            placeholder_text="Search Appointment..."
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

        # Left Frame

        self.left = ctk.CTkScrollableFrame(
         self.body,
         width=430,
         corner_radius=10
        )

        self.left.pack(
         side="left",
         fill="both",
         expand=False,
         padx=(0, 10)
        )


        # Right Frame

        self.right = ctk.CTkFrame(
            self.body
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # Appointment Form
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Appointment Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # Appointment ID
        ctk.CTkLabel(
            self.left,
            text="Appointment ID"
        ).pack(anchor="w", padx=20)

        self.appointment_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Appointment ID",
            state="disabled"
        )
        self.appointment_id.pack(fill="x", padx=20, pady=5)

        # Patient
        ctk.CTkLabel(
            self.left,
            text="Patient"
        ).pack(anchor="w", padx=20)

        self.patient = ctk.CTkComboBox(
            self.left,
            values=[]
        )
        self.patient.pack(fill="x", padx=20, pady=5)

        # Doctor
        ctk.CTkLabel(
            self.left,
            text="Doctor"
        ).pack(anchor="w", padx=20)

        self.doctor = ctk.CTkComboBox(
            self.left,
            values=[]
        )
        self.doctor.pack(fill="x", padx=20, pady=5)

        # Department
        ctk.CTkLabel(
            self.left,
            text="Department"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            values=[
                "Cardiology",
                "Neurology",
                "Orthopedics",
                "Pediatrics",
                "General Medicine",
                "Gynecology",
                "Dermatology",
                "ENT"
            ]
        )
        self.department.pack(fill="x", padx=20, pady=5)

        # Appointment Date
        ctk.CTkLabel(
            self.left,
            text="Appointment Date"
        ).pack(anchor="w", padx=20)

        self.appointment_date = DateEntry(
            self.left,
            width=18,
            date_pattern="dd-mm-yyyy"
        )

        self.appointment_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Appointment Time
        ctk.CTkLabel(
            self.left,
            text="Appointment Time"
        ).pack(anchor="w", padx=20)

        self.appointment_time = ctk.CTkComboBox(
            self.left,
            values=[
                "09:00 AM",
                "09:30 AM",
                "10:00 AM",
                "10:30 AM",
                "11:00 AM",
                "11:30 AM",
                "12:00 PM",
                "12:30 PM",
                "01:00 PM",
                "01:30 PM",
                "02:00 PM",
                "02:30 PM",
                "03:00 PM",
                "03:30 PM",
                "04:00 PM",
                "04:30 PM",
                "05:00 PM"
            ]
        )
        self.appointment_time.pack(fill="x", padx=20, pady=5)
        self.appointment_time.set("09:00 AM")

        # Visit Type
        ctk.CTkLabel(
            self.left,
            text="Visit Type"
        ).pack(anchor="w", padx=20)

        self.visit_type = ctk.CTkComboBox(
            self.left,
            values=[
                "New",
                "Follow-up"
            ]
        )
        self.visit_type.pack(fill="x", padx=20, pady=5)

        # Token Number
        ctk.CTkLabel(
            self.left,
            text="Token Number"
        ).pack(anchor="w", padx=20)

        self.token_no = ctk.CTkEntry(
            self.left,
            placeholder_text="Token Number"
        )
        self.token_no.pack(fill="x", padx=20, pady=5)

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
                "Scheduled",
                "Completed",
                "Cancelled"
            ]
        )
        self.status.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # Remarks
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Remarks"
        ).pack(anchor="w", padx=20)

        self.remarks = ctk.CTkTextbox(
            self.left,
            height=80
        )
        self.remarks.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values

        self.department.set("General Medicine")
        self.visit_type.set("New")
        self.status.set("Scheduled")

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
        # Appointment List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Appointment List",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

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
            "Appointment ID",
            "Patient",
            "Doctor",
            "Department",
            "Date",
            "Time",
            "Token",
            "Status"

        )

        self.appointment_table = ttk.Treeview(

            self.table_frame,

            columns=columns,

            show="headings",

            yscrollcommand=self.scroll_y.set

        )

        self.scroll_y.configure(
            command=self.appointment_table.yview
        )

        for col in columns:

            self.appointment_table.heading(
                col,
                text=col
            )

            self.appointment_table.column(
                col,
                width=120,
                anchor="center"
            )

        self.appointment_table.pack(
            fill="both",
            expand=True
        )

            