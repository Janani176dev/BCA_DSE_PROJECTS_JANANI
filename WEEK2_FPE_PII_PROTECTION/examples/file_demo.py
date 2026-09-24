import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crypto.fpe import FPEService, generate_synthetic_records, read_csv, write_csv

with TemporaryDirectory() as directory:
    path = Path(directory) / "records.csv"
    records = generate_synthetic_records(2)
    service = FPEService(b"0123456789abcdef", b"csv")
    write_csv(path, service.protect_records(records, {"customer_id": "alphanumeric", "card_number": "numeric", "phone": "numeric"}))
    assert service.unprotect_records(read_csv(path), {"customer_id": "alphanumeric", "card_number": "numeric", "phone": "numeric"}) == records
    print("[+] CSV batch round trip succeeded")
