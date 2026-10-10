"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Doctor Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class DoctorService:

    def validate_doctor(
        self,
        full_name,
        department,
        specialization,
        mobile,
        email,
        experience,
        consultation_fee
    ):

        if full_name == "":

            messagebox.showerror(
                "Validation",
                "Doctor Name is required."
            )

            return False

        if department == "":

            messagebox.showerror(
                "Validation",
                "Department is required."
            )

            return False

        if specialization == "":

            messagebox.showerror(
                "Validation",
                "Specialization is required."
            )

            return False

        if mobile == "":

            messagebox.showerror(
                "Validation",
                "Mobile Number is required."
            )

            return False

        if len(mobile) != 10 or not mobile.isdigit():

            messagebox.showerror(
                "Validation",
                "Invalid Mobile Number."
            )

            return False

        if email != "" and "@" not in email:

            messagebox.showerror(
                "Validation",
                "Invalid Email Address."
            )

            return False

        if experience != "":

            if not experience.isdigit():

                messagebox.showerror(
                    "Validation",
                    "Experience must be numeric."
                )

                return False

        if consultation_fee != "":

            try:
                float(consultation_fee)
            except ValueError:

                messagebox.showerror(
                    "Validation",
                    "Invalid Consultation Fee."
                )

                return False

        return True