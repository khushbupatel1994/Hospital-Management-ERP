"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings Controller
Version : 3.0
===========================================================
"""

from tkinter import filedialog, messagebox

from frontend.settings.settings_ui import SettingsUI
from frontend.settings.settings_service import SettingsService
from frontend.settings.settings_crud import SettingsCRUD


class Settings(SettingsUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = SettingsService()

        self.crud = SettingsCRUD()

        self.bind_events()

        self.load_settings()


    # ==========================================
    # Bind Events
    # ==========================================

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

    # ==========================================
    # Browse Logo
    # ==========================================

    def browse_logo(self):

        filename = filedialog.askopenfilename(

            title="Select Hospital Logo",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]

        )

        if filename:

            self.logo_path.delete(0, "end")

            self.logo_path.insert(0, filename)

    # ==========================================
    # Save Settings
    # ==========================================

    def save_settings(self):

        hospital_name = self.hospital_name.get().strip()

        phone = self.phone.get().strip()

        email = self.email.get().strip()

        if not self.service.validate_settings(
            hospital_name,
            phone,
            email
        ):
            return

        success = self.crud.save_settings(
            hospital_name,
            self.address.get().strip(),
            "",
            "",
            "",
            phone,
            email,
            self.website.get().strip(),
            self.gst_number.get().strip(),
            self.currency.get(),
            "",
            self.logo_path.get().strip(),
            self.theme.get()
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Settings saved successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to save settings."
            )

    # ==========================================
    # Reset Form
    # ==========================================

    def reset_form(self):

        self.hospital_name.delete(0, "end")

        self.phone.delete(0, "end")

        self.email.delete(0, "end")

        self.address.delete(0, "end")

        self.website.delete(0, "end")

        self.gst_number.delete(0, "end")

        self.logo_path.delete(0, "end")

        self.currency.set("INR")

        self.theme.set("System")

    # ==========================================
    # Load Settings
    # ==========================================

    def load_settings(self):

        data = self.crud.load_settings()

        if not data:

            return

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

        self.hospital_name.delete(0, "end")
        self.hospital_name.insert(0, hospital_name or "")

        self.address.delete(0, "end")
        self.address.insert(0, address or "")

        self.phone.delete(0, "end")
        self.phone.insert(0, phone or "")

        self.email.delete(0, "end")
        self.email.insert(0, email or "")

        self.website.delete(0, "end")
        self.website.insert(0, website or "")

        self.gst_number.delete(0, "end")
        self.gst_number.insert(0, gst_number or "")

        self.logo_path.delete(0, "end")
        self.logo_path.insert(0, logo_path or "")

        self.currency.set(currency or "INR")

        self.theme.set(theme or "System")