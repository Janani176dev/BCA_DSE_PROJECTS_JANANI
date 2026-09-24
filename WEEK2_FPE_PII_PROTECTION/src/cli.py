"""CLI for synthetic PII format-preserving protection."""
from __future__ import annotations

import argparse
import base64
from pathlib import Path

from .crypto.fpe import FPEService, read_csv, read_json, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Protect synthetic structured data with FPE")
    parser.add_argument("--key", required=True, help="base64 key, at least 16 decoded bytes")
    parser.add_argument("--tweak", default="")
    parser.add_argument("action", choices=("encrypt", "decrypt"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--format", choices=("json", "csv"), required=True)
    args = parser.parse_args()
    service = FPEService(base64.b64decode(args.key), args.tweak.encode())
    reader, writer = (read_json, write_json) if args.format == "json" else (read_csv, write_csv)
    fields = {"customer_id": "alphanumeric", "card_number": "numeric", "phone": "numeric"}
    records = reader(args.input)
    result = service.protect_records(records, fields) if args.action == "encrypt" else service.unprotect_records(records, fields)
    writer(args.output, result)


if __name__ == "__main__":
    main()
