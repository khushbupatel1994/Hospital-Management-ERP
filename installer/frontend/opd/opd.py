"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : OPD Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox

from frontend.opd.opd_ui import OPDUI
from frontend.opd.opd_service import OPDService
from frontend.opd.opd_crud import OPDCRUD


class OPD(OPDUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = OPDService()

        self.crud = OPDCRUD()

        self.bind_events()

        self.load_opd()
        self.load_patients()
        self.load_doctors()
        self.add_btn.configure(command=self.add_opd)
        self.update_btn.configure(command=self.update_opd)
        self.delete_btn.configure(command=self.delete_opd)
        self.clear_btn.configure(command=self.clear_form)

        self.opd_id.configure(state="normal")

        self.opd_id.insert(
            0,
            self.crud.generate_opd_id()
        )

        self.opd_id.configure(state="readonly")

    def load_patients(self):

        patients = self.service.get_all_patient_names()

        self.patient.configure(values=patients)
    def load_doctors(self):

        doctors = self.service.get_all_doctor_names()

        self.doctor.configure(values=doctors)
    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_opd
        )

        self.update_btn.configure(
            command=self.update_opd
        )

        self.delete_btn.configure(
            command=self.delete_opd
        )

        self.search_btn.configure(
            command=self.search_opd
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_opd()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.opd_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_opd
        )

    # ==========================================
    # Add OPD
    # ==========================================

    def add_opd(self):

        patient = self.patient.get()
        doctor = self.doctor.get()
        department = self.department.get()
        visit_date = self.visit_date.get().strip()
        visit_time = self.visit_time.get().strip()
        chief_complaint = self.chief_complaint.get("1.0", "end").strip()
        diagnosis = self.diagnosis.get("1.0", "end").strip()
        prescription = self.prescription.get("1.0", "end").strip()
        followup_date = self.followup_date.get().strip()
        notes = self.notes.get("1.0", "end").strip()
        status = self.status.get()

        if not self.service.validate_opd(

            patient,
            doctor,
            department,
            visit_date,
            visit_time

        ):
            return

        opd_id = self.crud.generate_opd_id()

        self.opd_id.configure(state="normal")
        self.opd_id.delete(0, "end")
        self.opd_id.insert(0, opd_id)
        self.opd_id.configure(state="readonly")
        success = self.crud.add_opd(

            opd_id,

            patient,

            doctor,

            department,

            visit_date,

            visit_time,

            chief_complaint,

            diagnosis,

            prescription,

            followup_date,

            notes,

            status

        )

        if success:

            messagebox.showinfo(
                "Success",
                "OPD record added successfully."
            )

            self.clear_form()

            self.load_opd()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add OPD record."
            )
       

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.opd_id.configure(state="normal")

        self.opd_id.delete(0, "end")

        self.opd_id.insert(
            0,
            self.crud.generate_opd_id()
        )

        self.opd_id.configure(state="readonly")
        self.patient.set("")

        self.doctor.set("")

        self.department.set("General Medicine")

        self.visit_date.delete(0, "end")

        self.visit_time.delete(0, "end")

        self.chief_complaint.delete("1.0", "end")

        self.diagnosis.delete("1.0", "end")

        self.prescription.delete("1.0", "end")

        self.followup_date.delete(0, "end")

        self.notes.delete("1.0", "end")

        self.status.set("Open")
        self.selected_opd_id = None

      
    # ==========================================
    # Load OPD
    # ==========================================

    def load_opd(self):

        for item in self.opd_table.get_children():

            self.opd_table.delete(item)

        rows = self.crud.load_opd()

        for row in rows:

            self.opd_table.insert(

                "",

                "end",

                values=row

            )

    # ==========================================
    # Load Selected OPD
    # ==========================================

    def load_selected_opd(self, event=None):

        selected = self.opd_table.focus()

        if not selected:
            return

        values = self.opd_table.item(
                selected,
                "values"
        )

        opd = self.crud.get_opd_by_id(
                values[0]
        )

        if not opd:
            return

        self.selected_opd_id = opd[0]

        self.opd_id.configure(state="normal")

        self.opd_id.delete(0, "end")

        self.opd_id.insert(
                0,
                opd[1]
            )

        self.opd_id.configure(state="readonly")

        self.patient.set(opd[2])

        self.doctor.set(opd[3])

        self.department.set(opd[4])

        self.visit_date.delete(0, "end")
        self.followup_date.delete(0, "end")
        self.visit_date.insert(0, opd[5])

        self.visit_time.delete(0, "end")
        self.visit_time.insert(0, opd[6])

        self.chief_complaint.delete("1.0", "end")
        self.chief_complaint.insert("1.0", opd[7])

        self.diagnosis.delete("1.0", "end")
        self.diagnosis.insert("1.0", opd[8])

        self.prescription.delete("1.0", "end")
        self.prescription.insert("1.0", opd[9])

        self.followup_date.delete(0, "end")
        self.followup_date.insert(0, opd[10])

        self.notes.delete("1.0", "end")
        self.notes.insert("1.0", opd[11])

        self.status.set(opd[12])

    # ==========================================
    # Update OPD
    # ==========================================

    def update_opd(self):

        if not hasattr(self, "selected_opd_id"):
            messagebox.showwarning(
                "Warning",
                "Please select an OPD record."
            )
            return

        patient = self.patient.get()
        doctor = self.doctor.get()
        department = self.department.get()
        visit_date = self.visit_date.get().strip()
        visit_time = self.visit_time.get().strip()
        chief_complaint = self.chief_complaint.get("1.0", "end").strip()
        diagnosis = self.diagnosis.get("1.0", "end").strip()
        prescription = self.prescription.get("1.0", "end").strip()
        followup_date = self.followup_date.get().strip()
        notes = self.notes.get("1.0", "end").strip()
        status = self.status.get()

        if not self.service.validate_opd(
            patient,
            doctor,
            department,
            visit_date,
            visit_time
        ):
            return

        success = self.crud.update_opd(
            self.selected_opd_id,
            patient,
            doctor,
            department,
            visit_date,
            visit_time,
            chief_complaint,
            diagnosis,
            prescription,
            followup_date,
            notes,
            status
        )

        if success:
            messagebox.showinfo(
                "Success",
                "OPD updated successfully."
            )
            self.load_opd()
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Unable to update OPD."
            )


    # ==========================================
    # Delete OPD
    # ==========================================

    def delete_opd(self):

        selected = self.opd_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an OPD record."
            )

            return

        values = self.opd_table.item(
            selected,
            "values"
        )

        opd_db_id = values[0]

        opd = self.crud.get_opd_by_id(
            opd_db_id
        )

        if not opd:

            messagebox.showerror(
                "Error",
                "OPD record not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this OPD record?"
        ):

            if self.crud.delete_opd(
                opd_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "OPD deleted successfully."
                )

                self.load_opd()

                self.clear_form()

                self.selected_opd_id = None


    # ==========================================
    # Search OPD
    # ==========================================

    def search_opd(self):

        keyword = self.search_entry.get().strip()

        for item in self.opd_table.get_children():

            self.opd_table.delete(item)

        rows = self.crud.search_opd(keyword)

        for row in rows:

            self.opd_table.insert(
                "",
                "end",
                values=row
            )
