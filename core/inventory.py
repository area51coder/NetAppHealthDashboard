"""
=========================================================
Inventory Module
Reads NetApp Cluster Inventory
=========================================================
"""

import csv
from pathlib import Path


CLUSTER_FILE = Path("config") / "clusters.csv"


def load_clusters():
    """
    Read cluster inventory from CSV.

    Returns:
        list: List of cluster dictionaries
    """

    if not CLUSTER_FILE.exists():
        raise FileNotFoundError(
            f"Cluster inventory not found: {CLUSTER_FILE}"
        )

    clusters = []

    with open(CLUSTER_FILE, mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        required_columns = [
            "ClusterName",
            "IP",
            "Environment"
        ]

        # Validate required columns
        for column in required_columns:
            if column not in reader.fieldnames:
                raise ValueError(
                    f"Missing required column: {column}"
                )

        # Read rows
        for row in reader:

            clusters.append({
                "ClusterName": row["ClusterName"].strip(),
                "IP": row["IP"].strip(),
                "Environment": row["Environment"].strip()
            })

    return clusters


if __name__ == "__main__":

    cluster_list = load_clusters()

    print("\nNetApp Cluster Inventory\n")

    for cluster in cluster_list:
        print(cluster)