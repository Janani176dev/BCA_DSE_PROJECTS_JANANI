# Threat model

An attacker may read, reorder, modify, truncate, or replay stored packets and may know AAD. The attacker does not possess the AES key. GCM provides confidentiality and integrity for the packet contents, but it does not prevent replay, traffic analysis, key compromise, endpoint compromise, or unauthorized access. Add authenticated sequence numbers, key lifecycle controls, and access policy in a real protocol.
