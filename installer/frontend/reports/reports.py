"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Reports Controller
Version : 2.0
===========================================================
"""
import os
import webbrowser
from tempfile import NamedTemporaryFile
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import filedialog
from openpyxl import Workbook
from openpyxl.styles import Font
from tkinter import messagebox
from datetime import date
from frontend.reports.reports_ui import ReportsUI
from frontend.reports.reports_service import ReportsService
from frontend.reports.reports_crud import ReportsCRUD


class Reports(ReportsUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = ReportsService()

        self.crud = ReportsCRUD()

        self.bind_events()

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.generate_btn.configure(
            command=self.generate_report
        )

        self.export_btn.configure(
            command=self.export_report
        )

        self.print_btn.configure(
            command=self.print_report
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.search_btn.configure(
            command=self.search_report
        )

    # ==========================================
    # Generate Report
    # ==========================================

    def generate_report(self):
        report_type = self.report_type.get()
        from_date = self.from_date.get_date().strftime("%d-%m-%Y")
        to_date = self.to_date.get_date().strftime("%d-%m-%Y")
        department = self.department.get()
        export_format = self.export_format.get()

        if not self.service.validate_report(
                report_type,
                from_date,
                to_date,
                department,
                export_format
        ):
            return

        # Clear Existing Data
        for item in self.report_table.get_children():
            self.report_table.delete(item)

        # Report Mapping
        report_methods = {
            "Patient Report": self.crud.load_patient_report,
            "Doctor Report": lambda: self.crud.load_doctor_report(
                from_date,
                to_date,
                department
       ),
            "Appointment Report": lambda: self.crud.load_appointment_report(
                from_date,
                to_date,
                department
     ),
           "OPD Report": lambda: self.crud.load_opd_report(
                from_date,
                to_date,
                department
       ),
            "IPD Report": self.crud.load_ipd_report,
            "Billing Report": self.crud.load_billing_report,
            "Pharmacy Report": self.crud.load_pharmacy_report,
            "Laboratory Report": self.crud.load_laboratory_report,
            "Inventory Report": self.crud.load_inventory_report,
            "Accounts Report": self.crud.load_accounts_report
        }

        # Patient Report With Filter
        if report_type == "Patient Report":
            rows = self.crud.load_patient_report(
                from_date,
                to_date,
                department
            )
        else:
            rows = report_methods.get(
                report_type,
                lambda: []
            )()

        if report_type == "Patient Report":
            columns = (
                "Patient ID",
                "Registration No",
                "Patient Name",
                "Gender",
                "Age",
                "Mobile",
                "Department",
                "Created At"
            )
        elif report_type == "Doctor Report":
            columns = (
                "Doctor ID",
                "Doctor Name",
                "Specialization",
                "Qualification",
                "Mobile",
                "Consultation Fee"
            )
        elif report_type == "Appointment Report":
            columns = (
                "Appointment ID",
                "Patient",
                "Doctor",
                "Department",
                "Date",
                "Time",
                "Token",
                "Status"
            )
        elif report_type == "OPD Report":
            columns = (
                "OPD ID",
                "Patient",
                "Doctor",
                "Department",
                "Visit Date",
                "Visit Time",
                "Diagnosis",
                "Status"
            )
        elif report_type == "IPD Report":
            columns = (
                "IPD ID",
                "Patient",
                "Doctor",
                "Ward",
                "Room",
                "Admission",
                "Discharge",
                "Status"
            )
        elif report_type == "Billing Report":
            columns = (
                "Bill ID",
                "Patient",
                "Doctor",
                "Bill Date",
                "Total",
                "Discount",
                "Net Amount",
                "Payment Status"
            )
        elif report_type == "Pharmacy Report":
            columns = (
                "Medicine ID",
                "Medicine Name",
                "Company",
                "Category",
                "Stock",
                "Price",
                "Expiry Date"
            )
        elif report_type == "Laboratory Report":
            columns = (
                "Test ID",
                "Test Name",
                "Patient",
                "Doctor",
                "Department",
                "Test Fee",
                "Status"
            )
        elif report_type == "Inventory Report":
            columns = (
                "Item ID",
                "Item Name",
                "Category",
                "Supplier",
                "Stock",
                "Price",
                "Expiry"
            )
        elif report_type == "Accounts Report":
            columns = (
                "Transaction ID",
                "Type",
                "Category",
                "Amount",
                "Payment Mode",
                "Date"
            )
        else:
            columns = ()

        self.report_table.config(columns=columns)
        self.report_table["show"] = "headings"

        for col in columns:
            self.report_table.heading(col, text=col)
            self.report_table.column(col, width=120, anchor="center")

        # Insert Data
        for row in rows:
            self.report_table.insert("", "end", values=row)

        self.total_records.configure(
            text=f"Total Records : {len(rows)}"
        )

        self.update_summary()
        messagebox.showinfo(
            "Success",
            f"{report_type} generated successfully."
        )


    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):
        self.report_type.set("Patient Report")
        self.from_date.set_date(date.today())
        self.to_date.set_date(date.today())
        self.department.set("All Departments")
        self.export_format.set("Screen Preview")

        for item in self.report_table.get_children():
            self.report_table.delete(item)

        self.total_records.configure(
            text="Total Records : 0"
        )
        self.total_amount.configure(
            text="Total Amount : ₹0.00"
        )
    # ==========================================
    # Search Report
    # ==========================================

    def search_report(self):
        keyword = self.search_entry.get().strip().lower()

        for item in self.report_table.get_children():
            values = self.report_table.item(
                item,
                "values"
            )

            found = False

            for value in values:
                if keyword in str(value).lower():
                    found = True
                    break

            if found:
                self.report_table.reattach(
                    item,
                    "",
                    "end"
                )
            else:
                self.report_table.detach(item)

        self.total_records.configure(
            text=f"Total Records : {len(self.report_table.get_children())}"
        )


    # ==========================================
    # Export Report
    # ==========================================

    def export_report(self):

        if len(self.report_table.get_children()) == 0:
            messagebox.showwarning(
                "No Data",
                "Generate report first."
            )
            return

        export_format = self.export_format.get()

        # =========================
        # Excel Export
        # =========================
        if export_format == "Excel":

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel File", "*.xlsx")],
                title="Save Excel Report"
            )

            if not file_path:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = self.report_type.get()

            columns = self.report_table["columns"]

            for col_no, heading in enumerate(columns, start=1):
                cell = ws.cell(row=1, column=col_no)
                cell.value = heading
                cell.font = Font(bold=True)

            row_no = 2

            for item in self.report_table.get_children():
                values = self.report_table.item(item, "values")

                for col_no, value in enumerate(values, start=1):
                    ws.cell(row=row_no, column=col_no).value = value

                row_no += 1

            for column_cells in ws.columns:
                length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 5

            wb.save(file_path)

            messagebox.showinfo(
                "Success",
                "Excel exported successfully."
            )

        # =========================
        # CSV Export
        # =========================

        elif export_format == "CSV":

            file_path = filedialog.asksaveasfilename(

                defaultextension=".csv",

                filetypes=[
                    ("CSV File", "*.csv")
                ],

                title="Save CSV Report"

            )


            if not file_path:

                return


            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)


                # Header

                columns = self.report_table["columns"]

                writer.writerow(columns)


                # Data

                for item in self.report_table.get_children():

                    values = self.report_table.item(
                        item,
                        "values"
                    )

                    writer.writerow(values)



            messagebox.showinfo(
                "Success",
                "CSV exported successfully."
            )

        # =========================
        # PDF Export
        # =========================
        elif export_format == "PDF":

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF File", "*.pdf")],
                title="Save PDF Report"
            )

            if not file_path:
                return

            doc = SimpleDocTemplate(file_path)

            styles = getSampleStyleSheet()

            elements = []

            elements.append(
                Paragraph(
                    "<b>Cloud Secure Hospital ERP</b>",
                    styles["Title"]
                )
            )

            elements.append(
                Paragraph(
                    self.report_type.get(),
                    styles["Heading2"]
                )
            )

            columns = list(self.report_table["columns"])

            data = [columns]

            for item in self.report_table.get_children():
                data.append(
                    list(self.report_table.item(item)["values"])
                )

            table = Table(data)

            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("GRID", (0,0), (-1,-1), 1, colors.black),
                ("BACKGROUND", (0,1), (-1,-1), colors.beige),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0,0), (-1,0), 8),
            ]))

            elements.append(table)

            doc.build(elements)

            messagebox.showinfo(
                "Success",
                "PDF exported successfully."
            )

    # =========================
    # Screen Preview
    # =========================
        else:

         messagebox.showinfo(
            "Screen Preview",
            "Report is already displayed on the screen."
        )


    # ==========================================
    # Print Report
    # ==========================================

    def print_report(self):
        if len(self.report_table.get_children()) == 0:
            messagebox.showwarning(
                "No Data",
                "Generate report first."
            )
            return

        temp_pdf = NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        pdf_file = temp_pdf.name
        temp_pdf.close()

        doc = SimpleDocTemplate(pdf_file)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>Cloud Secure Hospital ERP</b>",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                self.report_type.get(),
                styles["Heading2"]
            )
        )

        columns = list(self.report_table["columns"])

        data = [columns]

        for item in self.report_table.get_children():
            data.append(
                list(self.report_table.item(item)["values"])
            )

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BACKGROUND",(0,1),(-1,-1),colors.beige),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")
        ]))

        elements.append(table)

        doc.build(elements)

        webbrowser.open_new(pdf_file)

        messagebox.showinfo(
            "Print",
            "PDF opened.\nPress Ctrl + P to print."
        )

    # ==========================================
    # Update Report Summary
    # ==========================================
    def update_summary(self):
        total_records = len(self.report_table.get_children())
        total_amount = 0.0
        report = self.report_type.get()

        for item in self.report_table.get_children():
            values = self.report_table.item(item, "values")

            try:
                if report == "Doctor Report":
                    total_amount += float(values[5])      # Consultation Fee

                elif report == "Pharmacy Report":
                    total_amount += float(values[5])      # Price

                elif report == "Billing Report":
                    total_amount += float(values[6])      # Net Amount

                elif report == "OPD Report":
                       pass     # Consultation Fee

                elif report == "Accounts Report":
                    total_amount += float(values[3])      # Amount

                elif report == "Laboratory Report":
                    total_amount += float(values[5])      # Test Fee

                elif report == "Inventory Report":
                    total_amount += float(values[5])      # Selling Price

            except (ValueError, TypeError, IndexError):
                pass

        self.total_records.configure(
            text=f"Total Records : {total_records}"
        )

        # Patient, Appointment, IPD reports me amount nahi hota
        if report in ("Patient Report", "Appointment Report", "IPD Report"):
            self.total_amount.configure(
                text="Total Amount : N/A"
            )
        else:
            self.total_amount.configure(
                text=f"Total Amount : ₹{total_amount:,.2f}"
            )

    # ==========================================
    # Refresh Report
    # ==========================================
    def refresh_report(self):
        self.generate_report()