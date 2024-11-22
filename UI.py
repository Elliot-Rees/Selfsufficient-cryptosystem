"""
Why did the random number generator go to therapy?

It couldn’t handle the pressure of always being unpredictable!
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
from Yarrow import Yarrow
from scan import scan

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

# Function to enable encryption
def encrypt_message():
    encryption_window = tk.Toplevel(root)
    encryption_window.title("Encrypt Message")
    encryption_window.geometry("400x200")

    tk.Label(encryption_window, text="Enter Message to Encrypt:").pack(pady=5)
    message_entry = tk.Entry(encryption_window, width=40)
    message_entry.pack(pady=5)

    def encrypt():
        message = message_entry.get()
        if message:
            encrypted_message = "".join(chr(ord(char) + 3) for char in message)  # Simple Caesar cipher
            messagebox.showinfo("Encrypted Message", f"Encrypted Message:\n{encrypted_message}")
        else:
            messagebox.showwarning("Input Required", "Please enter a message to encrypt.")

    tk.Button(encryption_window, text="Encrypt", command=encrypt).pack(pady=10)

# Function to toggle encryption button state
def toggle_encrypt_button():
    if encrypt_var.get():
        encrypt_button.config(state="normal")
    else:
        encrypt_button.config(state="disabled")

# Function to handle scanning for keys and decrypting message.txt if key with "#" is found
def scan_for_key_and_decrypt():
    try:
        # Call the scan function from the 'scan' module and retrieve the key
        key_info = scan()  # Assuming scan() returns the key with a '#' appended if applicable

        if key_info:
            key = key_info.get('key', '')
            if '#' in key:
                decrypted_message = xor_decrypt_with_key(key)
                if decrypted_message:
                    messagebox.showinfo("Decrypted Message", f"Decrypted Message:\n{decrypted_message}")
                else:
                    messagebox.showerror("Decryption Failed", "Failed to decrypt message.txt.")
            else:
                messagebox.showinfo("Key Found", f"Key found: {key}\nNo decryption needed.")
        else:
            messagebox.showwarning("No Key Found", "No valid key was found on the drives.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during scanning: {str(e)}")

# Function to XOR the contents of message.txt with the key
def xor_decrypt_with_key(key):
    try:
        # Read the contents of message.txt
        with open("message.txt", "r") as message_file:
            message = message_file.read()

        # Perform XOR between each character of the message and the key
        decrypted_message = ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(message))
        return decrypted_message
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None

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
tk.Checkbutton(root, text="Enable Message Encryption", variable=encrypt_var, command=toggle_encrypt_button).pack(pady=10)

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
encrypt_button = tk.Button(root, text="Encrypt Message", command=encrypt_message, state="disabled")
encrypt_button.pack(pady=10)

# Add button for scanning and decrypting
tk.Button(root, text="Scan for Key", command=scan_for_key_and_decrypt).pack(pady=10)

# Start the application
root.mainloop()
