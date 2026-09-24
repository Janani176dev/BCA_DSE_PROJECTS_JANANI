"""AES-GCM authenticated encryption with serializable packets."""
from __future__ import annotations

import base64
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

LOGGER = logging.getLogger(__name__)
NONCE_SIZE = 12
KEY_SIZES = {16, 24, 32}


class CryptoPacketError(ValueError):
    """Raised when an encrypted packet is malformed."""


@dataclass(frozen=True)
class EncryptedPacket:
    """Transport representation for AES-GCM ciphertext and metadata."""

    nonce: bytes
    ciphertext: bytes

    def to_json(self) -> str:
        return json.dumps({
            "nonce": base64.b64encode(self.nonce).decode("ascii"),
            "ciphertext": base64.b64encode(self.ciphertext).decode("ascii"),
        })

    @classmethod
    def from_json(cls, value: str) -> "EncryptedPacket":
        try:
            payload = json.loads(value)
            nonce = base64.b64decode(payload["nonce"], validate=True)
            ciphertext = base64.b64decode(payload["ciphertext"], validate=True)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise CryptoPacketError("Invalid encrypted packet") from exc
        if len(nonce) != NONCE_SIZE or len(ciphertext) < 16:
            raise CryptoPacketError("Packet has invalid nonce or authentication tag")
        return cls(nonce, ciphertext)


class AESGCMService:
    """Encrypts text and files with a caller-supplied AES key."""

    def __init__(self, key: bytes) -> None:
        if len(key) not in KEY_SIZES:
            raise ValueError("AES key must be 128, 192, or 256 bits")
        self._cipher = AESGCM(key)

    @classmethod
    def generate(cls, key_size: int = 32) -> "AESGCMService":
        if key_size not in KEY_SIZES:
            raise ValueError("key_size must be 16, 24, or 32 bytes")
        return cls(AESGCM.generate_key(bit_length=key_size * 8))

    def encrypt(self, plaintext: bytes, aad: bytes | None = None) -> EncryptedPacket:
        nonce = os.urandom(NONCE_SIZE)
        return EncryptedPacket(nonce, self._cipher.encrypt(nonce, plaintext, aad))

    def decrypt(self, packet: EncryptedPacket, aad: bytes | None = None) -> bytes:
        if len(packet.nonce) != NONCE_SIZE or len(packet.ciphertext) < 16:
            raise CryptoPacketError("Malformed encrypted packet")
        try:
            return self._cipher.decrypt(packet.nonce, packet.ciphertext, aad)
        except InvalidTag as exc:
            LOGGER.warning("AES-GCM authentication failed")
            raise ValueError("Authentication failed: wrong key, AAD, nonce, or ciphertext") from exc

    def encrypt_text(self, plaintext: str, aad: bytes | None = None) -> EncryptedPacket:
        return self.encrypt(plaintext.encode("utf-8"), aad)

    def decrypt_text(self, packet: EncryptedPacket, aad: bytes | None = None) -> str:
        return self.decrypt(packet, aad).decode("utf-8")

    def encrypt_file(self, source: Path, destination: Path, aad: bytes | None = None) -> None:
        destination.write_text(self.encrypt(source.read_bytes(), aad).to_json(), encoding="utf-8")

    def decrypt_file(self, source: Path, destination: Path, aad: bytes | None = None) -> None:
        destination.write_bytes(self.decrypt(EncryptedPacket.from_json(source.read_text(encoding="utf-8")), aad))

    @property
    def key(self) -> bytes:
        """Return the key for controlled demo use; callers should use a secret store in production."""
        return self._cipher._key  # type: ignore[attr-defined]
