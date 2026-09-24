from pathlib import Path

import pytest

try:
    from WEEK1_AES_GCM.src.crypto.aes_gcm import AESGCMService, EncryptedPacket
except ModuleNotFoundError:
    from src.crypto.aes_gcm import AESGCMService, EncryptedPacket


def test_round_trip_and_aad() -> None:
    service = AESGCMService.generate()
    packet = service.encrypt_text("hello", b"context")
    assert service.decrypt_text(packet, b"context") == "hello"
    with pytest.raises(ValueError):
        service.decrypt_text(packet, b"changed")


@pytest.mark.parametrize("mutation", ["ciphertext", "nonce"])
def test_tampering_fails(mutation: str) -> None:
    service = AESGCMService.generate()
    packet = service.encrypt(b"payload")
    if mutation == "ciphertext":
        packet = EncryptedPacket(packet.nonce, bytes([packet.ciphertext[0] ^ 1]) + packet.ciphertext[1:])
    else:
        packet = EncryptedPacket(bytes([packet.nonce[0] ^ 1]) + packet.nonce[1:], packet.ciphertext)
    with pytest.raises(ValueError):
        service.decrypt(packet)


def test_wrong_key_empty_and_large_plaintext() -> None:
    service = AESGCMService.generate()
    other = AESGCMService.generate()
    packet = service.encrypt(b"")
    assert service.decrypt(packet) == b""
    with pytest.raises(ValueError):
        other.decrypt(packet)
    large = b"x" * 1_000_000
    assert service.decrypt(service.encrypt(large)) == large


def test_file_round_trip(tmp_path: Path) -> None:
    service = AESGCMService.generate()
    source, encrypted, recovered = tmp_path / "in.bin", tmp_path / "enc.json", tmp_path / "out.bin"
    source.write_bytes(b"file contents")
    service.encrypt_file(source, encrypted)
    service.decrypt_file(encrypted, recovered)
    assert recovered.read_bytes() == source.read_bytes()
