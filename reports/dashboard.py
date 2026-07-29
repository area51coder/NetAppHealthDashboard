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


# =========================================================
# Project Paths
# =========================================================

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


# =========================================================
# Read CSV
# =========================================================

def read_csv(filename):
    """
    Safely read CSV.

    Returns empty dataframe
    if file is missing.
    """

    file = REPORT_DIR / filename

    if not file.exists():

        logger.info(
            f"{filename} not found."
        )

        return pd.DataFrame()

    try:

        return pd.read_csv(file)

    except Exception as ex:

        logger.exception(ex)

        return pd.DataFrame()


# =========================================================
# Format Size
# =========================================================

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

    while size >= 1024 and index < len(units)-1:

        size /= 1024

        index += 1

    return f"{size:.2f} {units[index]}"


# =========================================================
# Health Color
# =========================================================

def health_color(status):

    if pd.isna(status):

        return "gray"

    status = str(status).strip().lower()

    if status in (

        "healthy",
        "ok",
        "online",
        "true"

    ):

        return "green"

    elif status in (

        "warning",
        "degraded"

    ):

        return "yellow"

    elif status in (

        "critical",
        "failed",
        "offline",
        "false"

    ):

        return "red"

    return "gray"


# =========================================================
# Health Badge
# =========================================================

def health_badge(status):

    color = health_color(status)

    return f"""

    <span class="badge {color}">
        {status}
    </span>

    """


# =========================================================
# Safe Value
# =========================================================

def safe(value):

    if pd.isna(value):

        return "-"

    return value


# =========================================================
# DataFrame to Records
# =========================================================

def records(df):

    if df.empty:

        return []

    return df.fillna("").to_dict(
        orient="records"
    )


# =========================================================
# Overall Health Score
# =========================================================

def calculate_health_score(cluster_df):

    if cluster_df.empty:

        return 0

    healthy = 0

    total = len(cluster_df)

    for _, row in cluster_df.iterrows():

        if str(

            row.get(
                "Health",
                ""
            )

        ).lower() == "healthy":

            healthy += 1

    return round(

        (healthy / total) * 100,

        1

    )


# =========================================================
# Summary Cards
# =========================================================

def build_summary(

    cluster_df,

    node_df,

    aggregate_df,

    volume_df,

    disk_df,

    network_df,

    snapmirror_df,

    events_df

):

    return {

        "clusters": len(cluster_df),

        "nodes": len(node_df),

        "aggregates": len(aggregate_df),

        "volumes": len(volume_df),

        "disks": len(disk_df),

        "ports": len(network_df),

        "snapmirror": len(snapmirror_df),

        "events": len(events_df)

    }


# =========================================================
# Capacity Summary
# =========================================================

def build_capacity(aggregate_df):

    total = 0

    used = 0

    free = 0

    percent = 0

    if not aggregate_df.empty:

        if "TotalCapacity" in aggregate_df.columns:

            total = aggregate_df[
                "TotalCapacity"
            ].sum()

        if "UsedCapacity" in aggregate_df.columns:

            used = aggregate_df[
                "UsedCapacity"
            ].sum()

        free = total - used

        if total > 0:

            percent = round(

                used / total * 100,

                2

            )

    return {

        "total":

            format_size(total),

        "used":

            format_size(used),

        "free":

            format_size(free),

        "used_percent":

            percent

    }
# =========================================================
# Cluster Section
# =========================================================

def build_cluster_table(cluster_df):

    table = []

    if cluster_df.empty:
        return table

    for _, row in cluster_df.iterrows():

        table.append({

            "ClusterName": safe(row.get("ClusterName")),

            "Version": safe(row.get("Version")),

            "ManagementIP": safe(row.get("ManagementIP")),

            "Location": safe(row.get("Location")),

            "Contact": safe(row.get("Contact")),

            "Timezone": safe(row.get("Timezone")),

            "State": safe(row.get("State")),

            "Health": safe(row.get("Health")),

            "HealthColor": health_color(
                row.get("Health")
            )

        })

    return table


