from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenuBar, QStatusBar, QPushButton, QMainWindow, QScrollArea
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication, Qt
from PyQt5 import QtGui


class CustomWidget(QWidget):
    def __init__(self, text, data, central_widget, button_needed=False, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.central_widget = central_widget
        # Set CustomWidget background to be transparent
        # white background with alpha = 100
        self.setStyleSheet("background-color: rgba(255, 255, 255, 100);")

        # set layout
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)

        # create text edit
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(60)
        self.label = QLabel()
        self.label.setText(data)  # Set the dynamic data here
        self.label.setFixedWidth(730)
        self.layout.addWidget(self.label)
        self.label.setFont(font)
        self.label.setText("Bilal\n\nAwan\n\nBilal\n\nAwan")

        # create button if button_needed is True
        if button_needed:
            self.button = QPushButton()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("pics/retry.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button.setIcon(icon)
            self.button.setIconSize(QSize(100, 50))  # Set the size of the icon
            # Set the fixed size of the button to match the icon size
            self.button.setFixedSize(QSize(100, 50))
            self.button.setFlat(True)

            # Create a QHBoxLayout for the button
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)
            button_layout.setAlignment(Qt.AlignBottom)
            button_layout.addWidget(self.button)

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
        self.central_widget.setGeometry(QRect(30, 70, 964, 400))

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
