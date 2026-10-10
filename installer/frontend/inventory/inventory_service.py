"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Inventory Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class InventoryService:

    # ==========================================
    # Validate Inventory Item
    # ==========================================

    def validate_item(

        self,

        item_name,

        category,

        supplier,

        purchase_price,

        selling_price,

        stock_quantity,

        minimum_stock,

        gst

    ):

        if item_name.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Item Name is required."
            )

            return False

        if category.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Category is required."
            )

            return False

        if supplier.strip() == "":

            messagebox.showerror(
                "Validation Error",
                "Supplier is required."
            )

            return False

        try:

            purchase_price = float(purchase_price)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Purchase Price must be numeric."
            )

            return False

        try:

            selling_price = float(selling_price)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Selling Price must be numeric."
            )

            return False

        try:

            stock_quantity = int(stock_quantity)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Stock Quantity must be an integer."
            )

            return False

        try:

            minimum_stock = int(minimum_stock)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Minimum Stock must be an integer."
            )

            return False

        try:

            gst = float(gst)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "GST must be numeric."
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

        if minimum_stock < 0:

            messagebox.showerror(
                "Validation Error",
                "Minimum Stock cannot be negative."
            )

            return False

        if gst < 0:

            messagebox.showerror(
                "Validation Error",
                "GST cannot be negative."
            )

            return False

        return True