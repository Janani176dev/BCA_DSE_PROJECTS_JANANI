# Week 3: CRYSTALS-Kyber and ML-KEM

CRYSTALS-Kyber is the historical name of the lattice-based KEM standardized by NIST as **ML-KEM in FIPS 203**. This independent Python 3.11+ project uses `cryptography`'s maintained standardized API; it does not implement lattice cryptography from scratch.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
python examples/basic_demo.py
python -m src.cli --parameter-set ML-KEM-1024
```

The current dependency exposes ML-KEM-768 and ML-KEM-1024. Alice generates a key pair, Bob encapsulates to the public key, and Alice decapsulates the ciphertext with the private key. Both receive the same shared secret.

## Hybrid note

The tests include a conceptual X25519 + ML-KEM composition followed by HKDF. Real hybrid protocols require standardized composition, transcript binding, algorithm negotiation, key confirmation, and careful failure behavior. This demo is not a wire protocol.
