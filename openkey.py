import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Keyboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent)
        self.text_bar = None
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        buttons = [
            "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
            "A", "S", "D", "F", "G", "H", "J", "K", "L", "",
            "Z", "X", "C", "V", "B", "N", "M", "", "", ""
        ]
        positions = [(i, j) for i in range(3) for j in range(10)]
        for position, button in zip(positions, buttons):
            if button:
                btn = QtWidgets.QPushButton(button)
                btn.setMinimumSize(30, 30)
                grid.addWidget(btn, *position)
                btn.clicked.connect(self.buttonClicked)
            else:
                sp = QtWidgets.QSpacerItem(30, 30)
                grid.addItem(sp, *position)

        self.setWindowTitle("Keyboard")
        self.resize(300, 150)

    def setTextBar(self, text_bar):
        self.text_bar = text_bar

    def buttonClicked(self):
        button = self.sender()
        if self.text_bar:
            self.text_bar.insert(button.text())

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.text_bar = QtWidgets.QLineEdit()
        self.keyboard = Keyboard()
        self.keyboard.setTextBar(self.text_bar)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.text_bar)
        self.statusBar()

        open_keyboard = QtWidgets.QAction(QtGui.QIcon("keyboard.png"), "Open Keyboard", self)
        open_keyboard.setShortcut("Ctrl+K")
        open_keyboard.setStatusTip("Open Keyboard")
        open_keyboard.triggered.connect(self.openKeyboard)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(open_keyboard)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Text Bar")
        self.show()

    def openKeyboard(self):
        self.keyboard.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            text = self.text_bar.text()
            print(f"Saving data: {text}")
            self.text_bar.clear()
            self.keyboard.hide()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
