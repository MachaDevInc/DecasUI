from PyQt5.QtCore import QObject, pyqtSignal
import sys
import os
import subprocess
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget
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

import board
import busio
import serial
from adafruit_pn532.i2c import PN532_I2C

proc1 = subprocess.Popen(["python", "progress bar.py"])
time.sleep(1)
proc1.terminate()


class VirtualKeyboard(tk.Tk):

    def __init__(self, on_enter_callback):
        super().__init__()

        self.title("Virtual Keyboard")
        self.configure(bg='black')

        self.input_var = tk.StringVar()
        self.input_label = tk.Entry(
            self, textvariable=self.input_var, width=80)
        self.input_label.grid(row=0, column=0, columnspan=15)

        self.keys = [
            ['`', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y',
                'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h',
                'j', 'k', 'l', ';', '\'', 'Enter'],
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
                button = tk.Button(
                    self, text=key, width=5, height=2, command=lambda k=key: self.press_key(k))
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


class SharedData(QObject):

    def __init__(self):
        super().__init__()
        self._date = None
        self._time = None
        self._date = QDate.currentDate().toString("yyyy-MM-dd")
        self._time = QTime.currentTime().toString()

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
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('Ready.ui', self)

        self.stacked_widget = stacked_widget
        self.setting.clicked.connect(self.open_next)
        self.connection.clicked.connect(self.open_connection)
        self.work.clicked.connect(self.open_work)

    def open_next(self):
        self.usb_window = USBWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def open_connection(self):
        self.connection_window = connectionWindow(self.stacked_widget)
        self.connection_window.showFullScreen()
        self.hide()

    def open_work(self):
        self.work_window = workWindow(self.stacked_widget)
        self.work_window.showFullScreen()
        self.hide()


class connectionWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('connection.ui', self)

        self.back.clicked.connect(self.go_back)

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()


class workWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('Work.ui', self)

        self.back.clicked.connect(self.go_back)

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()


class USBWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('inset.ui', self)

        self.stacked_widget = stacked_widget
        self.wifi_window = WifiWindow(self.stacked_widget)
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

    # def open_wifi(self):
    #     # Show the existing wifi_window instance
    #     self.wifi_window.showFullScreen()
    #     self.hide()

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()

    def open_wifi(self):
        # Pass 'self.stacked_widget' as an argument when creating a new WifiWindow instance
        self.usb_window = WifiWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def open_about(self):
        self.about_window = aboutWindow()
        self.about_window.showFullScreen()
        self.hide()

    def open_rs(self):
        self.rs_window = RSWindow(self.stacked_widget)
        self.rs_window.showFullScreen()
        self.hide()

    def open_usb(self):
        self.usb_window = usbWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def open_bluetooth(self):
        self.usb_window = bluetoothWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()


class aboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('About.ui', self)

        self.back.clicked.connect(self.go_back)

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()


class WifiWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('wifiset.ui', self)

        self.stacked_widget = stacked_widget

        self.back.clicked.connect(self.go_back)

        self.password.clicked.connect(
            lambda: self.open_virtual_keyboard(self.textEdit1))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)
        interface = "wlan0"  # The default interface for Raspberry Pi's WiFi
        cmd = f"iwlist {interface} scan"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        lines = output.split("\n")
        networks = []

        for line in lines:
            line = line.strip()
            if "ESSID" in line:
                networks.append(line.split(":")[1].strip('"'))

        for network in networks:
            self.ssid.addItems({network})

        # Connect the combo box's activated signal to a slot function
        self.ssid.activated[str].connect(self.on_combobox_activated)

    def on_combobox_activated(self, text):
        print(f"Selected option: {text}")

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def go_back(self):
        self.usb_window = USBWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, text_edit, entered_text):
        text_edit.setPlainText(entered_text)

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(
            lambda entered_text: self.update_text_edit(text_edit, entered_text))
        virtual_keyboard.mainloop()


class RSWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('RSset.ui', self)

        self.back.clicked.connect(self.go_back)
        self.address.clicked.connect(
            lambda: self.open_virtual_keyboard(self.textEdit))
        self.baudrate.addItems(["9600", "19200", "38400", "115200"])
        self.parity.addItems(["None", "Even", "Odd"])
        # Connect the combo box's activated signal to a slot function
        self.baudrate.activated[str].connect(self.on_combobox_activated)

        self.parity.activated[str].connect(self.on_combobox_activated1)

    def on_combobox_activated(self, text):
        print(f"Selected option: {text}")

    def on_combobox_activated1(self, text):
        print(f"Selected option: {text}")

    def go_back(self):
        self.usb_window = USBWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, text_edit, entered_text):
        text_edit.setPlainText(entered_text)

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(
            lambda entered_text: self.update_text_edit(text_edit, entered_text))
        virtual_keyboard.mainloop()


class usbWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('usbset.ui', self)

        self.back.clicked.connect(self.go_back)
        self.comport.addItems(["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"])

        # Connect the combo box's activated signal to a slot function
        self.comport.activated[str].connect(self.on_combobox_activated)

    def on_combobox_activated(self, text):
        print(f"Selected option: {text}")

    def go_back(self):
        self.usb_window = USBWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, entered_text):
        self.textEdit.setPlainText(entered_text)

    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard(self.update_text_edit)
        virtual_keyboard.mainloop()


class bluetoothWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('bluetooth.ui', self)

        self.back.clicked.connect(self.go_back)
        self.bluetooth1.addItems(["Device1", "Device2 ", "Device3"])

        # Connect the combo box's activated signal to a slot function
        self.bluetooth1.activated[str].connect(self.on_combobox_activated)

    def on_combobox_activated(self, text):
        print(f"Selected option: {text}")

    def go_back(self):
        self.usb_window = USBWindow(self.stacked_widget)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, entered_text):
        self.textEdit.setPlainText(entered_text)

    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard(self.update_text_edit)
        virtual_keyboard.mainloop()


# Define similar classes for WifiWindow, RsWindow, and SetWindow
class SettingsWindow1(QMainWindow, Ui_MainWindow3):
    def __init__(self, stacked_widget, file_path):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        self.file_path = file_path
        self.next1.clicked.connect(self.open_keyboard)
        self.Retreive.clicked.connect(self.next_settings5)
        self.process()

    def process(self):
        print(self.file_path)
        # Barcode
        # Configure the serial port and baud rate
        serial_port = "/dev/ttySC0"
        baud_rate = 9600

        # Command to be sent
        start_scan_command = "7E 00 08 01 00 02 01 AB CD"
        start_scan_command_bytes = bytes.fromhex(start_scan_command.replace(" ", ""))
        start_stop_command = "7E 00 08 01 00 02 00 AB CD"
        start_stop_command_bytes = bytes.fromhex(start_stop_command.replace(" ", ""))

        # PN532
        # Configure the PN532 connection
        i2c = busio.I2C(board.SCL, board.SDA)
        pn532 = PN532_I2C(i2c, debug=False)
        ic, ver, rev, support = pn532.firmware_version
        print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

        # Configure PN532 to communicate with RFID cards
        pn532.SAM_configuration()

        scanned = False
        scanned_data = ""
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Connected to {serial_port} at {baud_rate} baud rate.")

            # Send the start scan command
            ser.write(start_scan_command_bytes)

            while scanned is not True:
                # Read data from the serial port
                data_bytes = ser.readline()
                data = data_bytes[-2:].decode("utf-8").strip()

                # If data is received, print it and exit the loop
                while data != "31":
                    # Read data from the serial port
                    data = ser.readline().decode("utf-8").strip()
                    # If data is received, print it
                    if data:
                        print(f"Received data: {data}")
                        scanned_data = data
                        scanned = True
                        # Send the stop scan command
                        ser.write(start_stop_command_bytes)
                        break
                        
                    print("Scanning RFID and Barcode...")
                    uid = pn532.read_passive_target(timeout=0.5)
                    if uid is not None:
                        uid_string = ''.join([hex(i)[2:].zfill(2) for i in uid])  # Convert UID to a string
                        print("Found an RFID card with UID:", uid_string)
                        scanned_data = uid_string
                        scanned = True
                        # Send the stop scan command
                        ser.write(start_stop_command_bytes)
                        break
                        
                    # Wait for a short period before reading the next data
                    time.sleep(0.1)

    def open_keyboard(self):
        self.settings_window = NumericKeyboard(self)
        self.settings_window.showFullScreen()

    def next_settings5(self):
        proc2 = subprocess.Popen(["python", "s5.py"])
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

        self.cross.clicked.connect(self.destroy)

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
        proc2 = subprocess.Popen(["python", "s6.py"])
        time.sleep(10)
        proc2.terminate()

    def get_saved_value(self):
        return self.saved_value

    def destroy(self):
        self.hide()


class DirectoryChecker(QObject):
    open_settings_window1_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.path_data = ""  # Initialize path_data with an empty string

    def check_directory(self):
        directory_path = '/var/spool/cups-pdf/ANONYMOUS/'
        # directory_path = 'D:/DecasUI/DecasUI/ANONYMOUS/'

        contents = os.listdir(directory_path)

        if contents:
            for content in contents:
                file_path = os.path.join(directory_path, content)
                if os.path.isfile(file_path):
                    print(file_path)
            self.path_data = file_path  # Update path_data with the last file_path
            self.open_settings_window1_signal.emit()


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.stacked_widget = QStackedWidget()

        self.setting_window = SettingWindow(self.stacked_widget)
        self.stacked_widget.addWidget(self.setting_window)
        self.stacked_widget.showFullScreen()

        self.directory_checker = DirectoryChecker()
        self.directory_checker.open_settings_window1_signal.connect(
            self.open_settings_window1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.directory_checker.check_directory)
        self.timer.start(500)

    def open_settings_window1(self):
        file_path = self.directory_checker.path_data
        self.SettingsWindow1_window = SettingsWindow1(
            self.stacked_widget, file_path)
        self.stacked_widget.addWidget(self.SettingsWindow1_window)
        self.stacked_widget.setCurrentWidget(self.SettingsWindow1_window)
        self.stacked_widget.removeWidget(self.setting_window)
        self.timer.stop()


if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.exec_())
