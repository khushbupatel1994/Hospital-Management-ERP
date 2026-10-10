"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Inventory Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import datetime
from frontend.inventory.inventory_ui import InventoryUI
from frontend.inventory.inventory_service import InventoryService
from frontend.inventory.inventory_crud import InventoryCRUD


class Inventory(InventoryUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = InventoryService()

        self.crud = InventoryCRUD()

        self.bind_events()

        self.load_items()
       

        self.item_id.configure(state="normal")

        self.item_id.insert(
            0,
            self.crud.generate_item_id()
        )

        self.item_id.configure(state="disabled")

        self.selected_item_id = None

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_item
        )

        self.update_btn.configure(
            command=self.update_item
        )

        self.delete_btn.configure(
            command=self.delete_item
        )

        self.search_btn.configure(
            command=self.search_item
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.inventory_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_item
        )
        self.search_entry.bind(
           "<KeyRelease>",
           lambda e: self.search_item()
        )

    # ==========================================
    # Add Item
    # ==========================================

    def add_item(self):

        item_name = self.item_name.get().strip()

        category = self.category.get()

        supplier = self.supplier.get().strip()

        batch_no = self.batch_no.get().strip()

        purchase_price = self.purchase_price.get().strip()

        selling_price = self.selling_price.get().strip()

        stock_quantity = self.stock_quantity.get().strip()

        minimum_stock = self.minimum_stock.get().strip()

        unit = self.unit.get()

        gst = self.gst.get().strip()

        expiry_date = self.expiry_date.get().strip()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_item(

            item_name,

            category,

            supplier,

            purchase_price,

            selling_price,

            stock_quantity,

            minimum_stock,

            gst

        ):

            return

        self.item_id.configure(state="normal")

        item_id = self.item_id.get()

        self.item_id.configure(state="disabled")

        success = self.crud.add_item(

            item_id,

            item_name,

            category,

            supplier,

            batch_no,

            float(purchase_price),

            float(selling_price),

            int(stock_quantity),

            int(minimum_stock),

            unit,

            float(gst),

            expiry_date,

            remarks

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Inventory Item added successfully."
            )

            self.load_items()

            self.clear_form()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add inventory item."
            )


    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.item_id.configure(state="normal")

        self.item_id.delete(0, "end")

        self.item_id.insert(
            0,
            self.crud.generate_item_id()
        )

        self.item_id.configure(state="disabled")

        self.item_name.delete(0, "end")

        self.category.set("Medicine")

        self.supplier.delete(0, "end")

        self.batch_no.delete(0, "end")

        self.purchase_price.delete(0, "end")

        self.selling_price.delete(0, "end")

        self.stock_quantity.delete(0, "end")

        self.minimum_stock.delete(0, "end")

        self.unit.set("Piece")

        self.gst.delete(0, "end")

        self.expiry_date.set_date(datetime.today())

        self.remarks.delete(
            "1.0",
            "end"
        )

        self.selected_item_id = None


    # ==========================================
    # Load Items
    # ==========================================

    def load_items(self):

        for item in self.inventory_table.get_children():

            self.inventory_table.delete(item)

        rows = self.crud.load_items()

        for row in rows:

            self.inventory_table.insert(

                "",

                "end",

                values=row

            )

  
    # ==========================================
    # Load Selected Item
    # ==========================================

    def load_selected_item(self, event=None):

        selected = self.inventory_table.focus()

        if not selected:
            return

        values = self.inventory_table.item(
            selected,
            "values"
        )

        item = self.crud.get_item_by_id(
            int(values[0])
        )

        if not item:
            return

        self.selected_item_id = item[0]

        self.item_id.configure(state="normal")

        self.item_id.delete(0, "end")

        self.item_id.insert(
            0,
            item[1]
        )

        self.item_id.configure(state="disabled")

        self.item_name.delete(0, "end")
        self.item_name.insert(0, item[2])

        self.category.set(item[3])

        self.supplier.delete(0, "end")
        self.supplier.insert(0, item[4])

        self.batch_no.delete(0, "end")
        self.batch_no.insert(0, item[5])

        self.purchase_price.delete(0, "end")
        self.purchase_price.insert(0, item[6])

        self.selling_price.delete(0, "end")
        self.selling_price.insert(0, item[7])

        self.stock_quantity.delete(0, "end")
        self.stock_quantity.insert(0, item[8])

        self.minimum_stock.delete(0, "end")
        self.minimum_stock.insert(0, item[9])

        self.unit.set(item[10])

        self.gst.delete(0, "end")
        self.gst.insert(0, item[11])

        self.expiry_date.delete(0, "end")
        self.expiry_date.insert(0, item[12])

        self.remarks.delete("1.0", "end")
        self.remarks.insert("1.0", item[13])

    # ==========================================
    # Update Item
    # ==========================================

    def update_item(self):

        if self.selected_item_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select an inventory item."
            )

            return

        item_name = self.item_name.get().strip()

        category = self.category.get()

        supplier = self.supplier.get().strip()

        batch_no = self.batch_no.get().strip()

        purchase_price = self.purchase_price.get().strip()

        selling_price = self.selling_price.get().strip()

        stock_quantity = self.stock_quantity.get().strip()

        minimum_stock = self.minimum_stock.get().strip()

        unit = self.unit.get()

        gst = self.gst.get().strip()

        expiry_date = self.expiry_date.get().strip()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_item(
            item_name,
            category,
            supplier,
            purchase_price,
            selling_price,
            stock_quantity,
            minimum_stock,
            gst
        ):
            return

        success = self.crud.update_item(
            self.selected_item_id,
            item_name,
            category,
            supplier,
            batch_no,
            float(purchase_price),
            float(selling_price),
            int(stock_quantity),
            int(minimum_stock),
            unit,
            float(gst),
            expiry_date,
            remarks
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Inventory Item updated successfully."
            )

            self.load_items()

            self.clear_form()

        else:

            messagebox.showerror(
                "Error",
                "Unable to update inventory item."
            )

    # ==========================================
    # Delete Item
    # ==========================================

    def delete_item(self):

        selected = self.inventory_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an inventory item."
            )

            return

        values = self.inventory_table.item(
            selected,
            "values"
        )

        item_db_id = int(values[0])

        item = self.crud.get_item_by_id(
            item_db_id
        )

        if not item:

            messagebox.showerror(
                "Error",
                "Inventory item not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this inventory item?"
        ):

            if self.crud.delete_item(
                item_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Inventory Item deleted successfully."
                )

                self.load_items()

                self.clear_form()

                self.selected_item_id = None

    # ==========================================
    # Search Item
    # ==========================================

    def search_item(self):

        keyword = self.search_entry.get().strip()

        for item in self.inventory_table.get_children():

            self.inventory_table.delete(item)

        rows = self.crud.search_item(keyword)

        for row in rows:

            self.inventory_table.insert(
                "",
                "end",
                values=row
            )
            