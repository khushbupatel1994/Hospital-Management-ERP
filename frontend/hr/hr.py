import customtkinter as ctk
from PIL import Image
from frontend.hr.hr_ui import HRUI
from backend.hr.hr_crud import HRCRUD


class HR:

    def __init__(self, root):

        self.root = root

        # Database
        self.crud = HRCRUD()

        # UI
        self.ui = HRUI(root)

        # Connect buttons
        self.connect_buttons()

        # Load employees
        self.load_employees()
        self.set_new_employee_id()

    # ==========================================
    # Connect Buttons
    # ==========================================

    def connect_buttons(self):

        self.ui.add_btn.configure(
            command=self.add_employee
        )

        self.ui.update_btn.configure(
            command=self.update_employee
        )

        self.ui.delete_btn.configure(
            command=self.delete_employee
        )

        self.ui.clear_btn.configure(
            command=self.clear_form
        )

        self.ui.search_btn.configure(
            command=self.search_employee
        )

        self.ui.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_employee()
        )

        self.ui.employee_table.bind(
            "<ButtonRelease-1>",
            self.select_employee
        )

    # ==========================================
    # Load Employees
    # ==========================================

    def load_employees(self):

        for item in self.ui.employee_table.get_children():

            self.ui.employee_table.delete(item)

        try:

            employees = self.crud.load_employees()

            for employee in employees:

                self.ui.employee_table.insert(
                    "",
                    "end",
                    values=employee
                )

        except Exception as e:

            print("Load Employee Error:", e)

    # ==========================================
    # Set New Employee ID
    # ==========================================

    def set_new_employee_id(self):

        employee_id = self.crud.generate_employee_id()

        self.ui.employee_id.configure(
            state="normal"
        )

        self.ui.employee_id.delete(
            0,
            "end"
        )

        self.ui.employee_id.insert(
            0,
            employee_id
        )

        self.ui.employee_id.configure(
            state="disabled"
        )

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.ui.employee_id.configure(
            state="normal"
        )

        self.ui.employee_id.delete(
            0,
            "end"
        )

        self.ui.employee_id.configure(
            state="disabled"
        )

        self.ui.full_name.delete(0, "end")
        self.ui.father_name.delete(0, "end")
        self.ui.dob.delete(0, "end")
        self.ui.mobile.delete(0, "end")
        self.ui.email.delete(0, "end")
        self.ui.city.delete(0, "end")
        self.ui.state.delete(0, "end")
        self.ui.pincode.delete(0, "end")
        self.ui.designation.delete(0, "end")
        self.ui.basic_salary.delete(0, "end")
        self.ui.aadhaar_no.delete(0, "end")
        self.ui.pan_no.delete(0, "end")
        self.ui.qualification.delete(0, "end")
        self.ui.experience.delete(0, "end")

        self.ui.address.delete(
            "1.0",
            "end"
        )

        self.ui.remarks.delete(
            "1.0",
            "end"
        )

        self.ui.gender.set("Male")
        self.ui.blood_group.set("O+")
        self.ui.marital_status.set("Single")
        self.ui.department.set("Administration")
        self.ui.employment_type.set("Full Time")
        self.ui.shift.set("General")
        self.ui.status.set("Active")

        self.ui.joining_date.delete(
            0,
            "end"
        )

        self.selected_employee_id = None
        self.set_new_employee_id()

    # ==========================================
    # Add Employee
    # ==========================================

    def add_employee(self):

        print("===== ADD EMPLOYEE CLICKED =====")

        name = self.ui.full_name.get().strip()

        if not name:

            print("Employee Name Required")

            return

        employee_id = self.crud.generate_employee_id()
        # Show Employee ID in UI
        self.ui.employee_id.configure(
            state="normal"
        )

        self.ui.employee_id.delete(
            0,
            "end"
        )

        self.ui.employee_id.insert(
            0,
            employee_id
        )

        self.ui.employee_id.configure(
            state="disabled"
        )

        success = self.crud.add_employee(

            employee_id,

            name,

            self.ui.father_name.get().strip(),

            self.ui.gender.get(),

            self.ui.dob.get().strip(),

            self.ui.blood_group.get(),

            self.ui.marital_status.get(),

            self.ui.mobile.get().strip(),

            self.ui.email.get().strip(),

            self.ui.address.get(
                "1.0",
                "end"
            ).strip(),

            self.ui.city.get().strip(),

            self.ui.state.get().strip(),

            self.ui.pincode.get().strip(),

            self.ui.department.get(),

            self.ui.designation.get().strip(),

            self.ui.joining_date.get().strip(),

            self.ui.employment_type.get(),

            self.ui.basic_salary.get().strip(),

            self.ui.shift.get(),

            self.ui.status.get(),

            self.ui.aadhaar_no.get().strip(),

            self.ui.pan_no.get().strip(),

            self.ui.qualification.get().strip(),

            self.ui.experience.get().strip(),

            self.ui.photo_path,

            self.ui.remarks.get(
                "1.0",
                "end"
            ).strip()
        )

        if success:

            print("Employee Added Successfully")

            self.load_employees()

            self.clear_form()

