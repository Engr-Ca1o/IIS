import os, sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QToolButton
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap, QFont, QIcon
from db_connector import connect_to_database

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# --- Helper function to create a header container with no margins ---
def create_header_container(logo_left_path, title_text, subtitle_text, dept_text, logo_right_path):
    header_container = QWidget()
    header_container.setObjectName("headerContainer")
    header_container.setStyleSheet("""
        #headerContainer {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0814ce, stop:1 #f0f8ff);
        }
    """)
    header_layout = QHBoxLayout(header_container)
    header_layout.setContentsMargins(0, 20, 0, 0)
    header_layout.setSpacing(0)
    
    # Left logo
    logo_left = QLabel()
    pixmap_left = QPixmap(logo_left_path)
    logo_left.setPixmap(pixmap_left)
    logo_left.setStyleSheet("background: transparent;")
    logo_left.setScaledContents(True)
    logo_left.setFixedSize(100, 100)
    header_layout.addWidget(logo_left, alignment=Qt.AlignCenter)
    
    # Center text block in its own widget with transparent background
    center_widget = QWidget()
    center_widget.setStyleSheet("background: transparent;")
    center_layout = QVBoxLayout(center_widget)
    center_layout.setContentsMargins(0, 0, 0, 0)
    center_layout.setSpacing(0)
    
    title_label = QLabel(title_text)
    title_label.setFont(QFont("Old English Text MT", 50, QFont.Bold))
    # You can force the font size via stylesheet if needed:
    title_label.setStyleSheet("color: #ffffff; background: transparent; font-size: 50pt; font-weight: bold;")
    title_label.setAlignment(Qt.AlignCenter)
    
    subtitle_label = QLabel(subtitle_text)
    subtitle_label.setFont(QFont("Arial", 12))
    subtitle_label.setStyleSheet("color: #000000; background: transparent; font-weight: bold;")
    subtitle_label.setAlignment(Qt.AlignCenter)
    
    dept_label = QLabel(dept_text)
    dept_label.setFont(QFont("Arial", 12))
    dept_label.setStyleSheet("color: #000000; background: transparent; font-weight: bold;")
    dept_label.setAlignment(Qt.AlignCenter)
    
    center_layout.addWidget(title_label)
    center_layout.addWidget(subtitle_label)
    center_layout.addWidget(dept_label)
    
    header_layout.addWidget(center_widget, alignment=Qt.AlignCenter)
    
    # Right logo
    logo_right = QLabel()
    pixmap_right = QPixmap(logo_right_path)
    logo_right.setPixmap(pixmap_right)
    logo_right.setStyleSheet("background: transparent;")
    logo_right.setScaledContents(True)
    logo_right.setFixedSize(100, 100)
    header_layout.addWidget(logo_right, alignment=Qt.AlignCenter)
    
    return header_container

