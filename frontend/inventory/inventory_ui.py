"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Inventory Management UI
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry

class InventoryUI:

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
            text="📦 Inventory / Store Management",
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
            placeholder_text="Search Item..."
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

        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420
        )

        self.left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        self.right = ctk.CTkFrame(self.body)

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # Inventory Information
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Inventory Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # ==========================================
        # Item ID
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Item ID"
        ).pack(anchor="w", padx=20)

        self.item_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Item ID",
            state="disabled"
        )

        self.item_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Item Name
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Item Name"
        ).pack(anchor="w", padx=20)

        self.item_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Enter Item Name"
        )

        self.item_name.pack(
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
                "Medicine",
                "Surgical",
                "Injection",
                "Consumable",
                "Medical Equipment",
                "Laboratory",
                "Others"
            ]
        )

        self.category.pack(
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
        # Batch Number
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Batch Number"
        ).pack(anchor="w", padx=20)

        self.batch_no = ctk.CTkEntry(
            self.left,
            placeholder_text="Batch Number"
        )

        self.batch_no.pack(
            fill="x",
            padx=20,
            pady=5
        )

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

        # Default Category

        self.category.set("Medicine")

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
                "Piece",
                "Strip",
                "Box",
                "Bottle",
                "Vial",
                "Tube",
                "Pack",
                "Kg",
                "Gram",
                "Liter",
                "ml"
            ]
        )

        self.unit.pack(
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
        # Expiry Date
        # ==========================================

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

                # Default Unit

        self.unit.set("Piece")

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
        # Inventory Item List
        # ==========================================

        ctk.CTkLabel(
            self.right,
            text="Inventory Item List",
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
            "Item ID",
            "Item Name",
            "Category",
            "Supplier",
            "Stock",
            "Selling Price",
            "Expiry Date"
        )

        self.inventory_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.inventory_table.yview
        )

        for col in columns:

            self.inventory_table.heading(
                col,
                text=col
            )

        self.inventory_table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.inventory_table.column(
            "Item ID",
            width=120,
            anchor="center"
        )

        self.inventory_table.column(
            "Item Name",
            width=220
        )

        self.inventory_table.column(
            "Category",
            width=140,
            anchor="center"
        )

        self.inventory_table.column(
            "Supplier",
            width=180
        )

        self.inventory_table.column(
            "Stock",
            width=100,
            anchor="center"
        )

        self.inventory_table.column(
            "Selling Price",
            width=120,
            anchor="e"
        )

        self.inventory_table.column(
            "Expiry Date",
            width=130,
            anchor="center"
        )

        self.inventory_table.pack(
            fill="both",
            expand=True
        )