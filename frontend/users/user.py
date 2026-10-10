"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : User Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox

from frontend.users.user_ui import UserUI
from frontend.users.user_service import UserService
from frontend.users.user_crud import UserCRUD


class User(UserUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = UserService()
        self.crud = UserCRUD()

        self.bind_events()

        self.load_users()

     # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_user
        )

        self.update_btn.configure(
            command=self.update_user
        )

        self.delete_btn.configure(
            command=self.delete_user
        )

        self.search_btn.configure(
            command=self.search_user
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_user()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.user_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_user
        )

     # ==========================================
    # Add User
    # ==========================================

    def add_user(self):

        employee_id = self.employee_id.get().strip()
        full_name = self.full_name.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        role = self.role.get()
        department = self.department.get()
        mobile = self.mobile.get().strip()
        email = self.email.get().strip()
        status = self.status.get()
        security_question = self.security_question.get().strip()
        security_answer = self.security_answer.get().strip()

        # Validation
        if not self.service.validate_user(
            employee_id,
            full_name,
            username,
            password,
            role,
            department,
            mobile,
            email
        ):
            return

        # Duplicate Check
        duplicate = self.crud.check_duplicate(
            employee_id,
            username
        )

        if duplicate:

            messagebox.showerror(
                "Duplicate User",
                "Employee ID or Username already exists."
            )

            return

        success = self.crud.add_user(
            employee_id,
            full_name,
            username,
            password,
            role,
            department,
            mobile,
            email,
            security_question,
            security_answer,
            status
        )

        if success:

            messagebox.showinfo(
                "Success",
                "User added successfully."
            )

            self.clear_form()
            self.load_users()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add user."
            )

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.employee_id.delete(0, "end")
        self.full_name.delete(0, "end")
        self.username.delete(0, "end")
        self.password.delete(0, "end")
        self.mobile.delete(0, "end")
        self.email.delete(0, "end")

        self.security_question.set("")
        self.security_answer.delete(0, "end")

        self.role.set("")
        self.department.set("")
        self.status.set("Active")

    # ==========================================
    # Load Users
    # ==========================================

    def load_users(self):

        # पुराना Data हटाओ
        for item in self.user_table.get_children():
            self.user_table.delete(item)

        # नया Data लाओ
        rows = self.crud.load_users()

        for row in rows:

            self.user_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Search User
    # ==========================================

    def search_user(self):

        keyword = self.search_entry.get().strip()

        for item in self.user_table.get_children():
            self.user_table.delete(item)

        rows = self.crud.search_user(keyword)

        for row in rows:

            self.user_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Delete User
    # ==========================================

    def delete_user(self):

        selected = self.user_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a user."
            )

            return

        values = self.user_table.item(selected, "values")

        user_id = values[0]

        if messagebox.askyesno(
            "Confirm",
            "Delete this user?"
        ):

            if self.crud.delete_user(user_id):

                messagebox.showinfo(
                    "Success",
                    "User deleted successfully."
                )

                self.load_users()

                self.clear_form()

     # ==========================================
    # Load Selected User
    # ==========================================

    def load_selected_user(self, event=None):

        selected = self.user_table.focus()

        if not selected:
            return

        values = self.user_table.item(selected, "values")

        self.selected_user_id = values[0]

        self.employee_id.delete(0, "end")
        self.employee_id.insert(0, values[1])

        self.full_name.delete(0, "end")
        self.full_name.insert(0, values[2])

        self.username.delete(0, "end")
        self.username.insert(0, values[3])

        self.role.set(values[4])
        self.department.set(values[5])

        self.mobile.delete(0, "end")
        self.mobile.insert(0, values[6])

        self.status.set(values[7])

    # ==========================================
    # Update User
    # ==========================================

    def update_user(self):

        if not hasattr(self, "selected_user_id"):

            messagebox.showwarning(
                "Warning",
                "Please select a user."
            )

            return

        success = self.crud.update_user(
            self.selected_user_id,
            self.employee_id.get().strip(),
            self.full_name.get().strip(),
            self.username.get().strip(),
            self.role.get(),
            self.department.get(),
            self.mobile.get().strip(),
            self.email.get().strip(),
            self.security_question.get().strip(),
            self.security_answer.get().strip(),
            self.status.get()
        )

        if success:

            messagebox.showinfo(
                "Success",
                "User updated successfully."
            )

            self.load_users()
            self.clear_form()

        else:

            messagebox.showerror(
                "Error",
                "Unable to update user."
            )
