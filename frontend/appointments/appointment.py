"""
===========================================================
Cloud Secure Hospital ERP
Appointment Management
Role Based Appointment Access
Version : 6.0
===========================================================

Features:
- Appointment CRUD
- Doctor-wise appointment filtering
- Doctor login -> only assigned patients
- Patient Father/Husband Name
- Patient Disease
- Doctor Department
- Search
- Refresh
- Add / Update / Delete
- Role based access
- Existing database safe migration
===========================================================
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from database.database import Database
from frontend.appointments.appointment_ui import AppointmentUI


class Appointment(Database):

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(
        self,
        parent,
        user=None,
        role=None,
        api_client=None
    ):
        super().__init__()

        self.parent = parent
        self.api_client = api_client
        self.user = user

        self.role = (
            str(role).strip()
            if role
            else ""
        )

        self.selected_appointment_id = None

        # -------------------------------------------------
        # Database connection
        # -------------------------------------------------

        try:
            self.connect()
        except Exception as e:
            print(
                "Appointment Database Error:",
                e
            )

        # -------------------------------------------------
        # Appointment table
        # -------------------------------------------------

        self.create_appointment_table()

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.ui = AppointmentUI(
            self.parent,
            controller=self
        )

        # -------------------------------------------------
        # Events
        # -------------------------------------------------

        self.bind_events()

        # -------------------------------------------------
        # Initial data
        # -------------------------------------------------

        self.initialize_data()

        print(
            "📅 Appointment Screen Loaded"
        )

    # =====================================================
    # CREATE / VERIFY APPOINTMENT TABLE
    # =====================================================

    def create_appointment_table(self):

        try:

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS appointments(

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    appointment_id TEXT UNIQUE,

                    patient_name TEXT,

                    doctor_name TEXT,

                    department TEXT,

                    appointment_date TEXT,

                    appointment_time TEXT,

                    visit_type TEXT,

                    token_no TEXT,

                    status TEXT,

                    remarks TEXT,

                    created_at TEXT
                    DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            self.commit()

            print(
                "✅ Appointment Table Verified"
            )

            self.migrate_appointment_table()

        except Exception as e:

            print(
                "Appointment Table Error:",
                e
            )

    # =====================================================
    # MIGRATION
    # =====================================================

    def migrate_appointment_table(self):

        try:

            self.cursor.execute(
                "PRAGMA table_info(appointments)"
            )

            existing_columns = {
                row[1]
                for row in self.cursor.fetchall()
            }

            required_columns = [
                (
                    "father_husband_name",
                    "TEXT"
                ),
                (
                    "disease",
                    "TEXT"
                )
            ]

            for column, data_type in required_columns:

                if column not in existing_columns:

                    self.cursor.execute(
                        f"""
                        ALTER TABLE appointments
                        ADD COLUMN {column} {data_type}
                        """
                    )

                    print(
                        f"✅ Added appointments.{column}"
                    )

            self.commit()

            print(
                "✅ Appointment table migration completed"
            )

        except Exception as e:

            print(
                "Appointment Migration Error:",
                e
            )

    # =====================================================
    # BIND EVENTS
    # =====================================================

    def bind_events(self):

        try:

            if hasattr(
                self.ui,
                "add_button"
            ):
                self.ui.add_button.configure(
                    command=self.add_appointment
                )

            if hasattr(
                self.ui,
                "update_button"
            ):
                self.ui.update_button.configure(
                    command=self.update_appointment
                )

            if hasattr(
                self.ui,
                "delete_button"
            ):
                self.ui.delete_button.configure(
                    command=self.delete_appointment
                )

            if hasattr(
                self.ui,
                "search_button"
            ):
                self.ui.search_button.configure(
                    command=self.search_appointment
                )

            if hasattr(
                self.ui,
                "refresh_button"
            ):
                self.ui.refresh_button.configure(
                    command=self.refresh_appointments
                )

            print(
                "✅ Appointment Events Bound"
            )

        except Exception as e:

            print(
                "Appointment Event Error:",
                e
            )

    # =====================================================
    # INITIAL DATA
    # =====================================================

    def initialize_data(self):

        try:

            self.load_doctors()
            self.load_patients()
            self.load_appointments()

        except Exception as e:

            print(
                "Appointment Initialization Error:",
                e
            )

    # =====================================================
    # ROLE
    # =====================================================

    def is_doctor(self):

        return (
            self.role.lower()
            == "doctor"
        )

    # =====================================================
    # TABLE COLUMNS
    # =====================================================

    def get_table_columns(
        self,
        table_name
    ):

        columns = []

        try:

            self.cursor.execute(
                f"""
                PRAGMA table_info({table_name})
                """
            )

            for row in self.cursor.fetchall():

                if len(row) > 1:

                    if row[1]:

                        columns.append(
                            str(
                                row[1]
                            ).strip()
                        )

        except Exception as e:

            print(
                f"Table Columns Error ({table_name}):",
                e
            )

        return columns

    # =====================================================
    # FIND COLUMN
    # =====================================================

    def find_column(
        self,
        columns,
        candidates
    ):

        lower_map = {
            str(column).lower(): column
            for column in columns
        }

        for candidate in candidates:

            if (
                candidate.lower()
                in lower_map
            ):

                return lower_map[
                    candidate.lower()
                ]

        return None

    # =====================================================
    # PATIENT COLUMNS
    # =====================================================

    def get_patient_columns(self):

        return self.get_table_columns(
            "patients"
        )

    # =====================================================
    # LOGGED-IN DOCTOR IDENTITY
    # =====================================================

    def get_logged_in_doctor_names(
        self
    ):

        names = []

        def add(value):

            if value is None:
                return

            value = str(
                value
            ).strip()

            if not value:
                return

            # Never treat password hash as identity.
            if (
                value.startswith("$2b$")
                or value.startswith("$2a$")
                or value.startswith("$2y$")
            ):
                return

            existing = {
                item.lower()
                for item in names
            }

            if value.lower() not in existing:

                names.append(
                    value
                )

        try:

            # -------------------------------------------------
            # sqlite3.Row / mapping-like object
            # -------------------------------------------------

            if (
                hasattr(
                    self.user,
                    "keys"
                )
                and callable(
                    self.user.keys
                )
            ):

                keys = set(
                    self.user.keys()
                )

                for key in (
                    "full_name",
                    "name",
                    "doctor_name",
                    "display_name",
                    "username",
                    "user_name",
                    "employee_id",
                    "doctor_id",
                    "doctor_code",
                    "email"
                ):

                    if key in keys:

                        add(
                            self.user[key]
                        )

            # -------------------------------------------------
            # dictionary
            # -------------------------------------------------

            elif isinstance(
                self.user,
                dict
            ):

                for key in (
                    "full_name",
                    "name",
                    "doctor_name",
                    "display_name",
                    "username",
                    "user_name",
                    "employee_id",
                    "doctor_id",
                    "doctor_code",
                    "email"
                ):

                    add(
                        self.user.get(
                            key
                        )
                    )

            # -------------------------------------------------
            # tuple/list
            # -------------------------------------------------

            elif isinstance(
                self.user,
                (tuple, list)
            ):

                # users table:
                # 1 employee_id
                # 2 full_name
                # 3 username

                if len(self.user) > 1:

                    add(
                        self.user[1]
                    )

                if len(self.user) > 2:

                    add(
                        self.user[2]
                    )

                if len(self.user) > 3:

                    add(
                        self.user[3]
                    )

            # -------------------------------------------------
            # Resolve from users table
            # -------------------------------------------------

            username = None
            employee_id = None
            full_name = None

            if (
                hasattr(
                    self.user,
                    "keys"
                )
                and callable(
                    self.user.keys
                )
            ):

                keys = set(
                    self.user.keys()
                )

                if "username" in keys:

                    username = (
                        self.user["username"]
                    )

                elif "user_name" in keys:

                    username = (
                        self.user["user_name"]
                    )

                if "employee_id" in keys:

                    employee_id = (
                        self.user["employee_id"]
                    )

                if "full_name" in keys:

                    full_name = (
                        self.user["full_name"]
                    )

                elif "name" in keys:

                    full_name = (
                        self.user["name"]
                    )

            elif isinstance(
                self.user,
                dict
            ):

                username = (
                    self.user.get(
                        "username"
                    )
                    or
                    self.user.get(
                        "user_name"
                    )
                )

                employee_id = (
                    self.user.get(
                        "employee_id"
                    )
                )

                full_name = (
                    self.user.get(
                        "full_name"
                    )
                    or
                    self.user.get(
                        "name"
                    )
                )

            elif isinstance(
                self.user,
                (tuple, list)
            ):

                if len(self.user) > 3:

                    username = (
                        self.user[3]
                    )

                if len(self.user) > 2:

                    full_name = (
                        self.user[2]
                    )

                if len(self.user) > 1:

                    employee_id = (
                        self.user[1]
                    )

            # -------------------------------------------------
            # Username lookup
            # -------------------------------------------------

            if username:

                self.cursor.execute(
                    """
                    SELECT
                        employee_id,
                        full_name,
                        username
                    FROM users
                    WHERE LOWER(TRIM(username))
                        =
                        LOWER(TRIM(?))
                    LIMIT 1
                    """,
                    (
                        str(
                            username
                        ).strip(),
                    )
                )

                row = (
                    self.cursor.fetchone()
                )

                if row:

                    for value in row:

                        add(
                            value
                        )

            # -------------------------------------------------
            # Employee lookup
            # -------------------------------------------------

            if employee_id:

                try:

                    self.cursor.execute(
                        """
                        SELECT
                            employee_id,
                            full_name,
                            username
                        FROM users
                        WHERE LOWER(TRIM(employee_id))
                            =
                            LOWER(TRIM(?))
                        LIMIT 1
                        """,
                        (
                            str(
                                employee_id
                            ).strip(),
                        )
                    )

                    row = (
                        self.cursor.fetchone()
                    )

                    if row:

                        for value in row:

                            add(
                                value
                            )

                except Exception as e:

                    print(
                        "Employee ID Mapping Warning:",
                        e
                    )

            add(
                full_name
            )

        except Exception as e:

            print(
                "Doctor Identity Error:",
                e
            )

        print(
            "🔐 Logged Doctor Identity Candidates:",
            names
        )

        return names

    # =====================================================
    # FIND ACTUAL DOCTOR NAME
    # =====================================================

    def get_logged_doctor_full_names(
        self
    ):

        result = []

        candidates = (
            self.get_logged_in_doctor_names()
        )

        if not candidates:

            print(
                "🩺 Matched Doctor Names: []"
            )

            return result

        def add(value):

            if value is None:
                return

            value = str(
                value
            ).strip()

            if not value:
                return

            if (
                value.lower()
                not in {
                    x.lower()
                    for x in result
                }
            ):

                result.append(
                    value
                )

        try:

            columns = (
                self.get_table_columns(
                    "doctors"
                )
            )

            identity_columns = [
                column
                for column in (
                    "doctor_id",
                    "doctor_code",
                    "full_name",
                    "name",
                    "email",
                    "mobile"
                )
                if column in columns
            ]

            if identity_columns:

                select_columns = []

                for column in (
                    "full_name",
                    "name",
                    "doctor_id",
                    "doctor_code"
                ):

                    if column in columns:

                        select_columns.append(
                            column
                        )

                if select_columns:

                    self.cursor.execute(
                        f"""
                        SELECT
                            {", ".join(select_columns)}
                        FROM doctors
                        """
                    )

                    rows = (
                        self.cursor.fetchall()
                    )

                    for row in rows:

                        row_values = [
                            str(value).strip()
                            for value in row
                            if value
                        ]

                        for candidate in candidates:

                            candidate_lower = (
                                str(candidate)
                                .strip()
                                .lower()
                            )

                            for index, value in enumerate(
                                row_values
                            ):

                                value_lower = (
                                    value.lower()
                                )

                                if (
                                    value_lower
                                    == candidate_lower
                                    or
                                    candidate_lower
                                    in value_lower
                                    or
                                    value_lower
                                    in candidate_lower
                                ):

                                    # Prefer actual doctor full name.
                                    for idx, column in enumerate(
                                        select_columns
                                    ):

                                        if (
                                            column in (
                                                "full_name",
                                                "name"
                                            )
                                            and
                                            row[idx]
                                        ):

                                            add(
                                                row[idx]
                                            )

            # -------------------------------------------------
            # fallback candidates
            # -------------------------------------------------

            for candidate in candidates:

                add(
                    candidate
                )

        except Exception as e:

            print(
                "Doctor Name Lookup Error:",
                e
            )

            for candidate in candidates:

                add(
                    candidate
                )

        print(
            "🩺 Matched Doctor Names:",
            result
        )

        return result

    # =====================================================
    # LOAD DOCTORS
    # =====================================================

    def load_doctors(self):

        try:

            if self.is_doctor():

                doctors = (
                    self.get_logged_doctor_full_names()
                )

                if not doctors:

                    doctors = (
                        self.get_logged_in_doctor_names()
                    )

                if hasattr(
                    self.ui,
                    "set_doctors"
                ):

                    self.ui.set_doctors(
                        doctors
                    )

                print(
                    "🩺 Doctor Login - Own Doctor Only:",
                    doctors
                )

                return doctors

            self.cursor.execute(
                """
                SELECT full_name
                FROM doctors
                WHERE full_name IS NOT NULL
                AND TRIM(full_name) <> ''
                ORDER BY full_name
                """
            )

            rows = (
                self.cursor.fetchall()
            )

            doctors = []

            for row in rows:

                if row and row[0]:

                    doctors.append(
                        str(
                            row[0]
                        ).strip()
                    )

            if hasattr(
                self.ui,
                "set_doctors"
            ):

                self.ui.set_doctors(
                    doctors
                )

            return doctors

        except Exception as e:

            print(
                "Load Doctors Error:",
                e
            )

            return []

    # =====================================================
    # LOAD PATIENTS
    # =====================================================

    def load_patients(self):

        try:

            # -------------------------------------------------
            # Doctor = only assigned patients
            # -------------------------------------------------

            if self.is_doctor():

                doctor_names = (
                    self.get_logged_doctor_full_names()
                )

                if not doctor_names:

                    doctor_names = (
                        self.get_logged_in_doctor_names()
                    )

                if not doctor_names:

                    print(
                        "⚠ Doctor identity not found"
                    )

                    if hasattr(
                        self.ui,
                        "set_patients"
                    ):

                        self.ui.set_patients(
                            []
                        )

                    return []

                conditions = []
                params = []

                for doctor_name in doctor_names:

                    conditions.append(
                        """
                        LOWER(TRIM(doctor_name))
                        =
                        LOWER(TRIM(?))
                        """
                    )

                    params.append(
                        doctor_name
                    )

                query = f"""
                    SELECT DISTINCT patient_name
                    FROM appointments
                    WHERE (
                        {" OR ".join(conditions)}
                    )
                    AND patient_name IS NOT NULL
                    AND TRIM(patient_name) <> ''
                    ORDER BY patient_name
                """

                self.cursor.execute(
                    query,
                    tuple(params)
                )

                rows = (
                    self.cursor.fetchall()
                )

                patients = []

                for row in rows:

                    if row and row[0]:

                        patients.append(
                            str(
                                row[0]
                            ).strip()
                        )

                if hasattr(
                    self.ui,
                    "set_assigned_patients"
                ):

                    self.ui.set_assigned_patients(
                        patients
                    )

                elif hasattr(
                    self.ui,
                    "set_patients"
                ):

                    self.ui.set_patients(
                        patients
                    )

                print(
                    "👨‍⚕ Assigned Patients:",
                    patients
                )

                return patients

            # -------------------------------------------------
            # Other roles = all patients
            # -------------------------------------------------

            columns = (
                self.get_patient_columns()
            )

            name_column = (
                self.find_column(
                    columns,
                    [
                        "patient_name",
                        "name",
                        "full_name"
                    ]
                )
            )

            if not name_column:

                return []

            self.cursor.execute(
                f"""
                SELECT
                    {name_column}
                FROM patients
                WHERE {name_column} IS NOT NULL
                AND TRIM({name_column}) <> ''
                ORDER BY {name_column}
                """
            )

            rows = (
                self.cursor.fetchall()
            )

            patients = []

            for row in rows:

                if row and row[0]:

                    patients.append(
                        str(
                            row[0]
                        ).strip()
                    )

            if hasattr(
                self.ui,
                "set_patients"
            ):

                self.ui.set_patients(
                    patients
                )

            return patients

        except Exception as e:

            print(
                "Load Patients Error:",
                e
            )

            return []

    # =====================================================
    # PATIENT DETAILS
    # =====================================================

    def get_patient_details_without_ui(
        self,
        patient_name
    ):

        if not patient_name:

            return None

        try:

            columns = (
                self.get_patient_columns()
            )

            name_column = (
                self.find_column(
                    columns,
                    [
                        "patient_name",
                        "name",
                        "full_name"
                    ]
                )
            )

            father_column = (
                self.find_column(
                    columns,
                    [
                        "father_husband_name",
                        "father_name",
                        "husband_name",
                        "guardian_name",
                        "relative_name"
                    ]
                )
            )

            disease_column = (
                self.find_column(
                    columns,
                    [
                        "disease",
                        "diseases",
                        "diagnosis",
                        "problem",
                        "medical_problem",
                        "complaint"
                    ]
                )
            )

            department_column = (
                self.find_column(
                    columns,
                    [
                        "department"
                    ]
                )
            )

            if not name_column:

                return None

            selected_columns = [
                name_column
            ]

            if father_column:

                selected_columns.append(
                    father_column
                )

            if disease_column:

                selected_columns.append(
                    disease_column
                )

            if department_column:

                selected_columns.append(
                    department_column
                )

            self.cursor.execute(
                f"""
                SELECT
                    {", ".join(selected_columns)}
                FROM patients
                WHERE LOWER(TRIM({name_column}))
                    =
                    LOWER(TRIM(?))
                LIMIT 1
                """,
                (
                    patient_name,
                )
            )

            row = (
                self.cursor.fetchone()
            )

            if not row:

                return None

            result = {
                "patient_name": "",
                "father_husband_name": "",
                "disease": "",
                "department": ""
            }

            index = 0

            result[
                "patient_name"
            ] = row[index] or ""

            index += 1

            if father_column:

                if len(row) > index:

                    result[
                        "father_husband_name"
                    ] = row[index] or ""

                index += 1

            if disease_column:

                if len(row) > index:

                    result[
                        "disease"
                    ] = row[index] or ""

                index += 1

            if department_column:

                if len(row) > index:

                    result[
                        "department"
                    ] = row[index] or ""

            return result

        except Exception as e:

            print(
                "Patient Details Error:",
                e
            )

            return None

    # =====================================================
    # GET PATIENT DETAILS
    # =====================================================

    def get_patient_details(
        self,
        patient_name
    ):

        details = (
            self.get_patient_details_without_ui(
                patient_name
            )
        )

        if details and hasattr(
            self.ui,
            "set_patient_details"
        ):

            self.ui.set_patient_details(
                details
            )

        return details

    # =====================================================
    # GET DOCTOR DEPARTMENT
    # =====================================================

    def get_doctor_department(
        self,
        doctor_name
    ):

        try:

            self.cursor.execute(
                """
                SELECT department
                FROM doctors
                WHERE LOWER(TRIM(full_name))
                    =
                    LOWER(TRIM(?))
                LIMIT 1
                """,
                (
                    doctor_name,
                )
            )

            row = (
                self.cursor.fetchone()
            )

            if row and row[0]:

                return str(
                    row[0]
                ).strip()

        except Exception as e:

            print(
                "Doctor Department Error:",
                e
            )

        return ""

    # =====================================================
    # GENERATE APPOINTMENT ID
    # =====================================================

    def generate_appointment_id(self):

        try:

            self.cursor.execute(
                """
                SELECT
                    MAX(id)
                FROM appointments
                """
            )

            row = (
                self.cursor.fetchone()
            )

            last_id = (
                row[0]
                if row and row[0]
                else 0
            )

            next_id = (
                int(last_id)
                + 1
            )

            return (
                f"APT{next_id:06d}"
            )

        except Exception:

            return (
                "APT"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )

    # =====================================================
    # GENERATE TOKEN
    # =====================================================

    def generate_token_no(self):

        try:

            today = datetime.now().strftime(
                "%d/%m/%Y"
            )

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM appointments
                WHERE appointment_date=?
                """,
                (
                    today,
                )
            )

            row = (
                self.cursor.fetchone()
            )

            count = (
                row[0]
                if row
                else 0
            )

            return str(
                count + 1
            )

        except Exception:

            return "1"

    # =====================================================
    # DUPLICATE TOKEN
    # =====================================================

    def check_duplicate_token(
        self,
        token_no,
        appointment_db_id=None
    ):

        try:

            if appointment_db_id:

                self.cursor.execute(
                    """
                    SELECT id
                    FROM appointments
                    WHERE token_no=?
                    AND id<>?
                    """,
                    (
                        token_no,
                        appointment_db_id
                    )
                )

            else:

                self.cursor.execute(
                    """
                    SELECT id
                    FROM appointments
                    WHERE token_no=?
                    """,
                    (
                        token_no,
                    )
                )

            return (
                self.cursor.fetchone()
            )

        except Exception as e:

            print(
                "Token Check Error:",
                e
            )

            return None

    # =====================================================
    # FORM DATA
    # =====================================================

    def get_form_data(self):

        try:

            if hasattr(
                self.ui,
                "get_form_data"
            ):

                return (
                    self.ui.get_form_data()
                )

        except Exception as e:

            print(
                "Get Form Data Error:",
                e
            )

        return {}

    # =====================================================
    # ADD APPOINTMENT
    # =====================================================

    def add_appointment(self):

        try:

            data = (
                self.get_form_data()
            )

            patient_name = str(
                data.get(
                    "patient_name",
                    ""
                )
            ).strip()

            father_husband_name = str(
                data.get(
                    "father_husband_name",
                    ""
                )
            ).strip()

            disease = str(
                data.get(
                    "disease",
                    ""
                )
            ).strip()

            doctor_name = str(
                data.get(
                    "doctor_name",
                    ""
                )
            ).strip()

            department = str(
                data.get(
                    "department",
                    ""
                )
            ).strip()

            appointment_date = str(
                data.get(
                    "appointment_date",
                    ""
                )
            ).strip()

            appointment_time = str(
                data.get(
                    "appointment_time",
                    ""
                )
            ).strip()

            visit_type = str(
                data.get(
                    "visit_type",
                    "OPD"
                )
            ).strip()

            token_no = str(
                data.get(
                    "token_no",
                    ""
                )
            ).strip()

            status = str(
                data.get(
                    "status",
                    "Pending"
                )
            ).strip()

            remarks = str(
                data.get(
                    "remarks",
                    ""
                )
            ).strip()

            # -------------------------------------------------
            # If fields are blank, get them from patient record.
            # -------------------------------------------------

            patient_details = (
                self.get_patient_details_without_ui(
                    patient_name
                )
            )

            if patient_details:

                if not father_husband_name:

                    father_husband_name = str(
                        patient_details.get(
                            "father_husband_name",
                            ""
                        )
                    ).strip()

                if not disease:

                    disease = str(
                        patient_details.get(
                            "disease",
                            ""
                        )
                    ).strip()

                if (
                    not department
                    and patient_details.get(
                        "department"
                    )
                ):

                    department = str(
                        patient_details.get(
                            "department"
                        )
                    ).strip()

            # -------------------------------------------------
            # Validation
            # -------------------------------------------------

            if not patient_name:

                self.show_error(
                    "Please select Patient."
                )

                return False

            if not doctor_name:

                self.show_error(
                    "Please select Doctor."
                )

                return False

            if not appointment_date:

                self.show_error(
                    "Please enter Appointment Date."
                )

                return False

            if not appointment_time:

                self.show_error(
                    "Please enter Appointment Time."
                )

                return False

            # -------------------------------------------------
            # Doctor security
            # -------------------------------------------------

            if self.is_doctor():

                allowed_doctors = (
                    self.get_logged_doctor_full_names()
                )

                if not allowed_doctors:

                    allowed_doctors = (
                        self.get_logged_in_doctor_names()
                    )

                allowed = any(
                    str(name).strip().lower()
                    ==
                    doctor_name.strip().lower()
                    for name in allowed_doctors
                )

                if not allowed:

                    self.show_error(
                        "You can only create appointments "
                        "for your own patients."
                    )

                    return False

            # -------------------------------------------------
            # Token
            # -------------------------------------------------

            if not token_no:

                token_no = (
                    self.generate_token_no()
                )

            # -------------------------------------------------
            # Duplicate token
            # -------------------------------------------------

            if self.check_duplicate_token(
                token_no
            ):

                self.show_error(
                    f"Token {token_no} already exists."
                )

                return False

            # -------------------------------------------------
            # Appointment ID
            # -------------------------------------------------

            appointment_id = (
                self.generate_appointment_id()
            )

            # -------------------------------------------------
            # -------------------------------------------------
            # CLOUD API ADD
            # -------------------------------------------------

            if self.api_client:

                payload = {
                    "appointment_id": appointment_id,
                    "patient_name": patient_name,
                    "father_husband_name": father_husband_name,
                    "disease": disease,
                    "doctor_name": doctor_name,
                    "department": department,
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time,
                    "visit_type": visit_type,
                    "token_no": token_no,
                    "status": status,
                    "remarks": remarks
                }

                try:

                    print("Adding Appointment through Central API...")

                    api_result = self.api_client.request(
                        "POST",
                        "/api/v1/modules/appointments/records",
                        json={"data": payload}
                    )

                    if isinstance(api_result, dict) and api_result.get("ok"):

                        cloud_id = api_result.get("id")

                        self.selected_appointment_id = (
                            int(cloud_id)
                            if cloud_id is not None
                            else None
                        )

                        print("Central Appointment Created:", api_result)

                        self.show_success(
                            f"Appointment {appointment_id} added successfully."
                        )

                        self.load_appointments()

                        return True

                    self.show_error(
                        "Unable to add appointment on the hospital server."
                    )
                    return False

                except Exception as e:

                    print("Cloud Appointment Add Error:", e)

                    self.show_error(
                        f"Unable to add appointment on the hospital server.\n\n{e}"
                    )
                    return False

            # INSERT
            # -------------------------------------------------

            self.cursor.execute(
                """
                INSERT INTO appointments
                (
                    appointment_id,
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    status,
                    remarks
                )
                VALUES
                (
                    ?,?,?,?,?,?,?,?,?,?,?,?
                )
                """,
                (
                    appointment_id,
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    status,
                    remarks
                )
            )

            self.commit()

            # -------------------------------------------------
            # Find actual inserted DB ID
            # -------------------------------------------------

            self.cursor.execute(
                """
                SELECT id
                FROM appointments
                WHERE appointment_id=?
                LIMIT 1
                """,
                (
                    appointment_id,
                )
            )

            inserted = (
                self.cursor.fetchone()
            )

            if inserted:

                self.selected_appointment_id = int(
                    inserted[0]
                )

            print(
                "✅ Appointment Added:",
                appointment_id
            )

            self.show_success(
                f"Appointment {appointment_id} "
                f"added successfully."
            )

            self.load_appointments()

            self.load_patients()

            return True

        except Exception as e:

            print(
                "Add Appointment Error:",
                e
            )

            self.show_error(
                f"Add Appointment Error:\n{e}"
            )

            return False

    # =====================================================
    # LOAD APPOINTMENTS
    # =====================================================

    def load_appointments(
        self,
        keyword=""
    ):

        try:

            # =================================================
            # CLOUD API LOAD
            # =================================================

            if self.api_client:

                print("Loading Appointments from Central API...")

                response = self.api_client.request(
                    "GET",
                    "/api/v1/modules/appointments/records",
                    params={
                        "limit": 100,
                        "offset": 0,
                        "search": str(keyword or "").strip()
                    }
                )

                items = response.get("items", []) if isinstance(response, dict) else []

                # Keep the complete cloud records locally so row selection
                # does not require a separate GET /records/{id} endpoint.
                self._cloud_appointments = items if isinstance(items, list) else []

                display_rows = []

                for item in items:
                    display_rows.append((
                        item.get("id", ""),
                        item.get("appointment_id", ""),
                        item.get("patient_name", ""),
                        item.get("father_husband_name", ""),
                        item.get("disease", ""),
                        item.get("doctor_name", ""),
                        item.get("department", ""),
                        item.get("appointment_date", ""),
                        item.get("appointment_time", ""),
                        item.get("token_no", ""),
                        item.get("status", "") or "Pending",
                        item.get("remarks", "")
                    ))

                if hasattr(self.ui, "load_data"):
                    self.ui.load_data(display_rows)

                print("Appointments Loaded from Cloud:", len(display_rows))
                return display_rows


            base_query = """
                SELECT
                    a.id,
                    a.appointment_id,
                    a.patient_name,
                    a.father_husband_name,
                    a.disease,
                    a.doctor_name,
                    a.department,
                    a.appointment_date,
                    a.appointment_time,
                    a.visit_type,
                    a.token_no,
                    a.status,
                    a.remarks
                FROM appointments a
            """

            conditions = []
            params = []

            # -------------------------------------------------
            # Doctor filter
            # -------------------------------------------------

            if self.is_doctor():

                doctor_names = (
                    self.get_logged_doctor_full_names()
                )

                if not doctor_names:

                    doctor_names = (
                        self.get_logged_in_doctor_names()
                    )

                if not doctor_names:

                    conditions.append(
                        "1=0"
                    )

                else:

                    doctor_conditions = []

                    for doctor_name in doctor_names:

                        doctor_conditions.append(
                            """
                            LOWER(TRIM(a.doctor_name))
                            =
                            LOWER(TRIM(?))
                            """
                        )

                        params.append(
                            doctor_name
                        )

                    conditions.append(
                        "("
                        + " OR ".join(
                            doctor_conditions
                        )
                        + ")"
                    )

            # -------------------------------------------------
            # Search
            # -------------------------------------------------

            keyword = str(
                keyword or ""
            ).strip()

            if keyword:

                search = (
                    f"%{keyword}%"
                )

                conditions.append(
                    """
                    (
                        a.appointment_id LIKE ?
                        OR a.patient_name LIKE ?
                        OR COALESCE(a.father_husband_name, '') LIKE ?
                        OR COALESCE(a.disease, '') LIKE ?
                        OR a.doctor_name LIKE ?
                        OR a.department LIKE ?
                        OR a.appointment_date LIKE ?
                        OR a.appointment_time LIKE ?
                        OR a.visit_type LIKE ?
                        OR a.token_no LIKE ?
                        OR a.status LIKE ?
                        OR a.remarks LIKE ?
                    )
                    """
                )

                params.extend(
                    [
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search,
                        search
                    ]
                )

            # -------------------------------------------------
            # WHERE
            # -------------------------------------------------

            if conditions:

                base_query += (
                    " WHERE "
                    + " AND ".join(
                        conditions
                    )
                )

            base_query += """
                ORDER BY a.id DESC
            """

            self.cursor.execute(
                base_query,
                tuple(params)
            )

            rows = (
                self.cursor.fetchall()
            )

            display_rows = []

            for row in rows:

                # -------------------------------------------------
                # Direct appointment values
                # -------------------------------------------------

                father = (
                    row[3]
                    if len(row) > 3
                    else ""
                )

                disease = (
                    row[4]
                    if len(row) > 4
                    else ""
                )

                # -------------------------------------------------
                # Fallback to patient record only when empty
                # -------------------------------------------------

                if (
                    not str(
                        father or ""
                    ).strip()
                    or
                    not str(
                        disease or ""
                    ).strip()
                ):

                    patient_details = (
                        self.get_patient_details_without_ui(
                            row[2]
                        )
                    )

                    if patient_details:

                        if not str(
                            father or ""
                        ).strip():

                            father = (
                                patient_details.get(
                                    "father_husband_name",
                                    ""
                                )
                            )

                        if not str(
                            disease or ""
                        ).strip():

                            disease = (
                                patient_details.get(
                                    "disease",
                                    ""
                                )
                            )

                # -------------------------------------------------
                # UI row
                # -------------------------------------------------

                display_row = (
                    row[0],       # DB ID
                    row[1],       # Appointment ID
                    row[2],       # Patient
                    father,       # Father/Husband
                    disease,      # Disease
                    row[5],       # Doctor
                    row[6],       # Department
                    row[7],       # Date
                    row[8],       # Time
                    row[10],      # Token
                    row[11],      # Status
                    row[12]       # Remarks
                )

                display_rows.append(
                    display_row
                )

            if hasattr(
                self.ui,
                "load_data"
            ):

                self.ui.load_data(
                    display_rows
                )

            print(
                f"📅 Appointments Loaded: "
                f"{len(rows)}"
            )

            if self.is_doctor():

                print(
                    "🔒 Doctor appointment filtering active"
                )

            return display_rows

        except Exception as e:

            print(
                "Load Appointments Error:",
                e
            )

            self.show_error(
                f"Load Appointments Error:\n{e}"
            )

            return []

    # =====================================================
    # FIND APPOINTMENT FOR PATIENT
    # =====================================================

    def find_appointment_id_for_patient(
        self,
        patient_name
    ):

        try:

            patient_name = str(
                patient_name or ""
            ).strip()

            if not patient_name:

                return None

            sql = """
                SELECT id
                FROM appointments
                WHERE LOWER(TRIM(patient_name))
                    =
                    LOWER(TRIM(?))
            """

            params = [
                patient_name
            ]

            if self.is_doctor():

                names = (
                    self.get_logged_doctor_full_names()
                    or
                    self.get_logged_in_doctor_names()
                )

                if names:

                    sql += (
                        " AND ("
                        +
                        " OR ".join(
                            [
                                """
                                LOWER(TRIM(doctor_name))
                                =
                                LOWER(TRIM(?))
                                """
                                for _ in names
                            ]
                        )
                        +
                        ")"
                    )

                    params.extend(
                        names
                    )

                else:

                    sql += (
                        " AND 1=0"
                    )

            sql += """
                ORDER BY id DESC
                LIMIT 1
            """

            self.cursor.execute(
                sql,
                tuple(params)
            )

            row = (
                self.cursor.fetchone()
            )

            if row:

                self.selected_appointment_id = int(
                    row[0]
                )

                print(
                    "✅ Appointment Auto-Selected "
                    f"for Patient: {patient_name} "
                    f"-> {row[0]}"
                )

                return int(
                    row[0]
                )

            self.selected_appointment_id = None

            return None

        except Exception as e:

            print(
                "Find Appointment Error:",
                e
            )

            return None

    # =====================================================
    # SELECT APPOINTMENT
    # =====================================================

    def select_appointment(
        self,
        appointment_db_id
    ):

        try:

            appointment_db_id = int(
                appointment_db_id
            )

            # -------------------------------------------------
            # CLOUD API SELECT
            # -------------------------------------------------
            #
            # The appointments API currently provides the collection
            # endpoint only. Use the records already loaded into
            # self._cloud_appointments instead of calling
            # /records/{id}.
            # -------------------------------------------------

            if self.api_client:

                cloud_items = getattr(
                    self,
                    "_cloud_appointments",
                    []
                )

                if isinstance(cloud_items, list):

                    for appointment in cloud_items:

                        if not isinstance(appointment, dict):
                            continue

                        try:
                            cloud_id = int(
                                appointment.get("id")
                            )
                        except (TypeError, ValueError):
                            continue

                        if cloud_id != appointment_db_id:
                            continue

                        self.selected_appointment_id = (
                            appointment_db_id
                        )

                        # Convert the Cloud API dictionary into the same
                        # tuple structure expected by appointment_row_selected().
                        cloud_row = (
                            appointment.get("id", ""),
                            appointment.get("appointment_id", ""),
                            appointment.get("patient_name", ""),
                            appointment.get("father_husband_name", ""),
                            appointment.get("disease", ""),
                            appointment.get("doctor_name", ""),
                            appointment.get("department", ""),
                            appointment.get("appointment_date", ""),
                            appointment.get("appointment_time", ""),
                            appointment.get("visit_type", "OPD"),
                            appointment.get("token_no", ""),
                            appointment.get("status", "Pending") or "Pending",
                            appointment.get("remarks", "")
                        )

                        print(
                            "✅ Selected Cloud Appointment:",
                            appointment_db_id
                        )

                        return cloud_row

                print(
                    "Cloud appointment not found in cache:",
                    appointment_db_id
                )

            # -------------------------------------------------
            # LOCAL DATABASE FALLBACK
            # -------------------------------------------------

            self.cursor.execute(
                """
                SELECT
                    id,
                    appointment_id,
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    status,
                    remarks
                FROM appointments
                WHERE id=?
                LIMIT 1
                """,
                (
                    appointment_db_id,
                )
            )

            row = (
                self.cursor.fetchone()
            )

            if not row:

                self.selected_appointment_id = None

                print(
                    "⚠ Appointment not found:",
                    appointment_db_id
                )

                return None

            self.selected_appointment_id = (
                appointment_db_id
            )

            father = row[3] or ""
            disease = row[4] or ""

            # -------------------------------------------------
            # Fallback from patient table
            # -------------------------------------------------

            patient_details = (
                self.get_patient_details_without_ui(
                    row[2]
                )
            )

            if patient_details:

                if not str(
                    father
                ).strip():

                    father = (
                        patient_details.get(
                            "father_husband_name",
                            ""
                        )
                    )

                if not str(
                    disease
                ).strip():

                    disease = (
                        patient_details.get(
                            "disease",
                            ""
                        )
                    )

            normalized = (
                row[0],              # DB ID
                row[1],              # Appointment ID
                row[2],              # Patient
                father,              # Father/Husband
                disease,             # Disease
                row[5],              # Doctor
                row[6],              # Department
                row[7],              # Date
                row[8],              # Time
                row[9],              # Visit Type
                row[10],             # Token
                row[11],             # Status
                row[12]              # Remarks
            )

            print(
                "✅ Selected Appointment:",
                appointment_db_id
            )

            return normalized

        except Exception as e:

            print(
                "Select Appointment Error:",
                e
            )

            self.selected_appointment_id = None

            return None

    # =====================================================
    # UPDATE APPOINTMENT
    # =====================================================

    def update_appointment(self):

        try:

            appointment_db_id = (
                self.selected_appointment_id
            )

            if not appointment_db_id:

                self.show_error(
                    "Please select an appointment first."
                )

                return False

            # -------------------------------------------------
            # Make sure appointment still exists
            # -------------------------------------------------

            self.cursor.execute(
                """
                SELECT id
                FROM appointments
                WHERE id=?
                LIMIT 1
                """,
                (
                    appointment_db_id,
                )
            )

            exists = (
                self.cursor.fetchone()
            )

            if not exists:

                self.selected_appointment_id = None

                self.show_error(
                    "Selected appointment no longer exists."
                )

                return False

            data = (
                self.get_form_data()
            )

            patient_name = str(
                data.get(
                    "patient_name",
                    ""
                )
            ).strip()

            father_husband_name = str(
                data.get(
                    "father_husband_name",
                    ""
                )
            ).strip()

            disease = str(
                data.get(
                    "disease",
                    ""
                )
            ).strip()

            doctor_name = str(
                data.get(
                    "doctor_name",
                    ""
                )
            ).strip()

            department = str(
                data.get(
                    "department",
                    ""
                )
            ).strip()

            appointment_date = str(
                data.get(
                    "appointment_date",
                    ""
                )
            ).strip()

            appointment_time = str(
                data.get(
                    "appointment_time",
                    ""
                )
            ).strip()

            visit_type = str(
                data.get(
                    "visit_type",
                    "OPD"
                )
            ).strip()

            token_no = str(
                data.get(
                    "token_no",
                    ""
                )
            ).strip()

            status = str(
                data.get(
                    "status",
                    "Pending"
                )
            ).strip()

            remarks = str(
                data.get(
                    "remarks",
                    ""
                )
            ).strip()

            # -------------------------------------------------
            # Fallback patient data
            # -------------------------------------------------

            patient_details = (
                self.get_patient_details_without_ui(
                    patient_name
                )
            )

            if patient_details:

                if not father_husband_name:

                    father_husband_name = str(
                        patient_details.get(
                            "father_husband_name",
                            ""
                        )
                    ).strip()

                if not disease:

                    disease = str(
                        patient_details.get(
                            "disease",
                            ""
                        )
                    ).strip()

            # -------------------------------------------------
            # Validation
            # -------------------------------------------------

            if not patient_name:

                self.show_error(
                    "Patient is required."
                )

                return False

            if not doctor_name:

                self.show_error(
                    "Doctor is required."
                )

                return False

            # -------------------------------------------------
            # Doctor security
            # -------------------------------------------------

            if self.is_doctor():

                allowed_doctors = (
                    self.get_logged_doctor_full_names()
                    or
                    self.get_logged_in_doctor_names()
                )

                valid = any(
                    str(name).strip().lower()
                    ==
                    doctor_name.strip().lower()
                    for name in allowed_doctors
                )

                if not valid:

                    self.show_error(
                        "You can only update your own appointment."
                    )

                    return False

            # -------------------------------------------------
            # Duplicate token
            # -------------------------------------------------

            if self.check_duplicate_token(
                token_no,
                appointment_db_id
            ):

                self.show_error(
                    f"Token {token_no} already exists."
                )

                return False

            # -------------------------------------------------
            # CLOUD UPDATE
            # -------------------------------------------------

            if self.api_client:

                payload = {
                    "appointment_id": data.get("appointment_id", ""),
                    "patient_name": patient_name,
                    "father_husband_name": father_husband_name,
                    "disease": disease,
                    "doctor_name": doctor_name,
                    "department": department,
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time,
                    "visit_type": visit_type,
                    "token_no": token_no,
                    "status": status,
                    "remarks": remarks
                }

                try:

                    print(
                        "Updating Appointment through Central API...",
                        appointment_db_id
                    )

                    response = self.api_client.request(
                        "PUT",
                        f"/api/v1/modules/appointments/records/{appointment_db_id}",
                        json={"data": payload}
                    )

                    print(
                        "✅ Cloud Appointment Updated:",
                        response
                    )

                    self.selected_appointment_id = (
                        appointment_db_id
                    )

                    self.show_success(
                        "Appointment updated successfully."
                    )

                    self.load_appointments()

                    return True

                except Exception as e:

                    print(
                        "Cloud Update Appointment Error:",
                        e
                    )

                    self.show_error(
                        f"Cloud Update Appointment Error:\n{e}"
                    )

                    return False

            # -------------------------------------------------
            # UPDATE
            # -------------------------------------------------

            self.cursor.execute(
                """
                UPDATE appointments
                SET
                    patient_name=?,
                    father_husband_name=?,
                    disease=?,
                    doctor_name=?,
                    department=?,
                    appointment_date=?,
                    appointment_time=?,
                    visit_type=?,
                    token_no=?,
                    status=?,
                    remarks=?
                WHERE id=?
                """,
                (
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    status,
                    remarks,
                    appointment_db_id
                )
            )

            updated_rows = (
                self.cursor.rowcount
            )

            self.commit()

            # -------------------------------------------------
            # Verify update
            # -------------------------------------------------

            self.cursor.execute(
                """
                SELECT
                    id,
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name
                FROM appointments
                WHERE id=?
                LIMIT 1
                """,
                (
                    appointment_db_id,
                )
            )

            updated_record = (
                self.cursor.fetchone()
            )

            if not updated_record:

                self.show_error(
                    "Appointment could not be verified."
                )

                return False

            print(
                "✅ Appointment Updated:",
                appointment_db_id,
                "| SQL rows:",
                updated_rows
            )

            self.show_success(
                "Appointment updated successfully."
            )

            # Keep selected record.
            self.selected_appointment_id = (
                appointment_db_id
            )

            self.load_appointments()

            return True

        except Exception as e:

            print(
                "Update Appointment Error:",
                e
            )

            self.show_error(
                f"Update Appointment Error:\n{e}"
            )

            return False

    # =====================================================
    # DELETE APPOINTMENT
    # =====================================================

    def delete_appointment(self):

        try:

            appointment_db_id = (
                self.selected_appointment_id
            )

            if not appointment_db_id:

                self.show_error(
                    "Please select an appointment first."
                )

                return False

            confirm = messagebox.askyesno(
                "Delete Appointment",
                "Are you sure you want to delete this appointment?"
            )

            if not confirm:

                return False

            # -------------------------------------------------
            # CLOUD DELETE
            # -------------------------------------------------

            if self.api_client:

                # -------------------------------------------------
                # Doctor security for Cloud Delete
                # -------------------------------------------------

                if self.is_doctor():

                    doctor_names = (
                        self.get_logged_doctor_full_names()
                        or
                        self.get_logged_in_doctor_names()
                    )

                    if not doctor_names:

                        self.show_error(
                            "Doctor identity not found."
                        )

                        return False

                    cloud_appointment = None

                    for item in getattr(
                        self,
                        "_cloud_appointments",
                        []
                    ):

                        if not isinstance(item, dict):
                            continue

                        try:
                            cloud_id = int(
                                item.get("id")
                            )
                        except (TypeError, ValueError):
                            continue

                        if cloud_id == int(
                            appointment_db_id
                        ):

                            cloud_appointment = item
                            break

                    if not cloud_appointment:

                        self.show_error(
                            "Selected appointment was not found in Cloud data."
                        )

                        return False

                    cloud_doctor = str(
                        cloud_appointment.get(
                            "doctor_name",
                            ""
                        )
                    ).strip().lower()

                    allowed = any(
                        cloud_doctor
                        ==
                        str(name).strip().lower()
                        for name in doctor_names
                    )

                    if not allowed:

                        self.show_error(
                            "You can only delete your own appointment."
                        )

                        return False

                try:

                    print(
                        "Deleting Appointment through Central API...",
                        appointment_db_id
                    )

                    response = self.api_client.request(
                        "DELETE",
                        f"/api/v1/modules/appointments/records/{appointment_db_id}"
                    )

                    print(
                        "✅ Cloud Appointment Deleted:",
                        response
                    )

                    self.selected_appointment_id = None

                    self.show_success(
                        "Appointment deleted successfully."
                    )

                    self.load_appointments()

                    return True

                except Exception as e:

                    print(
                        "Cloud Delete Appointment Error:",
                        e
                    )

                    self.show_error(
                        f"Cloud Delete Appointment Error:\n{e}"
                    )

                    return False

            # -------------------------------------------------
            # Doctor security
            # -------------------------------------------------

            if self.is_doctor():

                doctor_names = (
                    self.get_logged_doctor_full_names()
                    or
                    self.get_logged_in_doctor_names()
                )

                if not doctor_names:

                    self.show_error(
                        "Doctor identity not found."
                    )

                    return False

                conditions = []

                params = [
                    appointment_db_id
                ]

                for doctor_name in doctor_names:

                    conditions.append(
                        """
                        LOWER(TRIM(doctor_name))
                        =
                        LOWER(TRIM(?))
                        """
                    )

                    params.append(
                        doctor_name
                    )

                query = (
                    """
                    DELETE FROM appointments
                    WHERE id=?
                    AND (
                    """
                    +
                    " OR ".join(
                        conditions
                    )
                    +
                    ")"
                )

                self.cursor.execute(
                    query,
                    tuple(params)
                )

            else:

                self.cursor.execute(
                    """
                    DELETE FROM appointments
                    WHERE id=?
                    """,
                    (
                        appointment_db_id,
                    )
                )

            deleted_rows = (
                self.cursor.rowcount
            )

            self.commit()

            if deleted_rows == 0:

                self.show_error(
                    "Appointment was not deleted."
                )

                return False

            self.selected_appointment_id = None

            self.show_success(
                "Appointment deleted successfully."
            )

            self.load_appointments()

            self.load_patients()

            return True

        except Exception as e:

            print(
                "Delete Appointment Error:",
                e
            )

            self.show_error(
                f"Delete Appointment Error:\n{e}"
            )

            return False

    # =====================================================
    # SEARCH
    # =====================================================

    def search_appointment(
        self,
        keyword=None
    ):

        try:

            if keyword is None:

                if hasattr(
                    self.ui,
                    "search_var"
                ):

                    keyword = (
                        self.ui.search_var.get()
                    )

                else:

                    keyword = ""

            keyword = str(
                keyword or ""
            ).strip()

            print(
                "🔍 Appointment Search:",
                keyword
            )

            return self.load_appointments(
                keyword
            )

        except Exception as e:

            print(
                "Search Appointment Error:",
                e
            )

            return []

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh_appointments(self):

        try:

            if hasattr(
                self.ui,
                "search_var"
            ):

                self.ui.search_var.set(
                    ""
                )

            self.selected_appointment_id = None

            self.load_doctors()
            self.load_patients()
            self.load_appointments()

            print(
                "🔄 Appointment List Refreshed"
            )

        except Exception as e:

            print(
                "Refresh Appointment Error:",
                e
            )

    # =====================================================
    # GET SELECTED APPOINTMENT ID
    # =====================================================

    def get_selected_appointment_id(
        self
    ):

        return (
            self.selected_appointment_id
        )

    # =====================================================
    # GET APPOINTMENT BY ID
    # =====================================================

    def get_appointment_by_id(
        self,
        appointment_db_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    appointment_id,
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    status,
                    remarks,
                    created_at
                FROM appointments
                WHERE id=?
                LIMIT 1
                """,
                (
                    appointment_db_id,
                )
            )

            return (
                self.cursor.fetchone()
            )

        except Exception as e:

            print(
                "Get Appointment Error:",
                e
            )

            return None

    # =====================================================
    # ALL APPOINTMENTS
    # =====================================================

    def get_all_appointments(self):

        return (
            self.load_appointments()
        )

    # =====================================================
    # SHOW ERROR
    # =====================================================

    def show_error(
        self,
        message
    ):

        try:

            messagebox.showerror(
                "Hospital ERP",
                message
            )

        except Exception:

            print(
                "ERROR:",
                message
            )

    # =====================================================
    # SHOW SUCCESS
    # =====================================================

    def show_success(
        self,
        message
    ):

        try:

            messagebox.showinfo(
                "Hospital ERP",
                message
            )

        except Exception:

            print(
                "SUCCESS:",
                message
            )

    # =====================================================
    # DESTROY
    # =====================================================

    def destroy(self):

        try:

            if hasattr(
                self.ui,
                "main_frame"
            ):

                self.ui.main_frame.destroy()

        except Exception as e:

            print(
                "Appointment Destroy Error:",
                e
            )
