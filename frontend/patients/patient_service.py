"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Patient Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox
import re


class PatientService:

    # ==========================================
    # Validate Patient
    # ==========================================

    def validate_patient(
        self,
        patient_name,
        gender,
        age,
        mobile,
        email,
        doctor,
        department
    ):

        # Patient Name
        if patient_name == "":

            messagebox.showerror(
                "Validation",
                "Patient Name is required."
            )

            return False

        # Gender
        if gender == "":

            messagebox.showerror(
                "Validation",
                "Please select Gender."
            )

            return False

        # Age
        if age == "":

            messagebox.showerror(
                "Validation",
                "Age is required."
            )

            return False

        if not age.isdigit():

            messagebox.showerror(
                "Validation",
                "Age must be numeric."
            )

            return False

        # Mobile
        if not re.fullmatch(r"[6-9]\d{9}", mobile):

            messagebox.showerror(
                "Validation",
                "Invalid Mobile Number."
            )

            return False

        # Email
        if email:

            if not re.fullmatch(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                email
            ):

                messagebox.showerror(
                    "Validation",
                    "Invalid Email Address."
                )

                return False

        # Doctor
        if doctor == "Select Doctor":

            messagebox.showerror(
                "Validation",
                "Please select Doctor."
            )

            return False

        # Department
        if department == "":

            messagebox.showerror(
                "Validation",
                "Please select Department."
            )

            return False

        return True

    