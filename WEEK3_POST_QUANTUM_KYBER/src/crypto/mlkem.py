"""Small wrapper around cryptography's standardized ML-KEM API."""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import mlkem, x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

PARAMETERS: dict[str, tuple[type[Any], type[Any]]] = {
    "ML-KEM-768": (mlkem.MLKEM768PrivateKey, mlkem.MLKEM768PublicKey),
    "ML-KEM-1024": (mlkem.MLKEM1024PrivateKey, mlkem.MLKEM1024PublicKey),
}


@dataclass(frozen=True)
class MLKEMKeyPair:
    private_key: Any
    public_key: Any
    parameter_set: str


class MLKEMService:
    """Generate and use NIST ML-KEM key pairs without implementing the primitive."""

    def __init__(self, parameter_set: str = "ML-KEM-768") -> None:
        if parameter_set not in PARAMETERS:
            raise ValueError(f"Unsupported parameter set: {parameter_set}")
        self.parameter_set = parameter_set

    def generate_keypair(self) -> MLKEMKeyPair:
        private = PARAMETERS[self.parameter_set][0].generate()
        return MLKEMKeyPair(private, private.public_key(), self.parameter_set)

    @staticmethod
    def encapsulate(public_key: Any) -> tuple[bytes, bytes]:
        shared_secret, ciphertext = public_key.encapsulate()
        return ciphertext, shared_secret

    @staticmethod
    def decapsulate(private_key: Any, ciphertext: bytes) -> bytes:
        if not isinstance(ciphertext, bytes) or not ciphertext:
            raise ValueError("ciphertext must be non-empty bytes")
        return private_key.decapsulate(ciphertext)

    @staticmethod
    def serialize_public_key(public_key: Any) -> str:
        raw = public_key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return base64.b64encode(raw).decode("ascii")

    @staticmethod
    def hybrid_secret(classical_private: x25519.X25519PrivateKey, classical_peer_public: x25519.X25519PublicKey, pq_secret: bytes) -> bytes:
        classical_secret = classical_private.exchange(classical_peer_public)
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"demo-hybrid-mlkem").derive(classical_secret + pq_secret)
