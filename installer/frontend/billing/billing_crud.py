"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Billing CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class BillingCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_billing_table()

    # ==========================================
    # Create Billing Table
    # ==========================================

    def create_billing_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            bill_id TEXT UNIQUE,

            patient TEXT NOT NULL,

            doctor TEXT NOT NULL,

            bill_date TEXT,

            consultation_fee REAL,

            medicine_charges REAL,

            lab_charges REAL,

            other_charges REAL,

            discount REAL,

            total_amount REAL,

            payment_mode TEXT,

            bill_status TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    def generate_bill_id(self):

        self.cursor.execute("""
            SELECT bill_id
            FROM billing
            WHERE bill_id LIKE 'BILL%'
            ORDER BY id DESC
            LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row and row[0]:

            try:
                last_number = int(
                    row[0].replace("BILL", "")
                )

            except ValueError:
                last_number = 0

        else:
            last_number = 0

        next_number = last_number + 1

        return f"BILL{next_number:06d}"

    # ==========================================
    # Add Bill
    # ==========================================

    def add_bill(
        self,
        bill_id,
        patient,
        doctor,
        bill_date,
        consultation_fee,
        medicine_charges,
        lab_charges,
        other_charges,
        discount,
        total_amount,
        payment_mode,
        bill_status,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO billing
                (
                    bill_id,
                    patient,
                    doctor,
                    bill_date,
                    consultation_fee,
                    medicine_charges,
                    lab_charges,
                    other_charges,
                    discount,
                    total_amount,
                    payment_mode,
                    bill_status,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                bill_id,
                patient,
                doctor,
                bill_date,
                consultation_fee,
                medicine_charges,
                lab_charges,
                other_charges,
                discount,
                total_amount,
                payment_mode,
                bill_status,
                remarks
            ))
            
            print("INSERT SUCCESS - BEFORE COMMIT")

            self.commit()

            print("COMMIT SUCCESS - BILL SAVED")

            return True
        except Exception as e:

            import traceback
            traceback.print_exc()

            print("Add Bill Error:", e)

            return False

    # ==========================================
    # Load Bills
    # ==========================================

    def load_bills(self):

        self.cursor.execute("""
            SELECT
                id,
                bill_id,
                patient,
                doctor,
                bill_date,
                total_amount,
                payment_mode,
                bill_status
            FROM billing
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()


    # ==========================================
    # Search Bill
    # ==========================================

    def search_bill(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                bill_id,
                patient,
                doctor,
                bill_date,
                total_amount,
                payment_mode,
                bill_status
            FROM billing
            WHERE
                bill_id LIKE :keyword
                OR bill_no LIKE :keyword
                OR patient LIKE :keyword
                OR patient_name LIKE :keyword
                OR doctor LIKE :keyword
                OR doctor_name LIKE :keyword
                OR bill_date LIKE :keyword
                OR CAST(total_amount AS TEXT) LIKE :keyword
                OR CAST(total AS TEXT) LIKE :keyword
                OR payment_mode LIKE :keyword
                OR payment_method LIKE :keyword
                OR bill_status LIKE :keyword
                OR payment_status LIKE :keyword
                OR remarks LIKE :keyword
                OR created_by LIKE :keyword
                OR EXISTS (
                    SELECT 1
                    FROM patients AS patient_record
                    WHERE patient_record.mobile LIKE :keyword
                      AND (
                          patient_record.patient_name = billing.patient
                          OR patient_record.name = billing.patient
                          OR patient_record.patient_name = billing.patient_name
                          OR patient_record.name = billing.patient_name
                      )
                )
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()


    # ==========================================
    # Get Bill By ID
    # ==========================================

    def get_bill_by_id(self, bill_db_id):
        self.cursor.execute("""
          SELECT
            id,
            bill_id,

            COALESCE(
                NULLIF(patient_name, ''),
                NULLIF(patient, ''),
                ''
            ) AS patient,

            COALESCE(
                NULLIF(doctor_name, ''),
                NULLIF(doctor, ''),
                ''
            ) AS doctor,

            bill_date,

            COALESCE(
                NULLIF(consultation_fee, 0),
                consultation,
                0
            ) AS consultation_fee,

            COALESCE(
                NULLIF(medicine_charges, 0),
                medicine_charge,
                0
            ) AS medicine_charges,

            COALESCE(
                NULLIF(lab_charges, 0),
                lab_charge,
                0
            ) AS lab_charges,

            COALESCE(
                NULLIF(other_charges, 0),
                other_charge,
                0
            ) AS other_charges,

            discount,

            COALESCE(
                NULLIF(total_amount, 0),
                total,
                0
            ) AS total_amount,

            COALESCE(
                NULLIF(payment_mode, ''),
                payment_method,
                ''
            ) AS payment_mode,

            COALESCE(
                NULLIF(bill_status, ''),
                payment_status,
                ''
            ) AS bill_status,

            remarks

        FROM billing
        WHERE id=?
    """, (bill_db_id,))

        return self.cursor.fetchone()


    # ==========================================
    # Update Bill
    # ==========================================

    def update_bill(
        self,
        bill_db_id,
        patient,
        doctor,
        bill_date,
        consultation_fee,
        medicine_charges,
        lab_charges,
        other_charges,
        discount,
        total_amount,
        payment_mode,
        bill_status,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE billing
                SET
                    patient=?,
                    doctor=?,
                    bill_date=?,
                    consultation_fee=?,
                    medicine_charges=?,
                    lab_charges=?,
                    other_charges=?,
                    discount=?,
                    total_amount=?,
                    payment_mode=?,
                    bill_status=?,
                    remarks=?
                WHERE id=?
            """, (
                patient,
                doctor,
                bill_date,
                consultation_fee,
                medicine_charges,
                lab_charges,
                other_charges,
                discount,
                total_amount,
                payment_mode,
                bill_status,
                remarks,
                bill_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Bill Error:", e)

            return False


    # ==========================================
    # Delete Bill
    # ==========================================

    def delete_bill(self, bill_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM billing WHERE id=?",
                (bill_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Bill Error:", e)

            return False

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
    # Get Doctor Details
    # ==========================================

    def get_doctor_details(self, doctor_name):

        self.cursor.execute("""
            SELECT department, consultation_fee
            FROM doctors
            WHERE full_name=?
        """, (doctor_name,))

        return self.cursor.fetchone()
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
