"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Patient Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime, date
from PIL import Image
import shutil
import os
import customtkinter as ctk
from frontend.patients.patient_ui import PatientUI
from frontend.patients.patient_service import PatientService
from frontend.patients.patient_crud import PatientCRUD

class Patient(PatientUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = PatientService()
        self.crud = PatientCRUD()

        self.bind_events()

        self.load_doctors()

        self.load_patients()

        self.patient_id.configure(state="normal")
        self.patient_id.insert(0, self.crud.generate_patient_id())
        self.patient_id.configure(state="disabled")

        self.registration_no.configure(state="normal")
        self.registration_no.insert(0, self.crud.generate_registration_no())
        self.registration_no.configure(state="disabled")
        

    def load_doctors(self):

        rows = self.crud.load_doctors()

        doctor_list = [row[0] for row in rows]

        if not doctor_list:
            doctor_list = ["Select Doctor"]

        self.doctor.configure(values=doctor_list)
        self.doctor.set(doctor_list[0])

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_patient
        )

        self.update_btn.configure(
            command=self.update_patient
        )

        self.delete_btn.configure(
            command=self.delete_patient
        )

        self.search_btn.configure(
            command=self.search_patient
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_patient()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )
        self.photo_btn.configure(
            command=self.upload_photo
        )

        self.patient_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_patient
        )
        self.dob.bind(
          "<<DateEntrySelected>>",
          self.calculate_age
        )
    # ==========================================
    # Upload Patient Photo
    # ==========================================

    def upload_photo(self):

        file_path = filedialog.askopenfilename(
            title="Select Patient Photo",
             filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png"),
            ("JPG Files", "*.jpg"),
            ("PNG Files", "*.png")
        ]
    )

        if not file_path:
            return

        try:
            # Patient ID
            patient_id = self.patient_id.get().strip()

            if not patient_id:
                messagebox.showwarning(
                    "Warning",
                    "Patient ID not available."
                )
                return

            # Check file size
            file_size = os.path.getsize(file_path)

            # Maximum 2 MB
            if file_size > 2 * 1024 * 1024:

                messagebox.showerror(
                    "File Too Large",
                    "Patient photo must be less than 2 MB."
                )

                return

            # Create folder
            folder = os.path.join(
                "assets",
                "patients"
            )

            os.makedirs(
                folder,
                exist_ok=True
            )

            # Destination
            destination = os.path.join(
                folder,
                patient_id + ".jpg"
            )

            # Open image
            image = Image.open(file_path)

            # Convert to RGB
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Resize
            image.thumbnail(
                (300, 400)
            )

            # Save
            image.save(
                destination,
                "JPEG",
                quality=90
            )

            # Display image
            display_image = Image.open(
                destination
            )

            display_image.thumbnail(
                (120, 140)
            )

            self.photo = ctk.CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=(120, 140)
            )

            self.photo_label.configure(
                image=self.photo,
                text=""
            )

            messagebox.showinfo(
                "Success",
                "Patient photo uploaded successfully."
            )

        except Exception as e:

            print(
                "Patient Photo Error:",
                e
            )

            messagebox.showerror(
                "Error",
                "Unable to upload patient photo."
            )

    # ==========================================
    # Add Patient
    # ==========================================

    def add_patient(self):

        patient_name = self.patient_name.get().strip()
        gender = self.gender.get()
        dob = self.dob.get().strip()
        age = self.age.get().strip()
        blood_group = self.blood_group.get()
        mobile = self.mobile.get().strip()
        email = self.email.get().strip()
        address = self.address.get("1.0", "end").strip()
        city = self.city.get().strip()
        state = self.state.get().strip()
        pin_code = self.pin_code.get().strip()
        aadhaar = self.aadhaar.get().strip()
        doctor = self.doctor.get()
        department = self.department.get()
        patient_type = self.patient_type.get()
        status = self.status.get()

        if not self.service.validate_patient(
            patient_name,
            gender,
            age,
            mobile,
            email,
            doctor,
            department
        ):
            return

        # Duplicate Mobile Check
        duplicate = self.crud.check_duplicate_mobile(
            mobile
        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )

            return
        # ==========================================
        # Duplicate Aadhaar Check
        # ==========================================

        duplicate = self.crud.check_duplicate_aadhaar(
            aadhaar
        )
        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Aadhaar Number already exists."
            )

            return

        success = self.crud.add_patient(

            self.patient_id.get(),

            self.registration_no.get(),

            patient_name,

            gender,

            dob,

            age,

            blood_group,

            mobile,

            email,

            address,

            city,

            state,

            pin_code,

            aadhaar,

            doctor,

            department,

            patient_type,

            status

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Patient added successfully."
            )

            self.clear_form()

            self.load_patients()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add patient."
            )
       

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):
        self.patient_id.configure(state="normal")
        self.patient_id.delete(0, "end")
        self.patient_id.insert(0, self.crud.generate_patient_id())
        self.patient_id.configure(state="disabled")

        self.registration_no.configure(state="normal")
        self.registration_no.delete(0, "end")
        self.registration_no.insert(0, self.crud.generate_registration_no())
        self.registration_no.configure(state="disabled")

        self.patient_name.delete(0, "end")
        self.gender.set("Male")
        self.dob.delete(0, "end")
        self.age.delete(0, "end")
        self.blood_group.set("O+")
        self.mobile.delete(0, "end")
        self.email.delete(0, "end")
        self.address.delete("1.0", "end")
        self.city.delete(0, "end")
        self.state.delete(0, "end")
        self.pin_code.delete(0, "end")
        self.aadhaar.delete(0, "end")
        self.doctor.set("Select Doctor")
        self.department.set("General Medicine")
        self.patient_type.set("OPD")
        self.status.set("Active")

    # ==========================================
    # Load Patients
    # ==========================================

    def load_patients(self):

        for item in self.patient_table.get_children():
            self.patient_table.delete(item)

        rows = self.crud.load_patients()

        for row in rows:
            self.patient_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Load Selected Patient
    # ==========================================

    def load_selected_patient(self, event=None):

        selected = self.patient_table.focus()

        if not selected:
            return

        values = self.patient_table.item(
            selected,
            "values"
        )

        patient = self.crud.get_patient_by_id(values[0])

        if not patient:
            return

        self.selected_patient_id = patient[0]

        self.patient_id.configure(state="normal")
        self.patient_id.delete(0, "end")
        self.patient_id.insert(0, patient[1])
        self.patient_id.configure(state="disabled")

        self.registration_no.configure(state="normal")
        self.registration_no.delete(0, "end")
        self.registration_no.insert(0, patient[2])
        self.registration_no.configure(state="disabled")

        self.patient_name.delete(0, "end")
        self.patient_name.insert(0, patient[3])

        self.gender.set(patient[4])
        self.dob.delete(0, "end")
        self.dob.insert(0, patient[5])

        self.age.delete(0, "end")
        self.age.insert(0, patient[6])

        self.blood_group.set(patient[7])

        self.mobile.delete(0, "end")
        self.mobile.insert(0, patient[8])

        self.email.delete(0, "end")
        self.email.insert(0, patient[9])

        self.address.delete("1.0", "end")
        self.address.insert("1.0", patient[10])

        self.city.delete(0, "end")
        self.city.insert(0, patient[11])

        self.state.delete(0, "end")
        self.state.insert(0, patient[12])

        self.pin_code.delete(0, "end")
        self.pin_code.insert(0, patient[13])

        self.aadhaar.delete(0, "end")
        self.aadhaar.insert(0, patient[14])

        self.doctor.set(patient[15])

        self.department.set(patient[16])

        self.patient_type.set(patient[17])

        self.status.set(patient[18])


    # ==========================================
    # Delete Patient
    # ==========================================

    def delete_patient(self):

        selected = self.patient_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a patient."
            )

            return
        

        values = self.patient_table.item(
            selected,
            "values"
        )

        patient_db_id = values[0]

        if messagebox.askyesno(
            "Confirm",
            "Delete this patient?"
        ):
            if self.crud.delete_patient(patient_db_id):
                messagebox.showinfo(
                    "Success",
                    "Patient deleted successfully."
                )

                self.load_patients()

                self.clear_form()

                self.selected_patient_id = None
    # ==========================================
    # Update Patient
    # ==========================================

    def update_patient(self):

        if not getattr(self, "selected_patient_id", None):

            messagebox.showwarning(
                "Warning",
                "Please select a patient."
            )

            return

        # ==========================================
        # Duplicate Mobile Check
        # ==========================================

        duplicate = self.crud.check_duplicate_mobile(
            self.mobile.get().strip(),
            self.selected_patient_id
        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Mobile Number already exists."
            )

            return

        # ==========================================
        # Duplicate Aadhaar Check
        # ==========================================

        duplicate = self.crud.check_duplicate_aadhaar(
            self.aadhaar.get().strip(),
            self.selected_patient_id
        )

        if duplicate:

            messagebox.showerror(
                "Duplicate",
                "Aadhaar Number already exists."
            )

            return

        # ==========================================
        # Update Patient
        # ==========================================

        success = self.crud.update_patient(

            self.selected_patient_id,

            self.patient_name.get().strip(),
            self.gender.get(),
            self.dob.get().strip(),
            self.age.get().strip(),
            self.blood_group.get(),
            self.mobile.get().strip(),
            self.email.get().strip(),
            self.address.get("1.0", "end").strip(),
            self.city.get().strip(),
            self.state.get().strip(),
            self.pin_code.get().strip(),
            self.aadhaar.get().strip(),
            self.doctor.get(),
            self.department.get(),
            self.patient_type.get(),
            self.status.get()

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Patient updated successfully."
            )

            self.load_patients()

            self.clear_form()

            self.selected_patient_id = None

        else:

            messagebox.showerror(
                "Error",
                "Unable to update patient."
            )

    # ==========================================
    # Search Patient
    # ==========================================

    def search_patient(self):

        keyword = self.search_entry.get().strip()

        for item in self.patient_table.get_children():
            self.patient_table.delete(item)

        rows = self.crud.search_patient(keyword)

        for row in rows:

            self.patient_table.insert(
                "",
                "end",
                values=row
            )

    # ==========================================
    # Calculate Age
    # ==========================================

    def calculate_age(self, event=None):

        try:

            dob = datetime.strptime(
                self.dob.get(),
                "%d-%m-%Y"
            ).date()

            today = date.today()

            age = today.year - dob.year

            if (today.month, today.day) < (dob.month, dob.day):
                age -= 1

            self.age.configure(state="normal")

            self.age.delete(0, "end")

            self.age.insert(0, str(age))

            self.age.configure(state="readonly")

        except:

            pass
