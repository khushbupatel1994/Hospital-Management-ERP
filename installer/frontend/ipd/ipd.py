"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : IPD Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from datetime import datetime
from frontend.ipd.ipd_ui import IPDUI
from frontend.ipd.ipd_service import IPDService
from frontend.ipd.ipd_crud import IPDCRUD


class IPD:

    def __init__(self, root):

        self.root = root

        # UI
        self.ui = IPDUI(root)

        # Database Objects
        self.crud = IPDCRUD()
        self.service = IPDService()

        # Widgets Shortcut (यदि आपने ऐसे बनाए हैं)
        self.patient = self.ui.patient
        self.doctor = self.ui.doctor
        self.admission_id = self.ui.admission_id
        self.ward = self.ui.ward
        self.bed_no = self.ui.bed_no

        self.admission_date = self.ui.admission_date
        self.discharge_date = self.ui.discharge_date

        self.diagnosis = self.ui.diagnosis
        self.treatment = self.ui.treatment

        self.daily_charges = self.ui.daily_charges
        self.status = self.ui.status
        self.remarks = self.ui.remarks

        self.add_btn = self.ui.add_btn
        self.update_btn = self.ui.update_btn
        self.delete_btn = self.ui.delete_btn
        self.clear_btn = self.ui.clear_btn
        self.search_btn = self.ui.search_btn

        self.search_entry = self.ui.search_entry

        self.ipd_table = self.ui.ipd_table

        self.load_patients()
        self.load_doctors()

        self.bind_events()
        self.load_admissions()
        self.clear_form()
    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_admission
        )

        self.update_btn.configure(
            command=self.update_admission
        )

        self.delete_btn.configure(
            command=self.delete_admission
        )

        self.search_btn.configure(
            command=self.search_admission
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_admission()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.ipd_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_admission
        )

    # ==========================================
    # Add Admission
    # ==========================================

    def add_admission(self):

        patient = self.patient.get()
        doctor = self.doctor.get()
        ward = self.ward.get()
        bed_no = self.bed_no.get().strip()

        admission_date = self.admission_date.get().strip()
        discharge_date = self.discharge_date.get().strip()

        diagnosis = self.diagnosis.get(
            "1.0",
            "end"
        ).strip()

        treatment = self.treatment.get(
            "1.0",
            "end"
        ).strip()

        daily_charges = self.daily_charges.get().strip()

        status = self.status.get()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_admission(
            patient,
            doctor,
            ward,
            bed_no,
            admission_date,
            daily_charges
        ):
            return

        self.admission_id.configure(state="normal")

        admission_id = self.admission_id.get()

        self.admission_id.configure(state="readonly")

        success = self.crud.add_admission(
            admission_id,
            patient,
            doctor,
            ward,
            bed_no,
            admission_date,
            discharge_date,
            diagnosis,
            treatment,
            float(daily_charges),
            status,
            remarks
        )

        if success:
            messagebox.showinfo(
                "Success",
                "IPD Admission added successfully."
            )
            self.load_admissions()
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Unable to add IPD admission."
            )


    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.admission_id.configure(state="normal")

        self.admission_id.delete(0, "end")

        self.admission_id.insert(
            0,
            self.crud.generate_admission_id()
        )

        self.admission_id.configure(state="readonly")

        self.patient.set("")

        self.doctor.set("")

        self.ward.set("General Ward")

        self.bed_no.set("Bed-001")

        self.admission_date.set_date(datetime.today())
        self.discharge_date.set_date(datetime.today())

        self.diagnosis.delete(
            "1.0",
            "end"
        )

        self.treatment.delete(
            "1.0",
            "end"
        )

        self.daily_charges.delete(0, "end")

        self.status.set("Admitted")

        self.remarks.delete(
            "1.0",
            "end"
        )

        self.selected_admission_id = None


    # ==========================================
    # Load Admissions
    # ==========================================

    def load_admissions(self):

        for item in self.ipd_table.get_children():
            self.ipd_table.delete(item)

        rows = self.crud.load_admissions()

        for row in rows:
            self.ipd_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Load Selected Admission
    # ==========================================

    def load_selected_admission(self, event=None):
        selected = self.ipd_table.focus()

        if not selected:
            return

        values = self.ipd_table.item(
            selected,
            "values"
        )

        admission = self.crud.get_admission_by_id(
            int(values[0])
        )

        if not admission:
            return

        self.selected_admission_id = admission[0]

        self.admission_id.configure(state="normal")

        self.admission_id.delete(0, "end")

        self.admission_id.insert(
            0,
            admission[1]
    )
        self.admission_id.configure(state="readonly")

        self.patient.set(admission[2])

        self.doctor.set(admission[3])

        self.ward.set(admission[4])

        self.bed_no.set(admission[5])

        self.admission_date.set_date(admission[6])
        self.discharge_date.set_date(admission[7])

        self.diagnosis.delete("1.0", "end")
        self.diagnosis.insert("1.0", admission[8])

        self.treatment.delete("1.0", "end")
        self.treatment.insert("1.0", admission[9])

        self.daily_charges.delete(0, "end")
        self.daily_charges.insert(0, admission[10])

        self.status.set(admission[11])

        self.remarks.delete("1.0", "end")
        self.remarks.insert("1.0", admission[12])

    # ==========================================
    # Update Admission
    # ==========================================

    def update_admission(self):
        if self.selected_admission_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select an IPD admission."
            )
            return

        patient = self.patient.get()
        doctor = self.doctor.get()
        ward = self.ward.get()
        bed_no = self.bed_no.get().strip()

        admission_date = self.admission_date.get().strip()
        discharge_date = self.discharge_date.get().strip()

        diagnosis = self.diagnosis.get(
            "1.0",
            "end"
        ).strip()

        treatment = self.treatment.get(
            "1.0",
            "end"
        ).strip()

        daily_charges = self.daily_charges.get().strip()

        status = self.status.get()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_admission(
            patient,
            doctor,
            ward,
            bed_no,
            admission_date,
            daily_charges
        ):
            return

        success = self.crud.update_admission(
            self.selected_admission_id,
            patient,
            doctor,
            ward,
            bed_no,
            admission_date,
            discharge_date,
            diagnosis,
            treatment,
            float(daily_charges),
            status,
            remarks
        )

        if success:
            messagebox.showinfo(
                "Success",
                "IPD Admission updated successfully."
            )
            self.load_admissions()
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Unable to update IPD admission."
            )

    # ==========================================
    # Delete Admission
    # ==========================================

    def delete_admission(self):
        selected = self.ipd_table.focus()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select an IPD admission."
            )
            return

        values = self.ipd_table.item(
            selected,
            "values"
        )

        admission_db_id = int(values[0])

        admission = self.crud.get_admission_by_id(
            admission_db_id
        )

        if not admission:
            messagebox.showerror(
                "Error",
                "IPD admission not found."
            )
            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this IPD admission?"
        ):
            if self.crud.delete_admission(
                admission_db_id
            ):
                messagebox.showinfo(
                    "Success",
                    "IPD Admission deleted successfully."
                )
                self.load_admissions()
                self.clear_form()
                self.selected_admission_id = None

    # ==========================================
    # Search Admission
    # ==========================================

    def search_admission(self):
        keyword = self.search_entry.get().strip()

        for item in self.ipd_table.get_children():
            self.ipd_table.delete(item)

        rows = self.crud.search_admission(keyword)

        for row in rows:
            self.ipd_table.insert(
                "",
                "end",
                values=row
            )

    def load_patients(self):
        try:
            patients = self.crud.get_patient_names()

            if patients:
                self.patient.configure(values=patients)
                self.patient.set(patients[0])
            else:
                self.patient.configure(values=["No Patient"])
                self.patient.set("No Patient")

        except Exception as e:
            print("Load Patient Error:", e)

    def load_doctors(self):
        try:
            doctors = self.crud.get_doctor_names()

            if doctors:
                self.doctor.configure(values=doctors)
                self.doctor.set(doctors[0])
            else:
                self.doctor.configure(values=["No Doctor"])
                self.doctor.set("No Doctor")

        except Exception as e:
            print("Load Doctor Error:", e)
