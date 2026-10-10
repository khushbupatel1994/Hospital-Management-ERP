import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from PIL import Image

class HRUI:

    def __init__(self, root):

        self.root = root

        self.create_widgets()

    # ==========================================
    # Main UI
    # ==========================================

    def create_widgets(self):

        self.main = ctk.CTkFrame(
            self.root,
            corner_radius=10
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Header
        # ==========================================

        self.header = ctk.CTkFrame(
            self.main,
            height=70
        )

        self.header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header,
            text="👨‍💼 HR & Employee Management",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=20
        )

        # Search

        self.search_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        self.search_frame.pack(
            side="right",
            padx=20
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=250,
            placeholder_text="Search Employee..."
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100
        )

        self.search_btn.pack(
            side="left",
            padx=5
        )

        # ==========================================
        # Body
        # ==========================================

        self.body = ctk.CTkFrame(
            self.main
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Left Form
        # ==========================================

        self.left = ctk.CTkScrollableFrame(
            self.body,
            width=420
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=False,
            padx=(0, 10)
        )

        ctk.CTkLabel(
            self.left,
            text="Employee Information",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        # ==========================================
        # Employee ID
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Employee ID"
        ).pack(anchor="w", padx=20)

        self.employee_id = ctk.CTkEntry(
            self.left,
            placeholder_text="Auto Generated",
            state="disabled"
        )

        self.employee_id.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Full Name
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Full Name"
        ).pack(anchor="w", padx=20)

        self.full_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Employee Name"
        )

        self.full_name.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Father Name
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Father / Husband Name"
        ).pack(anchor="w", padx=20)

        self.father_name = ctk.CTkEntry(
            self.left,
            placeholder_text="Father / Husband Name"
        )

        self.father_name.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Gender
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Gender"
        ).pack(anchor="w", padx=20)

        self.gender = ctk.CTkComboBox(
            self.left,
            values=[
                "Male",
                "Female",
                "Other"
            ]
        )

        self.gender.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.gender.set("Male")

        # ==========================================
        # DOB
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Date of Birth"
        ).pack(anchor="w", padx=20)

        self.dob = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            width=20
        )

        self.dob.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Blood Group
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Blood Group"
        ).pack(anchor="w", padx=20)

        self.blood_group = ctk.CTkComboBox(
            self.left,
            values=[
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )

        self.blood_group.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.blood_group.set("O+")

        # ==========================================
        # Marital Status
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Marital Status"
        ).pack(anchor="w", padx=20)

        self.marital_status = ctk.CTkComboBox(
            self.left,
            values=[
                "Single",
                "Married",
                "Divorced",
                "Widowed"
            ]
        )

        self.marital_status.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.marital_status.set("Single")

        # ==========================================
        # Mobile
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Mobile"
        ).pack(anchor="w", padx=20)

        self.mobile = ctk.CTkEntry(
            self.left,
            placeholder_text="Mobile Number"
        )

        self.mobile.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Email
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Email"
        ).pack(anchor="w", padx=20)

        self.email = ctk.CTkEntry(
            self.left,
            placeholder_text="Email Address"
        )

        self.email.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Address
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Address"
        ).pack(anchor="w", padx=20)

        self.address = ctk.CTkTextbox(
            self.left,
            height=80
        )

        self.address.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # City
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="City"
        ).pack(anchor="w", padx=20)

        self.city = ctk.CTkEntry(
            self.left,
            placeholder_text="City"
        )

        self.city.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # State
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="State"
        ).pack(anchor="w", padx=20)

        self.state = ctk.CTkEntry(
            self.left,
            placeholder_text="State"
        )

        self.state.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # PIN Code
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="PIN Code"
        ).pack(anchor="w", padx=20)

        self.pincode = ctk.CTkEntry(
            self.left,
            placeholder_text="PIN Code"
        )

        self.pincode.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Department
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Department"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.left,
            values=[
                "Administration",
                "Accounts",
                "HR",
                "Nursing",
                "Pharmacy",
                "Laboratory",
                "Reception",
                "IT",
                "Housekeeping",
                "Security"
            ]
        )

        self.department.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.department.set("Administration")

        # ==========================================
        # Designation
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Designation"
        ).pack(anchor="w", padx=20)

        self.designation = ctk.CTkEntry(
            self.left,
            placeholder_text="Designation"
        )

        self.designation.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Joining Date
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Joining Date"
        ).pack(anchor="w", padx=20)

        self.joining_date = DateEntry(
            self.left,
            date_pattern="dd-mm-yyyy",
            width=20
        )

        self.joining_date.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Employment Type
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Employment Type"
        ).pack(anchor="w", padx=20)

        self.employment_type = ctk.CTkComboBox(
            self.left,
            values=[
                "Full Time",
                "Part Time",
                "Contract",
                "Intern",
                "Temporary"
            ]
        )

        self.employment_type.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.employment_type.set("Full Time")

        # ==========================================
        # Basic Salary
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Basic Salary"
        ).pack(anchor="w", padx=20)

        self.basic_salary = ctk.CTkEntry(
            self.left,
            placeholder_text="Basic Salary"
        )

        self.basic_salary.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Shift
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Shift"
        ).pack(anchor="w", padx=20)

        self.shift = ctk.CTkComboBox(
            self.left,
            values=[
                "Morning",
                "Afternoon",
                "Evening",
                "Night",
                "General"
            ]
        )

        self.shift.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.shift.set("General")

        # ==========================================
        # Status
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Status"
        ).pack(anchor="w", padx=20)

        self.status = ctk.CTkComboBox(
            self.left,
            values=[
                "Active",
                "Inactive",
                "On Leave",
                "Resigned",
                "Terminated"
            ]
        )

        self.status.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.status.set("Active")

        # ==========================================
        # Aadhaar
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Aadhaar Number"
        ).pack(anchor="w", padx=20)

        self.aadhaar_no = ctk.CTkEntry(
            self.left,
            placeholder_text="Aadhaar Number"
        )

        self.aadhaar_no.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # PAN
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="PAN Number"
        ).pack(anchor="w", padx=20)

        self.pan_no = ctk.CTkEntry(
            self.left,
            placeholder_text="PAN Number"
        )

        self.pan_no.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Qualification
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Qualification"
        ).pack(anchor="w", padx=20)

        self.qualification = ctk.CTkEntry(
            self.left,
            placeholder_text="Qualification"
        )

        self.qualification.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Experience
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Experience"
        ).pack(anchor="w", padx=20)

        self.experience = ctk.CTkEntry(
            self.left,
            placeholder_text="Years / Experience"
        )

        self.experience.pack(
            fill="x",
            padx=20,
            pady=5
        )
        # ==========================================
        # Employee Photo
        # ==========================================

        self.photo_path = ""

        self.photo_label = ctk.CTkLabel(
            self.left,
            text="No Photo",
            width=180,
            height=180,
            fg_color=("gray85", "gray20"),
            corner_radius=10
        )

        self.photo_label.pack(
            padx=20,
            pady=10
        )

        self.photo_btn = ctk.CTkButton(
            self.left,
            text="📷 Choose Photo",
            command=self.choose_photo
        )

        self.photo_btn.pack(
            padx=20,
            pady=10
        )

        # ==========================================
        # Remarks
        # ==========================================

        ctk.CTkLabel(
            self.left,
            text="Remarks"
        ).pack(anchor="w", padx=20)

        self.remarks = ctk.CTkTextbox(
            self.left,
            height=80
        )

        self.remarks.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # ==========================================
        # Buttons
        # ==========================================

        self.button_frame = ctk.CTkFrame(
            self.left,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Add",
            width=150
        )

        self.add_btn.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.update_btn = ctk.CTkButton(
            self.button_frame,
            text="Update",
            width=150
        )

        self.update_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="Delete",
            width=150
        )

        self.delete_btn.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            width=150
        )

        self.clear_btn.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # ==========================================
        # Right Employee List
        # ==========================================

        self.right = ctk.CTkFrame(
            self.body
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.right,
            text="Employee List",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        self.table_frame = ctk.CTkFrame(
            self.right
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Scrollbar

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame,
            orientation="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # Employee Table
        # ==========================================

        columns = (
            "ID",
            "Employee ID",
            "Name",
            "Department",
            "Designation",
            "Mobile",
            "Joining Date",
            "Salary",
            "Status"
        )

        self.employee_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=self.scroll_y.set
        )

        self.scroll_y.configure(
            command=self.employee_table.yview
        )

        for col in columns:

            self.employee_table.heading(
                col,
                text=col
            )

            self.employee_table.column(
                col,
                width=120,
                anchor="center"
            )

        self.employee_table.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # Choose Employee Photo
        # ==========================================

    def choose_photo(self):

        file_path = filedialog.askopenfilename(
            title="Select Employee Photo",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("JPG Files", "*.jpg"),
                ("PNG Files", "*.png")
            ]
        )

        if not file_path:
            return

        self.photo_path = file_path

        try:

            image = Image.open(file_path)

            image.thumbnail((180, 180))

            self.photo_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.photo_label.configure(
                image=self.photo_image,
                text=""
            )

        except Exception as e:

            print("Photo Load Error:", e)
