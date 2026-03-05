import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Ui_card import Card

# ----------------- Results Dialog -----------------
class ResultsDialog(QDialog):
    def __init__(self, depression_score, dementia_score, language="en"):
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

        if language == "ja":
            text = f"うつスコア: {depression_score}\n認知スコア: {dementia_score}"
            close_text = "閉じる"
        else:
            text = f"Depression Score: {depression_score}\nDementia Score: {dementia_score}"
            close_text = "Close"

        results_label = QLabel(text)
        results_label.setAlignment(Qt.AlignCenter)
        results_label.setWordWrap(True)
        results_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(results_label)

        close_btn = QPushButton(close_text)
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

# ----------------- Dementia Screen -----------------
class DementiaScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # ----------------- Tasks -----------------
        self.tasks_en = [
            ("What year is it?", ["2025", "2026"], "2026", 5),
            ("Where are you right now?", ["🏠 Home", "🏥 Hospital"], "🏠 Home", 5),
            ("Remember first item & click", ["🍎 Apple", "🔑 Key"], "🍎 Apple", 3),
            ("Calculation\n100 − 7 =", ["93", "91"], "93", 5),
            ("What do we use to write?", ["✏️ Pen", "🥄 Spoon"], "✏️ Pen", 1),
            ("What did you see before?", ["🍎 Apple", "🚗 Car"], "🍎 Apple", 3),
            ("Name the object", ["✏️ Pen", "⌚ Watch"], "⌚ Watch", 1),
            ("Repeat the phrase", ["Accept", "Reject"], "Accept", 1),
            ("Paper Activity", ["Accept", "Reject"], "Accept", 3),
            ("Close your eyes", ["Accept", "Reject"], "Accept", 1),
            ("Write a sentence", ["Accept", "Reject"], "Accept", 1),
            ("Copy this picture", ["Accept", "Reject"], "Accept", 1),
        ]

        self.tasks_ja = [
            ("今年は何年ですか？", ["2025年", "2026年"], "2026年", 5),
            ("今どこにいますか？", ["🏠 家", "🏥 病院"], "🏠 家", 5),
            ("最初のアイテムを覚えて選んでください", ["🍎 りんご", "🔑 鍵"], "🍎 りんご", 3),
            ("計算\n100 − 7 =", ["93", "91"], "93", 5),
            ("書くときに使うものは何ですか？", ["✏️ ペン", "🥄 スプーン"], "✏️ ペン", 1),
            ("前に見たものは何ですか？", ["🍎 りんご", "🚗 車"], "🍎 りんご", 3),
            ("この物の名前は？", ["✏️ ペン", "⌚ 時計"], "⌚ 時計", 1),
            ("フレーズを繰り返してください", ["承認", "拒否"], "承認", 1),
            ("紙の指示に従ってください", ["承認", "拒否"], "承認", 3),
            ("目を閉じてください", ["承認", "拒否"], "承認", 1),
            ("文章を書いてください", ["承認", "拒否"], "承認", 1),
            ("この図をコピーしてください", ["承認", "拒否"], "承認", 1),
        ]

        self.tasks = self.tasks_en
        self.total_points = sum(t[3] for t in self.tasks_en)
        self.step = 0
        self.answers = []
        self.editing_mode = False

        # ----------------- UI Layout -----------------
        root = QVBoxLayout(self)
        root.addStretch()

        self.card = Card()
        self.card.setFixedWidth(420)
        root.addWidget(self.card, alignment=Qt.AlignCenter)
        root.addStretch()

        # Navigation
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("⬅")
        self.prev_btn.setFixedWidth(45)
        self.prev_btn.setStyleSheet("font-size:22px; border:none;")
        self.prev_btn.clicked.connect(self.go_previous)

        self.progress = QLabel()
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setStyleSheet("font-weight:bold; font-size:16px;")

        self.next_btn = QPushButton("➡")
        self.next_btn.setFixedWidth(45)
        self.next_btn.setStyleSheet("font-size:22px; border:none;")
        self.next_btn.clicked.connect(self.go_next)

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.progress, stretch=1)
        nav_layout.addWidget(self.next_btn)
        self.card.layout.addLayout(nav_layout)

        # Icon
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)
        self.card.layout.addWidget(self.icon)

        # Score
        self.score_lbl = QLabel()
        self.score_lbl.setAlignment(Qt.AlignCenter)
        self.score_lbl.setStyleSheet("font-weight:bold; font-size:18px;")
        self.card.layout.addWidget(self.score_lbl)

        # Question
        self.question = QLabel()
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setWordWrap(True)
        self.question.setStyleSheet("font-weight:bold; font-size:22px;")
        self.card.layout.addWidget(self.question)

        # Answer Buttons
        self.buttons = []
        self.normal_style = "font-weight:bold; font-size:20px;"
        self.selected_style = """
        QPushButton {
            font-weight:bold;
            font-size:20px;
            background-color: #6a0dad;   
            color: white;
            border-radius: 6px;
        }
        """
        for _ in range(2):
            btn = QPushButton()
            btn.setStyleSheet(self.normal_style)
            btn.clicked.connect(self.select_answer)
            self.buttons.append(btn)
            self.card.layout.addWidget(btn)

        # Close & Results Buttons
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(lambda: self.window().close())
        self.close_btn.hide()
        self.card.layout.addWidget(self.close_btn, alignment=Qt.AlignCenter)

        self.results_btn = QPushButton("View Combined Results")
        self.results_btn.clicked.connect(self.show_combined_results)
        self.results_btn.hide()
        self.card.layout.addWidget(self.results_btn, alignment=Qt.AlignCenter)

        # Icon path
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

    # ----------------- Start -----------------
    def start(self, user_id):
        self.user_id = user_id
        self.tasks = self.tasks_en if self.main.language == "en" else self.tasks_ja
        self.total_points = sum(t[3] for t in self.tasks)
        self.step = 0
        self.answers = [None] * len(self.tasks)
        self.editing_mode = False

        self.icon.show()
        self.progress.show()
        self.score_lbl.show()
        self.prev_btn.show()
        self.next_btn.show()
        self.close_btn.hide()
        self.results_btn.hide()

        for btn in self.buttons:
            btn.show()

        self.load_task()

    # ----------------- Load Task -----------------
    def load_task(self):
        if self.step >= len(self.tasks):
            self.finish()
            return

        question, options, _, _ = self.tasks[self.step]

        pixmap = QPixmap(os.path.join(self.icon_path, f"p{self.step + 1}.png"))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon.setPixmap(pixmap)
        else:
            self.icon.clear()

        self.progress.setText(f"Step {self.step + 1} of {len(self.tasks)}")

        current_score = sum(points for i, (_, _, correct, points) in enumerate(self.tasks)
                            if self.answers[i] == correct)

        if self.main.language == "ja":
            self.score_lbl.setText(f"スコア: {current_score}/{self.total_points}")
        else:
            self.score_lbl.setText(f"Score: {current_score}/{self.total_points}")

        self.question.setText(question)

        for i, btn in enumerate(self.buttons):
            btn.setText(options[i])
            btn.setStyleSheet(self.normal_style)

        if self.answers[self.step] is not None:
            for btn in self.buttons:
                if btn.text() == self.answers[self.step]:
                    btn.setStyleSheet(self.selected_style)

        self.prev_btn.setEnabled(self.step > 0)
        self.next_btn.setEnabled(self.answers[self.step] is not None)

    # ----------------- Navigation -----------------
    def go_next(self):
        if self.answers[self.step] is None:
            return
        if self.step < len(self.tasks) - 1:
            self.step += 1
            self.load_task()
        else:
            self.finish()

    def go_previous(self):
        if self.step > 0:
            self.step -= 1
            self.editing_mode = True
            self.load_task()

    def select_answer(self):
        selected = self.sender().text()
        self.answers[self.step] = selected
        for btn in self.buttons:
            btn.setStyleSheet(self.selected_style if btn.text() == selected else self.normal_style)
        self.next_btn.setEnabled(True)
        if not self.editing_mode:
            self.go_next()

    # ----------------- Finish -----------------
    def finish(self):
        final_score = sum(points for i, (_, _, correct, points) in enumerate(self.tasks)
                          if self.answers[i] == correct)

        if final_score >= 24:
            result_en = "Normal Cognitive Function"
            result_ja = "正常な認知機能"
        elif final_score >= 18:
            result_en = "Mild Cognitive Impairment"
            result_ja = "軽度認知障害"
        elif final_score >= 9:
            result_en = "Moderate Impairment"
            result_ja = "中等度障害"
        else:
            result_en = "Severe Cognitive Impairment"
            result_ja = "重度認知障害"

        result = result_ja if self.main.language == "ja" else result_en
        self.question.setText(f"{result}\n\nFinal Score: {final_score}/{self.total_points}"
                              if self.main.language == "en"
                              else f"{result}\n\n最終スコア: {final_score}/{self.total_points}")

        # Hide navigation and answer buttons
        self.icon.hide()
        self.progress.hide()
        self.score_lbl.hide()
        self.prev_btn.hide()
        self.next_btn.hide()
        for btn in self.buttons:
            btn.hide()

        # Show Close and Results buttons
        self.close_btn.show()
        self.results_btn.show()

        # Store dementia score
        self.dementia_score = final_score

    # ----------------- Show Combined Results -----------------
    def show_combined_results(self):
        depression_score = getattr(self.main.depression, "score", "N/A")
        dlg = ResultsDialog(depression_score, self.dementia_score, self.main.language)
        dlg.exec_()