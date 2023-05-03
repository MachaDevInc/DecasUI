import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # load the UI file
        uic.loadUi('pic1.ui', self)

        # create a timer to update the progress bar value
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(50)  # update the progress bar every 50ms

        self.show()

    def update_progress_bar(self):
        value = self.progressBar.value() + 1
        self.progressBar.setValue(value)

        # stop the timer when the progress bar reaches 100%
        if value >= 100:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