# --- Base class for shared styling, common emergency section, and navigation ---
class BaseInformationForm(QWidget):
    def __init__(self, window_title, window_icon_path):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon(window_icon_path))
        # The overall background for the form remains light blue
        self.setStyleSheet("QWidget { background-color: #f0f8ff; font-size: 12pt; }")
        self.font = QFont("Arial", 11)
        self.enye_uppercase = True  # Initialize the toggle state for Ñ/ñ
    
    def go_back(self):
        from first_page import Page  # Import here to avoid circular dependency
        self.landing = Page()
        self.landing.show()
        self.close()
        
    def create_emergency_section(self, person_type="Student"):
        emergency_title = QLabel("Emergency Contact")
        emergency_title.setAlignment(Qt.AlignCenter)
        emergency_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-top: 15px; margin-bottom: 10px;")
        
        emergency_form_layout = QFormLayout()
        self.emergency_name_edit = QLineEdit()
        emergency_form_layout.addRow("Name:", self.emergency_name_edit)
        
        self.emergency_relation_edit = QLineEdit()
        emergency_form_layout.addRow("Relation to {}:".format(person_type), self.emergency_relation_edit)
        
        self.emergency_contact_edit = QLineEdit()
        validator = QRegExpValidator(QRegExp(r"\d{0,11}"), self.emergency_contact_edit)
        self.emergency_contact_edit.setValidator(validator)
        self.emergency_contact_edit.setMaxLength(11)
        emergency_form_layout.addRow("Contact Number:", self.emergency_contact_edit)
        
        return emergency_title, emergency_form_layout

    def add_enye_button(self, layout):
        """Adds an Ñ button to the top of the form."""
        enye_button = QToolButton()
        enye_button.setText("Ñ")
        enye_button.setStyleSheet("font-size: 14pt; padding: 5px;")
        enye_button.clicked.connect(self.insert_enye_character)
        layout.addWidget(enye_button, alignment=Qt.AlignLeft)

    def insert_enye_character(self):
        """Inserts the Ñ or ñ character into the currently focused field."""
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            cursor_position = focused_widget.cursorPosition()
            current_text = focused_widget.text()
            # Toggle between uppercase Ñ and lowercase ñ
            if self.enye_uppercase:
                new_text = current_text[:cursor_position] + "Ñ" + current_text[cursor_position:]
            else:
                new_text = current_text[:cursor_position] + "ñ" + current_text[cursor_position:]
            focused_widget.setText(new_text)
            focused_widget.setCursorPosition(cursor_position + 1)
            # Toggle the state for the next click
            self.enye_uppercase = not self.enye_uppercase

    def insert_uppercase_enye(self):
        """Inserts the uppercase Ñ character into the currently focused field."""
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            cursor_position = focused_widget.cursorPosition()
            current_text = focused_widget.text()
            new_text = current_text[:cursor_position] + "Ñ" + current_text[cursor_position:]
            focused_widget.setText(new_text)
            focused_widget.setCursorPosition(cursor_position + 1)

    def insert_lowercase_enye(self):
        """Inserts the lowercase ñ character into the currently focused field."""
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            cursor_position = focused_widget.cursorPosition()
            current_text = focused_widget.text()
            new_text = current_text[:cursor_position] + "ñ" + current_text[cursor_position:]
            focused_widget.setText(new_text)
            focused_widget.setCursorPosition(cursor_position + 1)

