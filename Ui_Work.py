from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenuBar, QStatusBar, QPushButton, QApplication, QMainWindow, QScrollArea, QTextEdit
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication
from PyQt5 import QtGui


class CustomWidget(QWidget):
    def __init__(self, text, data, central_widget, button_needed=False, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.central_widget = central_widget
        # Set CustomWidget background to be transparent
        # white background with alpha = 100
        self.setStyleSheet("background-color: rgba(255, 255, 255, 100);")

        # set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # create text edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(data)  # Set the dynamic data here
        self.layout.addWidget(self.text_edit)

        # create button if button_needed is True
        if button_needed:
            self.button = QPushButton(self.central_widget)
            # self.button.setStyleSheet("background-color:transparent;")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("pics/retry.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button.setIcon(icon)
            self.button.setIconSize(QSize(150, 60))  # Set the size of the icon
            self.button.setFixedSize(QSize(150, 60))  # Set the fixed size of the button to match the icon size
            self.button.setFlat(True)

            # Create a QHBoxLayout for the button
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)
            button_layout.addWidget(self.button)
            button_layout.addStretch(1)

            # Add the button layout to the main layout
            self.layout.addLayout(button_layout)


class JobsMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(JobsMainWindow, self).__init__(parent)
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(pics/Standby.png);
                background-repeat: no-repeat
            }
        """)

        # Set the window size
        self.resize(1024, 600)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(
            "pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(412, 0, 250, 100))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        # Create a central widget
        self.central_widget = QWidget(self.centralwidget)
        self.central_widget.setGeometry(QRect(40, 90, 951, 410))

        # Create a QVBoxLayout
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QScrollArea
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.scroll_area)

        # Create a widget for the scroll area content
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        # Create a QVBoxLayout for the scroll area content
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Add custom widgets to the scroll area content layout
        for i in range(10):
            data = f""  # Replace this with your actual data
            if i == 5:
                widget = CustomWidget(f"", data, self.central_widget, False)
            else:
                widget = CustomWidget(f"", data, self.central_widget, True)
            self.scroll_layout.addWidget(widget)

        self.back = QPushButton(self.centralwidget)
        self.back.setGeometry(QRect(50, 480, 75, 75))
        self.back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "pics/1 (400 × 400 px).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setIconSize(QSize(75, 75))
        self.back.setFlat(True)
        self.back.setObjectName("back")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("JobsMainWindow", "JobsMainWindow"))
        self.label_2.setText(_translate(
            "JobsMainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">RECENT JOBS</span></p></body></html>"))
