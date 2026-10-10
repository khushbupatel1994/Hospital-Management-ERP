import threading
import customtkinter as ctk
from tkinter import messagebox
from .ai_service import HospitalAIService


class AIAssistant(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=16)
        self.service = HospitalAIService()
        self._build()

    def _build(self):
        title = ctk.CTkLabel(self, text="🤖 AI Hospital Assistant", font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(anchor="w", padx=24, pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Ask about hospital operations, appointments, laboratory workload, inventory and billing summaries.",
            text_color="gray",
        )
        subtitle.pack(anchor="w", padx=24, pady=(0, 16))

        self.chat = ctk.CTkTextbox(self, height=430, wrap="word")
        self.chat.pack(fill="both", expand=True, padx=24, pady=8)
        self.chat.insert("end", "AI: Hello! I can help with hospital ERP summaries.\n\n")
        self.chat.configure(state="disabled")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=(8, 24))

        self.entry = ctk.CTkEntry(row, placeholder_text="Example: How many pending appointments are there?")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda _event: self.ask())

        self.ask_button = ctk.CTkButton(row, text="Ask AI", width=110, command=self.ask)
        self.ask_button.pack(side="right")

    def _append(self, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", text + "\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def ask(self):
        question = self.entry.get().strip()
        if not question:
            messagebox.showinfo("AI Assistant", "Please enter a question.", parent=self.winfo_toplevel())
            return

        self.entry.delete(0, "end")
        self._append("You: " + question)
        self.ask_button.configure(state="disabled", text="Thinking...")

        def worker():
            try:
                answer = self.service.ask(question)
            except Exception as exc:
                answer = f"AI error: {exc}"

            self.after(0, lambda: self._finish(answer))

        threading.Thread(target=worker, daemon=True).start()

    def _finish(self, answer):
        self._append("AI: " + answer)
        self.ask_button.configure(state="normal", text="Ask AI")

    def destroy(self):
        try:
            self.service.close()
        except Exception:
            pass
        super().destroy()
