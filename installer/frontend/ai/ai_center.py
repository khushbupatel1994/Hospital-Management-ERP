import customtkinter as ctk
from ai.ai_insights import AIInsights
from ai.ai_service import HospitalAIService
from ai.system_health import SystemHealth
from tkinter import messagebox
import threading


class AICenter(ctk.CTkFrame):
    """Enterprise AI command center for operational intelligence."""
    def __init__(self, parent):
        super().__init__(parent, corner_radius=16)
        self.service = HospitalAIService()
        self.insights = AIInsights()
        self.health = SystemHealth()
        self._build()
        self.refresh()

    def _build(self):
        ctk.CTkLabel(self, text="🤖 AI Hospital Intelligence", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", padx=24, pady=(22, 2))
        ctk.CTkLabel(self, text="Operational intelligence, alerts and controlled AI assistance — not autonomous clinical decision-making.", text_color="gray").pack(anchor="w", padx=24, pady=(0, 16))

        self.metrics = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics.pack(fill="x", padx=20, pady=8)

        self.health_label = ctk.CTkLabel(self, text="System health: checking...", anchor="w")
        self.health_label.pack(fill="x", padx=24, pady=(8, 2))

        self.alert_box = ctk.CTkTextbox(self, height=180, wrap="word")
        self.alert_box.pack(fill="x", padx=24, pady=10)
        self.alert_box.configure(state="disabled")

        ctk.CTkLabel(self, text="Ask the AI Assistant", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=24, pady=(12, 4))
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=(0, 12))
        self.entry = ctk.CTkEntry(row, placeholder_text="Example: How many pending appointments are there?")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda _e: self.ask())
        self.ask_btn = ctk.CTkButton(row, text="Ask AI", width=110, command=self.ask)
        self.ask_btn.pack(side="right")

        self.answer = ctk.CTkTextbox(self, height=150, wrap="word")
        self.answer.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.answer.insert("end", "AI response will appear here.\n")
        self.answer.configure(state="disabled")

    def _metric(self, title, value):
        card = ctk.CTkFrame(self.metrics, corner_radius=12)
        card.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(card, text=title, text_color="gray").pack(pady=(12, 0))
        ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(3, 12))

    def refresh(self):
        for w in self.metrics.winfo_children(): w.destroy()
        data, insights = self.insights.build()
        for title, value in [("Patients", data['patients']), ("Doctors", data['active_doctors']), ("Today Appointments", data['today_appointments']), ("Pending Labs", data['lab_pending']), ("Low Stock", data['low_pharmacy_stock'] + data['low_inventory_stock']), ("Active IPD", data['ipd_active'])]:
            self._metric(title, value)
        self.alert_box.configure(state="normal")
        self.alert_box.delete("1.0", "end")
        for title, msg, action in insights:
            self.alert_box.insert("end", f"{title}: {msg}\nAction: {action}\n\n")
        self.alert_box.configure(state="disabled")
        health = self.health.check()
        mode = "LIVE AI configured" if health["api_configured"] else "Offline AI mode"
        status = "READY" if health["database"] and health["tables"] else "CHECK REQUIRED"
        self.health_label.configure(text=f"System health: {status}  •  Database: {'OK' if health['database'] else 'ERROR'}  •  Core tables: {'OK' if health['tables'] else 'ERROR'}  •  {mode}")

    def ask(self):
        q = self.entry.get().strip()
        if not q:
            messagebox.showinfo("AI Assistant", "Please enter a question.", parent=self.winfo_toplevel())
            return
        self.entry.delete(0, "end")
        self.ask_btn.configure(state="disabled", text="Thinking...")
        def worker():
            try: ans = self.service.ask(q)
            except Exception as e: ans = f"AI service error: {e}"
            self.after(0, lambda: self._show(ans))
        threading.Thread(target=worker, daemon=True).start()

    def _show(self, text):
        self.answer.configure(state="normal")
        self.answer.delete("1.0", "end")
        self.answer.insert("end", text)
        self.answer.configure(state="disabled")
        self.ask_btn.configure(state="normal", text="Ask AI")

    def destroy(self):
        for service in (self.service, self.insights):
            try: service.close()
            except Exception: pass
        super().destroy()
