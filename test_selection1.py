import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Ui_card import Card


class TestSelectionScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # ---------------- Root Layout ----------------
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        root.setSpacing(20)

        # ---------------- Card Container ----------------
        self.card = Card()
        root.addWidget(self.card)

        # ---------------- Title ----------------
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)
        self.card.layout.addWidget(self.title)

        # ---------------- Depression Section ----------------
        self.dep_icon = QLabel()
        dep_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo\search.png")
        dep_pix = QPixmap(dep_icon_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.dep_icon.setPixmap(dep_pix)
        self.dep_icon.setAlignment(Qt.AlignCenter)
        self.card.layout.addWidget(self.dep_icon)

        self.dep_btn = QPushButton()
        self.dep_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.dep_btn.clicked.connect(self.main.ask_depression)
        self.card.layout.addWidget(self.dep_btn)

        # ---------------- Dementia Section ----------------
        self.dem_icon = QLabel()
        dem_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo\search.png")
        dem_pix = QPixmap(dem_icon_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.dem_icon.setPixmap(dem_pix)
        self.dem_icon.setAlignment(Qt.AlignCenter)
        self.card.layout.addWidget(self.dem_icon)

        self.dem_btn = QPushButton()
        self.dem_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.dem_btn.clicked.connect(self.main.ask_dementia)
        self.card.layout.addWidget(self.dem_btn)

        # ---------------- Initialize Language ----------------
        self.reset_buttons_and_title()

    # ---------------- Reset Buttons and Title ----------------
    def reset_buttons_and_title(self):
        """Reset the start buttons and title based on language."""
        if self.main.language == "en":
            self.title.setText("Smart Health Screening")
        else:
            self.title.setText("スマート健康診断")

        # Always display Start test #1 / #2
        self.dep_btn.setText("Start test #1")
        self.dem_btn.setText("Start test #2")

    # ---------------- Optional: Call this if language changes ----------------
    def update_language(self):
        """If the user changes language mid-session, update title but keep buttons as Start test #1/2."""
        self.reset_buttons_and_title()