"""
===========================================================
Cloud Secure Hospital ERP
Login Controller
===========================================================
"""

import json
import os
from tkinter import messagebox

import customtkinter as ctk

from frontend.login.login_ui import LoginUI
from frontend.login.login_service import LoginService
from frontend.login.login_crud import LoginCRUD
from frontend.dashboard.admin_dashboard import AdminDashboard
from config.paths import CONFIG_DIR
from frontend.license.license_manager import LicenseManager
from frontend.license.license_gate import LicenseGate
from server.client import ERPApiClient


class LoginApp(LoginUI):

    def __init__(self, root):

        super().__init__(root)

        self.root = root

        self.service = LoginService()

        self.crud = LoginCRUD()

        # Central API Client
        self.api_client = ERPApiClient(
            base_url=os.getenv(
                "ERP_API_URL",
                "http://192.168.31.88:8000"
            ),
            api_key=os.getenv(
                "ERP_API_KEY",
                ""
            )
        )

        # License Manager
        self.license_manager = LicenseManager()

        # Remember Me File
        self.remember_file = os.path.join(CONFIG_DIR, "login.json")
        self.login_history_id = None

        # Buttons
        self.login_btn.configure(
            command=self.login
        )

        self.forgot_user_btn.configure(
            command=self.forgot_user_id
        )

        self.forgot_pass_btn.configure(
            command=self.forgot_password
        )

        # Load Remember Me
        self.load_remember_me()

    # ==================================================
    # Login
    # ==================================================

    def login(self):

        username = self.username.get().strip()

        password = self.password.get().strip()

        if not self.service.validate_input(
            username,
            password
        ):
            return

        try:
            api_result = self.api_client.login(
                username,
                password
            )

            api_user = api_result.get("user", {})

            # Keep compatibility with existing dashboard/modules
            # that currently expect the old users-table tuple.
            user = (
                api_user.get("id", 0),
                api_user.get("employee_id", ""),
                api_user.get(
                    "name",
                    api_user.get("full_name", "")
                ),
                api_user.get("username", username),
                None,
                api_user.get("role", ""),
                api_user.get("department", ""),
                api_user.get("mobile", ""),
                api_user.get("email", ""),
                api_user.get("security_question", ""),
                api_user.get("security_answer", ""),
                api_user.get("status", "Active"),
                api_user.get("last_login", ""),
                api_user.get("created_at", ""),
                api_user.get("failed_attempts", 0),
                api_user.get("account_locked", 0)
            )

        except Exception as e:
            print("API Login Error:", e)
            messagebox.showerror(
                "Login Failed",
                "Unable to login to the hospital server."
            )
            return

        if user == "LOCKED":
            messagebox.showerror(
                "Account Locked",
                "This account is locked after too many failed attempts."
            )
            return

        if user:

            # ==================================================
            # LICENSE CHECK
            # ==================================================

            license_result = self.license_manager.validate_license()

            if not license_result.get("valid"):
                print(
                    "❌ License Blocked:",
                    license_result.get("status")
                )

                gate = LicenseGate(self.root)
                gate.show_license_window(license_result)
                return

            print(
                "✅ License Active | "
                f"Customer={license_result.get('customer_name')} | "
                f"Expiry={license_result.get('expiry_date')} | "
                f"Remaining={license_result.get('remaining_days')} days"
            )

            # Save Remember Me
            self.save_remember_me()

            messagebox.showinfo(
                "Success",
                f"Welcome {user[2]}"
            )

            # Remove Login Screen
            for widget in self.root.winfo_children():

                widget.destroy()

            self.root.update_idletasks()

            # Open Dashboard
            AdminDashboard(
                self.root,
                user,
                login_history_id=None,
                api_client=self.api_client
            )

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password"
            )

    # ==================================================
    # License Block / Activation Window
    # ==================================================

    def show_license_block(self, result):
        gate = LicenseGate(self.root)
        gate.show_license_window(result)

    # ==================================================
    # Remember Me Save
    # ==================================================

    def save_remember_me(self):

        if not hasattr(self, "remember_me"):
            return

        os.makedirs(CONFIG_DIR, exist_ok=True)

        if self.remember_me.get():

            data = {

                "remember": True,

                "username": self.username.get()

            }

        else:

            data = {

                "remember": False,

                "username": ""

            }

        with open(
            self.remember_file,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # ==================================================
    # Load Remember Me
    # ==================================================

    def load_remember_me(self):

        if not os.path.exists(
            self.remember_file
        ):
            return

        with open(
            self.remember_file,
            "r"
        ) as file:

            data = json.load(file)

        if data.get("remember"):

            self.username.insert(
                0,
                data.get("username")
            )

            self.remember_me.set(True)

    # ==================================================
    # Forgot User ID
    # ==================================================

    def forgot_user_id(self):

        win = ctk.CTkToplevel(self.root)
        win.title("Forgot User ID")
        win.geometry("450x350")
        win.resizable(False, False)

        ctk.CTkLabel(
            win,
            text="Forgot User ID",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            win,
            text="Enter your registered Mobile Number and Email"
        ).pack(pady=5)

        mobile = ctk.CTkEntry(
            win,
            width=320,
            placeholder_text="Mobile Number"
        )
        mobile.pack(pady=10)

        email = ctk.CTkEntry(
            win,
            width=320,
            placeholder_text="Email Address"
        )
        email.pack(pady=10)

        def find_user():

            mobile_value = mobile.get().strip()
            email_value = email.get().strip()

            if not mobile_value or not email_value:
                messagebox.showwarning(
                    "Required",
                    "Please enter Mobile Number and Email.",
                    parent=win
                )
                return

            result = self.crud.forgot_user_id(
                mobile_value,
                email_value
            )

            if result:

                username = result[0]

                messagebox.showinfo(
                    "User ID Found",
                    f"Your User ID is:\n\n{username}",
                    parent=win
                )

                win.destroy()

            else:

                messagebox.showerror(
                    "Not Found",
                    "No account found with these details.",
                    parent=win
                )

        ctk.CTkButton(
            win,
            text="Find User ID",
            width=320,
            height=40,
            command=find_user
        ).pack(pady=20)
    # ==================================================
    # Forgot Password
    # ==================================================

    def forgot_password(self):

        win = ctk.CTkToplevel(self.root)
        win.title("Forgot Password")
        win.geometry("500x600")
        win.resizable(False, False)

        ctk.CTkLabel(
            win,
            text="Forgot Password",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            win,
            text="Verify your account to reset password"
        ).pack(pady=5)

        username = ctk.CTkEntry(
            win,
            width=350,
            placeholder_text="Username"
        )
        username.pack(pady=10)

        question_label = ctk.CTkLabel(
            win,
            text="Security Question will appear here",
            wraplength=400
        )
        question_label.pack(pady=15)

        answer = ctk.CTkEntry(
            win,
            width=350,
            placeholder_text="Security Answer"
        )
        answer.pack(pady=10)

        new_password = ctk.CTkEntry(
            win,
            width=350,
            placeholder_text="New Password",
            show="*"
        )
        new_password.pack(pady=10)

        confirm_password = ctk.CTkEntry(
            win,
            width=350,
            placeholder_text="Confirm New Password",
            show="*"
        )
        confirm_password.pack(pady=10)

        def load_question():

            username_value = username.get().strip()

            if not username_value:
                messagebox.showwarning(
                    "Required",
                    "Please enter your Username.",
                    parent=win
                )
                return

            user = self.crud.get_user(
                username_value
            )

            if not user:
                messagebox.showerror(
                    "Not Found",
                    "Username not found.",
                    parent=win
                )
                return

            question = user[9]

            if not question:
                messagebox.showerror(
                    "Security Question",
                    "Security question is not configured for this account.",
                    parent=win
                )
                return

            question_label.configure(
                text=f"Security Question:\n{question}"
            )

        def reset_password():

            username_value = username.get().strip()
            answer_value = answer.get().strip()
            new_password_value = new_password.get().strip()
            confirm_value = confirm_password.get().strip()

            if not username_value:
                messagebox.showwarning(
                    "Required",
                    "Please enter Username.",
                    parent=win
                )
                return

            if not answer_value:
                messagebox.showwarning(
                    "Required",
                    "Please enter Security Answer.",
                    parent=win
                )
                return

            if not new_password_value:
                messagebox.showwarning(
                    "Required",
                    "Please enter New Password.",
                    parent=win
                )
                return

            if len(new_password_value) < 6:
                messagebox.showwarning(
                    "Password",
                    "Password must be at least 6 characters.",
                    parent=win
                )
                return

            if new_password_value != confirm_value:
                messagebox.showerror(
                    "Password",
                    "New Password and Confirm Password do not match.",
                    parent=win
                )
                return

            user = self.crud.get_user(
                username_value
            )

            if not user:
                messagebox.showerror(
                    "Error",
                    "Username not found.",
                    parent=win
                )
                return

            question = user[9]

            verified = self.crud.verify_security(
                username_value,
                question,
                answer_value
            )

            if not verified:
                messagebox.showerror(
                    "Verification Failed",
                    "Incorrect security answer.",
                    parent=win
                )
                return

            success = self.crud.update_password(
                username_value,
                new_password_value
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Password reset successfully.\n\nYou can now login with your new password.",
                    parent=win
                )

                win.destroy()

        ctk.CTkButton(
            win,
            text="Get Security Question",
            width=350,
            height=40,
            command=load_question
        ).pack(pady=15)

        ctk.CTkButton(
            win,
            text="Reset Password",
            width=350,
            height=40,
            command=reset_password
        ).pack(pady=20)
