# Implementation notes

The installed `cryptography` 50.0.1 API currently exposes ML-KEM-768 and ML-KEM-1024, so the project advertises those supported parameter sets rather than inventing ML-KEM-512 support. Ciphertext mutation is rejected by the backend.
