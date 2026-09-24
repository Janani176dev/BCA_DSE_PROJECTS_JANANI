# Threat model

An attacker can observe public keys and ciphertexts and modify ciphertext in transit. ML-KEM protects the shared secret under its assumptions when private keys remain confidential. It does not authenticate identities, prevent endpoint compromise, provide replay protection, or define application-level key confirmation.
