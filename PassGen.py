import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password(length, use_letters, use_numbers, use_symbols):
    """Generate a random password based on specified criteria."""
    if not (use_letters or use_numbers or use_symbols):
        raise ValueError("At least one character set (letters, numbers, symbols) must be selected")

    character_set = ""
    if use_letters:
        character_set += string.ascii_letters
    if use_numbers:
        character_set += string.digits
    if use_symbols:
        character_set += string.punctuation

    if len(character_set) == 0:
        raise ValueError("Character set cannot be empty")

    password = ''.join(random.choice(character_set) for _ in range(length))
    return password


def on_generate():
    try:
        length = int(length_entry.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        password = generate_password(length, use_letters, use_numbers, use_symbols)
        result_var.set(password)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def on_copy():
    password = result_var.get()
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard")


# Create the main window
root = tk.Tk()
root.title("Advanced Password Generator")

# Create and place widgets
tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=5)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).grid(row=1, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(row=3, column=0, columnspan=2)

generate_button = tk.Button(root, text="Generate Password", command=on_generate)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

tk.Label(root, text="Generated Password:").grid(row=5, column=0, padx=10, pady=5)
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, state='readonly')
result_entry.grid(row=5, column=1, padx=10, pady=5)

copy_button = tk.Button(root, text="Copy to Clipboard", command=on_copy)
copy_button.grid(row=6, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
