# Implementation notes

The `cryptography` package supplies AES-GCM and tag verification. Empty plaintext is valid. The packet parser rejects malformed base64, nonce lengths, and too-short ciphertexts before invoking the primitive.
