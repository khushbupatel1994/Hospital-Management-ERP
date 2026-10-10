"""
===========================================================
Cloud Secure Hospital ERP
Role Based Permission System
Version : 5.0
===========================================================
"""


class Permissions:

    # =====================================================
    # ALL ROLE PERMISSIONS
    # =====================================================

    ROLES = {

        # =================================================
        # SUPER ADMIN
        # =================================================

        "Super Admin": {

            "dashboard": True,
            "users": True,
            "patients": True,
            "doctors": True,
            "appointments": True,
            "opd": True,
            "ipd": True,
            "billing": True,
            "pharmacy": True,
            "laboratory": True,
            "inventory": True,
            "accounts": True,
            "reports": True,
            "analytics": True,
            "ai": True,
            "hr": True,
            "settings": True,
            "backup": True
        },

        # =================================================
        # ADMIN
        # =================================================

        "Admin": {

            "dashboard": True,

            "users": True,
            "patients": True,
            "doctors": True,
            "appointments": True,
            "opd": True,
            "ipd": True,

            "billing": True,
            "pharmacy": True,
            "laboratory": True,
            "inventory": True,
            "accounts": True,

            "reports": True,
            "analytics": True,
            "ai": True,

            "hr": True,

            "settings": False,
            "backup": False
        },

        # =================================================
        # DOCTOR
        # =================================================

        "Doctor": {

            # -------------------------------
            # Dashboard
            # -------------------------------

            "dashboard": True,

            # -------------------------------
            # User Management
            # -------------------------------

            "users": False,

            # -------------------------------
            # Clinical
            # -------------------------------

            "patients": True,
            "doctors": False,
            "appointments": True,
            "opd": True,
            "ipd": True,

            # -------------------------------
            # Financial
            # -------------------------------

            "billing": False,
            "accounts": False,

            # -------------------------------
            # Pharmacy / Inventory
            # -------------------------------

            "pharmacy": False,
            "inventory": False,

            # -------------------------------
            # Laboratory
            # -------------------------------

            "laboratory": True,

            # -------------------------------
            # Reports
            # -------------------------------

            "reports": True,

            # -------------------------------
            # Analytics / AI
            # -------------------------------

            "analytics": False,
            "ai": True,

            # -------------------------------
            # HR / Settings / Backup
            # -------------------------------

            "hr": False,
            "settings": False,
            "backup": False
        },

        # =================================================
        # NURSE
        # =================================================

        "Nurse": {

            "dashboard": True,

            "users": False,

            "patients": True,
            "doctors": False,
            "appointments": True,

            "opd": True,
            "ipd": True,

            "billing": False,

            "pharmacy": False,
            "laboratory": True,
            "inventory": False,
            "accounts": False,

            "reports": True,
            "analytics": False,
            "ai": False,

            "hr": False,
            "settings": False,
            "backup": False
        },

        # =================================================
        # RECEPTIONIST
        # =================================================

        "Receptionist": {

            "dashboard": True,

            "users": False,

            "patients": True,
            "doctors": True,
            "appointments": True,

            "opd": True,
            "ipd": False,

            "billing": True,

            "pharmacy": False,
            "laboratory": False,
            "inventory": False,

            "accounts": False,

            "reports": False,
            "analytics": False,
            "ai": False,

            "hr": False,
            "settings": False,
            "backup": False
        },

        # =================================================
        # OLD RECEPTION ROLE
        # =================================================

        "Reception": {

            "dashboard": True,

            "users": False,

            "patients": True,
            "doctors": True,
            "appointments": True,

            "opd": True,
            "ipd": False,

            "billing": True,

            "pharmacy": False,
            "laboratory": False,
            "inventory": False,

            "accounts": False,

            "reports": False,
            "analytics": False,
            "ai": False,

            "hr": False,
            "settings": False,
            "backup": False
        },

        # =================================================
        # ACCOUNTANT
        # =================================================

        "Accountant": {

            "dashboard": True,

            "users": False,

            "patients": False,
            "doctors": False,
            "appointments": False,

            "opd": False,
            "ipd": False,

            # -------------------------------
            # Financial
            # -------------------------------

            "billing": True,
            "accounts": True,

            # -------------------------------
            # Other Modules
            # -------------------------------

            "pharmacy": False,
            "laboratory": False,
            "inventory": False,

            # -------------------------------
            # Reports
            # -------------------------------

            "reports": True,
            "analytics": True,

            "ai": False,
            "hr": False,

            "settings": False,
            "backup": False
        },

        # =================================================
        # PHARMACIST
        # =================================================

        "Pharmacist": {

            "dashboard": True,

            "users": False,

            "patients": True,
            "doctors": False,
            "appointments": False,

            "opd": False,
            "ipd": False,

            "billing": False,

            # -------------------------------
            # Pharmacy
            # -------------------------------

            "pharmacy": True,

            "laboratory": False,

            # -------------------------------
            # Inventory
            # -------------------------------

            "inventory": True,

            "accounts": False,

            "reports": True,
            "analytics": False,

            "ai": False,
            "hr": False,

            "settings": False,
            "backup": False
        },

        # =================================================
        # LAB TECHNICIAN
        # =================================================

        "Lab Technician": {

            "dashboard": True,

            "users": False,

            "patients": True,
            "doctors": False,
            "appointments": False,

            "opd": False,
            "ipd": False,

            "billing": False,
            "pharmacy": False,

            # -------------------------------
            # Laboratory
            # -------------------------------

            "laboratory": True,

            "inventory": False,
            "accounts": False,

            "reports": True,
            "analytics": False,

            "ai": False,
            "hr": False,

            "settings": False,
            "backup": False
        },

        # =================================================
        # HR
        # =================================================

        "HR": {

            "dashboard": True,

            "users": False,

            "patients": False,
            "doctors": False,
            "appointments": False,

            "opd": False,
            "ipd": False,

            "billing": False,
            "pharmacy": False,
            "laboratory": False,
            "inventory": False,
            "accounts": False,

            "reports": True,
            "analytics": False,
            "ai": False,

            # -------------------------------
            # HR
            # -------------------------------

            "hr": True,

            "settings": False,
            "backup": False
        },

        # =================================================
        # INVENTORY MANAGER
        # =================================================

        "Inventory Manager": {

            "dashboard": True,

            "users": False,

            "patients": False,
            "doctors": False,
            "appointments": False,

            "opd": False,
            "ipd": False,

            "billing": False,

            # -------------------------------
            # Pharmacy
            # -------------------------------

            "pharmacy": True,

            "laboratory": False,

            # -------------------------------
            # Inventory
            # -------------------------------

            "inventory": True,

            "accounts": False,

            "reports": True,
            "analytics": False,
            "ai": False,

            "hr": False,

            "settings": False,
            "backup": False
        }
    }

    # =====================================================
    # CHECK PERMISSION
    # =====================================================

    @classmethod
    def has_permission(
        cls,
        role,
        module
    ):

        if not role:
            return False

        role = str(
            role
        ).strip()

        module = str(
            module
        ).strip().lower()

        permissions = cls.ROLES.get(
            role,
            {}
        )

        allowed = permissions.get(
            module,
            False
        )

        print(
            f"Permission | "
            f"Role={role} | "
            f"Module={module} | "
            f"Allowed={allowed}"
        )

        return allowed

    # =====================================================
    # GET ROLE PERMISSIONS
    # =====================================================

    @classmethod
    def get_permissions(
        cls,
        role
    ):

        if not role:
            return {}

        role = str(
            role
        ).strip()

        return cls.ROLES.get(
            role,
            {}
        ).copy()

    # =====================================================
    # GET ALL ROLES
    # =====================================================

    @classmethod
    def get_roles(cls):

        return list(
            cls.ROLES.keys()
        )

    # =====================================================
    # CHECK ROLE
    # =====================================================

    @classmethod
    def role_exists(
        cls,
        role
    ):

        if not role:
            return False

        return (
            str(role).strip()
            in cls.ROLES
        )

    # =====================================================
    # GET ALLOWED MODULES
    # =====================================================

    @classmethod
    def get_allowed_modules(
        cls,
        role
    ):

        permissions = cls.get_permissions(
            role
        )

        return [
            module
            for module, allowed
            in permissions.items()
            if allowed
        ]

    # =====================================================
    # GET DENIED MODULES
    # =====================================================

    @classmethod
    def get_denied_modules(
        cls,
        role
    ):

        permissions = cls.get_permissions(
            role
        )

        return [
            module
            for module, allowed
            in permissions.items()
            if not allowed
        ]

    # =====================================================
    # REVENUE PERMISSION
    # =====================================================

    @classmethod
    def can_view_revenue(
        cls,
        role
    ):

        allowed_roles = [
            "Super Admin",
            "Admin",
            "Accountant"
        ]

        if not role:
            return False

        return (
            str(role).strip()
            in allowed_roles
        )

    # =====================================================
    # DOCTOR ROLE CHECK
    # =====================================================

    @classmethod
    def is_doctor(
        cls,
        role
    ):

        if not role:
            return False

        return (
            str(role).strip()
            == "Doctor"
        )

    # =====================================================
    # ADMIN ROLE CHECK
    # =====================================================

    @classmethod
    def is_admin(
        cls,
        role
    ):

        if not role:
            return False

        return (
            str(role).strip()
            in [
                "Super Admin",
                "Admin"
            ]
        )

    # =====================================================
    # FINANCIAL ROLE CHECK
    # =====================================================

    @classmethod
    def is_financial_role(
        cls,
        role
    ):

        if not role:
            return False

        return (
            str(role).strip()
            in [
                "Super Admin",
                "Admin",
                "Accountant"
            ]
        )
