# results.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt

class ResultsDialog(QDialog):
    def __init__(self, depression_score, dementia_score):
        super().__init__()
        self.setWindowTitle("Test Results")
        self.resize(400, 300)
        self.setStyleSheet("background-color: #5B2C6F; color: white; font-weight: bold; font-family: Segoe UI;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Combined Test Results")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        results_label = QLabel(f"Depression Score: {depression_score}\nDementia Score: {dementia_score}")
        results_label.setAlignment(Qt.AlignCenter)
        results_label.setWordWrap(True)
        results_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(results_label)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            background-color: #9A84B7;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 15px;
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        layout.setAlignment(Qt.AlignCenter)