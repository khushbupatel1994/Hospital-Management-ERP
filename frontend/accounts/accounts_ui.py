"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Accounts Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class AccountsUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Create Widgets
    # ==========================================

    def create_widgets(self):

        self.main = ctk.CTkFrame(
            self.root,
            corner_radius=10
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Header
        # ==========================================

        self.header = ctk.CTkFrame(
            self.main,
            height=70
        )

        self.header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header,
            text="💰 Accounts Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

        # ==========================================
        # Search
        # ==========================================

        self.search_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        self.search_frame.pack(
            side="right",
            padx=20
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=250,
            placeholder_text="Search Transaction..."
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100
        )

        self.search_btn.pack(
            side="left",
            padx=5
        )

        # ==========================================
        # Body
        # ==========================================

        self.body = ctk.CTkFrame(self.main)
        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Left Scrollable Frame
        self.left = ctk.CTkScrollableFrame(
          self.body,
          width=420,
          corner_radius=10
        )


        self.left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # Right Frame
        self.right = ctk.CTkFrame(self.body)
        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )
        # ==========================================
        # Transaction Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Transaction Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)
        # ==========================================
        # Transaction ID
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Transaction ID"
        ).pack(anchor="w", padx=20)

        self.transaction_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Transaction ID",
            state="disabled"
        )

        self.transaction_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Transaction Type
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Transaction Type"
        ).pack(anchor="w", padx=20)

        self.transaction_type = ctk.CTkComboBox(
            self.left,
            values=[
                "Income",
                "Expense"
            ]
        )

        self.transaction_type.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Category
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Category"
        ).pack(anchor="w", padx=20)

        self.category = ctk.CTkComboBox(
            self.left,
            values=[
                "Consultation",
                "Pharmacy",
                "Laboratory",
                "IPD",
                "Salary",
                "Purchase",
                "Electricity",
                "Rent",
                "Maintenance",
                "Miscellaneous"
            ]
        )

        self.category.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Amount
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Amount"
        ).pack(anchor="w", padx=20)

        self.amount = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.amount.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Payment Mode
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Payment Mode"
        ).pack(anchor="w", padx=20)

        self.payment_mode = ctk.CTkComboBox(
            self.left,
            values=[
                "Cash",
                "UPI",
                "Card",
                "Cheque",
                "Bank Transfer"
            ]
        )

        self.payment_mode.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Transaction Date
        ctk.CTkLabel(
            self.left,
            text="Transaction Date"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        self.transaction_date = DateEntry(
            self.left,
            width=30,
            date_pattern="dd-mm-yyyy",
            background="#1f6aa5",
            foreground="white",
            borderwidth=1
        )

        self.transaction_date.pack(
            fill="x",
            padx=20
        )
        # ==========================================
        # Description
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Description"
        ).pack(anchor="w", padx=20)

        self.description = ctk.CTkTextbox(
            self.left,
            height=80
        )

        self.description.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values

        self.transaction_type.set("Income")

        self.category.set("Consultation")

        self.payment_mode.set("Cash")

        # ==========================================
        # Remarks
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Remarks"
        ).pack(anchor="w", padx=20)

        self.remarks = ctk.CTkTextbox(
            self.left,
            height=70
        )

        self.remarks.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Buttons
        # ==========================================

        self.button_frame = ctk.CTkFrame(
            self.left,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Add"
        )

        self.add_btn.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.update_btn = ctk.CTkButton(
            self.button_frame,
            text="Update"
        )

        self.update_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete"
        )

        self.delete_btn.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear"
        )

        self.clear_btn.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # ==========================================
        # Transaction List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Accounts Transaction List",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=10
        )

        self.table_frame = ctk.CTkFrame(
            self.right
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Scrollbar
        # ==========================================

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # Treeview
        # ==========================================

        columns = (
            "ID",
            "Transaction ID",
            "Type",
            "Category",
            "Amount",
            "Payment Mode",
            "Date"
        )

        self.accounts_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.accounts_table.yview
        )

        for col in columns:

            self.accounts_table.heading(
                col,
                text=col
            )

        self.accounts_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.accounts_table.column(
            "Transaction ID",
            width=150,
            anchor="center"
        )

        self.accounts_table.column(
            "Type",
            width=120,
            anchor="center"
        )

        self.accounts_table.column(
            "Category",
            width=170
        )

        self.accounts_table.column(
            "Amount",
            width=120,
            anchor="e"
        )

        self.accounts_table.column(
            "Payment Mode",
            width=140,
            anchor="center"
        )

        self.accounts_table.column(
            "Date",
            width=130,
            anchor="center"
        )

        self.accounts_table.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # Treeview Style
        # ==========================================

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#1F6AA5")],
            foreground=[("selected", "white")]
        )

        # ==========================================
        # Column Stretch
        # ==========================================

        for col in columns:

            self.accounts_table.column(

                col,

                stretch=True

            )

        # ==========================================
        # Focus
        # ==========================================

        self.search_entry.focus()

        # ==========================================
        # End of UI
        # ==========================================