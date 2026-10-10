"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Billing Controller
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from frontend.billing.billing_ui import BillingUI
from frontend.billing.billing_service import BillingService
from frontend.billing.billing_crud import BillingCRUD
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import filedialog


class Billing(BillingUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = BillingService()

        self.crud = BillingCRUD()

        self.bind_events()


        self.load_patients()
        self.load_doctors()


        self.load_bills()

        self.bill_id.configure(state="normal")

        self.bill_id.insert(
            0,
            self.crud.generate_bill_id()
        )

        self.bill_id.configure(state="disabled")

    # ==========================================
    # Bind Events
    # ==========================================
    def bind_events(self):

        self.delete_btn.configure(command=self.delete_bill)
        self.search_btn.configure(command=self.search_bill)
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_bill()
        )
        self.clear_btn.configure(command=self.clear_form)

        self.add_btn.configure(command=self.add_bill)
        self.update_btn.configure(command=self.update_bill)

        self.billing_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_bill
        )

        self.patient.configure(command=self.on_patient_change)
        self.doctor.configure(command=self.on_doctor_change)

        self.consultation_fee.bind("<KeyRelease>", self.calculate_total)
        self.medicine_charges.bind("<KeyRelease>", self.calculate_total)
        self.lab_charges.bind("<KeyRelease>", self.calculate_total)
        self.other_charges.bind("<KeyRelease>", self.calculate_total)
        self.discount.bind("<KeyRelease>", self.calculate_total)
        self.gst.bind("<KeyRelease>", self.calculate_total)

        self.print_btn.configure(command=self.print_bill)

    # ==========================================
    # Add Bill
    # ==========================================
    def add_bill(self):
        print("===== ADD BILL CLICKED =====")
        patient = self.patient.get()
        doctor = self.doctor.get()
        bill_date = self.bill_date.get().strip()

        consultation_fee = self.consultation_fee.get().strip() or "0"
        medicine_charges = self.medicine_charges.get().strip() or "0"
        lab_charges = self.lab_charges.get().strip() or "0"
        other_charges = self.other_charges.get().strip() or "0"
        discount = self.discount.get().strip() or "0"

        gst = self.gst.get().strip() or "0"

        subtotal = (
            float(consultation_fee)
            + float(medicine_charges)
            + float(lab_charges)
            + float(other_charges)
            - float(discount)
        )

        gst_amount = subtotal * float(gst) / 100

        total = subtotal + gst_amount

        self.total_amount.configure(state="normal")
        self.total_amount.delete(0, "end")
        self.total_amount.insert(0, f"{total:.2f}")
        self.total_amount.configure(state="disabled")

        payment_mode = self.payment_mode.get()
        bill_status = self.bill_status.get()
        remarks = self.remarks.get("1.0", "end").strip()
        print("Validation Start")

        if not self.service.validate_bill(
            patient,
            doctor,
            bill_date,
            str(total)
        ):
            return
        print("Validation Passed")

        self.bill_id.configure(state="normal")
        bill_id = self.bill_id.get()
        self.bill_id.configure(state="disabled")
        print("Patient :", patient)
        print("Doctor :", doctor)
        print("Bill Date :", bill_date)
        print("Total :", total)
        print("Calling CRUD add_bill()...")
        
        success = self.crud.add_bill(
            bill_id,
            patient,
            doctor,
            bill_date,
            float(consultation_fee),
            float(medicine_charges),
            float(lab_charges),
            float(other_charges),
            float(discount),
            total,
            payment_mode,
            bill_status,
            remarks
        )
        print("CRUD Result:", success)

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

    # ==========================================
    # Clear Form
    # ==========================================
    def clear_form(self):
        try:
            self.patient.set("")
            self.doctor.set("")

            self.selected_bill_id = None

            # ==============================
            # Department
            # ==============================
            self.department.configure(state="normal")
            self.department.delete(0, "end")
            self.department.configure(state="disabled")

            # ==============================
            # Mobile
            # ==============================
            self.mobile.configure(state="normal")
            self.mobile.delete(0, "end")
            self.mobile.configure(state="disabled")

            # ==============================
            # Age
            # ==============================
            self.age.configure(state="normal")
            self.age.delete(0, "end")
            self.age.configure(state="disabled")

            # ==============================
            # Gender
            # ==============================
            self.gender.configure(state="normal")
            self.gender.delete(0, "end")
            self.gender.configure(state="disabled")

            # ==============================
            # Date
            # ==============================
            self.bill_date.set_date(date.today())

            # ==============================
            # Charges
            # ==============================
            self.consultation_fee.delete(0, "end")
            self.medicine_charges.delete(0, "end")
            self.lab_charges.delete(0, "end")
            self.other_charges.delete(0, "end")
            self.discount.delete(0, "end")
            self.gst.delete(0, "end")

            # ==============================
            # Total Amount
            # ==============================
            self.total_amount.configure(state="normal")
            self.total_amount.delete(0, "end")
            self.total_amount.configure(state="disabled")

            # ==============================
            # Payment Mode
            # ==============================
            self.payment_mode.set("Cash")

            # ==============================
            # Bill Status
            # ==============================
            self.bill_status.set("Pending")

            # ==============================
            # Remarks
            # ==============================
            self.remarks.delete("1.0", "end")

            # ==============================
            # Selected Bill Reset
            # ==============================
        except Exception as e:
            print("❌ Clear Form Error:", e)

    # ==========================================

    def load_bills(self):

        for item in self.billing_table.get_children():

            self.billing_table.delete(item)

        rows = self.crud.load_bills()

        for row in rows:

            self.billing_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Load Selected Bill
    # ==========================================

    def load_selected_bill(self, event=None):

        selected = self.billing_table.focus()

        if not selected:
            return

        values = self.billing_table.item(
            selected,
            "values"
        )

        if not values:
            return

        bill = self.crud.get_bill_by_id(values[0])

        if not bill:
            return

        self.selected_bill_id = bill[0]

        # ==========================================
        # Bill ID
        # ==========================================

        self.bill_id.configure(state="normal")
        self.bill_id.delete(0, "end")
        self.bill_id.insert(0, str(bill[1] or ""))
        self.bill_id.configure(state="disabled")

        # ==========================================
        # Patient - CTkComboBox
        # ==========================================

        self.patient.set(
            str(bill[2] or "")
        )

        # ==========================================
        # Doctor - CTkComboBox
        # ==========================================

        self.doctor.set(
            str(bill[3] or "")
        )

        # ==========================================
        # Bill Date
        # ==========================================

        self.bill_date.set_date(bill[4])

        # ==========================================
        # Charges
        # ==========================================

        self.consultation_fee.delete(0, "end")
        self.consultation_fee.insert(
            0,
            str(bill[5] or 0)
        )

        self.medicine_charges.delete(0, "end")
        self.medicine_charges.insert(
            0,
            str(bill[6] or 0)
        )

        self.lab_charges.delete(0, "end")
        self.lab_charges.insert(
            0,
            str(bill[7] or 0)
        )

        self.other_charges.delete(0, "end")
        self.other_charges.insert(
            0,
            str(bill[8] or 0)
        )

        self.discount.delete(0, "end")
        self.discount.insert(
            0,
            str(bill[9] or 0)
        )

        # ==========================================
        # Total
        # ==========================================

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

        # ==========================================
        # Payment / Status
        # ==========================================

        self.payment_mode.set(
            str(bill[11] or "Cash")
        )

        self.bill_status.set(
            str(bill[12] or "Pending")
        )

        # ==========================================
        # Remarks
        # ==========================================

        self.remarks.delete(
            "1.0",
            "end"
        )

        self.remarks.insert(
            "1.0",
            str(bill[13] or "")
        )


    # ==========================================
    # Update Bill
    # ==========================================

    def update_bill(self):
        if not hasattr(self, "selected_bill_id") or self.selected_bill_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        patient = self.patient.get()
        doctor = self.doctor.get()
        bill_date = self.bill_date.get().strip()

        consultation_fee = self.consultation_fee.get().strip() or "0"
        medicine_charges = self.medicine_charges.get().strip() or "0"
        lab_charges = self.lab_charges.get().strip() or "0"
        other_charges = self.other_charges.get().strip() or "0"
        discount = self.discount.get().strip() or "0"
        gst = self.gst.get().strip() or "0"

        subtotal = (
            float(consultation_fee)
            + float(medicine_charges)
            + float(lab_charges)
            + float(other_charges)
            - float(discount)
        )

        gst_amount = subtotal * float(gst) / 100

        total = subtotal + gst_amount

        self.total_amount.configure(state="normal")
        self.total_amount.delete(0, "end")
        self.total_amount.insert(0, f"{total:.2f}")
        self.total_amount.configure(state="disabled")

        payment_mode = self.payment_mode.get()
        bill_status = self.bill_status.get()
        remarks = self.remarks.get("1.0", "end").strip()

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

            float(consultation_fee),

            float(medicine_charges),

            float(lab_charges),

            float(other_charges),

            float(discount),

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


    # ==========================================
    # Delete Bill
    # ==========================================

    def delete_bill(self):

        selected = self.billing_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        values = self.billing_table.item(
            selected,
            "values"
        )

        bill_db_id = values[0]

        bill = self.crud.get_bill_by_id(bill_db_id)

        if not bill:

            messagebox.showerror(
                "Error",
                "Bill not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this bill?"
        ):

            if self.crud.delete_bill(
                bill_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Bill deleted successfully."
                )

                self.load_bills()

                self.clear_form()

                self.selected_bill_id = None


    # ==========================================
    # Search Bill
    # ==========================================

    def search_bill(self):

        keyword = self.search_entry.get().strip()

        for item in self.billing_table.get_children():

            self.billing_table.delete(item)

        rows = self.crud.search_bill(keyword)

        for row in rows:

            self.billing_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Load Patients
    # ==========================================

    def load_patients(self):

        rows = self.crud.load_patients()

        patient_list = [row[0] for row in rows]

        if not patient_list:
            patient_list = ["Select Patient"]

        self.patient.configure(values=patient_list)
        self.patient.set(patient_list[0])
       
    # ==========================================
    # Load Doctors
    # ==========================================

    def load_doctors(self):

        rows = self.crud.load_doctors()

        doctor_list = [row[0] for row in rows]

        if not doctor_list:
            doctor_list = ["Select Doctor"]

        self.doctor.configure(values=doctor_list)
        self.doctor.set(doctor_list[0])

        # Load Department & Consultation Fee
        if doctor_list[0] != "Select Doctor":
            self.on_doctor_change(doctor_list[0])

    # ==========================================
    # Calculate Total
    # ==========================================

    def calculate_total(self, event=None):

        try:

            consultation = float(self.consultation_fee.get() or 0)
            medicine = float(self.medicine_charges.get() or 0)
            lab = float(self.lab_charges.get() or 0)
            other = float(self.other_charges.get() or 0)
            discount = float(self.discount.get() or 0)

            gst = float(self.gst.get() or 0)

            subtotal = consultation + medicine + lab + other - discount

            gst_amount = subtotal * gst / 100

            total = subtotal + gst_amount

            self.total_amount.configure(state="normal")
            self.total_amount.delete(0, "end")
            self.total_amount.insert(0, f"{total:.2f}")
            self.total_amount.configure(state="disabled")

        except Exception:
            pass

    def on_doctor_change(self, doctor_name):

        data = self.crud.get_doctor_details(doctor_name)
        print("Selected Doctor:", doctor_name)

        data = self.crud.get_doctor_details(doctor_name)

        print("Doctor Data:", data)

        if data:

            department = data[0] or "Not Assigned"
            fee = data[1] or 0

            self.department.configure(state="normal")
            self.department.delete(0, "end")
            self.department.insert(0, department)
            self.department.configure(state="disabled")

            self.consultation_fee.delete(0, "end")
            self.consultation_fee.insert(0, fee)

            self.calculate_total()

    # ==========================================
    # Patient Change
    # ==========================================

    def on_patient_change(self, patient_name):

        data = self.crud.get_patient_details(patient_name)
        print("Selected Patient:", patient_name)

        data = self.crud.get_patient_details(patient_name)

        print("Patient Data:", data)

        if data:
            mobile, age, gender = data

            self.mobile.configure(state="normal")
            self.mobile.delete(0, "end")
            self.mobile.insert(0, str(mobile))
            self.mobile.configure(state="disabled")

            self.age.configure(state="normal")
            self.age.delete(0, "end")
            self.age.insert(0, str(age))
            self.age.configure(state="disabled")

            self.gender.configure(state="normal")
            self.gender.delete(0, "end")
            self.gender.insert(0, str(gender))
            self.gender.configure(state="disabled")

       # ==========================================
    # Print Bill
    # ==========================================

    def print_bill(self):

        # Check selected bill
        if not hasattr(self, "selected_bill_id") or self.selected_bill_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        # Get bill from database
        bill = self.crud.get_bill_by_id(
            self.selected_bill_id
        )

        if not bill:

            messagebox.showerror(
                "Error",
                "Bill data not found."
            )

            return

        # ==========================================
        # Invoice Window
        # ==========================================

        win = ctk.CTkToplevel(self.root)

        win.title("Hospital Invoice")

        win.geometry("760x820")

        win.resizable(True, True)

        # ==========================================
        # Main Scrollable Frame
        # ==========================================

        main_frame = ctk.CTkScrollableFrame(
            win
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Hospital Header
        # ==========================================

        header = ctk.CTkFrame(
            main_frame,
            corner_radius=10
        )

        header.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            header,
            text="🏥 CLOUD SECURE HOSPITAL",
            font=("Segoe UI", 28, "bold")
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            header,
            text="Hospital Management & Accounting ERP",
            font=("Segoe UI", 14)
        ).pack(
            pady=(0, 5)
        )

        ctk.CTkLabel(
            header,
            text="Medical Billing Invoice",
            font=("Segoe UI", 13)
        ).pack(
            pady=(0, 15)
        )

        # ==========================================
        # Bill Information
        # ==========================================

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
            text=f"Bill ID : {bill[1]}",
            font=("Segoe UI", 14, "bold")
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        ctk.CTkLabel(
            details,
            text=f"Date : {bill[4]}",
            font=("Segoe UI", 14)
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=10,
            sticky="e"
        )

        ctk.CTkLabel(
            details,
            text=f"Patient : {bill[2]}",
            font=("Segoe UI", 14)
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        ctk.CTkLabel(
            details,
            text=f"Doctor : {bill[3]}",
            font=("Segoe UI", 14)
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

        # ==========================================
        # Bill Details
        # ==========================================

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
            font=("Segoe UI", 18, "bold")
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

        for row_no, (name, amount) in enumerate(
            items,
            start=1
        ):

            ctk.CTkLabel(
                charges,
                text=name,
                font=("Segoe UI", 14)
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
                text=f"₹ {amount_value:,.2f}",
                font=("Segoe UI", 14)
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

        # ==========================================
        # Grand Total
        # ==========================================

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
            font=("Segoe UI", 20, "bold")
        ).pack(
            side="left",
            padx=25,
            pady=15
        )

        ctk.CTkLabel(
            total_frame,
            text=f"₹ {total_value:,.2f}",
            font=("Segoe UI", 22, "bold")
        ).pack(
            side="right",
            padx=25,
            pady=15
        )

        # ==========================================
        # Payment Information
        # ==========================================

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
            text=f"Payment Mode : {bill[11]}",
            font=("Segoe UI", 14)
        ).pack(
            side="left",
            padx=20,
            pady=12
        )

        ctk.CTkLabel(
            payment_frame,
            text=f"Status : {bill[12]}",
            font=("Segoe UI", 14, "bold")
        ).pack(
            side="right",
            padx=20,
            pady=12
        )

        # ==========================================
        # Remarks
        # ==========================================

        if bill[13]:

            ctk.CTkLabel(
                main_frame,
                text=f"Remarks : {bill[13]}",
                font=("Segoe UI", 12),
                wraplength=650,
                justify="left"
            ).pack(
                padx=15,
                pady=5,
                anchor="w"
            )

        # ==========================================
        # Thank You
        # ==========================================

        ctk.CTkLabel(
            main_frame,
            text="Thank You • Visit Again",
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=15
        )

        # ==========================================
        # Buttons
        # ==========================================

        button_frame = ctk.CTkFrame(
            main_frame
        )

        button_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Print Button

        ctk.CTkButton(
            button_frame,
            text="🖨 Print",
            width=220,
            height=40,
            command=lambda: self.windows_print(
                self.create_invoice_text(bill)
            )
        ).pack(
            side="left",
            padx=20,
            pady=10
        )

        # PDF Button

        ctk.CTkButton(
            button_frame,
            text="📄 Save PDF",
            width=220,
            height=40,
            command=lambda: self.save_pdf(
                self.create_invoice_text(bill)
            )
        ).pack(
            side="right",
            padx=20,
            pady=10
        )


    # ==========================================
    # Create Invoice Text
    # ==========================================

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

        invoice = f"""
==================================================
              CLOUD SECURE HOSPITAL
       Hospital Management & Accounting ERP
               MEDICAL INVOICE
==================================================

Bill ID       : {bill[1]}
Bill Date     : {bill[4]}

Patient Name  : {bill[2]}
Doctor Name   : {bill[3]}

--------------------------------------------------
BILL DETAILS
--------------------------------------------------

Consultation Fee       : ₹ {consultation:,.2f}
Medicine Charges       : ₹ {medicine:,.2f}
Laboratory Charges     : ₹ {laboratory:,.2f}
Other Charges          : ₹ {other:,.2f}
Discount               : ₹ {discount:,.2f}

--------------------------------------------------

GRAND TOTAL            : ₹ {total:,.2f}

--------------------------------------------------

Payment Mode           : {bill[11]}
Payment Status         : {bill[12]}

Remarks                : {bill[13] or ""}

==================================================

                 Thank You
                 Visit Again

==================================================
"""

        return invoice


    # ==========================================
    # Windows Print
    # ==========================================

    def windows_print(
        self,
        invoice
    ):

        print(invoice)

        messagebox.showinfo(
            "Print",
            "Printing feature will be connected next."
        )


    # ==========================================
    # Save PDF
    # ==========================================

    def save_pdf(
        self,
        invoice
    ):

        file = filedialog.asksaveasfilename(

            defaultextension=".pdf",

            filetypes=[
                ("PDF Files", "*.pdf")
            ],

            initialfile="Hospital_Invoice.pdf"
        )

        if not file:

            return

        try:

            styles = getSampleStyleSheet()

            pdf = SimpleDocTemplate(
                file,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            story = []

            for line in invoice.split("\n"):

                line = line.strip()

                if not line:

                    story.append(
                        Paragraph(
                            "&nbsp;",
                            styles["Normal"]
                        )
                    )

                    continue

                # Escape special HTML characters
                line = (
                    line
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
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
