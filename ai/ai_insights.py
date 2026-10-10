"""Deterministic operational insights used by the enterprise dashboard."""
from .ai_queries import AIQueryService


class AIInsights:
    def __init__(self):
        self.q = AIQueryService()

    def build(self):
        d = self.q.summary()
        insights = []
        if d['pending_appointments']:
            insights.append(("Appointments", f"{d['pending_appointments']} appointments are still pending.", "Review the appointment queue."))
        if d['low_pharmacy_stock'] + d['low_inventory_stock']:
            insights.append(("Inventory", f"{d['low_pharmacy_stock'] + d['low_inventory_stock']} stock items are at or below minimum level.", "Check procurement/reorder workflow."))
        if d['expiring_inventory']:
            insights.append(("Expiry Watch", f"{d['expiring_inventory']} inventory items expire within 30 days.", "Review batches before dispensing."))
        if d['lab_pending']:
            insights.append(("Laboratory", f"{d['lab_pending']} laboratory tests are pending.", "Review the lab work queue."))
        if d['ipd_active']:
            insights.append(("IPD", f"{d['ipd_active']} active IPD admissions are recorded.", "Monitor ward and bed operations."))
        if not insights:
            insights.append(("Operations", "No high-priority operational alert was detected by the rule engine.", "Continue routine monitoring."))
        return d, insights[:6]

    def close(self):
        self.q.close()
