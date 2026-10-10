"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Billing Controller
Version : 3.0
===========================================================
"""

import os
import customtkinter as ctk

from tkinter import messagebox, filedialog
from datetime import date

from frontend.billing.billing_ui import BillingUI
from frontend.billing.billing_service import BillingService
from frontend.billing.billing_crud import BillingCRUD
from frontend.settings.settings_crud import SettingsCRUD

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class Billing(BillingUI):

    # ==================================================
    # INITIALIZE
    # ==================================================

    def __init__(self, root):

        super().__init__(root)

        # ------------------------------------------------
        # Billing Service
        # ------------------------------------------------

        self.service = BillingService()

        # ------------------------------------------------
        # Billing CRUD
        # ------------------------------------------------

        self.crud = BillingCRUD()

        # ------------------------------------------------
        # Hospital Settings
        # ------------------------------------------------

        self.settings_crud = SettingsCRUD()

        self.load_hospital_settings()

        # ------------------------------------------------
        # Events
        # ------------------------------------------------

        self.bind_events()

        # ------------------------------------------------
        # Load Data
        # ------------------------------------------------

        self.load_patients()
        self.load_doctors()
        self.load_bills()

        # ------------------------------------------------
        # Generate Bill ID
        # ------------------------------------------------

        try:

            self.bill_id.configure(
                state="normal"
            )

            self.bill_id.delete(
                0,
                "end"
            )

            self.bill_id.insert(
                0,
                self.crud.generate_bill_id()
            )

            self.bill_id.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "❌ Bill ID Error:",
                e
            )


    # ==================================================
    # LOAD HOSPITAL SETTINGS
    # ==================================================

    def load_hospital_settings(self):

        try:

            data = self.settings_crud.load_settings()

            # ------------------------------------------------
            # Default Values
            # ------------------------------------------------

            self.hospital_name = "CLOUD SECURE HOSPITAL"

            self.hospital_address = ""

            self.hospital_city = ""

            self.hospital_state = ""

            self.hospital_pincode = ""

            self.hospital_phone = ""

            self.hospital_email = ""

            self.hospital_website = ""

            self.hospital_gst = ""

            self.hospital_currency = "INR"

            self.invoice_footer = "Thank You • Visit Again"

            self.hospital_logo = ""

            self.hospital_theme = "System"

            # ------------------------------------------------
            # Database Settings
            # ------------------------------------------------

            if data:

                self.hospital_name = str(
                    data[0] or self.hospital_name
                ).strip()

                self.hospital_address = str(
                    data[1] or ""
                ).strip()

                self.hospital_city = str(
                    data[2] or ""
                ).strip()

                self.hospital_state = str(
                    data[3] or ""
                ).strip()

                self.hospital_pincode = str(
                    data[4] or ""
                ).strip()

                self.hospital_phone = str(
                    data[5] or ""
                ).strip()

                self.hospital_email = str(
                    data[6] or ""
                ).strip()

                self.hospital_website = str(
                    data[7] or ""
                ).strip()

                self.hospital_gst = str(
                    data[8] or ""
                ).strip()

                self.hospital_currency = str(
                    data[9] or "INR"
                ).strip()

                self.invoice_footer = str(
                    data[10] or "Thank You • Visit Again"
                ).strip()

                self.hospital_logo = str(
                    data[11] or ""
                ).strip()

                self.hospital_theme = str(
                    data[12] or "System"
                ).strip()

            print(
                "🏥 Hospital Name:",
                self.hospital_name
            )

            print(
                "🖼 Hospital Logo:",
                self.hospital_logo
            )

        except Exception as e:

            print(
                "❌ Hospital Settings Error:",
                e
            )

            self.hospital_name = (
                "CLOUD SECURE HOSPITAL"
            )

            self.hospital_address = ""

            self.hospital_city = ""

            self.hospital_state = ""

            self.hospital_pincode = ""

            self.hospital_phone = ""

            self.hospital_email = ""

            self.hospital_website = ""

            self.hospital_gst = ""

            self.hospital_currency = "INR"

            self.invoice_footer = (
                "Thank You • Visit Again"
            )

            self.hospital_logo = ""

            self.hospital_theme = "System"


    # ==================================================
    # BIND EVENTS
    # ==================================================

    def bind_events(self):

        self.delete_btn.configure(
            command=self.delete_bill
        )

        self.search_btn.configure(
            command=self.search_bill
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_bill()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.add_btn.configure(
            command=self.add_bill
        )

        self.update_btn.configure(
            command=self.update_bill
        )

        self.billing_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_bill
        )

        self.patient.configure(
            command=self.on_patient_change
        )

        self.doctor.configure(
            command=self.on_doctor_change
        )

        self.consultation_fee.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.medicine_charges.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.lab_charges.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.other_charges.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.discount.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.gst.bind(
            "<KeyRelease>",
            self.calculate_total
        )

        self.print_btn.configure(
            command=self.print_bill
        )


    # ==================================================
    # ADD BILL
    # ==================================================

    def add_bill(self):

        print(
            "===== ADD BILL CLICKED ====="
        )

        try:

            patient = self.patient.get()

            doctor = self.doctor.get()

            bill_date = (
                self.bill_date.get().strip()
            )

            consultation_fee = (
                self.consultation_fee.get().strip()
                or "0"
            )

            medicine_charges = (
                self.medicine_charges.get().strip()
                or "0"
            )

            lab_charges = (
                self.lab_charges.get().strip()
                or "0"
            )

            other_charges = (
                self.other_charges.get().strip()
                or "0"
            )

            discount = (
                self.discount.get().strip()
                or "0"
            )

            gst = (
                self.gst.get().strip()
                or "0"
            )

            # ------------------------------------------------
            # Calculate Subtotal
            # ------------------------------------------------

            subtotal = (

                float(consultation_fee)

                + float(medicine_charges)

                + float(lab_charges)

                + float(other_charges)

                - float(discount)

            )

            # ------------------------------------------------
            # GST
            # ------------------------------------------------

            gst_amount = (
                subtotal
                * float(gst)
                / 100
            )

            # ------------------------------------------------
            # Total
            # ------------------------------------------------

            total = (
                subtotal
                + gst_amount
            )

            self.total_amount.configure(
                state="normal"
            )

            self.total_amount.delete(
                0,
                "end"
            )

            self.total_amount.insert(
                0,
                f"{total:.2f}"
            )

            self.total_amount.configure(
                state="disabled"
            )

            payment_mode = (
                self.payment_mode.get()
            )

            bill_status = (
                self.bill_status.get()
            )

            remarks = (
                self.remarks.get(
                    "1.0",
                    "end"
                ).strip()
            )

            # ------------------------------------------------
            # Validation
            # ------------------------------------------------

            if not self.service.validate_bill(
                patient,
                doctor,
                bill_date,
                str(total)
            ):
                return

            # ------------------------------------------------
            # Bill ID
            # ------------------------------------------------

            self.bill_id.configure(
                state="normal"
            )

            bill_id = self.bill_id.get()

            self.bill_id.configure(
                state="disabled"
            )

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            success = self.crud.add_bill(

                bill_id,

                patient,

                doctor,

                bill_date,

                float(
                    consultation_fee
                ),

                float(
                    medicine_charges
                ),

                float(
                    lab_charges
                ),

                float(
                    other_charges
                ),

                float(
                    discount
                ),

                total,

                payment_mode,

                bill_status,

                remarks

            )

            print(
                "CRUD Result:",
                success
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Bill added successfully."
                )

                self.load_bills()

                self.clear_form()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to add bill."
                )

        except Exception as e:

            print(
                "❌ Add Bill Error:",
                e
            )

            messagebox.showerror(
                "Error",
                str(e)
            )


    # ==================================================
    # CLEAR FORM
    # ==================================================

    def clear_form(self):

        try:

            self.patient.set("")

            self.doctor.set("")

            self.selected_bill_id = None

            # Department

            self.department.configure(
                state="normal"
            )

            self.department.delete(
                0,
                "end"
            )

            self.department.configure(
                state="disabled"
            )

            # Mobile

            self.mobile.configure(
                state="normal"
            )

            self.mobile.delete(
                0,
                "end"
            )

            self.mobile.configure(
                state="disabled"
            )

            # Age

            self.age.configure(
                state="normal"
            )

            self.age.delete(
                0,
                "end"
            )

            self.age.configure(
                state="disabled"
            )

            # Gender

            self.gender.configure(
                state="normal"
            )

            self.gender.delete(
                0,
                "end"
            )

            self.gender.configure(
                state="disabled"
            )

            # Date

            self.bill_date.set_date(
                date.today()
            )

            # Charges

            self.consultation_fee.delete(
                0,
                "end"
            )

            self.medicine_charges.delete(
                0,
                "end"
            )

            self.lab_charges.delete(
                0,
                "end"
            )

            self.other_charges.delete(
                0,
                "end"
            )

            self.discount.delete(
                0,
                "end"
            )

            self.gst.delete(
                0,
                "end"
            )

            # Total

            self.total_amount.configure(
                state="normal"
            )

            self.total_amount.delete(
                0,
                "end"
            )

            self.total_amount.configure(
                state="disabled"
            )

            # Payment

            self.payment_mode.set(
                "Cash"
            )

            self.bill_status.set(
                "Pending"
            )

            # Remarks

            self.remarks.delete(
                "1.0",
                "end"
            )

            # New Bill ID

            self.bill_id.configure(
                state="normal"
            )

            self.bill_id.delete(
                0,
                "end"
            )

            self.bill_id.insert(
                0,
                self.crud.generate_bill_id()
            )

            self.bill_id.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "❌ Clear Form Error:",
                e
            )


    # ==================================================
    # LOAD BILLS
    # ==================================================

    def load_bills(self):

        try:

            for item in (
                self.billing_table.get_children()
            ):

                self.billing_table.delete(
                    item
                )

            rows = self.crud.load_bills()

            for row in rows:

                self.billing_table.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            print(
                "❌ Load Bills Error:",
                e
            )


    # ==================================================
    # LOAD SELECTED BILL
    # ==================================================

    def load_selected_bill(
        self,
        event=None
    ):

        try:

            selected = (
                self.billing_table.focus()
            )

            if not selected:
                return

            values = (
                self.billing_table.item(
                    selected,
                    "values"
                )
            )

            if not values:
                return

            bill = (
                self.crud.get_bill_by_id(
                    values[0]
                )
            )

            if not bill:
                return

            self.selected_bill_id = bill[0]

            # Bill ID

            self.bill_id.configure(
                state="normal"
            )

            self.bill_id.delete(
                0,
                "end"
            )

            self.bill_id.insert(
                0,
                str(bill[1] or "")
            )

            self.bill_id.configure(
                state="disabled"
            )

            # Patient

            self.patient.set(
                str(bill[2] or "")
            )

            # Doctor

            self.doctor.set(
                str(bill[3] or "")
            )

            # Date

            self.bill_date.set_date(
                bill[4]
            )

            # Charges

            fields = [

                (
                    self.consultation_fee,
                    bill[5]
                ),

                (
                    self.medicine_charges,
                    bill[6]
                ),

                (
                    self.lab_charges,
                    bill[7]
                ),

                (
                    self.other_charges,
                    bill[8]
                ),

                (
                    self.discount,
                    bill[9]
                )

            ]

            for widget, value in fields:

                widget.delete(
                    0,
                    "end"
                )

                widget.insert(
                    0,
                    str(value or 0)
                )

            # Total

            self.total_amount.configure(
                state="normal"
            )

            self.total_amount.delete(
                0,
                "end"
            )

            self.total_amount.insert(
                0,
                str(bill[10] or 0)
            )

            self.total_amount.configure(
                state="disabled"
            )

            # Payment

            self.payment_mode.set(
                str(
                    bill[11]
                    or "Cash"
                )
            )

            self.bill_status.set(
                str(
                    bill[12]
                    or "Pending"
                )
            )

            # Remarks

            self.remarks.delete(
                "1.0",
                "end"
            )

            self.remarks.insert(
                "1.0",
                str(
                    bill[13]
                    or ""
                )
            )

        except Exception as e:

            print(
                "❌ Selected Bill Error:",
                e
            )


    # ==================================================
    # UPDATE BILL
    # ==================================================

    def update_bill(self):

        if not hasattr(
            self,
            "selected_bill_id"
        ) or self.selected_bill_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        try:

            patient = self.patient.get()

            doctor = self.doctor.get()

            bill_date = (
                self.bill_date.get().strip()
            )

            consultation_fee = (
                self.consultation_fee.get().strip()
                or "0"
            )

            medicine_charges = (
                self.medicine_charges.get().strip()
                or "0"
            )

            lab_charges = (
                self.lab_charges.get().strip()
                or "0"
            )

            other_charges = (
                self.other_charges.get().strip()
                or "0"
            )

            discount = (
                self.discount.get().strip()
                or "0"
            )

            gst = (
                self.gst.get().strip()
                or "0"
            )

            subtotal = (

                float(consultation_fee)

                + float(medicine_charges)

                + float(lab_charges)

                + float(other_charges)

                - float(discount)

            )

            gst_amount = (
                subtotal
                * float(gst)
                / 100
            )

            total = (
                subtotal
                + gst_amount
            )

            self.total_amount.configure(
                state="normal"
            )

            self.total_amount.delete(
                0,
                "end"
            )

            self.total_amount.insert(
                0,
                f"{total:.2f}"
            )

            self.total_amount.configure(
                state="disabled"
            )

            payment_mode = (
                self.payment_mode.get()
            )

            bill_status = (
                self.bill_status.get()
            )

            remarks = (
                self.remarks.get(
                    "1.0",
                    "end"
                ).strip()
            )

            if not self.service.validate_bill(
                patient,
                doctor,
                bill_date,
                str(total)
            ):
                return

            success = self.crud.update_bill(

                self.selected_bill_id,

                patient,

                doctor,

                bill_date,

                float(
                    consultation_fee
                ),

                float(
                    medicine_charges
                ),

                float(
                    lab_charges
                ),

                float(
                    other_charges
                ),

                float(
                    discount
                ),

                total,

                payment_mode,

                bill_status,

                remarks

            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Bill updated successfully."
                )

                self.load_bills()

                self.clear_form()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to update bill."
                )

        except Exception as e:

            print(
                "❌ Update Bill Error:",
                e
            )

            messagebox.showerror(
                "Error",
                str(e)
            )


    # ==================================================
    # DELETE BILL
    # ==================================================

    def delete_bill(self):

        selected = (
            self.billing_table.focus()
        )

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        values = (
            self.billing_table.item(
                selected,
                "values"
            )
        )

        bill_db_id = values[0]

        bill = (
            self.crud.get_bill_by_id(
                bill_db_id
            )
        )

        if not bill:

            messagebox.showerror(
                "Error",
                "Bill not found."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this bill?"
        )

        if not confirm:
            return

        try:

            success = (
                self.crud.delete_bill(
                    bill_db_id
                )
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Bill deleted successfully."
                )

                self.load_bills()

                self.clear_form()

                self.selected_bill_id = None

        except Exception as e:

            print(
                "❌ Delete Bill Error:",
                e
            )


    # ==================================================
    # SEARCH BILL
    # ==================================================

    def search_bill(self):

        try:

            keyword = (
                self.search_entry.get().strip()
            )

            for item in (
                self.billing_table.get_children()
            ):

                self.billing_table.delete(
                    item
                )

            rows = (
                self.crud.search_bill(
                    keyword
                )
            )

            for row in rows:

                self.billing_table.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            print(
                "❌ Search Bill Error:",
                e
            )


    # ==================================================
    # LOAD PATIENTS
    # ==================================================

    def load_patients(self):

        try:

            rows = (
                self.crud.load_patients()
            )

            patient_list = [
                row[0]
                for row in rows
            ]

            if not patient_list:

                patient_list = [
                    "Select Patient"
                ]

            self.patient.configure(
                values=patient_list
            )

            self.patient.set(
                patient_list[0]
            )

        except Exception as e:

            print(
                "❌ Patient Load Error:",
                e
            )


    # ==================================================
    # LOAD DOCTORS
    # ==================================================

    def load_doctors(self):

        try:

            rows = (
                self.crud.load_doctors()
            )

            doctor_list = [
                row[0]
                for row in rows
            ]

            if not doctor_list:

                doctor_list = [
                    "Select Doctor"
                ]

            self.doctor.configure(
                values=doctor_list
            )

            self.doctor.set(
                doctor_list[0]
            )

            if (
                doctor_list[0]
                != "Select Doctor"
            ):

                self.on_doctor_change(
                    doctor_list[0]
                )

        except Exception as e:

            print(
                "❌ Doctor Load Error:",
                e
            )


    # ==================================================
    # CALCULATE TOTAL
    # ==================================================

    def calculate_total(
        self,
        event=None
    ):

        try:

            consultation = float(
                self.consultation_fee.get()
                or 0
            )

            medicine = float(
                self.medicine_charges.get()
                or 0
            )

            lab = float(
                self.lab_charges.get()
                or 0
            )

            other = float(
                self.other_charges.get()
                or 0
            )

            discount = float(
                self.discount.get()
                or 0
            )

            gst = float(
                self.gst.get()
                or 0
            )

            subtotal = (
                consultation
                + medicine
                + lab
                + other
                - discount
            )

            gst_amount = (
                subtotal
                * gst
                / 100
            )

            total = (
                subtotal
                + gst_amount
            )

            self.total_amount.configure(
                state="normal"
            )

            self.total_amount.delete(
                0,
                "end"
            )

            self.total_amount.insert(
                0,
                f"{total:.2f}"
            )

            self.total_amount.configure(
                state="disabled"
            )

        except Exception:

            pass


    # ==================================================
    # DOCTOR CHANGE
    # ==================================================

    def on_doctor_change(
        self,
        doctor_name
    ):

        try:

            data = (
                self.crud.get_doctor_details(
                    doctor_name
                )
            )

            print(
                "Selected Doctor:",
                doctor_name
            )

            print(
                "Doctor Data:",
                data
            )

            if data:

                department = (
                    data[0]
                    or "Not Assigned"
                )

                fee = (
                    data[1]
                    or 0
                )

                self.department.configure(
                    state="normal"
                )

                self.department.delete(
                    0,
                    "end"
                )

                self.department.insert(
                    0,
                    department
                )

                self.department.configure(
                    state="disabled"
                )

                self.consultation_fee.delete(
                    0,
                    "end"
                )

                self.consultation_fee.insert(
                    0,
                    fee
                )

                self.calculate_total()

        except Exception as e:

            print(
                "❌ Doctor Change Error:",
                e
            )


    # ==================================================
    # PATIENT CHANGE
    # ==================================================

    def on_patient_change(
        self,
        patient_name
    ):

        try:

            data = (
                self.crud.get_patient_details(
                    patient_name
                )
            )

            print(
                "Selected Patient:",
                patient_name
            )

            print(
                "Patient Data:",
                data
            )

            if data:

                mobile, age, gender = data

                self.mobile.configure(
                    state="normal"
                )

                self.mobile.delete(
                    0,
                    "end"
                )

                self.mobile.insert(
                    0,
                    str(mobile)
                )

                self.mobile.configure(
                    state="disabled"
                )

                self.age.configure(
                    state="normal"
                )

                self.age.delete(
                    0,
                    "end"
                )

                self.age.insert(
                    0,
                    str(age)
                )

                self.age.configure(
                    state="disabled"
                )

                self.gender.configure(
                    state="normal"
                )

                self.gender.delete(
                    0,
                    "end"
                )

                self.gender.insert(
                    0,
                    str(gender)
                )

                self.gender.configure(
                    state="disabled"
                )

        except Exception as e:

            print(
                "❌ Patient Change Error:",
                e
            )


    # ==================================================
    # PRINT BILL
    # ==================================================

    def print_bill(self):

        if not hasattr(
            self,
            "selected_bill_id"
        ) or self.selected_bill_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        try:

            bill = (
                self.crud.get_bill_by_id(
                    self.selected_bill_id
                )
            )

            if not bill:

                messagebox.showerror(
                    "Error",
                    "Bill data not found."
                )

                return

            # ------------------------------------------------
            # Refresh Settings
            # ------------------------------------------------

            self.load_hospital_settings()

            # ------------------------------------------------
            # Invoice Window
            # ------------------------------------------------

            win = ctk.CTkToplevel(
                self.root
            )

            win.title(
                f"{self.hospital_name} - Invoice"
            )

            win.geometry(
                "760x820"
            )

            win.resizable(
                True,
                True
            )

            # ------------------------------------------------
            # Main Frame
            # ------------------------------------------------

            main_frame = (
                ctk.CTkScrollableFrame(
                    win
                )
            )

            main_frame.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            # ------------------------------------------------
            # Header
            # ------------------------------------------------

            header = ctk.CTkFrame(
                main_frame,
                corner_radius=10
            )

            header.pack(
                fill="x",
                padx=10,
                pady=(10, 5)
            )

            # ------------------------------------------------
            # Logo
            # ------------------------------------------------

            logo_loaded = False

            try:

                if (
                    self.hospital_logo
                    and os.path.exists(
                        self.hospital_logo
                    )
                ):

                    from PIL import Image

                    logo_image = Image.open(
                        self.hospital_logo
                    )

                    logo_image.thumbnail(
                        (100, 100)
                    )

                    self.invoice_logo = (
                        ctk.CTkImage(
                            light_image=logo_image,
                            dark_image=logo_image,
                            size=(90, 90)
                        )
                    )

                    ctk.CTkLabel(
                        header,
                        text="",
                        image=self.invoice_logo
                    ).pack(
                        pady=(15, 5)
                    )

                    logo_loaded = True

            except Exception as e:

                print(
                    "⚠ Invoice Logo Error:",
                    e
                )

            # ------------------------------------------------
            # Hospital Name
            # ------------------------------------------------

            ctk.CTkLabel(
                header,
                text=(
                    f"🏥 {self.hospital_name}"
                ),
                font=(
                    "Segoe UI",
                    28,
                    "bold"
                )
            ).pack(
                pady=(10, 5)
            )

            # ------------------------------------------------
            # Address
            # ------------------------------------------------

            address_parts = []

            if self.hospital_address:
                address_parts.append(
                    self.hospital_address
                )

            location = ", ".join(
                [
                    x
                    for x in [
                        self.hospital_city,
                        self.hospital_state,
                        self.hospital_pincode
                    ]
                    if x
                ]
            )

            if location:
                address_parts.append(
                    location
                )

            if address_parts:

                ctk.CTkLabel(
                    header,
                    text="\n".join(
                        address_parts
                    ),
                    font=(
                        "Segoe UI",
                        12
                    ),
                    wraplength=650
                ).pack(
                    pady=3
                )

            # ------------------------------------------------
            # Contact
            # ------------------------------------------------

            contact_parts = []

            if self.hospital_phone:

                contact_parts.append(
                    f"Phone: {self.hospital_phone}"
                )

            if self.hospital_email:

                contact_parts.append(
                    f"Email: {self.hospital_email}"
                )

            if contact_parts:

                ctk.CTkLabel(
                    header,
                    text=" | ".join(
                        contact_parts
                    ),
                    font=(
                        "Segoe UI",
                        11
                    )
                ).pack(
                    pady=3
                )

            ctk.CTkLabel(
                header,
                text=(
                    "Hospital Management & "
                    "Accounting ERP"
                ),
                font=(
                    "Segoe UI",
                    14
                )
            ).pack(
                pady=5
            )

            ctk.CTkLabel(
                header,
                text="Medical Billing Invoice",
                font=(
                    "Segoe UI",
                    13
                )
            ).pack(
                pady=(0, 15)
            )

            # ------------------------------------------------
            # Bill Information
            # ------------------------------------------------

            details = ctk.CTkFrame(
                main_frame,
                corner_radius=10
            )

            details.pack(
                fill="x",
                padx=10,
                pady=5
            )

            ctk.CTkLabel(
                details,
                text=(
                    f"Bill ID : {bill[1]}"
                ),
                font=(
                    "Segoe UI",
                    14,
                    "bold"
                )
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=10,
                sticky="w"
            )

            ctk.CTkLabel(
                details,
                text=(
                    f"Date : {bill[4]}"
                ),
                font=(
                    "Segoe UI",
                    14
                )
            ).grid(
                row=0,
                column=1,
                padx=20,
                pady=10,
                sticky="e"
            )

            ctk.CTkLabel(
                details,
                text=(
                    f"Patient : {bill[2]}"
                ),
                font=(
                    "Segoe UI",
                    14
                )
            ).grid(
                row=1,
                column=0,
                padx=20,
                pady=10,
                sticky="w"
            )

            ctk.CTkLabel(
                details,
                text=(
                    f"Doctor : {bill[3]}"
                ),
                font=(
                    "Segoe UI",
                    14
                )
            ).grid(
                row=1,
                column=1,
                padx=20,
                pady=10,
                sticky="e"
            )

            details.grid_columnconfigure(
                0,
                weight=1
            )

            details.grid_columnconfigure(
                1,
                weight=1
            )

            # ------------------------------------------------
            # Bill Details
            # ------------------------------------------------

            charges = ctk.CTkFrame(
                main_frame,
                corner_radius=10
            )

            charges.pack(
                fill="x",
                padx=10,
                pady=10
            )

            ctk.CTkLabel(
                charges,
                text="BILL DETAILS",
                font=(
                    "Segoe UI",
                    18,
                    "bold"
                )
            ).grid(
                row=0,
                column=0,
                columnspan=2,
                pady=15
            )

            items = [

                (
                    "Consultation Fee",
                    bill[5]
                ),

                (
                    "Medicine Charges",
                    bill[6]
                ),

                (
                    "Laboratory Charges",
                    bill[7]
                ),

                (
                    "Other Charges",
                    bill[8]
                ),

                (
                    "Discount",
                    bill[9]
                )

            ]

            for row_no, (
                name,
                amount
            ) in enumerate(
                items,
                start=1
            ):

                ctk.CTkLabel(
                    charges,
                    text=name,
                    font=(
                        "Segoe UI",
                        14
                    )
                ).grid(
                    row=row_no,
                    column=0,
                    padx=25,
                    pady=7,
                    sticky="w"
                )

                try:

                    amount_value = float(
                        amount or 0
                    )

                except:

                    amount_value = 0.0

                ctk.CTkLabel(
                    charges,
                    text=(
                        f"{self.hospital_currency} "
                        f"{amount_value:,.2f}"
                    ),
                    font=(
                        "Segoe UI",
                        14
                    )
                ).grid(
                    row=row_no,
                    column=1,
                    padx=25,
                    pady=7,
                    sticky="e"
                )

            charges.grid_columnconfigure(
                0,
                weight=1
            )

            charges.grid_columnconfigure(
                1,
                weight=1
            )

            # ------------------------------------------------
            # Grand Total
            # ------------------------------------------------

            total_frame = ctk.CTkFrame(
                main_frame,
                corner_radius=10
            )

            total_frame.pack(
                fill="x",
                padx=10,
                pady=5
            )

            try:

                total_value = float(
                    bill[10] or 0
                )

            except:

                total_value = 0.0

            ctk.CTkLabel(
                total_frame,
                text="GRAND TOTAL",
                font=(
                    "Segoe UI",
                    20,
                    "bold"
                )
            ).pack(
                side="left",
                padx=25,
                pady=15
            )

            ctk.CTkLabel(
                total_frame,
                text=(
                    f"{self.hospital_currency} "
                    f"{total_value:,.2f}"
                ),
                font=(
                    "Segoe UI",
                    22,
                    "bold"
                )
            ).pack(
                side="right",
                padx=25,
                pady=15
            )

            # ------------------------------------------------
            # Payment
            # ------------------------------------------------

            payment_frame = ctk.CTkFrame(
                main_frame,
                corner_radius=10
            )

            payment_frame.pack(
                fill="x",
                padx=10,
                pady=10
            )

            ctk.CTkLabel(
                payment_frame,
                text=(
                    f"Payment Mode : {bill[11]}"
                ),
                font=(
                    "Segoe UI",
                    14
                )
            ).pack(
                side="left",
                padx=20,
                pady=12
            )

            ctk.CTkLabel(
                payment_frame,
                text=(
                    f"Status : {bill[12]}"
                ),
                font=(
                    "Segoe UI",
                    14,
                    "bold"
                )
            ).pack(
                side="right",
                padx=20,
                pady=12
            )

            # ------------------------------------------------
            # Remarks
            # ------------------------------------------------

            if bill[13]:

                ctk.CTkLabel(
                    main_frame,
                    text=(
                        f"Remarks : {bill[13]}"
                    ),
                    font=(
                        "Segoe UI",
                        12
                    ),
                    wraplength=650,
                    justify="left"
                ).pack(
                    padx=15,
                    pady=5,
                    anchor="w"
                )

            # ------------------------------------------------
            # Footer
            # ------------------------------------------------

            ctk.CTkLabel(
                main_frame,
                text=(
                    self.invoice_footer
                    or "Thank You • Visit Again"
                ),
                font=(
                    "Segoe UI",
                    15,
                    "bold"
                )
            ).pack(
                pady=15
            )

            # ------------------------------------------------
            # Buttons
            # ------------------------------------------------

            button_frame = ctk.CTkFrame(
                main_frame
            )

            button_frame.pack(
                fill="x",
                padx=10,
                pady=10
            )

            ctk.CTkButton(
                button_frame,
                text="🖨 Print",
                width=220,
                height=40,
                command=lambda: (
                    self.windows_print(
                        self.create_invoice_text(
                            bill
                        )
                    )
                )
            ).pack(
                side="left",
                padx=20,
                pady=10
            )

            ctk.CTkButton(
                button_frame,
                text="📄 Save PDF",
                width=220,
                height=40,
                command=lambda: (
                    self.save_pdf(
                        self.create_invoice_text(
                            bill
                        )
                    )
                )
            ).pack(
                side="right",
                padx=20,
                pady=10
            )

        except Exception as e:

            print(
                "❌ Invoice Error:",
                e
            )

            messagebox.showerror(
                "Invoice Error",
                str(e)
            )


    # ==================================================
    # CREATE INVOICE TEXT
    # ==================================================

    def create_invoice_text(
        self,
        bill
    ):

        try:

            consultation = float(
                bill[5] or 0
            )

        except:

            consultation = 0.0

        try:

            medicine = float(
                bill[6] or 0
            )

        except:

            medicine = 0.0

        try:

            laboratory = float(
                bill[7] or 0
            )

        except:

            laboratory = 0.0

        try:

            other = float(
                bill[8] or 0
            )

        except:

            other = 0.0

        try:

            discount = float(
                bill[9] or 0
            )

        except:

            discount = 0.0

        try:

            total = float(
                bill[10] or 0
            )

        except:

            total = 0.0

        # ------------------------------------------------
        # Contact Information
        # ------------------------------------------------

        contact_lines = []

        if self.hospital_address:

            contact_lines.append(
                self.hospital_address
            )

        location = ", ".join(
            [
                x
                for x in [
                    self.hospital_city,
                    self.hospital_state,
                    self.hospital_pincode
                ]
                if x
            ]
        )

        if location:

            contact_lines.append(
                location
            )

        if self.hospital_phone:

            contact_lines.append(
                f"Phone: {self.hospital_phone}"
            )

        if self.hospital_email:

            contact_lines.append(
                f"Email: {self.hospital_email}"
            )

        contact_text = "\n".join(
            contact_lines
        )

        # ------------------------------------------------
        # Invoice
        # ------------------------------------------------

        invoice = f"""
