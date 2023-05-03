import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateTimeEdit

class DateTimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ready.ui', self)

        # Get the QDateTimeEdit widgets for date and time
        self.date_edit = self.findChild(QDateTimeEdit, 'dateEdit')
        self.time_edit = self.findChild(QDateTimeEdit, 'timeEdit')

        # Set signals and slots
        self.date_edit.dateTimeChanged.connect(self.update_date_time)
        self.time_edit.timeChanged.connect(self.update_date_time)

        # Initialize QTimer to update the time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_date_time(self):
        current_date_time = self.date_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        print("Updated Date and Time:", current_date_time)

    def update_time(self):
        # Get the current time and increment it by 1 second
        new_time = self.time_edit.dateTime().addSecs(1)
        self.time_edit.setDateTime(new_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DateTimeApp()
    window.show()
    sys.exit(app.exec_())
