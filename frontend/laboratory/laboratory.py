"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory Controller
Version : 3.0
===========================================================
"""

import os
import sys
import tempfile
import subprocess

from tkinter import messagebox, filedialog
from datetime import datetime

import customtkinter as ctk

from frontend.laboratory.laboratory_ui import LaboratoryUI
from frontend.laboratory.laboratory_service import LaboratoryService
from frontend.laboratory.laboratory_crud import LaboratoryCRUD

from frontend.settings.settings_crud import SettingsCRUD


class Laboratory(LaboratoryUI):

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self, root):

        super().__init__(root)

        # -------------------------------------------------
        # Existing Services
        # -------------------------------------------------

        self.service = LaboratoryService()

        self.crud = LaboratoryCRUD()

        # -------------------------------------------------
        # Settings
        # -------------------------------------------------

        self.settings_crud = SettingsCRUD()

        self.hospital_name = (
            "CLOUD SECURE HOSPITAL"
        )

        self.hospital_address = ""

        self.hospital_city = ""

        self.hospital_state = ""

        self.hospital_pincode = ""

        self.hospital_phone = ""

        self.hospital_email = ""

        self.hospital_logo = ""

        self.hospital_currency = "INR"

        self.invoice_footer = (
            "Thank You • Visit Again"
        )

        self.load_hospital_settings()

        # -------------------------------------------------
        # Events
        # -------------------------------------------------

        self.bind_events()

        # -------------------------------------------------
        # Report Buttons
        # -------------------------------------------------

        self.create_report_buttons()

        # -------------------------------------------------
        # Load Data
        # -------------------------------------------------

        self.load_patients()

        self.load_doctors()

        self.load_tests()

        # -------------------------------------------------
        # Generate Test ID
        # -------------------------------------------------

        self.test_id.configure(
            state="normal"
        )

        self.test_id.delete(
            0,
            "end"
        )

        self.test_id.insert(
            0,
            self.crud.generate_test_id()
        )

        self.test_id.configure(
            state="disabled"
        )

        self.selected_test_id = None

        print(
            "🧪 Laboratory Screen Loaded"
        )


    # =====================================================
    # LOAD HOSPITAL SETTINGS
    # =====================================================

    def load_hospital_settings(self):

        try:

            data = (
                self.settings_crud.load_settings()
            )

            if data:

                # -----------------------------------------
                # Based on existing Settings structure
                # -----------------------------------------

                self.hospital_name = str(
                    data[0] or
                    "CLOUD SECURE HOSPITAL"
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

                self.hospital_currency = str(
                    data[9] or "INR"
                ).strip()

                self.invoice_footer = str(
                    data[10] or
                    "Thank You • Visit Again"
                ).strip()

                self.hospital_logo = str(
                    data[11] or ""
                ).strip()

            print(
                "🏥 Laboratory Hospital:",
                self.hospital_name
            )

            print(
                "🖼 Laboratory Logo:",
                self.hospital_logo
            )

        except Exception as e:

            print(
                "⚠ Laboratory Settings Error:",
                e
            )


    # =====================================================
    # CREATE REPORT BUTTONS
    # =====================================================

    def create_report_buttons(self):

        try:

            # ------------------------------------------------
            # View Report
            # ------------------------------------------------

            self.report_btn = ctk.CTkButton(

                self.button_frame,

                text="🧾 View Report",

                width=120,

                command=self.view_report

            )

            self.report_btn.grid(

                row=2,

                column=0,

                padx=5,

                pady=5

            )

            # ------------------------------------------------
            # Print Report
            # ------------------------------------------------

            self.print_report_btn = ctk.CTkButton(

                self.button_frame,

                text="🖨 Print Report",

                width=120,

                command=self.print_report

            )

            self.print_report_btn.grid(

                row=2,

                column=1,

                padx=5,

                pady=5

            )

            # ------------------------------------------------
            # Save PDF
            # ------------------------------------------------

            self.pdf_report_btn = ctk.CTkButton(

                self.button_frame,

                text="📄 Save PDF",

                width=245,

                command=self.save_report_pdf

            )

            self.pdf_report_btn.grid(

                row=3,

                column=0,

                columnspan=2,

                padx=5,

                pady=5

            )

            print(
                "✅ Laboratory Report Buttons Added"
            )

        except Exception as e:

            print(
                "⚠ Report Buttons Error:",
                e
            )


    # =====================================================
    # BIND EVENTS
    # =====================================================

    def bind_events(self):

        self.add_btn.configure(

            command=self.add_test

        )

        self.update_btn.configure(

            command=self.update_test

        )

        self.delete_btn.configure(

            command=self.delete_test

        )

        self.search_btn.configure(

            command=self.search_test

        )

        self.clear_btn.configure(

            command=self.clear_form

        )

        self.laboratory_table.bind(

            "<<TreeviewSelect>>",

            self.load_selected_test

        )

        self.search_entry.bind(

            "<KeyRelease>",

            lambda e:
            self.search_test()

        )

        self.doctor.configure(

            command=self.on_doctor_change

        )

        self.patient.configure(

            command=self.on_patient_change

        )


    # =====================================================
    # ADD TEST
    # =====================================================

    def add_test(self):

        test_name = (
            self.test_name.get().strip()
        )

        department = (
            self.department.get()
        )

        sample_type = (
            self.sample_type.get()
        )

        test_fee = (
            self.test_fee.get().strip()
        )

        normal_range = (
            self.normal_range.get().strip()
        )

        patient = (
            self.patient.get()
        )

        doctor = (
            self.doctor.get()
        )

        test_date = (
            self.test_date.get().strip()
        )

        test_result = (
            self.test_result.get(
                "1.0",
                "end"
            ).strip()
        )

        status = (
            self.status.get()
        )

        remarks = (
            self.remarks.get(
                "1.0",
                "end"
            ).strip()
        )

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not self.service.validate_test(

            test_name,

            department,

            patient,

            doctor,

            test_fee

        ):

            return

        # -------------------------------------------------
        # Test ID
        # -------------------------------------------------

        self.test_id.configure(
            state="normal"
        )

        test_id = (
            self.test_id.get()
        )

        self.test_id.configure(
            state="disabled"
        )

        # -------------------------------------------------
        # Add to Database
        # -------------------------------------------------

        try:

            success = self.crud.add_test(

                test_id,

                test_name,

                department,

                sample_type,

                float(test_fee),

                normal_range,

                patient,

                doctor,

                test_date,

                test_result,

                status,

                remarks

            )

            if success:

                messagebox.showinfo(

                    "Success",

                    "Laboratory Test added successfully."

                )

                self.load_tests()

                self.clear_form()

            else:

                messagebox.showerror(

                    "Error",

                    "Unable to add laboratory test."

                )

        except Exception as e:

            print(
                "❌ Add Test Error:",
                e
            )

            messagebox.showerror(

                "Error",

                str(e)

            )


    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        try:

            self.test_id.configure(
                state="normal"
            )

            self.test_id.delete(
                0,
                "end"
            )

            self.test_id.insert(

                0,

                self.crud.generate_test_id()

            )

            self.test_id.configure(
                state="disabled"
            )

            self.test_name.delete(
                0,
                "end"
            )

            self.department.set(
                "Pathology"
            )

            self.sample_type.set(
                "Blood"
            )

            self.test_fee.delete(
                0,
                "end"
            )

            self.normal_range.delete(
                0,
                "end"
            )

            self.patient.set(
                ""
            )

            self.mobile.delete(
                0,
                "end"
            )

            self.age.delete(
                0,
                "end"
            )

            self.gender.set(
                ""
            )

            self.doctor.set(
                ""
            )

            self.test_date.set_date(
                datetime.today()
            )

            self.test_result.delete(
                "1.0",
                "end"
            )

            self.status.set(
                "Pending"
            )

            self.remarks.delete(
                "1.0",
                "end"
            )

            self.selected_test_id = None

            self.test_name.focus()

        except Exception as e:

            print(
                "❌ Clear Form Error:",
                e
            )


    # =====================================================
    # LOAD TESTS
    # =====================================================

    def load_tests(self):

        try:

            for item in (
                self.laboratory_table.get_children()
            ):

                self.laboratory_table.delete(
                    item
                )

            rows = (
                self.crud.load_tests()
            )

            for row in rows:

                self.laboratory_table.insert(

                    "",

                    "end",

                    values=row

                )

        except Exception as e:

            print(
                "❌ Load Tests Error:",
                e
            )


    # =====================================================
    # LOAD SELECTED TEST
    # =====================================================

    def load_selected_test(
        self,
        event=None
    ):

        try:

            selected = (
                self.laboratory_table.focus()
            )

            if not selected:

                return

            values = (
                self.laboratory_table.item(

                    selected,

                    "values"

                )
            )

            if not values:

                return

            test = (
                self.crud.get_test_by_id(
                    int(values[0])
                )
            )

            if not test:

                return

            self.selected_test_id = (
                test[0]
            )

            # Test ID

            self.test_id.configure(
                state="normal"
            )

            self.test_id.delete(
                0,
                "end"
            )

            self.test_id.insert(
                0,
                test[1]
            )

            self.test_id.configure(
                state="disabled"
            )

            # Test Name

            self.test_name.delete(
                0,
                "end"
            )

            self.test_name.insert(
                0,
                test[2]
            )

            # Department

            self.department.set(
                test[3]
            )

            # Sample

            self.sample_type.set(
                test[4]
            )

            # Fee

            self.test_fee.delete(
                0,
                "end"
            )

            self.test_fee.insert(
                0,
                test[5]
            )

            # Normal Range

            self.normal_range.delete(
                0,
                "end"
            )

            self.normal_range.insert(
                0,
                test[6]
            )

            # Patient

            self.patient.set(
                test[7]
            )

            # Doctor

            self.doctor.set(
                test[8]
            )

            # Date

            self.test_date.set_date(
                test[9]
            )

            # Result

            self.test_result.delete(
                "1.0",
                "end"
            )

            self.test_result.insert(
                "1.0",
                test[10]
            )

            # Status

            self.status.set(
                test[11]
            )

            # Remarks

            self.remarks.delete(
                "1.0",
                "end"
            )

            self.remarks.insert(
                "1.0",
                test[12]
            )

        except Exception as e:

            print(
                "❌ Selected Test Error:",
                e
            )


    # =====================================================
    # UPDATE TEST
    # =====================================================

    def update_test(self):

        if self.selected_test_id is None:

            messagebox.showwarning(

                "Warning",

                "Please select a laboratory test."

            )

            return

        test_name = (
            self.test_name.get().strip()
        )

        department = (
            self.department.get()
        )

        sample_type = (
            self.sample_type.get()
        )

        test_fee = (
            self.test_fee.get().strip()
        )

        normal_range = (
            self.normal_range.get().strip()
        )

        patient = (
            self.patient.get()
        )

        doctor = (
            self.doctor.get()
        )

        test_date = (
            self.test_date.get().strip()
        )

        test_result = (
            self.test_result.get(
                "1.0",
                "end"
            ).strip()
        )

        status = (
            self.status.get()
        )

        remarks = (
            self.remarks.get(
                "1.0",
                "end"
            ).strip()
        )

        if not self.service.validate_test(

            test_name,

            department,

            patient,

            doctor,

            test_fee

        ):

            return

        try:

            success = self.crud.update_test(

                self.selected_test_id,

                test_name,

                department,

                sample_type,

                float(test_fee),

                normal_range,

                patient,

                doctor,

                test_date,

                test_result,

                status,

                remarks

            )

            if success:

                messagebox.showinfo(

                    "Success",

                    "Laboratory Test updated successfully."

                )

                self.load_tests()

                self.clear_form()

            else:

                messagebox.showerror(

                    "Error",

                    "Unable to update laboratory test."

                )

        except Exception as e:

            print(
                "❌ Update Test Error:",
                e
            )

            messagebox.showerror(

                "Error",

                str(e)

            )


    # =====================================================
    # DELETE TEST
    # =====================================================

    def delete_test(self):

        selected = (
            self.laboratory_table.focus()
        )

        if not selected:

            messagebox.showwarning(

                "Warning",

                "Please select a laboratory test."

            )

            return

        values = (
            self.laboratory_table.item(

                selected,

                "values"

            )
        )

        if not values:

            return

        try:

            test_db_id = int(
                values[0]
            )

        except ValueError:

            messagebox.showerror(

                "Error",

                "Invalid laboratory test ID."

            )

            return

        test = (
            self.crud.get_test_by_id(
                test_db_id
            )
        )

        if not test:

            messagebox.showerror(

                "Error",

                "Laboratory test not found."

            )

            return

        if messagebox.askyesno(

            "Confirm",

            "Delete this laboratory test?"

        ):

            try:

                success = (
                    self.crud.delete_test(
                        test_db_id
                    )
                )

                if success:

                    messagebox.showinfo(

                        "Success",

                        "Laboratory Test deleted successfully."

                    )

                    self.load_tests()

                    self.clear_form()

                    self.selected_test_id = None

            except Exception as e:

                print(
                    "❌ Delete Test Error:",
                    e
                )


    # =====================================================
    # SEARCH TEST
    # =====================================================

    def search_test(self):

        try:

            keyword = (
                self.search_entry.get().strip()
            )

            for item in (
                self.laboratory_table.get_children()
            ):

                self.laboratory_table.delete(
                    item
                )

            rows = (
                self.crud.search_test(
                    keyword
                )
            )

            for row in rows:

                self.laboratory_table.insert(

                    "",

                    "end",

                    values=row

                )

        except Exception as e:

            print(
                "❌ Search Test Error:",
                e
            )


    # =====================================================
    # DOCTOR CHANGE
    # =====================================================

    def on_doctor_change(
        self,
        doctor_name
    ):

        try:

            department = (
                self.crud.get_doctor_department(
                    doctor_name
                )
            )

            if department:

                self.department.set(
                    department
                )

        except Exception as e:

            print(
                "❌ Doctor Change Error:",
                e
            )


    # =====================================================
    # PATIENT CHANGE
    # =====================================================

    def on_patient_change(
        self,
        patient_name
    ):

        try:

            patient = (
                self.crud.get_patient_details(
                    patient_name
                )
            )

            if not patient:

                return

            mobile, age, gender = patient

            self.mobile.delete(
                0,
                "end"
            )

            self.mobile.insert(
                0,
                mobile
            )

            self.age.delete(
                0,
                "end"
            )

            self.age.insert(
                0,
                str(age)
            )

            self.gender.set(
                gender
            )

        except Exception as e:

            print(
                "❌ Patient Change Error:",
                e
            )


    # =====================================================
    # LOAD PATIENTS
    # =====================================================

    def load_patients(self):

        try:

            patients = (
                self.crud.get_patient_names()
            )

            self.patient.configure(
                values=patients
            )

            if patients:

                self.patient.set(
                    patients[0]
                )

        except Exception as e:

            print(
                "❌ Load Patients Error:",
                e
            )


    # =====================================================
    # LOAD DOCTORS
    # =====================================================

    def load_doctors(self):

        try:

            doctors = (
                self.crud.get_doctor_names()
            )

            self.doctor.configure(
                values=doctors
            )

            if doctors:

                self.doctor.set(
                    doctors[0]
                )

        except Exception as e:

            print(
                "❌ Load Doctors Error:",
                e
            )


    # =====================================================
    # GET SELECTED TEST
    # =====================================================

    def get_selected_test(self):

        selected = (
            self.laboratory_table.focus()
        )

        if not selected:

            messagebox.showwarning(

                "Warning",

                "Please select a laboratory test."

            )

            return None

        values = (
            self.laboratory_table.item(

                selected,

                "values"

            )
        )

        if not values:

            return None

        try:

            test_id = int(
                values[0]
            )

        except ValueError:

            messagebox.showerror(

                "Error",

                "Invalid laboratory test ID."

            )

            return None

        test = (
            self.crud.get_test_by_id(
                test_id
            )
        )

        if not test:

            messagebox.showerror(

                "Error",

                "Laboratory test not found."

            )

            return None

        return test


    # =====================================================
    # CREATE REPORT DATA
    # =====================================================

    def create_report_data(
        self,
        test
    ):

        return {

            "db_id":
                test[0],

            "test_id":
                test[1],

            "test_name":
                test[2],

            "department":
                test[3],

            "sample_type":
                test[4],

            "test_fee":
                test[5],

            "normal_range":
                test[6],

            "patient":
                test[7],

            "doctor":
                test[8],

            "test_date":
                test[9],

            "test_result":
                test[10],

            "status":
                test[11],

            "remarks":
                test[12]

        }


    # =====================================================
    # VIEW REPORT
    # =====================================================

    def view_report(self):

        test = (
            self.get_selected_test()
        )

        if not test:

            return

        self.load_hospital_settings()

        data = (
            self.create_report_data(
                test
            )
        )

        # -------------------------------------------------
        # Report Window
        # -------------------------------------------------

        report_window = ctk.CTkToplevel(
            self.root
        )

        report_window.title(

            f"{self.hospital_name} "
            f"- Laboratory Report"

        )

        report_window.geometry(
            "850x850"
        )

        report_window.minsize(
            700,
            700
        )

        # -------------------------------------------------
        # Main
        # -------------------------------------------------

        main = ctk.CTkScrollableFrame(
            report_window
        )

        main.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = ctk.CTkFrame(
            main,
            corner_radius=12
        )

        header.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Logo
        # -------------------------------------------------

        try:

            if (

                self.hospital_logo

                and os.path.isfile(
                    self.hospital_logo
                )

            ):

                from PIL import Image

                image = Image.open(
                    self.hospital_logo
                ).convert(
                    "RGBA"
                )

                image.thumbnail(
                    (100, 100)
                )

                self.report_logo = (
                    ctk.CTkImage(

                        light_image=image,

                        dark_image=image,

                        size=(90, 90)

                    )
                )

                ctk.CTkLabel(

                    header,

                    image=self.report_logo,

                    text=""

                ).pack(
                    pady=(15, 5)
                )

        except Exception as e:

            print(
                "⚠ Report Logo Error:",
                e
            )

        # -------------------------------------------------
        # Hospital Name
        # -------------------------------------------------

        ctk.CTkLabel(

            header,

            text=self.hospital_name,

            font=(
                "Segoe UI",
                28,
                "bold"
            )

        ).pack(
            pady=5
        )

        ctk.CTkLabel(

            header,

            text="LABORATORY INVESTIGATION REPORT",

            font=(
                "Segoe UI",
                17,
                "bold"
            )

        ).pack(
            pady=(0, 10)
        )

        # -------------------------------------------------
        # Contact
        # -------------------------------------------------

        contact = []

        if self.hospital_address:

            contact.append(
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

            contact.append(
                location
            )

        if self.hospital_phone:

            contact.append(

                f"Phone: "
                f"{self.hospital_phone}"

            )

        if self.hospital_email:

            contact.append(

                f"Email: "
                f"{self.hospital_email}"

            )

        if contact:

            ctk.CTkLabel(

                header,

                text="\n".join(contact),

                font=(
                    "Segoe UI",
                    11
                ),

                justify="center"

            ).pack(
                pady=(0, 12)
            )

        # -------------------------------------------------
        # Patient Information
        # -------------------------------------------------

        patient_frame = ctk.CTkFrame(
            main,
            corner_radius=10
        )

        patient_frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        ctk.CTkLabel(

            patient_frame,

            text="PATIENT INFORMATION",

            font=(
                "Segoe UI",
                17,
                "bold"
            )

        ).grid(

            row=0,

            column=0,

            columnspan=2,

            pady=12

        )

        patient_fields = [

            (
                "Patient Name",
                data["patient"]
            ),

            (
                "Doctor",
                data["doctor"]
            ),

            (
                "Test ID",
                data["test_id"]
            ),

            (
                "Test Date",
                data["test_date"]
            )

        ]

        for index, (
            label,
            value
        ) in enumerate(
            patient_fields,
            start=1
        ):

            row = (index - 1) // 2 + 1

            column = (index - 1) % 2

            ctk.CTkLabel(

                patient_frame,

                text=f"{label}:",

                font=(
                    "Segoe UI",
                    12,
                    "bold"
                )

            ).grid(

                row=row,

                column=column * 2,

                padx=(20, 5),

                pady=8,

                sticky="e"

            )

            ctk.CTkLabel(

                patient_frame,

                text=str(value or ""),

                font=(
                    "Segoe UI",
                    12
                )

            ).grid(

                row=row,

                column=column * 2 + 1,

                padx=(5, 20),

                pady=8,

                sticky="w"

            )

        patient_frame.grid_columnconfigure(
            1,
            weight=1
        )

        patient_frame.grid_columnconfigure(
            3,
            weight=1
        )

        # -------------------------------------------------
        # Test Information
        # -------------------------------------------------

        test_frame = ctk.CTkFrame(
            main,
            corner_radius=10
        )

        test_frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        ctk.CTkLabel(

            test_frame,

            text="TEST INFORMATION",

            font=(
                "Segoe UI",
                17,
                "bold"
            )

        ).grid(

            row=0,

            column=0,

            columnspan=2,

            pady=12

        )

        test_fields = [

            (
                "Test Name",
                data["test_name"]
            ),

            (
                "Department",
                data["department"]
            ),

            (
                "Sample Type",
                data["sample_type"]
            ),

            (
                "Normal Range",
                data["normal_range"]
            ),

            (
                "Test Fee",
                f"{self.hospital_currency} "
                f"{float(data['test_fee'] or 0):,.2f}"
            ),

            (
                "Status",
                data["status"]
            )

        ]

        for row_index, (
            label,
            value
        ) in enumerate(
            test_fields,
            start=1
        ):

            ctk.CTkLabel(

                test_frame,

                text=f"{label}:",

                font=(
                    "Segoe UI",
                    12,
                    "bold"
                )

            ).grid(

                row=row_index,

                column=0,

                padx=20,

                pady=7,

                sticky="e"

            )

            ctk.CTkLabel(

                test_frame,

                text=str(value or ""),

                font=(
                    "Segoe UI",
                    12
                ),

                wraplength=450,

                justify="left"

            ).grid(

                row=row_index,

                column=1,

                padx=20,

                pady=7,

                sticky="w"

            )

        test_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        result_frame = ctk.CTkFrame(

            main,

            corner_radius=10

        )

        result_frame.pack(

            fill="x",

            padx=5,

            pady=8

        )

        ctk.CTkLabel(

            result_frame,

            text="LABORATORY RESULT",

            font=(
                "Segoe UI",
                17,
                "bold"
            )

        ).pack(
            pady=(12, 8)
        )

        result_text = (
            data["test_result"]
            or "Result not entered."
        )

        result_box = ctk.CTkTextbox(

            result_frame,

            height=130

        )

        result_box.pack(

            fill="x",

            padx=15,

            pady=10

        )

        result_box.insert(

            "1.0",

            result_text

        )

        result_box.configure(

            state="disabled"

        )

        # -------------------------------------------------
        # Remarks
        # -------------------------------------------------

        if data["remarks"]:

            ctk.CTkLabel(

                main,

                text=(
                    f"Remarks: "
                    f"{data['remarks']}"
                ),

                font=(
                    "Segoe UI",
                    12
                ),

                wraplength=700,

                justify="left"

            ).pack(

                anchor="w",

                padx=15,

                pady=8

            )

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        ctk.CTkLabel(

            main,

            text=(
                self.invoice_footer
                or "Thank You • Visit Again"
            ),

            font=(
                "Segoe UI",
                13,
                "bold"
            )

        ).pack(
            pady=20
        )

        # -------------------------------------------------
        # Close
        # -------------------------------------------------

        ctk.CTkButton(

            main,

            text="Close",

            width=180,

            command=report_window.destroy

        ).pack(
            pady=(0, 15)
        )


    # =====================================================
    # CREATE REPORT TEXT
    # =====================================================

    def create_report_text(
        self,
        test
    ):

        self.load_hospital_settings()

        data = (
            self.create_report_data(
                test
            )
        )

        try:

            fee = float(
                data["test_fee"] or 0
            )

        except:

            fee = 0.0

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

                f"Phone: "
                f"{self.hospital_phone}"

            )

        if self.hospital_email:

            contact_lines.append(

                f"Email: "
                f"{self.hospital_email}"

            )

        contact_text = "\n".join(
            contact_lines
        )

        report = f"""

