import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip


def generate_password(length, use_letters=True, use_numbers=True, use_symbols=True):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type (letters, numbers, symbols) must be selected.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_new_password():
    length = int(length_entry.get())
    use_letters = letters_var.get() == 1
    use_numbers = numbers_var.get() == 1
    use_symbols = symbols_var.get() == 1

    try:
        password = generate_password(length, use_letters, use_numbers, use_symbols)
        password_label.config(text=password)
        pyperclip.copy(password)  # Copy to clipboard
    except ValueError as e:
        password_label.config(text=str(e))


root = tk.Tk()
root.title("Password Generator")


options_frame = ttk.Frame(root, padding="10")
options_frame.grid(row=0, column=0, sticky="nsew")


length_label = ttk.Label(options_frame, text="Length:")
length_label.grid(row=0, column=0, sticky="w")
length_entry = ttk.Entry(options_frame)
length_entry.grid(row=0, column=1, sticky="w")
length_entry.insert(0, "12")


letters_var = tk.IntVar(value=1)
letters_check = ttk.Checkbutton(options_frame, text="Letters", variable=letters_var)
letters_check.grid(row=1, column=0, sticky="w")

numbers_var = tk.IntVar(value=1)
numbers_check = ttk.Checkbutton(options_frame, text="Numbers", variable=numbers_var)
numbers_check.grid(row=1, column=1, sticky="w")

symbols_var = tk.IntVar(value=1)
symbols_check = ttk.Checkbutton(options_frame, text="Symbols", variable=symbols_var)
symbols_check.grid(row=1, column=2, sticky="w")


generate_button = ttk.Button(options_frame, text="Generate Password", command=generate_new_password)
generate_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))


password_label = ttk.Label(root, text="")
password_label.grid(row=1, column=0, padx=10, pady=(10, 0))


refresh_button = ttk.Button(root, text="↺", command=generate_new_password)
refresh_button.grid(row=2, column=0, pady=(0, 10))


copy_button = ttk.Button(root, text="Copy to Clipboard", command=lambda: pyperclip.copy(password_label.cget("text")))
copy_button.grid(row=3, column=0, pady=(0, 10))


root.columnconfigure(0, weight=1)


root.mainloop()