# =========================================================
# Node Section
# =========================================================

def build_node_table(node_df):

    table = []

    if node_df.empty:
        return table

    for _, row in node_df.iterrows():

        table.append({

            "Node": safe(row.get("Node")),

            "Model": safe(row.get("Model")),

            "Serial": safe(row.get("Serial")),

            "CPU": safe(row.get("CPU")),

            "Memory": safe(row.get("Memory")),

            "Uptime": safe(row.get("Uptime")),

            "Health": safe(row.get("Health")),

            "HealthColor": health_color(
                row.get("Health")
            )

        })

    return table


# =========================================================
# Aggregate Section
# =========================================================

def build_aggregate_table(aggregate_df):

    table = []

    if aggregate_df.empty:
        return table

    for _, row in aggregate_df.iterrows():

        total = row.get("TotalCapacity", 0)

        used = row.get("UsedCapacity", 0)

        free = row.get("FreeCapacity", 0)

        usage = row.get("UsagePercent", "-")

        table.append({

            "Aggregate": safe(row.get("Aggregate")),

            "Raid": safe(row.get("Raid")),

            "State": safe(row.get("State")),

            "TotalCapacity": format_size(total),

            "UsedCapacity": format_size(used),

            "FreeCapacity": format_size(free),

            "UsagePercent": usage

        })

    return table


# =========================================================
# Volume Section
# =========================================================

def build_volume_table(volume_df):

    table = []

    if volume_df.empty:
        return table

    for _, row in volume_df.iterrows():

        total = row.get("TotalSize", 0)

        used = row.get("UsedSize", 0)

        available = row.get("AvailableSize", 0)

        table.append({

            "Volume": safe(row.get("Volume")),

            "SVM": safe(row.get("SVM")),

            "State": safe(row.get("State")),

            "TotalSize": format_size(total),

            "UsedSize": format_size(used),

            "AvailableSize": format_size(available),

            "SnapshotReserve": safe(
                row.get("SnapshotReserve")
            ),

            "Usage": safe(
                row.get("Usage")
            )

        })

    return table


# =========================================================
# Cluster Health Counts
# =========================================================

def build_cluster_health(cluster_df):

    result = {

        "healthy": 0,

        "warning": 0,

        "critical": 0,

        "unknown": 0

    }

    if cluster_df.empty:
        return result

    for status in cluster_df["Health"]:

        color = health_color(status)

        if color == "green":

            result["healthy"] += 1

        elif color == "yellow":

            result["warning"] += 1

        elif color == "red":

            result["critical"] += 1

        else:

            result["unknown"] += 1

    return result


# =========================================================
# Executive Summary
# =========================================================

def build_executive_summary(

        cluster_df,

        node_df,

        aggregate_df,

        volume_df,

        disk_df,

        events_df

):

    return {

        "HealthScore": calculate_health_score(
            cluster_df
        ),

        "ClusterHealth": build_cluster_health(
            cluster_df
        ),

        "Clusters": len(cluster_df),

        "Nodes": len(node_df),

        "Aggregates": len(aggregate_df),

        "Volumes": len(volume_df),

        "Disks": len(disk_df),

        "Events": len(events_df)

    }
# =========================================================
# Disk Section
# =========================================================

def build_disk_table(disk_df):

    table = []

    if disk_df.empty:
        return table

    for _, row in disk_df.iterrows():

        table.append({

            "Node": safe(row.get("Node")),

            "Disk": safe(row.get("Disk")),

            "ContainerType": safe(row.get("ContainerType")),

            "State": safe(row.get("State")),

            "Type": safe(row.get("Type")),

            "RPM": safe(row.get("RPM")),

            "Health": safe(row.get("Health")),

            "HealthColor": health_color(
                row.get("Health")
            )

        })

    return table


# =========================================================
# Network Section
# =========================================================

