import sys
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from Ready import Ui_MainWindow2
from inset import Ui_MainWindow7
from wifiset import Ui_MainWindow8
from usbset import Ui_MainWindow10
from RSset import Ui_MainWindow9


# VirtualKeyboard class implementation goes here

class ReadyScreen(QMainWindow, Ui_MainWindow2):
    def __init__(self, *args, **kwargs):
        super(ReadyScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setting.clicked.connect(self.open_inset_screen)
        self.virtual_keyboard_button.clicked.connect(self.open_virtual_keyboard)  # Add this line

    def open_inset_screen(self):
        self.parent().stacked_widget.setCurrentIndex(1)

    def open_virtual_keyboard(self):
        self.parent().open_virtual_keyboard()



class InsetScreen(QMainWindow, Ui_MainWindow7):
    def __init__(self, *args, **kwargs):
        super(InsetScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.back.clicked.connect(self.go_to_previous_screen)
        # Add other button connections here
        self.rs.clicked.connect(self.open_rs_set_screen)
        self.usb.clicked.connect(self.open_usb_set_screen)
        self.wifi.clicked.connect(self.open_wifi_set_screen)

    def open_wifi_set_screen(self):
        self.parent().stacked_widget.setCurrentIndex(2)

    def open_usb_set_screen(self):
        self.parent().stacked_widget.setCurrentIndex(4)

    def open_rs_set_screen(self):
        self.parent().stacked_widget.setCurrentIndex(3)
    def go_to_previous_screen(self):
        self.parent().stacked_widget.setCurrentIndex(0)
class WifiSetScreen(QMainWindow, Ui_MainWindow8):
    def __init__(self, *args, **kwargs):
        super(WifiSetScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.back.clicked.connect(self.go_to_previous_screen)
        # Add other button connections here

    def go_to_previous_screen(self):
        self.parent().stacked_widget.setCurrentIndex(0)
class USBSetScreen(QMainWindow, Ui_MainWindow10):
    def __init__(self, *args, **kwargs):
        super(USBSetScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.back.clicked.connect(self.go_to_previous_screen)
        # Add other button connections here


    def go_to_previous_screen(self):
        self.parent().stacked_widget.setCurrentIndex(0)
class RSSetScreen(QMainWindow, Ui_MainWindow9):
    def __init__(self, *args, **kwargs):
        super(RSSetScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.back.clicked.connect(self.go_to_previous_screen)
        # Add other button connections here

    def go_to_previous_screen(self):
        self.parent().stacked_widget.setCurrentIndex(0)


# Similarly, create separate classes for WifiSetScreen, USBSetScreen, and RSSetScreen

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.stacked_widget = QStackedWidget()
        self.ready_screen = ReadyScreen()
        self.inset_screen = InsetScreen()
        self.wifi_set_screen = WifiSetScreen()
        self.usb_set_screen = USBSetScreen()
        self.RS_set_screen=RSSetScreen()
        # Add instances of other screens here

        self.stacked_widget.addWidget(self.ready_screen)
        self.stacked_widget.addWidget(self.inset_screen)
        self.stacked_widget.addWidget(self.wifi_set_screen)
        self.stacked_widget.addWidget(self.usb_set_screen)
        self.stacked_widget.addWidget(self.RS_set_screen)
        # Add the other screens to the stacked widget here
        self.open_virtual_keyboard()
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.setCurrentIndex(0)

    def open_virtual_keyboard(self):
        # Implement the virtual keyboard opening logic here
        virtual_keyboard = VirtualKeyboard()
        virtual_keyboard.mainloop()
        pass

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Virtual Keyboard")
        self.configure(bg='black')

        self.input_var = tk.StringVar()
        self.input_label = tk.Entry(self, textvariable=self.input_var, width=80)
        self.input_label.grid(row=0, column=0, columnspan=15)

        self.keys = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', ' ', 'Alt', 'Ctrl']
        ]

        self.shift_mappings = {
            '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?'
        }

        self.caps_lock_on = False
        self.shift_on = False
        self.create_keyboard()

    def create_keyboard(self):
        for row_index, row in enumerate(self.keys, start=1):
            for col_index, key in enumerate(row):
                button = tk.Button(self, text=key, width=5, height=2, command=lambda k=key: self.press_key(k))
                button.grid(row=row_index, column=col_index, padx=2, pady=2)

    def press_key(self, key):
        if key == 'Backspace':
            self.input_var.set(self.input_var.get()[:-1])
        elif key == 'Enter':
            print(f"Input: {self.input_var.get()}")
            self.input_var.set('')
            self.destroy()
        elif key == 'Caps Lock':
            self.caps_lock_on = not self.caps_lock_on
        elif key == 'Shift':
            self.shift_on = not self.shift_on
            return
        elif key not in ('Ctrl', 'Alt', 'Tab'):
            if self.shift_on:
                key = self.shift_mappings.get(key, key.upper())
                self.shift_on = False

            char = key.upper() if self.caps_lock_on and key.isalpha() else key
            self.input_var.set(self.input_var.get() + char)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
