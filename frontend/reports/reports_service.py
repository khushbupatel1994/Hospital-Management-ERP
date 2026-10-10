"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Reports Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import datetime


class ReportsService:

    # ==========================================
    # Validate Report
    # ==========================================

    def validate_report(

        self,

        report_type,

        from_date,

        to_date,

        department,

        export_format

    ):

        if report_type.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Please select Report Type."
            )

            return False

        if from_date.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "From Date is required."
            )

            return False

        if to_date.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "To Date is required."
            )

            return False

        if department.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Please select Department."
            )

            return False

        if export_format.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Please select Export Format."
            )

            return False

        # Validate Date Format

        try:

            from_dt = datetime.strptime(
                from_date,
                "%d-%m-%Y"
            )

            to_dt = datetime.strptime(
                to_date,
                "%d-%m-%Y"
            )

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Date format should be DD-MM-YYYY."
            )

            return False

        # Check Date Range

        if from_dt > to_dt:

            messagebox.showerror(
                "Validation Error",
                "From Date cannot be greater than To Date."
            )

            return False

        return True