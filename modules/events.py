"""
=========================================================
NetApp Health Dashboard
EMS Event Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session):
    """
    Collect EMS Events.

    Returns
    -------
    list
    """

    logger.info("Collecting EMS Events...")

    response = get(
        session,
        "/api/support/ems/events"
    )

    records = response.get("records", [])

    events = []

    for record in records:

        event = {

            "EventTime": record.get("time"),

            "Severity": record.get("severity"),

            "EventName": record.get("name"),

            "Message": record.get("message"),

            "Node": (
                record.get("node") or {}
            ).get("name"),

            "Source": record.get("source"),

            "Category": record.get("category")

        }

        events.append(event)

    logger.info(
        f"Collected {len(events)} EMS event(s)."
    )

    return events