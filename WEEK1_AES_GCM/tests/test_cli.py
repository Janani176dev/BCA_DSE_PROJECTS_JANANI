from src.crypto.aes_gcm import AESGCMService, EncryptedPacket


def test_packet_serialization() -> None:
    service = AESGCMService.generate()
    packet = service.encrypt_text("cli-shaped packet")
    assert service.decrypt_text(EncryptedPacket.from_json(packet.to_json())) == "cli-shaped packet"