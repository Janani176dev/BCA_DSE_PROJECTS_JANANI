import pytest

from src.crypto.aes_gcm import AESGCMService


def test_invalid_key_size_is_rejected() -> None:
    with pytest.raises(ValueError):
        AESGCMService(b"short")