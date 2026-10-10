"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : User Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk


class UserUI:

    def __init__(self, root):
        self.root = root

        # अगर root Window है तभी title सेट करें
        if hasattr(self.root, "title"):
            self.root.title("User Management")

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

        # ==============================
        # Header
        # ==============================

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
            text="👥 User Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

        # ==============================
        # Search Area
        # ==============================

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
            placeholder_text="Search User..."
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

        # ==============================
        # Body
        # ==============================

        self.body = ctk.CTkFrame(
            self.main
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Left Form
        self.left = ctk.CTkScrollableFrame(
          self.body,
          width=420,
          corner_radius=10
)
        self.left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        # USER FORM

        ctk.CTkLabel(
       self.left,
         text="User Information",
        font=("Segoe UI", 20, "bold")
       ).pack(pady=15)

        # Employee ID
        ctk.CTkLabel(self.left, text="Employee ID").pack(anchor="w", padx=20)

        self.employee_id = ctk.CTkEntry(
         self.left,
       placeholder_text="Employee ID"
)
        self.employee_id.pack(fill="x", padx=20, pady=5)
        # Full Name
        ctk.CTkLabel(self.left, text="Full Name").pack(anchor="w", padx=20)

        self.full_name = ctk.CTkEntry(
         self.left,
        placeholder_text="Full Name"
)
        self.full_name.pack(fill="x", padx=20, pady=5)

          # Username
        ctk.CTkLabel(self.left, text="Username").pack(anchor="w", padx=20)
        self.username = ctk.CTkEntry(
          self.left,
           placeholder_text="Username"
)
        self.username.pack(fill="x", padx=20, pady=5)

        # Password
        ctk.CTkLabel(self.left, text="Password").pack(anchor="w", padx=20)
        self.password = ctk.CTkEntry(
         self.left,
          placeholder_text="Password",
          show="*"
)
        self.password.pack(fill="x", padx=20, pady=5)

        # Role
        ctk.CTkLabel(self.left, text="Role").pack(anchor="w", padx=20)

        self.role = ctk.CTkComboBox(
          self.left,
             values=[
                "Super Admin",
                "Admin",
                "Doctor",
                "Nurse",
                "Receptionist",
                "Accountant",
                "Pharmacist",
                "Lab Technician",
                "HR",
                "Inventory Manager"
            ]
        )
        self.role.pack(fill="x", padx=20, pady=5)

        # Department
        ctk.CTkLabel(self.left, text="Department").pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
           self.left,
              values=[
                  "Administration",
                  "OPD",
                  "IPD",
                  "Billing",
                  "Pharmacy",
                  "Laboratory",
                  "Accounts"
              ]
)
        self.department.pack(fill="x", padx=20, pady=5)

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

        # ==========================================
        # Security Question
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Security Question"
        ).pack(
            anchor="w",
            padx=20
        )

        self.security_question = ctk.CTkComboBox(
            self.left,
            values=[
                "What is your favourite color?",
                "What is your birthplace?",
                "What is your first school name?",
                "What is your favourite food?"
            ]
        )

        self.security_question.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Security Answer
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Security Answer"
        ).pack(
            anchor="w",
            padx=20
        )

        self.security_answer = ctk.CTkEntry(
            self.left,
            placeholder_text="Security Answer"
        )

        self.security_answer.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Status
        ctk.CTkLabel(self.left, text="Status").pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Active",
                "Inactive"
            ]
        )
        self.status.pack(fill="x", padx=20, pady=5)

        # ==========================================
        # BUTTONS
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
        # USER LIST
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="User List",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self.right)

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Scrollbar
        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # Treeview
        columns = (
            "ID",
            "Employee ID",
            "Full Name",
            "Username",
            "Role",
            "Department",
            "Mobile",
            "Status"
        )

        self.user_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.user_table.yview
        )

        for col in columns:

            self.user_table.heading(
                col,
                text=col
            )

            self.user_table.column(
                col,
                anchor="center",
                width=120
            )

        self.user_table.pack(
            fill="both",
            expand=True
        )