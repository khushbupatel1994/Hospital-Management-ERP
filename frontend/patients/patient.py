"""
===========================================================
Cloud Secure Hospital ERP
Module  : Patient Controller
Version : 5.0
===========================================================

Features:
- Patient CRUD
- Doctor-wise patient access
- Role-based patient filtering
- Doctor sees only assigned patients
- Admin/Super Admin sees all patients
- Doctor can work only with own patients
- Patient photo upload
- Search
- Update
- Delete
- Database-safe behavior
===========================================================
"""

from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime, date
from PIL import Image
import os
import shutil
import customtkinter as ctk

from frontend.patients.patient_ui import PatientUI
from frontend.patients.patient_service import PatientService
from frontend.patients.patient_crud import PatientCRUD


class Patient(PatientUI):

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(
        self,
        root,
        user=None,
        role=None,
        api_client=None
    ):
        super().__init__(root)

        # -------------------------------------------------
        # Login information
        # -------------------------------------------------

        self.user = user

        self.role = (
            str(role).strip()
            if role
            else ""
        )

        self.selected_patient_id = None

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        self.api_client = api_client

        self.service = PatientService()
        self.crud = PatientCRUD()

        print(
            "✅ Patient Controller Loaded"
        )

        print(
            f"🔐 Patient Module Role: {self.role}"
        )

        # -------------------------------------------------
        # Events
        # -------------------------------------------------

        self.bind_events()

        # -------------------------------------------------
        # Initial data
        # -------------------------------------------------

        self.load_doctors()
        self.load_patients()

        # -------------------------------------------------
        # Generate Patient ID
        # -------------------------------------------------

        try:

            self.patient_id.configure(
                state="normal"
            )

            self.patient_id.delete(
                0,
                "end"
            )

            self.patient_id.insert(
                0,
                self.crud.generate_patient_id()
            )

            self.patient_id.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "Patient ID Error:",
                e
            )

        # -------------------------------------------------
        # Generate Registration Number
        # -------------------------------------------------

        try:

            self.registration_no.configure(
                state="normal"
            )

            self.registration_no.delete(
                0,
                "end"
            )

            self.registration_no.insert(
                0,
                self.crud.generate_registration_no()
            )

            self.registration_no.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "Registration Number Error:",
                e
            )

    # =====================================================
    # DOCTOR ROLE CHECK
    # =====================================================

    def is_doctor(self):

        return (
            self.role.lower()
            == "doctor"
        )

    # =====================================================
    # GET LOGGED-IN DOCTOR NAMES
    # =====================================================

    def get_logged_in_doctor_names(
        self
    ):

        names = []

        # -------------------------------------------------
        # Helper
        # -------------------------------------------------

        def add_name(value):

            if value is None:
                return

            value = str(
                value
            ).strip()

            if not value:
                return

            # Never use password hash
            if (
                value.startswith("$2b$")
                or
                value.startswith("$2a$")
                or
                value.startswith("$2y$")
            ):
                return

            existing = {
                item.lower()
                for item in names
            }

            if (
                value.lower()
                not in existing
            ):

                names.append(
                    value
                )

        try:

            # =================================================
            # sqlite Row / mapping
            # =================================================

            if (
                hasattr(
                    self.user,
                    "keys"
                )
                and
                callable(
                    self.user.keys
                )
            ):

                keys = set(
                    self.user.keys()
                )

                possible_keys = [
                    "employee_id",
                    "doctor_id",
                    "doctor_code",
                    "full_name",
                    "name",
                    "doctor_name",
                    "display_name",
                    "username",
                    "user_name",
                    "email"
                ]

                for key in possible_keys:

                    if key in keys:

                        add_name(
                            self.user[key]
                        )

            # =================================================
            # Dictionary user
            # =================================================

            elif isinstance(
                self.user,
                dict
            ):

                possible_keys = [
                    "employee_id",
                    "doctor_id",
                    "doctor_code",
                    "full_name",
                    "name",
                    "doctor_name",
                    "display_name",
                    "username",
                    "user_name",
                    "email"
                ]

                for key in possible_keys:

                    add_name(
                        self.user.get(
                            key
                        )
                    )

            # =================================================
            # Tuple / list user
            #
            # Existing login structure:
            #
            # [employee_id,
            #  full_name,
            #  username,
            #  password_hash,
            #  ...]
            # =================================================

            elif isinstance(
                self.user,
                (tuple, list)
            ):

                if len(
                    self.user
                ) > 1:

                    add_name(
                        self.user[1]
                    )

                if len(
                    self.user
                ) > 2:

                    add_name(
                        self.user[2]
                    )

                if len(
                    self.user
                ) > 3:

                    add_name(
                        self.user[3]
                    )

            # =================================================
            # Resolve actual user from users table
            # =================================================

            username = None
            employee_id = None
            full_name = None

            if (
                hasattr(
                    self.user,
                    "keys"
                )
                and
                callable(
                    self.user.keys
                )
            ):

                keys = set(
                    self.user.keys()
                )

                if (
                    "username"
                    in keys
                ):

                    username = (
                        self.user[
                            "username"
                        ]
                    )

                elif (
                    "user_name"
                    in keys
                ):

                    username = (
                        self.user[
                            "user_name"
                        ]
                    )

                if (
                    "employee_id"
                    in keys
                ):

                    employee_id = (
                        self.user[
                            "employee_id"
                        ]
                    )

                if (
                    "full_name"
                    in keys
                ):

                    full_name = (
                        self.user[
                            "full_name"
                        ]
                    )

                elif (
                    "name"
                    in keys
                ):

                    full_name = (
                        self.user[
                            "name"
                        ]
                    )

            elif isinstance(
                self.user,
                dict
            ):

                username = (
                    self.user.get(
                        "username"
                    )
                    or
                    self.user.get(
                        "user_name"
                    )
                )

                employee_id = (
                    self.user.get(
                        "employee_id"
                    )
                )

                full_name = (
                    self.user.get(
                        "full_name"
                    )
                    or
                    self.user.get(
                        "name"
                    )
                )

            elif isinstance(
                self.user,
                (tuple, list)
            ):

                if len(
                    self.user
                ) > 2:

                    full_name = (
                        self.user[1]
                    )

                if len(
                    self.user
                ) > 1:

                    employee_id = (
                        self.user[0]
                    )

                if len(
                    self.user
                ) > 2:

                    username = (
                        self.user[2]
                    )

            # =================================================
            # Username lookup
            # =================================================

            if username:

                try:

                    self.crud.cursor.execute(
                        """
                        SELECT
                            employee_id,
                            full_name,
                            username
                        FROM users
                        WHERE LOWER(TRIM(username))
                            =
                            LOWER(TRIM(?))
                        LIMIT 1
                        """,
                        (
                            str(
                                username
                            ).strip(),
                        )
                    )

                    row = (
                        self.crud.cursor.fetchone()
                    )

                    if row:

                        for value in row:

                            add_name(
                                value
                            )

                except Exception as e:

                    print(
                        "Username lookup warning:",
                        e
                    )

            # =================================================
            # Employee ID lookup
            # =================================================

            if employee_id:

                try:

                    self.crud.cursor.execute(
                        """
                        SELECT
                            employee_id,
                            full_name,
                            username
                        FROM users
                        WHERE LOWER(TRIM(employee_id))
                            =
                            LOWER(TRIM(?))
                        LIMIT 1
                        """,
                        (
                            str(
                                employee_id
                            ).strip(),
                        )
                    )

                    row = (
                        self.crud.cursor.fetchone()
                    )

                    if row:

                        for value in row:

                            add_name(
                                value
                            )

                except Exception as e:

                    print(
                        "Employee lookup warning:",
                        e
                    )

            add_name(
                full_name
            )

        except Exception as e:

            print(
                "Doctor Identity Error:",
                e
            )

        print(
            "🔐 Patient Module Doctor Identities:",
            names
        )

        return names

    # =====================================================
    # GET ACTUAL DOCTOR NAME FROM DOCTORS TABLE
    # =====================================================

    def get_actual_doctor_names(
        self
    ):

        candidates = (
            self.get_logged_in_doctor_names()
        )

        if not candidates:

            return []

        actual_names = []

        def add_name(value):

            if value is None:
                return

            value = str(
                value
            ).strip()

            if not value:
                return

            if (
                value.lower()
                not in {
                    name.lower()
                    for name in actual_names
                }
            ):

                actual_names.append(
                    value
                )

        try:

            columns = []

            self.crud.cursor.execute(
                "PRAGMA table_info(doctors)"
            )

            for row in (
                self.crud.cursor.fetchall()
            ):

                if len(row) > 1:

                    columns.append(
                        row[1]
                    )

            identity_columns = [
                column
                for column in (
                    "full_name",
                    "name",
                    "doctor_id",
                    "doctor_code",
                    "email"
                )
                if column in columns
            ]

            if not identity_columns:

                return candidates

            select_columns = []

            for column in (
                "full_name",
                "name",
                "doctor_id",
                "doctor_code",
                "email"
            ):

                if column in columns:

                    select_columns.append(
                        column
                    )

            self.crud.cursor.execute(
                f"""
                SELECT
                    {", ".join(select_columns)}
                FROM doctors
                """
            )

            rows = (
                self.crud.cursor.fetchall()
            )

            for row in rows:

                for candidate in candidates:

                    candidate_text = (
                        str(
                            candidate
                        ).strip().lower()
                    )

                    for index, value in enumerate(
                        row
                    ):

                        if not value:
                            continue

                        value_text = (
                            str(
                                value
                            ).strip().lower()
                        )

                        if (
                            value_text
                            ==
                            candidate_text
                            or
                            candidate_text
                            in value_text
                            or
                            value_text
                            in candidate_text
                        ):

                            # Prefer full_name
                            for idx, column in enumerate(
                                select_columns
                            ):

                                if (
                                    column
                                    in (
                                        "full_name",
                                        "name"
                                    )
                                    and
                                    row[idx]
                                ):

                                    add_name(
                                        row[idx]
                                    )

            # Fallback
            for candidate in candidates:

                add_name(
                    candidate
                )

        except Exception as e:

            print(
                "Doctor Table Lookup Error:",
                e
            )

            for candidate in candidates:

                add_name(
                    candidate
                )

        print(
            "🩺 Patient Module Matched Doctors:",
            actual_names
        )

        return actual_names

    # =====================================================
    # LOAD DOCTORS
    # =====================================================

    def load_doctors(self):

        try:

            # =================================================
            # DOCTOR LOGIN
            # =================================================

            if self.is_doctor():

                doctors = (
                    self.get_actual_doctor_names()
                )

                if not doctors:

                    doctors = (
                        self.get_logged_in_doctor_names()
                    )

                if not doctors:

                    doctors = [
                        "No Doctor"
                    ]

                self.doctor.configure(
                    values=doctors
                )

                self.doctor.set(
                    doctors[0]
                )

                print(
                    "🩺 Doctor Login - Own Doctor:",
                    doctors
                )

                return doctors

            # =================================================
            # ADMIN / SUPER ADMIN
            # =================================================

            rows = (
                self.crud.load_doctors()
            )

            doctor_list = []

            for row in rows:

                if row and row[0]:

                    doctor_list.append(
                        str(
                            row[0]
                        ).strip()
                    )

            if not doctor_list:

                doctor_list = [
                    "Select Doctor"
                ]

            self.doctor.configure(
                values=doctor_list
            )

            self.doctor.set(
                doctor_list[0]
            )

            return doctor_list

        except Exception as e:

            print(
                "Load Doctors Error:",
                e
            )

            try:

                self.doctor.configure(
                    values=[
                        "Select Doctor"
                    ]
                )

                self.doctor.set(
                    "Select Doctor"
                )

            except Exception:
                pass

            return []

    # =====================================================
    # BIND EVENTS
    # =====================================================

    def bind_events(self):

        try:

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
                lambda event:
                self.search_patient()
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

        except Exception as e:

            print(
                "Patient Event Binding Error:",
                e
            )

    # =====================================================
    # UPLOAD PATIENT PHOTO
    # =====================================================

    def upload_photo(self):

        file_path = filedialog.askopenfilename(
            title="Select Patient Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                ),
                (
                    "JPG Files",
                    "*.jpg"
                ),
                (
                    "PNG Files",
                    "*.png"
                )
            ]
        )

        if not file_path:

            return

        try:

            patient_id = (
                self.patient_id
                .get()
                .strip()
            )

            if not patient_id:

                messagebox.showwarning(
                    "Warning",
                    "Patient ID not available."
                )

                return

            # -------------------------------------------------
            # Max size 2 MB
            # -------------------------------------------------

            file_size = os.path.getsize(
                file_path
            )

            if file_size > (
                2 * 1024 * 1024
            ):

                messagebox.showerror(
                    "File Too Large",
                    "Patient photo must be less than 2 MB."
                )

                return

            folder = os.path.join(
                "assets",
                "patients"
            )

            os.makedirs(
                folder,
                exist_ok=True
            )

            destination = os.path.join(
                folder,
                patient_id + ".jpg"
            )

            image = Image.open(
                file_path
            )

            if image.mode != "RGB":

                image = image.convert(
                    "RGB"
                )

            image.thumbnail(
                (
                    300,
                    400
                )
            )

            image.save(
                destination,
                "JPEG",
                quality=90
            )

            display_image = Image.open(
                destination
            )

            display_image.thumbnail(
                (
                    120,
                    140
                )
            )

            self.photo = ctk.CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=(
                    120,
                    140
                )
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

    # =====================================================
    # ADD PATIENT
    # =====================================================

    def add_patient(self):

        try:

            patient_name = (
                self.patient_name
                .get()
                .strip()
            )

            gender = (
                self.gender.get()
            )

            dob = (
                self.dob
                .get()
                .strip()
            )

            age = (
                self.age
                .get()
                .strip()
            )

            blood_group = (
                self.blood_group.get()
            )

            mobile = (
                self.mobile
                .get()
                .strip()
            )

            email = (
                self.email
                .get()
                .strip()
            )

            address = (
                self.address
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )

            city = (
                self.city
                .get()
                .strip()
            )

            state = (
                self.state
                .get()
                .strip()
            )

            pin_code = (
                self.pin_code
                .get()
                .strip()
            )

            aadhaar = (
                self.aadhaar
                .get()
                .strip()
            )

            doctor = (
                self.doctor.get()
            )

            department = (
                self.department.get()
            )

            patient_type = (
                self.patient_type.get()
            )

            status = (
                self.status.get()
            )

            # =================================================
            # Doctor Security
            # =================================================

            if self.is_doctor():

                allowed_doctors = (
                    self.get_actual_doctor_names()
                )

                if not allowed_doctors:

                    allowed_doctors = (
                        self.get_logged_in_doctor_names()
                    )

                allowed = any(
                    str(
                        name
                    ).strip().lower()
                    ==
                    str(
                        doctor
                    ).strip().lower()
                    for name in allowed_doctors
                )

                if not allowed:

                    messagebox.showerror(
                        "Permission Denied",
                        "Doctor can add only patients assigned to own name."
                    )

                    return

            # =================================================
            # Validation
            # =================================================

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

            # =================================================
            # Duplicate Mobile
            # =================================================

            duplicate = (
                self.crud.check_duplicate_mobile(
                    mobile
                )
            )

            if duplicate:

                messagebox.showerror(
                    "Duplicate",
                    "Mobile Number already exists."
                )

                return

            # =================================================
            # Duplicate Aadhaar
            # =================================================

            duplicate = (
                self.crud.check_duplicate_aadhaar(
                    aadhaar
                )
            )

            if duplicate:

                messagebox.showerror(
                    "Duplicate",
                    "Aadhaar Number already exists."
                )

                return

            # =================================================
            # Optional Father/Husband + Disease
            # =================================================

            father_husband_name = ""

            disease = ""

            if hasattr(
                self,
                "father_husband_name"
            ):

                try:

                    father_husband_name = (
                        self.father_husband_name
                        .get()
                        .strip()
                    )

                except Exception:
                    father_husband_name = ""

            if hasattr(
                self,
                "disease"
            ):

                try:

                    disease = (
                        self.disease
                        .get()
                        .strip()
                    )

                except Exception:
                    disease = ""

            # =================================================
            # Save
            # =================================================

            if self.api_client:

                print(
                    "?? Adding Patient through Central API..."
                )

                payload = {
                    "patient_name": patient_name,
                    "name": patient_name,
                    "gender": gender,
                    "dob": dob,
                    "age": age,
                    "blood_group": blood_group,
                    "mobile": mobile,
                    "email": email,
                    "address": address,
                    "city": city,
                    "state": state,
                    "pin_code": pin_code,
                    "aadhaar": aadhaar,
                    "disease": disease,
                    "doctor": doctor,
                    "department": department,
                    "patient_type": patient_type,
                    "assigned_doctor": doctor,
                    "status": status,
                    "father_husband_name": father_husband_name
                }

                api_result = self.api_client.request(
                    "POST",
                    "/api/v1/modules/patients/records",
                    json={"data": payload}
                )

                success = bool(
                    isinstance(api_result, dict)
                    and api_result.get("ok")
                )

                print(
                    "? Central Patient Created:",
                    api_result
                )

            else:

                success = (
                    self.crud.add_patient(
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
                        status,
                        father_husband_name,
                        disease
                    )
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

        except Exception as e:

            print(
                "Add Patient Controller Error:",
                e
            )

            messagebox.showerror(
                "Error",
                f"Unable to add patient.\n\n{e}"
            )

    # =====================================================
    # LOAD PATIENTS
    # =====================================================

    def load_patients(self):

        try:

            # -------------------------------------------------
            # Clear table
            # -------------------------------------------------

            for item in self.patient_table.get_children():
                self.patient_table.delete(item)

            # =================================================
            # API MODE
            # =================================================

            if self.api_client:

                print("?? Loading Patients from Central API...")

                response = self.api_client.request(
                    "GET",
                    "/api/v1/modules/patients/records",
                    params={
                        "limit": 100,
                        "offset": 0,
                        "search": ""
                    }
                )

                items = response.get("items", []) if isinstance(response, dict) else []

                # =================================================
                # DOCTOR LOGIN FILTER
                # =================================================

                if self.is_doctor():

                    doctor_names = self.get_actual_doctor_names()

                    if not doctor_names:
                        doctor_names = self.get_logged_in_doctor_names()

                    normalized_doctors = {
                        str(name).strip().lower()
                        for name in doctor_names
                        if name
                    }

                    if not normalized_doctors:
                        print("? Doctor identity not found.")
                        return

                    filtered_items = []

                    for item in items:

                        assigned_doctor = str(
                            item.get("assigned_doctor")
                            or item.get("doctor")
                            or ""
                        ).strip().lower()

                        if assigned_doctor in normalized_doctors:
                            filtered_items.append(item)

                    items = filtered_items

                    print(
                        "???? Doctor Patient Filter:",
                        doctor_names
                    )

                    print(
                        "???? Assigned Patient Count:",
                        len(items)
                    )

                else:

                    print(
                        "?? All Patients Count:",
                        len(items)
                    )

                # =================================================
                # API ITEM -> EXISTING TABLE ROW
                # =================================================

                rows = []

                for item in items:

                    rows.append(
                        (
                            item.get("id", ""),
                            item.get("patient_id", ""),
                            item.get("registration_no", ""),
                            item.get("patient_name")
                            or item.get("name")
                            or "",
                            item.get("gender", ""),
                            item.get("age", ""),
                            item.get("mobile", ""),
                            item.get("assigned_doctor")
                            or item.get("doctor")
                            or "",
                            item.get("department", ""),
                            item.get("status", "")
                        )
                    )

            # =================================================
            # LOCAL FALLBACK
            # =================================================

            else:

                print(
                    "?? API client unavailable - using local patient data."
                )

                if self.is_doctor():

                    doctor_names = self.get_actual_doctor_names()

                    if not doctor_names:
                        doctor_names = self.get_logged_in_doctor_names()

                    if not doctor_names:

                        print(
                            "? Doctor identity not found."
                        )

                        return

                    conditions = []
                    params = []

                    for doctor_name in doctor_names:

                        conditions.append(
                            """
                            LOWER(TRIM(doctor))
                            =
                            LOWER(TRIM(?))
                            """
                        )

                        params.append(
                            doctor_name
                        )

                    query = (
                        """
                        SELECT
                            id,
                            patient_id,
                            registration_no,
                            patient_name,
                            gender,
                            age,
                            mobile,
                            doctor,
                            department,
                            status
                        FROM patients
                        WHERE
                            (
                        """
                        + " OR ".join(conditions)
                        + """
                            )
                        ORDER BY id DESC
                        """
                    )

                    self.crud.cursor.execute(
                        query,
                        tuple(params)
                    )

                    rows = self.crud.cursor.fetchall()

                    print(
                        "???? Doctor Patient Filter:",
                        doctor_names
                    )

                    print(
                        "???? Assigned Patient Count:",
                        len(rows)
                    )

                else:

                    rows = self.crud.load_patients()

                    print(
                        "?? All Patients Count:",
                        len(rows)
                    )

            # =================================================
            # DISPLAY
            # =================================================

            for row in rows:

                self.patient_table.insert(
                    "",
                    "end",
                    values=row
                )

            print(
                "? Patient Table Loaded:",
                len(rows)
            )

        except Exception as e:

            print(
                "Load Patients Error:",
                e
            )

    # =====================================================
    # LOAD SELECTED PATIENT
    # =====================================================

    def load_selected_patient(
        self,
        event=None
    ):

        try:

            selected = (
                self.patient_table.focus()
            )

            if not selected:

                return

            values = (
                self.patient_table.item(
                    selected,
                    "values"
                )
            )

            if not values:

                return

            patient_db_id = values[0]

            patient = (
                self.crud.get_patient_by_id(
                    patient_db_id
                )
            )

            if not patient:

                return

            # =================================================
            # Doctor security
            # =================================================

            if self.is_doctor():

                allowed_doctors = (
                    self.get_actual_doctor_names()
                )

                if not allowed_doctors:

                    allowed_doctors = (
                        self.get_logged_in_doctor_names()
                    )

                patient_doctor = str(
                    patient[15] or ""
                ).strip().lower()

                allowed = any(
                    patient_doctor
                    ==
                    str(
                        doctor_name
                    ).strip().lower()
                    for doctor_name in allowed_doctors
                )

                if not allowed:

                    messagebox.showerror(
                        "Permission Denied",
                        "You cannot access this patient."
                    )

                    return

            # =================================================
            # Save selected ID
            # =================================================

            self.selected_patient_id = (
                patient[0]
            )

            # =================================================
            # Patient ID
            # =================================================

            self.patient_id.configure(
                state="normal"
            )

            self.patient_id.delete(
                0,
                "end"
            )

            self.patient_id.insert(
                0,
                patient[1]
            )

            self.patient_id.configure(
                state="disabled"
            )

            # =================================================
            # Registration Number
            # =================================================

            self.registration_no.configure(
                state="normal"
            )

            self.registration_no.delete(
                0,
                "end"
            )

            self.registration_no.insert(
                0,
                patient[2]
            )

            self.registration_no.configure(
                state="disabled"
            )

            # =================================================
            # Name
            # =================================================

            self.patient_name.delete(
                0,
                "end"
            )

            self.patient_name.insert(
                0,
                patient[3]
            )

            # =================================================
            # Gender
            # =================================================

            self.gender.set(
                patient[4]
                or
                ""
            )

            # =================================================
            # DOB
            # =================================================

            self.dob.delete(
                0,
                "end"
            )

            self.dob.insert(
                0,
                patient[5]
                or
                ""
            )

            # =================================================
            # Age
            # =================================================

            self.age.delete(
                0,
                "end"
            )

            self.age.insert(
                0,
                str(
                    patient[6]
                    or
                    ""
                )
            )

            # =================================================
            # Blood Group
            # =================================================

            self.blood_group.set(
                patient[7]
                or
                ""
            )

            # =================================================
            # Mobile
            # =================================================

            self.mobile.delete(
                0,
                "end"
            )

            self.mobile.insert(
                0,
                patient[8]
                or
                ""
            )

            # =================================================
            # Email
            # =================================================

            self.email.delete(
                0,
                "end"
            )

            self.email.insert(
                0,
                patient[9]
                or
                ""
            )

            # =================================================
            # Address
            # =================================================

            self.address.delete(
                "1.0",
                "end"
            )

            self.address.insert(
                "1.0",
                patient[10]
                or
                ""
            )

            # =================================================
            # City
            # =================================================

            self.city.delete(
                0,
                "end"
            )

            self.city.insert(
                0,
                patient[11]
                or
                ""
            )

            # =================================================
            # State
            # =================================================

            self.state.delete(
                0,
                "end"
            )

            self.state.insert(
                0,
                patient[12]
                or
                ""
            )

            # =================================================
            # Pin Code
            # =================================================

            self.pin_code.delete(
                0,
                "end"
            )

            self.pin_code.insert(
                0,
                patient[13]
                or
                ""
            )

            # =================================================
            # Aadhaar
            # =================================================

            self.aadhaar.delete(
                0,
                "end"
            )

            self.aadhaar.insert(
                0,
                patient[14]
                or
                ""
            )

            # =================================================
            # Doctor
            # =================================================

            self.doctor.set(
                patient[15]
                or
                ""
            )

            # =================================================
            # Department
            # =================================================

            self.department.set(
                patient[16]
                or
                ""
            )

            # =================================================
            # Patient Type
            # =================================================

            self.patient_type.set(
                patient[17]
                or
                ""
            )

            # =================================================
            # Status
            # =================================================

            self.status.set(
                patient[18]
                or
                ""
            )

            print(
                "✅ Patient Selected:",
                patient[3]
            )

        except Exception as e:

            print(
                "Load Selected Patient Error:",
                e
            )

    # =====================================================
    # UPDATE PATIENT
    # =====================================================

    def update_patient(self):

        try:

            if not getattr(
                self,
                "selected_patient_id",
                None
            ):

                messagebox.showwarning(
                    "Warning",
                    "Please select a patient."
                )

                return

            # =================================================
            # Re-check selected patient
            # =================================================

            selected_patient = (
                self.crud.get_patient_by_id(
                    self.selected_patient_id
                )
            )

            if not selected_patient:

                self.selected_patient_id = None

                messagebox.showerror(
                    "Error",
                    "Selected patient no longer exists."
                )

                return

            # =================================================
            # Doctor security
            # =================================================

            if self.is_doctor():

                allowed_doctors = (
                    self.get_actual_doctor_names()
                )

                if not allowed_doctors:

                    allowed_doctors = (
                        self.get_logged_in_doctor_names()
                    )

                current_doctor = str(
                    selected_patient[15]
                    or
                    ""
                ).strip().lower()

                allowed = any(
                    current_doctor
                    ==
                    str(
                        doctor_name
                    ).strip().lower()
                    for doctor_name in allowed_doctors
                )

                if not allowed:

                    messagebox.showerror(
                        "Permission Denied",
                        "You can update only your own patients."
                    )

                    return

                # -------------------------------------------------
                # Prevent changing patient to another doctor
                # -------------------------------------------------

                selected_doctor = str(
                    self.doctor.get()
                ).strip()

                allowed_new_doctor = any(
                    selected_doctor.lower()
                    ==
                    str(
                        doctor_name
                    ).strip().lower()
                    for doctor_name in allowed_doctors
                )

                if not allowed_new_doctor:

                    messagebox.showerror(
                        "Permission Denied",
                        "Doctor cannot reassign patient to another doctor."
                    )

                    return

            # =================================================
            # Duplicate Mobile
            # =================================================

            duplicate = (
                self.crud.check_duplicate_mobile(
                    self.mobile.get().strip(),
                    self.selected_patient_id
                )
            )

            if duplicate:

                messagebox.showerror(
                    "Duplicate",
                    "Mobile Number already exists."
                )

                return

            # =================================================
            # Duplicate Aadhaar
            # =================================================

            duplicate = (
                self.crud.check_duplicate_aadhaar(
                    self.aadhaar.get().strip(),
                    self.selected_patient_id
                )
            )

            if duplicate:

                messagebox.showerror(
                    "Duplicate",
                    "Aadhaar Number already exists."
                )

                return

            # =================================================
            # Optional Father/Husband + Disease
            # =================================================

            father_husband_name = ""

            disease = ""

            if hasattr(
                self,
                "father_husband_name"
            ):

                try:

                    father_husband_name = (
                        self.father_husband_name
                        .get()
                        .strip()
                    )

                except Exception:
                    father_husband_name = ""

            if hasattr(
                self,
                "disease"
            ):

                try:

                    disease = (
                        self.disease
                        .get()
                        .strip()
                    )

                except Exception:
                    disease = ""

            # =================================================
            # Update
            # =================================================

            # =================================================
            # CLOUD API UPDATE
            # =================================================

            if self.api_client:

                payload = {
                    "patient_name": self.patient_name.get().strip(),
                    "name": self.patient_name.get().strip(),
                    "gender": self.gender.get(),
                    "dob": self.dob.get().strip(),
                    "age": self.age.get().strip(),
                    "blood_group": self.blood_group.get(),
                    "mobile": self.mobile.get().strip(),
                    "email": self.email.get().strip(),
                    "address": self.address.get("1.0", "end").strip(),
                    "city": self.city.get().strip(),
                    "state": self.state.get().strip(),
                    "pin_code": self.pin_code.get().strip(),
                    "aadhaar": self.aadhaar.get().strip(),
                    "doctor": self.doctor.get(),
                    "department": self.department.get(),
                    "patient_type": self.patient_type.get(),
                    "status": self.status.get(),
                    "father_husband_name": father_husband_name,
                    "disease": disease,
                }

                api_result = self.api_client.request(
                    "PUT",
                    f"/api/v1/modules/patients/records/{self.selected_patient_id}",
                    json={"data": payload}
                )

                if api_result.get("ok"):
                    messagebox.showinfo(
                        "Success",
                        "Patient updated successfully."
                    )

                    selected_id = self.selected_patient_id
                    self.load_patients()
                    self.selected_patient_id = selected_id
                    return

                messagebox.showerror(
                    "Error",
                    "Unable to update patient on the hospital server."
                )
                return


            success = (
                self.crud.update_patient(
                    self.selected_patient_id,
                    self.patient_name.get().strip(),
                    self.gender.get(),
                    self.dob.get().strip(),
                    self.age.get().strip(),
                    self.blood_group.get(),
                    self.mobile.get().strip(),
                    self.email.get().strip(),
                    self.address.get(
                        "1.0",
                        "end"
                    ).strip(),
                    self.city.get().strip(),
                    self.state.get().strip(),
                    self.pin_code.get().strip(),
                    self.aadhaar.get().strip(),
                    self.doctor.get(),
                    self.department.get(),
                    self.patient_type.get(),
                    self.status.get(),
                    father_husband_name,
                    disease
                )
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Patient updated successfully."
                )

                selected_id = (
                    self.selected_patient_id
                )

                self.load_patients()

                self.selected_patient_id = (
                    selected_id
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to update patient."
                )

        except Exception as e:

            print(
                "Update Patient Error:",
                e
            )

            messagebox.showerror(
                "Error",
                f"Unable to update patient.\n\n{e}"
            )

    # =====================================================
    # DELETE PATIENT
    # =====================================================

    def delete_patient(self):

        try:

            selected = (
                self.patient_table.focus()
            )

            if not selected:

                messagebox.showwarning(
                    "Warning",
                    "Please select a patient."
                )

                return

            values = (
                self.patient_table.item(
                    selected,
                    "values"
                )
            )

            if not values:

                return

            patient_db_id = (
                values[0]
            )

            # =================================================
            # Doctor security
            # =================================================

            if self.is_doctor():

                patient = (
                    self.crud.get_patient_by_id(
                        patient_db_id
                    )
                )

                if not patient:

                    messagebox.showerror(
                        "Error",
                        "Patient not found."
                    )

                    return

                allowed_doctors = (
                    self.get_actual_doctor_names()
                )

                if not allowed_doctors:

                    allowed_doctors = (
                        self.get_logged_in_doctor_names()
                    )

                patient_doctor = str(
                    patient[15]
                    or
                    ""
                ).strip().lower()

                allowed = any(
                    patient_doctor
                    ==
                    str(
                        doctor_name
                    ).strip().lower()
                    for doctor_name in allowed_doctors
                )

                if not allowed:

                    messagebox.showerror(
                        "Permission Denied",
                        "You can delete only your own patients."
                    )

                    return

            # =================================================
            # Confirm
            # =================================================

            if not messagebox.askyesno(
                "Confirm",
                "Delete this patient?"
            ):

                return

            # =================================================
            # Delete
            # =================================================

            if self.crud.delete_patient(
                patient_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Patient deleted successfully."
                )

                self.load_patients()

                self.clear_form()

                self.selected_patient_id = None

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to delete patient."
                )

        except Exception as e:

            print(
                "Delete Patient Error:",
                e
            )

            messagebox.showerror(
                "Error",
                f"Unable to delete patient.\n\n{e}"
            )

    # =====================================================
    # SEARCH PATIENT
    # =====================================================

    def search_patient(self):

        try:

            keyword = (
                self.search_entry
                .get()
                .strip()
            )

            # -------------------------------------------------
            # Clear table
            # -------------------------------------------------

            for item in (
                self.patient_table
                .get_children()
            ):

                self.patient_table.delete(
                    item
                )

            # =================================================
            # API MODE
            # =================================================

            if self.api_client:

                print(
                    "?? Searching Patients through Central API..."
                )

                response = self.api_client.request(
                    "GET",
                    "/api/v1/modules/patients/records",
                    params={
                        "limit": 100,
                        "offset": 0,
                        "search": keyword
                    }
                )

                items = (
                    response.get("items", [])
                    if isinstance(response, dict)
                    else []
                )

                # =================================================
                # DOCTOR SEARCH FILTER
                # =================================================

                if self.is_doctor():

                    doctor_names = (
                        self.get_actual_doctor_names()
                    )

                    if not doctor_names:

                        doctor_names = (
                            self.get_logged_in_doctor_names()
                        )

                    normalized_doctors = {
                        str(name).strip().lower()
                        for name in doctor_names
                        if name
                    }

                    if not normalized_doctors:

                        return

                    filtered_items = []

                    for item in items:

                        assigned_doctor = str(
                            item.get("assigned_doctor")
                            or item.get("doctor")
                            or ""
                        ).strip().lower()

                        if assigned_doctor in normalized_doctors:

                            filtered_items.append(
                                item
                            )

                    items = filtered_items

                # =================================================
                # API ITEM -> EXISTING TABLE ROW
                # =================================================

                rows = []

                for item in items:

                    rows.append(
                        (
                            item.get("id", ""),
                            item.get("patient_id", ""),
                            item.get("registration_no", ""),
                            item.get("patient_name")
                            or item.get("name")
                            or "",
                            item.get("gender", ""),
                            item.get("age", ""),
                            item.get("mobile", ""),
                            item.get("assigned_doctor")
                            or item.get("doctor")
                            or "",
                            item.get("department", ""),
                            item.get("status", "")
                        )
                    )

            # =================================================
            # LOCAL FALLBACK
            # =================================================

            else:

                if self.is_doctor():

                    doctor_names = (
                        self.get_actual_doctor_names()
                    )

                    if not doctor_names:

                        doctor_names = (
                            self.get_logged_in_doctor_names()
                        )

                    if not doctor_names:

                        return

                    doctor_conditions = []
                    params = []

                    for doctor_name in doctor_names:

                        doctor_conditions.append(
                            """
                            LOWER(TRIM(doctor))
                            =
                            LOWER(TRIM(?))
                            """
                        )

                        params.append(
                            doctor_name
                        )

                    search_value = (
                        f"%{keyword}%"
                    )

                    search_conditions = """
                        (
                            patient_id LIKE ?
                            OR registration_no LIKE ?
                            OR patient_name LIKE ?
                            OR mobile LIKE ?
                            OR email LIKE ?
                            OR address LIKE ?
                            OR city LIKE ?
                            OR state LIKE ?
                            OR aadhaar LIKE ?
                            OR disease LIKE ?
                            OR doctor LIKE ?
                            OR department LIKE ?
                            OR patient_type LIKE ?
                            OR status LIKE ?
                        )
                    """

                    params.extend(
                        [
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value,
                            search_value
                        ]
                    )

                    query = (
                        """
                        SELECT
                            id,
                            patient_id,
                            registration_no,
                            patient_name,
                            gender,
                            age,
                            mobile,
                            doctor,
                            department,
                            status
                        FROM patients
                        WHERE
                            (
                                """
                        + " OR ".join(
                            doctor_conditions
                        )
                        + """
                            )
                        AND
                            """
                        + search_conditions
                        + """
                        ORDER BY id DESC
                        """
                    )

                    self.crud.cursor.execute(
                        query,
                        tuple(params)
                    )

                    rows = (
                        self.crud.cursor.fetchall()
                    )

                else:

                    rows = (
                        self.crud.search_patient(
                            keyword
                        )
                    )

            # =================================================
            # DISPLAY
            # =================================================

            for row in rows:

                self.patient_table.insert(
                    "",
                    "end",
                    values=row
                )

            print(
                "?? Patient Search Results:",
                len(rows)
            )

        except Exception as e:

            print(
                "Patient Search Error:",
                e
            )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        try:

            # -------------------------------------------------
            # Patient ID
            # -------------------------------------------------

            self.patient_id.configure(
                state="normal"
            )

            self.patient_id.delete(
                0,
                "end"
            )

            self.patient_id.insert(
                0,
                self.crud.generate_patient_id()
            )

            self.patient_id.configure(
                state="disabled"
            )

            # -------------------------------------------------
            # Registration
            # -------------------------------------------------

            self.registration_no.configure(
                state="normal"
            )

            self.registration_no.delete(
                0,
                "end"
            )

            self.registration_no.insert(
                0,
                self.crud.generate_registration_no()
            )

            self.registration_no.configure(
                state="disabled"
            )

            # -------------------------------------------------
            # Basic fields
            # -------------------------------------------------

            self.patient_name.delete(
                0,
                "end"
            )

            self.gender.set(
                "Male"
            )

            self.dob.delete(
                0,
                "end"
            )

            self.age.delete(
                0,
                "end"
            )

            self.blood_group.set(
                "O+"
            )

            self.mobile.delete(
                0,
                "end"
            )

            self.email.delete(
                0,
                "end"
            )

            self.address.delete(
                "1.0",
                "end"
            )

            self.city.delete(
                0,
                "end"
            )

            self.state.delete(
                0,
                "end"
            )

            self.pin_code.delete(
                0,
                "end"
            )

            self.aadhaar.delete(
                0,
                "end"
            )

            # -------------------------------------------------
            # Doctor
            # -------------------------------------------------

            if self.is_doctor():

                doctors = (
                    self.get_actual_doctor_names()
                )

                if not doctors:

                    doctors = (
                        self.get_logged_in_doctor_names()
                    )

                if doctors:

                    self.doctor.set(
                        doctors[0]
                    )

                else:

                    self.doctor.set(
                        "No Doctor"
                    )

            else:

                self.doctor.set(
                    "Select Doctor"
                )

            # -------------------------------------------------
            # Other
            # -------------------------------------------------

            self.department.set(
                "General Medicine"
            )

            self.patient_type.set(
                "OPD"
            )

            self.status.set(
                "Active"
            )

            # -------------------------------------------------
            # Optional fields
            # -------------------------------------------------

            if hasattr(
                self,
                "father_husband_name"
            ):

                try:

                    self.father_husband_name.delete(
                        0,
                        "end"
                    )

                except Exception:
                    pass

            if hasattr(
                self,
                "disease"
            ):

                try:

                    self.disease.delete(
                        0,
                        "end"
                    )

                except Exception:
                    pass

            self.selected_patient_id = None

        except Exception as e:

            print(
                "Clear Patient Form Error:",
                e
            )

    # =====================================================
    # CALCULATE AGE
    # =====================================================

    def calculate_age(
        self,
        event=None
    ):

        try:

            dob_text = (
                self.dob
                .get()
                .strip()
            )

            dob = datetime.strptime(
                dob_text,
                "%d-%m-%Y"
            ).date()

            today = date.today()

            age = (
                today.year
                -
                dob.year
            )

            if (
                today.month,
                today.day
            ) < (
                dob.month,
                dob.day
            ):

                age -= 1

            self.age.configure(
                state="normal"
            )

            self.age.delete(
                0,
                "end"
            )

            self.age.insert(
                0,
                str(age)
            )

            self.age.configure(
                state="readonly"
            )

        except Exception:

            pass

    # =====================================================
    # REFRESH PATIENT LIST
    # =====================================================

    def refresh_patients(self):

        try:

            if hasattr(
                self,
                "search_entry"
            ):

                self.search_entry.delete(
                    0,
                    "end"
                )

            self.selected_patient_id = None

            self.load_doctors()
            self.load_patients()

            print(
                "🔄 Patient List Refreshed"
            )

        except Exception as e:

            print(
                "Refresh Patients Error:",
                e
            )
