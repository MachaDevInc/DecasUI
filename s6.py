from w6 import Ui_MainWindow6
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
class MyMainWindow(QMainWindow, Ui_MainWindow6):
    def __init__(self, parent=None):
        super(MyMainWindow,self).__init__(parent)

        # Set window properties
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

