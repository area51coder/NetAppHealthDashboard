from core.config import load_settings
from core.inventory import load_clusters
from core.authentication import load_credentials

from core.connection import (
    connect,
    disconnect,
    get
)

settings = load_settings()

clusters = load_clusters()

credentials = load_credentials()

cluster = clusters[0]

credential = credentials[
    cluster["ClusterName"]
]

session = connect(
    cluster,
    credential,
    settings
)

print("\nCONNECTED\n")

# ------------------------------
# Test GET Cluster
# ------------------------------

cluster_info = get(
    session,
    "/api/cluster"
)

print(cluster_info)

disconnect(session)