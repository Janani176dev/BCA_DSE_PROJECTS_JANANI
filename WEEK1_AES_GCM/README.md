# Week 1: AES-GCM AEAD

This independent Python 3.11+ project demonstrates authenticated encryption with associated data (AEAD) using `cryptography`'s AES-GCM implementation.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python examples/basic_demo.py
pytest
```

Generate a demo key without storing it in source:

```powershell
$key = python -c "import base64; from cryptography.hazmat.primitives.ciphers.aead import AESGCM; print(base64.b64encode(AESGCM.generate_key(bit_length=256)).decode())"
python -m src.cli --key $key encrypt-text "secret demo" --aad request-42
# For a PowerShell-safe exchange, write/read the JSON packet as a file:
python -m src.cli --key $key encrypt-text "secret demo" --aad request-42 --output packet.json
python -m src.cli --key $key decrypt-text --packet-file packet.json --aad request-42
```

The packet contains a random 96-bit nonce and ciphertext with the 128-bit GCM tag. AAD is authenticated but remains visible. Any wrong key, changed AAD, nonce, ciphertext, or tag causes decryption to fail.

## Security notes

Never reuse a nonce with the same key. Keep keys in a secret manager or environment-backed key provider, and do not expose the demo `key` property in production. This project is educational and does not provide key rotation, access control, secure deletion, or a production file envelope format.
