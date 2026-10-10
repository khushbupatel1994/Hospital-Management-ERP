"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Patient Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry


class PatientUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Main UI
    # ==========================================

    def create_widgets(self):

        # Main Container
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
            text="🧑 Patient Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

        # Search Frame
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
            placeholder_text="Search Patient..."
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

        # Left Form
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

        # ==========================================
        # Patient Form
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Patient Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # Patient ID
        ctk.CTkLabel(self.left, text="Patient ID").pack(anchor="w", padx=20)

        self.patient_id = ctk.CTkEntry(
          self.left,
          placeholder_text="Auto Generated",
          state="disabled"
        )
        self.patient_id.pack(fill="x", padx=20, pady=5)

        # Registration No
        ctk.CTkLabel(self.left, text="Registration No").pack(anchor="w", padx=20)

        self.registration_no = ctk.CTkEntry(
           self.left,
            placeholder_text="Registration No",
            state="disabled"
        )
        self.registration_no.pack(fill="x", padx=20, pady=5)

        # Patient Name
        ctk.CTkLabel(self.left, text="Patient Name").pack(anchor="w", padx=20)

        self.patient_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Patient Name"
        )
        self.patient_name.pack(fill="x", padx=20, pady=5)

        # Gender
        ctk.CTkLabel(self.left, text="Gender").pack(anchor="w", padx=20)

        self.gender = ctk.CTkComboBox(
            self.left,
            values=[
                "Male",
                "Female",
                "Other"
            ]
        )
        self.gender.pack(fill="x", padx=20, pady=5)

        # DOB
        ctk.CTkLabel(self.left, text="Date of Birth").pack(anchor="w", padx=20)

        self.dob = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            width=20
        )

        self.dob.pack(
            fill="x",
            padx=20,
            pady=5
        )
        # Age
        ctk.CTkLabel(self.left, text="Age").pack(anchor="w", padx=20)

        self.age = ctk.CTkEntry(
            self.left,
            placeholder_text="Auto Age",
            state="readonly"
        )
        self.age.pack(fill="x", padx=20, pady=5)

        # Blood Group
        ctk.CTkLabel(self.left, text="Blood Group").pack(anchor="w", padx=20)

        self.blood_group = ctk.CTkComboBox(
            self.left,
            values=[
                "A+","A-",
                "B+","B-",
                "AB+","AB-",
                "O+","O-"
            ]
        )
        self.blood_group.pack(fill="x", padx=20, pady=5)

        # Mobile
        ctk.CTkLabel(self.left, text="Mobile").pack(anchor="w", padx=20)

        self.mobile = ctk.CTkEntry(
            self.left,
            placeholder_text="Mobile Number"
        )
        self.mobile.pack(fill="x", padx=20, pady=5)

        # Email
        ctk.CTkLabel(self.left, text="Email").pack(anchor="w", padx=20)

        self.email = ctk.CTkEntry(
            self.left,
            placeholder_text="Email Address"
        )
        self.email.pack(fill="x", padx=20, pady=5)

        # Address
        ctk.CTkLabel(self.left, text="Address").pack(anchor="w", padx=20)

        self.address = ctk.CTkTextbox(
            self.left,
            height=80
        )
        self.address.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # City
        # ==========================================

        ctk.CTkLabel(self.left, text="City").pack(anchor="w", padx=20)

        self.city = ctk.CTkEntry(
            self.left,
            placeholder_text="City"
        )
        self.city.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # State
        # ==========================================

        ctk.CTkLabel(self.left, text="State").pack(anchor="w", padx=20)

        self.state = ctk.CTkEntry(
            self.left,
            placeholder_text="State"
        )
        self.state.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # PIN Code
        # ==========================================

        ctk.CTkLabel(self.left, text="PIN Code").pack(anchor="w", padx=20)

        self.pin_code = ctk.CTkEntry(
            self.left,
            placeholder_text="PIN Code"
        )
        self.pin_code.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # Aadhaar
        # ==========================================

        ctk.CTkLabel(self.left, text="Aadhaar Number").pack(anchor="w", padx=20)

        self.aadhaar = ctk.CTkEntry(
            self.left,
            placeholder_text="Aadhaar Number"
        )
        self.aadhaar.pack(fill="x", padx=20, pady=5)
        # ==========================================
        # Doctor
        # ==========================================

        ctk.CTkLabel(self.left, text="Doctor").pack(anchor="w", padx=20)

        self.doctor = ctk.CTkComboBox(
            self.left,
            values=[
                "Select Doctor"
            ]
        )
        self.doctor.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # Department
        # ==========================================

        ctk.CTkLabel(self.left, text="Department").pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            values=[
                "General Medicine",
                "Cardiology",
                "Orthopedics",
                "Neurology",
                "Pediatrics",
                "Gynecology",
                "ENT",
                "Dermatology"
            ]
        )
        self.department.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # Patient Type
        # ==========================================

        ctk.CTkLabel(self.left, text="Patient Type").pack(anchor="w", padx=20)

        self.patient_type = ctk.CTkComboBox(
            self.left,
            values=[
                "OPD",
                "IPD",
                "Emergency"
            ]
        )
        self.patient_type.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # Status
        # ==========================================

        ctk.CTkLabel(self.left, text="Status").pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Active",
                "Discharged"
            ]
        )
        self.status.pack(fill="x", padx=20, pady=5)
        # ==========================================
# Patient Photo
# ==========================================

        ctk.CTkLabel(
         self.left,
         text="Patient Photo"
        ).pack(anchor="w", padx=20)

        self.photo_label = ctk.CTkLabel(
          self.left,
          text="No Photo",
          width=120,
          height=140
        )

        self.photo_label.pack(
          padx=20,
          pady=5
        )

        self.photo_btn = ctk.CTkButton(
          self.left,
          text="Upload Photo"
        )

        self.photo_btn.pack(
          padx=20,
          pady=5
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
            pady=20
        )

        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Add"
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

        # Right Table
        self.right = ctk.CTkFrame(
            self.body
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # Patient List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Patient List",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # Table Frame
        self.table_frame = ctk.CTkFrame(
            self.right
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Vertical Scrollbar
        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # Columns
        columns = (
            "ID",
            "Patient ID",
            "Registration No",
            "Patient Name",
            "Gender",
            "Age",
            "Mobile",
            "Doctor",
            "Department",
            "Status"
        )

        # Treeview
        self.patient_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.patient_table.yview
        )

        # Headings
        for col in columns:

            self.patient_table.heading(
                col,
                text=col
            )

            self.patient_table.column(
                col,
                width=130,
                anchor="center"
            )

        self.patient_table.pack(
            fill="both",
            expand=True
        )