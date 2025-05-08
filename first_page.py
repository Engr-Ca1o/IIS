import os, sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui     import QFont, QIcon, QPixmap, QPainter, QPainterPath, QFontMetrics, QPen
from PyQt5.QtCore    import Qt
import iisforms

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class StrokeLabel(QLabel):
    def __init__(self, text="", parent=None,
                 stroke_color=Qt.black, stroke_width=2,
                 text_color=Qt.black):
        super().__init__(text, parent)
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width
        self._text_color = text_color
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        fm = QFontMetrics(self.font())
        text_rect = fm.boundingRect(self.text())
        x = (self.width()  - text_rect.width())  / 2
        y = (self.height() - text_rect.height()) / 2 + fm.ascent()
        path = QPainterPath()
        path.addText(x, y, self.font(), self.text())
        pen = QPen(self._stroke_color, self._stroke_width,
                   Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._text_color)
        painter.drawPath(path)

class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Identification and Information System")
        self.setGeometry(275, 70, 900, 600)
        self.showMaximized()

        # Load images via resource_path
        self.bg_image   = QPixmap(resource_path("arial.jpg"))
        self.logo_label = QLabel(self)
        logo_pixmap    = QPixmap(resource_path("hcc-logo.png"))
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(250, 250)
        self.logo_label.setStyleSheet("background: transparent; margin: 25px;")

        self.setStyleSheet("""
            QWidget { background-color: #45b6fe; }
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
                border: 2px solid;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #ffdb4d; }
            QLabel { color: #0033cc; }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        welcome_label = StrokeLabel("IDENTIFICATION AND INFORMATION SYSTEM",
                                   stroke_color=Qt.white, stroke_width=5,
                                   text_color=Qt.black)
        welcome_label.setFont(QFont("Segoe UI", 25, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("background: transparent; margin: 25px;")
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        studBtn = QPushButton("Student")
        studBtn.setFont(QFont("Segoe UI", 20, QFont.Bold))
        studBtn.clicked.connect(self.stud_registration)
        button_layout.addWidget(studBtn)

        empBtn = QPushButton("Employee")
        empBtn.setFont(QFont("Segoe UI", 20, QFont.Bold))
        empBtn.clicked.connect(self.emp_registration)
        button_layout.addWidget(empBtn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def stud_registration(self):
        self.reg_form = iisforms.StudentInformationForm()
        self.reg_form.show()
        self.close()

    def emp_registration(self):
        self.reg_form = iisforms.EmployeeInformationForm()
        self.reg_form.show()
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.3)
        if not self.bg_image.isNull():
            painter.drawPixmap(self.rect(), self.bg_image)
        super().paintEvent(event)

def open_app_landing():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("mmd-logo.png")))
    window = Page()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    open_app_landing()