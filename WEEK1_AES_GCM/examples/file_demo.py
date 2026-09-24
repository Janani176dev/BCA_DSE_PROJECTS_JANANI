import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.aes_gcm import AESGCMService

with TemporaryDirectory() as directory:
    root = Path(directory)
    source, encrypted, recovered = root / "plain.txt", root / "encrypted.json", root / "recovered.txt"
    source.write_text("synthetic file payload", encoding="utf-8")
    service = AESGCMService.generate()
    service.encrypt_file(source, encrypted, b"file-v1")
    service.decrypt_file(encrypted, recovered, b"file-v1")
    print(f"[+] File round trip successful: {recovered.read_text(encoding='utf-8')}")
