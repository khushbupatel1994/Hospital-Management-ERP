"""Read-only, schema-aware queries for the Hospital ERP AI layer."""
from datetime import date, timedelta
from database.database import Database


class AIQueryService:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def _one(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else 0

    def _rows(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def _table_exists(self, name):
        return bool(self._one("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (name,)))

    def summary(self):
        today = date.today().isoformat()
        week_start = (date.today() - timedelta(days=6)).isoformat()
        data = {
            "doctors": int(self._one("SELECT COUNT(*) FROM doctors")),
            "active_doctors": int(self._one("SELECT COUNT(*) FROM doctors WHERE LOWER(COALESCE(status,''))='active'")),
            "patients": int(self._one("SELECT COUNT(*) FROM patients")),
            "appointments": int(self._one("SELECT COUNT(*) FROM appointments")),
            "pending_appointments": int(self._one("SELECT COUNT(*) FROM appointments WHERE LOWER(COALESCE(status,''))='pending'")),
            "today_appointments": int(self._one("SELECT COUNT(*) FROM appointments WHERE appointment_date=?", (today,))),
            "lab_pending": int(self._one("SELECT COUNT(*) FROM lab_tests WHERE LOWER(COALESCE(status,''))='pending'")) if self._table_exists('lab_tests') else 0,
            "low_pharmacy_stock": int(self._one("SELECT COUNT(*) FROM pharmacy WHERE quantity <= minimum_stock")) if self._table_exists('pharmacy') else 0,
            "low_inventory_stock": int(self._one("SELECT COUNT(*) FROM inventory WHERE stock_quantity <= minimum_stock")) if self._table_exists('inventory') else 0,
            "expiring_inventory": int(self._one("SELECT COUNT(*) FROM inventory WHERE expiry_date IS NOT NULL AND expiry_date <> '' AND expiry_date <= date('now','+30 day')")) if self._table_exists('inventory') else 0,
            "ipd_active": int(self._one("SELECT COUNT(*) FROM ipd WHERE LOWER(COALESCE(status,'')) NOT IN ('discharged','closed')")) if self._table_exists('ipd') else 0,
            "revenue": float(self._one("SELECT COALESCE(SUM(CASE WHEN total_amount > 0 THEN total_amount ELSE total END),0) FROM billing")),
            "week_revenue": float(self._one("SELECT COALESCE(SUM(CASE WHEN total_amount > 0 THEN total_amount ELSE total END),0) FROM billing WHERE bill_date >= ?", (week_start,))),
        }
        return data

    def top_departments(self, limit=5):
        return self._rows("""SELECT COALESCE(department,'Unassigned') AS department, COUNT(*) AS total
                            FROM appointments GROUP BY department ORDER BY total DESC LIMIT ?""", (limit,))

    def low_stock_items(self, limit=10):
        rows = []
        if self._table_exists('inventory'):
            rows.extend(self._rows("""SELECT item_name, stock_quantity, minimum_stock, expiry_date
                                    FROM inventory WHERE stock_quantity <= minimum_stock
                                    ORDER BY stock_quantity ASC LIMIT ?""", (limit,)))
        if self._table_exists('pharmacy') and len(rows) < limit:
            rows.extend(self._rows("""SELECT medicine_name, quantity, minimum_stock, expiry_date
                                    FROM pharmacy WHERE quantity <= minimum_stock
                                    ORDER BY quantity ASC LIMIT ?""", (limit-len(rows),)))
        return rows[:limit]

    def close(self):
        self.db.close()
