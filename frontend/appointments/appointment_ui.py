"""
===========================================================
Cloud Secure Hospital ERP
Appointment Management UI
Version : 6.0
===========================================================

Features:
- Patient selection
- Father / Husband Name
- Disease
- Doctor
- Department
- Appointment Date
- Appointment Time
- Visit Type
- Token
- Status
- Remarks
- Search
- Refresh
- Add / Update / Delete / Clear
- Horizontal + Vertical scrolling
- Appointment row selection
- Doctor role compatibility
===========================================================
"""

import customtkinter as ctk


class AppointmentUI:

    # ======================================================
    # INITIALIZE
    # ======================================================

    def __init__(
        self,
        parent,
        controller=None
    ):

        self.parent = parent
        self.controller = controller

        # ==================================================
        # VARIABLES
        # ==================================================

        self.patient_var = ctk.StringVar()

        self.father_var = ctk.StringVar()

        self.disease_var = ctk.StringVar()

        self.doctor_var = ctk.StringVar()

        self.department_var = ctk.StringVar()

        self.date_var = ctk.StringVar()

        self.time_var = ctk.StringVar()

        self.visit_type_var = ctk.StringVar(
            value="OPD"
        )

        self.token_var = ctk.StringVar()

        self.status_var = ctk.StringVar(
            value="Pending"
        )

        self.search_var = ctk.StringVar()

        # ==================================================
        # SELECTION
        # ==================================================

        self.selected_id = None

        self.selected_appointment_id = None

        # ==================================================
        # BUILD UI
        # ==================================================

        self.build_ui()

    # ======================================================
    # ROLE
    # ======================================================

    def get_role(self):

        if not self.controller:
            return ""

        role = getattr(
            self.controller,
            "role",
            ""
        )

        if not role:

            role = getattr(
                self.controller,
                "current_role",
                ""
            )

        return str(
            role
        ).strip()

    # ======================================================
    # USER
    # ======================================================

    def get_user(self):

        if not self.controller:
            return None

        return getattr(
            self.controller,
            "user",
            None
        )

    # ======================================================
    # MAIN UI
    # ======================================================

    def build_ui(self):

        # ==================================================
        # MAIN FRAME
        # ==================================================

        self.main_frame = ctk.CTkFrame(
            self.parent,
            corner_radius=12
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ==================================================
        # TITLE
        # ==================================================

        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        title_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        self.title_label = ctk.CTkLabel(
            title_frame,
            text="📅 Appointment Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.title_label.pack(
            side="left"
        )

        # ==================================================
        # SEARCH AREA
        # ==================================================

        search_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text=(
                "Search Patient / Doctor / "
                "Appointment ID..."
            ),
            width=400,
            height=40
        )

        self.search_entry.pack(
            side="left",
            padx=(0, 10)
        )

        self.search_button = ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            width=120,
            height=40,
            command=self.search_clicked
        )

        self.search_button.pack(
            side="left"
        )

        self.refresh_button = ctk.CTkButton(
            search_frame,
            text="↻ Refresh",
            width=120,
            height=40,
            command=self.refresh_clicked
        )

        self.refresh_button.pack(
            side="left",
            padx=10
        )

        # ==================================================
        # FORM FRAME
        # ==================================================

        self.form_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.form_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ==================================================
        # COLUMN CONFIGURATION
        # ==================================================

        for column in range(3):

            self.form_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # ==================================================
        # PATIENT
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Patient Name",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.patient_combo = ctk.CTkComboBox(
            self.form_frame,
            variable=self.patient_var,
            values=["No Patient"],
            width=260,
            height=38,
            command=self.patient_selected
        )

        self.patient_combo.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # FATHER / HUSBAND
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Father / Husband Name",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.father_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.father_var,
            width=260,
            height=38,
            placeholder_text="Father / Husband Name"
        )

        self.father_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # DISEASE
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Disease",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.disease_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.disease_var,
            width=260,
            height=38,
            placeholder_text="Disease"
        )

        self.disease_entry.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # DOCTOR
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Doctor",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.doctor_combo = ctk.CTkComboBox(
            self.form_frame,
            variable=self.doctor_var,
            values=["No Doctor"],
            width=260,
            height=38,
            command=self.doctor_selected
        )

        self.doctor_combo.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # DEPARTMENT
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Department",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=2,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.department_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.department_var,
            width=260,
            height=38
        )

        self.department_entry.grid(
            row=3,
            column=1,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # DATE
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Appointment Date",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.date_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.date_var,
            width=260,
            height=38,
            placeholder_text="DD/MM/YYYY"
        )

        self.date_entry.grid(
            row=3,
            column=2,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # TIME
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Appointment Time",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.time_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.time_var,
            width=260,
            height=38,
            placeholder_text="10:00 AM"
        )

        self.time_entry.grid(
            row=5,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # VISIT TYPE
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Visit Type",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=4,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.visit_combo = ctk.CTkComboBox(
            self.form_frame,
            variable=self.visit_type_var,
            values=[
                "OPD",
                "IPD",
                "Follow-up",
                "Emergency"
            ],
            width=260,
            height=38
        )

        self.visit_combo.grid(
            row=5,
            column=1,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # TOKEN
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Token No",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=4,
            column=2,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.token_entry = ctk.CTkEntry(
            self.form_frame,
            textvariable=self.token_var,
            width=260,
            height=38
        )

        self.token_entry.grid(
            row=5,
            column=2,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # STATUS
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Status",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=6,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.status_combo = ctk.CTkComboBox(
            self.form_frame,
            variable=self.status_var,
            values=[
                "Pending",
                "Confirmed",
                "Completed",
                "Cancelled"
            ],
            width=260,
            height=38
        )

        self.status_combo.grid(
            row=7,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # REMARKS
        # ==================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Remarks",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=6,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.remarks_entry = ctk.CTkEntry(
            self.form_frame,
            width=550,
            height=38,
            placeholder_text="Remarks"
        )

        self.remarks_entry.grid(
            row=7,
            column=1,
            columnspan=2,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # ==================================================
        # BUTTON FRAME
        # ==================================================

        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ==================================================
        # ADD
        # ==================================================

        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="➕ Add Appointment",
            width=160,
            height=40,
            command=self.add_clicked
        )

        self.add_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # UPDATE
        # ==================================================

        self.update_button = ctk.CTkButton(
            self.button_frame,
            text="✏ Update",
            width=130,
            height=40,
            command=self.update_clicked
        )

        self.update_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # DELETE
        # ==================================================

        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="🗑 Delete",
            width=130,
            height=40,
            command=self.delete_clicked
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # CLEAR
        # ==================================================

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            width=120,
            height=40,
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # OLD VARIABLE COMPATIBILITY
        # ==================================================

        self.add_btn = self.add_button

        self.update_btn = self.update_button

        self.delete_btn = self.delete_button

        self.clear_btn = self.clear_button

        # ==================================================
        # APPOINTMENT LIST CONTAINER
        # ==================================================

        self.table_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # ==================================================
        # TABLE TITLE
        # ==================================================

        self.table_title = ctk.CTkLabel(
            self.table_frame,
            text="Appointment List",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.table_title.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        # ==================================================
        # TABLE CANVAS FRAME
        # ==================================================

        self.canvas_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )

        self.canvas_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(5, 8)
        )

        # ==================================================
        # CANVAS
        # ==================================================

        self.table_canvas = ctk.CTkCanvas(
            self.canvas_frame,
            highlightthickness=0,
            borderwidth=0
        )

        self.table_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # VERTICAL SCROLLBAR
        # ==================================================

        self.scroll_y = ctk.CTkScrollbar(
            self.canvas_frame,
            orientation="vertical",
            command=self.table_canvas.yview
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # ==================================================
        # HORIZONTAL SCROLLBAR
        # ==================================================

        self.scroll_x = ctk.CTkScrollbar(
            self.table_frame,
            orientation="horizontal",
            command=self.table_canvas.xview
        )

        self.scroll_x.pack(
            side="bottom",
            fill="x",
            padx=8,
            pady=(0, 8)
        )

        # ==================================================
        # SCROLL COMMANDS
        # ==================================================

        self.table_canvas.configure(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        # ==================================================
        # INNER TABLE
        # ==================================================

        self.table = ctk.CTkFrame(
            self.table_canvas,
            fg_color="transparent"
        )

        self.table_window = (
            self.table_canvas.create_window(
                (0, 0),
                window=self.table,
                anchor="nw"
            )
        )

        # ==================================================
        # UPDATE SCROLL REGION
        # ==================================================

        self.table.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.table_canvas.bind(
            "<Configure>",
            self._canvas_configure
        )

        # ==================================================
        # MOUSE WHEEL
        # ==================================================

        self.table_canvas.bind(
            "<MouseWheel>",
            self._on_mousewheel
        )

        # ==================================================
        # INITIAL LOAD
        # ==================================================

        self.load_data()

    # ======================================================
    # SCROLL REGION
    # ======================================================

    def _update_scroll_region(
        self,
        event=None
    ):

        try:

            self.table_canvas.configure(
                scrollregion=(
                    self.table_canvas.bbox(
                        "all"
                    )
                )
            )

        except Exception as e:

            print(
                "Table Scroll Region Error:",
                e
            )

    # ======================================================
    # CANVAS CONFIGURE
    # ======================================================

    def _canvas_configure(
        self,
        event=None
    ):

        try:

            # Do not force width.
            # Keep full table width available
            # so horizontal scroll can work.

            self.table_canvas.configure(
                scrollregion=(
                    self.table_canvas.bbox(
                        "all"
                    )
                )
            )

        except Exception:
            pass

    # ======================================================
    # MOUSE WHEEL
    # ======================================================

    def _on_mousewheel(
        self,
        event
    ):

        try:

            self.table_canvas.yview_scroll(
                int(
                    -1
                    *
                    (event.delta / 120)
                ),
                "units"
            )

        except Exception:
            pass

    # ======================================================
    # CLEAN VALUE
    # ======================================================

    def _clean_value(
        self,
        value
    ):

        if value is None:
            return ""

        value = str(
            value
        ).strip()

        # Never show passwords / hashes.
        if value.startswith(
            "$2b$"
        ):
            return ""

        if value.startswith(
            "$2a$"
        ):
            return ""

        if value.startswith(
            "$2y$"
        ):
            return ""

        return value

    # ======================================================
    # SET DOCTORS
    # ======================================================

    def set_doctors(
        self,
        doctors
    ):

        values = []

        for row in doctors or []:

            if isinstance(
                row,
                (tuple, list)
            ):

                value = (
                    row[0]
                    if len(row) > 0
                    else ""
                )

            else:

                value = row

            value = self._clean_value(
                value
            )

            if not value:
                continue

            if value.lower() in (
                "password",
                "username",
                "no doctor"
            ):

                continue

            if value not in values:

                values.append(
                    value
                )

        # ==================================================
        # Doctor role -> only own doctor
        # ==================================================

        if (
            self.get_role().lower()
            == "doctor"
        ):

            logged_names = (
                self.get_logged_in_doctor_names()
            )

            if logged_names:

                matched = []

                for doctor in values:

                    if self.names_match(
                        doctor,
                        logged_names
                    ):

                        matched.append(
                            doctor
                        )

                values = matched

        if not values:

            values = [
                "No Doctor"
            ]

        self.doctor_combo.configure(
            values=values
        )

        # Automatically select only doctor.

        if (
            len(values) == 1
            and
            values[0] != "No Doctor"
        ):

            self.doctor_var.set(
                values[0]
            )

            self.doctor_selected(
                values[0]
            )

        elif (
            self.doctor_var.get()
            not in values
        ):

            self.doctor_var.set(
                values[0]
            )

    # ======================================================
    # GET LOGGED-IN DOCTOR NAMES
    # ======================================================

    def get_logged_in_doctor_names(
        self
    ):

        names = []

        user = self.get_user()

        if not user:

            return names

        def add_name(
            value
        ):

            if value is None:
                return

            value = self._clean_value(
                value
            )

            if not value:
                return

            if value.lower() in (
                "password",
                "username"
            ):

                return

            if value.lower() not in {
                item.lower()
                for item in names
            }:

                names.append(
                    value
                )

        try:

            # =================================================
            # Tuple / List
            # =================================================

            if isinstance(
                user,
                (tuple, list)
            ):

                # Existing login record typically:
                # [employee_id, full_name,
                #  username, password_hash, ...]

                for index in (
                    0,
                    1,
                    2
                ):

                    if len(user) > index:

                        value = user[index]

                        if value:

                            # Do not add obvious hashes.
                            if str(
                                value
                            ).startswith("$2"):

                                continue

                            add_name(
                                value
                            )

            # =================================================
            # Dictionary
            # =================================================

            elif isinstance(
                user,
                dict
            ):

                for field in (
                    "employee_id",
                    "doctor_id",
                    "doctor_code",
                    "full_name",
                    "doctor_name",
                    "name",
                    "display_name",
                    "username",
                    "user_name"
                ):

                    if field in user:

                        add_name(
                            user.get(
                                field
                            )
                        )

            # =================================================
            # Other / String
            # =================================================

            else:

                add_name(
                    user
                )

        except Exception as e:

            print(
                "Doctor Identity Error:",
                e
            )

        return names

    # ======================================================
    # DOCTOR NAME MATCH
    # ======================================================

    def names_match(
        self,
        doctor_name,
        logged_names
    ):

        doctor_name = str(
            doctor_name
            or
            ""
        ).strip().lower()

        if not doctor_name:

            return False

        for name in logged_names:

            name = str(
                name
                or
                ""
            ).strip().lower()

            if not name:

                continue

            if (
                doctor_name
                ==
                name
            ):

                return True

            # Remove DR prefix.
            d1 = (
                doctor_name
                .replace(
                    "dr.",
                    ""
                )
                .replace(
                    "dr ",
                    ""
                )
                .strip()
            )

            d2 = (
                name
                .replace(
                    "dr.",
                    ""
                )
                .replace(
                    "dr ",
                    ""
                )
                .strip()
            )

            if d1 == d2:

                return True

        return False

    # ======================================================
    # SET PATIENTS
    # ======================================================

    def set_patients(
        self,
        patients
    ):

        values = []

        for row in patients or []:

            if isinstance(
                row,
                (tuple, list)
            ):

                value = (
                    row[0]
                    if len(row) > 0
                    else ""
                )

            else:

                value = row

            value = self._clean_value(
                value
            )

            if not value:

                continue

            if value.lower() in (
                "password",
                "username",
                "no patient"
            ):

                continue

            if value not in values:

                values.append(
                    value
                )

        if not values:

            values = [
                "No Patient"
            ]

        self.patient_combo.configure(
            values=values
        )

        # Do not automatically force a random patient.

    # ======================================================
    # ASSIGNED PATIENTS
    # ======================================================

    def set_assigned_patients(
        self,
        patients
    ):

        self.set_patients(
            patients
        )

    # ======================================================
    # PATIENT SELECTED
    # ======================================================

    def patient_selected(
        self,
        value=None
    ):

        patient = (
            value
            if value is not None
            else self.patient_var.get()
        )

        patient = str(
            patient
            or
            ""
        ).strip()

        if not patient:

            return

        if patient == "No Patient":

            return

        if self.controller:

            try:

                # ------------------------------------------------
                # Existing appointment for this patient:
                # auto select latest own appointment.
                # ------------------------------------------------

                if hasattr(
                    self.controller,
                    "find_appointment_id_for_patient"
                ):

                    appointment_id = (
                        self.controller
                        .find_appointment_id_for_patient(
                            patient
                        )
                    )

                    if appointment_id:

                        appointment = (
                            self.controller
                            .select_appointment(
                                appointment_id
                            )
                        )

                        if appointment:

                            self.appointment_row_selected(
                                appointment
                            )

                            print(
                                f"✅ Existing appointment "
                                f"selected: {appointment_id}"
                            )

                            return

                # ------------------------------------------------
                # Patient details
                # ------------------------------------------------

                details = (
                    self.controller
                    .get_patient_details(
                        patient
                    )
                )

                if details:

                    self.set_patient_details(
                        details
                    )

            except Exception as e:

                print(
                    "Patient Selection Error:",
                    e
                )

    # ======================================================
    # SET PATIENT DETAILS
    # ======================================================

    def set_patient_details(
        self,
        details
    ):

        try:

            father = ""

            disease = ""

            department = ""

            patient_name = ""

            # ==================================================
            # Dictionary
            # ==================================================

            if isinstance(
                details,
                dict
            ):

                patient_name = details.get(
                    "patient_name",
                    ""
                )

                father = details.get(
                    "father_husband_name",
                    ""
                )

                disease = details.get(
                    "disease",
                    ""
                )

                department = details.get(
                    "department",
                    ""
                )

            # ==================================================
            # Tuple / List
            # ==================================================

            elif isinstance(
                details,
                (tuple, list)
            ):

                # Expected:
                # 0 = patient name
                # 1 = father/husband
                # 2 = disease
                # 3 = department

                patient_name = (
                    details[0]
                    if len(details) > 0
                    else ""
                )

                father = (
                    details[1]
                    if len(details) > 1
                    else ""
                )

                disease = (
                    details[2]
                    if len(details) > 2
                    else ""
                )

                department = (
                    details[3]
                    if len(details) > 3
                    else ""
                )

            else:

                return

            # ==================================================
            # Fill patient
            # ==================================================

            if patient_name:

                self.patient_var.set(
                    str(
                        patient_name
                    )
                )

            # ==================================================
            # Father/Husband
            # ==================================================

            self.father_var.set(
                ""
                if father is None
                else str(
                    father
                )
            )

            # ==================================================
            # Disease
            # ==================================================

            self.disease_var.set(
                ""
                if disease is None
                else str(
                    disease
                )
            )

            # ==================================================
            # Department
            # ==================================================

            if department:

                self.department_var.set(
                    str(
                        department
                    )
                )

        except Exception as e:

            print(
                "Set Patient Details Error:",
                e
            )

    # ======================================================
    # DOCTOR SELECTED
    # ======================================================

    def doctor_selected(
        self,
        value=None
    ):

        doctor = (
            value
            if value is not None
            else self.doctor_var.get()
        )

        doctor = str(
            doctor
            or
            ""
        ).strip()

        if not doctor:

            return

        if doctor == "No Doctor":

            return

        self.doctor_var.set(
            doctor
        )

        if self.controller:

            try:

                department = (
                    self.controller
                    .get_doctor_department(
                        doctor
                    )
                )

                if department:

                    self.department_var.set(
                        department
                    )

            except Exception as e:

                print(
                    "Doctor Selection Error:",
                    e
                )

    # ======================================================
    # ADD
    # ======================================================

    def add_clicked(self):

        if not self.controller:

            return

        try:

            self.controller.add_appointment()

        except Exception as e:

            print(
                "Add Button Error:",
                e
            )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_clicked(self):

        if not self.controller:

            return

        try:

            self.controller.update_appointment()

        except Exception as e:

            print(
                "Update Button Error:",
                e
            )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_clicked(self):

        if not self.controller:

            return

        try:

            self.controller.delete_appointment()

        except Exception as e:

            print(
                "Delete Button Error:",
                e
            )

    # ======================================================
    # SEARCH
    # ======================================================

    def search_clicked(self):

        keyword = (
            self.search_var
            .get()
            .strip()
        )

        if not self.controller:

            return

        try:

            self.controller.search_appointment(
                keyword
            )

        except Exception as e:

            print(
                "Search Button Error:",
                e
            )

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh_clicked(self):

        self.search_var.set(
            ""
        )

        if self.controller:

            try:

                self.controller.refresh_appointments()

                return

            except Exception as e:

                print(
                    "Controller Refresh Error:",
                    e
                )

        # Fallback.
        self.load_data()

    # ======================================================
    # LOAD TABLE
    # ======================================================

    def load_data(
        self,
        rows=None
    ):

        try:

            # ------------------------------------------------
            # Clear old table
            # ------------------------------------------------

            for widget in (
                self.table.winfo_children()
            ):

                widget.destroy()

            if rows is None:

                rows = []

            # =================================================
            # HEADERS
            # =================================================

            headers = [
                "Appointment ID",
                "Patient Name",
                "Father / Husband",
                "Disease",
                "Doctor",
                "Department",
                "Date",
                "Time",
                "Token",
                "Status"
            ]

            # =================================================
            # WIDTHS
            # =================================================

            widths = [
                145,
                150,
                175,
                140,
                170,
                175,
                125,
                110,
                80,
                115
            ]

            # =================================================
            # HEADER
            # =================================================

            for col, header in enumerate(
                headers
            ):

                self.table.grid_columnconfigure(
                    col,
                    minsize=widths[col]
                )

                label = ctk.CTkLabel(
                    self.table,
                    text=header,
                    width=widths[col],
                    height=38,
                    font=ctk.CTkFont(
                        size=13,
                        weight="bold"
                    ),
                    anchor="w"
                )

                label.grid(
                    row=0,
                    column=col,
                    padx=8,
                    pady=8,
                    sticky="w"
                )

            # =================================================
            # DATA
            # =================================================

            for row_index, row in enumerate(
                rows,
                start=1
            ):

                values = list(
                    row
                )

                # ---------------------------------------------
                # Current controller row:
                #
                # 0 = database ID
                # 1 = appointment ID
                # 2 = patient
                # 3 = father
                # 4 = disease
                # 5 = doctor
                # 6 = department
                # 7 = date
                # 8 = time
                # 9 = visit type
                # 10 = token
                # 11 = status
                # 12 = remarks
                # ---------------------------------------------

                display = [

                    values[1]
                    if len(values) > 1
                    else "",

                    values[2]
                    if len(values) > 2
                    else "",

                    values[3]
                    if len(values) > 3
                    else "",

                    values[4]
                    if len(values) > 4
                    else "",

                    values[5]
                    if len(values) > 5
                    else "",

                    values[6]
                    if len(values) > 6
                    else "",

                    values[7]
                    if len(values) > 7
                    else "",

                    values[8]
                    if len(values) > 8
                    else "",

                    values[10]
                    if len(values) > 10
                    else "",

                    values[11]
                    if len(values) > 11
                    else ""
                ]

                # ---------------------------------------------
                # DB ID
                # ---------------------------------------------

                appointment_db_id = (
                    values[0]
                    if len(values) > 0
                    else None
                )

                # =================================================
                # CELLS
                # =================================================

                for col, value in enumerate(
                    display
                ):

                    cell_value = (
                        ""
                        if value is None
                        else str(
                            value
                        )
                    )

                    cell = ctk.CTkLabel(
                        self.table,
                        text=cell_value,
                        width=widths[col],
                        height=35,
                        anchor="w"
                    )

                    cell.grid(
                        row=row_index,
                        column=col,
                        padx=8,
                        pady=5,
                        sticky="w"
                    )

                    # ---------------------------------------------
                    # Row click
                    # ---------------------------------------------

                    if appointment_db_id is not None:

                        self._bind_row_click(
                            cell,
                            appointment_db_id
                        )

            # =================================================
            # UPDATE SCROLL
            # =================================================

            self.table.update_idletasks()

            self._update_scroll_region()

        except Exception as e:

            print(
                "Load Table Error:",
                e
            )

    # ======================================================
    # ROW CLICK
    # ======================================================

    def _bind_row_click(
        self,
        widget,
        appointment_db_id
    ):

        try:

            widget.bind(
                "<Button-1>",
                lambda event,
                db_id=appointment_db_id:
                    self.appointment_row_clicked(
                        db_id
                    )
            )

        except Exception as e:

            print(
                "Row Bind Error:",
                e
            )

    # ======================================================
    # SELECT APPOINTMENT
    # ======================================================

    def appointment_row_clicked(
        self,
        appointment_db_id
    ):

        try:

            appointment_db_id = int(
                appointment_db_id
            )

            self.selected_id = (
                appointment_db_id
            )

            self.selected_appointment_id = (
                appointment_db_id
            )

            if not self.controller:

                return

            appointment = (
                self.controller
                .select_appointment(
                    appointment_db_id
                )
            )

            if not appointment:

                return

            self.appointment_row_selected(
                appointment
            )

            print(
                "✅ Appointment Selected:",
                appointment_db_id
            )

        except Exception as e:

            print(
                "Appointment Row Selection Error:",
                e
            )

    # ======================================================
    # LOAD SELECTED APPOINTMENT DATA
    # ======================================================

    def appointment_row_selected(
        self,
        appointment
    ):

        try:

            values = list(
                appointment
            )

            # =================================================
            # Current appointment tuple:
            #
            # 0=id
            # 1=appointment_id
            # 2=patient_name
            # 3=father
            # 4=disease
            # 5=doctor
            # 6=department
            # 7=date
            # 8=time
            # 9=visit_type
            # 10=token
            # 11=status
            # 12=remarks
            # =================================================

            if len(values) > 0:

                self.selected_id = values[0]

                self.selected_appointment_id = (
                    values[0]
                )

            # =================================================
            # Patient
            # =================================================

            if len(values) > 2:

                self.patient_var.set(
                    str(
                        values[2]
                        or
                        ""
                    )
                )

            # =================================================
            # Father / Husband
            # =================================================

            if len(values) > 3:

                self.father_var.set(
                    str(
                        values[3]
                        or
                        ""
                    )
                )

            # =================================================
            # Disease
            # =================================================

            if len(values) > 4:

                self.disease_var.set(
                    str(
                        values[4]
                        or
                        ""
                    )
                )

            # =================================================
            # Doctor
            # =================================================

            if len(values) > 5:

                self.doctor_var.set(
                    str(
                        values[5]
                        or
                        ""
                    )
                )

            # =================================================
            # Department
            # =================================================

            if len(values) > 6:

                self.department_var.set(
                    str(
                        values[6]
                        or
                        ""
                    )
                )

            # =================================================
            # Date
            # =================================================

            if len(values) > 7:

                self.date_var.set(
                    str(
                        values[7]
                        or
                        ""
                    )
                )

            # =================================================
            # Time
            # =================================================

            if len(values) > 8:

                self.time_var.set(
                    str(
                        values[8]
                        or
                        ""
                    )
                )

            # =================================================
            # Visit Type
            # =================================================

            if len(values) > 9:

                self.visit_type_var.set(
                    str(
                        values[9]
                        or
                        "OPD"
                    )
                )

            # =================================================
            # Token
            # =================================================

            if len(values) > 10:

                self.token_var.set(
                    str(
                        values[10]
                        or
                        ""
                    )
                )

            # =================================================
            # Status
            # =================================================

            if len(values) > 11:

                self.status_var.set(
                    str(
                        values[11]
                        or
                        "Pending"
                    )
                )

            # =================================================
            # Remarks
            # =================================================

            if len(values) > 12:

                self.remarks_entry.delete(
                    0,
                    "end"
                )

                self.remarks_entry.insert(
                    0,
                    str(
                        values[12]
                        or
                        ""
                    )
                )

            # =================================================
            # If father/disease are missing,
            # retrieve from patient record.
            # =================================================

            patient = (
                self.patient_var
                .get()
                .strip()
            )

            if (
                patient
                and
                self.controller
            ):

                try:

                    details = (
                        self.controller
                        .get_patient_details(
                            patient
                        )
                    )

                    if details:

                        # Do not overwrite already saved
                        # appointment values if they exist.

                        if not self.father_var.get().strip():

                            if isinstance(
                                details,
                                dict
                            ):

                                self.father_var.set(
                                    str(
                                        details.get(
                                            "father_husband_name",
                                            ""
                                        )
                                        or
                                        ""
                                    )
                                )

                        if not self.disease_var.get().strip():

                            if isinstance(
                                details,
                                dict
                            ):

                                self.disease_var.set(
                                    str(
                                        details.get(
                                            "disease",
                                            ""
                                        )
                                        or
                                        ""
                                    )
                                )

                except Exception as e:

                    print(
                        "Selected Patient Details Error:",
                        e
                    )

        except Exception as e:

            print(
                "Appointment Data Load Error:",
                e
            )

    # ======================================================
    # CLEAR FORM
    # ======================================================

    def clear_form(self):

        self.selected_id = None

        self.selected_appointment_id = None

        # --------------------------------------------------
        # Keep controller selection synchronized
        # --------------------------------------------------

        if self.controller:

            try:

                self.controller.selected_appointment_id = None

            except Exception:

                pass

        # ==================================================
        # Patient
        # ==================================================

        self.patient_var.set(
            ""
        )

        # ==================================================
        # Father
        # ==================================================

        self.father_var.set(
            ""
        )

        # ==================================================
        # Disease
        # ==================================================

        self.disease_var.set(
            ""
        )

        # ==================================================
        # Doctor
        # ==================================================

        self.doctor_var.set(
            ""
        )

        # ==================================================
        # Department
        # ==================================================

        self.department_var.set(
            ""
        )

        # ==================================================
        # Date
        # ==================================================

        self.date_var.set(
            ""
        )

        # ==================================================
        # Time
        # ==================================================

        self.time_var.set(
            ""
        )

        # ==================================================
        # Visit Type
        # ==================================================

        self.visit_type_var.set(
            "OPD"
        )

        # ==================================================
        # Token
        # ==================================================

        self.token_var.set(
            ""
        )

        # ==================================================
        # Status
        # ==================================================

        self.status_var.set(
            "Pending"
        )

        # ==================================================
        # Remarks
        # ==================================================

        self.remarks_entry.delete(
            0,
            "end"
        )

        # ==================================================
        # Search
        # ==================================================

        self.search_var.set(
            ""
        )

    # ======================================================
    # GET FORM DATA
    # ======================================================

    def get_form_data(
        self
    ):

        return {

            "patient_name":
                self.patient_var
                .get()
                .strip(),

            "father_husband_name":
                self.father_var
                .get()
                .strip(),

            "disease":
                self.disease_var
                .get()
                .strip(),

            "doctor_name":
                self.doctor_var
                .get()
                .strip(),

            "department":
                self.department_var
                .get()
                .strip(),

            "appointment_date":
                self.date_var
                .get()
                .strip(),

            "appointment_time":
                self.time_var
                .get()
                .strip(),

            "visit_type":
                self.visit_type_var
                .get()
                .strip(),

            "token_no":
                self.token_var
                .get()
                .strip(),

            "status":
                self.status_var
                .get()
                .strip(),

            "remarks":
                self.remarks_entry
                .get()
                .strip()
        }

    # ======================================================
    # SET FORM DATA
    # ======================================================

    def set_form_data(
        self,
        data
    ):

        if not data:

            return

        self.patient_var.set(
            str(
                data.get(
                    "patient_name",
                    ""
                )
                or
                ""
            )
        )

        self.father_var.set(
            str(
                data.get(
                    "father_husband_name",
                    ""
                )
                or
                ""
            )
        )

        self.disease_var.set(
            str(
                data.get(
                    "disease",
                    ""
                )
                or
                ""
            )
        )

        self.doctor_var.set(
            str(
                data.get(
                    "doctor_name",
                    ""
                )
                or
                ""
            )
        )

        self.department_var.set(
            str(
                data.get(
                    "department",
                    ""
                )
                or
                ""
            )
        )

        self.date_var.set(
            str(
                data.get(
                    "appointment_date",
                    ""
                )
                or
                ""
            )
        )

        self.time_var.set(
            str(
                data.get(
                    "appointment_time",
                    ""
                )
                or
                ""
            )
        )

        self.visit_type_var.set(
            str(
                data.get(
                    "visit_type",
                    "OPD"
                )
                or
                "OPD"
            )
        )

        self.token_var.set(
            str(
                data.get(
                    "token_no",
                    ""
                )
                or
                ""
            )
        )

        self.status_var.set(
            str(
                data.get(
                    "status",
                    "Pending"
                )
                or
                "Pending"
            )
        )

        self.remarks_entry.delete(
            0,
            "end"
        )

        self.remarks_entry.insert(
            0,
            str(
                data.get(
                    "remarks",
                    ""
                )
                or
                ""
            )
        )

    # ======================================================
    # GET SELECTED PATIENT
    # ======================================================

    def get_selected_patient(
        self
    ):

        return (
            self.patient_var
            .get()
            .strip()
        )

    # ======================================================
    # GET SELECTED DOCTOR
    # ======================================================

    def get_selected_doctor(
        self
    ):

        return (
            self.doctor_var
            .get()
            .strip()
        )

    # ======================================================
    # SHOW MESSAGE
    # ======================================================

    def show_message(
        self,
        message
    ):

        dialog = ctk.CTkToplevel(
            self.parent
        )

        dialog.title(
            "Hospital ERP"
        )

        dialog.geometry(
            "420x190"
        )

        dialog.transient(
            self.parent
        )

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=str(
                message
            ),
            font=ctk.CTkFont(
                size=15
            ),
            wraplength=370
        ).pack(
            padx=20,
            pady=35
        )

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack()

    # ======================================================
    # GET FRAME
    # ======================================================

    def get_frame(
        self
    ):

        return self.main_frame