"""
Why did the cryptographically secure random number generator go to therapy?

It couldn’t handle the pressure of always being unpredictable!
"""


import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
from Yarrow import Yarrow  

# Initialize the Yarrow instance
yarrow = Yarrow()

# Add entropy to initialize Yarrow's state
yarrow.add_entropy()
yarrow.add_entropy()

# Function to generate keys using Yarrow
def generate_keys_with_yarrow(num_keys):
    return [yarrow.generate_random(32).hex() for _ in range(num_keys)]

# Function to export keys
def export_keys(keys, export_format):
    file_path = None
    if export_format == "JSON":
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(keys, file)
    elif export_format == "Text":
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(keys))
    elif export_format == "CSV":
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Key"])  # Header
                for key in keys:
                    writer.writerow([key])
    if file_path:
        messagebox.showinfo("Export Successful", f"Keys exported successfully to {file_path}!")

# Function to enable encryption (mock functionality for demonstration)
def encrypt_message():
    encryption_window = tk.Toplevel(root)
    encryption_window.title("Encrypt Message")

    tk.Label(encryption_window, text="Enter Message to Encrypt:").pack(pady=5)
    message_entry = tk.Entry(encryption_window, width=40)
    message_entry.pack(pady=5)

    def encrypt():
        message = message_entry.get()
        encrypted_message = "".join(chr(ord(char) + 3) for char in message)  # Simple Caesar cipher
        messagebox.showinfo("Encrypted Message", f"Encrypted Message:\n{encrypted_message}")

    tk.Button(encryption_window, text="Encrypt", command=encrypt).pack(pady=10)

# Main UI setup
root = tk.Tk()
root.title("Random Acts of Security: The CSPRNG That Keeps You Guessing")
root.geometry("500x400")

# Number of keys to generate
num_keys_var = tk.IntVar(value=1)
infinite_keys_var = tk.BooleanVar(value=False)

tk.Label(root, text="Number of Keys to Generate:").pack(pady=5)
tk.Spinbox(root, from_=1, to=1000000, textvariable=num_keys_var, width=10).pack(pady=5)
tk.Checkbutton(root, text="Generate Infinite Keys", variable=infinite_keys_var).pack(pady=5)

# Export format selection
export_format_var = tk.StringVar(value="JSON")

tk.Label(root, text="Export Format:").pack(pady=5)
tk.Radiobutton(root, text="JSON", variable=export_format_var, value="JSON").pack()
tk.Radiobutton(root, text="Text", variable=export_format_var, value="Text").pack()
tk.Radiobutton(root, text="CSV", variable=export_format_var, value="CSV").pack()

# Encryption option
encrypt_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable Message Encryption", variable=encrypt_var).pack(pady=10)

# Generate and export keys
keys = []

def generate_and_export():
    global keys
    if infinite_keys_var.get():
        messagebox.showinfo("Not Implemented", "Infinite key generation is not implemented yet!")
    else:
        num_keys = num_keys_var.get()
        keys = generate_keys_with_yarrow(num_keys)
        export_keys(keys, export_format_var.get())

# Main buttons
tk.Button(root, text="Generate and Export Keys", command=generate_and_export).pack(pady=10)
tk.Button(root, text="Encrypt Message", command=encrypt_message, state="normal" if encrypt_var.get() else "disabled").pack(pady=10)

# Start the application
root.mainloop()
