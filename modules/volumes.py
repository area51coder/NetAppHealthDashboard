"""
=========================================================
NetApp Health Dashboard
Volume Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session, cluster_name):
    """
    Collect volume information.

    Returns
    -------
    list
    """

    logger.info("Collecting Volume Information...")

    response = get(
        session,
        "/api/storage/volumes"
    )

    records = response.get("records", [])

    volumes = []

    for record in records:

        space = record.get("space") or {}

        total_capacity = space.get("size", 0)

        used_capacity = space.get("used", 0)

        available_capacity = space.get("available", 0)

        snapshot = space.get("snapshot") or {}

        if total_capacity > 0:

            used_percent = round(
                (used_capacity / total_capacity) * 100,
                2
            )

        else:

            used_percent = 0

        volume = {
            "ClusterName": session.cluster_name,

            "VolumeName": record.get("name"),

            "UUID": record.get("uuid"),

            "SVM": (
                record.get("svm") or {}
            ).get("name"),

            "Aggregate": (
                record.get("aggregates") or [{}]
            )[0].get("name"),

            "TotalCapacity": total_capacity,

            "UsedCapacity": used_capacity,

            "AvailableCapacity": available_capacity,

            "UsedPercent": used_percent,

            "SnapshotReserve": snapshot.get("reserve_percent"),

            "SnapshotUsed": snapshot.get("used"),

            "State": record.get("state"),

            "Style": record.get("style"),

            "Type": record.get("type")

        }

        volumes.append(volume)

    logger.info(
        f"Collected {len(volumes)} volume(s)."
    )

    return volumes