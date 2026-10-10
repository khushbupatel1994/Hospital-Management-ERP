import os
from PIL import Image
import customtkinter as ctk
from config.paths import resource_path


class LoginUI:

    def __init__(self, root):

        self.root = root

        # ==========================================
        # Window
        # ==========================================

        self.root.title("Cloud Secure Hospital ERP")

        self.root.configure(
            fg_color="#F4F7FB"
        )

        self.create_widgets()

    # ==========================================
    # Create Login Screen
    # ==========================================

    def create_widgets(self):

        # ==========================================
        # Main Container
        # ==========================================

        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#D9E2EC"
        )

        self.main_frame.pack(
            expand=True,
            padx=40,
            pady=40
        )

        # ==========================================
        # LEFT SIDE - Hospital Image
        # ==========================================

        self.left_frame = ctk.CTkFrame(
            self.main_frame,
            width=560,
            height=650,
            corner_radius=18,
            fg_color="#EAF4FF"
        )

        self.left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 5),
            pady=10
        )

        self.left_frame.pack_propagate(False)

        # ------------------------------------------
        # Hospital Image
        # ------------------------------------------

        image_path = resource_path("assets", "hospital_login.png")

        if os.path.exists(image_path):

            self.hospital_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(450, 450)
            )

            self.hospital_image_label = ctk.CTkLabel(
                self.left_frame,
                image=self.hospital_image,
                text=""
            )

            self.hospital_image_label.pack(
                pady=(45, 10)
            )

        else:

            self.hospital_image_label = ctk.CTkLabel(
                self.left_frame,
                text="🏥",
                font=("Segoe UI", 100)
            )

            self.hospital_image_label.pack(
                pady=(100, 20)
            )

        # ------------------------------------------
        # Hospital Name
        # ------------------------------------------

        self.hospital_name = ctk.CTkLabel(
            self.left_frame,
            text="CLOUD SECURE",
            font=("Segoe UI", 28, "bold"),
            text_color="#1565C0"
        )

        self.hospital_name.pack(
            pady=(5, 2)
        )

        self.hospital_title = ctk.CTkLabel(
            self.left_frame,
            text="HOSPITAL ERP",
            font=("Segoe UI", 22, "bold"),
            text_color="#263238"
        )

        self.hospital_title.pack(
            pady=(0, 10)
        )

        self.hospital_subtitle = ctk.CTkLabel(
            self.left_frame,
            text="Hospital Management & Accounting ERP",
            font=("Segoe UI", 13),
            text_color="#607D8B"
        )

        self.hospital_subtitle.pack()

        # ==========================================
        # RIGHT SIDE - LOGIN
        # ==========================================

        self.login_frame = ctk.CTkFrame(
            self.main_frame,
            width=500,
            height=650,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        self.login_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(5, 10),
            pady=10
        )

        self.login_frame.pack_propagate(False)

        # ==========================================
        # Login Icon
        # ==========================================

        self.login_icon = ctk.CTkLabel(
            self.login_frame,
            text="🔐",
            font=("Segoe UI Emoji", 48)
        )

        self.login_icon.pack(
            pady=(45, 5)
        )

        # ==========================================
        # Title
        # ==========================================

        self.title = ctk.CTkLabel(
            self.login_frame,
            text="Welcome Back",
            font=("Segoe UI", 30, "bold"),
            text_color="#172B4D"
        )

        self.title.pack(
            pady=(5, 5)
        )

        # ==========================================
        # Subtitle
        # ==========================================

        self.subtitle = ctk.CTkLabel(
            self.login_frame,
            text="Login to Continue",
            font=("Segoe UI", 15),
            text_color="#607D8B"
        )

        self.subtitle.pack(
            pady=(0, 25)
        )

        # ==========================================
        # Username
        # ==========================================

        self.username = ctk.CTkEntry(
            self.login_frame,
            width=360,
            height=45,
            corner_radius=8,
            placeholder_text="Username",
            font=("Segoe UI", 14)
        )

        self.username.pack(
            pady=10
        )

        # ==========================================
        # Password
        # ==========================================

        self.password = ctk.CTkEntry(
            self.login_frame,
            width=360,
            height=45,
            corner_radius=8,
            placeholder_text="Password",
            show="*",
            font=("Segoe UI", 14)
        )

        self.password.pack(
            pady=10
        )

        # ==========================================
        # Show Password
        # ==========================================

        self.show_password = ctk.BooleanVar(
            value=False
        )

        self.show_password_checkbox = ctk.CTkCheckBox(
            self.login_frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            font=("Segoe UI", 13)
        )

        self.show_password_checkbox.pack(
            anchor="w",
            padx=70,
            pady=(5, 8)
        )

        # ==========================================
        # Remember Me
        # ==========================================

        self.remember_me = ctk.BooleanVar(
            value=False
        )

        self.remember_checkbox = ctk.CTkCheckBox(
            self.login_frame,
            text="Remember Me",
            variable=self.remember_me,
            font=("Segoe UI", 13)
        )

        self.remember_checkbox.pack(
            anchor="w",
            padx=70,
            pady=(0, 15)
        )

        # ==========================================
        # Login Button
        # ==========================================

        self.login_btn = ctk.CTkButton(
            self.login_frame,
            text="🔐  Login",
            width=360,
            height=48,
            corner_radius=8,
            fg_color="#1976D2",
            hover_color="#0D47A1",
            font=("Segoe UI", 15, "bold")
        )

        self.login_btn.pack(
            pady=10
        )

        # ==========================================
        # Forgot Buttons Frame
        # ==========================================

        self.bottom_frame = ctk.CTkFrame(
            self.login_frame,
            fg_color="transparent"
        )

        self.bottom_frame.pack(
            pady=(12, 5)
        )

        # ==========================================
        # Forgot User ID
        # ==========================================

        self.forgot_user_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Forgot User ID?",
            width=155,
            height=32,
            fg_color="transparent",
            hover_color="#E3F2FD",
            text_color="#1976D2",
            font=("Segoe UI", 12, "bold")
        )

        self.forgot_user_btn.grid(
            row=0,
            column=0,
            padx=3
        )

        # ==========================================
        # Forgot Password
        # ==========================================

        self.forgot_pass_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Forgot Password?",
            width=155,
            height=32,
            fg_color="transparent",
            hover_color="#E3F2FD",
            text_color="#1976D2",
            font=("Segoe UI", 12, "bold")
        )

        self.forgot_pass_btn.grid(
            row=0,
            column=1,
            padx=3
        )

        # ==========================================
        # Separator
        # ==========================================

        self.separator = ctk.CTkLabel(
            self.login_frame,
            text="────────────────────────",
            text_color="#CFD8DC"
        )

        self.separator.pack(
            pady=(10, 5)
        )

        # ==========================================
        # Exit Button
        # ==========================================

        self.exit_btn = ctk.CTkButton(
            self.login_frame,
            text="Exit",
            width=360,
            height=42,
            corner_radius=8,
            fg_color="#E53935",
            hover_color="#B71C1C",
            font=("Segoe UI", 14, "bold"),
            command=self.root.destroy
        )

        self.exit_btn.pack(
            pady=(5, 15)
        )

        # ==========================================
        # Version
        # ==========================================

        self.version_label = ctk.CTkLabel(
            self.login_frame,
            text="Cloud Secure Hospital ERP  •  Version 2.0",
            font=("Segoe UI", 11),
            text_color="#90A4AE"
        )

        self.version_label.pack(
            pady=(0, 5)
        )

    # ==========================================
    # Show / Hide Password
    # ==========================================

    def toggle_password(self):

        if self.show_password.get():

            self.password.configure(
                show=""
            )

        else:

            self.password.configure(
                show="*"
            )