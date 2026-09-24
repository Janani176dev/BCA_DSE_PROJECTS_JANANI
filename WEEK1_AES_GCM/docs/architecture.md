# Architecture

`AESGCMService` owns key validation and the encrypt/decrypt workflow. `EncryptedPacket` serializes only the public nonce and ciphertext-plus-tag. The CLI handles user input while the service remains reusable by applications and tests.
