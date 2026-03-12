# AES File Encryption Tool
A Python-based AES file encryption and decryption tool with folder support, interactive menu, and command-line arguments. Designed for secure, fast, and professional file handling

## Requirements
- Python 3.8+
- `cryptography` library
- `tqdm` library

## Features
- Supports recursive folder processing.
- Skips files that are already encrypted or not encrypted.
- Chunked encryption/decryption to safely handle large files.
- Interactive CLI.
- Command-line arguments support for automation.
- Prevents accidental double encryption or decrypting non-encrypted files.

## Usage
- python3 enc.py -e -f secret.txt          # Encrypt a single file
- python3 enc.py -d -f secret.txt.enc      # Decrypt a single file
- python3 enc.py -e -D Documents -r        # Encrypt folder recursively
- python3 enc.py -d -D backup -r           # Decrypt folder recursively
- python3 enc.py -e -D Documents -r --types .txt .pdf  # Encrypt specific file types

## Features
- Already encrypted files (.enc) are skipped automatically.
- Non-encrypted files during decryption are skipped.
- Passwords are requested securely and never stored.
- Works with large files using chunked AES-CBC encryption.

## Encryption Details
- Algorithm: AES (CBC mode)
- Key derivation: PBKDF2-HMAC-SHA256, 100,000 iterations
- Padding: PKCS7
- Salt + IV + optional header stored in file for safe decryption

## Limitations
- No parallel processing: Currently, files are encrypted/decrypted sequentially. Large folders may take time.
- No GUI: Fully CLI-based with optional interactive menu.
- No file recovery: Once a file is encrypted or decrypted, the original is replaced. Backup is recommended.
- Limited file type filtering: You can filter by extensions, but wildcards or patterns are not supported.
- Password-sensitive: If the wrong password is entered, decryption fails with a warning; no recovery is possible.
- Single-user focus: Designed for personal use; no multi-user or networked access.
