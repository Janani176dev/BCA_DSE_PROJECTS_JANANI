import pytest

try:
    from WEEK2_FPE_PII_PROTECTION.src.crypto.fpe import FPEValidationError, FPEService
except ModuleNotFoundError:
    from src.crypto.fpe import FPEValidationError, FPEService


@pytest.fixture
def service() -> FPEService:
    return FPEService(b"0123456789abcdef", b"demo")


def test_round_trip_and_format_preservation(service: FPEService) -> None:
    for value, domain in (("4532015112830366", "numeric"), ("CUST000123", "alphanumeric")):
        protected = service.encrypt(value, domain)
        assert len(protected) == len(value)
        assert service.decrypt(protected, domain) == value


def test_deterministic_and_tweak_sensitive(service: FPEService) -> None:
    assert service.encrypt("9876543210", "numeric") == service.encrypt("9876543210", "numeric")
    other = FPEService(service.key, b"other")
    assert service.encrypt("9876543210", "numeric") != other.encrypt("9876543210", "numeric")


def test_invalid_domain_and_value(service: FPEService) -> None:
    with pytest.raises(FPEValidationError):
        service.encrypt("ABC", "numeric")
    with pytest.raises(FPEValidationError):
        service.encrypt("ABC", "unknown")


def test_wrong_key_does_not_round_trip(service: FPEService) -> None:
    protected = service.encrypt("4532015112830366", "numeric")
    assert FPEService(b"fedcba9876543210", b"demo").decrypt(protected, "numeric") != "4532015112830366"
