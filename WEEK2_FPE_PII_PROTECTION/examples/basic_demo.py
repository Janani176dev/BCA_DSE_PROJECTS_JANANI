import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.fpe import FPEService

service = FPEService(b"demo-key-32-bytes-long-for-fpe!!")
value = "4532015112830366"
protected = service.encrypt(value, "numeric")
print("DEMO DATA - NOT REAL PAYMENT DATA")
print(f"original={value} protected={protected} recovered={service.decrypt(protected, 'numeric')}")
