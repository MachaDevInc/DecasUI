import tkinter as tk


class NumericKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Numeric Keyboard")
        self.geometry("300x300")

        self.result_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=10)

        entry = tk.Entry(entry_frame, textvariable=self.result_var, width=20)
        entry.grid(row=0, column=0)

        button_frame = tk.Frame(self)
        button_frame.pack()

        buttons = [
            ('7', 0, 0),
            ('8', 0, 1),
            ('9', 0, 2),
            ('4', 1, 0),
            ('5', 1, 1),
            ('6', 1, 2),
            ('1', 2, 0),
            ('2', 2, 1),
            ('3', 2, 2),
            ('0', 3, 0),
            ('Enter', 3, 1),
            ('Delete', 3, 2),
        ]

        for (text, row, column) in buttons:
            if text == 'Enter':
                button = tk.Button(button_frame, text=text, command=self.enter_pressed)
            elif text == 'Delete':
                button = tk.Button(button_frame, text=text, command=self.delete_pressed)
            else:
                button = tk.Button(button_frame, text=text, command=lambda t=text: self.append_number(t))

            button.grid(row=row, column=column, padx=5, pady=5, ipadx=10, ipady=10)

    def append_number(self, text):
        current_result = self.result_var.get()
        self.result_var.set(current_result + text)

    def enter_pressed(self):
        entered_number = self.result_var.get()
        print(f"Entered number: {entered_number}")
        self.destroy()

    def delete_pressed(self):
        current_result = self.result_var.get()
        if len(current_result) > 0:
            self.result_var.set(current_result[:-1])


if __name__ == "__main__":
    app = NumericKeyboard()
    app.mainloop()
