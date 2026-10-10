"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Doctor CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class DoctorCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_doctor_table()

# ==========================================
# Create Doctor Table
# ==========================================

    def create_doctor_table(self):

       self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        doctor_id TEXT UNIQUE,

        full_name TEXT NOT NULL,

        gender TEXT,

        department TEXT,

        specialization TEXT,

        qualification TEXT,

        experience INTEGER,

        mobile TEXT,

        email TEXT,

        consultation_fee REAL,

        opd_timing TEXT,

        available_days TEXT,

        status TEXT DEFAULT 'Active',

        created_at TEXT DEFAULT CURRENT_TIMESTAMP

    )
    """)

       self.commit()

# ==========================================
# Generate Doctor ID
# ==========================================

    def generate_doctor_id(self):

       self.cursor.execute(
        "SELECT COUNT(*) FROM doctors"
     )

       count = self.cursor.fetchone()[0] + 1

       return f"DOC{count:04d}"

# ==========================================
# Check Duplicate Mobile
# ==========================================

    def check_duplicate_mobile(
        self,
        mobile,
        doctor_db_id=None
    ):

        if doctor_db_id:

            self.cursor.execute(
                """
                SELECT id
                FROM doctors
                WHERE mobile=? AND id<>?
                """,
                (
                    mobile,
                    doctor_db_id
                )
            )

        else:

            self.cursor.execute(
                """
                SELECT id
                FROM doctors
                WHERE mobile=?
                """,
                (mobile,)
            )

        return self.cursor.fetchone()

# ==========================================
# Add Doctor
# ==========================================

    def add_doctor(
        self,
        doctor_id,
        full_name,
        gender,
        department,
        specialization,
        qualification,
        experience,
        mobile,
        email,
        consultation_fee,
        opd_timing,
        available_days,
        status
    ):

        try:

            self.cursor.execute("""
                INSERT INTO doctors
                (
                    doctor_id,
                    full_name,
                    gender,
                    department,
                    specialization,
                    qualification,
                    experience,
                    mobile,
                    email,
                    consultation_fee,
                    opd_timing,
                    available_days,
                    status
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                doctor_id,
                full_name,
                gender,
                department,
                specialization,
                qualification,
                experience,
                mobile,
                email,
                consultation_fee,
                opd_timing,
                available_days,
                status
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Doctor Error:", e)

            return False

# ==========================================
# Load Doctors
# ==========================================

    def load_doctors(self):

        self.cursor.execute("""
            SELECT
                id,
                doctor_id,
                full_name,
                department,
                specialization,
                mobile,
                consultation_fee,
                status
            FROM doctors
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

# ==========================================
# Search Doctor
# ==========================================

    def search_doctor(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                doctor_id,
                full_name,
                department,
                specialization,
                mobile,
                consultation_fee,
                status
            FROM doctors
            WHERE
                doctor_id LIKE :keyword
                OR doctor_code LIKE :keyword
                OR full_name LIKE :keyword
                OR name LIKE :keyword
                OR department LIKE :keyword
                OR specialization LIKE :keyword
                OR qualification LIKE :keyword
                OR CAST(experience AS TEXT) LIKE :keyword
                OR mobile LIKE :keyword
                OR phone LIKE :keyword
                OR email LIKE :keyword
                OR opd_timing LIKE :keyword
                OR available_days LIKE :keyword
                OR available_time LIKE :keyword
                OR joining_date LIKE :keyword
                OR status LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

# ==========================================
# Get Doctor By ID
# ==========================================

    def get_doctor_by_id(self, doctor_db_id):

        self.cursor.execute("""
            SELECT *
            FROM doctors
            WHERE id=?
        """, (doctor_db_id,))

        return self.cursor.fetchone()

# ==========================================
# Update Doctor
# ==========================================

    def update_doctor(
        self,
        doctor_db_id,
        full_name,
        gender,
        department,
        specialization,
        qualification,
        experience,
        mobile,
        email,
        consultation_fee,
        opd_timing,
        available_days,
        status
    ):

        try:

            self.cursor.execute("""
                UPDATE doctors
                SET
                    full_name=?,
                    gender=?,
                    department=?,
                    specialization=?,
                    qualification=?,
                    experience=?,
                    mobile=?,
                    email=?,
                    consultation_fee=?,
                    opd_timing=?,
                    available_days=?,
                    status=?
                WHERE id=?
            """, (
                full_name,
                gender,
                department,
                specialization,
                qualification,
                experience,
                mobile,
                email,
                consultation_fee,
                opd_timing,
                available_days,
                status,
                doctor_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Doctor Error:", e)

            return False

# ==========================================
# Delete Doctor
# ==========================================

    def delete_doctor(self, doctor_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM doctors WHERE id=?",
                (doctor_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Doctor Error:", e)

            return False