# --- Student Information Form ---
class StudentInformationForm(BaseInformationForm):
    def __init__(self):
        super().__init__("Student Registration", resource_path("mmd-logo.png"))
        self.setGeometry(275, 70, 800, 600)
        self.showMaximized()
        
        # Main layout for the window with no margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        
        
        # Add header container (full width, zero margins)
        header = create_header_container(
            resource_path("hcc-logo.png"),
            "Holy Cross Colleges, Inc.",
            "Sta. Lucia, Sta. Ana, Pampanga",
            "Information Communication Department",
            resource_path("mmd-logo.png")
        )
        main_layout.addWidget(header)
        
        # Create a form container widget with its own margins
        form_container = QWidget()
        form_container_layout = QVBoxLayout(form_container)
        form_container_layout.setContentsMargins(10, 10, 10, 10)
        form_container_layout.setSpacing(10)
        
        # Title for the form section
        student_title = QLabel("Student Information")
        student_title.setAlignment(Qt.AlignCenter)
        student_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-bottom: 10px;")
        form_container_layout.addWidget(student_title)
        
        # Name fields layout (Surname, First Name, MI, Extension)
        name_layout = QHBoxLayout()
        for label_text in ["Surname", "First Name", "MI.", "Ext."]:
            sub_layout = QVBoxLayout()
            line_edit = QLineEdit()
            line_edit.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(line_edit)
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(label)
            name_layout.addLayout(sub_layout)
            if label_text == "Surname":
                self.surname_edit = line_edit
            elif label_text == "First Name":
                self.first_name_edit = line_edit
            elif label_text == "MI.":
                self.mi_edit = line_edit
            elif label_text == "Ext.":
                self.extension_edit = line_edit
        
        self.surname_edit.textChanged.connect(self.onSurnameTextChanged)
        self.first_name_edit.textChanged.connect(self.onFirstNameTextChanged)
        self.mi_edit.textChanged.connect(self.onMITextChanged)
        
        name_form = QFormLayout()
        name_form.addRow("Name:", name_layout)
        form_container_layout.addLayout(name_form)
        
        # Additional fields
        extra_form = QFormLayout()
        address_layout = QHBoxLayout()
        for field in ["Barangay", "Town/Municipality", "Province"]:
            sub_layout = QVBoxLayout()
            line_edit = QLineEdit()
            line_edit.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(line_edit)
            label = QLabel(field)
            label.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(label)
            address_layout.addLayout(sub_layout)
            if field == "Barangay":
                self.barangay_edit = line_edit
            elif field == "Town/Municipality":
                self.town_edit = line_edit
            elif field == "Province":
                self.province_edit = line_edit
        extra_form.addRow("Address:", address_layout)
        
        self.student_id_edit = QLineEdit()
        extra_form.addRow("Student ID:", self.student_id_edit)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year"])
        extra_form.addRow("Year:", self.year_combo)
        
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
            "Bachelor of Science in Business Administration - Major in Financial Management",
            "Bachelor of Science in Business Administration - Major in Marketing Management",
            "Bachelor of Science in Business Administration - Major in Human Resources Management",
            "Bachelor of Science in Business Administration - Major in Operations Management",
            "Bachelor of Elementary Education",
            "Bachelor of Secondary Education - Major in English",
            "Bachelor of Secondary Education - Major in Mathematics",
            "Bachelor of Secondary Education - Major in Science",
            "Bachelor of Secondary Education - Major in Filipino",
            "Associate in Computer Technology"
        ])
        extra_form.addRow("Course:", self.course_combo)
        form_container_layout.addLayout(extra_form)
        
        # Emergency contact section
        em_title, em_layout = self.create_emergency_section("Student")
        form_container_layout.addWidget(em_title)
        form_container_layout.addLayout(em_layout)
        
        # Bottom buttons: Back, Submit, Ñ, and ñ
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.setContentsMargins(0, 0, 0, 0)
        bottom_button_layout.setSpacing(10)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("padding: 8px;")
        back_button.clicked.connect(self.go_back)

        submit_button = QPushButton("Submit Registration")
        submit_button.setStyleSheet("""
    QPushButton {
        background-color: #28a745;  /* Green background */
        color: white;              /* White text */
        font-weight: bold;         /* Bold text */
        padding: 8px;
        border-radius: 5px;        /* Rounded corners */
    }
    QPushButton:hover {
        background-color: #218838; /* Darker green on hover */
    }
    QPushButton:pressed {
        background-color: #1e7e34; /* Even darker green when pressed */
    }
""")
        submit_button.clicked.connect(self.submit_registration)

        # Button for uppercase Ñ
        uppercase_enye_button = QToolButton()
        uppercase_enye_button.setText("Ñ")
        uppercase_enye_button.setStyleSheet("font-size: 14pt; padding: 5px;")
        uppercase_enye_button.clicked.connect(self.insert_uppercase_enye)

        # Button for lowercase ñ
        lowercase_enye_button = QToolButton()
        lowercase_enye_button.setText("ñ")
        lowercase_enye_button.setStyleSheet("font-size: 14pt; padding: 5px;")
        lowercase_enye_button.clicked.connect(self.insert_lowercase_enye)

        bottom_button_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        bottom_button_layout.addStretch(1)
        bottom_button_layout.addWidget(uppercase_enye_button, alignment=Qt.AlignRight)
        bottom_button_layout.addWidget(lowercase_enye_button, alignment=Qt.AlignRight)
        bottom_button_layout.addWidget(submit_button, alignment=Qt.AlignRight)

        form_container_layout.addLayout(bottom_button_layout)
        
        main_layout.addWidget(form_container)
        self.setLayout(main_layout)
    
    def onSurnameTextChanged(self, text):
        new_text = text.upper()
        if new_text != text:
            self.surname_edit.blockSignals(True)
            self.surname_edit.setText(new_text)
            self.surname_edit.blockSignals(False)
    
    def onFirstNameTextChanged(self, text):
        words = text.split(" ")
        if words and words[-1] == "":
            new_text = " ".join(word.capitalize() for word in words[:-1]) + " "
        else:
            new_text = " ".join(word.capitalize() for word in words)
        if new_text != text:
            self.first_name_edit.blockSignals(True)
            self.first_name_edit.setText(new_text)
            self.first_name_edit.blockSignals(False)
    
    def onMITextChanged(self, text):
        if not text:
            return
        new_text = text.upper()
        if not new_text.endswith("."):
            new_text += "."
        new_text = new_text[:2]
        if new_text != text:
            self.mi_edit.blockSignals(True)
            self.mi_edit.setText(new_text)
            self.mi_edit.blockSignals(False)
    
    def submit_registration(self):
        surname = self.surname_edit.text().strip()
        first_name = self.first_name_edit.text().strip()
        mi = self.mi_edit.text().strip()
        extension = self.extension_edit.text().strip()
        barangay = self.barangay_edit.text().strip()
        town = self.town_edit.text().strip()
        province = self.province_edit.text().strip()
        address = f"{barangay}, {town}, {province}"
        student_id = self.student_id_edit.text().strip()
        year = self.year_combo.currentText()
        course = self.course_combo.currentText()
        emergency_name = self.emergency_name_edit.text().strip()
        emergency_relation = self.emergency_relation_edit.text().strip()
        emergency_contact = self.emergency_contact_edit.text().strip()
        
        required_fields = {
            "Surname": surname,
            "First Name": first_name,
            "Middle Initial": mi,
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
        
        if len(emergency_contact) != 11:
            QMessageBox.warning(self, "Input Error", 
                "Emergency Contact Number must be exactly 11 digits.")
            return
        
        conn = connect_to_database(user_role="student")
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Duplicate Entry", "This Student ID already exists.")
            conn.close()
            return
        
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
        self.emergency_relation_edit.clear()
        self.emergency_contact_edit.clear()


# --- Employee Information Form (similar structure) ---
class EmployeeInformationForm(BaseInformationForm):
    def __init__(self):
        super().__init__("Employee Registration", resource_path("mmd-logo.png"))
        self.setGeometry(275, 70, 800, 600)
        self.showMaximized()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margin for overall window

        header = create_header_container(
            resource_path("hcc-logo.png"),
            "Holy Cross Colleges, Inc.",
            "Sta. Lucia, Sta. Ana, Pampanga",
            "Information Communication Department",
            resource_path("mmd-logo.png")
        )
        main_layout.addWidget(header)
        
        form_container = QWidget()
        form_container_layout = QVBoxLayout(form_container)
        form_container_layout.setContentsMargins(10, 10, 10, 10)
        form_container_layout.setSpacing(10)
        
        emp_title = QLabel("Employee Information")
        emp_title.setAlignment(Qt.AlignCenter)
        emp_title.setStyleSheet("font-weight: bold; font-size: 14pt; margin-bottom: 10px;")
        form_container_layout.addWidget(emp_title)
        
        name_layout = QHBoxLayout()
        for label_text in ["Surname", "First Name", "MI.", "Ext."]:
            sub_layout = QVBoxLayout()
            line_edit = QLineEdit()
            line_edit.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(line_edit)
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(label)
            name_layout.addLayout(sub_layout)
            if label_text == "Surname":
                self.surname_edit = line_edit
            elif label_text == "First Name":
                self.first_name_edit = line_edit
            elif label_text == "MI.":
                self.mi_edit = line_edit
            elif label_text == "Ext.":
                self.extension_edit = line_edit
        
        self.surname_edit.textChanged.connect(self.onSurnameTextChanged)
        self.first_name_edit.textChanged.connect(self.onFirstNameTextChanged)
        self.mi_edit.textChanged.connect(self.onMITextChanged)
        
        name_form = QFormLayout()
        name_form.addRow("Name:", name_layout)
        form_container_layout.addLayout(name_form)
        
        extra_form = QFormLayout()
        address_layout = QHBoxLayout()
        for field in ["Barangay", "Town/Municipality", "Province"]:
            sub_layout = QVBoxLayout()
            line_edit = QLineEdit()
            line_edit.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(line_edit)
            label = QLabel(field)
            label.setAlignment(Qt.AlignCenter)
            sub_layout.addWidget(label)
            address_layout.addLayout(sub_layout)
            if field == "Barangay":
                self.barangay_edit = line_edit
            elif field == "Town/Municipality":
                self.town_edit = line_edit
            elif field == "Province":
                self.province_edit = line_edit
        extra_form.addRow("Address:", address_layout)
        
        self.employee_id_edit = QLineEdit()
        extra_form.addRow("Employee ID:", self.employee_id_edit)
        
        self.department_edit = QLineEdit()
        extra_form.addRow("Department:", self.department_edit)
        
        self.position_edit = QLineEdit()
        extra_form.addRow("Position:", self.position_edit)
        form_container_layout.addLayout(extra_form)
        
        em_title, em_layout = self.create_emergency_section("Employee")
        form_container_layout.addWidget(em_title)
        form_container_layout.addLayout(em_layout)
        
        # Bottom buttons: Back, Submit, Ñ, and ñ
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.setContentsMargins(0, 0, 0, 0)
        bottom_button_layout.setSpacing(10)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("padding: 8px;")
        back_button.clicked.connect(self.go_back)

        submit_button = QPushButton("Submit Registration")
        submit_button.setStyleSheet("""
    QPushButton {
        background-color: #28a745;  /* Green background */
        color: white;              /* White text */
        font-weight: bold;         /* Bold text */
        padding: 8px;
        border-radius: 5px;        /* Rounded corners */
    }
    QPushButton:hover {
        background-color: #218838; /* Darker green on hover */
    }
    QPushButton:pressed {
        background-color: #1e7e34; /* Even darker green when pressed */
    }
""")
        submit_button.clicked.connect(self.emp_submit)

        # Button for uppercase Ñ
        uppercase_enye_button = QToolButton()
        uppercase_enye_button.setText("Ñ")
        uppercase_enye_button.setStyleSheet("font-size: 14pt; padding: 5px;")
        uppercase_enye_button.clicked.connect(self.insert_uppercase_enye)

        # Button for lowercase ñ
        lowercase_enye_button = QToolButton()
        lowercase_enye_button.setText("ñ")
        lowercase_enye_button.setStyleSheet("font-size: 14pt; padding: 5px;")
        lowercase_enye_button.clicked.connect(self.insert_lowercase_enye)

        bottom_button_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        bottom_button_layout.addStretch(1)
        bottom_button_layout.addWidget(uppercase_enye_button, alignment=Qt.AlignRight)
        bottom_button_layout.addWidget(lowercase_enye_button, alignment=Qt.AlignRight)
        bottom_button_layout.addWidget(submit_button, alignment=Qt.AlignRight)

        form_container_layout.addLayout(bottom_button_layout)
        
        main_layout.addWidget(form_container)
        self.setLayout(main_layout)
    
    def onSurnameTextChanged(self, text):
        new_text = text.upper()
        if new_text != text:
            self.surname_edit.blockSignals(True)
            self.surname_edit.setText(new_text)
            self.surname_edit.blockSignals(False)
    
    def onFirstNameTextChanged(self, text):
        words = text.split(" ")
        if words and words[-1] == "":
            new_text = " ".join(word.capitalize() for word in words[:-1]) + " "
        else:
            new_text = " ".join(word.capitalize() for word in words)
        if new_text != text:
            self.first_name_edit.blockSignals(True)
            self.first_name_edit.setText(new_text)
            self.first_name_edit.blockSignals(False)
    
    def onMITextChanged(self, text):
        if not text:
            return
        new_text = text.upper()
        if not new_text.endswith("."):
            new_text += "."
        new_text = new_text[:2]
        if new_text != text:
            self.mi_edit.blockSignals(True)
            self.mi_edit.setText(new_text)
            self.mi_edit.blockSignals(False)
    
    def emp_submit(self):
        surname = self.surname_edit.text().strip()
        first_name = self.first_name_edit.text().strip()
        mi = self.mi_edit.text().strip()
        extension = self.extension_edit.text().strip()
        barangay = self.barangay_edit.text().strip()
        town = self.town_edit.text().strip()
        province = self.province_edit.text().strip()
        address = f"{barangay}, {town}, {province}"
        employee_id = self.employee_id_edit.text().strip()
        department = self.department_edit.text().strip()
        position = self.position_edit.text().strip()
        emergency_name = self.emergency_name_edit.text().strip()
        emergency_relation = self.emergency_relation_edit.text().strip()
        emergency_contact = self.emergency_contact_edit.text().strip()
        
        required_fields = {
            "Surname": surname,
            "First Name": first_name,
            "Middle Initial": self.mi_edit.text().strip(),
            "Barangay": barangay,
            "Town/Municipality": town,
            "Province": province,
            "Employee ID": employee_id,
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
        
        if len(emergency_contact) != 11:
            QMessageBox.warning(self, "Input Error",
                "Emergency Contact Number must be exactly 11 digits.")
            return
        
        conn = connect_to_database(user_role="employee")
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Duplicate Entry", "This Employee ID already exists.")
            conn.close()
            return
        
        query = """
            INSERT INTO employees (employee_id, surname, first_name, mi, extension, 
                                    address, department, position, emergency_name, emergency_relation, emergency_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (employee_id, surname, first_name, mi, extension, address, department, position,
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
        self.department_edit.clear()
        self.position_edit.clear()
        self.emergency_name_edit.clear()
        self.emergency_relation_edit.clear()
        self.emergency_contact_edit.clear()