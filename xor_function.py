import ctypes
import hashlib
from csprng_module import generate_key_windows, hash_key_sha256

def xor_with_key(plain_text, key):

    # Convert the plain text to bytes 
    plain_text_bytes = plain_text.encode('utf-8')
    
    # If the key is shorter than the plain text, extend it (using key modulo length)
    # If the key is longer, truncate it
    hashed_key = (key * (len(plain_text_bytes) // len(key) + 1))[:len(plain_text_bytes)]

    # XOR each byte of the plain text with the corresponding byte of the key
    xor_result = bytes([plain_text_bytes[i] ^ hashed_key[i] for i in range(len(plain_text_bytes))])

    return xor_result

if __name__ == "__main__":
    plain_text = "Test1234567890"
    
    key_size = 32  # 256-bit (32-byte)
    random_key = generate_key_windows(key_size)  # Call the csprng_module for key

    hashed_key = hash_key_sha256(random_key) # Hash the key using SHA-256

    xor_result = xor_with_key(plain_text, hashed_key) # XOR with the hashed key
    
    print(f"Plain Text: {plain_text}") #For testing
    print(f"Generated Key (hex): {random_key.hex()}") #For testing
    print(f"SHA-256 Hashed Key (hex): {hashed_key.hex()}") #For testing
    print(f"XOR Result (hex): {xor_result.hex()}") #For testing
