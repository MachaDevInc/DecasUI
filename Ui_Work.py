from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenuBar,
    QStatusBar,
    QPushButton,
    QMainWindow,
    QScrollArea,
    QTextEdit,
    QTextBrowser,
    QFrame,
)
from PyQt5.QtCore import QSize, QRect, QCoreApplication, Qt
from PyQt5 import QtGui


class CustomWidget(QWidget):
    def __init__(
        self,
        job_id,
        data,
        central_widget,
        button_needed=False,
        work_window=None,
        parent=None,
    ):
        super(CustomWidget, self).__init__(parent)
        self.central_widget = central_widget
        # Set CustomWidget background to be transparent
        # white background with alpha = 100
        self.job_id = job_id
        self.setStyleSheet("background-color: rgba(255, 255, 255, 100);")

        self.work_window = work_window  # Store a reference to the workWindow

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
        self.label.setFixedWidth(810)
        self.layout.addWidget(self.label)
        self.label.setFont(font)

        # create button if button_needed is True
        if button_needed:
            self.button = QPushButton()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("pics/retry.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.button.setIcon(icon)
            self.button.setIconSize(QSize(80, 40))  # Set the size of the icon
            # Set the fixed size of the button to match the icon size
            self.button.setFixedSize(QSize(80, 40))
            self.button.setFlat(True)
            if self.work_window is not None:
                self.button.clicked.connect(
                    lambda: self.work_window.on_button_clicked(self.job_id)
                )

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
        self.setStyleSheet(
            """
            QMainWindow {
                background-image: url(pics/Standby.png);
                background-repeat: no-repeat
            }
        """
        )

        # Set the window size
        self.resize(1024, 600)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(20, 0, 250, 100))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        # Create a central widget
        self.central_widget = QWidget(self.centralwidget)
        self.central_widget.setGeometry(QRect(30, 70, 994, 400))

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
        icon.addPixmap(
            QtGui.QPixmap("pics/1 (400 × 400 px).png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.back.setIcon(icon)
        self.back.setIconSize(QSize(75, 75))
        self.back.setFlat(True)
        self.back.setObjectName("back")
        self.search_text = QTextEdit(self.centralwidget)
        self.search_text.setGeometry(QRect(570, 40, 271, 45))
        self.search_text.setObjectName("search_text")
        self.textBrowser_2 = QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QRect(850, 40, 140, 45))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser_2.setPalette(palette)
        self.textBrowser_2.setFrameShape(QFrame.Box)
        self.textBrowser_2.setFrameShadow(QFrame.Raised)
        self.textBrowser_2.setLineWidth(4)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.search = QPushButton(self.centralwidget)
        self.search.setGeometry(QRect(850, 40, 140, 45))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.search.setPalette(palette)
        self.search.setLayoutDirection(Qt.LeftToRight)
        self.search.setAutoFillBackground(False)
        self.search.setStyleSheet('font: 75 24pt "MS Shell Dlg 2";')
        self.search.setText("")
        self.search.setIconSize(QSize(100, 100))
        self.search.setAutoDefault(False)
        self.search.setDefault(False)
        self.search.setFlat(True)
        self.search.setObjectName("search")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("JobsMainWindow", "JobsMainWindow"))
        self.label_2.setText(
            _translate(
                "JobsMainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">RECENT JOBS</span></p></body></html>',
            )
        )
        self.search_text.setHtml(
            _translate(
                "JobsMainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.textBrowser_2.setHtml(
            _translate(
                "JobsMainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:22pt; font-weight:600;">Search</span></p></body></html>',
            )
        )
