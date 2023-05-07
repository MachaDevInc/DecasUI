import sys
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi
import time
from PyQt5.QtCore import QTimer, QTime, QDate
from Ready import Ui_MainWindow2
from inset import Ui_MainWindow7
from wifiset import Ui_wifisetting
from usbset import Ui_usbsetting
from RSset import Ui_RS485
import subprocess
from w3 import Ui_MainWindow3
from W4 import Ui_MainWindow4
proc1 = subprocess.Popen(["python", "progress bar.py"])
time.sleep(1)
proc1.terminate()
class VirtualKeyboard(tk.Tk):


    def __init__(self, on_enter_callback):
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

            self.on_enter_callback = on_enter_callback

    def create_keyboard(self):
            for row_index, row in enumerate(self.keys, start=1):
                for col_index, key in enumerate(row):
                    button = tk.Button(self, text=key, width=5, height=2, command=lambda k=key: self.press_key(k))
                    button.grid(row=row_index, column=col_index, padx=2, pady=2)

    def press_key(self, key):
            if key == 'Backspace':
                self.input_var.set(self.input_var.get()[:-1])
            elif key == 'Enter':
                entered_text = self.input_var.get()
                print(f"Input: {entered_text}")
                self.input_var.set('')
                self.destroy()
                self.on_enter_callback(entered_text)
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
    pass
from PyQt5.QtCore import QObject, pyqtSignal

class SharedData(QObject):
    date_updated = pyqtSignal(str)
    time_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._date = None
        self._time = None

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.date_updated.emit(value)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.time_updated.emit(value)
    def set_system_time(self, date, time):
        self.date = date.toString()
        self.time = time.toString()

    def update_time(self):
        current_time = QTime.fromString(self.time)
        current_time = current_time.addSecs(1)
        self.time = current_time.toString()
def update_shared_data_time():
    shared_data.update_time()
shared_data = SharedData()

class SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Ready.ui', self)

        self.setting.clicked.connect(self.open_next)
        self.connection.clicked.connect(self.open_connection)
        self.next.clicked.connect(self.next_settings)

        self.work.clicked.connect(self.open_work)

    def open_next(self):
        self.usb_window = USBWindow()
        self.usb_window.show()
        self.hide()
    def next_settings(self):
        self.settings_window = SettingsWindow1(self)
        self.settings_window.show()
        self.hide()
    def open_connection(self):
        self.connection_window = connectionWindow()
        self.connection_window.show()
        self.hide()
    def open_work(self):
        self.work_window = workWindow()
        self.work_window.show()
        self.hide()
class connectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('connection.ui', self)

        self.back.clicked.connect(self.go_back)
    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()
class workWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Work.ui', self)

        self.back.clicked.connect(self.go_back)
    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()
class USBWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('inset.ui', self)
        self.wifi_window = WifiWindow()
        self.back.clicked.connect(self.go_back)
        self.usb.clicked.connect(self.open_usb)
        self.bluetooth.clicked.connect(self.open_bluetooth)
        self.wifi.clicked.connect(self.open_wifi)
        self.about.clicked.connect(self.open_about)
        self.rs.clicked.connect(self.open_rs)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.timeEdit.setTime(QTime.fromString(current_time))
        self.dateEdit.setDate(QDate.fromString(shared_data.date, "yyyy-MM-dd"))

    def open_wifi(self):
        # Show the existing wifi_window instance
        self.wifi_window.show()
        self.hide()
    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()

    def open_wifi(self):
        self.usb_window = WifiWindow()
        self.usb_window.show()
        self.hide()

    def open_about(self):
        self.about_window = aboutWindow()
        self.about_window.show()
        self.hide()
    def open_rs(self):
        self.usb_window = RSWindow()
        self.usb_window.show()
        self.hide()

    def open_usb(self):
        self.usb_window = usbWindow()
        self.usb_window.show()
        self.hide()
    def open_bluetooth(self):
        self.usb_window = bluetoothWindow()
        self.usb_window.show()
        self.hide()


    def update_system_time(self):
        current_time = QTime.currentTime().toString()
        shared_data.time = current_time
class aboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('About.ui', self)

        self.back.clicked.connect(self.go_back)


    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()
class WifiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('wifiset.ui', self)

        self.back.clicked.connect(self.go_back)
        self.connection.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit))

        self.password.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit1))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()

    def update_text_edit(self, text_edit, entered_text):
        text_edit.setPlainText(entered_text)

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(lambda entered_text: self.update_text_edit(text_edit, entered_text))
        virtual_keyboard.mainloop()
class RSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('RSset.ui', self)

        self.back.clicked.connect(self.go_back)
        self.address.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit))
        self.parity.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit2))
        self.baudrate.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit1))

    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()

    def update_text_edit(self, text_edit, entered_text):
        text_edit.setPlainText(entered_text)

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(lambda entered_text: self.update_text_edit(text_edit, entered_text))
        virtual_keyboard.mainloop()
class usbWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('usbset.ui', self)

        self.back.clicked.connect(self.go_back)
        self.COM.clicked.connect(self.open_virtual_keyboard)


    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()

    def update_text_edit(self, entered_text):
        self.textEdit.setPlainText(entered_text)

    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard(self.update_text_edit)
        virtual_keyboard.mainloop()
class bluetoothWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('bluetooth.ui', self)

        self.back.clicked.connect(self.go_back)
        self.bluetooth1.clicked.connect(self.open_virtual_keyboard)


    def go_back(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.hide()


    def update_text_edit(self, entered_text):
        self.textEdit.setPlainText(entered_text)

    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard(self.update_text_edit)
        virtual_keyboard.mainloop()
# Define similar classes for WifiWindow, RsWindow, and SetWindow
class SettingsWindow1(QMainWindow, Ui_MainWindow3):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.next1.clicked.connect(self.open_keyboard)

        self.Retreive.clicked.connect(self.next_settings5)
    def open_keyboard(self):
        self.settings_window = NumericKeyboard(self)
        self.settings_window.show()
    def next_settings5(self):
        proc2 = subprocess.Popen(["python", "s5.py"])
        time.sleep(10)
        proc2.terminate()
        proc2 = subprocess.Popen(["python", "s6.py"])
        time.sleep(10)
        proc2.terminate()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingWindow()
    window.show()
    timer = QTimer()
    timer.timeout.connect(update_shared_data_time)
    timer.start(1000)
    sys.exit(app.exec_())
