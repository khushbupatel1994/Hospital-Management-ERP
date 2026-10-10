"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Patient CRUD
Version : 2.0
===========================================================
"""

from database.database import Database
from datetime import datetime

class PatientCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

       
        self.create_patient_table()
        self.migrate_patient_table()

    # ==========================================
    # Create Patient Table
    # ==========================================

    def create_patient_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT UNIQUE,

            registration_no TEXT UNIQUE,

            patient_name TEXT NOT NULL,

            gender TEXT,

            dob TEXT,

            age INTEGER,

            blood_group TEXT,

            mobile TEXT,

            email TEXT,

            address TEXT,

            city TEXT,

            state TEXT,

            pin_code TEXT,

            aadhaar TEXT,

            doctor TEXT,

            department TEXT,

            patient_type TEXT,

            status TEXT DEFAULT 'Active',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    def migrate_patient_table(self):
        try:
            required_columns = [
                ("registration_date", "TEXT"),
                ("registration_time", "TEXT"),
                ("registration_day", "TEXT"),
                ("father_husband_name", "TEXT"),
                ("disease", "TEXT")
            ]

            self.cursor.execute(
                "PRAGMA table_info(patients)"
            )

            existing_columns = {
                row[1]
                for row in self.cursor.fetchall()
            }

            for column, data_type in required_columns:

                if column not in existing_columns:

                    self.cursor.execute(
                        f"""
                        ALTER TABLE patients
                        ADD COLUMN {column} {data_type}
                        """
                    )

                    print(
                        f"✅ Added patients.{column}"
                    )

            self.commit()

            print(
                "✅ Patient table migration completed"
            )

        except Exception as e:

            print(
                "Patient Migration Error:",
                e
            )

    # ==========================================
    # Generate Patient ID
    # ==========================================

    def generate_patient_id(self):

        self.cursor.execute("""
            SELECT patient_id
            FROM patients
            ORDER BY id DESC
            LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row:

            last_id = row[0]

            try:
                number = int(last_id.replace("PT", "")) + 1
            except:
                number = 1

        else:

            number = 1

        return f"PT{number:06d}"

    # ==========================================
    # Generate Registration Number
    # ==========================================

    def generate_registration_no(self):

        year = datetime.now().strftime("%Y")

        self.cursor.execute("""
            SELECT registration_no
            FROM patients
            ORDER BY id DESC
            LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row:

            try:
                number = int(row[0][-6:]) + 1
            except:
                number = 1

        else:

            number = 1

        return f"REG{year}{number:06d}"

    # ==========================================
    # Check Duplicate Mobile
    # ==========================================

    def check_duplicate_mobile(self, mobile, patient_db_id=None):

        if patient_db_id:

            self.cursor.execute(
                """
                SELECT id FROM patients
                WHERE mobile=? AND id<>?
                """,
                (mobile, patient_db_id)
            )

        else:

            self.cursor.execute(
                "SELECT id FROM patients WHERE mobile=?",
                (mobile,)
            )

        return self.cursor.fetchone()
    # ==========================================
    # Check Duplicate Aadhaar
    # ==========================================

    def check_duplicate_aadhaar(self, aadhaar, patient_db_id=None):

        if patient_db_id:

            self.cursor.execute(
                """
                SELECT id
                FROM patients
                WHERE aadhaar=? AND id<>?
                """,
                (aadhaar, patient_db_id)
            )

        else:

            self.cursor.execute(
                """
                SELECT id
                FROM patients
                WHERE aadhaar=?
                """,
                (aadhaar,)
            )

        return self.cursor.fetchone()

    # ==========================================
    # Add Patient
    # ==========================================

    def add_patient(
        self,
        patient_id,
        registration_no,
        patient_name,
        gender,
        dob,
        age,
        blood_group,
        mobile,
        email,
        address,
        city,
        state,
        pin_code,
        aadhaar,
        doctor,
        department,
        patient_type,
        status,
        father_husband_name="",
        disease=""
    ):

        try:

            self.cursor.execute("""
            INSERT INTO patients
            (
                patient_id,
                registration_no,
                patient_name,
                gender,
                dob,
                age,
                blood_group,
                mobile,
                email,
                address,
                city,
                state,
                pin_code,
                aadhaar,
                doctor,
                department,
                patient_type,
                status,
                father_husband_name,
                disease
            )
            VALUES (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?
            )
            """, (
                patient_id,
                registration_no,
                patient_name,
                gender,
                dob,
                age,
                blood_group,
                mobile,
                email,
                address,
                city,
                state,
                pin_code,
                aadhaar,
                doctor,
                department,
                patient_type,
                status,
                father_husband_name,
                disease
            ))

            self.commit()

            print(
                "✅ Patient Added Successfully"
            )

            return True

        except Exception as e:

            print(
                "Add Patient Error:",
                e
            )

            return False

    # ==========================================
    # Load Patients
    # ==========================================

    def load_patients(self):

        self.cursor.execute("""
            SELECT
                id,
                patient_id,
                registration_no,
                patient_name,
                gender,
                age,
                mobile,
                doctor,
                department,
                status
            FROM patients
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Search Patient
    # ==========================================

    def search_patient(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                patient_id,
                registration_no,
                patient_name,
                gender,
                age,
                mobile,
                doctor,
                department,
                status
            FROM patients
            WHERE
                patient_id LIKE :keyword
                OR registration_no LIKE :keyword
                OR patient_code LIKE :keyword
                OR patient_name LIKE :keyword
                OR name LIKE :keyword
                OR mobile LIKE :keyword
                OR phone LIKE :keyword
                OR email LIKE :keyword
                OR address LIKE :keyword
                OR city LIKE :keyword
                OR state LIKE :keyword
                OR pin_code LIKE :keyword
                OR pincode LIKE :keyword
                OR aadhaar LIKE :keyword
                OR disease LIKE :keyword
                OR emergency_contact LIKE :keyword
                OR doctor LIKE :keyword
                OR department LIKE :keyword
                OR patient_type LIKE :keyword
                OR status LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Patient By ID
    # ==========================================

    def get_patient_by_id(self, patient_db_id):

        self.cursor.execute("""
            SELECT
                id,
                COALESCE(patient_id, ''),
                COALESCE(registration_no, ''),
                COALESCE(NULLIF(patient_name, ''), NULLIF(name, ''), ''),
                COALESCE(gender, ''),
                COALESCE(dob, ''),
                COALESCE(age, 0),
                COALESCE(blood_group, ''),
                COALESCE(NULLIF(mobile, ''), NULLIF(phone, ''), ''),
                COALESCE(email, ''),
                COALESCE(address, ''),
                COALESCE(city, ''),
                COALESCE(state, ''),
                COALESCE(NULLIF(pin_code, ''), NULLIF(pincode, ''), ''),
                COALESCE(aadhaar, ''),
                COALESCE(doctor, ''),
                COALESCE(department, ''),
                COALESCE(patient_type, ''),
                COALESCE(status, '')
            FROM patients
            WHERE id=?
        """, (patient_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update Patient
    # ==========================================

    def update_patient(
    self,
    patient_db_id,
    patient_name,
    gender,
    dob,
    age,
    blood_group,
    mobile,
    email,
    address,
    city,
    state,
    pin_code,
    aadhaar,
    doctor,
    department,
    patient_type,
    status,
    father_husband_name="",
    disease=""
    ):
        try:
            self.cursor.execute("""
            UPDATE patients
            SET
                patient_name=?,
                gender=?,
                dob=?,
                age=?,
                blood_group=?,
                mobile=?,
                email=?,
                address=?,
                city=?,
                state=?,
                pin_code=?,
                aadhaar=?,
                doctor=?,
                department=?,
                patient_type=?,
                status=?,
                father_husband_name=?,
                disease=?
            WHERE id=?
        """, (
            patient_name,
            gender,
            dob,
            age,
            blood_group,
            mobile,
            email,
            address,
            city,
            state,
            pin_code,
            aadhaar,
            doctor,
            department,
            patient_type,
            status,
            father_husband_name,
            disease,
            patient_db_id
        ))

            self.commit()

            print(
                "✅ Patient Updated Successfully"
            )

            return True

        except Exception as e:

            print(
                "Update Patient Error:",
                e
            )

            return False

    # ==========================================
    # Delete Patient
    # ==========================================

    def delete_patient(self, patient_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM patients WHERE id=?",
                (patient_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Patient Error:", e)

            return False
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
