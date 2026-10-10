"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : OPD CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class OPDCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_opd_table()

    # ==========================================
    # Create OPD Table
    # ==========================================

    def create_opd_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS opd(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            opd_id TEXT UNIQUE,

            patient TEXT NOT NULL,

            doctor TEXT NOT NULL,

            department TEXT,

            visit_date TEXT,

            visit_time TEXT,

            chief_complaint TEXT,

            diagnosis TEXT,

            prescription TEXT,

            followup_date TEXT,

            notes TEXT,

            status TEXT DEFAULT 'Open',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate OPD ID
    # ==========================================

    def generate_opd_id(self):
        self.cursor.execute("SELECT MAX(id) FROM opd")
        result = self.cursor.fetchone()[0]

        if result is None:
            next_id = 1
        else:
            next_id = result + 1

        return f"OPD{next_id:06d}"
    # ==========================================
    # Add OPD
    # ==========================================

    def add_opd(
        self,
        opd_id,
        patient,
        doctor,
        department,
        visit_date,
        visit_time,
        chief_complaint,
        diagnosis,
        prescription,
        followup_date,
        notes,
        status
    ):

        try:

            self.cursor.execute("""
                INSERT INTO opd
                (
                    opd_id,
                    patient,
                    doctor,
                    department,
                    visit_date,
                    visit_time,
                    chief_complaint,
                    diagnosis,
                    prescription,
                    followup_date,
                    notes,
                    status
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                opd_id,
                patient,
                doctor,
                department,
                visit_date,
                visit_time,
                chief_complaint,
                diagnosis,
                prescription,
                followup_date,
                notes,
                status
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add OPD Error:", e)

            return False

    # ==========================================
    # Load OPD
    # ==========================================

    def load_opd(self):

        self.cursor.execute("""
            SELECT
                id,
                opd_id,
                patient,
                doctor,
                department,
                visit_date,
                visit_time,
                status
            FROM opd
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Search OPD
    # ==========================================

    def search_opd(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                opd_id,
                patient,
                doctor,
                department,
                visit_date,
                visit_time,
                status
                FROM opd
                 WHERE
                opd_id LIKE :keyword
                OR patient LIKE :keyword
                OR doctor LIKE :keyword
                OR department LIKE :keyword
                OR visit_date LIKE :keyword
                OR visit_time LIKE :keyword
                OR chief_complaint LIKE :keyword
                OR diagnosis LIKE :keyword
                OR prescription LIKE :keyword
                OR followup_date LIKE :keyword
                OR notes LIKE :keyword
                OR status LIKE :keyword
                OR EXISTS (
                    SELECT 1
                    FROM patients AS patient_record
                    WHERE patient_record.mobile LIKE :keyword
                      AND (
                          patient_record.patient_name = opd.patient
                          OR patient_record.name = opd.patient
                      )
                )
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get OPD By ID
    # ==========================================

    def get_opd_by_id(self, opd_db_id):

        self.cursor.execute("""
            SELECT *
            FROM opd
            WHERE id=?
        """, (opd_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update OPD
    # ==========================================

    def update_opd(
        self,
        opd_db_id,
        patient,
        doctor,
        department,
        visit_date,
        visit_time,
        chief_complaint,
        diagnosis,
        prescription,
        followup_date,
        notes,
        status
    ):

        try:

            self.cursor.execute("""
                UPDATE opd
                SET
                    patient=?,
                    doctor=?,
                    department=?,
                    visit_date=?,
                    visit_time=?,
                    chief_complaint=?,
                    diagnosis=?,
                    prescription=?,
                    followup_date=?,
                    notes=?,
                    status=?
                WHERE id=?
            """, (
                patient,
                doctor,
                department,
                visit_date,
                visit_time,
                chief_complaint,
                diagnosis,
                prescription,
                followup_date,
                notes,
                status,
                opd_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update OPD Error:", e)

            return False

    # ==========================================
    # Delete OPD
    # ==========================================

    def delete_opd(self, opd_db_id):
        try:

            self.cursor.execute(
                "DELETE FROM opd WHERE id=?",
                (opd_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete OPD Error:", e)

            return False