# ==========================================
# Select Employee
# ==========================================

    def select_employee(self, event=None):

        selected = self.ui.employee_table.selection()

        if not selected:
            return

        values = self.ui.employee_table.item(
            selected[0],
            "values"
        )

        if not values:
            return

        self.selected_employee_id = values[0]

        print(
            "Selected Employee:",
            self.selected_employee_id
        )

        employee = self.crud.get_employee_by_id(
            self.selected_employee_id
        )
        print("Employee Data:", employee)
        
        if not employee:
            print("Employee Not Found")
            return

        photo_path = employee[25]

        self.ui.photo_path = photo_path

        if photo_path:

            try:

                image = Image.open(photo_path)

                image.thumbnail((180,180))

                self.ui.photo_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                self.ui.photo_label.configure(
                    image=self.ui.photo_image,
                    text=""
                )

            except Exception as e:

                print("Photo Load Error:", e)

        else:

            self.ui.photo_label.configure(
                image=None,
                text="No Photo"
            )
        print("Employee Data:", employee)

        # ==========================================
        # Employee ID
        # ==========================================

        self.ui.employee_id.configure(
            state="normal"
        )

        self.ui.employee_id.delete(
            0,
            "end"
        )

        self.ui.employee_id.insert(
            0,
            employee[1] or ""
        )

        self.ui.employee_id.configure(
            state="disabled"
        )

        # ==========================================
        # Personal Information
        # ==========================================

        self.ui.full_name.delete(0, "end")
        self.ui.full_name.insert(
            0,
            employee[2] or ""
        )

        self.ui.father_name.delete(0, "end")
        self.ui.father_name.insert(
            0,
            employee[3] or ""
        )

        self.ui.gender.set(
            employee[4] or "Male"
        )

        # DOB Calendar
        if employee[5]:
            self.ui.dob.set_date(employee[5])

        self.ui.blood_group.set(
            employee[6] or "O+"
        )

        self.ui.marital_status.set(
            employee[7] or "Single"
        )

        # ==========================================
        # Contact Information
        # ==========================================

        self.ui.mobile.delete(0, "end")
        self.ui.mobile.insert(
            0,
            employee[8] or ""
        )

        self.ui.email.delete(0, "end")
        self.ui.email.insert(
            0,
            employee[9] or ""
        )

        self.ui.address.delete(
            "1.0",
            "end"
        )

        self.ui.address.insert(
            "1.0",
            employee[10] or ""
        )

        self.ui.city.delete(0, "end")
        self.ui.city.insert(
            0,
            employee[11] or ""
        )

        self.ui.state.delete(0, "end")
        self.ui.state.insert(
            0,
            employee[12] or ""
        )

        self.ui.pincode.delete(0, "end")
        self.ui.pincode.insert(
            0,
            employee[13] or ""
        )

        # ==========================================
        # Job Information
        # ==========================================

        self.ui.department.set(
            employee[14] or "Administration"
        )

        self.ui.designation.delete(
            0,
            "end"
        )

        self.ui.designation.insert(
            0,
            employee[15] or ""
        )

        # Joining Date Calendar
        if employee[16]:
            self.ui.joining_date.set_date(employee[16])

        self.ui.employment_type.set(
            employee[17] or "Full Time"
        )

        self.ui.basic_salary.delete(
            0,
            "end"
        )

        self.ui.basic_salary.insert(
            0,
            employee[18] or ""
        )

        self.ui.shift.set(
            employee[19] or "General"
        )

        self.ui.status.set(
            employee[20] or "Active"
        )

        # ==========================================
        # Documents
        # ==========================================

        self.ui.aadhaar_no.delete(
            0,
            "end"
        )

        self.ui.aadhaar_no.insert(
            0,
            employee[21] or ""
        )

        self.ui.pan_no.delete(
            0,
            "end"
        )

        self.ui.pan_no.insert(
            0,
            employee[22] or ""
        )

        self.ui.qualification.delete(
            0,
            "end"
        )

        self.ui.qualification.insert(
            0,
            employee[23] or ""
        )

        self.ui.experience.delete(
            0,
            "end"
        )

        self.ui.experience.insert(
            0,
            employee[24] or ""
        )

        # ==========================================
        # Remarks
        # ==========================================

        self.ui.remarks.delete(
            "1.0",
            "end"
        )

        self.ui.remarks.insert(
            "1.0",
            employee[26] or ""
        )

        print("✅ Employee Details Loaded")

        # ==========================================
        # Update Employee
        # ==========================================

    def update_employee(self):

        if not self.selected_employee_id:

            print("Please select employee")

            return

        print("===== UPDATE EMPLOYEE CLICKED =====")

        try:

            success = self.crud.update_employee(

                self.selected_employee_id,

                self.ui.full_name.get().strip(),

                self.ui.father_name.get().strip(),

                self.ui.gender.get(),

                self.ui.dob.get().strip(),

                self.ui.blood_group.get(),

                self.ui.marital_status.get(),

                self.ui.mobile.get().strip(),

                self.ui.email.get().strip(),

                self.ui.address.get(
                    "1.0",
                    "end"
                ).strip(),

                self.ui.city.get().strip(),

                self.ui.state.get().strip(),

                self.ui.pincode.get().strip(),

                self.ui.department.get(),

                self.ui.designation.get().strip(),

                self.ui.joining_date.get().strip(),

                self.ui.employment_type.get(),

                self.ui.basic_salary.get().strip(),

                self.ui.shift.get(),

                self.ui.status.get(),

                self.ui.aadhaar_no.get().strip(),

                self.ui.pan_no.get().strip(),

                self.ui.qualification.get().strip(),

                self.ui.experience.get().strip(),

                self.ui.photo_path,

                self.ui.remarks.get(
                    "1.0",
                    "end"
                ).strip()
            )

            if success:

                print("✅ Employee Updated Successfully")

                self.load_employees()

                self.clear_form()

            else:

                print("❌ Employee Update Failed")

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "Update Employee Error:",
                e
            )

        # ==========================================
        # Delete Employee
        # ==========================================

    def delete_employee(self):

        if not self.selected_employee_id:

            print("Please select employee")

            return

        success = self.crud.delete_employee(
            self.selected_employee_id
        )

        if success:

            print("Employee Deleted Successfully")

            self.load_employees()

            self.clear_form()

    # ==========================================
    # Search Employee
    # ==========================================

    def search_employee(self):

        keyword = self.ui.search_entry.get().strip()

        for item in self.ui.employee_table.get_children():

            self.ui.employee_table.delete(item)

        try:

            employees = self.crud.search_employee(
                keyword
            )

            for employee in employees:

                self.ui.employee_table.insert(
                    "",
                    "end",
                    values=employee
                )

        except Exception as e:

            print(
                "Search Employee Error:",
                e
            )
