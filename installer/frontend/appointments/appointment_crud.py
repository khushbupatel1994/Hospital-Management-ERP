"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Appointment CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class AppointmentCRUD(Database):

    def __init__(self):
        super().__init__()
        self.connect()
        self.create_appointment_table()

        # ==========================================
        # Create Appointment Table
        # ==========================================

    def create_appointment_table(self):

        self.cursor.execute("""
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

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Search Appointment
    # ==========================================
    def search_appointment(self, keyword):

        self.cursor.execute("""
        SELECT
            id,
            appointment_id,
            patient_name,
            doctor_name,
            department,
            appointment_date,
            appointment_time,
            token_no,
            status
        FROM appointments
        WHERE
            appointment_id LIKE :keyword
            OR CAST(patient_id AS TEXT) LIKE :keyword
            OR CAST(doctor_id AS TEXT) LIKE :keyword
            OR patient_name LIKE :keyword
            OR doctor_name LIKE :keyword
            OR department LIKE :keyword
            OR appointment_date LIKE :keyword
            OR appointment_time LIKE :keyword
            OR visit_type LIKE :keyword
            OR token_no LIKE :keyword
            OR CAST(token_number AS TEXT) LIKE :keyword
            OR purpose LIKE :keyword
            OR status LIKE :keyword
            OR remarks LIKE :keyword
            OR EXISTS (
                SELECT 1
                FROM patients AS patient_record
                WHERE patient_record.mobile LIKE :keyword
                  AND (
                      patient_record.patient_name = appointments.patient_name
                      OR patient_record.name = appointments.patient_name
                  )
            )
        ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Generate Appointment ID
    # ==========================================

    def generate_appointment_id(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        count = self.cursor.fetchone()[0] + 1

        return f"APT{count:06d}"

    # ==========================================
    # Generate Token Number
    # ==========================================

    def generate_token_no(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        count = self.cursor.fetchone()[0] + 1

        return str(count)

    # ==========================================
    # Check Duplicate Token
    # ==========================================

    def check_duplicate_token(
        self,
        token_no,
        appointment_db_id=None
    ):
        if appointment_db_id:

            self.cursor.execute(
                """
                SELECT id
                FROM appointments
                WHERE token_no=? AND id<>?
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
                (token_no,)
            )

        return self.cursor.fetchone()

    # ==========================================
    # Add Appointment
    # ==========================================

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

            self.cursor.execute("""
                INSERT INTO appointments
                (
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
                )
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
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
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Appointment Error:", e)

            return False

    # ==========================================
    # Load Appointments
    # ==========================================

    def load_appointments(self):

        self.cursor.execute("""
        SELECT
            id,
            appointment_id,
            patient_name,
            doctor_name,
            department,
            appointment_date,
            appointment_time,
            token_no,
            status
        FROM appointments
        ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Get Appointment By ID
    # ==========================================

    def get_appointment_by_id(self, appointment_db_id):

        self.cursor.execute("""
            SELECT *
            FROM appointments
            WHERE id=?
        """, (appointment_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update Appointment
    # ==========================================

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

            self.cursor.execute("""
                UPDATE appointments
                SET
                    patient_name=?,
                    doctor_name=?,
                    department=?,
                    appointment_date=?,
                    appointment_time=?,
                    visit_type=?,
                    token_no=?,
                    status=?,
                    remarks=?
                WHERE id=?
            """, (
                patient_name,
                doctor_name,
                department,
                appointment_date,
                appointment_time,
                visit_type,
                token_no,
                status,
                remarks,
                appointment_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Appointment Error:", e)

            return False

    # ==========================================
    # Delete Appointment
    # ==========================================

    def delete_appointment(self, appointment_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM appointments WHERE id=?",
                (appointment_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Appointment Error:", e)

            return False

    # ==========================================
    # Get Doctor Department
    # ==========================================

    def get_doctor_department(self, doctor_name):

        self.cursor.execute("""
            SELECT department
            FROM doctors
            WHERE full_name=?
        """, (doctor_name,))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

        # ==========================================
        # Load Doctors
        # ==========================================

    def load_doctors(self):

        self.cursor.execute("""
        SELECT full_name
        FROM doctors
        ORDER BY full_name
        """)

        return self.cursor.fetchall()


    # ==========================================
    # Load Patients
    # ==========================================

    def load_patients(self):

        self.cursor.execute("""
        SELECT patient_name
        FROM patients
        ORDER BY patient_name
        """)

        return self.cursor.fetchall()
