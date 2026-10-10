from database.database import Database


class HRCRUD(Database):

    def __init__(self):

        super().__init__()

        # Database connection
        self.connect()

        # Create employee table
        self.create_employee_table()

    # ==========================================
    # Create Employee Table
    # ==========================================

    def create_employee_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                employee_id TEXT UNIQUE,

                full_name TEXT,

                father_name TEXT,

                gender TEXT,

                dob TEXT,

                blood_group TEXT,

                marital_status TEXT,

                mobile TEXT,

                email TEXT,

                address TEXT,

                city TEXT,

                state TEXT,

                pincode TEXT,

                department TEXT,

                designation TEXT,

                joining_date TEXT,

                employment_type TEXT,

                basic_salary REAL,

                shift TEXT,

                status TEXT,

                aadhaar_no TEXT,

                pan_no TEXT,

                qualification TEXT,

                experience TEXT,

                photo TEXT,

                remarks TEXT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP

            )
        """)

        self.commit()

        print("✅ Employee Table Created")

    # ==========================================
    # Generate Employee ID
    # ==========================================

    def generate_employee_id(self):

        self.cursor.execute("""
            SELECT employee_id
            FROM employees
            WHERE employee_id LIKE 'EMP%'
            ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        max_number = 0

        for row in rows:

            employee_id = row[0]

            try:

                number = int(
                    employee_id.replace("EMP", "")
                )

                if number > max_number:
                    max_number = number

            except (ValueError, AttributeError):

                continue

        next_number = max_number + 1

        return f"EMP{next_number:06d}"

    # ==========================================
    # Add Employee
    # ==========================================

    def add_employee(
        self,
        employee_id,
        full_name,
        father_name,
        gender,
        dob,
        blood_group,
        marital_status,
        mobile,
        email,
        address,
        city,
        state,
        pincode,
        department,
        designation,
        joining_date,
        employment_type,
        basic_salary,
        shift,
        status,
        aadhaar_no,
        pan_no,
        qualification,
        experience,
        photo,
        remarks
    ):

        try:
            self.cursor.execute("""
            INSERT INTO employees
            (
                employee_id,
                full_name,
                father_name,
                gender,
                dob,
                blood_group,
                marital_status,
                mobile,
                email,
                address,
                city,
                state,
                pincode,
                department,
                designation,
                joining_date,
                employment_type,
                basic_salary,
                shift,
                status,
                aadhaar_no,
                pan_no,
                qualification,
                experience,
                photo,
                remarks
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
        """, (
                employee_id,
                full_name,
                father_name,
                gender,
                dob,
                blood_group,
                marital_status,
                mobile,
                email,
                address,
                city,
                state,
                pincode,
                department,
                designation,
                joining_date,
                employment_type,
                basic_salary,
                shift,
                status,
                aadhaar_no,
                pan_no,
                qualification,
                experience,
                photo,
                remarks
            ))

            self.commit()

            print("INSERT SUCCESS - EMPLOYEE SAVED")

            return True

        except Exception as e:

            import traceback
            traceback.print_exc()

            print("Add Employee Error:", e)

            return False

    # ==========================================
    # Load Employees
    # ==========================================

    def load_employees(self):

        self.cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                department,
                designation,
                mobile,
                joining_date,
                basic_salary,
                status
            FROM employees
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================================
    # Search Employee
    # ==========================================

    def search_employee(self, keyword):

        self.cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                department,
                designation,
                mobile,
                joining_date,
                basic_salary,
                status
            FROM employees
            WHERE
                employee_id LIKE :keyword
                OR full_name LIKE :keyword
                OR father_name LIKE :keyword
                OR mobile LIKE :keyword
                OR email LIKE :keyword
                OR department LIKE :keyword
                OR designation LIKE :keyword
                OR joining_date LIKE :keyword
                OR employment_type LIKE :keyword
                OR status LIKE :keyword
                OR aadhaar_no LIKE :keyword
                OR pan_no LIKE :keyword
                OR address LIKE :keyword
                OR city LIKE :keyword
                OR state LIKE :keyword
                OR pincode LIKE :keyword
            ORDER BY id DESC
        """, {"keyword": f"%{keyword}%"})

        return self.cursor.fetchall()


    # ==========================================
    # Get Employee By ID
    # ==========================================

    def get_employee_by_id(self, employee_db_id):

        self.cursor.execute("""
            SELECT *
            FROM employees
            WHERE id=?
        """, (employee_db_id,))

        return self.cursor.fetchone()

    # ==========================================
    # Update Employee
    # ==========================================

    def update_employee(
        self,
        employee_db_id,
        full_name,
        father_name,
        gender,
        dob,
        blood_group,
        marital_status,
        mobile,
        email,
        address,
        city,
        state,
        pincode,
        department,
        designation,
        joining_date,
        employment_type,
        basic_salary,
        shift,
        status,
        aadhaar_no,
        pan_no,
        qualification,
        experience,
        photo,
        remarks
    ):

        try:

            self.cursor.execute("""
                UPDATE employees
                SET
                    full_name=?,
                    father_name=?,
                    gender=?,
                    dob=?,
                    blood_group=?,
                    marital_status=?,
                    mobile=?,
                    email=?,
                    address=?,
                    city=?,
                    state=?,
                    pincode=?,
                    department=?,
                    designation=?,
                    joining_date=?,
                    employment_type=?,
                    basic_salary=?,
                    shift=?,
                    status=?,
                    aadhaar_no=?,
                    pan_no=?,
                    qualification=?,
                    experience=?,
                    photo=?,
                    remarks=?
                WHERE id=?
            """, (
                full_name,
                father_name,
                gender,
                dob,
                blood_group,
                marital_status,
                mobile,
            email,
            address,
            city,
            state,
            pincode,
            department,
            designation,
            joining_date,
            employment_type,
            basic_salary,
            shift,
            status,
            aadhaar_no,
            pan_no,
            qualification,
            experience,
            photo,
            remarks,
            employee_db_id
        ))

            self.commit()

            print("UPDATE SUCCESS - EMPLOYEE UPDATED")

            return True

        except Exception as e:

            import traceback
            traceback.print_exc()

            print("Update Employee Error:", e)

            return False

    # ==========================================
    # Delete Employee
    # ==========================================

    def delete_employee(self, employee_db_id):

        try:

            self.cursor.execute(
                "DELETE FROM employees WHERE id=?",
                (employee_db_id,)
            )

            self.commit()

            print("✅ Employee Deleted")

            return True

        except Exception as e:

            print("Delete Employee Error:", e)

            return False
