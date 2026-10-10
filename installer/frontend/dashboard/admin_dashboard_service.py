"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Admin Dashboard Service
Version : 3.0
===========================================================
"""

from database.database import Database


class AdminDashboardService(Database):

    def __init__(self):
        super().__init__()
        self.connect()

    # ==========================================
    # Total Doctors
    # ==========================================

    def get_total_doctors(self):

        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM doctors"
            )

            return self.cursor.fetchone()[0]

        except Exception as e:

            print("Doctor Count Error:", e)

            return 0

    # ==========================================
    # Total Patients
    # ==========================================

    def get_total_patients(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM patients"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total Appointments
    # ==========================================

    def get_total_appointments(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total OPD
    # ==========================================

    def get_total_opd(self):

        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM opd"
            )

            result = self.cursor.fetchone()[0]

            if result is None:
                return 0

            return result

        except Exception:
            return 0

    # ==========================================
    # Total IPD
    # ==========================================

    def get_total_ipd(self):

        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM ipd"
            )

            result = self.cursor.fetchone()[0]

            if result is None:
                return 0

            return result

        except Exception:
            return 0

    # ==========================================
    # Total Revenue
    # ==========================================

    def get_total_revenue(self):

        self.cursor.execute(
            "SELECT SUM(total_amount) FROM billing"
        )

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result