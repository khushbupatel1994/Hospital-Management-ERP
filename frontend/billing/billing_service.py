"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Billing Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class BillingService:

    # ==========================================
    # Validate Bill
    # ==========================================

    def validate_bill(

        self,

        patient,

        doctor,

        bill_date,

        total_amount

    ):

        if patient == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a patient."
            )

            return False

        if doctor == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a doctor."
            )

            return False

        if bill_date == "":

            messagebox.showerror(
                "Validation Error",
                "Bill Date is required."
            )

            return False

        if total_amount == "":

            messagebox.showerror(
                "Validation Error",
                "Total Amount is required."
            )

            return False

        try:

            if float(total_amount) < 0:

                messagebox.showerror(
                    "Validation Error",
                    "Total Amount cannot be negative."
                )

                return False

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Total Amount must be a valid number."
            )

            return False

        return True