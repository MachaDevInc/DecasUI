import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from W4 import Ui_MainWindow4

class NumericKeyboard(QMainWindow, Ui_MainWindow4):
    def __init__(self):
        super(NumericKeyboard, self).__init__()
        self.setupUi(self)
        self.saved_value = ""
        # Connect buttons to their respective functions
        self.b0.clicked.connect(lambda: self.add_number('0'))
        self.b1.clicked.connect(lambda: self.add_number('1'))
        self.b2.clicked.connect(lambda: self.add_number('2'))
        self.b3.clicked.connect(lambda: self.add_number('3'))
        self.b4.clicked.connect(lambda: self.add_number('4'))
        self.b5.clicked.connect(lambda: self.add_number('5'))
        self.b6.clicked.connect(lambda: self.add_number('6'))
        self.b7.clicked.connect(lambda: self.add_number('7'))
        self.b8.clicked.connect(lambda: self.add_number('8'))
        self.b9.clicked.connect(lambda: self.add_number('9'))

        self.Del.clicked.connect(self.delete_number)
        self.enter.clicked.connect(self.enter_pressed)

        self.Retry.clicked.connect(self.retry)
    def add_number(self, number):
        current_text = self.textEdit.toPlainText()
        new_text = current_text + number
        self.textEdit.setPlainText(new_text)

    def delete_number(self):
        current_text = self.textEdit.toPlainText()
        new_text = current_text[:-1]
        self.textEdit.setPlainText(new_text)

    def enter_pressed(self):
        self.saved_value = self.textEdit.toPlainText()
        print(f"Saved value: {self.saved_value}")
        self.close()

    def get_saved_value(self):
            return self.saved_value
    def retry(self):
        self.textEdit.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumericKeyboard()
    window.show()
    sys.exit(app.exec_())
