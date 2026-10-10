import customtkinter as ctk
from tkinter import messagebox
from server.client import ERPApiClient

class RemoteAICenter(ctk.CTkFrame):
    """Server-backed AI center. No central DB or AI secret is stored in the client."""
    def __init__(self, parent, api_client=None):
        super().__init__(parent, corner_radius=16)
        self.api = api_client or ERPApiClient()
        ctk.CTkLabel(self, text="🤖 AI Hospital Intelligence", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", padx=24, pady=(22,2))
        ctk.CTkLabel(self, text="Server-backed enterprise AI • controlled operational assistance", text_color="gray").pack(anchor="w", padx=24, pady=(0,16))
        self.metrics=ctk.CTkTextbox(self,height=150); self.metrics.pack(fill="x",padx=24,pady=10); self.metrics.configure(state="disabled")
        row=ctk.CTkFrame(self,fg_color="transparent"); row.pack(fill="x",padx=24,pady=10)
        self.entry=ctk.CTkEntry(row,placeholder_text="Ask: How many patients are registered?"); self.entry.pack(side="left",fill="x",expand=True,padx=(0,10))
        self.btn=ctk.CTkButton(row,text="Ask AI",command=self.ask); self.btn.pack(side="right")
        self.answer=ctk.CTkTextbox(self,height=180); self.answer.pack(fill="both",expand=True,padx=24,pady=(0,20))
        self.refresh()
    def refresh(self):
        try:
            d=self.api.summary(); text=(f"Patients: {d['patients']}\nDoctors: {d['doctors']}\nToday appointments: {d['today_appointments']}\nPending labs: {d['pending_lab_tests']}\nLow medicines: {d['low_medicines']}\nLow inventory: {d['low_inventory']}\nActive IPD: {d['active_ipd']}")
        except Exception as e: text=f"Server unavailable: {e}"
        self.metrics.configure(state="normal"); self.metrics.delete("1.0","end"); self.metrics.insert("end",text); self.metrics.configure(state="disabled")
    def ask(self):
        q=self.entry.get().strip()
        if not q: messagebox.showinfo("AI Assistant","Please enter a question."); return
        try: self.answer.delete("1.0","end"); self.answer.insert("end",self.api.ask_ai(q)["answer"])
        except Exception as e: self.answer.delete("1.0","end"); self.answer.insert("end",f"Server error: {e}")
