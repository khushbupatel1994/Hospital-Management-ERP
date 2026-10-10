"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings Controller
Version : 4.0
===========================================================
"""

import os

import customtkinter as ctk

from tkinter import (
    filedialog,
    messagebox
)

from frontend.settings.settings_ui import (
    SettingsUI
)

from frontend.settings.settings_service import (
    SettingsService
)

from frontend.settings.settings_crud import (
    SettingsCRUD
)


class Settings(SettingsUI):

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self, root):

        super().__init__(
            root
        )

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        self.service = SettingsService()

        self.crud = SettingsCRUD()

        # -------------------------------------------------
        # Events
        # -------------------------------------------------

        self.bind_events()

        # -------------------------------------------------
        # Load Database Settings
        # -------------------------------------------------

        self.load_settings()

    # =====================================================
    # BIND EVENTS
    # =====================================================

    def bind_events(self):

        self.save_btn.configure(
            command=self.save_settings
        )

        self.reset_btn.configure(
            command=self.reset_form
        )

        self.browse_btn.configure(
            command=self.browse_logo
        )

    # =====================================================
    # BROWSE LOGO
    # =====================================================

    def browse_logo(self):

        filename = filedialog.askopenfilename(

            parent=self.root,

            title="Select Hospital Logo",

            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.webp *.bmp"
                ),
                (
                    "PNG Files",
                    "*.png"
                ),
                (
                    "JPG Files",
                    "*.jpg *.jpeg"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not filename:

            return

        # -------------------------------------------------
        # Normalize Path
        # -------------------------------------------------

        filename = os.path.normpath(
            filename
        )

        # -------------------------------------------------
        # Put Path in Entry
        # -------------------------------------------------

        self.logo_path.delete(
            0,
            "end"
        )

        self.logo_path.insert(
            0,
            filename
        )

        # -------------------------------------------------
        # Update Preview Immediately
        # -------------------------------------------------

        self.update_logo_preview(
            filename
        )

        print(
            "Hospital Logo Selected:",
            filename
        )

    # =====================================================
    # APPLY THEME
    # =====================================================

    def apply_theme(
        self,
        theme
    ):

        try:

            if not theme:

                theme = "System"

            theme = str(
                theme
            ).strip()

            if theme.lower() == "dark":

                ctk.set_appearance_mode(
                    "Dark"
                )

                print(
                    "🎨 Theme Applied: Dark"
                )

            elif theme.lower() == "light":

                ctk.set_appearance_mode(
                    "Light"
                )

                print(
                    "🎨 Theme Applied: Light"
                )

            else:

                ctk.set_appearance_mode(
                    "System"
                )

                print(
                    "🎨 Theme Applied: System"
                )

        except Exception as e:

            print(
                "❌ Theme Apply Error:",
                e
            )

    # =====================================================
    # SAVE SETTINGS
    # =====================================================

    def save_settings(self):

        # -------------------------------------------------
        # Read Values
        # -------------------------------------------------

        hospital_name = (
            self.hospital_name
            .get()
            .strip()
        )

        phone = (
            self.phone
            .get()
            .strip()
        )

        email = (
            self.email
            .get()
            .strip()
        )

        address = (
            self.address
            .get()
            .strip()
        )

        website = (
            self.website
            .get()
            .strip()
        )

        gst_number = (
            self.gst_number
            .get()
            .strip()
        )

        currency = (
            self.currency
            .get()
            .strip()
        )

        logo_path = (
            self.logo_path
            .get()
            .strip()
        )

        theme = (
            self.theme
            .get()
            .strip()
        )

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not self.service.validate_settings(
            hospital_name,
            phone,
            email
        ):

            return

        # -------------------------------------------------
        # Save Database
        # -------------------------------------------------

        success = self.crud.save_settings(

            hospital_name,

            address,

            "",

            "",

            "",

            phone,

            email,

            website,

            gst_number,

            currency,

            "",

            logo_path,

            theme
        )

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        if success:

            # Apply theme
            self.apply_theme(
                theme
            )

            # Update preview
            self.update_logo_preview(
                logo_path
            )

            messagebox.showinfo(

                "Success",

                "Settings saved successfully.",

                parent=self.root
            )

            print(
                "✅ Settings Saved Successfully"
            )

        # -------------------------------------------------
        # Failed
        # -------------------------------------------------

        else:

            messagebox.showerror(

                "Error",

                "Failed to save settings.",

                parent=self.root
            )

            print(
                "❌ Settings Save Failed"
            )

    # =====================================================
    # RESET FORM
    # =====================================================

    def reset_form(self):

        # -------------------------------------------------
        # Hospital
        # -------------------------------------------------

        self.hospital_name.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Phone
        # -------------------------------------------------

        self.phone.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Email
        # -------------------------------------------------

        self.email.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Address
        # -------------------------------------------------

        self.address.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Website
        # -------------------------------------------------

        self.website.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # GST
        # -------------------------------------------------

        self.gst_number.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Logo Path
        # -------------------------------------------------

        self.logo_path.delete(
            0,
            "end"
        )

        # -------------------------------------------------
        # Currency
        # -------------------------------------------------

        self.currency.set(
            "INR"
        )

        # -------------------------------------------------
        # Theme
        # -------------------------------------------------

        self.theme.set(
            "System"
        )

        self.apply_theme(
            "System"
        )

        # -------------------------------------------------
        # Clear Preview
        # -------------------------------------------------

        self.logo_image = None

        self.logo_preview.configure(
            image=None,
            text="No Logo Selected"
        )

        self.logo_status.configure(
            text=""
        )

        print(
            "🔄 Settings Form Reset"
        )

    # =====================================================
    # LOAD SETTINGS
    # =====================================================

    def load_settings(self):

        try:

            data = self.crud.load_settings()

            # -------------------------------------------------
            # No Data
            # -------------------------------------------------

            if not data:

                print(
                    "ℹ No saved settings found."
                )

                self.apply_theme(
                    "System"
                )

                return

            # -------------------------------------------------
            # Unpack Database Data
            # -------------------------------------------------

            (
                hospital_name,
                address,
                city,
                state,
                pincode,
                phone,
                email,
                website,
                gst_number,
                currency,
                invoice_footer,
                logo_path,
                theme
            ) = data

            # -------------------------------------------------
            # Hospital Name
            # -------------------------------------------------

            self.hospital_name.delete(
                0,
                "end"
            )

            self.hospital_name.insert(
                0,
                hospital_name or ""
            )

            # -------------------------------------------------
            # Address
            # -------------------------------------------------

            self.address.delete(
                0,
                "end"
            )

            self.address.insert(
                0,
                address or ""
            )

            # -------------------------------------------------
            # Phone
            # -------------------------------------------------

            self.phone.delete(
                0,
                "end"
            )

            self.phone.insert(
                0,
                phone or ""
            )

            # -------------------------------------------------
            # Email
            # -------------------------------------------------

            self.email.delete(
                0,
                "end"
            )

            self.email.insert(
                0,
                email or ""
            )

            # -------------------------------------------------
            # Website
            # -------------------------------------------------

            self.website.delete(
                0,
                "end"
            )

            self.website.insert(
                0,
                website or ""
            )

            # -------------------------------------------------
            # GST
            # -------------------------------------------------

            self.gst_number.delete(
                0,
                "end"
            )

            self.gst_number.insert(
                0,
                gst_number or ""
            )

            # -------------------------------------------------
            # Logo Path
            # -------------------------------------------------

            self.logo_path.delete(
                0,
                "end"
            )

            self.logo_path.insert(
                0,
                logo_path or ""
            )

            # -------------------------------------------------
            # Currency
            # -------------------------------------------------

            self.currency.set(
                currency or "INR"
            )

            # -------------------------------------------------
            # Theme
            # -------------------------------------------------

            saved_theme = (
                theme or "System"
            )

            self.theme.set(
                saved_theme
            )

            # -------------------------------------------------
            # Apply Theme
            # -------------------------------------------------

            self.apply_theme(
                saved_theme
            )

            # -------------------------------------------------
            # Load Logo Preview
            # -------------------------------------------------

            if logo_path:

                self.update_logo_preview(
                    logo_path
                )

            else:

                self.update_logo_preview(
                    None
                )

            print(
                "✅ Settings Loaded Successfully"
            )

        except Exception as e:

            print(
                "❌ Load Settings Error:",
                e
            )

            self.apply_theme(
                "System"
            )

            self.update_logo_preview(
                None
            )