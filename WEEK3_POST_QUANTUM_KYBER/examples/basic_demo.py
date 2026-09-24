import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.mlkem import MLKEMService

service = MLKEMService("ML-KEM-768")
keys = service.generate_keypair()
ciphertext, bob_secret = service.encapsulate(keys.public_key)
alice_secret = service.decapsulate(keys.private_key, ciphertext)
print("[+] ML-KEM-768 encapsulated")
print(f"[+] Shared secrets match: {alice_secret == bob_secret}")
