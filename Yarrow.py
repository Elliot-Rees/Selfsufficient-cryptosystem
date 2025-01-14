import ctypes
import hashlib
import hmac
from ctypes import wintypes
from collections import deque

class Yarrow:
    def __init__(self, entropy_threshold_fast=100, entropy_threshold_slow=160):
        # Define entropy pools (Fast and Slow)
        self.fast_pool = deque()
        self.slow_pool = deque()
        
        # Entropy thresholds for reseeding
        self.entropy_threshold_fast = entropy_threshold_fast
        self.entropy_threshold_slow = entropy_threshold_slow
        
        # State: Initialization with some entropy
        self.state = self.get_bcrypt_entropy(32)  # Initial state (256-bit for security)
        
        # Counter to keep track of outputs
        self.counter = 0
    
    def get_bcrypt_entropy(self, num_bytes): # Collect entropy using the Windows Bcrypt library
        
        # Load bcrypt.dll
        bcrypt = ctypes.windll.bcrypt
        
        # Define buffer to hold random bytes
        buffer = (ctypes.c_ubyte * num_bytes)()
        
        # Call BCryptGenRandom to fill the buffer
        if bcrypt.BCryptGenRandom(None, ctypes.byref(buffer), num_bytes, 0x02) != 0:
            raise RuntimeError("Entropy could not be collected using BCryptGenRandom.")
        
        # Convert buffer to bytes and return
        return bytes(buffer)

    def add_entropy(self): # Adds entropy to fast and slow pools
    
        data = self.get_bcrypt_entropy(32)  # 256-bit entropy chunk
        self.fast_pool.append(data)
        if len(self.fast_pool) >= self.entropy_threshold_fast:
            self.reseed('fast')
        
        self.slow_pool.append(data)
        if len(self.slow_pool) >= self.entropy_threshold_slow:
            self.reseed('slow')
    
    def reseed(self, pool_type): # Reseeds the state with entropy from the specified pool

        if pool_type == 'fast' and len(self.fast_pool) >= self.entropy_threshold_fast:
            entropy = b''.join(self.fast_pool)
            self.fast_pool.clear()
        elif pool_type == 'slow' and len(self.slow_pool) >= self.entropy_threshold_slow:
            entropy = b''.join(self.slow_pool)
            self.slow_pool.clear()
        else:
            return  # Do nothing if thresholds are not met
        
        # Hash the entropy with the current state to produce a new state
        self.state = hashlib.sha256(self.state + entropy).digest()
        self.counter = 0  # Reset counter after reseed
        
    def generate_random(self, num_bytes=32):
        # Increment the counter and perform reseed if necessary
        self.counter += 1
        if self.counter > 100:  # Arbitrary reseed interval
            self.reseed('fast')
        
        # Create an HMAC of the state and counter for random output
        output = hmac.new(self.state, self.counter.to_bytes(8, 'big'), hashlib.sha256).digest()
        return output[:num_bytes]

yarrow = Yarrow()

# Collect entropy using BcryptGenRandom
yarrow.add_entropy()
yarrow.add_entropy()

# Generate a random 32-byte number
random_number = yarrow.generate_random()
print("Random number:", random_number.hex())