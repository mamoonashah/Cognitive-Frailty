import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout
from user_info import UserInfoScreen
from test_selection1 import TestSelectionScreen
from depression import DepressionScreen
from dementia import DementiaScreen
from admin_login import AdminLogin
from language_selection import LanguageSelectionWindow  # New pop-up


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mental Health Screening")
        self.resize(900, 700)

        # ---------------- Default language ----------------
        self.language = "en"  # default English

        # ---------------- Stack ----------------
        self.stack = QStackedLayout(self)

        # ---------------- Screens ----------------
        self.admin_login = AdminLogin(self)
        self.user_info = UserInfoScreen(self)
        self.test_selection = TestSelectionScreen(self)
        self.depression = DepressionScreen(self)
        self.dementia = DementiaScreen(self)

        # Add screens to stack
        self.stack.addWidget(self.admin_login)
        self.stack.addWidget(self.user_info)
        self.stack.addWidget(self.test_selection)
        self.stack.addWidget(self.depression)
        self.stack.addWidget(self.dementia)

        # ---------------- Start with Admin Login ----------------
        self.stack.setCurrentWidget(self.admin_login)

    # ---------------- Called after Admin Login ----------------
    def show_main_app(self):
        self.stack.setCurrentWidget(self.user_info)

    # ---------------- Go to Test Selection ----------------
    def go_to_test_selection(self, user_id):
        self.user_id = user_id
        self.stack.setCurrentWidget(self.test_selection)

    # ---------------- Language Selection before Depression ----------------
    def ask_depression(self):
        self.lang_window = LanguageSelectionWindow(self, self.start_depression)
        self.lang_window.show()

    # ---------------- Start Depression Test ----------------
    def start_depression(self):
        self.depression.start(self.user_id)
        self.stack.setCurrentWidget(self.depression)

    # ---------------- Language Selection before Dementia ----------------
    def ask_dementia(self):
        self.lang_window = LanguageSelectionWindow(self, self.start_dementia)
        self.lang_window.show()

    # ---------------- Start Dementia Test ----------------
    def start_dementia(self):
        self.dementia.start(self.user_id)
        self.stack.setCurrentWidget(self.dementia)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ---------------- Global Styles ----------------
    app.setStyleSheet("""
        QWidget {
            background-color: #5B2C6F;
            font-family: Segoe UI;
            font-weight: bold;
        }
        QLabel {
            color: #2D1B4E;
        }
        QLineEdit, QComboBox {
            padding: 12px;
            font-size: 20px;
            border-radius: 12px;
            font-weight: bold;
            border: 2.5px solid #9A84B7;
            background: white;
        }
        QPushButton {
            background-color: #9A84B7;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 14px;
            border-radius: 22px;
        }
        QPushButton:hover {
            background-color: #472573;
        }
    """)

    window = MainApp()
    window.show()
    sys.exit(app.exec_())