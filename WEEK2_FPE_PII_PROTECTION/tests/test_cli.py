try:
    from WEEK2_FPE_PII_PROTECTION.src.crypto.fpe import FPEService
except ModuleNotFoundError:
    from src.crypto.fpe import FPEService


def test_cli_field_shape_contract() -> None:
    service = FPEService(b"0123456789abcdef")
    value = service.encrypt("CUST000123", "alphanumeric")
    assert len(value) == 10