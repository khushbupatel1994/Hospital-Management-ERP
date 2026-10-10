"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Doctor Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox

from frontend.doctors.doctor_ui import DoctorUI
from frontend.doctors.doctor_service import DoctorService
from frontend.doctors.doctor_crud import DoctorCRUD


class Doctor(DoctorUI):

    def __init__(self, root, api_client=None):
        self.api_client = api_client

        super().__init__(root)

        self.service = DoctorService()

        self.crud = DoctorCRUD()

        self.bind_events()

        self.load_doctors()

        self.doctor_id.configure(state="normal")

        self.doctor_id.insert(
            0,
            self.crud.generate_doctor_id()
        )

        self.doctor_id.configure(state="disabled")

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_doctor
        )

        self.update_btn.configure(
            command=self.update_doctor
        )

        self.delete_btn.configure(
            command=self.delete_doctor
        )

        self.search_btn.configure(
            command=self.search_doctor
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_doctor()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.doctor_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_doctor
        )

    # ==========================================
    # Add Doctor
    # ==========================================

    def add_doctor(self):

        doctor_id = self.doctor_id.get()
        full_name = self.full_name.get().strip()
        gender = self.gender.get()
        department = self.department.get()
        specialization = self.specialization.get().strip()
        qualification = self.qualification.get().strip()
        experience = self.experience.get().strip()
        mobile = self.mobile.get().strip()
        email = self.email.get().strip()
        consultation_fee = self.consultation_fee.get().strip()
        opd_timing = self.opd_timing.get().strip()
        available_days = self.available_days.get().strip()
        status = self.status.get()

        # Validation
        if not self.service.validate_doctor(
            full_name,
            department,
            specialization,
            mobile,
            email,
            experience,
            consultation_fee
        ):
            return

        # =================================================
        # CLOUD API ADD
        # =================================================

        if self.api_client:

            payload = {
                "doctor_id": doctor_id,
                "full_name": full_name,
                "name": full_name,
                "gender": gender,
                "department": department,
                "specialization": specialization,
                "qualification": qualification,
                "experience": experience,
                "mobile": mobile,
                "email": email,
                "consultation_fee": consultation_fee,
                "opd_timing": opd_timing,
                "available_days": available_days,
                "status": status
            }

            try:
                print("Adding Doctor through Central API...")

                api_result = self.api_client.request(
                    "POST",
                    "/api/v1/modules/doctors/records",
                    json={"data": payload}
                )

                if isinstance(api_result, dict) and api_result.get("ok"):
                    print("Central Doctor Created:", api_result)
                    messagebox.showinfo(
                        "Success",
                        "Doctor added successfully."
                    )
                    self.clear_form()
                    self.load_doctors()
                    return

                messagebox.showerror(
                    "Error",
                    "Unable to add doctor on the hospital server."
                )
                return

            except Exception as e:
                print("Cloud Doctor Add Error:", e)
                messagebox.showerror(
                    "Error",
                    f"Unable to add doctor on the hospital server.\n\n{e}"
                )
                return


        # =================================================
        # CLOUD API UPDATE
        # =================================================

        if self.api_client:

            payload = {
                "full_name": self.full_name.get().strip(),
                "name": self.full_name.get().strip(),
                "gender": self.gender.get(),
                "department": self.department.get(),
                "specialization": self.specialization.get().strip(),
                "qualification": self.qualification.get().strip(),
                "experience": self.experience.get().strip(),
                "mobile": self.mobile.get().strip(),
                "email": self.email.get().strip(),
                "consultation_fee": self.consultation_fee.get().strip(),
                "opd_timing": self.opd_timing.get().strip(),
                "available_days": self.available_days.get().strip(),
                "status": self.status.get()
            }

            try:
                print("Updating Doctor through Central API...")

                api_result = self.api_client.request(
                    "PUT",
                    f"/api/v1/modules/doctors/records/{self.selected_doctor_id}",
                    json={"data": payload}
                )

                if isinstance(api_result, dict) and api_result.get("ok"):
                    print("Central Doctor Updated:", api_result)

                    messagebox.showinfo(
                        "Success",
                        "Doctor updated successfully."
                    )

                    self.load_doctors()
                    self.clear_form()
                    self.selected_doctor_id = None
                    return

                messagebox.showerror(
                    "Error",
                    "Unable to update doctor on the hospital server."
                )
                return

            except Exception as e:
                print("Cloud Doctor Update Error:", e)
                messagebox.showerror(
                    "Error",
                    f"Unable to update doctor on the hospital server.\n\n{e}"
                )
                return

        # Duplicate Mobile Check
        duplicate = self.crud.check_duplicate_mobile(mobile)
        if duplicate:
            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )
            return

        success = self.crud.add_doctor(
            doctor_id,
            full_name,
            gender,
            department,
            specialization,
            qualification,
            experience,
            mobile,
            email,
            consultation_fee,
            opd_timing,
            available_days,
            status
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Doctor added successfully."
            )
            self.clear_form()
            self.load_doctors()
        else:
            messagebox.showerror(
                "Error",
                "Unable to add doctor."
            )

