import pytest

try:
    from WEEK2_FPE_PII_PROTECTION.src.crypto.fpe import FPEService
except ModuleNotFoundError:
    from src.crypto.fpe import FPEService


def test_short_key_is_rejected() -> None:
    with pytest.raises(ValueError):
        FPEService(b"short")