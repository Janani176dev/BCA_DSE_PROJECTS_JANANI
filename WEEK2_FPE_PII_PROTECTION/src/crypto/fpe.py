"""Validated format-preserving encryption adapter."""
from __future__ import annotations

import csv
import json
import secrets
import string
from pathlib import Path
from typing import Iterable

import pyffx

DOMAINS = {
    "numeric": "0123456789",
    "alphanumeric": string.ascii_uppercase + string.digits,
}


class FPEValidationError(ValueError):
    """Raised when a value is outside its configured FPE domain."""


class FPEService:
    """Apply deterministic, length-preserving FPE within an explicit alphabet.

    The underlying library is a small FF-style educational dependency. Production
    deployments should select a maintained, audited NIST FF1/FF3-1 implementation.
    """

    def __init__(self, key: bytes, tweak: bytes = b"") -> None:
        if len(key) < 16:
            raise ValueError("FPE keys must contain at least 16 bytes")
        self.key = key
        self.tweak = tweak

    def _cipher(self, value: str, domain: str) -> pyffx.String:
        alphabet = DOMAINS.get(domain)
        if alphabet is None:
            raise FPEValidationError(f"Unsupported domain: {domain}")
        if not value or any(character not in alphabet for character in value):
            raise FPEValidationError(f"Value is invalid for {domain} domain")
        # pyffx includes the tweak in the key material so domains can be separated.
        return pyffx.String(self.key + self.tweak, alphabet=alphabet, length=len(value))

    def encrypt(self, value: str, domain: str) -> str:
        return self._cipher(value, domain).encrypt(value)

    def decrypt(self, value: str, domain: str) -> str:
        return self._cipher(value, domain).decrypt(value)

    def protect_records(self, records: Iterable[dict[str, str]], fields: dict[str, str]) -> list[dict[str, str]]:
        protected = []
        for record in records:
            output = dict(record)
            for field, domain in fields.items():
                if field not in output:
                    raise FPEValidationError(f"Missing field: {field}")
                output[field] = self.encrypt(output[field], domain)
            protected.append(output)
        return protected

    def unprotect_records(self, records: Iterable[dict[str, str]], fields: dict[str, str]) -> list[dict[str, str]]:
        restored = []
        for record in records:
            output = dict(record)
            for field, domain in fields.items():
                if field not in output:
                    raise FPEValidationError(f"Missing field: {field}")
                output[field] = self.decrypt(output[field], domain)
            restored.append(output)
        return restored


def generate_synthetic_records(count: int = 3) -> list[dict[str, str]]:
    if count < 1:
        raise ValueError("count must be positive")
    return [
        {
            "customer_id": f"CUST{index:06d}",
            "card_number": "4532015112830366" if index % 2 else "5555555555554444",
            "phone": f"987654{index:04d}",
        }
        for index in range(1, count + 1)
    ]


def write_json(path: Path, records: list[dict[str, str]]) -> None:
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def read_json(path: Path) -> list[dict[str, str]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise FPEValidationError("JSON must contain a list of objects")
    return value


def write_csv(path: Path, records: list[dict[str, str]]) -> None:
    if not records:
        raise ValueError("records must not be empty")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
