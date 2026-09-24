# AES-GCM concepts

AES is a block cipher. GCM turns AES into an AEAD construction: it encrypts plaintext and authenticates ciphertext plus optional Additional Authenticated Data (AAD). A nonce is public uniqueness material, not a password. The authentication tag detects tampering and must be checked before accepting plaintext.

The service uses a fresh 12-byte nonce from the operating system for every encryption. Reusing a nonce with one key can reveal relationships between plaintexts and undermine authentication.
