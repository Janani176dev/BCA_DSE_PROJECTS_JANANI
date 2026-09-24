"""Run a small AES-GCM demonstration."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.aes_gcm import AESGCMService

service = AESGCMService.generate()
packet = service.encrypt_text("Authenticated demo message", aad=b"week1")
print("[+] Ciphertext and tag generated")
print(service.decrypt_text(packet, aad=b"week1"))
