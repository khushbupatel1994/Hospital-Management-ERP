"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : OPD Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from database.database import Database

class OPDService(Database):

    def __init__(self):
        super().__init__()
        self.connect()

    # ==========================================
    # Validate OPD
    # ==========================================

    def validate_opd(

        self,

        patient,

        doctor,

        department,

        visit_date,

        visit_time

    ):

        if patient == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a patient."
            )

            return False

        if doctor == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a doctor."
            )

            return False

        if department == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a department."
            )

            return False

        if visit_date == "":

            messagebox.showerror(
                "Validation Error",
                "Visit Date is required."
            )

            return False

        if visit_time == "":

            messagebox.showerror(
                "Validation Error",
                "Visit Time is required."
            )

            return False

        return True
    def get_all_patient_names(self):
        self.cursor.execute("""
            SELECT patient_name
            FROM patients
            ORDER BY patient_name
        """)

        return [row[0] for row in self.cursor.fetchall()]

    def get_all_doctor_names(self):
        self.cursor.execute("""
            SELECT full_name
            FROM doctors
            ORDER BY full_name
        """)

        return [row[0] for row in self.cursor.fetchall()]