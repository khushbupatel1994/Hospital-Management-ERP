"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Analytics Controller
Version : 3.0
===========================================================
"""

from frontend.analytics.analytics_ui import AnalyticsUI
from frontend.analytics.dashboard_charts import DashboardCharts
from frontend.analytics.analytics_service import AnalyticsService

class Analytics(AnalyticsUI):

    def __init__(self, root):

        super().__init__(root)

        self.charts = DashboardCharts()

        self.service = AnalyticsService()

        self.load_dashboard()

    # ==========================================
    # Load Dashboard
    # ==========================================

    def load_dashboard(self):

        # Revenue Chart

        self.charts.revenue_chart(
            self.revenue_chart
        )

        # Patient Statistics

        self.charts.patient_chart(
            self.patient_chart
        )

        # Statistics Cards

        patient_count = self.service.get_total_patients()
        revenue = self.service.get_total_revenue()
        opd_count = self.service.get_total_opd()
        ipd_count = self.service.get_total_ipd()
        income = self.service.get_total_income()
        expense = self.service.get_total_expense()
        profit = income - expense

        self.patient_card.configure(
            text=f"Patients\n{patient_count}"
        )

        self.revenue_card.configure(
            text=f"Revenue\n₹{revenue:,.2f}"
        )

        self.opd_card.configure(
            text=f"OPD\n{opd_count}"
        )

        self.ipd_card.configure(
            text=f"IPD\n{ipd_count}"
        )

        # Low Stock Panel

        self.low_stock.delete("1.0", "end")
        low_stock_items = self.service.get_low_stock_items()

        if low_stock_items:
            for item_name, stock in low_stock_items:
                self.low_stock.insert(
                    "end",
                    f"• {item_name} - {stock} Left\n"
                )
        else:
            self.low_stock.insert(
                "end",
                "No Low Stock Items"
            )

        # Income vs Expense

        self.income_expense.delete("1.0", "end")

        self.income_expense.insert(
            "end",
            f"Income : ₹{income:,.2f}\n\n"
            f"Expense : ₹{expense:,.2f}\n\n"
            f"Profit : ₹{profit:,.2f}"
        )