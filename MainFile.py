from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5 import QtCore
import sys
import os
import subprocess
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget
from PyQt5.uic import loadUi
import time
from PyQt5.QtCore import QTimer, QTime, QDate
import subprocess

from Ui_Work import JobsMainWindow
from Ui_Work import CustomWidget

import board
import busio
import serial
from adafruit_pn532.i2c import PN532_I2C
from escpos.printer import Serial

import re
import json
import requests
from datetime import datetime

import sys
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

import uuid
import socket

import bluetooth

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

        # Set the window size
        self.resize(1024, 600)

        self.stacked_widget = stacked_widget
        self.setting.clicked.connect(self.open_next)
        self.connection.clicked.connect(self.open_connection)
        self.work.clicked.connect(self.open_work)

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
        self.timer.stop()
        self.hide()

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

        # Set the window size
        self.resize(1024, 600)
        self.back.clicked.connect(self.go_back)

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()


class workWindow(JobsMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Set the window size
        self.resize(1024, 600)
        
        self.show_jobs()
        self.back.clicked.connect(self.go_back)

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()

    def show_jobs(self):
        jobs = {}
        i = 0

        try:
            # Read the file
            with open('my_jobs.json', 'r') as f:
                jobs = json.load(f)  # This will give you a dictionary
                # Get the size of the dictionary
                size = len(jobs)
                print(f"The dictionary contains {size} key-value pairs.")
        except json.JSONDecodeError:
            print("File is not valid JSON")
        except FileNotFoundError:
            print("File 'my_jobs.json' not found.")

        if jobs:
            for value in jobs.values():
                # Add custom widgets to the scroll area content layout
                for i in range(10):
                    data = f""  # Replace this with your actual data
                    if i == 5:
                        widget = CustomWidget(
                            f"", data, self.central_widget, False)
                    else:
                        widget = CustomWidget(
                            f"", data, self.central_widget, True)
                    self.scroll_layout.addWidget(widget)


class USBWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('inset.ui', self)

        # Set the window size
        self.resize(1024, 600)
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
        self.about_window = aboutWindow(self.stacked_widget)
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
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._translate = QtCore.QCoreApplication.translate
        loadUi('About.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.mac.setText(self._translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">" +
                                         self.get_mac_address() + "</span></p></body></html>"))
        self.ip.setText(self._translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">" +
                                        self.get_local_ip_address('8.8.8.8') + "</span></p></body></html>"))
        self.back.clicked.connect(self.go_back)
        # Google's DNS as target to get the local ip
        print(self.get_local_ip_address('8.8.8.8'))

    def go_back(self):
        self.setting_window = SettingWindow(self.stacked_widget)
        self.setting_window.showFullScreen()
        self.hide()

    def get_mac_address(self):
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    def get_local_ip_address(self, target):
        ip_address = ''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((target, 1))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception as e:
            print("Error: %s" % e)
        return ip_address


class WifiWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('wifiset.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.network_ssid = ""
        self.network_password = ""
        self.stacked_widget = stacked_widget
        self._translate = QtCore.QCoreApplication.translate
        self.confirm.clicked.connect(self.done)
        self.back.clicked.connect(self.go_back)

        self.password.clicked.connect(
            lambda: self.open_virtual_keyboard(self.textEdit1))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

        self.status.setText(self._translate(
            "wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Scanning...Please wait!</span></p></body></html>"))
        self.discovery_thread = WiFiDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(
            self.add_wifi_item)
        self.discovery_thread.start()

        self.network_ssid = self.ssid.itemText(0)

        self.refresh.clicked.connect(self.refresh_wifi_scan)
        # Connect the combo box's activated signal to a slot function
        self.ssid.activated[str].connect(self.on_combobox_activated)

    def refresh_wifi_scan(self):
        self.ssid.clear()
        self.status.setText(self._translate(
            "wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Scanning...Please wait!</span></p></body></html>"))
        self.discovery_thread = WiFiDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(
            self.add_wifi_item)
        self.discovery_thread.start()

    def add_wifi_item(self, name, devices):
        self.status.setText(self._translate(
            "wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">" + devices + " network(s) found</span></p></body></html>"))
        self.ssid.addItem(name)

    def on_combobox_activated(self, text):
        self.network_ssid = text
        print(f"Selected option: {text}")

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def done(self):
        self.network_password = str(self.textEdit1.toPlainText())
        print(self.network_password)

        if (self.network_ssid != "" and self.network_password != ""):
            self.connect_wifi(self.network_ssid, self.network_password)

    def get_current_network(self):
        cmd = ["iwgetid", "-r"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")
            return None

        return output.strip()

    def get_ssid_psk(self, config):
        ssid_pattern = 'ssid="(.+?)"'
        psk_pattern = 'psk="(.+?)"'

        ssid = re.search(ssid_pattern, config)
        psk = re.search(psk_pattern, config)

        if ssid and psk:
            return ssid.group(1), psk.group(1)
        else:
            return None, None

    def connect_wifi(self, new_network_ssid, new_network_password):
        # Save the current network configuration
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as wifi_config:
            current_config = wifi_config.read()
            current_ssid, current_psk = self.get_ssid_psk(current_config)

            new_config = current_config
            new_config = new_config.replace(current_ssid, new_network_ssid)
            new_config = new_config.replace(current_psk, new_network_password)

        # Write the new network configuration to wpa_supplicant.conf
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as wifi_config:
            wifi_config.truncate(0)
            wifi_config.write(new_config)
            wifi_config.close()

        # Restart the wpa_supplicant service to connect to the new network
        cmd = ["sudo", "systemctl", "restart", "wpa_supplicant"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")

        cmd = ["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")

        # Check if the connection was successful
        time.sleep(10)  # Wait for the connection to establish

        new_ssid = self.get_current_network().decode('utf-8').strip()

        if new_network_ssid != new_ssid:
            print(
                "Failed to connect to the new network. Reverting to the previous network configuration.")

            # Revert to the previous network configuration
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi_config:
                wifi_config.truncate(0)
                wifi_config.write(current_config)
                wifi_config.close()

            # Restart the wpa_supplicant service to reconnect to the previous network
            cmd = ["sudo", "systemctl", "restart", "wpa_supplicant"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                print(f"Error: {error}")

            cmd = ["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                print(f"Error: {error}")

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

        # Set the window size
        self.resize(1024, 600)

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

        # Set the window size
        self.resize(1024, 600)

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
        self._translate = QtCore.QCoreApplication.translate
        loadUi('bluetooth.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.status.setText(self._translate(
            "bluetooth", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Scanning...Please wait!</span></p></body></html>"))
        self.discovery_thread = BluetoothDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(
            self.add_bluetooth_item)
        self.discovery_thread.start()

        self.refresh.clicked.connect(self.refresh_bluetooth_scan)
        self.back.clicked.connect(self.go_back)
        # Connect the combo box's activated signal to a slot function
        self.bluetooth1.activated[str].connect(self.on_combobox_activated)

    def refresh_bluetooth_scan(self):
        self.bluetooth1.clear()
        self.status.setText(self._translate(
            "bluetooth", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Scanning...Please wait!</span></p></body></html>"))
        self.discovery_thread = BluetoothDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(
            self.add_bluetooth_item)
        self.discovery_thread.start()

    def add_bluetooth_item(self, name, devices):
        self.status.setText(self._translate(
            "bluetooth", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">" + devices + " devices found</span></p></body></html>"))
        self.bluetooth1.addItem(name)

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


class WiFiDiscoveryThread(QThread):
    device_discovered = pyqtSignal(str, str)

    def run(self):
        interface = "wlan0"  # The default interface for Raspberry Pi's WiFi
        cmd = f"iwlist {interface} scan"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        lines = output.split("\n")
        networks = []

        for line in lines:
            line = line.strip()
            if "ESSID" in line:
                networks.append(line.split(":")[1].strip('"'))
        devices = str(len(networks))

        for network in networks:
            ssid = network
            self.device_discovered.emit(ssid, devices)


class BluetoothDiscoveryThread(QThread):
    device_discovered = pyqtSignal(str, str)

    def run(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = str(len(nearby_devices))
        print("Found {} devices.".format(len(nearby_devices)))
        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))
            self.device_discovered.emit(name, devices)


# Define similar classes for WifiWindow, RsWindow, and SetWindow
class ScanThread(QThread):
    foundUserID = pyqtSignal(str)

    def __init__(self, ser, pn532, start_stop_command_bytes):
        super().__init__()
        self.ser = ser
        self.pn532 = pn532
        self.start_stop_command_bytes = start_stop_command_bytes
        self.scanned = False
        self._isRunning = True

    def run(self):
        while self._isRunning:
            if not self.ser.isOpen():
                try:
                    self.ser.open()
                except Exception as e:
                    print(f"Failed to open serial port: {e}")
                    break

            try:
                data_bytes = self.ser.readline()
                data = data_bytes[-2:].decode("utf-8").strip()
                if data != "31":
                    data = self.ser.readline().decode("utf-8").strip()
                    if data:
                        self.foundUserID.emit(data)
                        self.scanned = True
                        self.ser.write(self.start_stop_command_bytes)

                    uid = self.pn532.read_passive_target(timeout=0.1)
                    if uid is not None:
                        uid_string = ''.join(
                            [hex(i)[2:].zfill(2) for i in uid])
                        self.foundUserID.emit(uid_string)
                        self.scanned = True
                        self.ser.write(self.start_stop_command_bytes)

            except Exception as e:
                print(f"Error reading from serial port: {e}")

            if self.scanned:
                self.stop()
                break

    def restart(self):
        self.stop()
        self._isRunning = True
        self.scanned = False
        self.start()

    def stop(self):
        self._isRunning = False
        # Close the serial port
        if self.ser.isOpen():
            try:
                self.ser.close()
            except Exception as e:
                print(f"Error closing serial port: {e}")
        self.wait()  # ensure the thread has fully stopped


class ProcessingThread(QThread):
    # Signal emitted when thread finishes
    finished_signal = pyqtSignal(str, bool)

    def __init__(self, file_path, userID, retry=False):
        super().__init__()
        self.file_path = file_path
        self.userID = userID
        self.retry = retry
        self.data_sent = False
        self.job_title = ""
        self.receiver = ""
        self.company_name = ""
        self.company_address = ""
        self.company_phone = ""
        self.date = ""
        self.receipt_number = ""
        self.payload = ""
        self.response = ""
        self.response_code = ""
        self.url = "http://filesharing.n2rtech.com/api/send-data?"

    def run(self):
        self.deviceID = self.get_mac_address()
        # self.deviceID = "10000000f7bbda73"
        self.retrieval_code = ""
        result = self.pdf_to_text_ocr()
        print(result)
        address = re.findall(
            r'^(.*(?:Street|Avenue|Road|Lane).*\d{4}?.*)$', result, re.MULTILINE)
        if address:
            address = address[0]
        else:
            address = " "
        print(address)

        keywords = ["item", "Quantity", "qty", "items"]
        keywords_info = ["Tax No", "Phone", "Email", "Invoice No", "Date"]

        receipt_info = self.find_table(result, keywords_info)
        info = self.extract_info(receipt_info)
        print(f"Tax Number: {info['Tax Number']}")
        print(f"Phone Number: {info['Phone Number']}")
        print(f"Email: {info['Email']}")
        print(f"Invoice Number: {info['Invoice Number']}")
        print(f"Date: {info['Date']}")
        print("\n\n")

        receipt_text = self.find_table(result, keywords)
        print(receipt_text)
        print("\n\n")

        receipt_text = receipt_text.replace('_', '0')
        receipt_text = receipt_text.replace('-', '0')
        receipt_text = receipt_text.replace('---', '0')
        items = self.extract_items(receipt_text)
        api_data = self.items_to_api_format(items)
        print(api_data)
        print("\n\n")

        print(self.userID)
        print("\n\n")

        print(self.deviceID)
        print("\n\n")

        # (data, receiver, company_name, company_address, company_phone, date, device_id, receipt_number)
        get_response = self.send_api_data(api_data, self.userID, "N2R Technologies3", address,
                                          info['Phone Number'], info['Date'], self.deviceID, info['Invoice Number'])
        self.decode_response(get_response)

        self.update_jobs_dict()

        # Emit signal when processing is done
        self.finished_signal.emit(self.retrieval_code, self.data_sent)

    def get_mac_address(self):
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    def find_table(self, text, keywords, min_columns=4):
        lines = text.split('\n')
        table_data = []
        header_found = False
        headers = []

        # Compile the regular expressions for case-insensitive keyword matching
        keyword_patterns = [re.compile(
            re.escape(kw), re.IGNORECASE) for kw in keywords]

        for line in lines:
            # Check if any of the keywords are present in the current line
            if any(pattern.search(line) for pattern in keyword_patterns):
                header_found = True
                headers.append(line)
                continue

            if header_found:
                row = line.split()

                # Stop processing when a row with fewer columns than min_columns is encountered
                if len(row) < min_columns:
                    break

                # Add the row to the table data
                table_data.append(line)

        # Reformat the table data
        formatted_table_data = []
        for data in table_data:
            formatted_data = ' '.join(data.split())
            formatted_table_data.append(formatted_data)

        # Join the headers and table data into a single string
        headers_string = "\n".join(headers)
        table_string = "\n".join(formatted_table_data)
        result = f"{headers_string}\n{table_string}"

        return result

    # def pdf_to_text_ocr(self):
    #     text = ''
    #     with pdfplumber.open(self.file_path) as pdf:
    #         for page in pdf.pages:
    #             text += page.extract_text()
    #     return text

    def pdf_to_text_ocr(self):
        # Convert PDF to images
        images = convert_from_path(self.file_path)

        # Initialize the OCR result string
        result = ""

        # Loop through the images and perform OCR
        for i, img in enumerate(images):
            # Extract non-table text from the page
            text = pytesseract.image_to_string(img, config="--psm 6 --oem 3")
            result += text
        return result

    def extract_items(self, text):
        lines = text.split('\n')
        items = []
        for line in lines:
            # Updated regex pattern to match item, quantity, unit price, tax, discount, and total
            pattern = r'\d+\s+([\w\s]+)\s+(\d+)\s+([\d\.]+)\s+([_\d\.%]+)\s+([_\d\.%]+)\s+([\d\.]+)'
            match = re.search(pattern, line)
            if match:
                item = match.group(1).strip()
                quantity = int(match.group(2))
                unit_price = float(match.group(3))
                tax = match.group(4)
                discount = match.group(5)
                total = float(match.group(6))
                items.append({
                    'item': item,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'tax': tax,
                    'discount': discount,
                    'total': total
                })
        return items

    def extract_info(self, text_info):
        # dictionary to hold the results
        info = {}

        # patterns for each of the data
        tax_pattern = r"Tax No\.:\s(\d+)"
        phone_pattern = r"Phone:\s(\d+)"
        email_pattern = r"Email:\s(\S+)"
        invoice_pattern = r"Bill to Invoice No\.:\s(\S+)"
        date_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2} \w{3}, \d{4}|\d{1,2},\w{3},\d{4}|\d{1,2} \w{3} \d{4})\b"

        # search for each pattern and add to dictionary
        tax_search = re.search(tax_pattern, text_info)
        if tax_search:
            info['Tax Number'] = tax_search.group(1)

        phone_search = re.search(phone_pattern, text_info)
        if phone_search:
            info['Phone Number'] = phone_search.group(1)

        email_search = re.search(email_pattern, text_info)
        if email_search:
            info['Email'] = email_search.group(1)

        invoice_search = re.search(invoice_pattern, text_info)
        if invoice_search:
            info['Invoice Number'] = invoice_search.group(1)

            # Extract only numbers from the text
            info['Invoice Number'] = "".join(
                filter(str.isdigit, info['Invoice Number']))

            # If the length of the numbers string is more than 9 characters
            if len(info['Invoice Number']) > 9:
                # Trim the numbers string to the first 9 characters
                info['Invoice Number'] = info['Invoice Number'][:9]

        match = re.search(date_pattern, str(text_info))
        if match:
            if '/' in match.group():
                info['Date'] = (datetime.strptime(
                    match.group(), "%d/%m/%Y").date()).isoformat()
            elif '-' in match.group():
                info['Date'] = (datetime.strptime(
                    match.group(), "%d-%m-%Y").date()).isoformat()
            elif ',' in match.group() and ' ' not in match.group():
                info['Date'] = (datetime.strptime(
                    match.group(), "%d,%b,%Y").date()).isoformat()
            elif ',' in match.group() and ' ' in match.group():
                info['Date'] = (datetime.strptime(
                    match.group(), "%d %b, %Y").date()).isoformat()
            elif ' ' in match.group() and ',' not in match.group():
                info['Date'] = (datetime.strptime(
                    match.group(), "%d %b %Y").date()).isoformat()

        return info

    def items_to_api_format(self, items):
        api_data = {}
        for i, item in enumerate(items):
            api_data[f'products[{i}][product]'] = item['item']
            api_data[f'products[{i}][quantity]'] = str(item['quantity'])
            api_data[f'products[{i}][price]'] = str(item['unit_price'])
            api_data[f'products[{i}][tax]'] = item['tax']
            api_data[f'products[{i}][total]'] = str(item['total'])
        return api_data

    def send_api_data(self, data, receiver, company_name, company_address, company_phone, date, device_id, receipt_number):
        payload = {'receiver': receiver,
                   'company_name': company_name,
                   'company_address': company_address,
                   'company_phone': company_phone,
                   'date': date,
                   'device_id': device_id,
                   'receipt_number': receipt_number}

        payload.update(data)
        files = [

        ]
        headers = {}

        response = requests.request(
            "POST", self.url, headers=headers, data=payload, files=files)

        self.receiver = receiver
        self.company_name = company_name
        self.company_address = company_address
        self.company_phone = company_phone
        self.date = date
        self.receipt_number = receipt_number
        self.payload = payload
        self.response = response.text
        return response.text

    def decode_response(self, response_text):
        # Parse the JSON string into a Python dictionary
        self.parsed_data = json.loads(response_text)

        # Check if 'success' or 'error' key exists in the parsed data
        if 'success' in self.parsed_data:
            self.response_code = "success"
            self.data_sent = True
            print("Data uploaded successfully to API.")

        elif 'error' in self.parsed_data:
            error = self.parsed_data['error']
            self.response_code = "error: " + str(error)
            response_message = self.parsed_data['response']

            # Print the error message
            print(f"Error: {error}")
            print(f"Response: {response_message}")

        else:
            print("Unexpected response format.")

        if 'CODE' in self.parsed_data:
            code = self.parsed_data['CODE']

            # Print the extracted values
            print(f"CODE: {code}")
            self.retrieval_code = str(code)

    def update_jobs_dict(self):
        jobs = {}
        i = 0

        try:
            # Read the file
            with open('my_jobs.json', 'r') as f:
                jobs = json.load(f)  # This will give you a dictionary
                # Get the size of the dictionary
                size = len(jobs)
                print(f"The dictionary contains {size} key-value pairs.")
        except json.JSONDecodeError:
            print("File is not valid JSON")
        except FileNotFoundError:
            print("File 'my_jobs.json' not found.")

        if jobs:
            # Get the last key-value pair added
            last_key, last_value = next(reversed(jobs.items()))
            print(f"Last key: {last_key}, last value: {last_value}")
            i = int(last_key)

        if (self.retry is not True):
            i += 1

            if i != 0:
                jobs[i] = {}
                jobs[i]["data_sent"] = self.data_sent
                jobs[i]["job_title"] = self.job_title
                jobs[i]["receiver"] = self.receiver
                jobs[i]["company_name"] = self.company_name
                jobs[i]["company_address"] = self.company_address
                jobs[i]["company_phone"] = self.company_phone
                jobs[i]["date"] = self.date
                jobs[i]["receipt_number"] = self.receipt_number
                jobs[i]["payload"] = self.payload
                jobs[i]["response"] = self.response
                jobs[i]["response_code"] = self.response_code

            # print(jobs)
            # Write the updated dictionary back to the file
            with open('my_jobs.json', 'w') as f:
                json.dump(jobs, f)


class SettingsWindow1(QMainWindow):
    def __init__(self, stacked_widget, file_path):
        super().__init__()
        loadUi('w3.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.stacked_widget = stacked_widget
        self.file_path = file_path
        self.next1.clicked.connect(self.open_keyboard)
        self.Retreive.clicked.connect(self.print_retrieval_code)

        # Barcode
        self.serial_port = "/dev/ttySC0"
        self.baud_rate = 9600
        start_scan_command = "7E 00 08 01 00 02 01 AB CD"
        self.start_scan_command_bytes = bytes.fromhex(
            start_scan_command.replace(" ", ""))
        start_stop_command = "7E 00 08 01 00 02 00 AB CD"
        self.start_stop_command_bytes = bytes.fromhex(
            start_stop_command.replace(" ", ""))

        # PN532
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(i2c, debug=False)
        self.pn532.SAM_configuration()

        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=0.5)
        self.ser.write(self.start_scan_command_bytes)

        self.scanThread = ScanThread(
            self.ser, self.pn532, self.start_stop_command_bytes)
        self.scanThread.foundUserID.connect(self.processUserID)
        self.scanThread.start()

        self.numeric_keyboard = NumericKeyboard(
            self, self.stacked_widget, self, self.scanThread, self.file_path)
        self.stacked_widget.addWidget(self.numeric_keyboard)

    def processUserID(self, scanned_data):
        self.userID = scanned_data
        print("Found a User ID:", scanned_data)
        self.processingThread = ProcessingThread(
            self.file_path, self.userID)
        self.processingThread.finished_signal.connect(
            self.onProcessingFinished)
        self.processingThread.start()

    def onProcessingFinished(self, retrieval_code, data_sent):
        self.code = retrieval_code
        self.data_sent = data_sent
        if self.data_sent:
            # use the remove() function to delete the file
            os.remove(self.file_path)
        print("Processing finished!")
        print(retrieval_code)

    def open_keyboard(self):
        self.scanThread.stop()
        index = self.stacked_widget.indexOf(self.numeric_keyboard)
        self.stacked_widget.setCurrentIndex(index)

    def print_retrieval_code(self):
        self.scanThread.stop()
        self.PrintRetrievalCode_window = PrintRetrievalCode(
            self.file_path, self.stacked_widget, self.scanThread)
        self.stacked_widget.addWidget(self.PrintRetrievalCode_window)
        self.stacked_widget.setCurrentWidget(self.PrintRetrievalCode_window)


class NumericKeyboard(QMainWindow):

    def __init__(self, parent, stacked_widget, numeric_keyboard, scanThread, file_path):
        super(NumericKeyboard, self).__init__()
        loadUi('W4.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.file_path = file_path
        self.numeric_keyboard = numeric_keyboard
        self.scanThread = scanThread
        self.number_found = False
        self.saved_value = ""
        self.name = ""
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
        self.Retry.clicked.connect(self.show_output)
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
        if self.number_found:
            self.userID = self.name
            self.processingThread = ProcessingThread(
                self.file_path, self.userID)
            self.processingThread.finished_signal.connect(
                self.onProcessingFinished)
            self.processingThread.start()
            self.DataSentWindow_window = DataSentWindow(
                self.file_path, self.stacked_widget, self.scanThread)
            self.stacked_widget.addWidget(self.DataSentWindow_window)
            self.stacked_widget.setCurrentWidget(self.DataSentWindow_window)

    def onProcessingFinished(self, retrieval_code, data_sent):
        self.code = retrieval_code
        self.data_sent = data_sent
        if self.data_sent:
            # use the remove() function to delete the file
            os.remove(self.file_path)
        print("Processing finished!")
        print(retrieval_code)

    def show_output(self):
        self.number = self.textEdit.toPlainText()
        print(f"Saved value: {self.number}")
        self.check_number_api()

    def destroy(self):
        # Switch back to the SettingsWindow1
        index = self.parent.stacked_widget.indexOf(self.numeric_keyboard)
        self.parent.stacked_widget.setCurrentIndex(index)
        # Restart the scanThread
        self.scanThread.restart()
        self.hide()

    def check_number_api(self):
        self.url = "http://filesharing.n2rtech.com/api/mobile-verify"
        self.payload = {'mobile': self.number}
        self.files = []
        self.headers = {}
        self.response = requests.request(
            "POST", self.url, headers=self.headers, data=self.payload, files=self.files)

        # Parse the JSON string into a Python dictionary
        self.parsed_data = json.loads(self.response.text)

        # Check if 'success' or 'error' key exists in the parsed data
        if 'success' in self.parsed_data:
            success = self.parsed_data['success']
            if self.parsed_data['firstname']:
                firstname = self.parsed_data['firstname']
                self.name = str(firstname)
                print(f"First name: {firstname}")
            if self.parsed_data['lastname']:
                lastname = self.parsed_data['lastname']
                self.name += str(lastname)
                print(f"Last name: {lastname}")

            # Print the extracted values
            print(f"Success: {success}")
            print(f"Name: {self.name}")
            self.username.setText(self.name)
            self.number_found = True

        elif 'error' in self.parsed_data:
            self.error = self.parsed_data['error']
            self.response_message = self.parsed_data['response']
            self.username.setText("Number not found!!!")

            # Print the error message
            print(f"Error: {self.error}")
            print(f"Response: {self.response_message}")
            self.number_found = False

        else:
            print("Unexpected response format.")
            self.number_found = False


class DataSentWindow(QMainWindow):
    def __init__(self, file_path, stacked_widget, scanThread):
        super().__init__()
        loadUi('w6.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.file_path = file_path
        self.stacked_widget = stacked_widget
        self.scanThread = scanThread

        self.timer = QTimer()
        self.timer.timeout.connect(self.go_home)
        self.timer.start(5000)

    def go_home(self):
        self.timer.stop()
        self.SettingWindow_window = SettingWindow(
            self.stacked_widget)
        self.stacked_widget.addWidget(self.SettingWindow_window)
        self.stacked_widget.setCurrentWidget(self.SettingWindow_window)


class PrintRetrievalCode(QMainWindow):
    def __init__(self, file_path, stacked_widget, scanThread):
        super().__init__()
        loadUi('w5.ui', self)

        # Set the window size
        self.resize(1024, 600)

        self.file_path = file_path
        self.stacked_widget = stacked_widget
        self.scanThread = scanThread

        self.userID = ""
        self.processingThread = ProcessingThread(
            self.file_path, self.userID)
        self.processingThread.finished_signal.connect(
            self.onProcessingFinished)
        self.processingThread.start()

    def onProcessingFinished(self, retrieval_code, data_sent):
        self.code = retrieval_code
        self.data_sent = data_sent
        if self.data_sent:
            pass
        # use the remove() function to delete the file
        os.remove(self.file_path)
        # self.thermal_print()
        print("Processing finished!")
        print(self.code)

        self.timer = QTimer()
        self.timer.timeout.connect(self.go_home)
        self.timer.start(500)

    def thermal_print(self):
        p = Serial(devfile='/dev/ttySC1',
                   baudrate=9600,
                   bytesize=8,
                   parity='N',
                   stopbits=1,
                   timeout=1.00,
                   dsrdtr=True
                   )
        p.set(
            align="center",
            font="b",
            width=1,
            height=1,
            density=2,
            invert=0,
            smooth=True,
            flip=False,
        )
        # Printing the image
        # here location can be your image path in “ ”
        p.image("/home/decas/Logo.png", impl="bitImageColumn")

        p.set(
            align="center",
            font="a",
            width=2,
            height=2,
            density=2,
            invert=0,
            smooth=False,
            flip=False,
        )
        p.text(str("TOKEN: " + str(self.code) + "\n"))

        # printing the initial data
        p.set(
            align="left",
        )
        p.text("\n")
        p.text("""Retrieve receipt on repslips.com\nSteps:\n
        1) Sign up / Log on to:  \n
                repslips.com\n2) Click on menu -->RETRIVAL \n
        3) Type the above code and SUBMIT \n
        4) View on recent Receipt \n
        Enjoy.........\n\n\n""")
        print("done")

    def go_home(self):
        self.timer.stop()
        self.SettingWindow_window = SettingWindow(
            self.stacked_widget)
        self.stacked_widget.addWidget(self.SettingWindow_window)
        self.stacked_widget.setCurrentWidget(self.SettingWindow_window)


class DirectoryChecker(QObject):
    open_settings_window1_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.path_data = ""  # Initialize path_data with an empty string

    def check_directory(self):
        # directory_path = '/home/decas/PDF/'
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


if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.exec_())


# Instructions/Commands
# sudo chmod 777 /tmp
# pip3 install pip3 install adafruit-circuitpython-pn532 pyserial escpos pytesseract cryptography==36.0.0 pdfplumber pdf2image
