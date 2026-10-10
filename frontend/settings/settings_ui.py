"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings UI
Version : 4.0
===========================================================
"""

import os
import customtkinter as ctk
from PIL import Image


class SettingsUI:

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self, root):

        self.root = root

        # Keep image reference alive
        self.logo_image = None

        self.create_widgets()

    # =====================================================
    # CREATE WIDGETS
    # =====================================================

    def create_widgets(self):

        # =================================================
        # MAIN FRAME
        # =================================================

        self.main_frame = ctk.CTkFrame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # TITLE
        # =================================================

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="⚙ Hospital Settings",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.title_label.pack(
            pady=15
        )

        # =================================================
        # SCROLLABLE FORM
        # =================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=900,
            height=500
        )

        self.form_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        # =================================================
        # HOSPITAL NAME
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Hospital Name",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.hospital_name = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.hospital_name.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # PHONE
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Phone Number",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.phone = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.phone.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # EMAIL
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Email",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.email = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.email.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # ADDRESS
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Address",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.address = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.address.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # WEBSITE
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Website",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.website = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.website.grid(
            row=4,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # GST
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="GST Number",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=5,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.gst_number = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.gst_number.grid(
            row=5,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # CURRENCY
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Currency",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=6,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.currency = ctk.CTkComboBox(
            self.form_frame,
            values=[
                "INR",
                "USD",
                "EUR",
                "GBP"
            ],
            width=500,
            height=38
        )

        self.currency.grid(
            row=6,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.currency.set(
            "INR"
        )

        # =================================================
        # THEME
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Theme",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=7,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.theme = ctk.CTkComboBox(
            self.form_frame,
            values=[
                "Light",
                "Dark",
                "System"
            ],
            width=500,
            height=38
        )

        self.theme.grid(
            row=7,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.theme.set(
            "System"
        )

        # =================================================
        # HOSPITAL LOGO PATH
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Hospital Logo",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=8,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.logo_path = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=38
        )

        self.logo_path.grid(
            row=8,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # =================================================
        # BROWSE BUTTON
        # =================================================

        self.browse_btn = ctk.CTkButton(
            self.form_frame,
            text="📁 Browse",
            width=130,
            height=38
        )

        self.browse_btn.grid(
            row=8,
            column=2,
            padx=10,
            pady=10
        )

        # =================================================
        # LOGO PREVIEW TITLE
        # =================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Logo Preview",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=9,
            column=0,
            padx=10,
            pady=15,
            sticky="nw"
        )

        # =================================================
        # LOGO PREVIEW FRAME
        # =================================================

        self.logo_preview_frame = ctk.CTkFrame(
            self.form_frame,
            width=300,
            height=180,
            corner_radius=12
        )

        self.logo_preview_frame.grid(
            row=9,
            column=1,
            columnspan=2,
            padx=10,
            pady=15,
            sticky="w"
        )

        self.logo_preview_frame.grid_propagate(
            False
        )

        # =================================================
        # LOGO PREVIEW LABEL
        # =================================================

        self.logo_preview = ctk.CTkLabel(
            self.logo_preview_frame,
            text="No Logo Selected",
            font=ctk.CTkFont(
                size=16
            )
        )

        self.logo_preview.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =================================================
        # STATUS LABEL
        # =================================================

        self.logo_status = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=ctk.CTkFont(
                size=12
            )
        )

        self.logo_status.grid(
            row=10,
            column=1,
            columnspan=2,
            padx=10,
            pady=(0, 15),
            sticky="w"
        )

        # =================================================
        # CONFIGURE GRID
        # =================================================

        self.form_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =================================================
        # BUTTON FRAME
        # =================================================

        self.button_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.button_frame.pack(
            side="bottom",
            pady=10
        )

        # =================================================
        # SAVE BUTTON
        # =================================================

        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="💾 Save Settings",
            width=180,
            height=42
        )

        self.save_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        # =================================================
        # RESET BUTTON
        # =================================================

        self.reset_btn = ctk.CTkButton(
            self.button_frame,
            text="🔄 Reset",
            width=180,
            height=42
        )

        self.reset_btn.grid(
            row=0,
            column=1,
            padx=10
        )

    # =====================================================
    # UPDATE LOGO PREVIEW
    # =====================================================

    def update_logo_preview(
        self,
        image_path
    ):

        try:

            if not image_path:

                self.logo_image = None

                self.logo_preview.configure(
                    image=None,
                    text="No Logo Selected"
                )

                self.logo_status.configure(
                    text=""
                )

                return

            # -------------------------------------------------
            # Normalize Path
            # -------------------------------------------------

            image_path = os.path.normpath(
                image_path
            )

            # -------------------------------------------------
            # Check File
            # -------------------------------------------------

            if not os.path.isfile(
                image_path
            ):

                self.logo_image = None

                self.logo_preview.configure(
                    image=None,
                    text="Logo File Not Found"
                )

                self.logo_status.configure(
                    text="Invalid logo path"
                )

                print(
                    "❌ Logo File Not Found:",
                    image_path
                )

                return

            # -------------------------------------------------
            # Open Image
            # -------------------------------------------------

            image = Image.open(
                image_path
            )

            # -------------------------------------------------
            # Convert Image
            # -------------------------------------------------

            image = image.convert(
                "RGBA"
            )

            # -------------------------------------------------
            # Create CTkImage
            # -------------------------------------------------

            self.logo_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(220, 130)
            )

            # -------------------------------------------------
            # Show Image
            # -------------------------------------------------

            self.logo_preview.configure(
                image=self.logo_image,
                text=""
            )

            self.logo_status.configure(
                text="✅ Logo loaded successfully"
            )

            print(
                "✅ Logo Preview Updated:",
                image_path
            )

        except Exception as e:

            self.logo_image = None

            self.logo_preview.configure(
                image=None,
                text="Unable to Load Logo"
            )

            self.logo_status.configure(
                text="Invalid or unsupported image"
            )

            print(
                "❌ Logo Preview Error:",
                e
            )