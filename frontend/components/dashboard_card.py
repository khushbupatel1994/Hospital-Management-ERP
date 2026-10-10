"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Dashboard Card
Version   : 2.0
===========================================================
"""

import customtkinter as ctk


class DashboardCard(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title,
        value="0",
        icon="📊"
    ):

        super().__init__(
           parent,
           width=250,
           height=170,
           corner_radius=15,
           fg_color="#2E86DE"
        )

        self.pack_propagate(False)

        self.title = title
        self.value = value
        self.icon = icon
        self.command = None

        self.create_card()

    # ==========================================
    # Create Card
    # ==========================================

    def create_card(self):

        self.icon_label = ctk.CTkLabel(
            self,
            text=self.icon,
            font=("Segoe UI Emoji", 32),
            text_color="white"
        )
        self.icon_label.pack(pady=(20, 8))

        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )

        self.title_label.pack(pady=(0, 5))

        self.value_label = ctk.CTkLabel(
            self,
            text=str(self.value),
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        self.value_label.pack(pady=(5, 15))

    # ==========================================
    # Card Action
    # ==========================================

    def set_command(self, command):
        """Run *command* when any visible part of the card is clicked."""
        self.command = command
        for widget in (self, self.icon_label, self.title_label, self.value_label):
            widget.bind("<Button-1>", self._run_command)

    def _run_command(self, _event=None):
        if self.command:
            self.command()

    # ==========================================
    # Update Card Value
    # ==========================================

    def update_value(self, value):

        self.value = value

        self.value_label.configure(
            text=str(value)
        )
