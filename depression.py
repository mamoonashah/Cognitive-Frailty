import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Ui_card import Card
# from database import save_depression_test  # Remove if not using a database

class DepressionScreen(QWidget):

    def __init__(self, main):
        super().__init__()
        self.main = main

        # ---------------- Root Layout ----------------
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addStretch()

        # ---------------- Card ----------------
        self.card = Card()
        self.card.setFixedWidth(420)
        root.addWidget(self.card, alignment=Qt.AlignCenter)
        root.addStretch()

        # ---------------- Arrow Navigation ----------------
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)

        self.back_arrow = QPushButton("⬅")
        self.forward_arrow = QPushButton("➡")
        self.back_arrow.setStyleSheet("font-weight:bold; font-size:20px;")
        self.forward_arrow.setStyleSheet("font-weight:bold; font-size:20px;")
        self.back_arrow.clicked.connect(self.prev_question)
        self.forward_arrow.clicked.connect(self.next_question)

        nav_layout.addWidget(self.back_arrow)
        nav_layout.addStretch()
        nav_layout.addWidget(self.forward_arrow)
        self.card.layout.addLayout(nav_layout)

        # ---------------- Progress ----------------
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-weight:bold; font-size:18px;")
        self.card.layout.addWidget(self.progress_label)

        # ---------------- Icon ----------------
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(130, 130)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.card.layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        # ---------------- Update Button ----------------
        self.update_btn = QPushButton("Update")
        self.update_btn.setFixedSize(90, 52)
        self.update_btn.setFocusPolicy(Qt.NoFocus)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 6px;
                padding-left: 6px;
                padding-right: 6px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.update_btn.clicked.connect(self.update_answer)
        self.update_btn.hide()
        self.card.layout.addSpacing(15)
        self.card.layout.addWidget(self.update_btn, alignment=Qt.AlignCenter)

        # ---------------- Question ----------------
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-weight:bold; font-size:22px;")
        self.card.layout.addWidget(self.question_label)

        # ---------------- YES / NO Buttons ----------------
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(30)

        self.yes_btn = QPushButton("YES")
        self.no_btn = QPushButton("NO")

        # -------- Button Styles for Highlight --------
        self.normal_style = "font-weight:bold; font-size:18px;"
        self.selected_style = """
        QPushButton {
            font-weight:bold;
            font-size:18px;
            background-color: #6a0dad;
            color: white;
            border-radius: 6px;
        }
        """

        self.yes_btn.setStyleSheet(self.normal_style)
        self.no_btn.setStyleSheet(self.normal_style)

        self.yes_btn.clicked.connect(lambda: self.select_answer(True))
        self.no_btn.clicked.connect(lambda: self.select_answer(False))

        self.btn_layout.addWidget(self.yes_btn)
        self.btn_layout.addWidget(self.no_btn)
        self.card.layout.addLayout(self.btn_layout)

        # ---------------- Back to Menu ----------------
        self.back_btn = QPushButton("Back to Test Selection")
        self.back_btn.setStyleSheet("font-weight:bold; font-size:18px;")
        self.back_btn.clicked.connect(self.back_to_menu)
        self.back_btn.hide()
        self.card.layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)

        # ---------------- Questions ----------------
        self.questions_en = [
            "Satisfied with life?",
            "Dropped many activities?",
            "Life feels empty?",
            "Often bored?",
            "In good spirits?",
            "Afraid of a bad happening?",
            "Feel happy most of the time?",
            "Feel helpless?",
            "Prefer staying at home?",
            "Memory problems?",
            "Wonderful to be alive?",
            "Feel worthless?",
            "Full of energy?",
            "Feel hopeless?",
            "Others better off than you?"
        ]

        self.questions_ja = [
            "生活に満足していますか？",
            "多くの活動をやめましたか？",
            "人生が空虚に感じますか？",
            "よく退屈しますか？",
            "気分は良いですか？",
            "悪いことが起こるのが怖いですか？",
            "ほとんどの時間、幸せを感じますか？",
            "無力だと感じますか？",
            "家にいる方が好きですか？",
            "記憶に問題がありますか？",
            "生きていることは素晴らしいと感じますか？",
            "自分には価値がないと感じますか？",
            "エネルギーに満ちていますか？",
            "希望がないと感じますか？",
            "他の人の方が自分より良い生活をしていると感じますか？"
        ]

        # True = YES indicates depressive
        self.dep_yes = [
            False, True, True, True, False,
            True, False, True, True, True,
            False, True, False, True, True
        ]

        # ---------------- Base path for icons ----------------
        self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "element")

    # ---------------- Start Test ----------------
    def start(self, user_id):
        self.user_id = user_id

        # Select language
        if self.main.language == "ja":
            self.questions = self.questions_ja
            self.yes_btn.setText("はい")
            self.no_btn.setText("いいえ")
        else:
            self.questions = self.questions_en
            self.yes_btn.setText("YES")
            self.no_btn.setText("NO")

        self.index = 0
        self.score = 0
        self.answers = [None] * len(self.questions)
        self.editing_mode = False

        self.back_arrow.show()
        self.forward_arrow.show()
        self.progress_label.show()
        self.yes_btn.show()
        self.no_btn.show()
        self.back_btn.hide()
        self.update_btn.hide()

        self.load_question()

    # ---------------- Load Question ----------------
    def load_question(self):
        if self.index < 0:
            self.index = 0
        if self.index >= len(self.questions):
            self.finish()
            return

        self.progress_label.setText(f"Question {self.index + 1} of {len(self.questions)}")
        self.question_label.setText(self.questions[self.index])

        # Restore previous highlight
        if self.answers[self.index] is not None:
            if self.answers[self.index]["answer"]:
                self.yes_btn.setStyleSheet(self.selected_style)
                self.no_btn.setStyleSheet(self.normal_style)
            else:
                self.no_btn.setStyleSheet(self.selected_style)
                self.yes_btn.setStyleSheet(self.normal_style)
        else:
            self.yes_btn.setStyleSheet(self.normal_style)
            self.no_btn.setStyleSheet(self.normal_style)

        # Load image from icon folder
        image_path = os.path.join(self.base_path, f"R{self.index + 1}.png")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.icon_label.setFixedSize(180, 180)
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.icon_label.setPixmap(pixmap)
            self.icon_label.setScaledContents(True)
        else:
            self.icon_label.clear()

        if self.answers[self.index] is not None:
            self.editing_mode = True
            self.update_btn.show()
        else:
            self.editing_mode = False
            self.update_btn.hide()

        self.forward_arrow.setEnabled(self.answers[self.index] is not None)

    # ---------------- Select Answer ----------------
    def select_answer(self, yes):
        score = 1 if (self.dep_yes[self.index] and yes) or (not self.dep_yes[self.index] and not yes) else 0
        self.answers[self.index] = {"answer": yes, "score": score}

        # Highlight selected button
        if yes:
            self.yes_btn.setStyleSheet(self.selected_style)
            self.no_btn.setStyleSheet(self.normal_style)
        else:
            self.no_btn.setStyleSheet(self.selected_style)
            self.yes_btn.setStyleSheet(self.normal_style)

        self.forward_arrow.setEnabled(True)

        if not self.editing_mode:
            self.next_question()

    # ---------------- Update Answer ----------------
    def update_answer(self):
        if self.answers[self.index] is None:
            return

        self.score = sum(a["score"] for a in self.answers if a is not None)
        self.editing_mode = False
        self.update_btn.hide()
        self.next_question()

    # ---------------- Navigation ----------------
    def next_question(self):
        if self.answers[self.index] is None:
            return

        if self.index < len(self.questions) - 1:
            self.index += 1
            self.load_question()
        else:
            self.finish()

    def prev_question(self):
        if self.index > 0:
            self.index -= 1
            self.load_question()

    # ---------------- Finish ----------------
    def finish(self):
        self.score = sum(a["score"] for a in self.answers if a is not None)

        if self.main.language == "ja":
            result_text = "うつ病の兆候は見られません" if self.score <= 5 else "うつ病の可能性があります"
        else:
            result_text = "No signs of depression" if self.score <= 5 else "Possible depression"

        # Optional: Save result
        # save_depression_test(self.user_id, self.answers, self.score, result_text)

        self.back_arrow.hide()
        self.forward_arrow.hide()
        self.progress_label.hide()
        self.yes_btn.hide()
        self.no_btn.hide()

        self.question_label.setText(result_text)
        self.icon_label.clear()
        self.back_btn.show()

    # ---------------- Back to Menu ----------------
    def back_to_menu(self):
        self.main.stack.setCurrentWidget(self.main.test_selection)