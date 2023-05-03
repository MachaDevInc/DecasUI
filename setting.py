import sys
import subprocess
import time
import tkinter as tk
from PyQt5.uic import loadUi
from functools import partial
proc1 = subprocess.Popen(["python", "progress bar.py"])
time.sleep(5)
proc1.terminate()
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate
from Ready import Ui_MainWindow2
from inset import Ui_MainWindow7
from wifiset import Ui_wifisetting
from usbset import Ui_usbsetting
from RSset import Ui_RS485
from w3 import Ui_MainWindow3
from newkey import NumericKeyboard
from w5 import Ui_MainWindow5
from w6 import Ui_MainWindow6
from W4 import Ui_MainWindow4
from genkey import VirtualKeyboard

class MainWindow(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setting.clicked.connect(self.open_settings)
        self.next.clicked.connect(self.next_settings)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime()
        self.timeEdit.setTime(current_time)

        if current_time.toString() == "00:00:00":
            current_date = QDate.currentDate()
        self.dateEdit.setDate(current_date)
    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        self.hide()
    def next_settings(self):
        self.settings_window = SettingsWindow1(self)
        self.settings_window.show()
        self.hide()



class SettingsWindow(QMainWindow, Ui_MainWindow7):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        self.usb.clicked.connect(self.open_usb_settings)
        self.wifi.clicked.connect(self.open_wifi_settings)
        self.rs.clicked.connect(self.open_rs_settings)
        self.back.clicked.connect(self.close_and_show_parent)

    def open_usb_settings(self):
        print("Opening USB Settings")
        self.sub_settings_window1 = SubSettingsWindow(self, Ui_MainWindow10)
        self.sub_settings_window1.show()
        self.hide()
    def open_wifi_settings(self):
        print("Opening WiFi Settings")
        self.sub_settings_window = SubSettingsWindow(self, Ui_MainWindow8)
        self.sub_settings_window.show()
        self.hide()

    def open_rs_settings(self):
        print("Opening RS Settings")
        self.sub_settings_window = SubSettingsWindow(self, Ui_MainWindow9)
        self.sub_settings_window.show()
        self.hide()

    def close_and_show_parent(self):
        self.parent.show()
        self.close()

class SubSettingsWindow(QMainWindow):
    def __init__(self, parent, settings_ui_class):
        super().__init__()
        self.parent = parent
        self.ui = settings_ui_class()
        self.ui.setupUi(self)
        print("SubSettingsWindow created")
        self.ui.back.clicked.connect(self.close_and_show_parent)


    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard()
        virtual_keyboard.mainloop()

    def close_and_show_parent(self):
        self.parent.show()
        self.close()
    def closeEvent(self, event):
        self.parent.show()
        event.accept()
class SubSettingsWindow1(QMainWindow):
    def __init__(self, parent, settings_ui_class):
        super().__init__()
        self.parent = parent
        self.ui = settings_ui_class()
        self.ui.setupUi(self)
        print("SubSettingsWindow created")
        self.ui.back.clicked.connect(self.close_and_show_parent)



    def close_and_show_parent(self):
        self.parent.show()
        self.close()
    def closeEvent(self, event):
        self.parent.show()
        event.accept()
class SubSettingsWindow2(QMainWindow):
    def __init__(self, parent, settings_ui_class):
            super().__init__()
            self.parent = parent
            self.ui = settings_ui_class()
            self.ui.setupUi(self)
            print("SubSettingsWindow created")
            self.ui.back.clicked.connect(self.close_and_show_parent)
            self.ui.COM.clicked.connect(self.open_virtual_keyboard)
    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard()
        virtual_keyboard.mainloop()
    def close_and_show_parent(self):
        self.parent.show()
        self.close()
    def closeEvent(self, event):
        self.parent.show()
        event.accept()
class SubSettingsWindow2(QMainWindow):
    def __init__(self, parent, settings_ui_class):
            super().__init__()
            self.parent = parent
            self.ui = settings_ui_class()
            self.ui.setupUi(self)
            print("SubSettingsWindow created")
            self.ui.COM.clicked.connect(self.open_virtual_keyboard1)


    def open_virtual_keyboard1(self):
        virtual_keyboard = VirtualKeyboard()
        virtual_keyboard.mainloop()

    def open_virtual_keyboard2(self):
            virtual_keyboard = VirtualKeyboard()
            virtual_keyboard.mainloop()

    def open_virtual_keyboard3(self):
                virtual_keyboard = VirtualKeyboard()
                virtual_keyboard.mainloop()

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
                '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(',
                '0': ')',
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
class SettingsWindow7(QMainWindow, VirtualKeyboard):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
class SubSettingsWindow4(QMainWindow):
    def __init__(self):
        super(SubSettingsWindow4, self).__init__()
        self.initUI()


class SettingsWindow1(QMainWindow, Ui_MainWindow3):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.next1.clicked.connect(self.open_keyboard)

    def open_keyboard(self):
        self.settings_window = NumericKeyboard(self)
        self.settings_window.show()

class NumericKeyboard(QMainWindow, Ui_MainWindow4):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        super(NumericKeyboard, self).__init__()
        self.setupUi(self)
        self.saved_value = ""
        # Connect buttons to their respective functions
        self.b0.clicked.connect(lambda: self.add_number('0'))
        self.b1.clicked.connect(lambda: self.add_number('1'))
        self.b2.clicked.connect(lambda: self.add_number('2'))
        self.b3.clicked.connect(lambda: self.add_number('3'))
        self.b4.clicked.connect(lambda: self.add_number('4'))
        self.b5.clicked.connect(lambda: self.add_number('5'))
        self.b6.clicked.connect(lambda: self.add_number('6'))
        self.b7.clicked.connect(lambda: self.add_number('7'))
        self.b8.clicked.connect(lambda: self.add_number('8'))
        self.b9.clicked.connect(lambda: self.add_number('9'))

        self.Del.clicked.connect(self.delete_number)
        self.enter.clicked.connect(self.enter_pressed)

        self.Retry.clicked.connect(self.retry)
    def add_number(self, number):
        current_text = self.textEdit.toPlainText()
        new_text = current_text + number
        self.textEdit.setPlainText(new_text)

    def delete_number(self):
        current_text = self.textEdit.toPlainText()
        new_text = current_text[:-1]
        self.textEdit.setPlainText(new_text)

    def enter_pressed(self):
        self.saved_value = self.textEdit.toPlainText()
        print(f"Saved value: {self.saved_value}")
        self.close()

    def get_saved_value(self):
            return self.saved_value
    def retry(self):
        self.textEdit.clear()

    def next_settings5(self):
        proc2 = subprocess.Popen(["python", "s5.py"])
        time.sleep(10)
        proc2.terminate()
        proc2 = subprocess.Popen(["python", "s6.py"])
        time.sleep(10)
        proc2.terminate()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())