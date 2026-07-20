"""
=========================================================
Authentication Module
Reads encrypted credentials from CSV
=========================================================
"""

import csv
from pathlib import Path
from cryptography.fernet import Fernet


CREDENTIAL_FILE = Path("config") / "credentials.csv"
KEY_FILE = Path("config") / "secret.key"


def load_key():
    """
    Load encryption key.
    """

    if not KEY_FILE.exists():
        raise FileNotFoundError(
            f"Encryption key not found : {KEY_FILE}"
        )

    return KEY_FILE.read_bytes()


def load_credentials():
    """
    Read credentials.csv and decrypt passwords.

    Returns:
        dict

        {
            "NetApp-Prod":
            {
                "username":"admin",
                "password":"xxxxx"
            },

            "NetApp-DR":
            {
                "username":"admin",
                "password":"xxxxx"
            }
        }
    """

    if not CREDENTIAL_FILE.exists():
        raise FileNotFoundError(
            f"Credential file not found : {CREDENTIAL_FILE}"
        )

    key = load_key()
    cipher = Fernet(key)

    credentials = {}

    with open(
        CREDENTIAL_FILE,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(
                "Credential file is empty."
            )

        required_columns = [
            "ClusterName",
            "Username",
            "Password"
        ]

        for column in required_columns:
            if column not in reader.fieldnames:
                raise ValueError(
                    f"Missing required column : {column}"
                )

        for row in reader:

            cluster = row["ClusterName"].strip()

            username = row["Username"].strip()

            encrypted_password = row["Password"].strip()

            password = cipher.decrypt(
                encrypted_password.encode()
            ).decode()

            credentials[cluster] = {
                "username": username,
                "password": password
            }

    return credentials


if __name__ == "__main__":

    creds = load_credentials()

    print("\nLoaded Credentials\n")

    for cluster, data in creds.items():

        print(f"Cluster  : {cluster}")
        print(f"Username : {data['username']}")
        print(f"Password : {data['password']}")
        print("-" * 40)
#key = load_key()

#print(key)
#print(len(key))

#cipher = Fernet(key)        