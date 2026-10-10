"""Controlled AI service for the Hospital ERP.

Only aggregate operational metrics are sent to an external model. Patient names,
contact details, identifiers, diagnoses, prescriptions and raw clinical records
are intentionally excluded from the AI prompt.
"""
import os
from .ai_queries import AIQueryService

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class HospitalAIService:
    def __init__(self):
        self.query_service = AIQueryService()
        self.client = None
        self.model = os.getenv("HOSPITAL_AI_MODEL", "").strip()
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if api_key and OpenAI and self.model:
            self.client = OpenAI(api_key=api_key)

    def get_context(self):
        return self.query_service.summary()

    def _offline(self, question, data):
        q = question.lower()
        if any(x in q for x in ("doctor", "डॉक्टर")):
            return f"There are {data['doctors']} doctors ({data['active_doctors']} active)."
        if any(x in q for x in ("patient", "मरीज", "रोगी")):
            return f"There are {data['patients']} patients registered in the ERP."
        if "appointment" in q or "अपॉइंटमेंट" in q:
            return f"There are {data['appointments']} appointments, with {data['pending_appointments']} pending and {data['today_appointments']} scheduled today."
        if "lab" in q or "laboratory" in q:
            return f"There are {data['lab_pending']} pending laboratory tests."
        if any(x in q for x in ("stock", "inventory", "medicine", "pharmacy", "स्टॉक")):
            return f"Low-stock items: {data['low_pharmacy_stock']} in pharmacy and {data['low_inventory_stock']} in inventory. {data['expiring_inventory']} inventory items are due to expire within 30 days."
        if "ipd" in q or "bed" in q or "admission" in q:
            return f"There are {data['ipd_active']} active IPD admissions."
        if "revenue" in q or "billing" in q:
            return f"Recorded billing revenue is ₹{data['revenue']:,.2f}; the last 7 days account for ₹{data['week_revenue']:,.2f}."
        return "AI live mode is not configured. Ask about doctors, patients, appointments, laboratory, stock, IPD or billing for an offline ERP summary."

    def ask(self, question):
        question = (question or "").strip()
        if not question:
            return "Please enter a question."
        data = self.get_context()
        if not self.client:
            return self._offline(question, data)

        prompt = f"""You are the administrative intelligence assistant for a hospital ERP.
Use ONLY the aggregate operational metrics below. Never invent numbers.
Do not diagnose, prescribe, triage, or make clinical decisions.
Do not request, expose, infer, or reconstruct personal patient information.
If a request requires patient-level clinical judgment, direct the user to the qualified clinician and the protected ERP record.
Answer in concise professional language and mention when a metric is only a system aggregate.

Aggregate metrics:
{data}

User question:
{question}
"""
        response = self.client.responses.create(model=self.model, input=prompt)
        return (response.output_text or "No response returned.").strip()

    def close(self):
        self.query_service.close()
