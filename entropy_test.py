import matplotlib.pyplot as plt
import numpy as np
import time
from Yarrow import Yarrow
# Initialize Yarrow instance
yarrow = Yarrow()

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 5))

while True:
    # Generate a large number of random numbers
    num_samples = 10000
    random_numbers = [int.from_bytes(yarrow.generate_random(4), 'big') for _ in range(num_samples)] 
    # Print current random number
    print("Current random number:", random_numbers[-1])   
    # Clear previous plot
    ax.clear()  
    # Plot histogram
    ax.hist(random_numbers, bins=50, density=True, alpha=0.6, color='b')
    ax.set_title("Distribution of Random Numbers Generated by Yarrow")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    
    plt.draw()
    plt.pause(5)  # Update every 5 seconds
