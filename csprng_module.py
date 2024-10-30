import ctypes
import ctypes.wintypes
import hashlib

# Load advapi32.dll
advapi32 = ctypes.WinDLL('advapi32')

# Constants
PROV_RSA_FULL = 1
CRYPT_SILENT = 0x40
KEY_LENGTH = 32  # 32 bytes (256-bit key)

# Specify a provider name E.G. "Microsoft Enhanced Cryptographic Provider v1.0"
MS_ENHANCED_PROV = "Microsoft Enhanced Cryptographic Provider v1.0" # SPN (Service Provider Name)

# Error codes
ERROR_SUCCESS = 0

# Data types
HCRYPTPROV = ctypes.wintypes.HANDLE

# Function prototypes
advapi32.CryptAcquireContextW.argtypes = [
    ctypes.POINTER(HCRYPTPROV), 
    ctypes.c_wchar_p,  # Container name (None)
    ctypes.c_wchar_p,  # Provider name (SPN)
    ctypes.wintypes.DWORD,  # Provider type
    ctypes.wintypes.DWORD   # Flags
]
advapi32.CryptAcquireContextW.restype = ctypes.wintypes.BOOL

advapi32.CryptGenRandom.argtypes = [
    HCRYPTPROV, 
    ctypes.wintypes.DWORD, 
    ctypes.POINTER(ctypes.c_ubyte)
]
advapi32.CryptGenRandom.restype = ctypes.wintypes.BOOL

advapi32.CryptReleaseContext.argtypes = [
    HCRYPTPROV, 
    ctypes.wintypes.DWORD
]
advapi32.CryptReleaseContext.restype = ctypes.wintypes.BOOL


def generate_key_windows(key_size: int, provider_name: str = MS_ENHANCED_PROV) -> bytes:
    # Acquire cryptographic context with a specific provider name (SPN)
    h_prov = HCRYPTPROV()
    if not advapi32.CryptAcquireContextW(
        ctypes.byref(h_prov), None, provider_name, PROV_RSA_FULL, CRYPT_SILENT):
        raise ctypes.WinError()

    try:
        # Generate the random key
        key = (ctypes.c_ubyte * key_size)()
        if not advapi32.CryptGenRandom(h_prov, key_size, key):
            raise ctypes.WinError()
        # Convert the key to bytes
        return bytes(key)

    finally:
        # Release the cryptographic context
        if not advapi32.CryptReleaseContext(h_prov, 0):
            raise ctypes.WinError()


def hash_key_sha256(key: bytes) -> bytes:
    sha256 = hashlib.sha256()
    sha256.update(key)
    return sha256.digest()

key_size = 32  # 256-bit key
key = generate_key_windows(key_size)
#print(f"Generated Key: {key.hex()}") # For testing 

# Hash the key using SHA-256
hashed_key = hash_key_sha256(key)
#print(f"SHA-256 Hash: {hashed_key.hex()}") # For testing
