"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Admin Dashboard Service
Version : 3.0
===========================================================
"""

from database.database import Database


class AdminDashboardService(Database):

    def __init__(self, api_client=None):
        self.api_client = api_client
        self.remote_dashboard = None

        if self.api_client:
            return

        super().__init__()
        self.connect()

    def _load_remote_dashboard(self):
        if not self.api_client:
            return None

        self.remote_dashboard = self.api_client.enterprise_dashboard()
        return self.remote_dashboard

    def _remote_value(self, key, default=0):
        try:
            data = self._load_remote_dashboard()
            if data is None:
                return default
            return data.get(key, default)
        except Exception as e:
            print("Remote Dashboard Error:", e)
            return default

    # ==========================================
    # Total Doctors
    # ==========================================

    def get_total_doctors(self):

        if self.api_client:
            return self._remote_value("doctors", 0)

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

        if self.api_client:
            return self._remote_value("patients", 0)

        self.cursor.execute(
            "SELECT COUNT(*) FROM patients"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total Appointments
    # ==========================================

    def get_total_appointments(self):

        if self.api_client:
            return self._remote_value("appointments", 0)

        self.cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total OPD
    # ==========================================

    def get_total_opd(self):

        if self.api_client:
            return self._remote_value("opd", 0)

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

        if self.api_client:
            return self._remote_value("active_ipd", 0)

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

        if self.api_client:
            return self._remote_value("revenue", 0)

        self.cursor.execute(
            "SELECT SUM(total_amount) FROM billing"
        )

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result