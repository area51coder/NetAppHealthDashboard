"""
=========================================================
NetApp Health Dashboard
Disk Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session):
    """
    Collect disk information.

    Returns
    -------
    list
    """

    logger.info("Collecting Disk Information...")

    response = get(
        session,
        "/api/storage/disks"
    )

    records = response.get("records", [])

    disks = []

    for record in records:

        state = (
            record.get("state") or ""
        ).lower()

        container = (
            record.get("container_type") or ""
        )

        failed = (
            state == "failed"
        )

        spare = (
            container.lower() == "spare"
        )

        reconstructing = (
            state == "reconstructing"
        )

        disk = {

            "DiskName": record.get("name"),

            "UUID": record.get("uuid"),

            "Node": (
                record.get("owner") or {}
            ).get("name"),

            "DiskType": record.get("type"),

            "ContainerType": container,

            "Health": (
                record.get("health") or {}
            ).get("status"),

            "State": record.get("state"),

            "Failed": failed,

            "Spare": spare,

            "Reconstructing": reconstructing

        }

        disks.append(disk)

    logger.info(
        f"Collected {len(disks)} disk(s)."
    )

    return disks