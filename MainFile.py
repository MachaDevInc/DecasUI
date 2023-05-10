from PyQt5.QtCore import QObject, pyqtSignal, QThread
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

import re
import json
import requests

import sys
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

import uuid

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
        while self._isRunning and not self.scanned:
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
                    uid_string = ''.join([hex(i)[2:].zfill(2) for i in uid])
                    self.foundUserID.emit(uid_string)
                    self.scanned = True
                    self.ser.write(self.start_stop_command_bytes)

    def restart(self):
        if self.isRunning():
            self.stop()
            self.wait()  # ensure the thread has fully stopped
        self._isRunning = True
        self.scanned = False
        self.start()

    def stop(self):
        self._isRunning = False
        self.wait()  # ensure the thread has fully stopped


class ProcessingThread(QThread):
    finished_signal = pyqtSignal()  # Signal emitted when thread finishes

    def __init__(self, file_path, userID, deviceID):
        super().__init__()
        self.file_path = file_path
        self.userID = userID
        self.deviceID = deviceID
        self.url = "http://filesharing.n2rtech.com/api/send-data?"

    def run(self):
        result = self.pdf_to_text_ocr()
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

        self.finished_signal.emit()  # Emit signal when processing is done

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

    def pdf_to_text_ocr(self):
        text = ''
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    # def pdf_to_text_ocr(self):
    #     # Convert PDF to images
    #     images = convert_from_path(self.file_path)

    #     # Initialize the OCR result string
    #     result = ""

    #     # Loop through the images and perform OCR
    #     for i, img in enumerate(images):
    #         # Extract non-table text from the page
    #         text = pytesseract.image_to_string(img, config="--psm 6 --oem 3")
    #         result += text
    #     return result

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
        date_pattern = r"Date: \b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2} \w{3}, \d{4}|\d{1,2},\w{3},\d{4}|\d{1,2} \w{3} \d{4})\b"

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

        date_search = re.search(date_pattern, text_info)
        if date_search:
            info['Date'] = date_search.group(1)

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

        return response.text

    def decode_response(self, response_text):
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(response_text)

        # Check if 'success' or 'error' key exists in the parsed data
        if 'success' in parsed_data:
            print("Data uploaded successfully to API.")

        elif 'error' in parsed_data:
            error = parsed_data['error']
            response_message = parsed_data['response']

            # Print the error message
            print(f"Error: {error}")
            print(f"Response: {response_message}")

        else:
            print("Unexpected response format.")

        if 'CODE' in parsed_data:
            retrieval_code = parsed_data['CODE']

            # Print the extracted values
            print(f"CODE: {retrieval_code}")


class SettingsWindow1(QMainWindow, Ui_MainWindow3):
    def __init__(self, stacked_widget, file_path):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        self.file_path = file_path
        self.next1.clicked.connect(self.open_keyboard)
        self.Retreive.clicked.connect(self.next_settings5)

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

        self.numeric_keyboard = NumericKeyboard(self, self, self.scanThread)
        self.stacked_widget.addWidget(self.numeric_keyboard)

    def processUserID(self, scanned_data):
        self.userID = scanned_data
        print("Found a User ID:", scanned_data)
        self.deviceID = self.get_mac_address()
        self.processingThread = ProcessingThread(
            self.file_path, self.userID, self.deviceID)
        self.processingThread.finished_signal.connect(
            self.onProcessingFinished)
        self.processingThread.start()

    def onProcessingFinished(self):
        print("Processing finished!")
        # You can add other code here to run when processing is done

    def get_mac_address(self):
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    def open_keyboard(self):
        self.scanThread.stop()
        self.scanThread.wait()
        index = self.stacked_widget.indexOf(self.numeric_keyboard)
        self.stacked_widget.setCurrentIndex(index)

    def next_settings5(self):
        self.scanThread.stop()
        self.scanThread.wait()
        proc2 = subprocess.Popen(["python", "s5.py"])
        time.sleep(10)
        proc2.terminate()


class NumericKeyboard(QMainWindow, Ui_MainWindow4):

    def __init__(self, parent, numeric_keyboard, scanThread):
        super().__init__()
        self.parent = parent
        self.numeric_keyboard = numeric_keyboard
        self.scanThread = scanThread
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
        self.number = self.textEdit.toPlainText()
        print(f"Saved value: {self.number}")
        self.check_number_api()
        # self.close()
        # proc2 = subprocess.Popen(["python", "s6.py"])
        # time.sleep(10)
        # proc2.terminate()

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
            name = ""
            success = self.parsed_data['success']
            if self.parsed_data['firstname']:
                firstname = self.parsed_data['firstname']
                name = str(firstname)
                print(f"First name: {firstname}")
            if self.parsed_data['lastname']:
                lastname = self.parsed_data['lastname']
                name += str(lastname)
                print(f"Last name: {lastname}")

            # Print the extracted values
            print(f"Success: {success}")
            print(f"Name: {name}")
            self.username.setText(name)

        elif 'error' in self.parsed_data:
            self.error = self.parsed_data['error']
            self.response_message = self.parsed_data['response']
            self.username.setText("Number not found!!!")

            # Print the error message
            print(f"Error: {self.error}")
            print(f"Response: {self.response_message}")

        else:
            print("Unexpected response format.")


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
