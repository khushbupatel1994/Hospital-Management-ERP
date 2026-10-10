"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Settings CRUD
Version : 3.0
===========================================================
"""

from database.database import Database


class SettingsCRUD(Database):

    def __init__(self):

        super().__init__()

        self.connect()

        self.create_settings_table()

    # ==========================================
    # Create Settings Table
    # ==========================================

    def create_settings_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hospital_name TEXT,

            address TEXT,

            city TEXT,

            state TEXT,

            pincode TEXT,

            phone TEXT,

            email TEXT,

            website TEXT,

            gst_number TEXT,

            currency TEXT,

            invoice_footer TEXT,

            logo_path TEXT,

            theme TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.commit()

    # ==========================================
    # Save Settings
    # ==========================================

    def save_settings(
        self,
        hospital_name,
        address,
        city,
        state,
        pincode,
        phone,
        email,
        website,
        gst_number,
        currency,
        invoice_footer,
        logo_path,
        theme
    ):

        try:

            # Only one settings record

            self.cursor.execute(
                "DELETE FROM settings"
            )

            self.cursor.execute("""
                INSERT INTO settings
                (
                    hospital_name,
                    address,
                    city,
                    state,
                    pincode,
                    phone,
                    email,
                    website,
                    gst_number,
                    currency,
                    invoice_footer,
                    logo_path,
                    theme
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                hospital_name,
                address,
                city,
                state,
                pincode,
                phone,
                email,
                website,
                gst_number,
                currency,
                invoice_footer,
                logo_path,
                theme
            ))

            self.commit()

            return True

        except Exception as e:

            print("Save Settings Error:", e)

            return False
    # ==========================================
    # Load Settings
    # ==========================================

    def load_settings(self):

        self.cursor.execute("""
            SELECT
                hospital_name,
                address,
                city,
                state,
                pincode,
                phone,
                email,
                website,
                gst_number,
                currency,
                invoice_footer,
                logo_path,
                theme
            FROM settings
            LIMIT 1
        """)

        return self.cursor.fetchone()
        