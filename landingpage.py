import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPainterPath, QFontMetrics, QPen
from PyQt5.QtCore import Qt
from forms import StudentInformationForm, EmployeeInformationForm

class StrokeLabel(QLabel):
    """
    A QLabel subclass that draws text with an outline (stroke).
    """
    def __init__(self, text="", parent=None,
                 stroke_color=Qt.black, stroke_width=2,
                 text_color=Qt.black):
        super().__init__(text, parent)
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width
        self._text_color = text_color
        
        # Make the label background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Center the text in the label
        fm = QFontMetrics(self.font())
        text_rect = fm.boundingRect(self.text())
        x = (self.width() - text_rect.width()) / 2
        y = (self.height() - text_rect.height()) / 2 + fm.ascent()

        # Create a path for the text
        path = QPainterPath()
        path.addText(x, y, self.font(), self.text())

        # Draw the stroke (outline)
        pen = QPen(self._stroke_color, self._stroke_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # Fill the text
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._text_color)
        painter.drawPath(path)

class LandingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Landing Page")
        self.setGeometry(100, 100, 500, 400)
        
        # Load the background image (update the path as needed)
        self.bg_image = QPixmap("arial.jpg")
        
        # Set a global stylesheet with a fresh font style
        self.setStyleSheet("""
            QWidget {
                background-color: #45b6fe; 
            }
                     
            QPushButton {
                background-color: #ffffff; 
                color: #0033cc; 
                font-weight: bold; 
                border: 2px solid;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45b6fe;
            }
            QLabel {
                color: #0033cc;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Add a logo at the top (optional)  
        self.logo_label = QLabel(self)
        pixmap = QPixmap("hcc-logo.png")  # Update with your logo path
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap)
        else:
            print("Logo not loaded.")
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(350, 350)
        self.logo_label.setStyleSheet("background: transparent; margin: 25px;")
        self.logo_label.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        
        # Welcome label with stroke applied
        welcome_label = StrokeLabel("IDENTIFICATION AND INFORMATION SYSTEM",
                                    stroke_color=Qt.white,
                                    stroke_width=5,
                                    text_color=Qt.black)
        welcome_label.setFont(QFont("Segoe UI", 25, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("background: transparent; margin: 25px;")
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)
        
        # student button
        studBtn = QPushButton("Student")
        studBtn.setFont(QFont("Segoe UI", 20, QFont.Bold))
        studBtn.setStyleSheet("color: black;")
        studBtn.clicked.connect(self.stud_registration)
        layout.addWidget(studBtn, alignment=Qt.AlignCenter)

        # Proceed button
        empBtn = QPushButton("Employee")
        empBtn.setFont(QFont("Segoe UI", 20, QFont.Bold))
        empBtn.setStyleSheet("color: black;")
        empBtn.clicked.connect(self.emp_registration)
        layout.addWidget(empBtn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
    
    def stud_registration(self):
        self.reg_form = StudentInformationForm()
        self.reg_form.show()
        self.close()


    def emp_registration(self):
        self.reg_form = EmployeeInformationForm()
        self.reg_form.show()
        self.close()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # Set low opacity for the background image
        painter.setOpacity(0.3)  # Adjust the opacity as needed
        if not self.bg_image.isNull():
            # Draw the background image scaled to the widget size
            painter.drawPixmap(self.rect(), self.bg_image)
        super().paintEvent(event)

def open_student_landing():
    app = QApplication(sys.argv)
    window = LandingPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    open_student_landing()
