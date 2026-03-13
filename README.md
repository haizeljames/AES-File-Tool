# 🔐 AES File Encryption Tool

A **Python-based AES file encryption and decryption utility** designed for secure and efficient file protection.
It supports **single files, folders, and recursive directory processing**, with both **interactive CLI mode** and **command-line automation**.

The tool focuses on **security, performance, and reliability**, ensuring that files are handled safely without accidental double encryption or incorrect decryption.

---

# 📦 Requirements

* **Python 3.8+**
* Python libraries:

  * `cryptography`
  * `tqdm`

Install dependencies:

```bash
pip install cryptography tqdm
```

---

# ✨ Features

* 🔐 **AES Encryption (CBC Mode)** for strong file security
* 📁 **Recursive folder encryption/decryption**
* ⚡ **Chunked processing** for safe handling of large files
* 🧠 **Smart file detection**

  * Skips already encrypted files
  * Skips non-encrypted files during decryption
* 💻 **Interactive CLI interface**
* ⚙️ **Command-line argument support** for automation
* 🔒 **Secure password input** (never stored)

---

# 🚀 Usage

## Encrypt a File

```bash
python3 main.py -e -f secret.txt
```

## Decrypt a File

```bash
python3 main.py -d -f secret.txt.enc
```

## Encrypt a Folder Recursively

```bash
python3 main.py -e -D Documents -r
```

## Decrypt a Folder Recursively

```bash
python3 main.py -d -D backup -r
```

## Encrypt Specific File Types

```bash
python3 main.py -e -D Documents -r --types .txt .pdf
```

---

# 🧠 Smart Processing Behavior

The tool includes safeguards to prevent common mistakes:

* Files already ending with `.enc` are **automatically skipped** during encryption.
* Files without `.enc` are **skipped during decryption**.
* Passwords are **securely requested at runtime**.
* Large files are processed using **chunked encryption** to reduce memory usage.

---

# 🔑 Encryption Details

| Component      | Implementation           |
| -------------- | ------------------------ |
| Algorithm      | AES                      |
| Mode           | CBC                      |
| Key Derivation | PBKDF2-HMAC-SHA256       |
| Iterations     | 100,000                  |
| Padding        | PKCS7                    |
| Metadata       | Salt + IV stored in file |

These parameters ensure **secure key derivation and reliable decryption**.

---

# ⚠️ Limitations

* **No parallel processing**
  Files are processed sequentially, so very large folders may take longer.

* **CLI-only interface**
  No graphical interface is provided.

* **No file recovery**
  Encrypted/decrypted files replace the original file. Backups are recommended.

* **Basic file type filtering**
  Only extension-based filtering is supported (no wildcard patterns).

* **Password dependent**
  If the wrong password is entered, decryption will fail and the file cannot be recovered.

* **Single-user design**
  Intended for personal file security, not for multi-user or network environments.

---

# 📜 License

This project is intended for **educational and personal security purposes**.

---

# 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
