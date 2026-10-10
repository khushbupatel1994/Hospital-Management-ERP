"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class LaboratoryCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_laboratory_table()

    # ==========================================
    # Create Laboratory Table
    # ==========================================

    def create_laboratory_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS laboratory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            test_id TEXT UNIQUE,

            test_name TEXT NOT NULL,

            department TEXT,

            sample_type TEXT,

            test_fee REAL,

            normal_range TEXT,

            patient TEXT,

            doctor TEXT,

            test_date TEXT,

            test_result TEXT,

            status TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate Test ID
    # ==========================================

    def generate_test_id(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM laboratory"
        )

        count = self.cursor.fetchone()[0] + 1

        return f"LAB{count:06d}"

    # ==========================================
    # Add Test
    # ==========================================

    def add_test(
        self,
        test_id,
        test_name,
        department,
        sample_type,
        test_fee,
        normal_range,
        patient,
        doctor,
        test_date,
        test_result,
        status,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO laboratory
                (
                    test_id,
                    test_name,
                    department,
                    sample_type,
                    test_fee,
                    normal_range,
                    patient,
                    doctor,
                    test_date,
                    test_result,
                    status,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                test_id,
                test_name,
                department,
                sample_type,
                test_fee,
                normal_range,
                patient,
                doctor,
                test_date,
                test_result,
                status,
                remarks
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Test Error:", e)

            return False


    # ==========================================
    # Load Tests
    # ==========================================

    def load_tests(self):

        self.cursor.execute("""
            SELECT
                id,
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
    # Get Doctor Names
    # ==========================================

    def get_doctor_names(self):

        self.cursor.execute("""
            SELECT full_name
            FROM doctors
            ORDER BY full_name
        """)

        return [row[0] for row in self.cursor.fetchall()]

    # ==========================================
    # Search Test
    # ==========================================

    def search_test(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                test_id,
                test_name,
                patient,
                doctor,
                department,
                test_fee,
                status
            FROM laboratory
            WHERE
                test_id LIKE :keyword
                OR test_name LIKE :keyword
                OR patient LIKE :keyword
                OR doctor LIKE :keyword
                OR department LIKE :keyword
                OR sample_type LIKE :keyword
                OR normal_range LIKE :keyword
                OR test_date LIKE :keyword
                OR test_result LIKE :keyword
                OR status LIKE :keyword
                OR remarks LIKE :keyword
                OR EXISTS (
                    SELECT 1
                    FROM patients AS patient_record
                    WHERE patient_record.mobile LIKE :keyword
                      AND (
                          patient_record.patient_name = laboratory.patient
                          OR patient_record.name = laboratory.patient
                      )
                )
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Test By ID
    # ==========================================

    def get_test_by_id(self, test_db_id):

        self.cursor.execute("""
            SELECT *
            FROM laboratory
            WHERE id=?
        """, (test_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update Test
    # ==========================================

    def update_test(
        self,
        test_db_id,
        test_name,
        department,
        sample_type,
        test_fee,
        normal_range,
        patient,
        doctor,
        test_date,
        test_result,
        status,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE laboratory
                SET
                    test_name=?,
                    department=?,
                    sample_type=?,
                    test_fee=?,
                    normal_range=?,
                    patient=?,
                    doctor=?,
                    test_date=?,
                    test_result=?,
                    status=?,
                    remarks=?
                WHERE id=?
            """, (
                test_name,
                department,
                sample_type,
                test_fee,
                normal_range,
                patient,
                doctor,
                test_date,
                test_result,
                status,
                remarks,
                test_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Test Error:", e)

            return False


    # ==========================================
    # Delete Test
    # ==========================================

    def delete_test(self, test_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM laboratory WHERE id=?",
                (test_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Test Error:", e)

            return False

    def get_patient_names(self):

        self.cursor.execute("""
            SELECT patient_name
            FROM patients
           ORDER BY patient_name
       """)

        return [row[0] for row in self.cursor.fetchall()]

    def get_doctor_department(self, doctor_name):

        self.cursor.execute("""
            SELECT department
            FROM doctors
            WHERE  full_name=?
        """, (doctor_name,))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return ""

    # ==========================================
    # Get Patient Details
    # ==========================================

    def get_patient_details(self, patient_name):

        self.cursor.execute("""
            SELECT mobile, age, gender
            FROM patients
            WHERE patient_name=?
        """, (patient_name,))

        return self.cursor.fetchone()
