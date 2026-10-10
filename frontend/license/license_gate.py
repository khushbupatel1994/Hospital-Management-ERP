"""
Cloud Secure Hospital ERP
License Gate UI
"""

import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

from .license_manager import LicenseManager


class LicenseGate:
    def __init__(self, root):
        self.root = root
        self.manager = LicenseManager()

    def check(self):
        result = self.manager.validate_license()
        print(f"🔐 License Status: {result.get('status')}")
        if result.get("valid"):
            print(
                f"✅ License Active | Customer={result.get('customer_name')} | "
                f"Expiry={result.get('expiry_date')} | "
                f"Remaining={result.get('remaining_days')} days"
            )
            return True

        self.show_license_window(result)
        return False

    def show_license_window(self, result=None):
        result = result or {}

        win = ctk.CTkToplevel(self.root)
        win.title("Cloud Secure Hospital ERP - License")
        win.geometry("620x520")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", self._close_all)
        win.grab_set()
        win.focus_force()

        status = result.get("status", "MISSING")
        title_text = "LICENSE EXPIRED" if status == "EXPIRED" else "LICENSE REQUIRED"

        ctk.CTkLabel(
            win,
            text=title_text,
            font=("Segoe UI", 28, "bold"),
        ).pack(pady=(35, 10))

        ctk.CTkLabel(
            win,
            text=(
                "Your Cloud Secure Hospital ERP license is not active.\n\n"
                f"Customer: {result.get('customer_name', 'Not activated')}\n"
                f"Expiry: {result.get('expiry_date', 'N/A')}\n\n"
                "Please import the renewal/activation license file provided by your developer."
            ),
            font=("Segoe UI", 14),
            justify="center",
            wraplength=520,
        ).pack(pady=10)

        path_var = ctk.StringVar(value="")

        entry = ctk.CTkEntry(
            win,
            width=450,
            height=42,
            textvariable=path_var,
            placeholder_text="Select license.key file",
        )
        entry.pack(pady=(20, 8))

        def browse():
            path = filedialog.askopenfilename(
                parent=win,
                title="Select License File",
                filetypes=[("License File", "*.key"), ("JSON", "*.json")],
            )
            if path:
                path_var.set(path)

        def activate():
            path = path_var.get().strip()
            if not path or not os.path.isfile(path):
                messagebox.showwarning(
                    "License",
                    "Please select a valid license file.",
                    parent=win,
                )
                return

            try:
                data = self.manager.load_license(path)
                result2 = self.manager.validate_license_data(data)
                if not result2["valid"]:
                    raise ValueError(result2["message"])

                self.manager.save_license(data)

                messagebox.showinfo(
                    "License Activated",
                    (
                        "License activated successfully.\n\n"
                        f"Customer: {result2['customer_name']}\n"
                        f"Expiry: {result2['expiry_date']}\n"
                        f"Remaining: {result2['remaining_days']} days"
                    ),
                    parent=win,
                )

                win.grab_release()
                win.destroy()

                # Restart the application cleanly so the login screen is rebuilt.
                self.root.after(100, self.root.destroy)

            except Exception as exc:
                messagebox.showerror(
                    "License Error",
                    str(exc),
                    parent=win,
                )

        ctk.CTkButton(
            win,
            text="Browse License File",
            width=300,
            height=42,
            command=browse,
        ).pack(pady=8)

        ctk.CTkButton(
            win,
            text="Activate License",
            width=300,
            height=46,
            command=activate,
        ).pack(pady=8)

        ctk.CTkButton(
            win,
            text="Exit Software",
            width=300,
            height=42,
            fg_color="gray",
            hover_color="#555555",
            command=self._close_all,
        ).pack(pady=(18, 5))

        ctk.CTkLabel(
            win,
            text="License management is controlled by the software developer.",
            font=("Segoe UI", 11),
        ).pack(pady=(10, 0))

    def _close_all(self):
        try:
            self.root.destroy()
        except Exception:
            pass
