"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Sidebar
Version   : 2.0
===========================================================
"""

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=250,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.create_sidebar()
       

    # ==========================================
    # Sidebar UI
    # ==========================================

    def create_sidebar(self):

        # Logo
        self.logo = ctk.CTkLabel(
            self,
            text="🏥\nCloud Secure\nHospital ERP",
            font=("Segoe UI", 20, "bold"),
            justify="center"
        )

        self.logo.pack(pady=(20, 30))
        # Scrollable Menu
        self.menu_frame = ctk.CTkScrollableFrame(
            self,
            width=220,
            height=600, 
            fg_color="transparent",
            corner_radius=0
        )

        self.menu_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )

        # Menu List
        menus = [
            "🏠 Dashboard",
            "👥 Users",
            "🧑 Patients",
            "👨‍⚕️ Doctors",
            "📅 Appointments",
            "🩺 OPD",
            "🛏 IPD",
            "💰 Billing",
            "💊 Pharmacy",
            "🧪 Laboratory",
            "📦 Inventory",
            "📊 Accounts",
            "📄 Reports",
            "📈 Analytics",
            "🤖 AI Intelligence",
            "👨‍💼 HR & Employee",
            "⚙ Settings",
            "💾 Backup",
            "🚪 Logout",
        ]

        # IMPORTANT
        self.buttons = {}

        for menu in menus:

            btn = ctk.CTkButton(
                self.menu_frame,
                text=menu,
                width=210,
                height=40,
                anchor="w",
                corner_radius=8
            )

            btn.pack(
                padx=10,
                pady=5,
                fill="x"
            )

            self.buttons[menu] = btn
            