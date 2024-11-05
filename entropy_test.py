import math
import csv
import argparse
import time
import signal
from collections import Counter
from csprng_module import generate_key_windows
import matplotlib.pyplot as plt

def calculate_entropy(key: bytes) -> float:
    frequency = Counter(key)
    key_length = len(key)

    entropy = -sum((freq / key_length) * math.log2(freq / key_length) for freq in frequency.values())
    return entropy

def run_entropy_analysis(num_iterations: int, csv_filename: str, infinite: bool):
    entropies = []

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Key (hex)", "Entropy (bits)"])

        try:
            iteration = 0
            while infinite or iteration < num_iterations:
                key_size = 32
                key = generate_key_windows(key_size)

                entropy = calculate_entropy(key)

                entropies.append(entropy)

                writer.writerow([key.hex(), entropy])
                file.flush()

                print(f"Key: {key.hex()} | Entropy: {entropy:.4f} bits")

                iteration += 1

                if iteration % 5 == 0:
                    plt.clf()
                    plt.hist(entropies, bins=40, color='skyblue', edgecolor='black')
                    plt.title("Entropy Distribution of Generated Keys")
                    plt.xlabel("Entropy (bits)")
                    plt.ylabel("Frequency")
                    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}'))
                    plt.pause(0.000000001)
                time.sleep(0)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Finalizing and saving results...")
            quit
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate keys, calculate entropy, and save results.")
    parser.add_argument("num_iterations", type=int, nargs='?', default=100, 
                        help="Number of keys to generate and analyze. Use 0 to run indefinitely.")
    parser.add_argument("csv_filename", type=str, help="CSV filename to save entropy results")
    parser.add_argument("-i", action="store_true", 
                        help="Run indefinitely, ignoring num_iterations")

    args = parser.parse_args()

    infinite_mode = args.i or args.num_iterations == 0

    run_entropy_analysis(args.num_iterations, args.csv_filename, infinite_mode)
