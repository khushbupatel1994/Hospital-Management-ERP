"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : User Service
Version : 2.0
===========================================================
"""

import re
from tkinter import messagebox


class UserService:

    # ==========================================
    # Validate User Form
    # ==========================================

    def validate_user(
        self,
        employee_id,
        full_name,
        username,
        password,
        role,
        department,
        mobile,
        email
    ):

        # Empty Validation
        if (
            employee_id == "" or
            full_name == "" or
            username == "" or
            password == "" or
            role == "" or
            department == "" or
            mobile == "" or
            email == ""
        ):

            messagebox.showerror(
                "Validation Error",
                "All fields are required."
            )

            return False

        # Mobile Validation
        if not mobile.isdigit() or len(mobile) != 10:

            messagebox.showerror(
                "Validation Error",
                "Mobile number must be 10 digits."
            )

            return False

        # Email Validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):

            messagebox.showerror(
                "Validation Error",
                "Invalid email address."
            )

            return False

        # Password Length
        if len(password) < 6:

            messagebox.showerror(
                "Validation Error",
                "Password must be at least 6 characters."
            )

            return False

        return True
    