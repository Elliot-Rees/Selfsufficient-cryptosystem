import ctypes
import ctypes.wintypes
# Load bcrypt.dll for AES key generation
bcrypt = ctypes.WinDLL('bcrypt')

# Constants
BCRYPT_SUCCESS = 0
BCRYPT_AES_ALGORITHM = "AES"

# Data types
BCRYPT_KEY_HANDLE = ctypes.wintypes.HANDLE
BCRYPT_ALG_HANDLE = ctypes.wintypes.HANDLE
BCRYPT_UINT32 = ctypes.wintypes.DWORD
BCRYPT_BYTE = ctypes.c_ubyte

# Function prototypes
bcrypt.BCryptOpenAlgorithmProvider.argtypes = [
    ctypes.POINTER(BCRYPT_ALG_HANDLE),
    ctypes.c_wchar_p,  # Algorithm
    ctypes.c_wchar_p,  # Provider
    BCRYPT_UINT32
]
bcrypt.BCryptOpenAlgorithmProvider.restype = BCRYPT_UINT32

bcrypt.BCryptDestroyKey.argtypes = [BCRYPT_KEY_HANDLE]
bcrypt.BCryptDestroyKey.restype = BCRYPT_UINT32

bcrypt.BCryptCloseAlgorithmProvider.argtypes = [BCRYPT_ALG_HANDLE, BCRYPT_UINT32]
bcrypt.BCryptCloseAlgorithmProvider.restype = BCRYPT_UINT32

bcrypt.BCryptGenRandom.argtypes = [
    ctypes.c_void_p,       # Output buffer
    ctypes.wintypes.DWORD, # Size of output buffer
    ctypes.wintypes.DWORD  # Flags
]
bcrypt.BCryptGenRandom.restype = BCRYPT_UINT32

def generate_random_bytes(size: int) -> bytes:
    # Create a buffer to hold the random bytes
    buffer = (BCRYPT_BYTE * size)()
    
    result = bcrypt.BCryptGenRandom(ctypes.byref(buffer), size, 0)
    
    if result != BCRYPT_SUCCESS:
        raise ctypes.WinError(result)  # Use the result directly
    
    return bytes(buffer)  # Return the bytes

def generate_aes_key(key_size: int) -> bytes:
    # Generate a random key
    key = generate_random_bytes(key_size)  # Key size in bytes
    return key

# Example usage
key_size = 256  # 256-bit key
key = generate_aes_key(key_size)
print(f"Generated AES Key: {key.hex()}")
