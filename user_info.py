# from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QMessageBox
# from PyQt5.QtCore import Qt
# from Ui_card import Card
# from PyQt5.QtGui import QPixmap

# class UserInfoScreen(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         root = QVBoxLayout(self)
#         root.setAlignment(Qt.AlignCenter)
#         card = Card()
#         root.addWidget(card)

#         # Image/logo
#         # Image/logo
#         logo = QLabel()
#         pixmap = QPixmap("img1.png")  # your folder path
#         pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         logo.setPixmap(pixmap)
#         logo.setAlignment(Qt.AlignCenter)
#         card.layout.addWidget(logo)

#         # Title
#         title = QLabel("User Information")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size:28px; font-weight:bold;")
#         card.layout.addWidget(title)

#         # Inputs
#         self.name = QLineEdit()
#         self.name.setPlaceholderText("Full Name")
#         card.layout.addWidget(self.name)

#         self.age = QLineEdit()
#         self.age.setPlaceholderText("Age")
#         card.layout.addWidget(self.age)

#         self.gender = QComboBox()
#         self.gender.addItems(["Select Gender", "Male", "Female"])
#         card.layout.addWidget(self.gender)

#         self.cnic = QLineEdit()
#         self.cnic.setPlaceholderText("CNIC")
#         card.layout.addWidget(self.cnic)

#         # Next button
#         next_btn = QPushButton("Next")
#         next_btn.clicked.connect(self.next)
#         card.layout.addWidget(next_btn)

#     def next(self):
#         if (not self.name.text() or not self.age.text() or
#             self.gender.currentIndex() == 0 or not self.cnic.text()):
#             QMessageBox.warning(self, "Error", "Please complete all fields")
#             return
#         if not self.age.text().isdigit():
#             QMessageBox.warning(self, "Error", "Age must be a number")
#             return

#         # Use CNIC as local user_id
#         user_id = self.cnic.text()
#         self.main.go_to_test_selection(user_id)
        

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Ui_card import Card


class UserInfoScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # -------- Root layout --------
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # -------- Centering logic --------
        root.addStretch()

        card = Card()
        card.setFixedWidth(450)  # keeps UI clean & centered
        root.addWidget(card, alignment=Qt.AlignCenter)

        root.addStretch()

        # -------- Logo --------
        logo = QLabel()
        pixmap = QPixmap("logo\img1.png").scaled(
            120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        card.layout.addWidget(logo)

        # -------- Title --------
        title = QLabel("User Information")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px; font-weight:bold;")
        card.layout.addWidget(title)

        # -------- Inputs --------
        self.name = QLineEdit()
        self.name.setPlaceholderText("Full Name")
        card.layout.addWidget(self.name)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        self.age.setMaxLength(3)
        card.layout.addWidget(self.age)

        self.gender = QComboBox()
        self.gender.addItems(["Select Gender", "Male", "Female"])
        card.layout.addWidget(self.gender)

        self.cnic = QLineEdit()
        self.cnic.setPlaceholderText("CNIC")
        card.layout.addWidget(self.cnic)

        # -------- Button --------
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next)
        card.layout.addWidget(next_btn)

    # -------- Validation --------
    def next(self):
        if not all([
            self.name.text(),
            self.age.text(),
            self.cnic.text(),
            self.gender.currentIndex() != 0
        ]):
            QMessageBox.warning(self, "Error", "Please complete all fields")
            return

        if not self.age.text().isdigit():
            QMessageBox.warning(self, "Error", "Age must be a number")
            return

        user_id = self.cnic.text()
        self.main.go_to_test_selection(user_id)

