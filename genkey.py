import tkinter as tk

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

if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    keyboard.mainloop()
