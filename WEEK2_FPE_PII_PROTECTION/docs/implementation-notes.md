# Implementation notes

The adapter creates a cipher for each exact input length and combines the configured tweak with key material to separate contexts. It intentionally supports only two explicit alphabets, preventing accidental mixed-format inputs.
