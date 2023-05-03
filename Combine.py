import sys
import subprocess
import time
proc1 = subprocess.Popen(["python", "main.py"])
time.sleep(10)
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


class Screen(QMainWindow):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent)
        self.screen_list = [
            Ui_MainWindow7(), Ui_MainWindow9(), Ui_MainWindow8(), Ui_MainWindow10(),
            Ui_MainWindow2(), Ui_MainWindow3(), Ui_MainWindow4(), Ui_MainWindow5(),
            Ui_MainWindow6()
        ]
        self.current_screen = 0
        self.setup_ui()

    def setup_ui(self):
        self.screen_list[self.current_screen].setupUi(self)

        if self.current_screen > 0:
            self.screen_list[self.current_screen].backwifiset.clicked.connect(self.go_back)
        if self.current_screen > 0:
            self.screen_list[self.current_screen].back.clicked.connect(self.go_back)
        if self.current_screen > 0:
            self.screen_list[self.current_screen].back.clicked.connect(self.go_back)
        if self.current_screen > 0:
            self.screen_list[self.current_screen].back.clicked.connect(self.go_back)


            # Next screen
        if self.current_screen1 < len(self.screen_list) - 1:
           self.screen_list[self.current_screen1].setting.clicked.connect(self.go_next)
        if self.current_screen1 < len(self.screen_list) - 1:

          self.screen_list[self.current_screen].wifi.clicked.connect(self.go_next)
        self.screen_list[self.current_screen].rs.clicked.connect(self.go_next)
        self.screen_list[self.current_screen].usb.clicked.connect(self.go_next)

    def go_next(self):
        self.current_screen += 1
        self.setup_ui()

    def go_back(self):
        self.current_screen -= 1
        self.setup_ui()

def main():
    app = QApplication(sys.argv)
    window = Screen()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
