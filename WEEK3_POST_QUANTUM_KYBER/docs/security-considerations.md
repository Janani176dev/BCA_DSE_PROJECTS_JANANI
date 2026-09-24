# Security considerations

Use the maintained library API and keep private keys in protected key storage. Bind the KEM exchange to identities and protocol transcripts, authenticate the resulting channel with AES-GCM or another AEAD, handle decapsulation failures safely, and follow current NIST guidance. Never serialize private keys into source or demo output.
