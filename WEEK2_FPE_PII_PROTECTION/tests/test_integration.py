from pathlib import Path

try:
    from WEEK2_FPE_PII_PROTECTION.src.crypto.fpe import FPEService, generate_synthetic_records, read_csv, read_json, write_csv, write_json
except ModuleNotFoundError:
    from src.crypto.fpe import FPEService, generate_synthetic_records, read_csv, read_json, write_csv, write_json


FIELDS = {"customer_id": "alphanumeric", "card_number": "numeric", "phone": "numeric"}


def test_batch_json_and_csv(tmp_path: Path) -> None:
    service = FPEService(b"0123456789abcdef", b"batch")
    records = generate_synthetic_records(3)
    json_path, csv_path = tmp_path / "data.json", tmp_path / "data.csv"
    write_json(json_path, records)
    write_csv(csv_path, records)
    for path, reader in ((json_path, read_json), (csv_path, read_csv)):
        protected = service.protect_records(reader(path), FIELDS)
        assert service.unprotect_records(protected, FIELDS) == records
