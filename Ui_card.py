from PyQt5.QtWidgets import QFrame, QVBoxLayout


class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 20px;
            padding: 25px;
        }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(18)
