import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap
from db_connector import connect_to_database

class StudentInformationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information Form")
        self.setGeometry(100, 100, 700, 400)
        self.setFixedSize(700, 600)
        # Apply a global stylesheet to enlarge font for all child widgets
        self.setStyleSheet("QWidget { font-size: 12pt; font-family: Arial; }")
        
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()


        # Create a label for the logo
        logo_label = QLabel()
        pixmap = QPixmap("mmd-logo.png")  # Replace with your logo file path
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)   # Allows the logo to scale if needed
        logo_label.setFixedSize(100, 100)      # Set the desired size for the logo
        header_layout.addWidget(logo_label, alignment=Qt.AlignRight)

        # Title layout (vertical) for college name and departments
        title_layout = QVBoxLayout()
        title_label = QLabel("Holy Cross College")
        title_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: #0033cc;")
        title_label.setAlignment(Qt.AlignCenter)
        dept_label = QLabel("Information Communication Department\nMultimedia Department")
        dept_label.setStyleSheet("font-size: 12pt; color: #0033cc;")
        dept_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        title_layout.addWidget(dept_label)
        header_layout.addLayout(title_layout)
        header_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(header_layout)


        
        # Title for Student Information section
        student_title = QLabel("Student Information")
        student_title.setAlignment(Qt.AlignCenter)
        student_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-bottom: 10px;")
        main_layout.addWidget(student_title)
        
        # Create a horizontal layout for the name fields
        name_layout = QHBoxLayout()

        # Surname field with label below
        surname_layout = QVBoxLayout()
        self.surname_edit = QLineEdit()
        self.surname_edit.setAlignment(Qt.AlignCenter)
        surname_layout.addWidget(self.surname_edit)
        surname_label = QLabel("Surname")
        surname_label.setAlignment(Qt.AlignCenter)
        surname_layout.addWidget(surname_label)
        name_layout.addLayout(surname_layout)
        
        # First Name field with label below
        first_name_layout = QVBoxLayout()
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setAlignment(Qt.AlignCenter)
        first_name_layout.addWidget(self.first_name_edit)
        first_name_label = QLabel("First Name")
        first_name_label.setAlignment(Qt.AlignCenter)
        first_name_layout.addWidget(first_name_label)
        name_layout.addLayout(first_name_layout)
        
        # Middle Initial field with label below
        mi_layout = QVBoxLayout()
        self.mi_edit = QLineEdit()
        self.mi_edit.setAlignment(Qt.AlignCenter)
        mi_layout.addWidget(self.mi_edit)
        mi_label = QLabel("MI.")
        mi_label.setAlignment(Qt.AlignCenter)
        mi_layout.addWidget(mi_label)
        name_layout.addLayout(mi_layout)
        
        # Extension field with label below
        ext_layout = QVBoxLayout()
        self.extension_edit = QLineEdit()
        self.extension_edit.setFixedWidth(50)
        self.extension_edit.setAlignment(Qt.AlignCenter)
        ext_layout.addWidget(self.extension_edit)
        ext_label = QLabel("Ext.")
        ext_label.setAlignment(Qt.AlignCenter)
        ext_layout.addWidget(ext_label)
        name_layout.addLayout(ext_layout)
        
        # Connect signals to update name fields automatically
        self.surname_edit.textChanged.connect(self.onSurnameTextChanged)
        self.first_name_edit.textChanged.connect(self.onFirstNameTextChanged)
        self.mi_edit.textChanged.connect(self.onMITextChanged)
        
        # Create a form row for the name fields with the label "Name:"
        name_form = QFormLayout()
        name_form.addRow("Name:", name_layout)
        main_layout.addLayout(name_form)
        
        # Other fields using QFormLayout for neat alignment
        form_layout = QFormLayout()
        
        # Composite Address: Barangay, Town/Municipality, Province
        address_layout = QHBoxLayout()

        # Barangay
        barangay_layout = QVBoxLayout()
        self.barangay_edit = QLineEdit()
        self.barangay_edit.setAlignment(Qt.AlignCenter)
        barangay_layout.addWidget(self.barangay_edit)
        barangay_label = QLabel("Barangay")
        barangay_label.setAlignment(Qt.AlignCenter)
        barangay_layout.addWidget(barangay_label)
        address_layout.addLayout(barangay_layout)

        # Town/Municipality
        town_layout = QVBoxLayout()
        self.town_edit = QLineEdit()
        self.town_edit.setAlignment(Qt.AlignCenter)
        town_layout.addWidget(self.town_edit)
        town_label = QLabel("Town/Municipality")
        town_label.setAlignment(Qt.AlignCenter)
        town_layout.addWidget(town_label)
        address_layout.addLayout(town_layout)
        # Province
        province_layout = QVBoxLayout()
        self.province_edit = QLineEdit()
        self.province_edit.setAlignment(Qt.AlignCenter)
        province_layout.addWidget(self.province_edit)
        province_label = QLabel("Province")
        province_label.setAlignment(Qt.AlignCenter)
        province_layout.addWidget(province_label)
        address_layout.addLayout(province_layout)
        
        form_layout.addRow("Address:", address_layout)
        
        self.student_id_edit = QLineEdit()
        form_layout.addRow("Student ID:", self.student_id_edit)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year"])
        form_layout.addRow("Year:", self.year_combo)
        
        self.course_combo = QComboBox()
        self.course_combo.addItems([
            "Bachelor of Science in Accountancy", 
            "Bachelor of Science in Accounting Information System",
            "Bachelor of Science in Civil Engineering", 
            "Bachelor of Science in Computer Engineering",
            "Bachelor of Science in Criminology",
            "Bachelor of Science in Hospitality Management",
            "Bachelor of Science in Tourism Management",
            "Bachelor of Science in Information Technology",
            "Bachelor of Science in Computer Science",
            "Bachelor of Science in Psychology",
            "Bachelor of Science in Business Administration - Financial Management",
            "Bachelor of Science in Business Administration - Marketing Management",
            "Bachelor of Science in Business Administration - Human Resources Management",
            "Bachelor of Science in Business Administration - Operations Management",
            "Bachelor of Elementary Education",
            "Bachelor of Secondary Education - English",
            "Bachelor of Secondary Education - Mathematics",
            "Bachelor of Secondary Education - Science",
            "Bachelor of Secondary Education - Filipino",
            "Associate in Computer Technology"
        ])
        form_layout.addRow("Course:", self.course_combo)
        
        main_layout.addLayout(form_layout)
   
        # Title for Emergency Contact section
        emergency_title = QLabel("Emergency Contact")
        emergency_title.setAlignment(Qt.AlignCenter)
        emergency_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-top: 15px; margin-bottom: 10px;")
        main_layout.addWidget(emergency_title)
        
        emergency_form_layout = QFormLayout()
        self.emergency_name_edit = QLineEdit()
        emergency_form_layout.addRow("Name:", self.emergency_name_edit)
        
        self.emergency_relation_combo = QComboBox()
        self.emergency_relation_combo.addItems(["Father", "Mother", "Guardian"])
        emergency_form_layout.addRow("Relation to Student:", self.emergency_relation_combo)
        
        self.emergency_contact_edit = QLineEdit()
        # Validator for digits and maximum 11 characters already set
        validator = QRegExpValidator(QRegExp(r"\d{0,11}"), self.emergency_contact_edit)
        self.emergency_contact_edit.setValidator(validator)
        self.emergency_contact_edit.setMaxLength(11)
        emergency_form_layout.addRow("Contact Number:", self.emergency_contact_edit)

        
        main_layout.addLayout(emergency_form_layout)
        
        # Submit button
        submit_button = QPushButton("Submit Registration")
        submit_button.setStyleSheet("padding: 8px;")
        submit_button.clicked.connect(self.submit_registration)
        main_layout.addWidget(submit_button)
        
        self.setLayout(main_layout)
    
    def onSurnameTextChanged(self, text):
        # Convert text to uppercase
        new_text = text.upper()
        if new_text != text:
            self.surname_edit.blockSignals(True)
            self.surname_edit.setText(new_text)
            self.surname_edit.blockSignals(False)
    
    def onFirstNameTextChanged(self, text):
        # Split using " " so we can detect trailing empty word if a space is added
        words = text.split(" ")
        # If the last word is empty, it means the user just typed a space.
        if words and words[-1] == "":
            # Capitalize all but the last word, then rejoin and add a trailing space.
            new_text = " ".join(word.capitalize() for word in words[:-1]) + " "
        else:
            new_text = " ".join(word.capitalize() for word in words)
        if new_text != text:
            self.first_name_edit.blockSignals(True)
            self.first_name_edit.setText(new_text)
            self.first_name_edit.blockSignals(False)

    def onMITextChanged(self, text):
        # Force the middle initial to be uppercase and ensure it ends with a period.
        # Limit to a single letter with a period (e.g., "A.")
        if not text:
            return
        new_text = text.upper()
        # If the text doesn't already end with a period, add one.
        if not new_text.endswith("."):
            new_text += "."
        # Limit to two characters (letter + period)
        new_text = new_text[:2]
        if new_text != text:
            self.mi_edit.blockSignals(True)
            self.mi_edit.setText(new_text)
            self.mi_edit.blockSignals(False)
    
    def submit_registration(self):
        # Gather form data from name fields
        surname = self.surname_edit.text().strip()
        first_name = self.first_name_edit.text().strip()
        mi = self.mi_edit.text().strip()
        extension = self.extension_edit.text().strip()  # Not required
        
        # Gather composite address parts and concatenate them
        barangay = self.barangay_edit.text().strip()
        town = self.town_edit.text().strip()
        province = self.province_edit.text().strip()
        address = f"{barangay}, {town}, {province}"
        
        student_id = self.student_id_edit.text().strip()
        year = self.year_combo.currentText()
        course = self.course_combo.currentText()
        
        emergency_name = self.emergency_name_edit.text().strip()
        emergency_relation = self.emergency_relation_combo.currentText()
        emergency_contact = self.emergency_contact_edit.text().strip()
        
        # Create a dictionary of required fields (all except extension)
        required_fields = {
            "Surname": surname,
            "First Name": first_name,
            "Middle Initial": mi,
            "Barangay": barangay,
            "Town/Municipality": town,
            "Province": province,
            "Student ID": student_id,
            "Emergency Contact Name": emergency_name,
            "Emergency Relation": emergency_relation,
            "Emergency Contact Number": emergency_contact,
        }
        
        missing = [field for field, value in required_fields.items() if not value]
        if missing:
            QMessageBox.warning(self, "Input Error", 
                "Please complete all required fields: " + ", ".join(missing))
            return
        
        # Check that the emergency contact number is exactly 11 digits
        if len(emergency_contact) != 11:
            QMessageBox.warning(self, "Input Error", 
                "Emergency Contact Number must be exactly 11 digits.")
            return
        
        # Connect to the database
        conn = connect_to_database(user_role="student")
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        # Check if student ID already exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Duplicate Entry", "This Student ID already exists.")
            conn.close()
            return
        
        # Insert new registration record; note the new column for extension
        query = """
            INSERT INTO students (student_id, surname, first_name, mi, extension, 
                                    address, year, course, emergency_name, relation_to_student, emergency_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (student_id, surname, first_name, mi, extension, address, year, course,
                  emergency_name, emergency_relation, emergency_contact)
        try:
            cursor.execute(query, values)
            conn.commit()
            QMessageBox.information(self, "Success", "Registration successful!")
            self.clear_form()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Registration failed: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def clear_form(self):
        self.surname_edit.clear()
        self.first_name_edit.clear()
        self.mi_edit.clear()
        self.extension_edit.clear()
        self.barangay_edit.clear()
        self.town_edit.clear()
        self.province_edit.clear()
        self.student_id_edit.clear()
        self.year_combo.setCurrentIndex(0)
        self.course_combo.setCurrentIndex(0)
        self.emergency_name_edit.clear()
        self.emergency_relation_combo.setCurrentIndex(0)
        self.emergency_contact_edit.clear()

class EmployeeInformationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Information Form")
        self.setGeometry(100, 100, 700, 400)
        self.setFixedSize(700, 600)
        # Apply a global stylesheet to enlarge font for all child widgets
        self.setStyleSheet("QWidget { font-size: 12pt; font-family: Arial; }")
        
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()


        # Create a label for the logo
        logo_label = QLabel()
        pixmap = QPixmap("mmd-logo.png")  # Replace with your logo file path
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)   # Allows the logo to scale if needed
        logo_label.setFixedSize(100, 100)      # Set the desired size for the logo
        header_layout.addWidget(logo_label, alignment=Qt.AlignRight)

        # Title layout (vertical) for college name and departments
        title_layout = QVBoxLayout()
        title_label = QLabel("Holy Cross College")
        title_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: #0033cc;")
        title_label.setAlignment(Qt.AlignCenter)
        dept_label = QLabel("Information Communication Department\nMultimedia Department")
        dept_label.setStyleSheet("font-size: 12pt; color: #0033cc;")
        dept_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        title_layout.addWidget(dept_label)
        header_layout.addLayout(title_layout)
        header_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(header_layout)
        
        # Title for Student Information section
        student_title = QLabel("Employee Information")
        student_title.setAlignment(Qt.AlignCenter)
        student_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-bottom: 10px;")
        main_layout.addWidget(student_title)
        
        # Create a horizontal layout for the name fields
        name_layout = QHBoxLayout()

        # Surname field with label below
        surname_layout = QVBoxLayout()
        self.surname_edit = QLineEdit()
        self.surname_edit.setAlignment(Qt.AlignCenter)
        surname_layout.addWidget(self.surname_edit)
        surname_label = QLabel("Surname")
        surname_label.setAlignment(Qt.AlignCenter)
        surname_layout.addWidget(surname_label)
        name_layout.addLayout(surname_layout)
        
        # First Name field with label below
        first_name_layout = QVBoxLayout()
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setAlignment(Qt.AlignCenter)
        first_name_layout.addWidget(self.first_name_edit)
        first_name_label = QLabel("First Name")
        first_name_label.setAlignment(Qt.AlignCenter)
        first_name_layout.addWidget(first_name_label)
        name_layout.addLayout(first_name_layout)
        
        # Middle Initial field with label below
        mi_layout = QVBoxLayout()
        self.mi_edit = QLineEdit()
        self.mi_edit.setAlignment(Qt.AlignCenter)
        mi_layout.addWidget(self.mi_edit)
        mi_label = QLabel("MI.")
        mi_label.setAlignment(Qt.AlignCenter)
        mi_layout.addWidget(mi_label)
        name_layout.addLayout(mi_layout)
        
        # Extension field with label below
        ext_layout = QVBoxLayout()
        self.extension_edit = QLineEdit()
        self.extension_edit.setFixedWidth(50)
        self.extension_edit.setAlignment(Qt.AlignCenter)
        ext_layout.addWidget(self.extension_edit)
        ext_label = QLabel("Ext.")
        ext_label.setAlignment(Qt.AlignCenter)
        ext_layout.addWidget(ext_label)
        name_layout.addLayout(ext_layout)
        
        # Connect signals to update name fields automatically
        self.surname_edit.textChanged.connect(self.onSurnameTextChanged)
        self.first_name_edit.textChanged.connect(self.onFirstNameTextChanged)
        self.mi_edit.textChanged.connect(self.onMITextChanged)
        
        # Create a form row for the name fields with the label "Name:"
        name_form = QFormLayout()
        name_form.addRow("Name:", name_layout)
        main_layout.addLayout(name_form)
        
        # Other fields using QFormLayout for neat alignment
        form_layout = QFormLayout()
        
        # Composite Address: Barangay, Town/Municipality, Province
        address_layout = QHBoxLayout()

        # Barangay
        barangay_layout = QVBoxLayout()
        self.barangay_edit = QLineEdit()
        self.barangay_edit.setAlignment(Qt.AlignCenter)
        barangay_layout.addWidget(self.barangay_edit)
        barangay_label = QLabel("Barangay")
        barangay_label.setAlignment(Qt.AlignCenter)
        barangay_layout.addWidget(barangay_label)
        address_layout.addLayout(barangay_layout)

        # Town/Municipality
        town_layout = QVBoxLayout()
        self.town_edit = QLineEdit()
        self.town_edit.setAlignment(Qt.AlignCenter)
        town_layout.addWidget(self.town_edit)
        town_label = QLabel("Town/Municipality")
        town_label.setAlignment(Qt.AlignCenter)
        town_layout.addWidget(town_label)
        address_layout.addLayout(town_layout)
        # Province
        province_layout = QVBoxLayout()
        self.province_edit = QLineEdit()
        self.province_edit.setAlignment(Qt.AlignCenter)
        province_layout.addWidget(self.province_edit)
        province_label = QLabel("Province")
        province_label.setAlignment(Qt.AlignCenter)
        province_layout.addWidget(province_label)
        address_layout.addLayout(province_layout)
        
        form_layout.addRow("Address:", address_layout)
        
        self.employee_id_edit = QLineEdit()
        form_layout.addRow("Employee ID:", self.employee_id_edit)

        self.department_edit = QLineEdit()
        form_layout.addRow("Department:", self.department_edit)

        self.position_edit = QLineEdit()
        form_layout.addRow("Position:", self.position_edit)
        
        main_layout.addLayout(form_layout)
   
        # Title for Emergency Contact section
        emergency_title = QLabel("Emergency Contact")
        emergency_title.setAlignment(Qt.AlignCenter)
        emergency_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-top: 15px; margin-bottom: 10px;")
        main_layout.addWidget(emergency_title)
        
        emergency_form_layout = QFormLayout()
        self.emergency_name_edit = QLineEdit()
        emergency_form_layout.addRow("Name:", self.emergency_name_edit)
        
        self.emergency_name_edit = QLineEdit()
        emergency_form_layout.addRow("Relation to Employee:", self.emergency_name_edit)
        
        self.emergency_contact_edit = QLineEdit()
        # Validator for digits and maximum 11 characters already set
        validator = QRegExpValidator(QRegExp(r"\d{0,11}"), self.emergency_contact_edit)
        self.emergency_contact_edit.setValidator(validator)
        self.emergency_contact_edit.setMaxLength(11)
        emergency_form_layout.addRow("Contact Number:", self.emergency_contact_edit)

        main_layout.addLayout(emergency_form_layout)
        
        # Submit button
        submit_button = QPushButton("Submit Registration")
        submit_button.setStyleSheet("padding: 8px;")
        submit_button.clicked.connect(self.emp_submit)
        main_layout.addWidget(submit_button)
        
        self.setLayout(main_layout)
    
    def onSurnameTextChanged(self, text):
        # Convert text to uppercase
        new_text = text.upper()
        if new_text != text:
            self.surname_edit.blockSignals(True)
            self.surname_edit.setText(new_text)
            self.surname_edit.blockSignals(False)
    
    def onFirstNameTextChanged(self, text):
        # Split using " " so we can detect trailing empty word if a space is added
        words = text.split(" ")
        # If the last word is empty, it means the user just typed a space.
        if words and words[-1] == "":
            # Capitalize all but the last word, then rejoin and add a trailing space.
            new_text = " ".join(word.capitalize() for word in words[:-1]) + " "
        else:
            new_text = " ".join(word.capitalize() for word in words)
        if new_text != text:
            self.first_name_edit.blockSignals(True)
            self.first_name_edit.setText(new_text)
            self.first_name_edit.blockSignals(False)

    def onMITextChanged(self, text):
        # Force the middle initial to be uppercase and ensure it ends with a period.
        # Limit to a single letter with a period (e.g., "A.")
        if not text:
            return
        new_text = text.upper()
        # If the text doesn't already end with a period, add one.
        if not new_text.endswith("."):
            new_text += "."
        # Limit to two characters (letter + period)
        new_text = new_text[:2]
        if new_text != text:
            self.mi_edit.blockSignals(True)
            self.mi_edit.setText(new_text)
            self.mi_edit.blockSignals(False)
    
    def emp_submit(self):
        # Gather form data from name fields
        surname = self.surname_edit.text().strip()
        first_name = self.first_name_edit.text().strip()
        mi = self.mi_edit.text().strip()
        extension = self.extension_edit.text().strip()  # Not required
        
        # Gather composite address parts and concatenate them
        barangay = self.barangay_edit.text().strip()
        town = self.town_edit.text().strip()
        province = self.province_edit.text().strip()
        address = f"{barangay}, {town}, {province}"
        
        emp_id = self.employee_id_edit.text().strip()
        
        department = self.department_edit.text().strip()

        position = self.position_edit.text().strip()
        
        emergency_name = self.emergency_name_edit.text().strip()
        emergency_relation = self.emergency_name_edit.text().strip()
        emergency_contact = self.emergency_contact_edit.text().strip()
        
        # Create a dictionary of required fields (all except extension)
        required_fields = {
            "Surname": surname,
            "First Name": first_name,
            "Middle Initial": mi,
            "Barangay": barangay,
            "Town/Municipality": town,
            "Province": province,
            "Employee ID": emp_id,
            "Department": department,
            "Position": position,
            "Emergency Contact Name": emergency_name,
            "Emergency Relation": emergency_relation,
            "Emergency Contact Number": emergency_contact,
        }
        
        missing = [field for field, value in required_fields.items() if not value]
        if missing:
            QMessageBox.warning(self, "Input Error", 
                "Please complete all required fields: " + ", ".join(missing))
            return
        
        # Check that the emergency contact number is exactly 11 digits
        if len(emergency_contact) != 11:
            QMessageBox.warning(self, "Input Error", 
                "Emergency Contact Number must be exactly 11 digits.")
            return
        
        # Connect to the database
        conn = connect_to_database(user_role="employee")
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        # Check if student ID already exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (emp_id,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Duplicate Entry", "This Student ID already exists.")
            conn.close()
            return
        
        # Insert new registration record; note the new column for extension
        query = """
            INSERT INTO students (emp_id, surname, first_name, mi, extension, 
                                    address, department, position, emergency_name, emergency_relation, emergency_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (emp_id, surname, first_name, mi, extension, address, department, position,
                  emergency_name, emergency_relation, emergency_contact)
        try:
            cursor.execute(query, values)
            conn.commit()
            QMessageBox.information(self, "Success", "Registration successful!")
            self.clear_form()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Registration failed: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def clear_form(self):
        self.surname_edit.clear()
        self.first_name_edit.clear()
        self.mi_edit.clear()
        self.extension_edit.clear()
        self.barangay_edit.clear()
        self.town_edit.clear()
        self.province_edit.clear()
        self.employee_id_edit.clear()
        self.emergency_name_edit.clear()
        self.department_edit.clear()
        self.position_edit.clear()
        self.emergency_contact_edit.clear()

