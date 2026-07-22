"""
=========================================================
NetApp Health Dashboard
Node Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session):
    """
    Collect node information.

    Returns
    -------
    list
    """

    logger.info("Collecting Node Information...")

    response = get(
        session,
        "/api/cluster/nodes"
    )

    records = response.get("records", [])

    nodes = []

    for record in records:

        node = {

            "NodeName": record.get("name"),

            "UUID": record.get("uuid"),

            "Model": (
                record.get("model") or {}
            ).get("name"),

            "SerialNumber": record.get("serial_number"),

            "Version": (
                record.get("version") or {}
            ).get("full"),

            "CPU": (
                record.get("cpu") or {}
            ).get("busy"),

            "Memory": (
                record.get("memory") or {}
            ).get("used"),

            "Health": (
                record.get("health") or {}
            ).get("status"),

            "State": record.get("state"),

            "Uptime": record.get("uptime")

        }

        nodes.append(node)

    logger.info(
        f"Collected {len(nodes)} node(s)."
    )

    return nodes