"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Sidebar
Version   : 3.0
===========================================================
"""

import os
import customtkinter as ctk
from PIL import Image


class Sidebar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        hospital_name="Cloud Secure Hospital ERP",
        logo_path=""
    ):

        super().__init__(
            parent,
            width=250,
            corner_radius=0
        )

        self.hospital_name = (
            hospital_name
            or "Cloud Secure Hospital ERP"
        )

        self.logo_path = (
            logo_path
            or ""
        )

        self.logo_image = None

        self.pack_propagate(False)

        self.create_sidebar()

    # =====================================================
    # CREATE SIDEBAR
    # =====================================================

    def create_sidebar(self):

        # =================================================
        # LOGO AREA
        # =================================================

        self.logo_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.logo_frame.pack(
            pady=(20, 10),
            padx=10,
            fill="x"
        )

        # =================================================
        # HOSPITAL LOGO
        # =================================================

        self.logo_image_label = ctk.CTkLabel(
            self.logo_frame,
            text="🏥",
            font=(
                "Segoe UI",
                34,
                "bold"
            ),
            width=70,
            height=70
        )

        self.logo_image_label.pack(
            pady=(0, 5)
        )

        self.load_logo()

        # =================================================
        # HOSPITAL NAME
        # =================================================

        self.logo = ctk.CTkLabel(
            self.logo_frame,
            text=self.format_hospital_name(),
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            justify="center"
        )

        self.logo.pack(
            pady=(0, 15)
        )

        # =================================================
        # SCROLLABLE MENU
        # =================================================

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

        # =================================================
        # MENU LIST
        # =================================================

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

            "🚪 Logout"

        ]

        # =================================================
        # BUTTON DICTIONARY
        # =================================================

        self.buttons = {}

        # =================================================
        # CREATE BUTTONS
        # =================================================

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

            self.buttons[
                menu
            ] = btn

    # =====================================================
    # FORMAT HOSPITAL NAME
    # =====================================================

    def format_hospital_name(self):

        name = (
            self.hospital_name
            or "Cloud Secure Hospital ERP"
        )

        # Long name ko multiple lines me show karega
        words = name.split()

        if len(words) <= 2:

            return (
                "🏥\n"
                + name
            )

        # Maximum approximately 3 words per line
        lines = []

        current = []

        for word in words:

            current.append(
                word
            )

            if len(current) >= 3:

                lines.append(
                    " ".join(current)
                )

                current = []

        if current:

            lines.append(
                " ".join(current)
            )

        return (
            "🏥\n"
            + "\n".join(lines)
        )

    # =====================================================
    # LOAD LOGO
    # =====================================================

    def load_logo(self):

        try:

            if not self.logo_path:

                return

            image_path = os.path.normpath(
                self.logo_path
            )

            if not os.path.isfile(
                image_path
            ):

                print(
                    "⚠ Sidebar Logo Not Found:",
                    image_path
                )

                return

            image = Image.open(
                image_path
            )

            image = image.convert(
                "RGBA"
            )

            self.logo_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(65, 65)
            )

            self.logo_image_label.configure(
                image=self.logo_image,
                text=""
            )

            print(
                "✅ Hospital Logo Loaded in Sidebar"
            )

        except Exception as e:

            print(
                "⚠ Sidebar Logo Error:",
                e
            )

    # =====================================================
    # UPDATE HOSPITAL INFORMATION
    # =====================================================

    def update_hospital_info(
        self,
        hospital_name=None,
        logo_path=None
    ):

        if hospital_name is not None:

            self.hospital_name = (
                hospital_name
                or "Cloud Secure Hospital ERP"
            )

            self.logo.configure(
                text=self.format_hospital_name()
            )

        if logo_path is not None:

            self.logo_path = (
                logo_path
                or ""
            )

            self.logo_image = None

            self.logo_image_label.configure(
                image=None,
                text="🏥"
            )

            self.load_logo()

        print(
            "✅ Sidebar Hospital Information Updated"
        )