"""Command-line interface for the AES-GCM project."""
from __future__ import annotations

import argparse
import base64
from pathlib import Path

from .crypto.aes_gcm import AESGCMService, EncryptedPacket


def _key(value: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("key must be base64") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="AES-GCM text and file encryption")
    parser.add_argument("--key", type=_key, required=True, help="base64-encoded AES key")
    subparsers = parser.add_subparsers(dest="command", required=True)
    encrypt_text = subparsers.add_parser("encrypt-text")
    encrypt_text.add_argument("plaintext")
    encrypt_text.add_argument("--aad", default="")
    encrypt_text.add_argument("--output", type=Path)
    decrypt_text = subparsers.add_parser("decrypt-text")
    decrypt_text.add_argument("packet", nargs="?")
    decrypt_text.add_argument("--packet-file", type=Path)
    decrypt_text.add_argument("--aad", default="")
    encrypt_file = subparsers.add_parser("encrypt-file")
    encrypt_file.add_argument("source", type=Path)
    encrypt_file.add_argument("destination", type=Path)
    decrypt_file = subparsers.add_parser("decrypt-file")
    decrypt_file.add_argument("source", type=Path)
    decrypt_file.add_argument("destination", type=Path)
    args = parser.parse_args()
    service = AESGCMService(args.key)
    if args.command == "encrypt-text":
        serialized = service.encrypt_text(args.plaintext, args.aad.encode()).to_json()
        if args.output:
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized)
    elif args.command == "decrypt-text":
        if not args.packet and not args.packet_file:
            parser.error("decrypt-text requires a packet or --packet-file")
        serialized = args.packet_file.read_text(encoding="utf-8") if args.packet_file else args.packet
        print(service.decrypt_text(EncryptedPacket.from_json(serialized), args.aad.encode()))
    elif args.command == "encrypt-file":
        service.encrypt_file(args.source, args.destination)
    else:
        service.decrypt_file(args.source, args.destination)


if __name__ == "__main__":
    main()
