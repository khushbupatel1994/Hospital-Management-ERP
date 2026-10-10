import customtkinter as ctk
from tkinter import messagebox
from server.client import ERPApiClient

class EnterpriseAICenter(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, corner_radius=16)
        self.api = api_client
        ctk.CTkLabel(self, text="🤖 Enterprise AI Command Center", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", padx=24, pady=(22,2))
        ctk.CTkLabel(self, text="Centralized AI • operational intelligence • server-side secrets", text_color="gray").pack(anchor="w", padx=24, pady=(0,16))
        self.dashboard = ctk.CTkTextbox(self, height=180); self.dashboard.pack(fill="x", padx=24, pady=10); self.dashboard.configure(state="disabled")
        row=ctk.CTkFrame(self, fg_color="transparent"); row.pack(fill="x", padx=24, pady=10)
        self.entry=ctk.CTkEntry(row, placeholder_text="Ask an approved hospital operations question")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,10)); self.entry.bind("<Return>", lambda _: self.ask())
        ctk.CTkButton(row, text="Ask AI", command=self.ask).pack(side="right")
        self.answer=ctk.CTkTextbox(self, height=170); self.answer.pack(fill="both", expand=True, padx=24, pady=(0,20))
        self.refresh()
    def refresh(self):
        try:
            d=self.api.enterprise_dashboard()
            text="\n".join([f"Patients: {d['patients']}",f"Doctors: {d['doctors']}",f"Today's appointments: {d['appointments_today']}",f"Pending appointments: {d['appointments_pending']}",f"Pending labs: {d['lab_pending']}",f"Low medicines: {d['low_medicines']}",f"Low inventory: {d['low_inventory']}",f"Active IPD: {d['active_ipd']}" ])
        except Exception as e: text=f"Server unavailable: {e}"
        self.dashboard.configure(state="normal"); self.dashboard.delete("1.0","end"); self.dashboard.insert("end",text); self.dashboard.configure(state="disabled")
    def ask(self):
        q=self.entry.get().strip()
        if not q: messagebox.showinfo("AI Assistant","Please enter a question.", parent=self.winfo_toplevel()); return
        try: self.answer.delete("1.0","end"); self.answer.insert("end", self.api.ask_ai(q).get("answer","No response"))
        except Exception as e: self.answer.delete("1.0","end"); self.answer.insert("end", f"Server error: {e}")
