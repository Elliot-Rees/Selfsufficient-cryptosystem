"""
WORK IN PROGRESS!!!
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def stream_cipher_encrypt(message, key, iv_key):
    # Ensure keys are the correct size
    key = key[:32]  # Use only the first 32 bytes for AES-256
    iv_key = iv_key[:32]  # Use only the first 32 bytes for the IV

    # Derive the IV from the IV key
    iv = AES.new(iv_key, AES.MODE_ECB).encrypt(b'\x00' * 16)  # IV is always 16 bytes for AES

    # Create cipher object for encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the message to match the block size (16 bytes for AES)
    padded_message = pad(message.encode(), AES.block_size)

    # Encrypt the padded message
    ciphertext = cipher.encrypt(padded_message)

    # Append the IV to the ciphertext
    result = ciphertext + iv
    return result

def stream_cipher_decrypt(ciphertext, key, iv_key):
    # Ensure keys are the correct size
    key = key[:32]
    iv_key = iv_key[:32]

    # Split the ciphertext and the IV
    iv = ciphertext[-16:]  # The last 16 bytes are the IV
    ciphertext = ciphertext[:-16]  # The rest is the ciphertext

    # Create cipher object for decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt and unpad the message
    padded_message = cipher.decrypt(ciphertext)
    message = unpad(padded_message, AES.block_size)

    return message.decode()

if __name__ == "__main__":
    key = b"this_is_a_256_bit_secret_key__"  # Must be 32 bytes for AES-256
    iv_key = b"iv_key_for_aes_256_bit_usage"  # Must also be 32 bytes
    message = "Encrypt this secret message using AES-256!"

    # Encrypt the message
    encrypted = stream_cipher_encrypt(message, key, iv_key)
    print(f"Encrypted (hex): {encrypted.hex()}")

    # Decrypt the message testing
    decrypted = stream_cipher_decrypt(encrypted, key, iv_key)
    print(f"Decrypted: {decrypted}")
