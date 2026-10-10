"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Appointment Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import date
from frontend.appointments.appointment_ui import AppointmentUI
from frontend.appointments.appointment_service import AppointmentService
from frontend.appointments.appointment_crud import AppointmentCRUD


class Appointment(AppointmentUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = AppointmentService()
        self.crud = AppointmentCRUD()

        self.bind_events()

        self.load_doctors()
        self.load_patients()

        self.load_appointments()

        self.appointment_id.configure(state="normal")
        self.appointment_id.insert(
            0,
            self.crud.generate_appointment_id()
        )
        self.appointment_id.configure(state="disabled")

        self.token_no.insert(
            0,
            self.crud.generate_token_no()
        )

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_appointment
        )

        self.update_btn.configure(
            command=self.update_appointment
        )

        self.delete_btn.configure(
            command=self.delete_appointment
        )

        self.search_btn.configure(
            command=self.search_appointment
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_appointment()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.appointment_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_appointment
        )
        self.doctor.configure(command=self.on_doctor_change)

        # ==========================================
        # Doctor Change
        # ==========================================

    def on_doctor_change(self, doctor_name):

        department = self.crud.get_doctor_department(
            doctor_name
        )

        if department:
            self.department.set(department)

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
    # Add Appointment
    # ==========================================

    def add_appointment(self):

        patient = self.patient.get()
        doctor = self.doctor.get()
        department = self.department.get()
        appointment_date = self.appointment_date.get().strip()
        appointment_time = self.appointment_time.get().strip()
        visit_type = self.visit_type.get()
        token_no = self.token_no.get().strip()
        status = self.status.get()
        remarks = self.remarks.get("1.0", "end").strip()

        if not self.service.validate_appointment(

            patient,
            doctor,
            department,
            appointment_date,
            appointment_time,
            token_no

        ):
            return

        duplicate = self.crud.check_duplicate_token(
            token_no
        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Token Number already exists."
            )

            return

        success = self.crud.add_appointment(

            self.appointment_id.get(),

            patient,

            doctor,

            department,

            appointment_date,

            appointment_time,

            visit_type,

            token_no,

            status,

            remarks

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Appointment added successfully."
            )

            self.clear_form()

            self.load_appointments()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add appointment."
            )

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.appointment_id.configure(state="normal")

        self.appointment_id.delete(0, "end")

        self.appointment_id.insert(
            0,
            self.crud.generate_appointment_id()
        )

        self.appointment_id.configure(state="disabled")

        self.patient.set("")

        self.doctor.set("")

        self.department.set("")

        self.appointment_date.set_date(date.today())

        self.appointment_time.set("")

        self.visit_type.set("")

        self.token_no.delete(0, "end")

        self.token_no.insert(
            0,
            self.crud.generate_token_no()
        )

        self.status.set("")

        self.remarks.delete(
            "1.0",
            "end"
        )

        self.selected_appointment_id = None

        # ==========================================
        # Load Appointments
        # ==========================================

    def load_appointments(self):

        for item in self.appointment_table.get_children():

            self.appointment_table.delete(item)

        rows = self.crud.load_appointments()

        for row in rows:

            self.appointment_table.insert(

                "",

                "end",

                values=row

            )

        # ==========================================
        # Load Selected Appointment
        # ==========================================

    def load_selected_appointment(self, event=None):

        selected = self.appointment_table.focus()

        if not selected:
            return

        values = self.appointment_table.item(
            selected,
            "values"
        )

        appointment = self.crud.get_appointment_by_id(
            values[0]
        )

        if not appointment:
            return

        self.selected_appointment_id = appointment[0]

        # Appointment ID
        self.appointment_id.configure(state="normal")
        self.appointment_id.delete(0, "end")
        self.appointment_id.insert(
            0,
            str(appointment[1] or "")
        )
        self.appointment_id.configure(state="disabled")

        # Patient
        self.patient.set(
            str(appointment[4] or "")
        )

        # Doctor
        self.doctor.set(
            str(appointment[5] or "")
        )

        # Department
        self.department.set(
            str(appointment[6] or "")
        )

        # Appointment Date
        self.appointment_date.set_date(
            appointment[7]
        )

        # Appointment Time
        self.appointment_time.set(
            str(appointment[8] or "")
        )

        # Visit Type
        self.visit_type.set(
            str(appointment[9] or "")
        )

        # Token Number
        self.token_no.delete(0, "end")
        self.token_no.insert(
            0,
            str(appointment[10] or "")
        )

        # Status
        self.status.set(
            str(appointment[13] or "Scheduled")
        )

        # Remarks
        self.remarks.delete(
            "1.0",
            "end"
        )

        self.remarks.insert(
            "1.0",
            str(appointment[14] or "")
        )
        # ==========================================
        # Update Appointment
        # ==========================================

    def update_appointment(self):

        if not hasattr(self, "selected_appointment_id"):

            messagebox.showwarning(
                "Warning",
                "Please select an appointment."
            )
            return

        if not self.service.validate_appointment(
            self.patient.get(),
            self.doctor.get(),
            self.department.get(),
            self.appointment_date.get().strip(),
            self.appointment_time.get().strip(),
            self.token_no.get().strip()
        ):
            return

        duplicate = self.crud.check_duplicate_token(

            self.token_no.get().strip(),

            self.selected_appointment_id

        )

        if duplicate:

            messagebox.showerror(

                "Duplicate",

                "Token Number already exists."

            )

            return

        patient = self.patient.get()
        doctor = self.doctor.get()
        department = self.department.get()
        appointment_date = self.appointment_date.get().strip()
        appointment_time = self.appointment_time.get().strip()
        visit_type = self.visit_type.get()
        token_no = self.token_no.get().strip()
        status = self.status.get()
        remarks = self.remarks.get("1.0", "end").strip()

        success = self.crud.update_appointment(
            self.selected_appointment_id,
            patient,
            doctor,
            department,
            appointment_date,
            appointment_time,
            visit_type,
            token_no,
            status,
            remarks
        )

        if success:

            messagebox.showinfo(

                "Success",

                "Appointment updated successfully."

            )

            self.load_appointments()

            self.clear_form()

            self.selected_appointment_id = None

        else:

            messagebox.showerror(

                "Error",

                "Unable to update appointment."

            )

        # ==========================================
        # Delete Appointment
        # ==========================================

    def delete_appointment(self):

        selected = self.appointment_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an appointment."
            )

            return

        values = self.appointment_table.item(
            selected,
            "values"
        )

        appointment_db_id = values[0]

        appointment = self.crud.get_appointment_by_id(
            appointment_db_id
        )

        if not appointment:

            messagebox.showerror(
                "Error",
                "Appointment not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this appointment?"
        ):

            if self.crud.delete_appointment(
                appointment_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Appointment deleted successfully."
                )

                self.load_appointments()

                self.clear_form()

                self.selected_appointment_id = None

    # ==========================================
    # Search Appointment
    # ==========================================

    def search_appointment(self):

        keyword = self.search_entry.get().strip()

        for item in self.appointment_table.get_children():

            self.appointment_table.delete(item)

        rows = self.crud.search_appointment(keyword)

        for row in rows:

            self.appointment_table.insert(

                "",

                "end",

                values=row

            )
