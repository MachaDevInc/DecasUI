import sys
import subprocess
import time
proc1 = subprocess.Popen(["python", "main.py"])
time.sleep(5)
proc1.terminate()
from PyQt5.QtWidgets import QApplication, QMainWindow
from inset import Ui_MainWindow7
from RSset import Ui_MainWindow9
from wifiset import Ui_MainWindow8
from usbset import Ui_MainWindow10
from Ready import Ui_MainWindow2
from w3 import Ui_MainWindow3
from W4 import Ui_MainWindow4
from w5 import Ui_MainWindow5
from w6 import Ui_MainWindow6
class MainWindow(QMainWindow):
    def __init__(self, screen_number):
        super().__init__()

        screen_classes = [Ui_MainWindow2, Ui_MainWindow7, Ui_MainWindow9, Ui_MainWindow8, Ui_MainWindow10, Ui_MainWindow3
                          , Ui_MainWindow4, Ui_MainWindow5, Ui_MainWindow6]

        self.ui = screen_classes[screen_number]()
        self.ui.setupUi(self)

        self.screen_number = screen_number
        self.init_buttons()

    def init_buttons(self):
        back_button = getattr(self.ui, f'back{self.screen_number}' if self.screen_number != 0 else 'back', None)
        next_button = getattr(self.ui, f'next{self.screen_number}' if self.screen_number != 0 else 'next', None)

        if back_button:
            back_button.clicked.connect(self.go_back)
        if next_button:
            next_button.clicked.connect(self.go_next)

        self.ui.next4.focusInEvent = self.show_keyboard

    def go_back(self):
        if self.screen_number > 0:
            self.close()
            self.previous_screen = MainWindow(self.screen_number - 1)
            self.previous_screen.show()

    def go_next(self):
        if self.screen_number < 4:
            self.close()
            self.next_screen = MainWindow(self.screen_number + 1)
            self.next_screen.show()

    def show_keyboard(self, event):
        text, ok = QInputDialog.getText(self, 'Keyboard', 'Enter text:')
        if ok:
            self.ui.next1.setText(text)
        super().focusInEvent(event)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(0)
    window.show()
    sys.exit(app.exec_())