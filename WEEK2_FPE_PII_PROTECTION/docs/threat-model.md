# Threat model

The service assumes an attacker can see protected values and their lengths and may compare repeated values. FPE limits structural changes but does not provide authentication, access control, or semantic privacy. Low-entropy identifiers remain vulnerable to guessing and frequency analysis.
