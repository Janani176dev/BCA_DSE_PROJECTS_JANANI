try:
    from WEEK3_POST_QUANTUM_KYBER.src.crypto.mlkem import MLKEMService
except ModuleNotFoundError:
    from src.crypto.mlkem import MLKEMService


def test_supported_parameter_set() -> None:
    assert MLKEMService("ML-KEM-768").parameter_set == "ML-KEM-768"