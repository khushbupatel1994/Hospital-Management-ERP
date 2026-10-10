"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings Service
Version : 3.0
===========================================================
"""

import re

from tkinter import messagebox


class SettingsService:

    # ==========================================
    # Validate Settings
    # ==========================================

    def validate_settings(

        self,

        hospital_name,

        phone,

        email

    ):

        if hospital_name.strip() == "":

            messagebox.showerror(

                "Validation Error",

                "Hospital Name is required."

            )

            return False

        if phone.strip() == "":

            messagebox.showerror(

                "Validation Error",

                "Phone Number is required."

            )

            return False

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showerror(

                "Validation Error",

                "Enter a valid 10-digit Phone Number."

            )

            return False

        if email.strip() == "":

            messagebox.showerror(

                "Validation Error",

                "Email is required."

            )

            return False

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, email):

            messagebox.showerror(

                "Validation Error",

                "Invalid Email Address."

            )

            return False

        return True