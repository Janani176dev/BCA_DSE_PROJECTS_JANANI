import pytest

try:
    from WEEK3_POST_QUANTUM_KYBER.src.crypto.mlkem import MLKEMService
except ModuleNotFoundError:
    from src.crypto.mlkem import MLKEMService


def test_unsupported_parameter_set_is_rejected() -> None:
    with pytest.raises(ValueError):
        MLKEMService("ML-KEM-512")