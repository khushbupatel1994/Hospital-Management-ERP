"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import datetime
from frontend.laboratory.laboratory_ui import LaboratoryUI
from frontend.laboratory.laboratory_service import LaboratoryService
from frontend.laboratory.laboratory_crud import LaboratoryCRUD


class Laboratory(LaboratoryUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = LaboratoryService()

        self.crud = LaboratoryCRUD()

        self.bind_events()
        self.load_patients()

        self.load_doctors()

        self.load_tests()

        self.test_id.configure(state="normal")

        self.test_id.insert(
            0,
            self.crud.generate_test_id()
        )

        self.test_id.configure(state="disabled")
        self.selected_test_id = None

    # ==========================================
    # Bind Events
    # ==========================================

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
            lambda e: self.search_test()
        )
        self.doctor.configure(
           command=self.on_doctor_change
        )
        self.patient.configure(
           command=self.on_patient_change
        )

    # ==========================================
    # Add Test
    # ==========================================

    def add_test(self):

     test_name = self.test_name.get().strip()
     department = self.department.get()
     sample_type = self.sample_type.get()
     test_fee = self.test_fee.get().strip()
     normal_range = self.normal_range.get().strip()

     patient = self.patient.get()
     doctor = self.doctor.get()

     test_date = self.test_date.get().strip()

     test_result = self.test_result.get(
        "1.0",
        "end"
     ).strip()

     status = self.status.get()

     remarks = self.remarks.get(
        "1.0",
        "end"
     ).strip()

     if not self.service.validate_test(

        test_name,

        department,

        patient,

        doctor,

        test_fee

     ):

        return

     self.test_id.configure(state="normal")

     test_id = self.test_id.get()

     self.test_id.configure(state="disabled")

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


    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

     self.test_id.configure(state="normal")

     self.test_id.delete(0, "end")

     self.test_id.insert(
        0,
        self.crud.generate_test_id()
     )

     self.test_id.configure(state="disabled")

     self.test_name.delete(0, "end")

     self.department.set("Pathology")

     self.sample_type.set("Blood")

     self.test_fee.delete(0, "end")

     self.normal_range.delete(0, "end")

     self.patient.set("")
     self.mobile.delete(0, "end")

     self.age.delete(0, "end")

     self.gender.set("")

     self.doctor.set("")

     self.test_date.set_date(datetime.today())

     self.test_result.delete(
        "1.0",
        "end"
     )

     self.status.set("Pending")

     self.remarks.delete(
        "1.0",
        "end"
     )

     self.selected_test_id = None
     self.test_name.focus()


    # ==========================================
    # Load Tests
    # ==========================================

    def load_tests(self):

     for item in self.laboratory_table.get_children():

        self.laboratory_table.delete(item)

     rows = self.crud.load_tests()

     for row in rows:

        self.laboratory_table.insert(

            "",

            "end",

            values=row

        )

    # ==========================================
    # Load Selected Test
    # ==========================================

    def load_selected_test(self, event=None):

        selected = self.laboratory_table.focus()

        if not selected:
            return

        values = self.laboratory_table.item(
            selected,
            "values"
        )

        test = self.crud.get_test_by_id(
            int(values[0])
        )

        if not test:
            return

        self.selected_test_id = test[0]

        self.test_id.configure(state="normal")

        self.test_id.delete(0, "end")

        self.test_id.insert(
            0,
            test[1]
        )

        self.test_id.configure(state="disabled")

        self.test_name.delete(0, "end")
        self.test_name.insert(0, test[2])

        self.department.set(test[3])

        self.sample_type.set(test[4])

        self.test_fee.delete(0, "end")
        self.test_fee.insert(0, test[5])

        self.normal_range.delete(0, "end")
        self.normal_range.insert(0, test[6])

        self.patient.set(test[7])

        self.doctor.set(test[8])

        self.test_date.set_date(test[9])

        self.test_result.delete("1.0", "end")
        self.test_result.insert("1.0", test[10])

        self.status.set(test[11])

        self.remarks.delete("1.0", "end")
        self.remarks.insert("1.0", test[12])

    # ==========================================
    # Update Test
    # ==========================================

    def update_test(self):

        if self.selected_test_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select a laboratory test."
            )
            return

        test_name = self.test_name.get().strip()
        department = self.department.get()
        sample_type = self.sample_type.get()
        test_fee = self.test_fee.get().strip()
        normal_range = self.normal_range.get().strip()

        patient = self.patient.get()
        doctor = self.doctor.get()

        test_date = self.test_date.get().strip()

        test_result = self.test_result.get(
            "1.0",
            "end"
        ).strip()

        status = self.status.get()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_test(
            test_name,
            department,
            patient,
            doctor,
            test_fee
        ):
            return

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


    # ==========================================
    # Delete Test
    # ==========================================

    def delete_test(self):

        selected = self.laboratory_table.focus()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a laboratory test."
            )
            return

        values = self.laboratory_table.item(
            selected,
            "values"
        )

        test_db_id = int(values[0])

        test = self.crud.get_test_by_id(
            test_db_id
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

            if self.crud.delete_test(
                test_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Laboratory Test deleted successfully."
                )

                self.load_tests()

                self.clear_form()

                self.selected_test_id = None


    # ==========================================
    # Search Test
    # ==========================================

    def search_test(self):

        keyword = self.search_entry.get().strip()

        for item in self.laboratory_table.get_children():

            self.laboratory_table.delete(item)

        rows = self.crud.search_test(keyword)

        for row in rows:

            self.laboratory_table.insert(
                "",
                "end",
                values=row
            )

    def on_doctor_change(self, doctor_name):

        department = self.crud.get_doctor_department(doctor_name)

        if department:
            self.department.set(department)

    # ==========================================
    # Patient Change
    # ==========================================

    def on_patient_change(self, patient_name):

        patient = self.crud.get_patient_details(patient_name)

        if not patient:
            return

        mobile, age, gender = patient

        self.mobile.delete(0, "end")
        self.mobile.insert(0, mobile)

        self.age.delete(0, "end")
        self.age.insert(0, str(age))

        self.gender.set(gender)

    # ==========================================
    # Load Patients
    # ==========================================

    def load_patients(self):

        patients = self.crud.get_patient_names()

        self.patient.configure(values=patients)

        if patients:
            self.patient.set(patients[0])

    # ==========================================
    # Load Doctors
    # ==========================================

    def load_doctors(self):

        doctors = self.crud.get_doctor_names()

        self.doctor.configure(values=doctors)

        if doctors:
            self.doctor.set(doctors[0])