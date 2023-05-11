from w6 import Ui_MainWindow6
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow6):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # Set window properties
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
