"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Admin Dashboard UI
Version : 4.2
===========================================================
"""

import customtkinter as ctk

from frontend.components.sidebar import Sidebar
from frontend.components.header import Header
from frontend.components.dashboard_card import DashboardCard
from frontend.components.statusbar import StatusBar

from frontend.dashboard.admin_dashboard_service import (
    AdminDashboardService
)


class AdminDashboardUI:

    REVENUE_ROLES = {
        "Super Admin",
        "Admin",
        "Accountant"
    }

    def __init__(self, root, username="User"):

        self.root = root
        self.username = username

        # ==================================================
        # ROLE
        # ==================================================

        self.role = str(
            getattr(
                self,
                "role",
                "Super Admin"
            )
        ).strip()

        # ==================================================
        # DASHBOARD TITLE
        # ==================================================

        role_titles = {

            "Super Admin":
                "Super Admin Dashboard",

            "Admin":
                "Admin Dashboard",

            "Doctor":
                "Doctor Dashboard",

            "Nurse":
                "Nurse Dashboard",

            "HR":
                "HR Dashboard",

            "Reception":
                "Reception Dashboard",

            "Receptionist":
                "Reception Dashboard",

            "Pharmacist":
                "Pharmacy Dashboard",

            "Lab Technician":
                "Laboratory Dashboard",

            "Accountant":
                "Accounts Dashboard",

            "Inventory Manager":
                "Inventory Dashboard"
        }

        self.dashboard_title = role_titles.get(
            self.role,
            f"{self.role} Dashboard"
        )

        # ==================================================
        # WINDOW
        # ==================================================

        self.root.title(
            "Cloud Secure Hospital ERP"
        )

        self.root.geometry(
            "1450x900"
        )

        self.root.minsize(
            1200,
            800
        )

        # ==================================================
        # DATABASE SERVICE
        # ==================================================

        # IMPORTANT:
        # Controller creates this before super().
        # Never overwrite it with None.

        if not hasattr(
            self,
            "dashboard_service"
        ):

            try:

                self.dashboard_service = (
                    AdminDashboardService()
                )

            except Exception as e:

                print(
                    "Dashboard Service Error:",
                    e
                )

                self.dashboard_service = None

        # ==================================================
        # CREATE DASHBOARD
        # ==================================================

        self.create_dashboard()

    # ======================================================
    # CREATE DASHBOARD
    # ======================================================

    def create_dashboard(self):

        # ==================================================
        # MAIN
        # ==================================================

        self.main = ctk.CTkFrame(
            self.root,
            corner_radius=0
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # SIDEBAR
        # ==================================================

        self.sidebar = Sidebar(
            self.main
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # ==================================================
        # RIGHT AREA
        # ==================================================

        self.right = ctk.CTkFrame(
            self.main,
            corner_radius=0
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==================================================
        # HEADER
        # ==================================================

        self.header = Header(
            self.right,
            username=self.username,
            hospital_name=self.hospital_name,
            logo_path=self.logo_path
        )

        self.header.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # ==================================================
        # CONTENT
        # ==================================================

        self.content = ctk.CTkScrollableFrame(
            self.right,
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )

        # ==================================================
        # STATUS BAR
        # ==================================================

        self.statusbar = StatusBar(
            self.right,
            username=self.username
        )

        self.statusbar.pack(
            side="bottom",
            fill="x"
        )

        # ==================================================
        # LOAD
        # ==================================================

        self.load_dashboard()

    # ======================================================
    # LOAD DASHBOARD
    # ======================================================

    def load_dashboard(self):

        # ==================================================
        # REMOVE OLD CONTENT
        # ==================================================

        for widget in self.content.winfo_children():

            widget.destroy()

        # ==================================================
        # DEFAULT VALUES
        # ==================================================

        doctors = 0
        patients = 0
        appointments = 0
        opd = 0
        ipd = 0
        revenue = 0

        # ==================================================
        # DATABASE VALUES
        # ==================================================

        if self.dashboard_service:

            try:

                doctors = (
                    self.dashboard_service
                    .get_total_doctors()
                )

            except Exception as e:

                print(
                    "Doctors Dashboard Error:",
                    e
                )

            try:

                patients = (
                    self.dashboard_service
                    .get_total_patients()
                )

            except Exception as e:

                print(
                    "Patients Dashboard Error:",
                    e
                )

            try:

                appointments = (
                    self.dashboard_service
                    .get_total_appointments()
                )

            except Exception as e:

                print(
                    "Appointments Dashboard Error:",
                    e
                )

            try:

                opd = (
                    self.dashboard_service
                    .get_total_opd()
                )

            except Exception as e:

                print(
                    "OPD Dashboard Error:",
                    e
                )

            try:

                ipd = (
                    self.dashboard_service
                    .get_total_ipd()
                )

            except Exception as e:

                print(
                    "IPD Dashboard Error:",
                    e
                )

            try:

                revenue = (
                    self.dashboard_service
                    .get_total_revenue()
                )

            except Exception as e:

                print(
                    "Revenue Dashboard Error:",
                    e
                )

        # ==================================================
        # SAFE VALUES
        # ==================================================

        doctors = 0 if doctors is None else doctors
        patients = 0 if patients is None else patients
        appointments = (
            0
            if appointments is None
            else appointments
        )

        opd = 0 if opd is None else opd
        ipd = 0 if ipd is None else ipd
        revenue = 0 if revenue is None else revenue

        # ==================================================
        # HEADER
        # ==================================================

        header_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        title = ctk.CTkLabel(
            header_frame,
            text=self.dashboard_title,
            font=(
                "Segoe UI",
                30,
                "bold"
            )
        )

        title.pack(
            side="left"
        )

        # ==================================================
        # REFRESH
        # ==================================================

        refresh_button = ctk.CTkButton(
            header_frame,
            text="⟳  Refresh",
            width=165,
            height=50,
            corner_radius=10,
            command=self.load_dashboard
        )

        refresh_button.pack(
            side="right"
        )

        # ==================================================
        # CARD FRAME
        # ==================================================

        self.card_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.card_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 5)
        )

        # ==================================================
        # GRID
        # ==================================================

        for column in range(3):

            self.card_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # ==================================================
        # IMPORTANT
        #
        # ALL SIX CARDS ARE ALWAYS CREATED.
        #
        # This prevents:
        #
        # AttributeError:
        # 'NoneType' object has no attribute
        # 'set_command'
        #
        # ==================================================

        self.doctor_card = DashboardCard(
            self.card_frame,
            title="Doctors",
            value=str(doctors),
            icon="👨‍⚕️"
        )

        self.doctor_card.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================================

        self.patient_card = DashboardCard(
            self.card_frame,
            title="Patients",
            value=str(patients),
            icon="🧑"
        )

        self.patient_card.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================================

        self.appointment_card = DashboardCard(
            self.card_frame,
            title="Appointments",
            value=str(appointments),
            icon="📅"
        )

        self.appointment_card.grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================================

        self.opd_card = DashboardCard(
            self.card_frame,
            title="OPD",
            value=str(opd),
            icon="🩺"
        )

        self.opd_card.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================================

        self.ipd_card = DashboardCard(
            self.card_frame,
            title="IPD",
            value=str(ipd),
            icon="🛏"
        )

        self.ipd_card.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================================

        # ==================================================
        # REVENUE CARD - ONLY FINANCIAL/ADMIN ROLES
        # ==================================================

        self.revenue_card = None

        if self.role in self.REVENUE_ROLES:

            self.revenue_card = DashboardCard(
                self.card_frame,
                title="Revenue",
                value=f"₹{float(revenue):,.2f}",
                icon="💰"
            )

            self.revenue_card.grid(
                row=1,
                column=2,
                padx=10,
                pady=10,
                sticky="nsew"
            )

        else:
            print(
                f"🔒 Revenue Hidden for Role: {self.role}"
            )

        # ==================================================
        # HOSPITAL OVERVIEW
        # ==================================================

        self.overview_frame = ctk.CTkFrame(
            self.content,
            corner_radius=12
        )

        self.overview_frame.pack(
            fill="x",
            padx=20,
            pady=(8, 15)
        )

        # ==================================================
        # OVERVIEW TITLE
        # ==================================================

        self.overview_title = ctk.CTkLabel(
            self.overview_frame,
            text="Hospital Overview",
            font=(
                "Segoe UI",
                25,
                "bold"
            )
        )

        self.overview_title.pack(
            pady=(12, 5)
        )

        # ==================================================
        # OVERVIEW ROW 1
        # ==================================================

        self.overview_row1 = ctk.CTkLabel(
            self.overview_frame,
            text=(
                f"Doctors: {doctors}"
                "    |    "
                f"Patients: {patients}"
                "    |    "
                f"Appointments: {appointments}"
            ),
            font=(
                "Segoe UI",
                16
            )
        )

        self.overview_row1.pack(
            pady=5
        )

        # ==================================================
        # OVERVIEW ROW 2
        # ==================================================

        overview_row2_text = (
            f"OPD: {opd}"
            "    |    "
            f"IPD: {ipd}"
        )

        if self.role in self.REVENUE_ROLES:
            overview_row2_text += (
                "    |    "
                f"Revenue: ₹{float(revenue):,.2f}"
            )

        self.overview_row2 = ctk.CTkLabel(
            self.overview_frame,
            text=overview_row2_text,
            font=(
                "Segoe UI",
                16
            )
        )

        self.overview_row2.pack(
            pady=5
        )

        # ==================================================
        # STATUS
        # ==================================================

        self.dashboard_status = ctk.CTkLabel(
            self.overview_frame,
            text="Dashboard loaded from database",
            font=(
                "Segoe UI",
                13
            )
        )

        self.dashboard_status.pack(
            pady=(5, 15)
        )

        # ==================================================
        # UPDATE
        # ==================================================

        self.content.update_idletasks()

    # ======================================================
    # UPDATE DASHBOARD VALUES
    # ======================================================

    def update_dashboard_values(
        self,
        doctors,
        patients,
        appointments,
        opd,
        ipd,
        revenue
    ):

        doctors = 0 if doctors is None else doctors
        patients = 0 if patients is None else patients
        appointments = (
            0
            if appointments is None
            else appointments
        )

        opd = 0 if opd is None else opd
        ipd = 0 if ipd is None else ipd
        revenue = 0 if revenue is None else revenue

        # ==================================================
        # CARDS
        # ==================================================

        if getattr(
            self,
            "doctor_card",
            None
        ) is not None:

            self.doctor_card.update_value(
                doctors
            )

        if getattr(
            self,
            "patient_card",
            None
        ) is not None:

            self.patient_card.update_value(
                patients
            )

        if getattr(
            self,
            "appointment_card",
            None
        ) is not None:

            self.appointment_card.update_value(
                appointments
            )

        if getattr(
            self,
            "opd_card",
            None
        ) is not None:

            self.opd_card.update_value(
                opd
            )

        if getattr(
            self,
            "ipd_card",
            None
        ) is not None:

            self.ipd_card.update_value(
                ipd
            )

        if getattr(
            self,
            "revenue_card",
            None
        ) is not None:

            self.revenue_card.update_value(
                f"₹{float(revenue):,.2f}"
            )

        # ==================================================
        # OVERVIEW
        # ==================================================

        if hasattr(
            self,
            "overview_row1"
        ):

            self.overview_row1.configure(
                text=(
                    f"Doctors: {doctors}"
                    "    |    "
                    f"Patients: {patients}"
                    "    |    "
                    f"Appointments: {appointments}"
                )
            )

        if hasattr(
            self,
            "overview_row2"
        ):

            overview_row2_text = (
                f"OPD: {opd}"
                "    |    "
                f"IPD: {ipd}"
            )

            if self.role in self.REVENUE_ROLES:
                overview_row2_text += (
                    "    |    "
                    f"Revenue: ₹{float(revenue):,.2f}"
                )

            self.overview_row2.configure(
                text=overview_row2_text
            )

        if hasattr(
            self,
            "dashboard_status"
        ):

            self.dashboard_status.configure(
                text="Dashboard updated successfully"
            )

        self.content.update_idletasks()