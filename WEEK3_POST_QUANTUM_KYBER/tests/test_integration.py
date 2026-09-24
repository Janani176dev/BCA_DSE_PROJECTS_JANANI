try:
    from WEEK3_POST_QUANTUM_KYBER.src.crypto.mlkem import MLKEMService
except ModuleNotFoundError:
    from src.crypto.mlkem import MLKEMService


def test_repeated_key_generation_is_independent() -> None:
    service = MLKEMService()
    first, second = service.generate_keypair(), service.generate_keypair()
    assert service.serialize_public_key(first.public_key) != service.serialize_public_key(second.public_key)