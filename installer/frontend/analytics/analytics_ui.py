"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Analytics UI
Version : 3.0
===========================================================
"""

import customtkinter as ctk

from tkinter import ttk


class AnalyticsUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Create Widgets
    # ==========================================

    def create_widgets(self):

        # Main Frame

        self.main_frame = ctk.CTkFrame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Title

        self.title_label = ctk.CTkLabel(

            self.main_frame,

            text="Dashboard Analytics",

            font=("Arial", 24, "bold")

        )

        self.title_label.pack(
            pady=10
        )

    # ==========================================
    # Statistics Cards
    # ==========================================

        self.card_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.card_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.patient_card = ctk.CTkLabel(

            self.card_frame,

            text="Patients\n0",

            width=180,

            height=90,

            corner_radius=10,

            font=("Arial",18,"bold")

        )

        self.patient_card.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.revenue_card = ctk.CTkLabel(

            self.card_frame,

            text="Revenue\n₹0",

            width=180,

            height=90,

            corner_radius=10,

            font=("Arial",18,"bold")

        )

        self.revenue_card.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.opd_card = ctk.CTkLabel(

            self.card_frame,

            text="OPD\n0",

            width=180,

            height=90,

            corner_radius=10,

            font=("Arial",18,"bold")

        )

        self.opd_card.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        self.ipd_card = ctk.CTkLabel(

            self.card_frame,

            text="IPD\n0",

            width=180,

            height=90,

            corner_radius=10,

            font=("Arial",18,"bold")

        )

        self.ipd_card.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

    # ==========================================
    # Charts Section
    # ==========================================

        self.chart_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.chart_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Revenue Chart

        self.revenue_chart = ctk.CTkFrame(
            self.chart_frame,
            width=500,
            height=300
        )

        self.revenue_chart.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.revenue_chart,
            text="Monthly Revenue Chart",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Patient Chart

        self.patient_chart = ctk.CTkFrame(
            self.chart_frame,
            width=500,
            height=300
        )

        self.patient_chart.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.patient_chart,
            text="Patient Statistics",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(1, weight=1)

    # ==========================================
    # Bottom Panels
    # ==========================================

        self.bottom_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.bottom_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Low Stock

        self.low_stock = ctk.CTkTextbox(
            self.bottom_frame,
            width=450,
            height=180
        )

        self.low_stock.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.low_stock.insert(
            "end",
            "Low Stock Items..."
        )

        # Income Expense

        self.income_expense = ctk.CTkTextbox(
            self.bottom_frame,
            width=450,
            height=180
        )

        self.income_expense.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.income_expense.insert(
            "end",
            "Income vs Expense..."
        )

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)