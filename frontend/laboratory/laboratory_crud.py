"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Laboratory CRUD
Version : 3.0
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
    # Generate Unique Test ID
    # ==========================================

    def generate_test_id(self):

        try:

            self.cursor.execute("""
                SELECT test_id
                FROM laboratory
                WHERE test_id LIKE 'LAB%'
            """)

            rows = self.cursor.fetchall()

            max_number = 0

            for row in rows:

                test_id = row[0]

                if not test_id:
                    continue

                try:

                    number = int(
                        str(test_id).replace("LAB", "")
                    )

                    if number > max_number:
                        max_number = number

                except (ValueError, TypeError):

                    continue

            # Next ID
            next_number = max_number + 1

            test_id = f"LAB{next_number:06d}"

            # ==========================================
            # Extra Safety Check
            # ==========================================

            while True:

                self.cursor.execute("""
                    SELECT 1
                    FROM laboratory
                    WHERE test_id = ?
                    LIMIT 1
                """, (test_id,))

                exists = self.cursor.fetchone()

                if not exists:
                    break

                next_number += 1

                test_id = f"LAB{next_number:06d}"

            return test_id

        except Exception as e:

            print(
                "Generate Test ID Error:",
                e
            )

            # ==========================================
            # Fallback ID
            # ==========================================

            import time

            timestamp_id = (
                int(time.time()) % 1000000
            )

            test_id = f"LAB{timestamp_id:06d}"

            # Final safety check
            while True:

                self.cursor.execute("""
                    SELECT 1
                    FROM laboratory
                    WHERE test_id = ?
                    LIMIT 1
                """, (test_id,))

                if not self.cursor.fetchone():
                    break

                timestamp_id += 1

                test_id = f"LAB{timestamp_id:06d}"

            return test_id

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

            # ==========================================
            # Check Test ID
            # ==========================================

            self.cursor.execute("""
                SELECT 1
                FROM laboratory
                WHERE test_id = ?
                LIMIT 1
            """, (test_id,))

            existing = self.cursor.fetchone()

            # If ID already exists, generate new ID
            if existing:

                print(
                    "Duplicate Test ID detected:",
                    test_id
                )

                test_id = self.generate_test_id()

                print(
                    "New Test ID generated:",
                    test_id
                )

            # ==========================================
            # Insert Laboratory Test
            # ==========================================

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

            print(
                "Add Test Error:",
                e
            )

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

        return [
            row[0]
            for row in self.cursor.fetchall()
        ]

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
                        patient_record.patient_name =
                        laboratory.patient

                        OR patient_record.name =
                        laboratory.patient
                    )
                )

            ORDER BY id DESC

        """, {
            "keyword": f"%{keyword}%"
        })

        return self.cursor.fetchall()

    # ==========================================
    # Get Test By ID
    # ==========================================

    def get_test_by_id(self, test_db_id):

        self.cursor.execute("""
            SELECT *
            FROM laboratory
            WHERE id = ?
        """, (
            test_db_id,
        ))

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
                    test_name = ?,
                    department = ?,
                    sample_type = ?,
                    test_fee = ?,
                    normal_range = ?,
                    patient = ?,
                    doctor = ?,
                    test_date = ?,
                    test_result = ?,
                    status = ?,
                    remarks = ?

                WHERE id = ?

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

            print(
                "Update Test Error:",
                e
            )

            return False

    # ==========================================
    # Delete Test
    # ==========================================

    def delete_test(self, test_db_id):

        try:

            self.cursor.execute(
                """
                DELETE FROM laboratory
                WHERE id = ?
                """,
                (
                    test_db_id,
                )
            )

            self.commit()

            return True

        except Exception as e:

            print(
                "Delete Test Error:",
                e
            )

            return False

    # ==========================================
    # Get Patient Names
    # ==========================================

    def get_patient_names(self):

        self.cursor.execute("""
            SELECT patient_name
            FROM patients
            ORDER BY patient_name
        """)

        return [
            row[0]
            for row in self.cursor.fetchall()
        ]

    # ==========================================
    # Get Doctor Department
    # ==========================================

    def get_doctor_department(
        self,
        doctor_name
    ):

        self.cursor.execute("""
            SELECT department
            FROM doctors
            WHERE full_name = ?
        """, (
            doctor_name,
        ))

        row = self.cursor.fetchone()

        if row:

            return row[0]

        return ""

    # ==========================================
    # Get Patient Details
    # ==========================================

    def get_patient_details(
        self,
        patient_name
    ):

        self.cursor.execute("""
            SELECT
                mobile,
                age,
                gender

            FROM patients

            WHERE patient_name = ?
        """, (
            patient_name,
        ))

        return self.cursor.fetchone()