# ==========================================
# Clear Form
# ==========================================

    def clear_form(self):

        self.doctor_id.configure(state="normal")

        self.doctor_id.delete(0, "end")

        self.doctor_id.insert(
            0,
            self.crud.generate_doctor_id()
        )

        self.doctor_id.configure(state="disabled")

        self.full_name.delete(0, "end")

        self.specialization.delete(0, "end")

        self.qualification.delete(0, "end")

        self.experience.delete(0, "end")

        self.mobile.delete(0, "end")

        self.email.delete(0, "end")

        self.consultation_fee.delete(0, "end")

        self.opd_timing.set("")

        self.available_days.set("")

        self.gender.set("Male")

        self.department.set("General Medicine")

        self.status.set("Active")

# ==========================================
# Load Doctors
# ==========================================

    def load_doctors(self):

        try:

            for item in self.doctor_table.get_children():
                self.doctor_table.delete(item)

            if self.api_client:

                print("Loading Doctors from Central API...")

                response = self.api_client.request(
                    "GET",
                    "/api/v1/modules/doctors/records",
                    params={
                        "limit": 100,
                        "offset": 0,
                        "search": ""
                    }
                )

                items = response.get("items", []) if isinstance(response, dict) else []

                print("All Doctors Count:", len(items))

                for row in items:

                    self.doctor_table.insert(
                        "",
                        "end",
                        values=(
                            row.get("id", "") ,
                            row.get("doctor_id", "") ,
                            row.get("full_name") or row.get("name", "") ,
                            row.get("department", "") ,
                            row.get("specialization", "") ,
                            row.get("mobile", "")
                        )
                    )

                return

            # Local fallback
            rows = self.crud.load_doctors()

            for row in rows:
                self.doctor_table.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:
            print("Load Doctors Error:", e)