def build_network_table(network_df):

    table = []

    if network_df.empty:
        return table

    for _, row in network_df.iterrows():

        table.append({

            "Node": safe(row.get("Node")),

            "Port": safe(row.get("Port")),

            "LIF": safe(row.get("LIF")),

            "Status": safe(row.get("Status")),

            "Speed": safe(row.get("Speed")),

            "Errors": safe(row.get("Errors")),

            "HealthColor": health_color(
                row.get("Status")
            )

        })

    return table


# =========================================================
# Performance Section
# =========================================================

def build_performance_table(performance_df):

    table = []

    if performance_df.empty:
        return table

    for _, row in performance_df.iterrows():

        table.append({

            "Object": safe(row.get("Object")),

            "CPU": safe(row.get("CPU")),

            "Latency": safe(row.get("Latency")),

            "IOPS": safe(row.get("IOPS")),

            "Throughput": safe(row.get("Throughput"))

        })

    return table


# =========================================================
# SnapMirror Section
# =========================================================

def build_snapmirror_table(snap_df):

    table = []

    if snap_df.empty:
        return table

    for _, row in snap_df.iterrows():

        table.append({

            "Source": safe(row.get("Source")),

            "Destination": safe(row.get("Destination")),

            "Lag": safe(row.get("Lag")),

            "Healthy": safe(row.get("Healthy")),

            "TransferStatus": safe(
                row.get("TransferStatus")
            ),

            "HealthColor": health_color(
                row.get("Healthy")
            )

        })

    return table


# =========================================================
# Events Section
# =========================================================

def build_events_table(events_df):

    table = []

    if events_df.empty:
        return table

    for _, row in events_df.iterrows():

        severity = safe(
            row.get("Severity")
        )

        table.append({

            "Time": safe(row.get("Time")),

            "Node": safe(row.get("Node")),

            "Severity": severity,

            "Message": safe(row.get("Message")),

            "Color": health_color(severity)

        })

    return table


# =========================================================
# Capacity Chart
# =========================================================

def build_capacity_chart(capacity):

    return {

        "labels": [

            "Used",

            "Free"

        ],

        "values": [

            capacity["used_percent"],

            round(

                100 -

                capacity["used_percent"],

                2

            )

        ]

    }


# =========================================================
# Cluster Health Chart
# =========================================================

def build_cluster_chart(cluster_df):

    healthy = 0

    warning = 0

    critical = 0

    unknown = 0

    if not cluster_df.empty:

        for status in cluster_df["Health"]:

            color = health_color(status)

            if color == "green":

                healthy += 1

            elif color == "yellow":

                warning += 1

            elif color == "red":

                critical += 1

            else:

                unknown += 1

    return {

        "labels": [

            "Healthy",

            "Warning",

            "Critical",

            "Unknown"

        ],

        "values": [

            healthy,

            warning,

            critical,

            unknown

        ]

    }


# =========================================================
# Event Severity Chart
# =========================================================

def build_event_chart(events_df):

    critical = 0

    warning = 0

    info = 0

    if not events_df.empty:

        for severity in events_df["Severity"]:

            value = str(severity).lower()

            if value == "critical":

                critical += 1

            elif value == "warning":

                warning += 1

            else:

                info += 1

    return {

        "labels": [

            "Critical",

            "Warning",

            "Information"

        ],

        "values": [

            critical,

            warning,

            info

        ]

    }


# =========================================================
# Performance Chart
# =========================================================

def build_performance_chart(performance_df):

    labels = []

    cpu = []

    latency = []

    if performance_df.empty:

        return {

            "labels": [],

            "cpu": [],

            "latency": []

        }

    for _, row in performance_df.iterrows():

        labels.append(

            safe(row.get("Object"))

        )

        cpu.append(

            row.get("CPU", 0)

        )

        latency.append(

            row.get("Latency", 0)

        )

    return {

        "labels": labels,

        "cpu": cpu,

        "latency": latency

    }

# =========================================================
# Dashboard Generator
# =========================================================

