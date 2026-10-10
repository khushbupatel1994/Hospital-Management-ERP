"""
===========================================================
Cloud Secure Hospital ERP
Module  : AI Intelligence Center
Version : 3.0
===========================================================

Features:
- Hospital operational metrics
- System health
- Operational alerts / insights
- AI Assistant
- Background AI processing
- Thread-safe SQLite usage
- UI updates on Tkinter main thread
- Safe service cleanup
===========================================================
"""

import threading
import customtkinter as ctk
from tkinter import messagebox

from ai.ai_insights import AIInsights
from ai.ai_service import HospitalAIService
from ai.system_health import SystemHealth


class AICenter(ctk.CTkFrame):

    """
    Enterprise AI command center.

    Important:
    HospitalAIService used for Ask AI is created inside the
    worker thread. This prevents SQLite objects created in
    the Tkinter/main thread from being reused by another
    thread.
    """

    # ======================================================
    # INITIALIZE
    # ======================================================

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=16
        )

        # --------------------------------------------------
        # Main-thread services
        # --------------------------------------------------

        self.insights = AIInsights()

        self.health = SystemHealth()

        # --------------------------------------------------
        # Do NOT create the AI service here for background
        # requests.
        #
        # It will be created inside worker().
        # --------------------------------------------------

        self.service = None

        # --------------------------------------------------
        # State
        # --------------------------------------------------

        self._destroyed = False

        self._worker_running = False

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        self._build()

        self.refresh()

    # ======================================================
    # BUILD UI
    # ======================================================

    def _build(self):

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ctk.CTkLabel(
            self,
            text="🤖 AI Hospital Intelligence",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=24,
            pady=(22, 2)
        )

        # --------------------------------------------------
        # Description
        # --------------------------------------------------

        ctk.CTkLabel(
            self,
            text=(
                "Operational intelligence, alerts and "
                "controlled AI assistance — not autonomous "
                "clinical decision-making."
            ),
            text_color="gray"
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 16)
        )

        # ==================================================
        # METRICS
        # ==================================================

        self.metrics = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.metrics.pack(
            fill="x",
            padx=20,
            pady=8
        )

        # ==================================================
        # HEALTH
        # ==================================================

        self.health_label = ctk.CTkLabel(
            self,
            text="System health: checking...",
            anchor="w"
        )

        self.health_label.pack(
            fill="x",
            padx=24,
            pady=(8, 2)
        )

        # ==================================================
        # ALERTS
        # ==================================================

        self.alert_box = ctk.CTkTextbox(
            self,
            height=180,
            wrap="word"
        )

        self.alert_box.pack(
            fill="x",
            padx=24,
            pady=10
        )

        self.alert_box.configure(
            state="disabled"
        )

        # ==================================================
        # AI TITLE
        # ==================================================

        ctk.CTkLabel(
            self,
            text="Ask the AI Assistant",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=24,
            pady=(12, 4)
        )

        # ==================================================
        # ASK ROW
        # ==================================================

        row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=24,
            pady=(0, 12)
        )

        # --------------------------------------------------
        # Question entry
        # --------------------------------------------------

        self.entry = ctk.CTkEntry(
            row,
            placeholder_text=(
                "Example: How many pending "
                "appointments are there?"
            )
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.entry.bind(
            "<Return>",
            lambda _event: self.ask()
        )

        # --------------------------------------------------
        # Ask button
        # --------------------------------------------------

        self.ask_btn = ctk.CTkButton(
            row,
            text="Ask AI",
            width=110,
            command=self.ask
        )

        self.ask_btn.pack(
            side="right"
        )

        # ==================================================
        # ANSWER
        # ==================================================

        self.answer = ctk.CTkTextbox(
            self,
            height=150,
            wrap="word"
        )

        self.answer.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 20)
        )

        self.answer.insert(
            "end",
            "AI response will appear here.\n"
        )

        self.answer.configure(
            state="disabled"
        )

    # ======================================================
    # METRIC CARD
    # ======================================================

    def _metric(
        self,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self.metrics,
            corner_radius=12
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="gray"
        ).pack(
            pady=(12, 0)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(3, 12)
        )

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh(self):

        if self._destroyed:

            return

        try:

            # ------------------------------------------------
            # Clear metrics
            # ------------------------------------------------

            for widget in (
                self.metrics.winfo_children()
            ):

                widget.destroy()

            # ------------------------------------------------
            # Build operational insights
            # ------------------------------------------------

            data, insights = (
                self.insights.build()
            )

            # ------------------------------------------------
            # Metrics
            # ------------------------------------------------

            metric_data = [

                (
                    "Patients",
                    data.get(
                        "patients",
                        0
                    )
                ),

                (
                    "Doctors",
                    data.get(
                        "active_doctors",
                        0
                    )
                ),

                (
                    "Today Appointments",
                    data.get(
                        "today_appointments",
                        0
                    )
                ),

                (
                    "Pending Labs",
                    data.get(
                        "lab_pending",
                        0
                    )
                ),

                (
                    "Low Stock",
                    (
                        data.get(
                            "low_pharmacy_stock",
                            0
                        )
                        +
                        data.get(
                            "low_inventory_stock",
                            0
                        )
                    )
                ),

                (
                    "Active IPD",
                    data.get(
                        "ipd_active",
                        0
                    )
                )
            ]

            for title, value in metric_data:

                self._metric(
                    title,
                    value
                )

            # ------------------------------------------------
            # Alerts
            # ------------------------------------------------

            self.alert_box.configure(
                state="normal"
            )

            self.alert_box.delete(
                "1.0",
                "end"
            )

            if insights:

                for title, msg, action in insights:

                    self.alert_box.insert(
                        "end",
                        (
                            f"{title}: {msg}\n"
                            f"Action: {action}\n\n"
                        )
                    )

            else:

                self.alert_box.insert(
                    "end",
                    "No operational alerts.\n"
                )

            self.alert_box.configure(
                state="disabled"
            )

            # ------------------------------------------------
            # System Health
            # ------------------------------------------------

            health = (
                self.health.check()
            )

            api_configured = bool(
                health.get(
                    "api_configured",
                    False
                )
            )

            database_ok = bool(
                health.get(
                    "database",
                    False
                )
            )

            tables_ok = bool(
                health.get(
                    "tables",
                    False
                )
            )

            mode = (
                "LIVE AI configured"
                if api_configured
                else
                "Offline AI mode"
            )

            status = (
                "READY"
                if database_ok
                and tables_ok
                else
                "CHECK REQUIRED"
            )

            self.health_label.configure(
                text=(
                    f"System health: {status}"
                    f"  •  Database: "
                    f"{'OK' if database_ok else 'ERROR'}"
                    f"  •  Core tables: "
                    f"{'OK' if tables_ok else 'ERROR'}"
                    f"  •  {mode}"
                )
            )

        except Exception as e:

            print(
                "AI Center Refresh Error:",
                e
            )

            try:

                self.health_label.configure(
                    text=(
                        "System health: ERROR"
                        f"  •  {e}"
                    )
                )

            except Exception:
                pass

    # ======================================================
    # ASK AI
    # ======================================================

    def ask(self):

        if self._destroyed:

            return

        # --------------------------------------------------
        # Prevent duplicate requests
        # --------------------------------------------------

        if self._worker_running:

            return

        # --------------------------------------------------
        # Get question
        # --------------------------------------------------

        try:

            question = (
                self.entry
                .get()
                .strip()
            )

        except Exception as e:

            print(
                "Question Read Error:",
                e
            )

            return

        # --------------------------------------------------
        # Empty question
        # --------------------------------------------------

        if not question:

            messagebox.showinfo(
                "AI Assistant",
                "Please enter a question.",
                parent=self.winfo_toplevel()
            )

            return

        # --------------------------------------------------
        # Clear input
        # --------------------------------------------------

        try:

            self.entry.delete(
                0,
                "end"
            )

        except Exception:
            pass

        # --------------------------------------------------
        # Disable button
        # --------------------------------------------------

        self._worker_running = True

        try:

            self.ask_btn.configure(
                state="disabled",
                text="Thinking..."
            )

        except Exception:
            pass

        # ==================================================
        # BACKGROUND WORKER
        # ==================================================

        def worker():

            local_service = None

            answer = None

            try:

                print(
                    "🤖 AI Worker Started"
                )

                # ------------------------------------------------
                # CRITICAL FIX:
                #
                # Create HospitalAIService INSIDE this worker
                # thread, so any SQLite connection created by
                # the service belongs to this same thread.
                # ------------------------------------------------

                local_service = (
                    HospitalAIService()
                )

                answer = (
                    local_service.ask(
                        question
                    )
                )

                if answer is None:

                    answer = (
                        "AI returned no response."
                    )

                answer = str(
                    answer
                )

                print(
                    "✅ AI Worker Completed"
                )

            except Exception as e:

                print(
                    "❌ AI Worker Error:",
                    e
                )

                answer = (
                    "AI service error:\n"
                    f"{e}"
                )

            finally:

                # ------------------------------------------------
                # Close only the service created by this thread.
                # ------------------------------------------------

                if local_service is not None:

                    try:

                        local_service.close()

                    except Exception as e:

                        print(
                            "AI Worker Service Close Error:",
                            e
                        )

                # ------------------------------------------------
                # Return to Tkinter main thread.
                # ------------------------------------------------

                try:

                    if not self._destroyed:

                        self.after(
                            0,
                            lambda result=answer:
                                self._show(
                                    result
                                )
                        )

                except Exception as e:

                    print(
                        "AI UI Callback Error:",
                        e
                    )

        # ==================================================
        # START THREAD
        # ==================================================

        try:

            threading.Thread(
                target=worker,
                daemon=True
            ).start()

        except Exception as e:

            self._worker_running = False

            try:

                self.ask_btn.configure(
                    state="normal",
                    text="Ask AI"
                )

            except Exception:
                pass

            messagebox.showerror(
                "AI Assistant",
                f"Unable to start AI worker.\n\n{e}",
                parent=self.winfo_toplevel()
            )

    # ======================================================
    # SHOW AI ANSWER
    # ======================================================

    def _show(
        self,
        text
    ):

        if self._destroyed:

            return

        try:

            self.answer.configure(
                state="normal"
            )

            self.answer.delete(
                "1.0",
                "end"
            )

            self.answer.insert(
                "end",
                str(
                    text
                )
            )

            self.answer.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "AI Answer Display Error:",
                e
            )

        finally:

            self._worker_running = False

            try:

                self.ask_btn.configure(
                    state="normal",
                    text="Ask AI"
                )

            except Exception:
                pass

    # ======================================================
    # CLEAR AI ANSWER
    # ======================================================

    def clear_answer(self):

        if self._destroyed:

            return

        try:

            self.answer.configure(
                state="normal"
            )

            self.answer.delete(
                "1.0",
                "end"
            )

            self.answer.insert(
                "end",
                "AI response will appear here.\n"
            )

            self.answer.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "Clear AI Answer Error:",
                e
            )

    # ======================================================
    # DESTROY
    # ======================================================

    def destroy(self):

        # --------------------------------------------------
        # Mark destroyed first
        # --------------------------------------------------

        self._destroyed = True

        # --------------------------------------------------
        # Disable worker completion from updating UI
        # --------------------------------------------------

        self._worker_running = False

        # --------------------------------------------------
        # NOTE:
        #
        # self.service is normally None because AI service
        # is created per worker thread.
        #
        # We intentionally do NOT try to close a worker's
        # SQLite connection from the Tkinter thread.
        # --------------------------------------------------

        if self.service is not None:

            try:

                self.service.close()

            except Exception as e:

                print(
                    "AI Service Close Error:",
                    e
                )

            self.service = None

        # --------------------------------------------------
        # Close insights
        # --------------------------------------------------

        if self.insights is not None:

            try:

                self.insights.close()

            except Exception as e:

                print(
                    "AI Insights Close Error:",
                    e
                )

            self.insights = None

        # --------------------------------------------------
        # Parent destroy
        # --------------------------------------------------

        super().destroy()