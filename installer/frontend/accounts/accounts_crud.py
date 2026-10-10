"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Accounts CRUD
Version : 2.0
===========================================================
"""

from database.database import Database


class AccountsCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_accounts_table()

    # ==========================================
    # Create Accounts Table
    # ==========================================

    def create_accounts_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            transaction_id TEXT UNIQUE,

            transaction_type TEXT NOT NULL,

            category TEXT,

            amount REAL,

            payment_mode TEXT,

            transaction_date TEXT,

            description TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Generate Transaction ID
    # ==========================================

    def generate_transaction_id(self):

        self.cursor.execute(
            "SELECT MAX(id) FROM accounts"
        )

        result = self.cursor.fetchone()[0]

        if result is None:

            result = 0

        return f"ACC{result + 1:06d}"

    # ==========================================
    # Add Transaction
    # ==========================================

    def add_transaction(
        self,
        transaction_id,
        transaction_type,
        category,
        amount,
        payment_mode,
        transaction_date,
        description,
        remarks
    ):

        try:

            self.cursor.execute("""
                INSERT INTO accounts
                (
                    transaction_id,
                    transaction_type,
                    category,
                    amount,
                    payment_mode,
                    transaction_date,
                    description,
                    remarks
                )
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                transaction_id,
                transaction_type,
                category,
                amount,
                payment_mode,
                transaction_date,
                description,
                remarks
            ))

            self.commit()

            return True

        except Exception as e:

            print("Add Transaction Error:", e)

            return False

    # ==========================================
    # Load Transactions
    # ==========================================

    def load_transactions(self):

        self.cursor.execute("""
            SELECT
                id,
                transaction_id,
                transaction_type,
                category,
                amount,
                payment_mode,
                transaction_date
            FROM accounts
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Search Transaction
    # ==========================================

    def search_transaction(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                transaction_id,
                transaction_type,
                category,
                amount,
                payment_mode,
                transaction_date
            FROM accounts
            WHERE
                transaction_id LIKE :keyword
                OR transaction_type LIKE :keyword
                OR category LIKE :keyword
                OR CAST(amount AS TEXT) LIKE :keyword
                OR payment_mode LIKE :keyword
                OR transaction_date LIKE :keyword
                OR description LIKE :keyword
                OR remarks LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()

    # ==========================================
    # Get Transaction By ID
    # ==========================================

    def get_transaction_by_id(self, transaction_db_id):

        self.cursor.execute("""
            SELECT *
            FROM accounts
            WHERE id=?
        """, (transaction_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update Transaction
    # ==========================================

    def update_transaction(
        self,
        transaction_db_id,
        transaction_type,
        category,
        amount,
        payment_mode,
        transaction_date,
        description,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE accounts
                SET
                    transaction_type=?,
                    category=?,
                    amount=?,
                    payment_mode=?,
                    transaction_date=?,
                    description=?,
                    remarks=?
                WHERE id=?
            """, (
                transaction_type,
                category,
                amount,
                payment_mode,
                transaction_date,
                description,
                remarks,
                transaction_db_id
            ))

            self.commit()

            return True

        except Exception as e:

            print("Update Transaction Error:", e)

            return False


    # ==========================================
    # Delete Transaction
    # ==========================================

    def delete_transaction(self, transaction_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM accounts WHERE id=?",
                (transaction_db_id,)
            )

            self.commit()

            return True

        except Exception as e:

            print("Delete Transaction Error:", e)

            return False
