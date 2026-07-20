"""
=========================================================
Encrypt NetApp Credentials
Author : Ravi Yadav

Purpose
-------
1. Read credentials.csv
2. Generate secret.key if not present
3. Encrypt plain text passwords
4. Update same credentials.csv
=========================================================
"""

import csv
from pathlib import Path
from cryptography.fernet import Fernet


CONFIG_DIR = Path("config")

CREDENTIAL_FILE = CONFIG_DIR / "credentials.csv"
KEY_FILE = CONFIG_DIR / "secret.key"


# --------------------------------------------------------
# Create or Load Encryption Key
# --------------------------------------------------------

def load_or_create_key():

    CONFIG_DIR.mkdir(exist_ok=True)

    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    key = Fernet.generate_key()

    KEY_FILE.write_bytes(key)

    print("Secret Key Created Successfully.")

    return key


# --------------------------------------------------------
# Encrypt Credentials
# --------------------------------------------------------

def encrypt_credentials():

    if not CREDENTIAL_FILE.exists():
        raise FileNotFoundError(
            f"{CREDENTIAL_FILE} not found."
        )

    key = load_or_create_key()

    cipher = Fernet(key)

    rows = []

    encrypted_count = 0
    skipped_count = 0

    # ----------------------------
    # Read Existing CSV
    # ----------------------------

    with open(
        CREDENTIAL_FILE,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        required_columns = [
            "ClusterName",
            "Username",
            "Password"
        ]

        if reader.fieldnames is None:
            raise ValueError("credentials.csv is empty.")

        for column in required_columns:

            if column not in reader.fieldnames:

                raise ValueError(
                    f"Missing column : {column}"
                )

        for row in reader:

            password = row["Password"].strip()

            # Already encrypted
            if password.startswith("gAAAAA"):

                skipped_count += 1

            else:

                password = cipher.encrypt(
                    password.encode()
                ).decode()

                encrypted_count += 1

            rows.append({

                "ClusterName": row["ClusterName"].strip(),

                "Username": row["Username"].strip(),

                "Password": password

            })

    # ----------------------------
    # Overwrite Same CSV
    # ----------------------------

    with open(
        CREDENTIAL_FILE,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ClusterName",
            "Username",
            "Password"
        ])

        for row in rows:

            writer.writerow([
                row["ClusterName"],
                row["Username"],
                row["Password"]
            ])

    print("\n====================================")
    print(" Credential Encryption Completed")
    print("====================================")
    print(f"Encrypted : {encrypted_count}")
    print(f"Skipped   : {skipped_count}")
    print(f"Updated   : {CREDENTIAL_FILE}")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    encrypt_credentials()