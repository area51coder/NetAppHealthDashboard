"""
=========================================================
NetApp Health Dashboard
Aggregate Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session):
    """
    Collect aggregate information.

    Returns
    -------
    list
    """

    logger.info("Collecting Aggregate Information...")

    response = get(
        session,
        "/api/storage/aggregates"
    )

    records = response.get("records", [])

    aggregates = []

    for record in records:

        block_storage = (
            record.get("space") or {}
        ).get("block_storage") or {}

        total_capacity = block_storage.get("size", 0)

        used_capacity = block_storage.get("used", 0)

        free_capacity = total_capacity - used_capacity

        if total_capacity > 0:

            used_percent = round(
                (used_capacity / total_capacity) * 100,
                2
            )

            free_percent = round(
                (free_capacity / total_capacity) * 100,
                2
            )

        else:

            used_percent = 0
            free_percent = 0

        aggregate = {

            "AggregateName": record.get("name"),

            "UUID": record.get("uuid"),

            "Node": (
                record.get("node") or {}
            ).get("name"),

            "RaidType": record.get("raid_type"),

            "TotalCapacity": total_capacity,

            "UsedCapacity": used_capacity,

            "FreeCapacity": free_capacity,

            "UsedPercent": used_percent,

            "FreePercent": free_percent,

            "State": record.get("state"),

            "Health": (
                record.get("health") or {}
            ).get("status")

        }

        aggregates.append(aggregate)

    logger.info(
        f"Collected {len(aggregates)} aggregate(s)."
    )

    return aggregates