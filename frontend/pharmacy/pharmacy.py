"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Pharmacy Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import datetime, timedelta
from frontend.pharmacy.pharmacy_ui import PharmacyUI
from frontend.pharmacy.pharmacy_service import PharmacyService
from frontend.pharmacy.pharmacy_crud import PharmacyCRUD


class Pharmacy(PharmacyUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = PharmacyService()

        self.crud = PharmacyCRUD()

        self.bind_events()

        self.load_medicines()

        self.medicine_id.configure(state="normal")

        self.medicine_id.insert(
            0,
            self.crud.generate_medicine_id()
        )

        self.medicine_id.configure(state="disabled")

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_medicine
        )

        self.update_btn.configure(
            command=self.update_medicine
        )

        self.delete_btn.configure(
            command=self.delete_medicine
        )

        self.search_btn.configure(
            command=self.search_medicine
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.pharmacy_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_medicine
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_medicine()
        )

    # ==========================================
    # Add Medicine
    # ==========================================

    def add_medicine(self):

        medicine_name = self.medicine_name.get().strip()
        company_name = self.company_name.get().strip()
        batch_no = self.batch_no.get().strip()
        category = self.category.get()
        expiry_date = self.expiry_date.get().strip()

        purchase_price = self.purchase_price.get().strip()
        selling_price = self.selling_price.get().strip()
        stock_quantity = self.stock_quantity.get().strip()
        minimum_stock = self.minimum_stock.get().strip() or "0"

        unit = self.unit.get()
        gst = self.gst.get().strip() or "0"

        manufacturer = self.manufacturer.get().strip()
        supplier = self.supplier.get().strip()
        remarks = self.remarks.get("1.0", "end").strip()

        if not self.service.validate_medicine(
            medicine_name,
            company_name,
            batch_no,
            purchase_price,
            selling_price,
            stock_quantity
        ):
            return

        # Always generate a fresh unique ID before adding
        medicine_id = self.crud.generate_medicine_id()

        self.medicine_id.configure(state="normal")
        self.medicine_id.delete(0, "end")
        self.medicine_id.insert(0, medicine_id)
        self.medicine_id.configure(state="disabled")

        success = self.crud.add_medicine(
            medicine_id,
            medicine_name,
            company_name,
            batch_no,
            category,
            expiry_date,
            float(purchase_price),
            float(selling_price),
            int(stock_quantity),
            int(minimum_stock),
            unit,
            float(gst),
            manufacturer,
            supplier,
            remarks
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Medicine added successfully."
            )
            self.load_medicines()
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Unable to add medicine."
            )


    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.medicine_id.configure(state="normal")

        self.medicine_id.delete(0, "end")

        self.medicine_id.insert(
            0,
            self.crud.generate_medicine_id()
        )

        self.medicine_id.configure(state="disabled")

        self.medicine_name.delete(0, "end")

        self.company_name.delete(0, "end")

        self.batch_no.delete(0, "end")

        self.category.set("Tablet")

        self.expiry_date.set_date(datetime.today())

        self.purchase_price.delete(0, "end")

        self.selling_price.delete(0, "end")

        self.stock_quantity.delete(0, "end")

        self.minimum_stock.delete(0, "end")

        self.unit.set("Strip")

        self.gst.delete(0, "end")

        self.manufacturer.delete(0, "end")

        self.supplier.delete(0, "end")

        self.remarks.delete("1.0", "end")

        self.selected_medicine_id = None


    # ==========================================
    # Load Medicines
    # ==========================================

    def load_medicines(self):

        for item in self.pharmacy_table.get_children():

            self.pharmacy_table.delete(item)

        rows = self.crud.load_medicines()
        for row in rows:
            medicine = self.crud.get_medicine_by_id(row[0])

            if not medicine:
                continue

            stock = medicine[9]
            minimum = medicine[10]

            expiry = datetime.strptime(
                medicine[6],
                "%d-%m-%Y"
            )

            today = datetime.today()

            if expiry <= today + timedelta(days=30):
                self.pharmacy_table.insert(
                    "",
                    "end",
                    values=row,
                    tags=("expiry",)
                )
            elif stock <= minimum:
                self.pharmacy_table.insert(
                    "",
                    "end",
                    values=row,
                    tags=("low",)
                )
            else:
                self.pharmacy_table.insert(
                    "",
                    "end",
                    values=row
                )

        # Configure Tags
        self.pharmacy_table.tag_configure(
            "low",
            background="#FFF3CD"
        )

        self.pharmacy_table.tag_configure(
            "expiry",
            background="#FFD6D6"
        )

    # ==========================================
    # Load Selected Medicine
    # ==========================================

    def load_selected_medicine(self, event=None):

        selected = self.pharmacy_table.focus()

        if not selected:
            return

        values = self.pharmacy_table.item(
            selected,
            "values"
        )

        medicine = self.crud.get_medicine_by_id(
            values[0]
        )

        if not medicine:
            return

        self.selected_medicine_id = medicine[0]

        self.medicine_id.configure(state="normal")

        self.medicine_id.delete(0, "end")

        self.medicine_id.insert(
            0,
            medicine[1]
        )

        self.medicine_id.configure(state="disabled")

        self.medicine_name.delete(0, "end")
        self.medicine_name.insert(0, medicine[2])

        self.company_name.delete(0, "end")
        self.company_name.insert(0, medicine[3])

        self.batch_no.delete(0, "end")
        self.batch_no.insert(0, medicine[4])

        self.category.set(medicine[5])

        self.expiry_date.set_date(medicine[6])

        self.purchase_price.delete(0, "end")
        self.purchase_price.insert(0, medicine[7])

        self.selling_price.delete(0, "end")
        self.selling_price.insert(0, medicine[8])

        self.stock_quantity.delete(0, "end")
        self.stock_quantity.insert(0, medicine[9])

        self.minimum_stock.delete(0, "end")
        self.minimum_stock.insert(0, medicine[10])

        self.unit.set(medicine[11])

        self.gst.delete(0, "end")
        self.gst.insert(0, medicine[12])

        self.manufacturer.delete(0, "end")
        self.manufacturer.insert(0, medicine[13])

        self.supplier.delete(0, "end")
        self.supplier.insert(0, medicine[14])

        self.remarks.delete("1.0", "end")
        self.remarks.insert("1.0", medicine[15])

    # ==========================================
    # Update Medicine
    # ==========================================

    def update_medicine(self):
        if not hasattr(self, "selected_medicine_id"):
            messagebox.showwarning(
                "Warning",
                "Please select a medicine."
            )
            return

        medicine_name = self.medicine_name.get().strip()
        company_name = self.company_name.get().strip()
        batch_no = self.batch_no.get().strip()
        category = self.category.get()
        expiry_date = self.expiry_date.get().strip()

        purchase_price = self.purchase_price.get().strip()
        selling_price = self.selling_price.get().strip()
        stock_quantity = self.stock_quantity.get().strip()
        minimum_stock = self.minimum_stock.get().strip() or "0"

        unit = self.unit.get()
        gst = self.gst.get().strip() or "0"

        manufacturer = self.manufacturer.get().strip()
        supplier = self.supplier.get().strip()
        remarks = self.remarks.get("1.0", "end").strip()

        if not self.service.validate_medicine(
            medicine_name,
            company_name,
            batch_no,
            purchase_price,
            selling_price,
            stock_quantity
        ):
            return

        success = self.crud.update_medicine(
            self.selected_medicine_id,
            medicine_name,
            company_name,
            batch_no,
            category,
            expiry_date,
            float(purchase_price),
            float(selling_price),
            int(stock_quantity),
            int(minimum_stock),
            unit,
            float(gst),
            manufacturer,
            supplier,
            remarks
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Medicine updated successfully."
            )
            self.load_medicines()
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Unable to update medicine."
            )


    # ==========================================
    # Delete Medicine
    # ==========================================

    def delete_medicine(self):

        selected = self.pharmacy_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a medicine."
            )

            return

        values = self.pharmacy_table.item(
            selected,
            "values"
        )

        medicine_db_id = values[0]

        medicine = self.crud.get_medicine_by_id(
            medicine_db_id
        )

        if not medicine:

            messagebox.showerror(
                "Error",
                "Medicine not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this medicine?"
        ):

            if self.crud.delete_medicine(
                medicine_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Medicine deleted successfully."
                )

                self.load_medicines()

                self.clear_form()

                self.selected_medicine_id = None


    # ==========================================
    # Search Medicine
    # ==========================================

    def search_medicine(self):

        keyword = self.search_entry.get().strip()

        for item in self.pharmacy_table.get_children():

            self.pharmacy_table.delete(item)

        rows = self.crud.search_medicine(keyword)

        for row in rows:

            self.pharmacy_table.insert(
                "",
                "end",
                values=row
            )