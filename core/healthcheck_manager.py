"""
=========================================================
NetApp Health Dashboard
Health Check Manager
=========================================================
"""

from utils.logger import Logger

from core.connection import connect
from core.connection import disconnect

from modules.cluster import collect as collect_cluster
from modules.nodes import collect as collect_nodes
from modules.aggregates import collect as collect_aggregates
from modules.volumes import collect as collect_volumes
from modules.disks import collect as collect_disks
from modules.network import collect as collect_network
from modules.performance import collect as collect_performance
from modules.snapmirror import collect as collect_snapmirror
from modules.events import collect as collect_events

from reports.csv_writer import write_csv

logger = Logger.get_logger()


def run(clusters, credentials, settings):
    """
    Execute Health Check for all clusters.

    Parameters
    ----------
    clusters : list

    credentials : dict

    settings : dict

    Returns
    -------
    dict
    """

    logger.info("Starting Health Check Manager...")

    all_results = {}

    for cluster in clusters:

        cluster_name = cluster["ClusterName"]

        logger.info(
            f"Processing Cluster : {cluster_name}"
        )

        if cluster_name not in credentials:

            logger.warning(
                f"Credentials not found for {cluster_name}"
            )

            continue

        session = None

        try:

            session = connect(
                cluster,
                credentials[cluster_name],
                settings
            )

            cluster_results = {

                "Cluster": collect_cluster(session),

                "Nodes": collect_nodes(session),

                "Aggregates": collect_aggregates(session),

                "Volumes": collect_volumes(session),

                "Disks": collect_disks(session),

                "Network": collect_network(session),

                "Performance": collect_performance(session),

                "SnapMirror": collect_snapmirror(session),

                "Events": collect_events(session)

            }

            # -------------------------------------------------
            # Generate CSV Reports
            # -------------------------------------------------

            write_csv(
                "Cluster.csv",
                cluster_results["Cluster"],
                append=True
            )

            write_csv(
                "Nodes.csv",
                cluster_results["Nodes"],
                append=True
            )

            write_csv(
                "Aggregates.csv",
                cluster_results["Aggregates"],
                append=True
            )

            write_csv(
                "Volumes.csv",
                cluster_results["Volumes"],
                append=True
            )

            write_csv(
                "Disks.csv",
                cluster_results["Disks"],
                append=True
            )

            write_csv(
                "Network.csv",
                cluster_results["Network"],
                append=True
            )

            write_csv(
                "Performance.csv",
                cluster_results["Performance"],
                append=True
            )

            write_csv(
                "SnapMirror.csv",
                cluster_results["SnapMirror"],
                append=True
            )

            write_csv(
                "Events.csv",
                cluster_results["Events"],
                append=True
            )

            all_results[cluster_name] = cluster_results

            logger.info(
                f"{cluster_name} Health Check Completed."
            )

        except Exception as ex:

            logger.exception(ex)

        finally:

            if session:

                disconnect(session)

    logger.info("Health Check Manager Finished.")

    return all_results