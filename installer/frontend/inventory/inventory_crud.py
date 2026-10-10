"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Inventory CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class InventoryCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_inventory_table()

    # ==========================================
    # Create Inventory Table
    # ==========================================

    def create_inventory_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_id TEXT UNIQUE,

            item_name TEXT NOT NULL,

            category TEXT,

            supplier TEXT,

            batch_no TEXT,

            purchase_price REAL,

            selling_price REAL,

            stock_quantity INTEGER,

            minimum_stock INTEGER,

            unit TEXT,

            gst REAL,

            expiry_date TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate Item ID
    # ==========================================

    def generate_item_id(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM inventory"
        )

        count = self.cursor.fetchone()[0] + 1

        return f"INV{count:06d}"

    # ==========================================
    # Add Item
    # ==========================================


    def add_item(
        self,
        item_id,
        item_name,
        category,
        supplier,
        batch_no,
        purchase_price,
        selling_price,
        stock_quantity,
        minimum_stock,
        unit,
        gst,
        expiry_date,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO inventory
                (
                    item_id,
                    item_name,
                    category,
                    supplier,
                    batch_no,
                    purchase_price,
                    selling_price,
                    stock_quantity,
                    minimum_stock,
                    unit,
                    gst,
                    expiry_date,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                item_id,
                item_name,
                category,
                supplier,
                batch_no,
                purchase_price,
                selling_price,
                stock_quantity,
                minimum_stock,
                unit,
                gst,
                expiry_date,
                remarks
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Item Error:", e)

            return False


    # ==========================================
    # Load Items
    # ==========================================

    def load_items(self):

        self.cursor.execute("""
            SELECT
                id,
                item_id,
                item_name,
                category,
                supplier,
                stock_quantity,
                selling_price,
                expiry_date
            FROM inventory
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()


   # ==========================================
   # Search Item
   # ==========================================

    def search_item(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                item_id,
                item_name,
                category,
                supplier,
                stock_quantity,
                selling_price,
                expiry_date
            FROM inventory
            WHERE
                item_id LIKE :keyword
                OR item_name LIKE :keyword
                OR category LIKE :keyword
                OR supplier LIKE :keyword
                OR batch_no LIKE :keyword
                OR CAST(purchase_price AS TEXT) LIKE :keyword
                OR CAST(selling_price AS TEXT) LIKE :keyword
                OR CAST(stock_quantity AS TEXT) LIKE :keyword
                OR unit LIKE :keyword
                OR expiry_date LIKE :keyword
                OR remarks LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Item By ID
    # ==========================================

    def get_item_by_id(self, item_db_id):

        self.cursor.execute("""
            SELECT *
            FROM inventory
            WHERE id=?
        """, (item_db_id,))

        return self.cursor.fetchone()


    # ==========================================
    # Update Item
    # ==========================================

    def update_item(
        self,
        item_db_id,
        item_name,
        category,
        supplier,
        batch_no,
        purchase_price,
        selling_price,
        stock_quantity,
        minimum_stock,
        unit,
        gst,
        expiry_date,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE inventory
                SET
                    item_name=?,
                    category=?,
                    supplier=?,
                    batch_no=?,
                    purchase_price=?,
                    selling_price=?,
                    stock_quantity=?,
                    minimum_stock=?,
                    unit=?,
                    gst=?,
                    expiry_date=?,
                    remarks=?
                WHERE id=?
            """, (
                item_name,
                category,
                supplier,
                batch_no,
                purchase_price,
                selling_price,
                stock_quantity,
                minimum_stock,
                unit,
                gst,
                expiry_date,
                remarks,
                item_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Item Error:", e)

            return False


    # ==========================================
    # Delete Item
    # ==========================================

    def delete_item(self, item_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM inventory WHERE id=?",
                (item_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Item Error:", e)

            return False

  
