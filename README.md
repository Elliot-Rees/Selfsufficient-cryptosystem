# Cryptographically Secure Random Number Generator (CSRNG) using the Yarrow Algorithm

## Overview

This project implements a **Cryptographically Secure Random Number Generator (CSRNG)** using the **Yarrow algorithm**, a well-established framework for generating high-entropy random data. It is designed to meet the rigorous demands of cryptographic applications, ensuring robustness against attacks and providing a reliable source of randomness.

## Features

- **High Entropy**: Utilizes multiple entropy sources to seed the generator, ensuring unpredictability.
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

## Apendix

- Entropy collected using the Windows Cryptographic Primitives Library (Bcrypt.dll)
- [FIPS 140 Cryptographic Primatives Library Vallidation](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp4825.pdf)