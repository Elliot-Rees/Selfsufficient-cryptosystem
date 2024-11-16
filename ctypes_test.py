import ctypes
import ctypes.wintypes

# Load bcrypt.dll
bcrypt = ctypes.WinDLL('bcrypt')
BCRYPT_SUCCESS = 0
BCRYPT_BYTE = ctypes.c_ubyte

# Function prototype for BCryptGenRandom
bcrypt.BCryptGenRandom.argtypes = [
    ctypes.c_void_p,       # Output buffer
    ctypes.wintypes.DWORD, # Size of output buffer
    ctypes.wintypes.DWORD  # Flags
]
bcrypt.BCryptGenRandom.restype = ctypes.wintypes.DWORD

def test_bcrypt_gen_random():
    size = 16  # 128 bits
    buffer = (BCRYPT_BYTE * size)()
    result = bcrypt.BCryptGenRandom(ctypes.byref(buffer), size, 0)  # Test without the flag

    if result == BCRYPT_SUCCESS:
        print("Random bytes generated successfully:", bytes(buffer).hex())
    else:
        error_code = ctypes.c_long(result & 0xFFFFFFFF).value
        raise ctypes.WinError(error_code)

if __name__ == "__main__":
    test_bcrypt_gen_random()
