"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Pharmacy CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class PharmacyCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_medicine_table()

    # ==========================================
    # Create Medicine Table
    # ==========================================

    def create_medicine_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            medicine_id TEXT UNIQUE,

            medicine_name TEXT NOT NULL,

            company_name TEXT,

            batch_no TEXT,

            category TEXT,

            expiry_date TEXT,

            purchase_price REAL,

            selling_price REAL,

            stock_quantity INTEGER,

            minimum_stock INTEGER,

            unit TEXT,

            gst REAL,

            manufacturer TEXT,

            supplier TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate Unique Medicine ID
    # ==========================================

    def generate_medicine_id(self):
        number = 1

        while True:
            medicine_id = f"MED{number:06d}"

            self.cursor.execute(
                """
                SELECT 1
                FROM medicines
                WHERE medicine_id = ?
                LIMIT 1
                """,
                (medicine_id,)
            )

            if not self.cursor.fetchone():
                return medicine_id

            number += 1

    # ==========================================
    # Add Medicine
    # ==========================================

    def add_medicine(
        self,
        medicine_id,
        medicine_name,
        company_name,
        batch_no,
        category,
        expiry_date,
        purchase_price,
        selling_price,
        stock_quantity,
        minimum_stock,
        unit,
        gst,
        manufacturer,
        supplier,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO medicines
                (
                    medicine_id,
                    medicine_name,
                    company_name,
                    batch_no,
                    category,
                    expiry_date,
                    purchase_price,
                    selling_price,
                    stock_quantity,
                    minimum_stock,
                    unit,
                    gst,
                    manufacturer,
                    supplier,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                medicine_id,
                medicine_name,
                company_name,
                batch_no,
                category,
                expiry_date,
                purchase_price,
                selling_price,
                stock_quantity,
                minimum_stock,
                unit,
                gst,
                manufacturer,
                supplier,
                remarks
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Medicine Error:", e)

            return False


    # ==========================================
    # Load Medicines
    # ==========================================

    def load_medicines(self):

        self.cursor.execute("""
            SELECT
                id,
                medicine_id,
                medicine_name,
                company_name,
                category,
                stock_quantity,
                selling_price,
                expiry_date
            FROM medicines
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()
        print("Medicines Table:", rows)

        return rows

    # ==========================================
    # Search Medicine
    # ==========================================

    def search_medicine(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                medicine_id,
                medicine_name,
                company_name,
                category,
                stock_quantity,
                selling_price,
                expiry_date
            FROM medicines
            WHERE
                medicine_id LIKE :keyword
                OR medicine_name LIKE :keyword
                OR company_name LIKE :keyword
                OR manufacturer LIKE :keyword
                OR supplier LIKE :keyword
                OR category LIKE :keyword
                OR batch_no LIKE :keyword
                OR expiry_date LIKE :keyword
                OR CAST(purchase_price AS TEXT) LIKE :keyword
                OR CAST(selling_price AS TEXT) LIKE :keyword
                OR CAST(stock_quantity AS TEXT) LIKE :keyword
                OR unit LIKE :keyword
                OR remarks LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Medicine By ID
    # ==========================================

    def get_medicine_by_id(self, medicine_db_id):

        self.cursor.execute("""
            SELECT *
            FROM medicines
            WHERE id=?
        """, (medicine_db_id,))

        return self.cursor.fetchone()


    # ==========================================
    # Update Medicine
    # ==========================================

    def update_medicine(
        self,
        medicine_db_id,
        medicine_name,
        company_name,
        batch_no,
        category,
        expiry_date,
        purchase_price,
        selling_price,
        stock_quantity,
        minimum_stock,
        unit,
        gst,
        manufacturer,
        supplier,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE medicines
                SET
                    medicine_name=?,
                    company_name=?,
                    batch_no=?,
                    category=?,
                    expiry_date=?,
                    purchase_price=?,
                    selling_price=?,
                    stock_quantity=?,
                    minimum_stock=?,
                    unit=?,
                    gst=?,
                    manufacturer=?,
                    supplier=?,
                    remarks=?
                WHERE id=?
            """, (
                medicine_name,
                company_name,
                batch_no,
                category,
                expiry_date,
                purchase_price,
                selling_price,
                stock_quantity,
                minimum_stock,
                unit,
                gst,
                manufacturer,
                supplier,
                remarks,
                medicine_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Medicine Error:", e)

            return False


    # ==========================================
    # Delete Medicine
    # ==========================================

    def delete_medicine(self, medicine_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM medicines WHERE id=?",
                (medicine_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Medicine Error:", e)

            return False
