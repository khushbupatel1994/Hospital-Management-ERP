"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Status Bar
Version   : 2.0
===========================================================
"""

import customtkinter as ctk
from datetime import datetime


class StatusBar(ctk.CTkFrame):

    def __init__(self, parent, username="Khushbu"):

        super().__init__(
            parent,
            height=35,
            corner_radius=0
        )

        self.username = username

        self.pack_propagate(False)

        self.create_statusbar()

    # ==========================================
    # Status Bar
    # ==========================================

    def create_statusbar(self):

        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        status = (
            f"🟢 Database : Connected     "
            f"☁ Cloud : Online     "
            f"👤 User : {self.username}     "
            f"🕒 {current_time}     "
            f"Version : 2.0"
        )

        self.status_label = ctk.CTkLabel(
            self,
            text=status,
            font=("Segoe UI", 12)
        )

        self.status_label.pack(
            side="left",
            padx=10
        )

    # ==========================================
    # Update Status
    # ==========================================

    def update_status(self, text):

        self.status_label.configure(
            text=text
        )