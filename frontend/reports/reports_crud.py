"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Reports CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class ReportsCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()
        self.check_opd_columns()

    def check_opd_columns(self):

        self.cursor.execute(
            "PRAGMA table_info(opd)"
        )

        columns = self.cursor.fetchall()

        print("OPD TABLE COLUMNS:")

        for col in columns:
            print(col)

    # ==========================================
    # Patient Report
    # ==========================================
    def load_patient_report(
        self,
        from_date=None,
        to_date=None,
        department=None
    ):

        query = """
        SELECT
            patient_id,
            registration_no,
            patient_name,
            gender,
            age,
            mobile,
            department,
            created_at
        FROM patients
        WHERE 1=1
        """

        params = []

        if from_date and to_date:

            from datetime import datetime

            from_date = datetime.strptime(
                from_date,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            to_date = datetime.strptime(
                to_date,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            query += """
            AND DATE(created_at)
            BETWEEN ?
            AND ?
            """

            params.append(from_date)
            params.append(to_date)

        if department and department != "All Departments":

            query += """
            AND department=?
            """

            params.append(department)

        query += """
        ORDER BY id DESC
        """

        self.cursor.execute(
            query,
            params
        )

        rows = self.cursor.fetchall()

        print("Patient Report Data:", rows)

        return rows

    # ==========================================
    # Doctor Report With Filter
    # ==========================================

    def load_doctor_report(
        self,
        from_date=None,
        to_date=None,
        department=None
    ):

        query = """
        SELECT
            doctor_id,
            full_name,
            specialization,
            qualification,
            mobile,
            consultation_fee
        FROM doctors
        WHERE 1=1
        """

        params = []

        if department and department != "All Departments":

            query += """
            AND specialization=?
            """

            params.append(department)

        query += """
        ORDER BY id DESC
        """

        self.cursor.execute(
            query,
            params
        )

        rows = self.cursor.fetchall()

        print("Doctor Report Data:", rows)

        return rows

    # ==========================================
    # Appointment Report With Filter
    # ==========================================

    def load_appointment_report(
        self,
        from_date=None,
        to_date=None,
        department=None
    ):

        query = """
            SELECT
                appointment_id,
                patient_name,
                doctor_name,
                department,
                appointment_date,
                appointment_time,
                token_no,
                status
            FROM appointments
            WHERE 1=1
        """

        params = []

        # ==========================================
        # Date Filter
        # ==========================================

        if from_date and to_date:

            from datetime import datetime

            try:
                from_date = datetime.strptime(
                    from_date,
                    "%d-%m-%Y"
                ).strftime("%Y-%m-%d")

                to_date = datetime.strptime(
                    to_date,
                    "%d-%m-%Y"
                ).strftime("%Y-%m-%d")

            except ValueError:
                print("Invalid appointment report date format")
                return []

            query += """
                AND (
                    CASE
                        WHEN appointment_date LIKE '__-__-____'
                        THEN
                            substr(appointment_date, 7, 4)
                            || '-' ||
                            substr(appointment_date, 4, 2)
                            || '-' ||
                            substr(appointment_date, 1, 2)
                        ELSE
                            appointment_date
                    END
                ) BETWEEN ? AND ?
            """

            params.append(from_date)
            params.append(to_date)

        # ==========================================
        # Department Filter
        # ==========================================

        if department and department != "All Departments":

            query += """
                AND department = ?
            """

            params.append(department)

        # ==========================================
        # Order
        # ==========================================

        query += """
            ORDER BY id DESC
        """

        # ==========================================
        # Execute
        # ==========================================

        print("Appointment Query:", query)
        print("Appointment Params:", params)

        self.cursor.execute(
            query,
            params
        )

        rows = self.cursor.fetchall()

        print(
            "Appointment Report Data:",
            rows
        )

        return rows
    # ==========================================
    # OPD Report With Filter
    # ==========================================

    def load_opd_report(
        self,
        from_date=None,
        to_date=None,
        department=None
    ):

        self.cursor.execute("SELECT * FROM opd")

        test = self.cursor.fetchall()

        print("ALL OPD DATA =", test)

        query = """
        SELECT
            opd_id,
            patient,
            doctor,
            department,
            visit_date,
            visit_time,
            diagnosis,
            status
        FROM opd
        WHERE 1=1
        """

        params = []

        if from_date and to_date:
            query += """
            AND visit_date BETWEEN ? AND ?
            """
            params.extend([from_date, to_date])

        if department and department != "All Departments":
            query += """
            AND department=?
            """
            params.append(department)

        query += """
        ORDER BY opd_id DESC
        """

        self.cursor.execute(
            query,
            params
        )

        rows = self.cursor.fetchall()

        print(
            "OPD Report Data:",
            rows
        )

        return rows

    # ==========================================
    # IPD Report
    # ==========================================

    def load_ipd_report(self):

        self.cursor.execute(
            "PRAGMA table_info(ipd)"
        )

        columns = self.cursor.fetchall()

        print("IPD TABLE COLUMNS:")

        for col in columns:
            print(col)

        self.cursor.execute("""
        SELECT
            id,
            patient,
            doctor,
            ward,
            bed_no,
            admission_date,
            discharge_date,
            status
        FROM ipd
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        print("IPD Report Data:", rows)

        return rows

    # ==========================================
    # Billing Report
    # ==========================================

    def load_billing_report(self):

        self.cursor.execute("""
        SELECT
            bill_id,
            patient,
            doctor,
            bill_date,
            total_amount,
            discount,
            total_amount,
            bill_status
        FROM billing
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        print("Billing Report Data:", rows)

        return rows

    def load_pharmacy_report(self):

        self.cursor.execute("""
        SELECT
            medicine_id,
            medicine_name,
            company_name,
            category,
            stock_quantity,
            selling_price,
            expiry_date
        FROM medicines
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()      # <-- Is line ko add karo
        print("Pharmacy Report:", rows)    # <-- Is line ko add karo
        return rows    
    # ==========================================
    # Laboratory Report
    # ==========================================
    def load_laboratory_report(self):

        self.cursor.execute("""
        SELECT
            test_id,
            test_name,
            patient,
            doctor,
            department,
            test_fee,
            status
        FROM laboratory
        ORDER BY id DESC
        """)

        return self.cursor.fetchall()
    # ==========================================
    # Inventory Report
    # ==========================================
    def load_inventory_report(self):

        self.cursor.execute("""
        SELECT
            item_id,
            item_name,
            category,
            supplier,
            stock_quantity,
            selling_price,
            expiry_date
        FROM inventory
        ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Accounts Report
    # ==========================================
    def load_accounts_report(self):
        self.cursor.execute("""
        SELECT
            transaction_id,
            transaction_type,
            category,
            amount,
            payment_mode,
            transaction_date
        FROM accounts
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()
        print("Accounts Report =", rows)
        return rows