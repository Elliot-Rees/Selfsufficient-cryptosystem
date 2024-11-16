# Cryptographically Secure Random Number Generator (CSRNG) using the Yarrow Algorithm

## DISCLAMER

- This software is provided for educational and personal use only. It is not intended for government, military, or commercial applications. The author makes no guarantees regarding the security, reliability, or suitability of this program for any specific purpose, including cryptographic or sensitive operations.

- Use of this program is at your own risk. The author is not responsible for any misuse, damages, or legal liabilities arising from the use or distribution of this software.

- By using this program, you agree to adhere to applicable laws and regulations and acknowledge that the software is provided "as is," without any warranties, express or implied. 

## Overview

This project implements a **Cryptographically Secure Random Number Generator (CSRNG)** using the **Yarrow algorithm**, a well-established framework for generating high-entropy random data. It is designed to meet the demands of cryptographic applications, ensuring robustness against attacks and providing a reliable source of cryptographically strong keys for use in cryptogrpahic systems such as AES, RC4, Salsa20 and One Time Pads.

## Features

- **High Entropy**: Utilizes multiple entropy sources to seed the generator.
- **Cryptographic Security**: Resistant to known attacks and suitable for cryptographic applications.
- **Reseeding**: Periodic reseeding minimizes the risk of entropy depletion.
- **Performance**: Optimized for efficient generation of random numbers.
- **Extensibility**: Easily integrates additional entropy sources.

## How It Works

The Yarrow algorithm combines entropy collection, mixing, and deterministic generation to produce secure random numbers:

1. **Entropy Accumulation**: Collects entropy from multiple sources, such as system timings, hardware events, or user input.
2. **Entropy Pools**: Manages two entropy pools:
   - A **fast pool** for frequent reseeding.
   - A **slow pool** for high-entropy reseeding.
3. **Reseeding Logic**: Ensures the generator is reseeded periodically based on entropy thresholds.
4. **Pseudo-Random Output**: Uses a cryptographically secure pseudo-random number generator (CSPRNG) to produce output from the internal state.

## Development Specification

- Python 3.12.7
- Windows 11 Pro 21H2
- OS Build 22000.194

# License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Apendix

- Entropy collected using the Windows Cryptographic Primitives Library (Bcrypt.dll)
- [FIPS 140 Cryptographic Primatives Library Vallidation](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp4825.pdf)