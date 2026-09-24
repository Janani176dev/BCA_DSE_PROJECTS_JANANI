import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.aes_gcm import AESGCMService

service = AESGCMService.generate()
packet = service.encrypt_text("end-to-end", b"record-1")
assert service.decrypt_text(packet, b"record-1") == "end-to-end"
print("[+] AES-GCM end-to-end exchange succeeded")
