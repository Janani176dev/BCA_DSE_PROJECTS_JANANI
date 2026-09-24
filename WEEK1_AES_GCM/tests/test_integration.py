from src.crypto.aes_gcm import AESGCMService


def test_text_workflow() -> None:
    service = AESGCMService.generate()
    packet = service.encrypt_text("integration", b"metadata")
    assert service.decrypt_text(packet, b"metadata") == "integration"