import pytest
from cryptography.hazmat.primitives.asymmetric import x25519

try:
    from WEEK3_POST_QUANTUM_KYBER.src.crypto.mlkem import MLKEMService
except ModuleNotFoundError:
    from src.crypto.mlkem import MLKEMService


@pytest.mark.parametrize("parameter_set", ["ML-KEM-768", "ML-KEM-1024"])
def test_end_to_end(parameter_set: str) -> None:
    service = MLKEMService(parameter_set)
    keys = service.generate_keypair()
    ciphertext, bob_secret = service.encapsulate(keys.public_key)
    assert service.decapsulate(keys.private_key, ciphertext) == bob_secret


def test_tampered_and_invalid_ciphertext_fail() -> None:
    service = MLKEMService()
    keys = service.generate_keypair()
    ciphertext, expected = service.encapsulate(keys.public_key)
    tampered = bytes([ciphertext[0] ^ 1]) + ciphertext[1:]
    assert service.decapsulate(keys.private_key, tampered) != expected
    with pytest.raises(ValueError):
        service.decapsulate(keys.private_key, b"")


def test_wrong_secret_key_fails_or_changes_secret() -> None:
    service = MLKEMService()
    first, second = service.generate_keypair(), service.generate_keypair()
    ciphertext, expected = service.encapsulate(first.public_key)
    try:
        actual = service.decapsulate(second.private_key, ciphertext)
    except ValueError:
        return
    assert actual != expected


def test_hybrid_composition_demo() -> None:
    service = MLKEMService()
    keys = service.generate_keypair()
    ciphertext, pq_bob = service.encapsulate(keys.public_key)
    alice_classical = x25519.X25519PrivateKey.generate()
    bob_classical = x25519.X25519PrivateKey.generate()
    alice = service.hybrid_secret(alice_classical, bob_classical.public_key(), service.decapsulate(keys.private_key, ciphertext))
    bob = service.hybrid_secret(bob_classical, alice_classical.public_key(), pq_bob)
    assert alice == bob
