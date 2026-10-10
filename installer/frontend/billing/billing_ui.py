"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Billing Management UI
Version : 2.0
===========================================================
"""
from tkcalendar import DateEntry
import customtkinter as ctk
from tkinter import ttk


class BillingUI:

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
            text="💰 Billing Management",
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
            placeholder_text="Search Bill..."
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

        self.body = ctk.CTkFrame(
            self.main
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420,
            height=650,
            corner_radius=10
        )

        self.left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )


        self.right = ctk.CTkFrame(
            self.body
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # Billing Form
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Billing Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # Bill ID
        ctk.CTkLabel(
            self.left,
            text="Bill ID"
        ).pack(anchor="w", padx=20)

        self.bill_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Bill ID",
            state="disabled"
        )

        self.bill_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Patient
        ctk.CTkLabel(
            self.left,
            text="Patient"
        ).pack(anchor="w", padx=20)

        self.patient = ctk.CTkComboBox(
            self.left,
            values=[]
        )

        self.patient.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Mobile
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Mobile"
        ).pack(anchor="w", padx=20)

        self.mobile = ctk.CTkEntry(
            self.left,
            placeholder_text="Mobile Number",
            state="disabled"
        )

        self.mobile.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Age
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Age"
        ).pack(anchor="w", padx=20)

        self.age = ctk.CTkEntry(
            self.left,
            placeholder_text="Age",
            state="disabled"
        )

        self.age.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Gender
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Gender"
        ).pack(anchor="w", padx=20)

        self.gender = ctk.CTkEntry(
            self.left,
            placeholder_text="Gender",
            state="disabled"
        )

        self.gender.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Doctor
        ctk.CTkLabel(
            self.left,
            text="Doctor"
        ).pack(anchor="w", padx=20)

        self.doctor = ctk.CTkComboBox(
            self.left,
            values=[]
        )

        self.doctor.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Department
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Department"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkEntry(
            self.left,
            placeholder_text="Department",
            state="disabled"
        )

        self.department.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Bill Date
        ctk.CTkLabel(
            self.left,
            text="Bill Date"
        ).pack(anchor="w", padx=20)

        self.bill_date = DateEntry(
           self.left,
            width=20,
            date_pattern="dd-mm-yyyy",
            font=("Segoe UI", 12)
        )

        self.bill_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Payment Mode
        ctk.CTkLabel(
            self.left,
            text="Payment Mode"
        ).pack(anchor="w", padx=20)

        self.payment_mode = ctk.CTkComboBox(
            self.left,
            values=[
                "Cash",
                "Card",
                "UPI",
                "Net Banking"
            ]
        )

        self.payment_mode.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Bill Status
        ctk.CTkLabel(
            self.left,
            text="Bill Status"
        ).pack(anchor="w", padx=20)

        self.bill_status = ctk.CTkComboBox(
            self.left,
            values=[
                "Paid",
                "Pending"
            ]
        )

        self.bill_status.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Values
        self.payment_mode.set("Cash")
        self.bill_status.set("Pending")

        # ==========================================
        # Consultation Fee
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Consultation Fee"
        ).pack(anchor="w", padx=20)

        self.consultation_fee = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.consultation_fee.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Medicine Charges
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Medicine Charges"
        ).pack(anchor="w", padx=20)

        self.medicine_charges = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.medicine_charges.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Lab Charges
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Lab Charges"
        ).pack(anchor="w", padx=20)

        self.lab_charges = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.lab_charges.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Other Charges
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Other Charges"
        ).pack(anchor="w", padx=20)

        self.other_charges = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.other_charges.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Discount
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Discount"
        ).pack(anchor="w", padx=20)

        self.discount = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
        )

        self.discount.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # GST
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="GST (%)"
        ).pack(anchor="w", padx=20)

        self.gst = ctk.CTkEntry(
            self.left,
            placeholder_text="0"
        )

        self.gst.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Total Amount
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Total Amount"
        ).pack(anchor="w", padx=20)

        self.total_amount = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00",
            state="disabled"
        )

        self.total_amount.pack(
            fill="x",
            padx=20,
            pady=5
        )

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
            pady=(5, 15)
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
        # Print Button
        # ==========================================

        self.print_btn = ctk.CTkButton(
            self.button_frame,
            text="🖨 Print",
            fg_color="#16A085"
        )

        self.print_btn.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        # ==========================================
        # Billing List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Billing List",
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

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        columns = (

            "ID",
            "Bill ID",
            "Patient",
            "Doctor",
            "Bill Date",
            "Total",
            "Payment",
            "Status"

        )

        self.billing_table = ttk.Treeview(

            self.table_frame,

            columns=columns,

            show="headings",

            yscrollcommand=self.scroll_y.set

        )

        self.scroll_y.configure(
            command=self.billing_table.yview
        )

        for col in columns:

            self.billing_table.heading(
                col,
                text=col
            )

        # Professional Column Width
        self.billing_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.billing_table.column(
            "Bill ID",
            width=110,
            anchor="center"
        )

        self.billing_table.column(
            "Patient",
            width=180
        )

        self.billing_table.column(
            "Doctor",
            width=180
        )

        self.billing_table.column(
            "Bill Date",
            width=110,
            anchor="center"
        )

        self.billing_table.column(
            "Total",
            width=120,
            anchor="e"
        )

        self.billing_table.column(
            "Payment",
            width=120,
            anchor="center"
        )

        self.billing_table.column(
            "Status",
            width=100,
            anchor="center"
        )

        self.billing_table.pack(
            fill="both",
            expand=True
        )