"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Doctor Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk


class DoctorUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

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
            text="👨‍⚕️ Doctor Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

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
        placeholder_text="Search Doctor..."
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
            height=650,
            corner_radius=10
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10),
            pady=5
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
        # Doctor Form
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Doctor Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # Doctor ID
        ctk.CTkLabel(
            self.left,
            text="Doctor ID"
        ).pack(anchor="w", padx=20)

        self.doctor_id = ctk.CTkEntry(
           self.left,
            placeholder_text="Doctor ID",
            state="disabled"
)
        self.doctor_id.pack(fill="x", padx=20, pady=5)

        # Full Name
        ctk.CTkLabel(
            self.left,
            text="Full Name"
        ).pack(anchor="w", padx=20)

        self.full_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Doctor Name"
        )
        self.full_name.pack(fill="x", padx=20, pady=5)

        # Gender
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
        self.gender.pack(fill="x", padx=20, pady=5)

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

        # Specialization
        ctk.CTkLabel(
            self.left,
            text="Specialization"
        ).pack(anchor="w", padx=20)

        self.specialization = ctk.CTkEntry(
            self.left,
            placeholder_text="Specialization"
        )
        self.specialization.pack(fill="x", padx=20, pady=5)

        # Qualification
        ctk.CTkLabel(
            self.left,
            text="Qualification"
        ).pack(anchor="w", padx=20)

        self.qualification = ctk.CTkEntry(
            self.left,
            placeholder_text="Qualification"
        )
        self.qualification.pack(fill="x", padx=20, pady=5)

        # Experience
        ctk.CTkLabel(
            self.left,
            text="Experience"
        ).pack(anchor="w", padx=20)

        self.experience = ctk.CTkEntry(
            self.left,
            placeholder_text="Years"
        )
        self.experience.pack(fill="x", padx=20, pady=5)

        # Mobile
        ctk.CTkLabel(
            self.left,
            text="Mobile"
        ).pack(anchor="w", padx=20)

        self.mobile = ctk.CTkEntry(
            self.left,
            placeholder_text="Mobile Number"
        )
        self.mobile.pack(fill="x", padx=20, pady=5)

        # Email
        ctk.CTkLabel(
            self.left,
            text="Email"
        ).pack(anchor="w", padx=20)

        self.email = ctk.CTkEntry(
            self.left,
            placeholder_text="Email Address"
        )
        self.email.pack(fill="x", padx=20, pady=5)

        # Consultation Fee
        ctk.CTkLabel(
            self.left,
            text="Consultation Fee"
        ).pack(anchor="w", padx=20)

        self.consultation_fee = ctk.CTkEntry(
            self.left,
            placeholder_text="Consultation Fee"
        )
        self.consultation_fee.pack(fill="x", padx=20, pady=5)

        # OPD Timing
        ctk.CTkLabel(
            self.left,
            text="OPD Timing"
        ).pack(anchor="w", padx=20)

        self.opd_timing = ctk.CTkComboBox(
            self.left,
            values=[
                "09:00 AM - 11:00 AM",
                "11:00 AM - 01:00 PM",
                "02:00 PM - 04:00 PM",
                "04:00 PM - 06:00 PM",
                "06:00 PM - 08:00 PM",
                "08:00 PM - 10:00 PM"
            ]
        )

        self.opd_timing.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.opd_timing.set("09:00 AM - 11:00 AM")
        # Available Days
        ctk.CTkLabel(
            self.left,
            text="Available Days"
        ).pack(anchor="w", padx=20)

        self.available_days = ctk.CTkComboBox(
            self.left,
            values=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
                "Monday - Friday",
                "Monday - Saturday",
                "All Days"
            ]
        )

        self.available_days.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.available_days.set("Monday - Friday")

        # Status
        ctk.CTkLabel(
            self.left,
            text="Status"
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Active",
                "Inactive"
            ]
        )
        self.status.pack(fill="x", padx=20, pady=5)
        self.gender.set("Male")

        self.department.set("General Medicine")

        self.status.set("Active")

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
           text="Add",
           width=150
        )
        self.add_btn.grid(row=0, column=0, padx=5, pady=5)

        self.update_btn = ctk.CTkButton(
            self.button_frame,
            text="Update"
        )
        self.update_btn.grid(row=0, column=1, padx=5, pady=5)

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete"
        )
        self.delete_btn.grid(row=1, column=0, padx=5, pady=5)

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear"
        )
        self.clear_btn.grid(row=1, column=1, padx=5, pady=5)
       
        # ==========================================
        # Doctor List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Doctor List",
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

        self.scroll_y = ctk.CTkScrollbar(
         self.table_frame,
          orientation="vertical"
)

        self.scroll_y.pack(
         side="right",
          fill="y"
)

        columns = (
            "ID",
            "Doctor ID",
            "Name",
            "Department",
            "Specialization",
            "Mobile",
            "Fee",
            "Status"
        )

        self.doctor_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.doctor_table.yview
        )

        for col in columns:
            self.doctor_table.heading(
                col,
                text=col
            )
            self.doctor_table.column(
                col,
                anchor="center",
                width=120
            )

        self.doctor_table.pack(
            fill="both",
            expand=True
        )