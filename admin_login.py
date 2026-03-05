from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Ui_card import Card


class AdminLogin(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # -------- Root layout --------
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        root.addStretch()

        # -------- Card --------
        card = Card()
        card.setFixedWidth(500)  # Same width as UserInfo
        root.addWidget(card, alignment=Qt.AlignCenter)

        root.addStretch()

        # -------- Logo --------
        logo = QLabel()
        pixmap = QPixmap("logo\img3.png").scaled(
            120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        card.layout.addWidget(logo)

        # -------- Title --------
        title = QLabel("Admin Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:30px; font-weight:bold;")
        card.layout.addWidget(title)

        # -------- Email --------
        self.email = QLineEdit()
        self.email.setPlaceholderText("Admin Email")
        card.layout.addWidget(self.email)

        # -------- Password --------
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        card.layout.addWidget(self.password)

        # -------- Button --------
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        card.layout.addWidget(login_btn)

    # -------- Login Logic --------
    def login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password")
            return

        ADMIN_EMAIL = "admin@clinic.com"
        ADMIN_PASSWORD = "admin"

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.email.clear()
            self.password.clear() 
            self.main.show_main_app()
        else:
            QMessageBox.critical(self, "Error", "Invalid email or password")