============================================================
                    {self.hospital_name}
             LABORATORY INVESTIGATION REPORT
============================================================

{contact_text}

------------------------------------------------------------
PATIENT INFORMATION
------------------------------------------------------------

Patient Name       : {data["patient"]}
Doctor             : {data["doctor"]}
Test ID            : {data["test_id"]}
Test Date          : {data["test_date"]}

------------------------------------------------------------
TEST INFORMATION
------------------------------------------------------------

Test Name          : {data["test_name"]}
Department         : {data["department"]}
Sample Type        : {data["sample_type"]}
Normal Range       : {data["normal_range"]}
Test Fee           : {self.hospital_currency} {fee:,.2f}
Status             : {data["status"]}

------------------------------------------------------------
LABORATORY RESULT
------------------------------------------------------------

{data["test_result"] or "Result not entered."}

------------------------------------------------------------
REMARKS
------------------------------------------------------------

{data["remarks"] or "No remarks."}

------------------------------------------------------------

                {self.invoice_footer}

============================================================
                 Authorized Laboratory
============================================================
"""

        return report


    # =====================================================
    # PRINT REPORT
    # =====================================================

    def print_report(self):

        test = (
            self.get_selected_test()
        )

        if not test:

            return

        report = (
            self.create_report_text(
                test
            )
        )

        try:

            # ---------------------------------------------
            # Create temporary text file
            # ---------------------------------------------

            temp_file = tempfile.NamedTemporaryFile(

                mode="w",

                suffix=".txt",

                delete=False,

                encoding="utf-8"

            )

            temp_file.write(
                report
            )

            temp_file.close()

            # ---------------------------------------------
            # Windows
            # ---------------------------------------------

            if sys.platform.startswith(
                "win"
            ):

                os.startfile(
                    temp_file.name,
                    "print"
                )

                messagebox.showinfo(

                    "Print",

                    "Laboratory report sent to printer."

                )

            else:

                subprocess.run(
                    [
                        "lp",
                        temp_file.name
                    ],
                    check=False
                )

        except Exception as e:

            print(
                "❌ Print Report Error:",
                e
            )

            messagebox.showerror(

                "Print Error",

                f"Unable to print report.\n\n{e}"

            )


    # =====================================================
    # SAVE REPORT PDF
    # =====================================================

    def save_report_pdf(self):

        test = (
            self.get_selected_test()
        )
        self.load_hospital_settings()

        data = self.create_report_data(test)

        if not data:
         messagebox.showerror(
        "Error",
        "Unable to create laboratory report data."
       )
         return

        if not test:

            return

        report = (
            self.create_report_text(
                test
            )
        )

        safe_name = (

            self.hospital_name

            .replace(
                " ",
                "_"
            )

            .replace(
                "/",
                "_"
            )

            .replace(
                "\\",
                "_"
            )

            .replace(
                ":",
                "_"
            )

        )

        test_id = str(
            test[1]
        )

        file_path = (
            filedialog.asksaveasfilename(

                title="Save Laboratory Report",

                defaultextension=".pdf",

                filetypes=[

                    (
                        "PDF Files",
                        "*.pdf"
                    )

                ],

                initialfile=(

                    f"{safe_name}_"
                    f"{test_id}_"
                    f"Laboratory_Report.pdf"

                )

            )
        )

        if not file_path:

            return

        try:

            from reportlab.lib.pagesizes import A4

            from reportlab.lib.styles import (
                getSampleStyleSheet,
                ParagraphStyle
            )

            from reportlab.lib.enums import (
                TA_CENTER
            )

            from reportlab.platypus import (

                SimpleDocTemplate,

                Paragraph,

                Spacer

            )

            # ---------------------------------------------
            # PDF Document
            # ---------------------------------------------

            document = SimpleDocTemplate(

                file_path,

                pagesize=A4,

                rightMargin=40,

                leftMargin=40,

                topMargin=40,

                bottomMargin=40

            )

            styles = (
                getSampleStyleSheet()
            )

            title_style = ParagraphStyle(

                "ReportTitle",

                parent=styles[
                    "Title"
                ],

                alignment=TA_CENTER,

                fontSize=18,

                leading=22

            )

            heading_style = ParagraphStyle(

                "Heading",

                parent=styles[
                    "Heading2"
                ],

                fontSize=12,

                leading=16

            )

            normal_style = ParagraphStyle(

                "NormalReport",

                parent=styles[
                    "Normal"
                ],

                fontSize=10,

                leading=14

            )

            story = []

            # ---------------------------------------------
            # Hospital Name
            # ---------------------------------------------

            story.append(

                Paragraph(

                    self.hospital_name,

                    title_style

                )

            )

            story.append(
                Spacer(1, 8)
            )

            story.append(

                Paragraph(

                    "LABORATORY "
                    "INVESTIGATION REPORT",

                    heading_style

                )

            )

            story.append(
                Spacer(1, 12)
            )

            # ---------------------------------------------
            # Contact
            # ---------------------------------------------

            contact = []

            if self.hospital_address:

                contact.append(
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

                contact.append(
                    location
                )

            if self.hospital_phone:

                contact.append(

                    f"Phone: "
                    f"{self.hospital_phone}"

                )

            if self.hospital_email:

                contact.append(

                    f"Email: "
                    f"{self.hospital_email}"

                )

            if contact:

                contact_html = (
                    "<br/>".join(
                        contact
                    )
                )

                story.append(

                    Paragraph(

                        contact_html,

                        normal_style

                    )

                )

                story.append(
                    Spacer(1, 12)
                )

            # ---------------------------------------------
            # Patient
            # ---------------------------------------------

            story.append(

                Paragraph(

                    "<b>PATIENT INFORMATION</b>",

                    heading_style

                )

            )

            story.append(

                Paragraph(

                    f"<b>Patient Name:</b> "
                    f"{data['patient']}<br/>"

                    f"<b>Doctor:</b> "
                    f"{data['doctor']}<br/>"

                    f"<b>Test ID:</b> "
                    f"{data['test_id']}<br/>"

                    f"<b>Test Date:</b> "
                    f"{data['test_date']}",

                    normal_style

                )

            )

            story.append(
                Spacer(1, 15)
            )

            # ---------------------------------------------
            # Test Information
            # ---------------------------------------------

            story.append(

                Paragraph(

                    "<b>TEST INFORMATION</b>",

                    heading_style

                )

            )

            story.append(

                Paragraph(

                    f"<b>Test Name:</b> "
                    f"{data['test_name']}<br/>"

                    f"<b>Department:</b> "
                    f"{data['department']}<br/>"

                    f"<b>Sample Type:</b> "
                    f"{data['sample_type']}<br/>"

                    f"<b>Normal Range:</b> "
                    f"{data['normal_range']}<br/>"

                    f"<b>Test Fee:</b> "
                    f"{self.hospital_currency} "
                    f"{float(data['test_fee'] or 0):,.2f}<br/>"

                    f"<b>Status:</b> "
                    f"{data['status']}",

                    normal_style

                )

            )

            story.append(
                Spacer(1, 15)
            )

            # ---------------------------------------------
            # Result
            # ---------------------------------------------

            story.append(

                Paragraph(

                    "<b>LABORATORY RESULT</b>",

                    heading_style

                )

            )

            result = (
                data["test_result"]
                or "Result not entered."
            )

            result = (
                result
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
                .replace(
                    "\n",
                    "<br/>"
                )
            )

            story.append(

                Paragraph(

                    result,

                    normal_style

                )

            )

            story.append(
                Spacer(1, 15)
            )

            # ---------------------------------------------
            # Remarks
            # ---------------------------------------------

            remarks = (
              data["remarks"]
                or "No remarks."
            )

            remarks = (
                remarks
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
                .replace(
                    "\n",
                    "<br/>"
                )
            )

            story.append(

                Paragraph(

                    f"<b>Remarks:</b><br/>"
                    f"{remarks}",

                    normal_style

                )

            )

            story.append(
                Spacer(1, 25)
            )

            # ---------------------------------------------
            # Footer
            # ---------------------------------------------

            footer = (
                self.invoice_footer
                or "Thank You • Visit Again"
            )

            story.append(

                Paragraph(

                    footer,

                    normal_style

                )

            )

            story.append(
                Spacer(1, 25)
            )

            story.append(

                Paragraph(

                    "Authorized Laboratory",

                    normal_style

                )

            )

            # ---------------------------------------------
            # Build PDF
            # ---------------------------------------------

            document.build(
                story
            )

            messagebox.showinfo(

                "Success",

                "Laboratory Report PDF "
                "saved successfully."

            )

            print(
                "✅ Laboratory PDF Saved:",
                file_path
            )

        except ImportError:

            messagebox.showerror(

                "PDF Error",

                "ReportLab is not installed.\n\n"
                "Run:\n"
                "pip install reportlab"

            )

        except Exception as e:

            print(
                "❌ PDF Report Error:",
                e
            )

            messagebox.showerror(

                "PDF Error",

                f"Unable to create PDF.\n\n{e}"

            )