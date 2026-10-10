"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Doctor Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox

from frontend.doctors.doctor_ui import DoctorUI
from frontend.doctors.doctor_service import DoctorService
from frontend.doctors.doctor_crud import DoctorCRUD


class Doctor(DoctorUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = DoctorService()

        self.crud = DoctorCRUD()

        self.bind_events()

        self.load_doctors()

        self.doctor_id.configure(state="normal")

        self.doctor_id.insert(
            0,
            self.crud.generate_doctor_id()
        )

        self.doctor_id.configure(state="disabled")

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_doctor
        )

        self.update_btn.configure(
            command=self.update_doctor
        )

        self.delete_btn.configure(
            command=self.delete_doctor
        )

        self.search_btn.configure(
            command=self.search_doctor
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_doctor()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.doctor_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_doctor
        )

    # ==========================================
    # Add Doctor
    # ==========================================

    def add_doctor(self):

        doctor_id = self.doctor_id.get()
        full_name = self.full_name.get().strip()
        gender = self.gender.get()
        department = self.department.get()
        specialization = self.specialization.get().strip()
        qualification = self.qualification.get().strip()
        experience = self.experience.get().strip()
        mobile = self.mobile.get().strip()
        email = self.email.get().strip()
        consultation_fee = self.consultation_fee.get().strip()
        opd_timing = self.opd_timing.get().strip()
        available_days = self.available_days.get().strip()
        status = self.status.get()

        # Validation
        if not self.service.validate_doctor(
            full_name,
            department,
            specialization,
            mobile,
            email,
            experience,
            consultation_fee
        ):
            return

        # Duplicate Mobile Check
        duplicate = self.crud.check_duplicate_mobile(mobile)
        if duplicate:
            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )
            return

        success = self.crud.add_doctor(
            doctor_id,
            full_name,
            gender,
            department,
            specialization,
            qualification,
            experience,
            mobile,
            email,
            consultation_fee,
            opd_timing,
            available_days,
            status
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Doctor added successfully."
            )
            self.clear_form()
            self.load_doctors()
        else:
            messagebox.showerror(
                "Error",
                "Unable to add doctor."
            )

# ==========================================
# Clear Form
# ==========================================

    def clear_form(self):

        self.doctor_id.configure(state="normal")

        self.doctor_id.delete(0, "end")

        self.doctor_id.insert(
            0,
            self.crud.generate_doctor_id()
        )

        self.doctor_id.configure(state="disabled")

        self.full_name.delete(0, "end")

        self.specialization.delete(0, "end")

        self.qualification.delete(0, "end")

        self.experience.delete(0, "end")

        self.mobile.delete(0, "end")

        self.email.delete(0, "end")

        self.consultation_fee.delete(0, "end")

        self.opd_timing.set("")

        self.available_days.set("")

        self.gender.set("Male")

        self.department.set("General Medicine")

        self.status.set("Active")

# ==========================================
# Load Doctors
# ==========================================

    def load_doctors(self):

        for item in self.doctor_table.get_children():
            self.doctor_table.delete(item)

        rows = self.crud.load_doctors()

        for row in rows:
            self.doctor_table.insert(
                "",
                "end",
                values=row
            )
# ==========================================
# Load Selected Doctor
# ==========================================

    def load_selected_doctor(self, event=None):

        selected = self.doctor_table.focus()

        if not selected:
            return

        values = self.doctor_table.item(
            selected,
            "values"
        )

        self.selected_doctor_id = values[0]

        doctor = self.crud.get_doctor_by_id(
            self.selected_doctor_id
        )

        if not doctor:
            return

        self.doctor_id.configure(state="normal")

        self.doctor_id.delete(0, "end")
        self.doctor_id.insert(0, doctor[1])

        self.doctor_id.configure(state="disabled")

        self.full_name.delete(0, "end")
        self.full_name.insert(0, doctor[2])

        self.gender.set(doctor[3])

        self.department.set(doctor[4])

        self.specialization.delete(0, "end")
        self.specialization.insert(0, doctor[5])

        self.qualification.delete(0, "end")
        self.qualification.insert(0, doctor[6])

        self.experience.delete(0, "end")
        self.experience.insert(0, doctor[7])

        self.mobile.delete(0, "end")
        self.mobile.insert(0, doctor[8])

        self.email.delete(0, "end")
        self.email.insert(0, doctor[9])

        self.consultation_fee.delete(0, "end")
        self.consultation_fee.insert(0, doctor[10])

        self.opd_timing.set(
           doctor[11] if doctor[11] else ""
        )

        self.available_days.set(
           doctor[12] if doctor[12] else ""
        )

        self.status.set(doctor[13])

# ==========================================
# Update Doctor
# ==========================================

    def update_doctor(self):

        if not hasattr(self, "selected_doctor_id"):


            messagebox.showwarning(
                "Warning",
                "Please select a doctor."
            )

            return

        # Duplicate Mobile Check

        duplicate = self.crud.check_duplicate_mobile(

            self.mobile.get().strip(),

            self.selected_doctor_id

        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )

            return

        success = self.crud.update_doctor(

        self.selected_doctor_id,

        self.full_name.get().strip(),

        self.gender.get(),

        self.department.get(),

        self.specialization.get().strip(),

        self.qualification.get().strip(),

        self.experience.get().strip(),

        self.mobile.get().strip(),

        self.email.get().strip(),

        self.consultation_fee.get().strip(),

        self.opd_timing.get().strip(),

        self.available_days.get().strip(),

        self.status.get()

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Doctor updated successfully."
            )

            self.load_doctors()

            self.clear_form()

            self.selected_doctor_id = None

        else:

            messagebox.showerror(
                "Error",
                "Unable to update doctor."
            )

# ==========================================
# Delete Doctor
# ==========================================

    def delete_doctor(self):

        selected = self.doctor_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a doctor."
            )

            return

        values = self.doctor_table.item(
            selected,
            "values"
        )

        doctor_db_id = values[0]

        if messagebox.askyesno(
            "Confirm",
            "Delete this doctor?"
        ):

            if self.crud.delete_doctor(doctor_db_id):

                messagebox.showinfo(
                    "Success",
                    "Doctor deleted successfully."
                )

                self.load_doctors()

                self.clear_form()

                self.selected_doctor_id = None

# ==========================================
# Search Doctor
# ==========================================

    def search_doctor(self):

        keyword = self.search_entry.get().strip()

        for item in self.doctor_table.get_children():

            self.doctor_table.delete(item)

        rows = self.crud.search_doctor(keyword)

        for row in rows:

            self.doctor_table.insert(
                "",
                "end",
                values=row
            )
