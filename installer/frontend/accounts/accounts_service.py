"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Accounts Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class AccountsService:

    # ==========================================
    # Validate Transaction
    # ==========================================

    def validate_transaction(

        self,

        transaction_type,

        category,

        amount,

        payment_mode,

        transaction_date

    ):

        if transaction_type.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Transaction Type is required."
            )

            return False

        if category.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Category is required."
            )

            return False

        if payment_mode.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Payment Mode is required."
            )

            return False

        if transaction_date.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Transaction Date is required."
            )

            return False

        try:

            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Amount must be numeric."
            )

            return False

        if amount <= 0:

            messagebox.showerror(
                "Validation Error",
                "Amount must be greater than zero."
            )

            return False

        return True