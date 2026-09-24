import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.fpe import FPEService, generate_synthetic_records

fields = {"customer_id": "alphanumeric", "card_number": "numeric", "phone": "numeric"}
service = FPEService(b"0123456789abcdef", b"e2e")
records = generate_synthetic_records(3)
protected = service.protect_records(records, fields)
assert service.unprotect_records(protected, fields) == records
print("[+] Synthetic PII batch round trip succeeded")
