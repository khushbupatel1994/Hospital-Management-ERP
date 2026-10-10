"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class LaboratoryService:

    # ==========================================
    # Validate Laboratory Test
    # ==========================================

    def validate_test(

        self,

        test_name,

        department,

        patient,

        doctor,

        test_fee

    ):

        if test_name.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Test Name is required."
            )

            return False

        if department.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Department is required."
            )

            return False

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

        try:

            test_fee = float(test_fee)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Test Fee must be numeric."
            )

            return False

        if test_fee < 0:

            messagebox.showerror(
                "Validation Error",
                "Test Fee cannot be negative."
            )

            return False

        return True