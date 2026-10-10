"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : IPD CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class IPDCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_ipd_table()

    # ==========================================
    # Create IPD Table
    # ==========================================

    def create_ipd_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ipd(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            admission_id TEXT UNIQUE,

            patient TEXT NOT NULL,

            doctor TEXT NOT NULL,

            ward TEXT,

            bed_no TEXT,

            admission_date TEXT,

            discharge_date TEXT,

            diagnosis TEXT,

            treatment TEXT,

            daily_charges REAL,

            status TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate Admission ID
    # ==========================================

    def generate_admission_id(self):

        self.cursor.execute(
            "SELECT MAX(id) FROM ipd"
        )

        result = self.cursor.fetchone()[0]

        if result is None:
            result = 0

        return f"IPD{result + 1:06d}"

    # ==========================================
    # Add Admission
    # ==========================================

    def add_admission(
        self,
        admission_id,
        patient,
        doctor,
        ward,
        bed_no,
        admission_date,
        discharge_date,
        diagnosis,
        treatment,
        daily_charges,
        status,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO ipd
                (
                    admission_id,
                    patient,
                    doctor,
                    ward,
                    bed_no,
                    admission_date,
                    discharge_date,
                    diagnosis,
                    treatment,
                    daily_charges,
                    status,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                admission_id,
                patient,
                doctor,
                ward,
                bed_no,
                admission_date,
                discharge_date,
                diagnosis,
                treatment,
                daily_charges,
                status,
                remarks
            ))

            self.commit()

            return True

        except Exception as e:

            import traceback
            traceback.print_exc()

            print("Add Admission Error:", e)

            return False


    # ==========================================
    # Load Admissions
    # ==========================================

    def load_admissions(self):

        self.cursor.execute("""
            SELECT
                id,
                admission_id,
                patient,
                doctor,
                ward,
                bed_no,
                admission_date,
                status
            FROM ipd
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()


    # ==========================================
    # Search Admission
    # ==========================================

    def search_admission(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                admission_id,
                patient,
                doctor,
                ward,
                bed_no,
                admission_date,
                status
            FROM ipd
            WHERE
                admission_id LIKE :keyword
                OR patient LIKE :keyword
                OR doctor LIKE :keyword
                OR ward LIKE :keyword
                OR bed_no LIKE :keyword
                OR admission_date LIKE :keyword
                OR discharge_date LIKE :keyword
                OR diagnosis LIKE :keyword
                OR treatment LIKE :keyword
                OR CAST(daily_charges AS TEXT) LIKE :keyword
                OR status LIKE :keyword
                OR remarks LIKE :keyword
                OR EXISTS (
                    SELECT 1
                    FROM patients AS patient_record
                    WHERE patient_record.mobile LIKE :keyword
                      AND (
                          patient_record.patient_name = ipd.patient
                          OR patient_record.name = ipd.patient
                      )
                )
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Admission By ID
    # ==========================================

    def get_admission_by_id(self, admission_db_id):

        self.cursor.execute("""
            SELECT *
            FROM ipd
            WHERE id=?
        """, (admission_db_id,))

        return self.cursor.fetchone()


    # ==========================================
    # Update Admission
    # ==========================================

    def update_admission(
        self,
        admission_db_id,
        patient,
        doctor,
        ward,
        bed_no,
        admission_date,
        discharge_date,
        diagnosis,
        treatment,
        daily_charges,
        status,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE ipd
                SET
                    patient=?,
                    doctor=?,
                    ward=?,
                    bed_no=?,
                    admission_date=?,
                    discharge_date=?,
                    diagnosis=?,
                    treatment=?,
                    daily_charges=?,
                    status=?,
                    remarks=?
                WHERE id=?
            """, (
                patient,
                doctor,
                ward,
                bed_no,
                admission_date,
                discharge_date,
                diagnosis,
                treatment,
                daily_charges,
                status,
                remarks,
                admission_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Admission Error:", e)

            return False


    # ==========================================
    # Delete Admission
    # ==========================================

    def delete_admission(self, admission_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM ipd WHERE id=?",
                (admission_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Admission Error:", e)

            return False

    def get_patient_names(self):
        self.cursor.execute(
            "SELECT patient_name FROM patients ORDER BY patient_name"
        )

        return [row[0] for row in self.cursor.fetchall()]

    def get_doctor_names(self):
        self.cursor.execute(
            "SELECT full_name FROM doctors ORDER BY full_name"
        )

        return [row[0] for row in self.cursor.fetchall()]
