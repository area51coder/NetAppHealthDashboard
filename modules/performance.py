"""
=========================================================
NetApp Health Dashboard
Performance Information Collector
=========================================================
"""

from utils.logger import Logger
from core.connection import get

logger = Logger.get_logger()


def collect(session, cluster_name):
    """
    Collect cluster performance information.

    Returns
    -------
    list
    """

    logger.info("Collecting Performance Information...")

    response = get(
        session,
        "/api/cluster/nodes"
    )

    records = response.get("records", [])

    performance = []

    for record in records:

        perf = {
            "ClusterName": session.cluster_name,

            "NodeName": record.get("name"),

            "UUID": record.get("uuid"),

            "CPU": (
                record.get("cpu") or {}
            ).get("busy"),

            "Latency": None,

            "IOPS": None,

            "Throughput": None

        }

        performance.append(perf)

    logger.info(
        f"Collected performance information for {len(performance)} node(s)."
    )

    return performance