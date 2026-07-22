"""
=========================================================
NetApp Health Dashboard
Network Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session):
    """
    Collect network port information.

    Returns
    -------
    list
    """

    logger.info("Collecting Network Information...")

    response = get(
        session,
        "/api/network/ethernet/ports"
    )

    records = response.get("records", [])

    ports = []

    for record in records:

        port = {

            "Node": (
                record.get("node") or {}
            ).get("name"),

            "Port": record.get("name"),

            "UUID": record.get("uuid"),

            "MACAddress": record.get("mac_address"),

            "MTU": record.get("mtu"),

            "Speed": (
                record.get("speed") or {}
            ).get("configured"),

            "Status": (
                record.get("state") or {}
            ).get("link"),

            "OperationalStatus": (
                record.get("state") or {}
            ).get("operational"),

            "RXErrors": (
                record.get("statistics") or {}
            ).get("receive_errors"),

            "TXErrors": (
                record.get("statistics") or {}
            ).get("transmit_errors")

        }

        ports.append(port)

    logger.info(
        f"Collected {len(ports)} network port(s)."
    )

    return ports