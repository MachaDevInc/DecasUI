# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReadymxKFCh.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QWidget)

class Ui_MainWindow2(object):
    def setupUi(self, MainWindow2):
        if not MainWindow2.objectName():
            MainWindow2.setObjectName(u"MainWindow2")
        MainWindow2.resize(1024, 600)
        self.centralwidget = QWidget(MainWindow2)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setPixmap(QPixmap(u"pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(370, 340, 261, 50))
        font = QFont()
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.setting = QPushButton(self.centralwidget)
        self.setting.setObjectName(u"setting")
        self.setting.setGeometry(QRect(170, 440, 100, 100))
        icon = QIcon()
        icon.addFile(u"pics/1 (90 \u00d7 90 px) (1).png", QSize(), QIcon.Normal, QIcon.Off)
        self.setting.setIcon(icon)
        self.setting.setIconSize(QSize(100, 100))
        self.setting.setFlat(True)
        self.work = QPushButton(self.centralwidget)
        self.work.setObjectName(u"work")
        self.work.setGeometry(QRect(30, 440, 100, 100))
        icon1 = QIcon()
        icon1.addFile(u"pics/1 (90 \u00d7 90 px) (2).png", QSize(), QIcon.Normal, QIcon.Off)
        self.work.setIcon(icon1)
        self.work.setIconSize(QSize(100, 100))
        self.work.setFlat(True)
        self.connection = QPushButton(self.centralwidget)
        self.connection.setObjectName(u"connection")
        self.connection.setGeometry(QRect(750, 440, 100, 100))
        icon2 = QIcon()
        icon2.addFile(u"pics/cokk.png", QSize(), QIcon.Normal, QIcon.Off)
        self.connection.setIcon(icon2)
        self.connection.setIconSize(QSize(100, 100))
        self.connection.setFlat(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(380, 70, 250, 250))
        self.label_3.setPixmap(QPixmap(u"pics/1 (400 \u00d7 400 px) (400 \u00d7 400 px).png"))
        self.label_3.setScaledContents(True)
        self.next = QPushButton(self.centralwidget)
        self.next.setObjectName(u"next")
        self.next.setGeometry(QRect(890, 440, 100, 100))
        icon3 = QIcon()
        icon3.addFile(u"pics/1 (90 \u00d7 90 px) (3).png", QSize(), QIcon.Normal, QIcon.Off)
        self.next.setIcon(icon3)
        self.next.setIconSize(QSize(100, 100))
        self.next.setFlat(True)
        self.dateTextEdit = QTextEdit(self.centralwidget)
        self.dateTextEdit.setObjectName(u"dateTextEdit")
        self.dateTextEdit.setGeometry(QRect(30, 30, 125, 30))
        self.timeTextEdit = QTextEdit(self.centralwidget)
        self.timeTextEdit.setObjectName(u"timeTextEdit")
        self.timeTextEdit.setGeometry(QRect(870, 30, 125, 30))
        MainWindow2.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow2)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        MainWindow2.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow2)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow2.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow2)

        QMetaObject.connectSlotsByName(MainWindow2)
    # setupUi

    def retranslateUi(self, MainWindow2):
        MainWindow2.setWindowTitle(QCoreApplication.translate("MainWindow2", u"MainWindow", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow2", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Device is Ready</span></p></body></html>", None))
        self.setting.setText("")
        self.work.setText("")
        self.connection.setText("")
        self.label_3.setText("")
        self.next.setText("")
    # retranslateUi

