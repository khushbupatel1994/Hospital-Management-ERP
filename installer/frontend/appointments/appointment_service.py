"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Appointment Service
Version : 2.0
===========================================================
"""

from tkinter import messagebox


class AppointmentService:

    # ==========================================
    # Validate Appointment
    # ==========================================

    def validate_appointment(

        self,

        patient,

        doctor,

        department,

        appointment_date,

        appointment_time,

        token_no

    ):

        if patient == "":

            messagebox.showerror(
                "Validation",
                "Patient is required."
            )

            return False

        if doctor == "":

            messagebox.showerror(
                "Validation",
                "Doctor is required."
            )

            return False

        if department == "":

            messagebox.showerror(
                "Validation",
                "Department is required."
            )

            return False

        if appointment_date == "":

            messagebox.showerror(
                "Validation",
                "Appointment Date is required."
            )

            return False

        if appointment_time == "":

            messagebox.showerror(
                "Validation",
                "Appointment Time is required."
            )

            return False

        if token_no == "":

            messagebox.showerror(
                "Validation",
                "Token Number is required."
            )

            return False

        return True