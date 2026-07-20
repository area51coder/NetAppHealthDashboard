"""
=========================================================
NetApp Health Dashboard
Main Application
=========================================================
"""

import csv
from pathlib import Path

from core.config import load_settings
from core.inventory import load_clusters
from core.authentication import load_credentials

from core.create_credentials import encrypt_credentials


# ---------------------------------------------------------
# Check if credentials are encrypted
# ---------------------------------------------------------

def check_plaintext_password():
    """
    Returns True if any password is plain text.
    """

    credential_file = (
        Path(__file__).resolve().parent
        / "config"
        / "credentials.csv"
    )

    if not credential_file.exists():
        raise FileNotFoundError(
            f"Credential file not found : {credential_file}"
        )

    with open(
        credential_file,
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            password = row["Password"].strip()

            # Fernet encrypted passwords start with gAAAAA
            if not password.startswith("gAAAAA"):
                return True

    return False


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("        NetApp Health Dashboard")
    print("=" * 60)

    # -----------------------------------------------------
    # Auto Encrypt Credentials
    # -----------------------------------------------------

    print("\nChecking Credentials...")

    if check_plaintext_password():

        print("Plain text password detected.")
        print("Encrypting credentials...")

        encrypt_credentials()

        print("Credentials encrypted successfully.")

    else:

        print("Credentials already encrypted.")

    # -----------------------------------------------------
    # Load Settings
    # -----------------------------------------------------

    print("\nLoading Settings...")

    settings = load_settings()

    print("Settings Loaded Successfully.")

    # -----------------------------------------------------
    # Load Inventory
    # -----------------------------------------------------

    print("\nLoading Cluster Inventory...")

    clusters = load_clusters()

    print(f"Clusters Loaded : {len(clusters)}")

    # -----------------------------------------------------
    # Load Credentials
    # -----------------------------------------------------

    print("\nLoading Credentials...")

    credentials = load_credentials()

    print(f"Credentials Loaded : {len(credentials)}")

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("Cluster Summary")
    print("=" * 60)

    for cluster in clusters:

        cluster_name = cluster["ClusterName"]

        print(f"\nCluster     : {cluster_name}")
        print(f"IP Address  : {cluster['IP']}")
        print(f"Environment : {cluster['Environment']}")

        if cluster_name in credentials:

            print(
                f"Username    : "
                f"{credentials[cluster_name]['username']}"
            )

            print("Password    : ********")

        else:

            print("Username    : NOT FOUND")
            print("Password    : NOT FOUND")

    print("\n")
    print("=" * 60)
    print("Initialization Completed Successfully")
    print("=" * 60)


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()