def generate_dashboard():

    logger.info(
        "Generating Dashboard..."
    )

    # -----------------------------------------------------
    # Read CSV Reports
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Executive Summary
    # -----------------------------------------------------

    summary = build_summary(

        cluster_df,

        node_df,

        aggregate_df,

        volume_df,

        disk_df,

        network_df,

        snapmirror_df,

        events_df

    )

    executive = build_executive_summary(

        cluster_df,

        node_df,

        aggregate_df,

        volume_df,

        disk_df,

        events_df

    )

    capacity = build_capacity(
        aggregate_df
    )

    health_score = calculate_health_score(
        cluster_df
    )

    cluster_health = build_cluster_health(
        cluster_df
    )

    # -----------------------------------------------------
    # Tables
    # -----------------------------------------------------

    cluster_table = build_cluster_table(
        cluster_df
    )

    node_table = build_node_table(
        node_df
    )

    aggregate_table = build_aggregate_table(
        aggregate_df
    )

    volume_table = build_volume_table(
        volume_df
    )

    disk_table = build_disk_table(
        disk_df
    )

    network_table = build_network_table(
        network_df
    )

    performance_table = build_performance_table(
        performance_df
    )

    snapmirror_table = build_snapmirror_table(
        snapmirror_df
    )

    events_table = build_events_table(
        events_df
    )

    # -----------------------------------------------------
    # Charts
    # -----------------------------------------------------

    capacity_chart = build_capacity_chart(
        capacity
    )

    cluster_chart = build_cluster_chart(
        cluster_df
    )

    event_chart = build_event_chart(
        events_df
    )

    performance_chart = build_performance_chart(
        performance_df
    )

    logger.info(
        "Dashboard Data Prepared Successfully."
    )
    # -----------------------------------------------------
    # Load Jinja Template
    # -----------------------------------------------------

    env = Environment(

        loader=FileSystemLoader(

            TEMPLATE_DIR

        ),

        autoescape=True

    )

    template = env.get_template(

        "dashboard.html"

    )

    # -----------------------------------------------------
    # Render HTML
    # -----------------------------------------------------

    html = template.render(

        generated=datetime.now().strftime(

            "%d-%b-%Y %H:%M:%S"

        ),

        # Summary
        summary=summary,

        executive=executive,

        health_score=health_score,

        cluster_health=cluster_health,

        capacity=capacity,

        # Tables
        cluster_table=cluster_table,

        node_table=node_table,

        aggregate_table=aggregate_table,

        volume_table=volume_table,

        disk_table=disk_table,

        network_table=network_table,

        performance_table=performance_table,

        snapmirror_table=snapmirror_table,

        events_table=events_table,

        # Charts
        capacity_chart=capacity_chart,

        cluster_chart=cluster_chart,

        event_chart=event_chart,

        performance_chart=performance_chart

    )

    # -----------------------------------------------------
    # Create Output Folder
    # -----------------------------------------------------

    REPORT_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    # -----------------------------------------------------
    # Write HTML Report
    # -----------------------------------------------------

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(

            html

        )

    # -----------------------------------------------------
    # Logging
    # -----------------------------------------------------

    logger.info(

        f"Dashboard Generated : {OUTPUT_FILE}"

    )

    logger.info(

        f"Clusters      : {summary['clusters']}"

    )

    logger.info(

        f"Nodes         : {summary['nodes']}"

    )

    logger.info(

        f"Aggregates    : {summary['aggregates']}"

    )

    logger.info(

        f"Volumes       : {summary['volumes']}"

    )

    logger.info(

        f"Disks         : {summary['disks']}"

    )

    logger.info(

        f"Ports         : {summary['ports']}"

    )

    logger.info(

        f"SnapMirror    : {summary['snapmirror']}"

    )

    logger.info(

        f"Events        : {summary['events']}"

    )

    logger.info(

        f"Health Score  : {health_score}%"

    )

    return OUTPUT_FILE    