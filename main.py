#!/usr/bin/env python3
import os
import argparse
import getpass
from tqdm import tqdm
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

EXT = ".enc"
CHUNK_SIZE = 64 * 1024  # 64 KB chunks
HEADER = b"MYENC"

examples = """
Examples:

Encrypt a file
  python3 main.py -e -f secret.txt

Decrypt a file
  python3 main.py -d -f secret.txt.enc

Encrypt folder recursively
  python3 main.py -e -D Documents -r --types .txt .pdf

Decrypt folder recursively
  python3 main.py -d -D Documents -r
"""

# ------------------- Key Derivation -------------------
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode())

# ------------------- File Encryption -------------------
def encrypt_file(filepath, password):
    if filepath.endswith(EXT):
        print(f"Skipped: {filepath} is already encrypted.")
        return
    if not os.path.isfile(filepath):
        print(f"Skipped: {filepath} does not exist.")
        return

    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    out_file = filepath + EXT
    with open(filepath, "rb") as fin, open(out_file, "wb") as fout:
        fout.write(salt + iv + HEADER)
        while chunk := fin.read(CHUNK_SIZE):
            padded_chunk = padder.update(chunk)
            if padded_chunk:
                fout.write(encryptor.update(padded_chunk))
        fout.write(encryptor.update(padder.finalize()) + encryptor.finalize())

    os.remove(filepath)
    print(f"Encrypted: {out_file}")

# ------------------- File Decryption -------------------
def decrypt_file(filepath, password):
    if not os.path.isfile(filepath):
        print(f"Skipped: {filepath} does not exist.")
        return
    if not filepath.endswith(EXT):
        print(f"Skipped: {filepath} is not encrypted. Cannot decrypt.")
        return

    with open(filepath, "rb") as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()

    if encrypted_data.startswith(HEADER):
        encrypted_data = encrypted_data[len(HEADER):]

    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()

    out_file = filepath[:-len(EXT)]
    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        final_data = unpadder.update(decrypted_data) + unpadder.finalize()
    except ValueError:
        print(f"Warning: {filepath} may have wrong password or be corrupted. Skipping.")
        return

    with open(out_file, "wb") as f:
        f.write(final_data)

    os.remove(filepath)
    print(f"Decrypted: {out_file}")

# ------------------- Folder Processing -------------------
def process_folder(folder, password, mode, recursive, types=None):
    files_to_process = []
    if recursive:
        for root, dirs, files in os.walk(folder):
            for file in files:
                files_to_process.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                files_to_process.append(full_path)

    if types:
        files_to_process = [f for f in files_to_process if os.path.splitext(f)[1] in types]

    if not files_to_process:
        print(f"No files to {mode} in {folder}")
        return

    print(f"Starting {mode}ion of {len(files_to_process)} files...")

    for path in tqdm(
        files_to_process,
        desc=f"{mode.capitalize()}ing files",
        unit="file",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files"
    ):
        if mode == "encrypt":
            encrypt_file(path, password)
        elif mode == "decrypt":
            decrypt_file(path, password)

# ------------------- Password Handling -------------------
def get_password(mode):
    if mode == "encrypt":
        while True:
            p1 = getpass.getpass("Enter keyphrase for encryption: ")
            p2 = getpass.getpass("Confirm keyphrase: ")
            if p1 == p2:
                return p1
            else:
                print("Keyphrases do not match. Try again.\n")
    else:
        return getpass.getpass("Enter keyphrase for decryption: ")

# ------------------- Professional CLI Menu -------------------
def cli_menu():
    print("\n=================================")
    print("        AES FILE TOOL")
    print("=================================")
    print("[1] Encrypt a file")
    print("[2] Decrypt a file")
    print("[3] Encrypt a folder")
    print("[4] Decrypt a folder")
    print("[5] Exit")
    choice = input("Select an option: ")
    return choice

# ------------------- Main Function -------------------
def main():
    parser = argparse.ArgumentParser(
        description="AES File Encryption Tool",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt mode")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt mode")
    parser.add_argument("-f", "--file", help="Target file")
    parser.add_argument("-D", "--dir", help="Target directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process folders recursively")
    parser.add_argument("--types", nargs="*", help="Specify file extensions to process, e.g. .txt .pdf")
    args = parser.parse_args()

    # ---------------- Menu Mode ----------------
    if not any(vars(args).values()):
        try:
            while True:
                choice = cli_menu()
                if choice == "1":
                    file = input("Enter file path: ")
                    if file.endswith(EXT):
                        print(f"Skipped: {file} is already encrypted.")
                    elif not os.path.isfile(file):
                        print(f"Skipped: {file} does not exist.")
                    else:
                        password = get_password("encrypt")
                        encrypt_file(file, password)

                elif choice == "2":
                    file = input("Enter file path: ")
                    if not file.endswith(EXT):
                        print(f"Skipped: {file} is not encrypted. Cannot decrypt.")
                    elif not os.path.isfile(file):
                        print(f"Skipped: {file} does not exist.")
                    else:
                        password = get_password("decrypt")
                        decrypt_file(file, password)

                elif choice == "3":
                    folder = input("Enter folder path: ")
                    password = get_password("encrypt")
                    types = input("Enter file extensions to include (space-separated, or leave blank): ").split()
                    process_folder(folder, password, "encrypt", True, types if types else None)

                elif choice == "4":
                    folder = input("Enter folder path: ")
                    password = get_password("decrypt")
                    types = input("Enter file extensions to include (space-separated, or leave blank): ").split()
                    process_folder(folder, password, "decrypt", True, types if types else None)

                elif choice == "5":
                    print("Exiting.")
                    break
                else:
                    print("Invalid option. Try again.")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting cleanly.")
        return

    # ---------------- CLI Args Mode ----------------
    mode = "encrypt" if args.encrypt else "decrypt"
    password = get_password(mode)

    if args.file:
        if mode == "encrypt":
            if args.file.endswith(EXT):
                print(f"Skipped: {args.file} is already encrypted.")
            elif not os.path.isfile(args.file):
                print(f"Skipped: {args.file} does not exist.")
            else:
                encrypt_file(args.file, password)
        else:
            if not args.file.endswith(EXT):
                print(f"Skipped: {args.file} is not encrypted. Cannot decrypt.")
            elif not os.path.isfile(args.file):
                print(f"Skipped: {args.file} does not exist.")
            else:
                decrypt_file(args.file, password)

    elif args.dir:
        process_folder(args.dir, password, mode, args.recursive, args.types)
    else:
        print("Provide a file (-f) or directory (-D)")

# ------------------- Entry Point -------------------
if __name__ == "__main__":
    main()
