"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Admin Dashboard UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk

from frontend.components.sidebar import Sidebar
from frontend.components.header import Header
from frontend.components.dashboard_card import DashboardCard
from frontend.components.statusbar import StatusBar


class AdminDashboardUI:

    def __init__(self, root, username="User"):

        self.root = root
        self.username = username

        self.root.title(
            "Cloud Secure Hospital ERP"
        )

        self.root.geometry("1450x850")

        self.create_dashboard()

    # ==========================================
    # Dashboard UI
    # ==========================================

    def create_dashboard(self):

        # Main Container
        self.main = ctk.CTkFrame(
            self.root,
            corner_radius=0
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # ==========================
        # Sidebar
        # ==========================

        self.sidebar = Sidebar(self.main)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # ==========================
        # Right Area
        # ==========================

        self.right = ctk.CTkFrame(
            self.main,
            corner_radius=0
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Header
        self.header = Header(
            self.right,
            username=self.username
        )

        self.header.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # Dashboard Content
        self.content = ctk.CTkFrame(
            self.right
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=15
        )


        # Status Bar
        self.statusbar = StatusBar(
            self.right,
            username=self.username
        )

        self.statusbar.pack(
            side="bottom",
            fill="x"
        )

        self.load_dashboard()

    def load_dashboard(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.card_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.card_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.doctor_card = DashboardCard(
            self.card_frame,
            title="Doctors",
            value="12",
            icon="👨‍⚕️"
        )
        self.doctor_card.pack(side="left", padx=10)

        self.patient_card = DashboardCard(
            self.card_frame,
            title="Patients",
            value="145",
            icon="🧑"
        )
        self.patient_card.pack(side="left", padx=10)

        self.appointment_card = DashboardCard(
            self.card_frame,
            title="Appointments",
            value="32",
            icon="📅"
        )
        self.appointment_card.pack(side="left", padx=10)

        self.opd_card = DashboardCard(
            self.card_frame,
            title="OPD",
            value="0",
            icon="🩺"
        )
        self.opd_card.pack(side="left", padx=10)

        self.ipd_card = DashboardCard(
            self.card_frame,
            title="IPD",
            value="0",
            icon="🛏"
        )
        self.ipd_card.pack(side="left", padx=10)

        self.revenue_card = DashboardCard(
            self.card_frame,
            title="Revenue",
            value="₹50,000",
            icon="💰"
        )
        self.revenue_card.pack(side="left", padx=10)