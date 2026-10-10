"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Appointment CRUD
Version : 4.0
===========================================================
"""

from database.database import Database


class AppointmentCRUD(Database):

    def __init__(self):
        super().__init__()
        self.connect()
        self.create_appointment_table()

    # ======================================================
    # CREATE TABLE
    # ======================================================

    def create_appointment_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id TEXT UNIQUE,
                patient_id INTEGER,
                doctor_id INTEGER,
                patient_name TEXT,
                doctor_name TEXT,
                department TEXT,
                appointment_date TEXT,
                appointment_time TEXT,
                visit_type TEXT,
                token_no TEXT,
                token_number INTEGER,
                purpose TEXT,
                status TEXT DEFAULT 'Pending',
                remarks TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.commit()

    # ======================================================
    # GENERATE APPOINTMENT ID
    # ======================================================

    def generate_appointment_id(self):

        self.cursor.execute("""
            SELECT COALESCE(MAX(id), 0) + 1
            FROM appointments
        """)

        number = self.cursor.fetchone()[0]

        return f"APT{number:06d}"

    # ======================================================
    # GENERATE TOKEN
    # ======================================================

    def generate_token_no(self):

        self.cursor.execute("""
            SELECT COALESCE(MAX(id), 0) + 1
            FROM appointments
        """)

        number = self.cursor.fetchone()[0]

        return str(number)

    # ======================================================
    # LOAD DOCTORS
    # ======================================================

    def load_doctors(self):

        try:

            self.cursor.execute("""
                SELECT full_name
                FROM doctors
                WHERE COALESCE(status, 'Active') != 'Inactive'
                ORDER BY full_name
            """)

            return self.cursor.fetchall()

        except Exception as e:

            print("Load Doctors Error:", e)

            return []

    # ======================================================
    # GET DOCTOR DEPARTMENT
    # ======================================================

    def get_doctor_department(self, doctor_name):

        try:

            self.cursor.execute("""
                SELECT department
                FROM doctors
                WHERE
                    LOWER(TRIM(full_name))
                    =
                    LOWER(TRIM(?))

                    OR

                    LOWER(TRIM(name))
                    =
                    LOWER(TRIM(?))

                LIMIT 1
            """, (
                doctor_name,
                doctor_name
            ))

            row = self.cursor.fetchone()

            if row:
                return row[0]

            return None

        except Exception as e:

            print(
                "Doctor Department Error:",
                e
            )

            return None

    # ======================================================
    # GET DOCTOR ID
    # ======================================================

    def get_doctor_id(self, doctor_name):

        self.cursor.execute("""
            SELECT id
            FROM doctors
            WHERE
                LOWER(TRIM(full_name))
                =
                LOWER(TRIM(?))

                OR

                LOWER(TRIM(name))
                =
                LOWER(TRIM(?))

            LIMIT 1
        """, (
            doctor_name,
            doctor_name
        ))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

    # ======================================================
    # LOAD ALL PATIENTS
    # ======================================================

    def load_patients(self):

        try:

            self.cursor.execute("""
                SELECT DISTINCT patient_name
                FROM patients
                WHERE
                    COALESCE(patient_name, '') != ''

                ORDER BY patient_name
            """)

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Load Patients Error:",
                e
            )

            return []

    # ======================================================
    # LOAD DOCTOR ASSIGNED PATIENTS
    # ======================================================

    def load_assigned_patients(
        self,
        doctor_name
    ):

        try:

            doctor_id = self.get_doctor_id(
                doctor_name
            )

            if doctor_id:

                self.cursor.execute("""
                    SELECT DISTINCT patient_name
                    FROM patients
                    WHERE
                        (
                            LOWER(TRIM(doctor))
                            =
                            LOWER(TRIM(?))
                        )

                        OR

                        assigned_doctor = ?

                    AND

                        COALESCE(patient_name, '') != ''

                    ORDER BY patient_name
                """, (
                    doctor_name,
                    doctor_id
                ))

            else:

                self.cursor.execute("""
                    SELECT DISTINCT patient_name
                    FROM patients
                    WHERE
                        LOWER(TRIM(doctor))
                        =
                        LOWER(TRIM(?))

                        AND

                        COALESCE(patient_name, '') != ''

                    ORDER BY patient_name
                """, (
                    doctor_name,
                ))

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Assigned Patient Error:",
                e
            )

            return []

    # ======================================================
    # PATIENT DETAILS
    # ======================================================

    def get_patient_details(
        self,
        patient_name
    ):

        try:

            self.cursor.execute("""
                SELECT
                    patient_name,
                    father_husband_name,
                    disease,
                    doctor,
                    department,
                    mobile,
                    age,
                    gender
                FROM patients

                WHERE
                    LOWER(TRIM(patient_name))
                    =
                    LOWER(TRIM(?))

                LIMIT 1
            """, (
                patient_name,
            ))

            return self.cursor.fetchone()

        except Exception as e:

            print(
                "Patient Details Error:",
                e
            )

            return None

    # ======================================================
    # CHECK DUPLICATE TOKEN
    # ======================================================

    def check_duplicate_token(
        self,
        token_no,
        appointment_id=None
    ):

        try:

            if appointment_id:

                self.cursor.execute("""
                    SELECT id
                    FROM appointments
                    WHERE
                        token_no = ?

                        AND

                        id != ?
                """, (
                    token_no,
                    appointment_id
                ))

            else:

                self.cursor.execute("""
                    SELECT id
                    FROM appointments
                    WHERE
                        token_no = ?
                """, (
                    token_no,
                ))

            return self.cursor.fetchone()

        except Exception as e:

            print(
                "Token Check Error:",
                e
            )

            return None

    # ======================================================
    # ADD APPOINTMENT
    # ======================================================

    def add_appointment(
        self,
        appointment_id,
        patient_name,
        doctor_name,
        department,
        appointment_date,
        appointment_time,
        visit_type,
        token_no,
        status,
        remarks
    ):

        try:

            patient_id = None
            doctor_id = None

            # ----------------------------------------------
            # PATIENT ID
            # ----------------------------------------------

            self.cursor.execute("""
                SELECT id
                FROM patients
                WHERE
                    LOWER(TRIM(patient_name))
                    =
                    LOWER(TRIM(?))

                LIMIT 1
            """, (
                patient_name,
            ))

            row = self.cursor.fetchone()

            if row:
                patient_id = row[0]

            # ----------------------------------------------
            # DOCTOR ID
            # ----------------------------------------------

            doctor_id = self.get_doctor_id(
                doctor_name
            )

            # ----------------------------------------------
            # INSERT
            # ----------------------------------------------

            self.cursor.execute("""
                INSERT INTO appointments(

                    appointment_id,
                    patient_id,
                    doctor_id,
                    patient_name,
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    token_no,
                    token_number,
                    purpose,
                    status,
                    remarks

                )

                VALUES(
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?
                )

            """, (

                appointment_id,
                patient_id,
                doctor_id,
                patient_name,
                doctor_name,
                department,
                appointment_date,
                appointment_time,
                visit_type,
                token_no,

                int(token_no)
                if str(token_no).isdigit()
                else None,

                "",
                status,
                remarks

            ))

            self.commit()

            return True

        except Exception as e:

            print(
                "Add Appointment Error:",
                e
            )

            return False

    # ======================================================
    # LOAD ALL APPOINTMENTS
    # ======================================================

    def load_appointments(self):

        try:

            self.cursor.execute("""
                SELECT

                    id,
                    appointment_id,
                    patient_name,
                    '',
                    '',
                    doctor_name,
                    department,
                    appointment_date,
                    appointment_time,
                    token_no,
                    status,
                    remarks

                FROM appointments

                ORDER BY id DESC
            """)

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Load Appointment Error:",
                e
            )

            return []

    # ======================================================
    # LOAD DOCTOR APPOINTMENTS
    # ======================================================

    def load_doctor_appointments(
        self,
        doctor_name
    ):

        try:

            self.cursor.execute("""
                SELECT

                    a.id,
                    a.appointment_id,
                    a.patient_name,

                    COALESCE(
                        p.father_husband_name,
                        ''
                    ),

                    COALESCE(
                        p.disease,
                        ''
                    ),

                    a.doctor_name,
                    a.department,
                    a.appointment_date,
                    a.appointment_time,
                    a.token_no,
                    a.status,
                    a.remarks

                FROM appointments a

                LEFT JOIN patients p

                    ON LOWER(
                        TRIM(p.patient_name)
                    )

                    =

                    LOWER(
                        TRIM(a.patient_name)
                    )

                WHERE

                    LOWER(
                        TRIM(a.doctor_name)
                    )

                    =

                    LOWER(
                        TRIM(?)
                    )

                ORDER BY a.id DESC

            """, (
                doctor_name,
            ))

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Doctor Appointment Error:",
                e
            )

            return []

    # ======================================================
    # SEARCH
    # ======================================================

    def search_appointment(
        self,
        keyword,
        doctor_name=None
    ):

        try:

            search = f"%{keyword}%"

            if doctor_name:

                self.cursor.execute("""
                    SELECT

                        a.id,
                        a.appointment_id,
                        a.patient_name,

                        COALESCE(
                            p.father_husband_name,
                            ''
                        ),

                        COALESCE(
                            p.disease,
                            ''
                        ),

                        a.doctor_name,
                        a.department,
                        a.appointment_date,
                        a.appointment_time,
                        a.token_no,
                        a.status,
                        a.remarks

                    FROM appointments a

                    LEFT JOIN patients p

                        ON LOWER(
                            TRIM(p.patient_name)
                        )

                        =

                        LOWER(
                            TRIM(a.patient_name)
                        )

                    WHERE

                        LOWER(
                            TRIM(a.doctor_name)
                        )

                        =

                        LOWER(
                            TRIM(?)
                        )

                    AND

                        (
                            a.patient_name LIKE ?
                            OR p.disease LIKE ?
                            OR a.appointment_id LIKE ?
                            OR a.token_no LIKE ?
                        )

                    ORDER BY a.id DESC

                """, (
                    doctor_name,
                    search,
                    search,
                    search,
                    search
                ))

            else:

                self.cursor.execute("""
                    SELECT

                        a.id,
                        a.appointment_id,
                        a.patient_name,
                        '',
                        '',
                        a.doctor_name,
                        a.department,
                        a.appointment_date,
                        a.appointment_time,
                        a.token_no,
                        a.status,
                        a.remarks

                    FROM appointments a

                    WHERE

                        a.patient_name LIKE ?
                        OR a.doctor_name LIKE ?
                        OR a.appointment_id LIKE ?
                        OR a.token_no LIKE ?

                    ORDER BY a.id DESC

                """, (
                    search,
                    search,
                    search,
                    search
                ))

            return self.cursor.fetchall()

        except Exception as e:

            print(
                "Search Appointment Error:",
                e
            )

            return []

    # ======================================================
    # UPDATE
    # ======================================================

    def update_appointment(
        self,
        appointment_db_id,
        patient_name,
        doctor_name,
        department,
        appointment_date,
        appointment_time,
        visit_type,
        token_no,
        status,
        remarks
    ):

        try:

            doctor_id = self.get_doctor_id(
                doctor_name
            )

            self.cursor.execute("""
                UPDATE appointments

                SET

                    patient_name = ?,
                    doctor_name = ?,
                    doctor_id = ?,
                    department = ?,
                    appointment_date = ?,
                    appointment_time = ?,
                    visit_type = ?,
                    token_no = ?,
                    token_number = ?,
                    status = ?,
                    remarks = ?

                WHERE id = ?

            """, (

                patient_name,
                doctor_name,
                doctor_id,
                department,
                appointment_date,
                appointment_time,
                visit_type,
                token_no,

                int(token_no)
                if str(token_no).isdigit()
                else None,

                status,
                remarks,
                appointment_db_id

            ))

            self.commit()

            return True

        except Exception as e:

            print(
                "Update Appointment Error:",
                e
            )

            return False

    # ======================================================
    # DELETE
    # ======================================================

    def delete_appointment(
        self,
        appointment_db_id
    ):

        try:

            self.cursor.execute("""
                DELETE FROM appointments
                WHERE id = ?
            """, (
                appointment_db_id,
            ))

            self.commit()

            return True

        except Exception as e:

            print(
                "Delete Appointment Error:",
                e
            )

            return False