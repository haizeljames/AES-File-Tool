# 🔐 **AES Encryption**
  - CBC Mode (`main.py`) for chunked, low-memory encryption
  - AES-GCM Mode (`upgraded_main.py`) for authenticated encryption (files <200 MB)

A **Python-based AES file encryption and decryption utility** designed for secure and efficient file protection.  
It supports **single files, folders, and recursive directory processing**, with both **interactive CLI mode** and **command-line automation**.

This repository now provides **two versions of the tool** for different use cases:

1. **`main.py` – Original CBC Mode**  
   - Low-memory chunked encryption  
   - Suitable for very large files  
   - AES-CBC + PKCS7 padding  
   - No tamper detection (less secure)  

2. **`upgraded_main.py` – AES-GCM Mode**  
   - High-security, authenticated encryption  
   - PBKDF2 with 200k iterations  
   - Tamper-proof, detects wrong passwords or modified files  
   - Reads full file into memory → best for files **<200 MB**  

> ⚠️ **Important:** You should choose **one version** of the tool and use it as `main.py`.  
> Do **not mix** the original CBC version with the upgraded AES-GCM version.  
> - Use the **original CBC version** for **low-memory or very large files**.  
> - Use the **upgraded AES-GCM version** for **high-security, small-to-medium files** (<200 MB).

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

* 🔐 **AES Encryption**
  - CBC Mode (`main.py`) for chunked, low-memory encryption
  - AES-GCM Mode (`upgraded_main.py`) for authenticated encryption (files <200 MB)
* 📁 **Recursive folder encryption/decryption**
* ⚡ **Chunked processing** (CBC) for safe handling of large files
* 🧠 **Smart file detection**
  - Skips already encrypted files
  - Skips non-encrypted files during decryption
* 💻 **Interactive CLI interface**
* ⚙️ **Command-line argument support** for automation
* 🔒 **Secure password input** (never stored)

---

# 🚀 Usage

> Note: If using AES-GCM, rename `upgraded_main.py` to `main.py` before running commands.

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

| Component      | CBC Mode (`main.py`)      | AES-GCM Mode (`upgraded_main.py`)          |
| -------------- | ------------------------ | ---------------------------------------- |
| Algorithm      | AES                      | AES                                       |
| Mode           | CBC                      | GCM (authenticated encryption)           |
| Key Derivation | PBKDF2-HMAC-SHA256       | PBKDF2-HMAC-SHA256                        |
| Iterations     | 100,000                  | 200,000                                   |
| Padding        | PKCS7                    | Not required (GCM handles padding)       |
| Metadata       | Salt + IV stored in file  | Salt + IV + Authentication Tag stored     |

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
