"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Login Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class LoginService:
    """
    Handles login validation and business logic.
    """

    @staticmethod
    def validate_input(username: str, password: str) -> bool:
        """
        Validate username and password fields.
        """

        username = username.strip()
        password = password.strip()

        if username == "":
            messagebox.showwarning(
                "Validation",
                "Please enter Username."
            )
            return False

        if password == "":
            messagebox.showwarning(
                "Validation",
                "Please enter Password."
            )
            return False

        return True