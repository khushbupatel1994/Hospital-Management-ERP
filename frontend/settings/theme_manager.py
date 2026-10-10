"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Theme Manager
Version : 1.0
===========================================================
"""

import customtkinter as ctk


class ThemeManager:

    # ==========================================
    # Apply Theme
    # ==========================================

    @staticmethod
    def apply(theme):

        if not theme:
            theme = "System"

        theme = str(theme).strip()

        # ==========================================
        # Light
        # ==========================================

        if theme.lower() == "light":

            ctk.set_appearance_mode(
                "Light"
            )

            print(
                "🎨 Theme Applied: Light"
            )

            return

        # ==========================================
        # Dark
        # ==========================================

        if theme.lower() == "dark":

            ctk.set_appearance_mode(
                "Dark"
            )

            print(
                "🎨 Theme Applied: Dark"
            )

            return

        # ==========================================
        # System
        # ==========================================

        ctk.set_appearance_mode(
            "System"
        )

        print(
            "🎨 Theme Applied: System"
        )

    # ==========================================
    # Get Current Theme
    # ==========================================

    @staticmethod
    def get_current():

        try:

            return ctk.get_appearance_mode()

        except Exception:

            return "System"