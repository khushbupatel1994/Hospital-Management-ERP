"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Component : Header
Version   : 3.0
===========================================================
"""

import os
import customtkinter as ctk
from datetime import datetime
from PIL import Image


class Header(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        username="User",
        hospital_name="Cloud Secure Hospital ERP",
        logo_path=""
    ):

        super().__init__(
            parent,
            height=85,
            corner_radius=10
        )

        self.username = username

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

        self.create_header()

    # =====================================================
    # CREATE HEADER
    # =====================================================

    def create_header(self):

        # =================================================
        # LEFT SIDE
        # =================================================

        left = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            padx=15,
            fill="y"
        )

        # =================================================
        # LOGO
        # =================================================

        self.logo_label = ctk.CTkLabel(
            left,
            text="🏥",
            font=(
                "Segoe UI",
                32,
                "bold"
            ),
            width=60,
            height=60
        )

        self.logo_label.pack(
            side="left",
            padx=(0, 10)
        )

        # Load actual hospital logo
        self.load_logo()

        # =================================================
        # HOSPITAL INFORMATION
        # =================================================

        info = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            pady=5
        )

        # -------------------------------------------------
        # Hospital Name
        # -------------------------------------------------

        self.hospital_name_label = ctk.CTkLabel(
            info,
            text=f"🏥 {self.hospital_name}",
            font=(
                "Segoe UI",
                21,
                "bold"
            )
        )

        self.hospital_name_label.pack(
            anchor="w"
        )

        # -------------------------------------------------
        # Subtitle
        # -------------------------------------------------

        self.subtitle_label = ctk.CTkLabel(
            info,
            text="Hospital Management & Accounting ERP",
            font=(
                "Segoe UI",
                11
            )
        )

        self.subtitle_label.pack(
            anchor="w"
        )

        # =================================================
        # RIGHT SIDE
        # =================================================

        right = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            padx=20
        )

        # =================================================
        # DATE / TIME
        # =================================================

        current = datetime.now().strftime(
            "%d-%m-%Y  %I:%M %p"
        )

        self.date_label = ctk.CTkLabel(
            right,
            text=current,
            font=(
                "Segoe UI",
                13
            )
        )

        self.date_label.pack(
            anchor="e"
        )

        # =================================================
        # USER
        # =================================================

        self.user_label = ctk.CTkLabel(
            right,
            text=f"👤 {self.username}",
            font=(
                "Segoe UI",
                15,
                "bold"
            )
        )

        self.user_label.pack(
            anchor="e"
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
                    "⚠ Header Logo Not Found:",
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
                size=(52, 52)
            )

            self.logo_label.configure(
                image=self.logo_image,
                text=""
            )

            print(
                "✅ Hospital Logo Loaded in Header"
            )

        except Exception as e:

            print(
                "⚠ Header Logo Error:",
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

            self.hospital_name_label.configure(
                text=f"🏥 {self.hospital_name}"
            )

        if logo_path is not None:

            self.logo_path = (
                logo_path
                or ""
            )

            self.logo_image = None

            self.logo_label.configure(
                image=None,
                text="🏥"
            )

            self.load_logo()

        print(
            "✅ Header Hospital Information Updated"
        )