# Load Selected Doctor
# ==========================================

    def load_selected_doctor(self, event=None):

        selected = self.doctor_table.focus()

        if not selected:
            return

        values = self.doctor_table.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_doctor_id = values[0]

        try:

            if self.api_client:

                print("Loading selected Doctor from Central API...")

                response = self.api_client.request(
                    "GET",
                    "/api/v1/modules/doctors/records",
                    params={
                        "limit": 100,
                        "offset": 0,
                        "search": ""
                    }
                )

                items = response.get("items", []) if isinstance(response, dict) else []

                doctor = next(
                    (row for row in items if str(row.get("id", "")) == str(self.selected_doctor_id)),
                    None
                )

                if not doctor:
                    messagebox.showerror(
                        "Error",
                        "Selected doctor was not found on the hospital server."
                    )
                    return

                self.doctor_id.configure(state="normal")
                self.doctor_id.delete(0, "end")
                self.doctor_id.insert(0, doctor.get("doctor_id", ""))
                self.doctor_id.configure(state="disabled")

                self.full_name.delete(0, "end")
                self.full_name.insert(0, doctor.get("full_name") or doctor.get("name", ""))

                self.gender.set(doctor.get("gender", "") or "")
                self.department.set(doctor.get("department", "") or "")

                self.specialization.delete(0, "end")
                self.specialization.insert(0, doctor.get("specialization", "") or "")

                self.qualification.delete(0, "end")
                self.qualification.insert(0, doctor.get("qualification", "") or "")

                self.experience.delete(0, "end")
                self.experience.insert(0, str(doctor.get("experience", "") or ""))

                self.mobile.delete(0, "end")
                self.mobile.insert(0, doctor.get("mobile") or doctor.get("phone", ""))

                self.email.delete(0, "end")
                self.email.insert(0, doctor.get("email", "") or "")

                self.consultation_fee.delete(0, "end")
                self.consultation_fee.insert(0, str(doctor.get("consultation_fee", "") or ""))

                self.opd_timing.set(doctor.get("opd_timing", "") or "")
                self.available_days.set(doctor.get("available_days", "") or "")
                self.status.set(doctor.get("status", "") or "")

                print("Selected Doctor Loaded:", doctor.get("full_name") or doctor.get("name", ""))
                return

            # Local fallback
            doctor = self.crud.get_doctor_by_id(self.selected_doctor_id)

            if not doctor:
                return

            self.doctor_id.configure(state="normal")
            self.doctor_id.delete(0, "end")
            self.doctor_id.insert(0, doctor[1])
            self.doctor_id.configure(state="disabled")

            self.full_name.delete(0, "end")
            self.full_name.insert(0, doctor[2])
            self.gender.set(doctor[3])
            self.department.set(doctor[4])

            self.specialization.delete(0, "end")
            self.specialization.insert(0, doctor[5])
            self.qualification.delete(0, "end")
            self.qualification.insert(0, doctor[6])
            self.experience.delete(0, "end")
            self.experience.insert(0, doctor[7])
            self.mobile.delete(0, "end")
            self.mobile.insert(0, doctor[8])
            self.email.delete(0, "end")
            self.email.insert(0, doctor[9])
            self.consultation_fee.delete(0, "end")
            self.consultation_fee.insert(0, doctor[10])
            self.opd_timing.set(doctor[11] if doctor[11] else "")
            self.available_days.set(doctor[12] if doctor[12] else "")
            self.status.set(doctor[13])

        except Exception as e:
            print("Load Selected Doctor Error:", e)
            messagebox.showerror(
                "Error",
                f"Unable to load selected doctor.\n\n{e}"
            )

# ==========================================
# Update Doctor
# ==========================================

    def update_doctor(self):

        if not hasattr(self, "selected_doctor_id"):


            messagebox.showwarning(
                "Warning",
                "Please select a doctor."
            )

            return

        # Duplicate Mobile Check

        duplicate = self.crud.check_duplicate_mobile(

            self.mobile.get().strip(),

            self.selected_doctor_id

        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )

            return

        success = self.crud.update_doctor(

        self.selected_doctor_id,

        self.full_name.get().strip(),

        self.gender.get(),

        self.department.get(),

        self.specialization.get().strip(),

        self.qualification.get().strip(),

        self.experience.get().strip(),

        self.mobile.get().strip(),

        self.email.get().strip(),

        self.consultation_fee.get().strip(),

        self.opd_timing.get().strip(),

        self.available_days.get().strip(),

        self.status.get()

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Doctor updated successfully."
            )

            self.load_doctors()

            self.clear_form()

            self.selected_doctor_id = None

        else:

            messagebox.showerror(
                "Error",
                "Unable to update doctor."
            )

# ==========================================
# Delete Doctor
# ==========================================

    def delete_doctor(self):

        selected = self.doctor_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a doctor."
            )

            return

        values = self.doctor_table.item(
            selected,
            "values"
        )

        doctor_db_id = values[0]

        if messagebox.askyesno(
            "Confirm",
            "Delete this doctor?"
        ):

            if self.crud.delete_doctor(doctor_db_id):

                messagebox.showinfo(
                    "Success",
                    "Doctor deleted successfully."
                )

                self.load_doctors()

                self.clear_form()

                self.selected_doctor_id = None

# ==========================================
# Search Doctor
# ==========================================

    def search_doctor(self):

        keyword = self.search_entry.get().strip()

        for item in self.doctor_table.get_children():

            self.doctor_table.delete(item)

        rows = self.crud.search_doctor(keyword)

        for row in rows:

            self.doctor_table.insert(
                "",
                "end",
                values=row
            )
