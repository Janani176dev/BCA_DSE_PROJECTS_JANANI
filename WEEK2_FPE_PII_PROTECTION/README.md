# Week 2: Format-Preserving Encryption

This independent Python 3.11+ project protects synthetic structured records while preserving length and character domain. All bundled values are `DEMO DATA - NOT REAL PERSONAL OR PAYMENT DATA`.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
python examples/basic_demo.py
```

FPE is deterministic for a key, tweak, alphabet, and value. The encryption domain is explicit (`numeric` or `alphanumeric`), and validation rejects characters outside it. JSON/CSV helpers support batch processing.

## Important limitation

`pyffx` provides an FF-style format-preserving construction suitable for this educational adapter, but teams should choose a maintained, independently audited implementation of NIST FF1 or FF3-1 for production. FPE does not authenticate records, hide length, prevent replay, or replace AES-GCM. Use authenticated encryption for general data and carefully control keys/tweaks.
