"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : IPD Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class IPDService:

    # ==========================================
    # Validate Admission
    # ==========================================

    def validate_admission(
        self,
        patient,
        doctor,
        ward,
        bed_no,
        admission_date,
        daily_charges,
    ):

        if patient.strip() == "":
            messagebox.showerror(
                "Validation Error",
                "Patient is required."
            )
            return False

        if doctor.strip() == "":
            messagebox.showerror(
                "Validation Error",
                "Doctor is required."
            )
            return False

        if ward.strip() == "":
            messagebox.showerror(
                "Validation Error",
                "Ward is required."
            )
            return False

        if bed_no.strip() == "":
            messagebox.showerror(
                "Validation Error",
                "Bed Number is required."
            )
            return False

        try:
            daily_charges = float(daily_charges)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Daily Charges must be numeric."
            )
            return False

        if admission_date.strip() == "":
            messagebox.showerror(
                "Validation Error",
                "Admission Date is required."
            )
            return False

        if daily_charges < 0:
            messagebox.showerror(
                "Validation Error",
                "Daily Charges cannot be negative."
            )
            return False

        return True