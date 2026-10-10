"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Analytics Service
Version : 3.0
===========================================================
"""

from database.database import Database


class AnalyticsService(Database):

    def __init__(self):

        super().__init__()

        self.connect()

    # ==========================================
    # Total Patients
    # ==========================================

    def get_total_patients(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM patients"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    #  Total Doctors
    # ==========================================

    def get_total_doctors(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM doctors"
        )

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total OPD
    # ==========================================

    def get_total_opd(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM opd
        """)

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    # ==========================================
    # Total IPD
    # ==========================================

    def get_total_ipd(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM ipd
        """)

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    # ==========================================
    # Total Revenue
    # ==========================================

    def get_total_revenue(self):

        self.cursor.execute("""
            SELECT SUM(total_amount)
            FROM billing
        """)

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    # ==========================================
    # Total Income
    # ==========================================

    def get_total_income(self):

        self.cursor.execute("""
            SELECT SUM(amount)
            FROM accounts
            WHERE transaction_type='Income'
        """)

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    # ==========================================
    # Total Expense
    # ==========================================

    def get_total_expense(self):

        self.cursor.execute("""
            SELECT SUM(amount)
            FROM accounts
            WHERE transaction_type='Expense'
        """)

        result = self.cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    # ==========================================
    # Low Stock Items
    # ==========================================

    def get_low_stock_items(self):

        self.cursor.execute("""
            SELECT
                item_name,
                stock_quantity
            FROM inventory
            WHERE stock_quantity <= minimum_stock
            ORDER BY stock_quantity ASC
        """)

        return self.cursor.fetchall()
    