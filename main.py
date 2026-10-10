"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Main File
Version : 2.0
===========================================================
"""

import customtkinter as ctk
from frontend.doctors.doctor_crud import DoctorCRUD
from frontend.patients.patient_crud import PatientCRUD
from frontend.appointments.appointment_crud import AppointmentCRUD

from config.settings import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT,
    THEME,
    APPEARANCE_MODE
)

from frontend.login.login import LoginApp


class HospitalERP:

    def __init__(self):

        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)

        self.root = ctk.CTk()

        self.root.title(APP_NAME)

        # Screen Size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Full Screen Geometry
        self.root.geometry("1200x700")

        self.root.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        DoctorCRUD()
        PatientCRUD()
        AppointmentCRUD()

        LoginApp(self.root)

        self.root.mainloop()


if __name__ == "__main__":

    HospitalERP()