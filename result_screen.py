from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ResultsScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.results_label = QLabel()
        self.layout.addWidget(self.results_label)

    def display_results(self, user_data, depression_result, dementia_result):
        text = f"""
        Results for {user_data['name']}:

        Depression Score: {depression_result}
        Dementia Score: {dementia_result}
        """
        self.results_label.setText(text)