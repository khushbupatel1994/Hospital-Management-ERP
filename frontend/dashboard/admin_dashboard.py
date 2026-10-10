"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Admin Dashboard Controller
Version : 5.0
===========================================================
"""

# ==========================================================
# STANDARD IMPORTS
# ==========================================================

from tkinter import messagebox


# ==========================================================
# DASHBOARD UI & SERVICE
# ==========================================================

from frontend.dashboard.admin_dashboard_ui import (
    AdminDashboardUI
)

from frontend.dashboard.admin_dashboard_service import (
    AdminDashboardService
)


# ==========================================================
# MODULES
# ==========================================================

from frontend.users.user import User

from frontend.patients.patient import Patient

from frontend.doctors.doctor import Doctor

from frontend.appointments.appointment import Appointment

from frontend.opd.opd import OPD

from frontend.ipd.ipd import IPD

from frontend.billing.billing import Billing

from frontend.pharmacy.pharmacy import Pharmacy

from frontend.laboratory.laboratory import Laboratory

from frontend.inventory.inventory import Inventory

from frontend.accounts.accounts import Accounts

from frontend.reports.reports import Reports

from frontend.analytics.analytics import Analytics

from frontend.hr.hr import HR

from frontend.settings.settings import Settings

from frontend.backup.backup import Backup

from frontend.ai.ai_center import AICenter


# ==========================================================
# SECURITY / PERMISSIONS
# ==========================================================

from backend.security.permissions import Permissions


# ==========================================================
# LOGIN
# ==========================================================

from frontend.login.login_crud import LoginCRUD


# ==========================================================
# SETTINGS DATABASE
# ==========================================================

from frontend.settings.settings_crud import SettingsCRUD


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

class AdminDashboard(AdminDashboardUI):

    # Only financial/admin roles can view revenue.
    REVENUE_ROLES = {
        "Super Admin",
        "Admin",
        "Accountant"
    }

    # ======================================================
    # INITIALIZE
    # ======================================================

    def __init__(
        self,
        root,
        user=None,
        login_history_id=None,
        api_client=None
    ):

        # --------------------------------------------------
        # STORE USER INFORMATION
        # --------------------------------------------------

        self.user = user

        self.login_history_id = (
            login_history_id
        )

        # ==================================================
        # USER ROLE
        # ==================================================

        if self.user:

            try:

                self.role = str(
                    self.user[5]
                ).strip()

            except (
                IndexError,
                TypeError,
                AttributeError
            ):

                self.role = "Super Admin"

        else:

            self.role = "Super Admin"

        # Normalize legacy role name.
        if self.role == "Reception":

            self.role = "Receptionist"

        # ==================================================
        # HOSPITAL SETTINGS
        # IMPORTANT:
        # These values MUST exist before super().__init__()
        # ==================================================

        self.hospital_name = (
            "Cloud Secure Hospital ERP"
        )

        self.logo_path = ""

        # --------------------------------------------------
        # Load Hospital Settings
        # --------------------------------------------------

        try:

            settings_crud = SettingsCRUD()

            settings = (
                settings_crud.load_settings()
            )

            if settings:

                # ------------------------------------------
                # SETTINGS TABLE ORDER
                #
                # 0  hospital_name
                # 1  address
                # 2  city
                # 3  state
                # 4  pincode
                # 5  phone
                # 6  email
                # 7  website
                # 8  gst_number
                # 9  currency
                # 10 invoice_footer
                # 11 logo_path
                # 12 theme
                # ------------------------------------------

                if (
                    len(settings) > 0
                    and settings[0]
                ):

                    self.hospital_name = str(
                        settings[0]
                    ).strip()

                if (
                    len(settings) > 11
                    and settings[11]
                ):

                    self.logo_path = str(
                        settings[11]
                    ).strip()

            print(
                f"🏥 Hospital Name: "
                f"{self.hospital_name}"
            )

            print(
                f"🖼 Hospital Logo: "
                f"{self.logo_path}"
            )

        except Exception as e:

            print(
                "⚠ Hospital Settings Error:",
                e
            )

            self.hospital_name = (
                "Cloud Secure Hospital ERP"
            )

            self.logo_path = ""

        # ==================================================
        # DASHBOARD SERVICE
        # IMPORTANT:
        # MUST EXIST BEFORE super().__init__()
        # ==================================================

        try:

            self.api_client = api_client

            self.dashboard_service = (
                AdminDashboardService(
                    api_client=api_client
                )
            )

        except Exception as e:

            print(
                "❌ Dashboard Service Error:",
                e
            )

            self.dashboard_service = None

        # ==================================================
        # INITIALIZE PARENT UI
        # ==================================================

        super().__init__(
            root,
            username=(
                self.user[2]
                if self.user
                else "Administrator"
            )
        )

        # ==================================================
        # CONTROLLER LOADED
        # ==================================================

        print(
            "✅ AdminDashboard Controller Loaded"
        )

        print(
            f"🔐 Current Role: "
            f"{self.role}"
        )

        # ==================================================
        # SIDEBAR EVENTS
        # ==================================================

        self.setup_sidebar_events()

        # ==================================================
        # APPLY PERMISSIONS
        # ==================================================

        self.apply_permissions()

        # ==================================================
        # OPEN DASHBOARD
        # ==================================================

        self.open_dashboard()

    # ======================================================
    # SIDEBAR EVENTS
    # ======================================================

    def setup_sidebar_events(self):

        buttons = self.sidebar.buttons

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        if "🏠 Dashboard" in buttons:

            buttons[
                "🏠 Dashboard"
            ].configure(
                command=self.open_dashboard
            )

        # --------------------------------------------------
        # Users
        # --------------------------------------------------

        if "👥 Users" in buttons:

            buttons[
                "👥 Users"
            ].configure(
                command=self.open_users
            )

        # --------------------------------------------------
        # Patients
        # --------------------------------------------------

        if "🧑 Patients" in buttons:

            buttons[
                "🧑 Patients"
            ].configure(
                command=self.open_patients
            )

        # --------------------------------------------------
        # Doctors
        # --------------------------------------------------

        if "👨‍⚕️ Doctors" in buttons:

            buttons[
                "👨‍⚕️ Doctors"
            ].configure(
                command=self.open_doctors
            )

        # --------------------------------------------------
        # Appointments
        # --------------------------------------------------

        if "📅 Appointments" in buttons:

            buttons[
                "📅 Appointments"
            ].configure(
                command=self.open_appointments
            )

        # --------------------------------------------------
        # OPD
        # --------------------------------------------------

        if "🩺 OPD" in buttons:

            buttons[
                "🩺 OPD"
            ].configure(
                command=self.open_opd
            )

        # --------------------------------------------------
        # IPD
        # --------------------------------------------------

        if "🛏 IPD" in buttons:

            buttons[
                "🛏 IPD"
            ].configure(
                command=self.open_ipd
            )

        # --------------------------------------------------
        # Billing
        # --------------------------------------------------

        if "💰 Billing" in buttons:

            buttons[
                "💰 Billing"
            ].configure(
                command=self.open_billing
            )

        # --------------------------------------------------
        # Pharmacy
        # --------------------------------------------------

        if "💊 Pharmacy" in buttons:

            buttons[
                "💊 Pharmacy"
            ].configure(
                command=self.open_pharmacy
            )

        # --------------------------------------------------
        # Laboratory
        # --------------------------------------------------

        if "🧪 Laboratory" in buttons:

            buttons[
                "🧪 Laboratory"
            ].configure(
                command=self.open_laboratory
            )

        # --------------------------------------------------
        # Inventory
        # --------------------------------------------------

        if "📦 Inventory" in buttons:

            buttons[
                "📦 Inventory"
            ].configure(
                command=self.open_inventory
            )

        # --------------------------------------------------
        # Accounts
        # --------------------------------------------------

        if "📊 Accounts" in buttons:

            buttons[
                "📊 Accounts"
            ].configure(
                command=self.open_accounts
            )

        # --------------------------------------------------
        # Reports
        # --------------------------------------------------

        if "📄 Reports" in buttons:

            buttons[
                "📄 Reports"
            ].configure(
                command=self.open_reports
            )

        # --------------------------------------------------
        # Analytics
        # --------------------------------------------------

        if "📈 Analytics" in buttons:

            buttons[
                "📈 Analytics"
            ].configure(
                command=self.open_analytics
            )

        # --------------------------------------------------
        # AI Intelligence
        # --------------------------------------------------

        if "🤖 AI Intelligence" in buttons:

            buttons[
                "🤖 AI Intelligence"
            ].configure(
                command=self.open_ai_assistant
            )

        # --------------------------------------------------
        # HR
        # --------------------------------------------------

        if "👨‍💼 HR & Employee" in buttons:

            buttons[
                "👨‍💼 HR & Employee"
            ].configure(
                command=self.open_hr
            )

        # --------------------------------------------------
        # Settings
        # --------------------------------------------------

        if "⚙ Settings" in buttons:

            buttons[
                "⚙ Settings"
            ].configure(
                command=self.open_settings
            )

        # --------------------------------------------------
        # Backup
        # --------------------------------------------------

        if "💾 Backup" in buttons:

            buttons[
                "💾 Backup"
            ].configure(
                command=self.open_backup
            )

        # --------------------------------------------------
        # Logout
        # --------------------------------------------------

        if "🚪 Logout" in buttons:

            buttons[
                "🚪 Logout"
            ].configure(
                command=self.logout
            )

    # ======================================================
    # PERMISSION CHECK
    # ======================================================

    def can_access(self, module):

        try:

            allowed = (
                Permissions.has_permission(
                    self.role,
                    module
                )
            )

        except Exception as e:

            print(
                "❌ Permission Check Error:",
                e
            )

            allowed = False

        print(
            f"🔐 Permission | "
            f"Role={self.role} | "
            f"Module={module} | "
            f"Allowed={allowed}"
        )

        if not allowed:

            messagebox.showwarning(
                "Access Denied",
                (
                    "You do not have permission "
                    f"to access {module.title()}."
                ),
                parent=self.root
            )

            return False

        return True

    # ======================================================
    # APPLY ROLE PERMISSIONS
    # ======================================================

    def apply_permissions(self):

        modules = {
            "users": "👥 Users",
            "patients": "🧑 Patients",
            "doctors": "👨‍⚕️ Doctors",
            "appointments": "📅 Appointments",
            "opd": "🩺 OPD",
            "ipd": "🛏 IPD",
            "billing": "💰 Billing",
            "pharmacy": "💊 Pharmacy",
            "laboratory": "🧪 Laboratory",
            "inventory": "📦 Inventory",
            "accounts": "📊 Accounts",
            "reports": "📄 Reports",
            "analytics": "📈 Analytics",
            "ai": "🤖 AI Intelligence",
            "hr": "👨‍💼 HR & Employee",
            "settings": "⚙ Settings",
            "backup": "💾 Backup",
        }

        print(
            f"🔐 Applying Permissions for Role: "
            f"{self.role}"
        )

        for module, button_name in modules.items():

            button = (
                self.sidebar.buttons.get(
                    button_name
                )
            )

            if button is None:

                print(
                    f"⚠ Button Not Found: "
                    f"{button_name}"
                )

                continue

            try:

                allowed = (
                    Permissions.has_permission(
                        self.role,
                        module
                    )
                )

            except Exception as e:

                print(
                    f"Permission Error "
                    f"{module}: {e}"
                )

                allowed = False

            if allowed:

                try:

                    button.pack(
                        fill="x",
                        padx=10,
                        pady=5
                    )

                except Exception:

                    try:
                        button.grid()

                    except Exception:
                        pass

                try:

                    button.configure(
                        state="normal"
                    )

                except Exception:
                    pass

                print(
                    f"   ✅ SHOW: {module}"
                )

            else:

                try:

                    button.pack_forget()

                except Exception:

                    try:
                        button.grid_remove()

                    except Exception:
                        pass

                print(
                    f"   ❌ HIDE: {module}"
                )

    # ======================================================
    # CLEAR CONTENT
    # ======================================================

    def clear_content(self):

        for widget in (
            self.content.winfo_children()
        ):

            widget.destroy()

    # ======================================================
    # OPEN USER MANAGEMENT
    # ======================================================

    def open_users(self):

        print(
            "Users Button Clicked"
        )

        if not self.can_access(
            "users"
        ):

            return

        self.clear_content()

        User(
            self.content
        )

        print(
            "User Screen Loaded"
        )

    # ======================================================
    # OPEN PATIENTS
    # ======================================================

    def open_patients(self):

        print(
            "Patients Button Clicked"
        )

        # --------------------------------------------------
        # Permission
        # --------------------------------------------------

        if not self.can_access(
            "patients"
        ):

            return

        # --------------------------------------------------
        # Clear old content
        # --------------------------------------------------

        self.clear_content()

        # --------------------------------------------------
        # IMPORTANT:
        # Pass logged-in user and role to Patient module.
        #
        # Doctor login:
        #   user -> logged-in user record
        #   role -> Doctor
        #
        # Patient module can now filter:
        #   patients.doctor = logged-in doctor
        # --------------------------------------------------

        try:

            Patient(
                self.content,
                user=self.user,
                role=self.role,
                api_client=self.api_client
            )

            print(
                "✅ Patient Screen Loaded"
            )

        except Exception as e:

            print(
                "❌ Patient Screen Error:",
                e
            )

            import traceback
            traceback.print_exc()

    # ======================================================
    # OPEN DOCTORS
    # ======================================================

    def open_doctors(self):

        if not self.can_access(
            "doctors"
        ):

            return

        self.clear_content()

        Doctor(
            self.content,
            api_client=self.api_client
        )

    # ======================================================
    # OPEN APPOINTMENTS
    # ======================================================

    def open_appointments(self):

        if not self.can_access(
            "appointments"
        ):

            return

        self.clear_content()

        Appointment(
            self.content,
            user=self.user,
            role=self.role,
            api_client=self.api_client
        )

    # ======================================================
    # OPEN OPD
    # ======================================================

    def open_opd(self):

        if not self.can_access(
            "opd"
        ):

            return

        self.clear_content()

        OPD(
            self.content
        )

    # ======================================================
    # OPEN IPD
    # ======================================================

    def open_ipd(self):

        if not self.can_access(
            "ipd"
        ):

            return

        self.clear_content()

        IPD(
            self.content
        )

    # ======================================================
    # OPEN BILLING
    # ======================================================

    def open_billing(self):

        if not self.can_access(
            "billing"
        ):

            return

        self.clear_content()

        Billing(
            self.content
        )

    # ======================================================
    # OPEN PHARMACY
    # ======================================================

    def open_pharmacy(self):

        if not self.can_access(
            "pharmacy"
        ):

            return

        self.clear_content()

        try:

            Pharmacy(
                self.content
            )

            print(
                "✅ Pharmacy Loaded Successfully"
            )

        except Exception:

            import traceback
            traceback.print_exc()

    # ======================================================
    # OPEN LABORATORY
    # ======================================================

    def open_laboratory(self):

        if not self.can_access(
            "laboratory"
        ):

            return

        self.clear_content()

        try:

            Laboratory(
                self.content
            )

            print(
                "✅ Laboratory Loaded Successfully"
            )

        except Exception:

            import traceback
            traceback.print_exc()

    # ======================================================
    # OPEN INVENTORY
    # ======================================================

    def open_inventory(self):

        if not self.can_access(
            "inventory"
        ):

            return

        self.clear_content()

        Inventory(
            self.content
        )

    # ======================================================
    # OPEN ACCOUNTS
    # ======================================================

    def open_accounts(self):

        if not self.can_access(
            "accounts"
        ):

            return

        self.clear_content()

        Accounts(
            self.content
        )

    # ======================================================
    # OPEN REPORTS
    # ======================================================

    def open_reports(self):

        if not self.can_access(
            "reports"
        ):

            return

        self.clear_content()

        Reports(
            self.content
        )

    # ======================================================
    # OPEN ANALYTICS
    # ======================================================

    def open_analytics(self):

        if not self.can_access(
            "analytics"
        ):

            return

        self.clear_content()

        Analytics(
            self.content
        )

    # ======================================================
    # OPEN SETTINGS
    # ======================================================

    def open_settings(self):

        if not self.can_access(
            "settings"
        ):

            return

        self.clear_content()

        Settings(
            self.content
        )

        print(
            "Settings Screen Loaded"
        )

    # ======================================================
    # OPEN HR
    # ======================================================

    def open_hr(self):

        if not self.can_access(
            "hr"
        ):

            return

        self.clear_content()

        HR(
            self.content
        )

        print(
            "HR Screen Loaded"
        )

    # ======================================================
    # OPEN BACKUP
    # ======================================================

    def open_backup(self):

        if not self.can_access(
            "backup"
        ):

            return

        self.clear_content()

        Backup(
            self.content
        )

        print(
            "Backup Screen Loaded"
        )

    # ======================================================
    # OPEN AI ASSISTANT
    # ======================================================

    def open_ai_assistant(self):

        print(
            "AI Assistant Button Clicked"
        )

        if not self.can_access(
            "ai"
        ):

            return

        self.clear_content()

        try:

            AICenter(
                self.content
            ).pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            print(
                "✅ AI Assistant Loaded"
            )

        except Exception:

            import traceback
            traceback.print_exc()

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if not confirm:

            return

        # --------------------------------------------------
        # Save Logout History
        # --------------------------------------------------

        try:

            crud = LoginCRUD()

            crud.logout(
                history_id=(
                    self.login_history_id
                ),
                username=(
                    self.user[3]
                    if self.user
                    else None
                )
            )

        except Exception as e:

            print(
                "Logout warning:",
                e
            )

        # --------------------------------------------------
        # Remove Dashboard
        # --------------------------------------------------

        for widget in (
            self.root.winfo_children()
        ):

            widget.destroy()

        self.root.update_idletasks()

        # --------------------------------------------------
        # Return To Login
        # --------------------------------------------------

        from frontend.login.login import (
            LoginApp
        )

        LoginApp(
            self.root
        )

    # ======================================================
    # OPEN DASHBOARD
    # ======================================================

    def open_dashboard(self):

        print(
            "Dashboard Button Clicked"
        )

        # --------------------------------------------------
        # Permission
        # --------------------------------------------------

        # Dashboard is the main landing page.
        # Do not block it if the permission system
        # does not contain a dashboard module.

        try:

            if not Permissions.has_permission(
                self.role,
                "dashboard"
            ):

                print(
                    "⚠ Dashboard permission "
                    "not defined; allowing dashboard."
                )

        except Exception:

            pass

        # --------------------------------------------------
        # Load Dashboard UI
        # --------------------------------------------------

        try:

            self.load_dashboard()

        except Exception as e:

            print(
                "❌ Dashboard Load Error:",
                e
            )

            import traceback
            traceback.print_exc()

            return

        # --------------------------------------------------
        # Update Dashboard Cards
        # --------------------------------------------------

        if not self.dashboard_service:

            print(
                "⚠ Dashboard Service "
                "not available."
            )

            return

        # --------------------------------------------------
        # Doctors
        # --------------------------------------------------

        try:

            if hasattr(
                self,
                "doctor_card"
            ):

                self.doctor_card.update_value(
                    self.dashboard_service
                    .get_total_doctors()
                )

        except Exception as e:

            print(
                "Doctors Card Error:",
                e
            )

        # --------------------------------------------------
        # Patients
        # --------------------------------------------------

        try:

            if hasattr(
                self,
                "patient_card"
            ):

                self.patient_card.update_value(
                    self.dashboard_service
                    .get_total_patients()
                )

        except Exception as e:

            print(
                "Patients Card Error:",
                e
            )

        # --------------------------------------------------
        # Appointments
        # --------------------------------------------------

        try:

            if hasattr(
                self,
                "appointment_card"
            ):

                self.appointment_card.update_value(
                    self.dashboard_service
                    .get_total_appointments()
                )

        except Exception as e:

            print(
                "Appointments Card Error:",
                e
            )

        # --------------------------------------------------
        # Revenue
        # --------------------------------------------------

        # Do not query or update revenue for restricted roles.

        if self.role not in self.REVENUE_ROLES:

            print(
                f"🔒 Revenue Hidden for Role: "
                f"{self.role}"
            )

        else:

            try:

                if hasattr(
                    self,
                    "revenue_card"
                ) and self.revenue_card:

                    revenue = (
                        self.dashboard_service
                        .get_total_revenue()
                    )

                    if revenue is None:

                        revenue = 0

                    self.revenue_card.update_value(
                        f"₹{float(revenue):,.2f}"
                    )

            except Exception as e:

                print(
                    "Revenue Card Error:",
                    e
                )

        # --------------------------------------------------
        # OPD
        # --------------------------------------------------

        try:

            if hasattr(
                self,
                "opd_card"
            ):

                self.opd_card.update_value(
                    self.dashboard_service
                    .get_total_opd()
                )

        except Exception as e:

            print(
                "OPD Card Error:",
                e
            )

        # --------------------------------------------------
        # IPD
        # --------------------------------------------------

        try:

            if hasattr(
                self,
                "ipd_card"
            ):

                self.ipd_card.update_value(
                    self.dashboard_service
                    .get_total_ipd()
                )

        except Exception as e:

            print(
                "IPD Card Error:",
                e
            )

        print(
            "Dashboard UI Loaded"
        )


