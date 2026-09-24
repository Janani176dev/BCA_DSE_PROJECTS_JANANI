"""CLI for a ML-KEM encapsulation demonstration."""
from __future__ import annotations

import argparse

from .crypto.mlkem import MLKEMService


def main() -> None:
    parser = argparse.ArgumentParser(description="CRYSTALS-Kyber / NIST ML-KEM demo")
    parser.add_argument("--parameter-set", choices=("ML-KEM-768", "ML-KEM-1024"), default="ML-KEM-768")
    args = parser.parse_args()
    service = MLKEMService(args.parameter_set)
    keys = service.generate_keypair()
    ciphertext, bob_secret = service.encapsulate(keys.public_key)
    alice_secret = service.decapsulate(keys.private_key, ciphertext)
    print(f"parameter_set={args.parameter_set}")
    print(f"ciphertext_bytes={len(ciphertext)}")
    print(f"shared_secret_match={alice_secret == bob_secret}")


if __name__ == "__main__":
    main()
