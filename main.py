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
from core.healthcheck_manager import run

from reports.csv_writer import clear_reports
from reports.dashboard import generate_dashboard

from utils.logger import Logger

logger = Logger.get_logger()


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
    print("      NetApp Health Dashboard")
    print("=" * 60)

    try:

        # -------------------------------------------------
        # Auto Encrypt Credentials
        # -------------------------------------------------

        logger.info("Checking Credentials...")

        if check_plaintext_password():

            logger.info(
                "Plain text password detected."
            )

            encrypt_credentials()

            logger.info(
                "Credentials encrypted successfully."
            )

        else:

            logger.info(
                "Credentials already encrypted."
            )

        # -------------------------------------------------
        # Load Settings
        # -------------------------------------------------

        logger.info("Loading Settings...")

        settings = load_settings()

        # -------------------------------------------------
        # Load Inventory
        # -------------------------------------------------

        logger.info("Loading Cluster Inventory...")

        clusters = load_clusters()

        logger.info(
            f"Clusters Loaded : {len(clusters)}"
        )

        # -------------------------------------------------
        # Load Credentials
        # -------------------------------------------------

        logger.info("Loading Credentials...")

        credentials = load_credentials()

        logger.info(
            f"Credentials Loaded : {len(credentials)}"
        )

        # -------------------------------------------------
        # Clear Old Reports
        # -------------------------------------------------

        logger.info("Cleaning Old Reports...")

        clear_reports()

        # -------------------------------------------------
        # Run Health Check
        # -------------------------------------------------

        logger.info("Starting Health Check...")

        run(

            clusters,

            credentials,

            settings

        )
        print("HealthCheckManager Finished")
        # -------------------------------------------------
        # Generate Dashboard
        # -------------------------------------------------

        logger.info("Generating Dashboard...")

        dashboard = generate_dashboard()

        logger.info(
            f"Dashboard Generated : {dashboard}"
        )

        print()
        print("=" * 60)
        print("Health Check Completed Successfully")
        print("=" * 60)
        print()
        print(f"Dashboard : {dashboard}")

    except Exception as ex:

        logger.exception(ex)

        print()
        print("=" * 60)
        print("Health Check Failed")
        print("=" * 60)

        raise


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":

    main()