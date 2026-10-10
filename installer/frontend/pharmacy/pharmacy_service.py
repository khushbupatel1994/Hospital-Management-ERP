"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Pharmacy Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class PharmacyService:

    # ==========================================
    # Validate Medicine
    # ==========================================

    def validate_medicine(

        self,

        medicine_name,

        company_name,

        batch_no,

        purchase_price,

        selling_price,

        stock_quantity

    ):

        if medicine_name.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Medicine Name is required."
            )

            return False

        if company_name.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Company Name is required."
            )

            return False

        if batch_no.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Batch Number is required."
            )

            return False

        try:

            purchase_price = float(purchase_price)

            selling_price = float(selling_price)

            stock_quantity = int(stock_quantity)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Purchase Price, Selling Price and Stock Quantity must be numeric."
            )

            return False

        if purchase_price < 0:

            messagebox.showerror(
                "Validation Error",
                "Purchase Price cannot be negative."
            )

            return False

        if selling_price < 0:

            messagebox.showerror(
                "Validation Error",
                "Selling Price cannot be negative."
            )

            return False

        if stock_quantity < 0:

            messagebox.showerror(
                "Validation Error",
                "Stock Quantity cannot be negative."
            )

            return False

        return True