==================================================
              {self.hospital_name}
       Hospital Management & Accounting ERP
                MEDICAL INVOICE
==================================================

{contact_text}

Bill ID       : {bill[1]}
Bill Date     : {bill[4]}

Patient Name  : {bill[2]}
Doctor Name   : {bill[3]}

--------------------------------------------------
BILL DETAILS
--------------------------------------------------

Consultation Fee       : {self.hospital_currency} {consultation:,.2f}
Medicine Charges       : {self.hospital_currency} {medicine:,.2f}
Laboratory Charges     : {self.hospital_currency} {laboratory:,.2f}
Other Charges          : {self.hospital_currency} {other:,.2f}
Discount               : {self.hospital_currency} {discount:,.2f}

--------------------------------------------------

GRAND TOTAL            : {self.hospital_currency} {total:,.2f}

--------------------------------------------------

Payment Mode           : {bill[11]}
Payment Status         : {bill[12]}

Remarks                : {bill[13] or ""}

==================================================

              {self.invoice_footer or "Thank You • Visit Again"}

==================================================
"""

        return invoice


    # ==================================================
    # WINDOWS PRINT
    # ==================================================

    def windows_print(
        self,
        invoice
    ):

        print(invoice)

        messagebox.showinfo(
            "Print",
            "Printing feature will be connected next."
        )


    # ==================================================
    # SAVE PDF
    # ==================================================

    def save_pdf(
        self,
        invoice
    ):

        safe_name = (
            self.hospital_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
        )

        file = (
            filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[
                    (
                        "PDF Files",
                        "*.pdf"
                    )
                ],
                initialfile=(
                    f"{safe_name}_Invoice.pdf"
                )
            )
        )

        if not file:
            return

        try:

            styles = (
                getSampleStyleSheet()
            )

            pdf = SimpleDocTemplate(

                file,

                pagesize=A4,

                rightMargin=40,

                leftMargin=40,

                topMargin=40,

                bottomMargin=40

            )

            story = []

            for line in invoice.split(
                "\n"
            ):

                line = line.strip()

                if not line:

                    story.append(
                        Paragraph(
                            "&nbsp;",
                            styles["Normal"]
                        )
                    )

                    continue

                # ------------------------------------------------
                # Escape HTML
                # ------------------------------------------------

                line = (
                    line
                    .replace(
                        "&",
                        "&amp;"
                    )
                    .replace(
                        "<",
                        "&lt;"
                    )
                    .replace(
                        ">",
                        "&gt;"
                    )
                )

                story.append(
                    Paragraph(
                        line,
                        styles["Normal"]
                    )
                )

            pdf.build(
                story
            )

            messagebox.showinfo(
                "Success",
                "Invoice PDF Saved Successfully."
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            messagebox.showerror(
                "PDF Error",
                f"Unable to save PDF.\n\n{e}"
            )