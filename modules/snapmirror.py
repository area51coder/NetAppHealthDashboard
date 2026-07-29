"""
=========================================================
NetApp Health Dashboard
SnapMirror Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session, cluster_name):
    """
    Collect SnapMirror information.

    Returns
    -------
    list
    """

    logger.info("Collecting SnapMirror Information...")

    response = get(
        session,
        "/api/snapmirror/relationships"
    )

    records = response.get("records", [])

    relationships = []

    for record in records:

        relationship = {
            "ClusterName": session.cluster_name,

            "UUID": record.get("uuid"),

            "Source": (
                record.get("source") or {}
            ).get("path"),

            "Destination": (
                record.get("destination") or {}
            ).get("path"),

            "RelationshipType": record.get("type"),

            "Policy": (
                record.get("policy") or {}
            ).get("name"),

            "Healthy": record.get("healthy"),

            "TransferStatus": (
                record.get("transfer") or {}
            ).get("state"),

            "LagTime": record.get("lag_time"),

            "State": record.get("state")

        }

        relationships.append(relationship)

    logger.info(
        f"Collected {len(relationships)} SnapMirror relationship(s)."
    )

    return relationships