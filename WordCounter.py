import sys
import re
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QEvent

class WordCountWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("字数统计器")
        self.setGeometry(200, 200, 400, 300)

        self.text_edit = QTextEdit()
        self.text_edit.installEventFilter(self)

        self.chinese_count_label = QLineEdit()
        self.chinese_count_label.setReadOnly(True)
        self.chinese_count_label.setFont(QFont("Arial", 12))
        self.chinese_count_label.setAlignment(Qt.AlignCenter)

        self.english_count_label = QLineEdit()
        self.english_count_label.setReadOnly(True)
        self.english_count_label.setFont(QFont("Arial", 12))
        self.english_count_label.setAlignment(Qt.AlignCenter)

        self.digit_count_label = QLineEdit()
        self.digit_count_label.setReadOnly(True)
        self.digit_count_label.setFont(QFont("Arial", 12))
        self.digit_count_label.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.text_edit, 0, 0, 1, 2)
        layout.addWidget(QLabel("中文字符数："), 1, 0)
        layout.addWidget(self.chinese_count_label, 1, 1)
        layout.addWidget(QLabel("英文单词数："), 2, 0)
        layout.addWidget(self.english_count_label, 2, 1)
        layout.addWidget(QLabel("数字字符数："), 3, 0)
        layout.addWidget(self.digit_count_label, 3, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.last_text = ""
        self.last_chinese_count = 0
        self.last_english_count = 0
        self.last_digit_count = 0

        self.adjust_font_size()
        self.update_counts()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counts)
        self.timer.start(50)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress or event.type() == QEvent.KeyRelease:
            return False

        return super().eventFilter(obj, event)

    def update_counts(self):
        text = self.text_edit.toPlainText()

        if text == self.last_text:
            return

        start_time = time.time()

        chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))
        words = re.findall(r'\b[A-Za-z]+\b', text)
        english_count = len(words)
        digit_count = sum(1 for char in text if char.isdigit())

        end_time = time.time()

        self.chinese_count_label.setText(str(chinese_count))
        self.english_count_label.setText(str(english_count))
        self.digit_count_label.setText(str(digit_count))

        self.adjust_font_size()

        self.last_text = text

        execution_time = end_time - start_time
        print("代码执行时间：", execution_time)

    def adjust_font_size(self):
        font_size = self.width() // 85
        font = self.text_edit.font()
        font.setPointSize(font_size)
        self.text_edit.setFont(font)

        font = self.chinese_count_label.font()
        font.setPointSize(font_size)
        self.chinese_count_label.setFont(font)

        font = self.english_count_label.font()
        font.setPointSize(font_size)
        self.english_count_label.setFont(font)

        font = self.digit_count_label.font()
        font.setPointSize(font_size)
        self.digit_count_label.setFont(font)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_font_size()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordCountWindow()
    window.setStyleSheet("QMainWindow {border-radius: 10px; background-color: #F0F0F0;}")
    window.move(app.desktop().screen().rect().center() - window.rect().center())
    window.show()
    sys.exit(app.exec_())
