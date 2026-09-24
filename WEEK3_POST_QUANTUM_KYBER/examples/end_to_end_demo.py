import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.mlkem import MLKEMService

for parameter_set in ("ML-KEM-768", "ML-KEM-1024"):
    service = MLKEMService(parameter_set)
    keys = service.generate_keypair()
    ciphertext, bob_secret = service.encapsulate(keys.public_key)
    assert service.decapsulate(keys.private_key, ciphertext) == bob_secret
    print(f"[+] {parameter_set} Alice/Bob exchange succeeded")
