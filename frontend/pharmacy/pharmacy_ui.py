"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Pharmacy Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class PharmacyUI:

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
            text="💊 Pharmacy Management",
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
            placeholder_text="Search Medicine..."
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
        self.body.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT
        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420,
            height=650      # height देना जरूरी है
        )

        self.left.pack(
            side="left",
            fill="both",    # y की जगह both
            expand=False,
            padx=(0,10),
            pady=5
        )

        # RIGHT
        self.right = ctk.CTkFrame(self.body)

        self.right.pack(
            side="left",
            fill="both",
            expand=True,
            pady=5
        )
        # ==========================================
        # Medicine Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Medicine Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # Medicine ID
        ctk.CTkLabel(
            self.left,
            text="Medicine ID"
        ).pack(anchor="w", padx=20)

        self.medicine_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Medicine ID",
            state="disabled"
        )

        self.medicine_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Medicine Name
        ctk.CTkLabel(
            self.left,
            text="Medicine Name"
        ).pack(anchor="w", padx=20)

        self.medicine_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Medicine Name"
        )

        self.medicine_name.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Company Name
        ctk.CTkLabel(
            self.left,
            text="Company Name"
        ).pack(anchor="w", padx=20)

        self.company_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Company Name"
        )

        self.company_name.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Batch Number
        ctk.CTkLabel(
            self.left,
            text="Batch Number"
        ).pack(anchor="w", padx=20)

        self.batch_no = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Batch Number"
        )

        self.batch_no.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Category
        ctk.CTkLabel(
            self.left,
            text="Category"
        ).pack(anchor="w", padx=20)

        self.category = ctk.CTkComboBox(
            self.left,
            values=[
                "Tablet",
                "Capsule",
                "Syrup",
                "Injection",
                "Drops",
                "Cream",
                "Ointment",
                "Powder",
                "Others"
            ]
        )

        self.category.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Expiry Date
        ctk.CTkLabel(
            self.left,
            text="Expiry Date"
        ).pack(anchor="w", padx=20)

        self.expiry_date = DateEntry(
            self.left,
            width=20,
            date_pattern="dd-mm-yyyy"
        )

        self.expiry_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Default Category
        self.category.set("Tablet")

        # ==========================================
        # Purchase Price
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Purchase Price"
        ).pack(anchor="w", padx=20)

        self.purchase_price = ctk.CTkEntry(
                self.left,
                placeholder_text="0.00"
        )

        self.purchase_price.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Selling Price
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Selling Price"
        ).pack(anchor="w", padx=20)

        self.selling_price = ctk.CTkEntry(
            self.left,
            placeholder_text="0.00"
     )

        self.selling_price.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Stock Quantity
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Stock Quantity"
        ).pack(anchor="w", padx=20)

        self.stock_quantity = ctk.CTkEntry(
            self.left,
            placeholder_text="0"
        )

        self.stock_quantity.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Minimum Stock
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Minimum Stock"
        ).pack(anchor="w", padx=20)

        self.minimum_stock = ctk.CTkEntry(
            self.left,
            placeholder_text="0"
        )

        self.minimum_stock.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Unit
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Unit"
        ).pack(anchor="w", padx=20)

        self.unit = ctk.CTkComboBox(
            self.left,
            values=[
                "Strip",
                "Bottle",
                "Box",
                "Piece",
                "Tube",
                "Packet",
                "Vial"
            ]
        )

        self.unit.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # GST (%)
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

        # Default Unit
        self.unit.set("Strip")

        # ==========================================
        # Manufacturer
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Manufacturer"
        ).pack(anchor="w", padx=20)

        self.manufacturer = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Manufacturer Name"
        )

        self.manufacturer.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Supplier
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Supplier"
        ).pack(anchor="w", padx=20)

        self.supplier = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Supplier Name"
        )

        self.supplier.pack(
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
        # Medicine List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Medicine List",
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
            "Medicine ID",
            "Medicine",
            "Company",
            "Category",
            "Stock",
            "Selling Price",
            "Expiry"
        )

        self.pharmacy_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.pharmacy_table.yview
        )

        for col in columns:

            self.pharmacy_table.heading(
                col,
                text=col
            )

        self.pharmacy_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.pharmacy_table.column(
            "Medicine ID",
            width=120,
            anchor="center"
        )

        self.pharmacy_table.column(
            "Medicine",
            width=220
        )

        self.pharmacy_table.column(
            "Company",
            width=180
        )

        self.pharmacy_table.column(
            "Category",
            width=120,
            anchor="center"
        )

        self.pharmacy_table.column(
            "Stock",
            width=90,
            anchor="center"
        )

        self.pharmacy_table.column(
            "Selling Price",
            width=120,
            anchor="e"
        )

        self.pharmacy_table.column(
            "Expiry",
            width=120,
            anchor="center"
        )

        self.pharmacy_table.pack(
            fill="both",
            expand=True
        )