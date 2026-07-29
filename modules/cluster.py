"""
=========================================================
NetApp Health Dashboard
Cluster Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session, cluster_name):
    """
    Collect cluster information.

    Returns
    -------
    dict
    """

    logger.info("Collecting Cluster Information...")

    response = get(
        session,
        "/api/cluster"
    )

    cluster = {

        "ClusterName": response.get("name"),

        "UUID": response.get("uuid"),

        "Version": (
            response.get("version") or {}
        ).get("full"),

        "Location": response.get("location"),

        "Contact": response.get("contact"),

        "Timezone": (
            response.get("timezone") or {}
        ).get("name"),

        "ManagementIP": (
            response.get("management_interfaces") or [{}]
        )[0].get("ip", {}).get("address"),

        "Health": (
            response.get("health") or {}
        ).get("status"),

        "State": response.get("state")

    }

    logger.info("Cluster Information Collected.")

    return cluster