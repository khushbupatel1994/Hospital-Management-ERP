"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Admin Dashboard
===========================================================
"""
from frontend.hr.hr import HR
from frontend.opd.opd import OPD
from frontend.ipd.ipd import IPD
from frontend.dashboard.admin_dashboard_service import AdminDashboardService
from frontend.dashboard.admin_dashboard_ui import AdminDashboardUI
import customtkinter as ctk
from frontend.users.user import User
from frontend.patients.patient import Patient
from frontend.doctors.doctor import Doctor
from frontend.appointments.appointment import Appointment
from frontend.billing.billing import Billing
from frontend.pharmacy.pharmacy import Pharmacy
from frontend.laboratory.laboratory import Laboratory
from frontend.inventory.inventory import Inventory
from frontend.accounts.accounts import Accounts
from frontend.reports.reports import Reports
from frontend.analytics.analytics import Analytics
from frontend.settings.settings import Settings
from frontend.backup.backup import Backup
from backend.security.permissions import Permissions
from frontend.login.login_crud import LoginCRUD
from tkinter import messagebox
from frontend.ai.ai_center import AICenter

class AdminDashboard(AdminDashboardUI):

    def __init__(self, root, user=None, login_history_id=None):

        super().__init__(root, username=(user[2] if user else "Administrator"))

        self.user = user
        self.login_history_id = login_history_id

        if self.user:
            self.role = self.user[5]
        else:
            self.role = "Super Admin"
        self.dashboard_service = AdminDashboardService()
        print("✅ AdminDashboard Controller Loaded")

        self.sidebar.buttons["🏠 Dashboard"].configure(command=self.open_dashboard)
        self.sidebar.buttons["👥 Users"].configure(command=self.open_users)
        self.sidebar.buttons["🧑 Patients"].configure(command=self.open_patients)
        self.sidebar.buttons["👨‍⚕️ Doctors"].configure(command=self.open_doctors)
        self.sidebar.buttons["📅 Appointments"].configure(command=self.open_appointments)
        self.sidebar.buttons["💰 Billing"].configure(command=self.open_billing)
        self.sidebar.buttons["💊 Pharmacy"].configure(command=self.open_pharmacy)
        self.sidebar.buttons["🧪 Laboratory"].configure(command=self.open_laboratory)
        self.sidebar.buttons["📦 Inventory"].configure(command=self.open_inventory)
        self.sidebar.buttons["📊 Accounts"].configure(command=self.open_accounts)
        self.sidebar.buttons["📄 Reports"].configure(command=self.open_reports)
        self.sidebar.buttons["🩺 OPD"].configure(command=self.open_opd)
        self.sidebar.buttons["🛏 IPD"].configure(command=self.open_ipd)
        self.sidebar.buttons["👨‍💼 HR & Employee"].configure(command=self.open_hr)
        self.sidebar.buttons["📈 Analytics"].configure(command=self.open_analytics)
        self.sidebar.buttons["🤖 AI Intelligence"].configure(command=self.open_ai_assistant)
        self.sidebar.buttons["⚙ Settings"].configure(command=self.open_settings)
        self.sidebar.buttons["💾 Backup"].configure(command=self.open_backup)
        self.sidebar.buttons["🚪 Logout"].configure(command=self.logout)
        self.apply_permissions()
        self.open_dashboard()

    # ==========================================
    # Apply Role Permission
    # ==========================================

    def apply_permissions(self):
        modules = {
            "users": "👥 Users",
            "patients": "🧑 Patients",
            "doctors": "👨‍⚕️ Doctors",
            "appointments": "📅 Appointments",
            "billing": "💰 Billing",
            "pharmacy": "💊 Pharmacy",
            "laboratory": "🧪 Laboratory",
            "inventory": "📦 Inventory",
            "accounts": "📊 Accounts",
            "reports": "📄 Reports",
            "opd": "🩺 OPD",
            "ipd": "🛏 IPD",
            "hr": "👨‍💼 HR & Employee",
            "analytics": "📈 Analytics",
            "ai": "🤖 AI Intelligence",
            "settings": "⚙ Settings",
            "backup": "💾 Backup"
        }

        for module, button_name in modules.items():
            if button_name not in self.sidebar.buttons:
                continue

            button = self.sidebar.buttons[button_name]
            if Permissions.has_permission(self.role, module):
                button.configure(state="normal")
            else:
                button.configure(state="disabled")

    # ==========================================
    # Open User Management
    # ==========================================

    def open_users(self):

        print("Users Button Clicked")

        for widget in self.content.winfo_children():
            widget.destroy()

        User(self.content)

        print("User Screen Loaded")
    def open_patients(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Patient(self.content)

    def open_doctors(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Doctor(self.content)

    def open_appointments(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Appointment(self.content)

    # ==========================================
    # Open OPD
    # ==========================================

    def open_opd(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        OPD(self.content)

    # ==========================================
    # Open IPD
    # ==========================================

    def open_ipd(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        IPD(self.content)

    def open_billing(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Billing(self.content)

    def open_pharmacy(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        try:
            Pharmacy(self.content)
            print("✅ Pharmacy Loaded Successfully")

        except Exception:
            import traceback
            traceback.print_exc()

    def open_laboratory(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        try:
            Laboratory(self.content)
            print("✅ Laboratory Loaded Successfully")

        except Exception:
            import traceback
            traceback.print_exc()

    def open_inventory(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Inventory(self.content)

    def open_accounts(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Accounts(self.content)

    def open_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Reports(self.content)

    def open_analytics(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Analytics(self.content)

    def open_settings(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Settings(self.content)

    # ==========================================
    # Open HR
    # ==========================================

    def open_hr(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        HR(self.content)

    def open_backup(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        Backup(self.content)

    # ==========================================
    # Logout
    # ==========================================

    def logout(self):

        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if not confirm:
            return

        try:
            crud = LoginCRUD()
            crud.logout(
                history_id=self.login_history_id,
                username=self.user[3] if self.user else None
            )
        except Exception as e:
            print("Logout warning:", e)

        # Remove dashboard widgets and return to login screen.
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.update_idletasks()
        # Local import prevents circular import with LoginApp -> AdminDashboard.
        from frontend.login.login import LoginApp
        LoginApp(self.root)

    # ==========================================
    # Open AI Assistant
    # ==========================================

    def open_ai_assistant(self):
        print("AI Assistant Button Clicked")
        for widget in self.content.winfo_children():
            widget.destroy()
        AICenter(self.content).pack(fill="both", expand=True, padx=10, pady=10)

    # ==========================================
    # Open Dashboard
    # ==========================================

    def open_dashboard(self):
        print("Dashboard Button Clicked")

        self.load_dashboard()

        self.doctor_card.update_value(
            self.dashboard_service.get_total_doctors()
        )

        self.patient_card.update_value(
            self.dashboard_service.get_total_patients()
        )

        self.appointment_card.update_value(
            self.dashboard_service.get_total_appointments()
        )

        self.revenue_card.update_value(
            f"₹{self.dashboard_service.get_total_revenue()}"
        )
        self.opd_card.update_value(
            self.dashboard_service.get_total_opd()
        )
        self.ipd_card.update_value(
            self.dashboard_service.get_total_ipd()
        )

        print("Dashboard UI Loaded")