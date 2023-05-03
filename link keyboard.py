from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox
from keyboard_widget import get_input

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keyboard Input")
        self.setGeometry(100, 100, 400, 200)

        self.text_bar = QLineEdit(self)
        self.text_bar.setGeometry(50, 50, 300, 30)
        self.text_bar.setPlaceholderText("Enter a value")

        self.button = QPushButton(self)
        self.button.setGeometry(150, 100, 100, 30)
        self.button.setText("Enter")

        self.button.clicked.connect(self.on_click)
        self.text_bar.mousePressEvent = self.show_keyboard

    def show_keyboard(self, event):
        user_input = get_input()
        self.text_bar.setText(user_input)

    def on_click(self):
        user_input = self.text_bar.text()
        if user_input == "":
            QMessageBox.warning(self, "Warning", "Please enter a value")
        else:
            QMessageBox.information(self, "Information", f"You entered: {user_input}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
