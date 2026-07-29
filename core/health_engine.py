"""
=========================================================
NetApp Health Dashboard
Health Engine
=========================================================
"""

from core import rules


# =========================================================
# MAIN
# =========================================================

def evaluate(
    cluster,
    nodes,
    aggregates,
    volumes,
    disks,
    network,
    performance,
    snapmirror,
    events
):

    score = rules.MAX_SCORE

    reasons = []

    score, reasons = check_cluster(
        cluster,
        score,
        reasons
    )

    score, reasons = check_nodes(
        nodes,
        score,
        reasons
    )

    score, reasons = check_aggregates(
        aggregates,
        score,
        reasons
    )

    score, reasons = check_volumes(
        volumes,
        score,
        reasons
    )

    score, reasons = check_disks(
        disks,
        score,
        reasons
    )

    score, reasons = check_network(
        network,
        score,
        reasons
    )

    score, reasons = check_performance(
        performance,
        score,
        reasons
    )

    score, reasons = check_snapmirror(
        snapmirror,
        score,
        reasons
    )

    score, reasons = check_events(
        events,
        score,
        reasons
    )

    if score == 100:

        health = "Healthy"

    else:

        health = "Critical"

    return {

        "Score": score,

        "Health": health,

        "State": "Online",

        "Reasons": reasons

    }


# =========================================================
# CLUSTER
# =========================================================

def check_cluster(cluster, score, reasons):

    if not cluster:

        score -= rules.CLUSTER_SCORE

        reasons.append("Cluster information unavailable")

    return score, reasons


# =========================================================
# NODES
# =========================================================

def check_nodes(nodes, score, reasons):

    for node in nodes:

        cpu = float(node.get("CPU", 0))

        memory = float(node.get("Memory", 0))

        if cpu > rules.CPU_LIMIT:

            score -= 2

            reasons.append(
                f"{node['NodeName']} CPU {cpu}%"
            )

        if memory > rules.MEMORY_LIMIT:

            score -= 2

            reasons.append(
                f"{node['NodeName']} Memory {memory}%"
            )

    return score, reasons


# =========================================================
# AGGREGATES
# =========================================================

def check_aggregates(aggregates, score, reasons):

    for aggr in aggregates:

        used = float(
            aggr.get(
                "UsedPercent",
                0
            )
        )

        if used > rules.AGGREGATE_USED_LIMIT:

            score -= 2

            reasons.append(
                f"{aggr['AggregateName']} Usage {used}%"
            )

    return score, reasons


# =========================================================
# VOLUMES
# =========================================================

def check_volumes(volumes, score, reasons):

    for volume in volumes:

        used = float(
            volume.get(
                "UsedPercent",
                0
            )
        )

        if used > rules.VOLUME_USED_LIMIT:

            score -= 1

            reasons.append(
                f"{volume['Volume']} Usage {used}%"
            )

    return score, reasons


# =========================================================
# DISKS
# =========================================================

def check_disks(disks, score, reasons):

    failed = 0

    for disk in disks:

        status = str(
            disk.get(
                "Health",
                ""
            )
        ).lower()

        if "failed" in status:

            failed += 1

    if failed > rules.FAILED_DISK_ALLOWED:

        score -= 10

        reasons.append(
            f"{failed} Failed Disk(s)"
        )

    return score, reasons


# =========================================================
# NETWORK
# =========================================================

def check_network(network, score, reasons):

    return score, reasons


# =========================================================
# PERFORMANCE
# =========================================================

def check_performance(performance, score, reasons):

    return score, reasons


# =========================================================
# SNAPMIRROR
# =========================================================

def check_snapmirror(snapmirror, score, reasons):

    return score, reasons


# =========================================================
# EVENTS
# =========================================================

def check_events(events, score, reasons):

    critical = 0

    for event in events:

        sev = str(
            event.get(
                "Severity",
                ""
            )
        ).lower()

        if sev == "critical":

            critical += 1

    if critical > rules.CRITICAL_EVENT_ALLOWED:

        score -= 5

        reasons.append(
            f"{critical} Critical EMS Event(s)"
        )

    return score, reasons