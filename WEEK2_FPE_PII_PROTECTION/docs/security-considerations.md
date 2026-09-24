# Security considerations

Use synthetic data in development. Store keys and tweaks in a secret-management system, separate tenants with domain-specific configuration, authenticate records with an AEAD envelope, and minimize retention. Never assume a preserved format makes payment data compliant or safe.
