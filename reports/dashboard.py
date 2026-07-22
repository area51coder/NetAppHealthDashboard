"""
=========================================================
NetApp Health Dashboard
Dashboard Generator
=========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

from jinja2 import (
    Environment,
    FileSystemLoader
)

from utils.logger import Logger

logger = Logger.get_logger()

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPORT_DIR = PROJECT_ROOT / "reports_output"

TEMPLATE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "templates"
)

OUTPUT_FILE = (
    REPORT_DIR
    / "HealthReport.html"
)


# ----------------------------------------------------------
# Read CSV
# ----------------------------------------------------------

def read_csv(filename):
    """
    Read CSV safely.
    """

    file = REPORT_DIR / filename

    if not file.exists():

        logger.warning(
            f"{filename} not found."
        )

        return pd.DataFrame()

    return pd.read_csv(file)


# ----------------------------------------------------------
# Capacity Formatter
# ----------------------------------------------------------

def format_size(size):

    try:

        size = float(size)

    except Exception:

        return "-"

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
        "PB"
    ]

    index = 0

    while size >= 1024 and index < len(units) - 1:

        size /= 1024

        index += 1

    return f"{size:.2f} {units[index]}"


# ----------------------------------------------------------
# Health Color
# ----------------------------------------------------------

def health_color(status):
    """
    Return HTML color based on health status.
    """

    # Handle blank / NaN / None values
    if status is None:
        return "#9E9E9E"

    status = str(status).strip()

    if status == "" or status.lower() == "nan":
        return "#9E9E9E"

    status = status.lower()

    if status in ("healthy", "ok", "true", "online"):
        return "#4CAF50"      # Green

    elif status in ("warning", "degraded"):
        return "#FFC107"      # Yellow

    elif status in ("critical", "failed", "offline", "false"):
        return "#F44336"      # Red

    return "#9E9E9E"
# ----------------------------------------------------------
# Dashboard Generator
# ----------------------------------------------------------

def generate_dashboard():

    logger.info(
        "Generating Dashboard..."
    )

    # ------------------------------------------------------

    cluster_df = read_csv(
        "Cluster.csv"
    )

    node_df = read_csv(
        "Nodes.csv"
    )

    aggregate_df = read_csv(
        "Aggregates.csv"
    )

    volume_df = read_csv(
        "Volumes.csv"
    )

    disk_df = read_csv(
        "Disks.csv"
    )

    network_df = read_csv(
        "Network.csv"
    )

    performance_df = read_csv(
        "Performance.csv"
    )

    snapmirror_df = read_csv(
        "SnapMirror.csv"
    )

    events_df = read_csv(
        "Events.csv"
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary = {

        "clusters": len(cluster_df),

        "nodes": len(node_df),

        "aggregates": len(aggregate_df),

        "volumes": len(volume_df),

        "disks": len(disk_df),

        "ports": len(network_df),

        "snapmirror": len(snapmirror_df),

        "events": len(events_df)

    }

    # ------------------------------------------------------
    # Capacity
    # ------------------------------------------------------

    total_capacity = 0
    used_capacity = 0

    if not aggregate_df.empty:

        total_capacity = (
            aggregate_df[
                "TotalCapacity"
            ].sum()
        )

        used_capacity = (
            aggregate_df[
                "UsedCapacity"
            ].sum()
        )

    free_capacity = (
        total_capacity -
        used_capacity
    )

    if total_capacity > 0:

        used_percent = round(

            (
                used_capacity
                / total_capacity
            ) * 100,

            2

        )

    else:

        used_percent = 0

    capacity = {

        "total":

            format_size(
                total_capacity
            ),

        "used":

            format_size(
                used_capacity
            ),

        "free":

            format_size(
                free_capacity
            ),

        "used_percent":

            used_percent

    }

    # ------------------------------------------------------
    # Cluster Table
    # ------------------------------------------------------

    cluster_table = []

    if not cluster_df.empty:

        for _, row in cluster_df.iterrows():

            cluster_table.append(

                {

                    "Cluster":

                        row.get(
                            "ClusterName",
                            "-"
                        ),

                    "Version":

                        row.get(
                            "Version",
                            "-"
                        ),

                    "Health":

                        row.get(
                            "Health",
                            "-"
                        ),

                    "State":

                        row.get(
                            "State",
                            "-"
                        ),

                    "IP":

                        row.get(
                            "ManagementIP",
                            "-"
                        ),

                    "HealthColor":

                        health_color(

                            row.get(
                                "Health",
                                ""
                            )

                        )

                }

            )

    # ------------------------------------------------------
    # Jinja
    # ------------------------------------------------------

    env = Environment(

        loader=FileSystemLoader(

            TEMPLATE_DIR

        )

    )

    template = env.get_template(

        "dashboard.html"

    )

    html = template.render(

        generated=datetime.now().strftime(

            "%d-%b-%Y %H:%M:%S"

        ),

        summary=summary,

        capacity=capacity,

        cluster_table=cluster_table

    )

    REPORT_DIR.mkdir(

        exist_ok=True

    )

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(

            html

        )

    logger.info(

        f"Dashboard Generated : {OUTPUT_FILE}"

    )

    return OUTPUT_FILE