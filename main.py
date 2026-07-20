"""
=========================================================
NetApp Health Dashboard
Main Application
=========================================================
"""

from core.config import load_settings
from core.inventory import load_clusters
from core.authentication import load_credentials


def main():

    print("=" * 60)
    print("      NetApp Health Dashboard")
    print("=" * 60)

    # -----------------------------------
    # Load Settings
    # -----------------------------------

    print("\nLoading Settings...")

    settings = load_settings()

    print("Settings Loaded Successfully.")

    # -----------------------------------
    # Load Cluster Inventory
    # -----------------------------------

    print("\nLoading Cluster Inventory...")

    clusters = load_clusters()

    print(f"Clusters Loaded : {len(clusters)}")

    # -----------------------------------
    # Load Credentials
    # -----------------------------------

    print("\nLoading Credentials...")

    credentials = load_credentials()

    print(f"Credentials Loaded : {len(credentials)}")

    # -----------------------------------
    # Display Summary
    # -----------------------------------

    print("\n")
    print("=" * 60)
    print("Cluster Summary")
    print("=" * 60)

    for cluster in clusters:

        cluster_name = cluster["ClusterName"]

        print(f"\nCluster      : {cluster_name}")
        print(f"IP Address   : {cluster['IP']}")
        print(f"Environment  : {cluster['Environment']}")

        if cluster_name in credentials:

            print(f"Username     : {credentials[cluster_name]['username']}")
            print("Password     : ********")

        else:

            print("Username     : NOT FOUND")
            print("Password     : NOT FOUND")

    print("\n")
    print("=" * 60)
    print("Initialization Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()