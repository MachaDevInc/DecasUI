import tkinter as tk
from functools import partial

class Keyboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Alphabetic Keyboard")
        self.configure(bg="white")
        self.geometry("1024x600")

        self.shift_on = False
        self.buttons = []

        self.input_field = tk.Entry(self, font=("Arial", 24))
        self.input_field.pack(fill=tk.X, padx=5, pady=5)

        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = tk.Frame(self)
        keyboard_frame.pack(pady=6)

        rows = [
            ("1234567890", 0),
            ("!@#$%^&*()", 1),
            ("qwertyuiop", 2),
            ("asdfghjkl", 3),
            ("zxcvbnm\"{", 4),
            (",./;'[]\\}|", 5),
            ("-=`<>?:_+~", 6),

        ]

        button_width = 10
        button_height = 4

        for chars, row in rows:
            button_row = []
            for i, char in enumerate(chars):
                key = tk.Button(
                    keyboard_frame,
                    text=char,
                    width=button_width,
                    height=button_height,
                    command=partial(self.press_key, char),
                )
                key.grid(row=row, column=i)
                button_row.append(key)
            self.buttons.append(button_row)

        shift_button = tk.Button(
            keyboard_frame, text="Shift", width=button_width, height=button_height, command=self.toggle_shift
        )
        shift_button.grid(row=4, column=10)

        backspace_button = tk.Button(
            keyboard_frame,
            text="Backspace",
            width=button_width,
            height=button_height,
            command=self.press_backspace,
        )
        backspace_button.grid(row=4, column=11)

    def press_key(self, char):
        if self.shift_on:
            char = char.upper()

        self.input_field.insert(tk.END, char)

    def toggle_shift(self):
        self.shift_on = not self.shift_on
        for row in self.buttons:
            for button in row:
                current_text = button.cget("text")
                updated_text = (
                    current_text.upper() if self.shift_on else current_text.lower()
                )
                button.config(text=updated_text)

    def press_backspace(self):
        text = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, text[:-1])

if __name__ == "__main__":
    keyboard = Keyboard()
    keyboard.mainloop()
