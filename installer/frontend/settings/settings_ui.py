"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings UI
Version : 3.0
===========================================================
"""

import customtkinter as ctk


class SettingsUI:

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
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(

            self.main_frame,

            text="Hospital Settings",

            font=("Arial", 24, "bold")

        )

        self.title_label.pack(
            pady=15
        )

        # ==========================================
        # Settings Form
        # ==========================================

        self.form_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=700,
            height=280
        )
        self.form_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Hospital Name

        ctk.CTkLabel(
            self.form_frame,
            text="Hospital Name"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.hospital_name = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.hospital_name.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Phone

        ctk.CTkLabel(
            self.form_frame,
            text="Phone Number"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.phone = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.phone.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Email

        ctk.CTkLabel(
            self.form_frame,
            text="Email"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.email = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.email.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # ==========================================
        # Address
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="Address"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.address = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.address.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )

        # ==========================================
        # Website
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="Website"
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.website = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.website.grid(
            row=4,
            column=1,
            padx=10,
            pady=10
        )

        # ==========================================
        # GST Number
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="GST Number"
        ).grid(
            row=5,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.gst_number = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.gst_number.grid(
            row=5,
            column=1,
            padx=10,
            pady=10
        )

        # ==========================================
        # Currency
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="Currency"
        ).grid(
            row=6,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.currency = ctk.CTkComboBox(
            self.form_frame,
            values=["INR", "USD", "EUR"]
        )

        self.currency.grid(
            row=6,
            column=1,
            padx=10,
            pady=10
        )

        self.currency.set("INR")

        # ==========================================
        # Theme
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="Theme"
        ).grid(
            row=7,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.theme = ctk.CTkComboBox(
            self.form_frame,
            values=["Light", "Dark", "System"]
        )

        self.theme.grid(
            row=7,
            column=1,
            padx=10,
            pady=10
        )

        self.theme.set("System")

        # ==========================================
        # Logo Path
        # ==========================================

        ctk.CTkLabel(
            self.form_frame,
            text="Hospital Logo"
        ).grid(
            row=8,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.logo_path = ctk.CTkEntry(
            self.form_frame,
            width=300
        )

        self.logo_path.grid(
            row=8,
            column=1,
            padx=10,
            pady=10
        )

        self.browse_btn = ctk.CTkButton(
            self.form_frame,
            text="Browse"
        )

        self.browse_btn.grid(
            row=8,
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
            side="bottom",
            pady=10
        )

        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Settings",
            width=180
        )

        self.save_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        self.reset_btn = ctk.CTkButton(
            self.button_frame,
            text="Reset",
            width=180
        )

        self.reset_btn.grid(
            row=0,
            column=1,
            padx=10
        )