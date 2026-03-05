from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class LanguageSelectionWindow(QWidget):
    def __init__(self, main, test_callback):
        """
        main: MainApp instance
        test_callback: function to call after selecting language (e.g., start_depression or start_dementia)
        """
        super().__init__()
        self.main = main
        self.test_callback = test_callback

        # ---------------- Window ----------------
        self.setWindowTitle("Select Language / 言語を選択")
        self.setFixedSize(360, 180)  # slightly larger to fit buttons properly

        # ---------------- White Background & Styling ----------------
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton {
                background-color: #9A84B7;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #472573;
            }
        """)

        # ---------------- Layout ----------------
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        # ---------------- Label ----------------
        label = QLabel("Select Language / 言語を選択")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # ---------------- Buttons ----------------
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.btn_english = QPushButton("English")
        self.btn_japanese = QPushButton("日本語")

        self.btn_english.clicked.connect(lambda: self.select_language("en"))
        self.btn_japanese.clicked.connect(lambda: self.select_language("ja"))

        btn_layout.addWidget(self.btn_english)
        btn_layout.addWidget(self.btn_japanese)
        layout.addLayout(btn_layout)

        # ---------------- Apply Layout ----------------
        self.setLayout(layout)

    # ---------------- Select Language ----------------
    def select_language(self, lang):
        self.main.language = lang  # store language in main app
        # update test selection buttons immediately
        if hasattr(self.main.test_selection, "update_language"):
            self.main.test_selection.update_language()
        self.close()  # close the pop-up
        self.test_callback()  # start the selected test