# Architecture

Input records are parsed, validated against field-specific domains, transformed by `FPEService`, then written in the original JSON or CSV shape. Decryption performs the inverse operation. Field mappings are explicit rather than inferred from names.
