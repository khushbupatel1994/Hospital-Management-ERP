"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Header
Version   : 2.0
===========================================================
"""

import customtkinter as ctk
from datetime import datetime


class Header(ctk.CTkFrame):

    def __init__(self, parent, username="Khushbu"):

        super().__init__(
            parent,
            height=70,
            corner_radius=10
        )

        self.username = username

        self.pack_propagate(False)

        self.create_header()

    # ==========================================
    # Header UI
    # ==========================================

    def create_header(self):

        # Left Side
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.pack(side="left", padx=15)

        ctk.CTkLabel(
            left,
            text="🏥 Cloud Secure Hospital ERP",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Hospital Management & Accounting ERP",
            font=("Segoe UI", 12)
        ).pack(anchor="w")

        # Right Side
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", padx=20)

        current = datetime.now().strftime("%d-%m-%Y  %I:%M %p")

        ctk.CTkLabel(
            right,
            text=current,
            font=("Segoe UI", 13)
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            text=f"👤 {self.username}",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="e")