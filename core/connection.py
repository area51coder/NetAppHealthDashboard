"""
=========================================================
NetApp Health Dashboard
REST Connection Manager
=========================================================
"""

import urllib3
import requests
import time

from requests import Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    RequestException,
)

from utils.logger import Logger

logger = Logger.get_logger()


# ---------------------------------------------------------
# Disable SSL Warning
# ---------------------------------------------------------

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ---------------------------------------------------------
# Connect to NetApp Cluster
# ---------------------------------------------------------

def connect(cluster, credentials, settings):
    """
    Create REST session and test connectivity.

    Parameters
    ----------
    cluster : dict
        Cluster information from clusters.csv

    credentials : dict
        Username and password

    settings : dict
        Settings loaded from settings.json

    Returns
    -------
    requests.Session
    """

    ip = cluster["IP"]

    username = credentials["username"]

    password = credentials["password"]

    verify_ssl = settings.get(
        "verify_ssl",
        False
    )

    timeout = settings.get(
        "timeout",
        30
    )

    logger.info(
        f"Connecting to {cluster['ClusterName']} ({ip})"
    )

    try:

        session = Session()

        session.auth = HTTPBasicAuth(
            username,
            password
        )

        session.verify = verify_ssl

        session.headers.update({

            "Accept": "application/json",

            "Content-Type": "application/json"

        })

        # Custom attributes
        session.base_url = f"https://{ip}"

        session.timeout = timeout

        # -------------------------------------------------
        # Test Connection
        # -------------------------------------------------

        response = session.get(
            f"{session.base_url}/api/cluster",
            timeout=session.timeout
        )

        response.raise_for_status()

        cluster_info = response.json()

        logger.info(
            f"Connected Successfully : "
            f"{cluster_info.get('name','Unknown')}"
        )

        return session

    except ConnectTimeout:

        logger.error(
            f"Connection Timeout : {ip}"
        )
        raise

    except ConnectionError:

        logger.error(
            f"Unable to connect : {ip}"
        )
        raise

    except HTTPError:

        logger.error(
            f"HTTP Error : "
            f"{response.status_code}"
        )
        raise

    except RequestException as ex:

        logger.exception(ex)
        raise

    except Exception as ex:

        logger.exception(ex)
        raise

# ---------------------------------------------------------
# Get Request
# ---------------------------------------------------------
# ---------------------------------------------------------
# GET Request
# ---------------------------------------------------------

def get(session, endpoint, params=None):
    """
    Execute HTTP GET request.

    Parameters
    ----------
    session : requests.Session

    endpoint : str

        Example:
            /api/cluster

    params : dict

        Optional Query Parameters

    Returns
    -------
    dict
    """

    url = f"{session.base_url}{endpoint}"

    logger.info(f"GET : {url}")

    start_time = time.time()

    try:

        response = session.get(
            url,
            params=params,
            timeout=session.timeout
        )

        response.raise_for_status()

        elapsed = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"Status : {response.status_code}"
        )

        logger.info(
            f"Execution Time : {elapsed} sec"
        )

        if response.text.strip():

            return response.json()

        return {}

    except HTTPError:

        logger.error(
            f"HTTP Error : {response.status_code}"
        )
        raise

    except ConnectTimeout:

        logger.error(
            f"Timeout : {url}"
        )
        raise

    except ConnectionError:

        logger.error(
            f"Connection Failed : {url}"
        )
        raise

    except ValueError:

        logger.error(
            "Invalid JSON Response."
        )
        raise

    except RequestException as ex:

        logger.exception(ex)
        raise

    except Exception as ex:

        logger.exception(ex)
        raise

# ---------------------------------------------------------
# Disconnect
# ---------------------------------------------------------

def disconnect(session):
    """
    Close REST session.
    """

    try:

        session.close()

        logger.info(
            "REST Session Closed."
        )

    except Exception as ex:

        logger.exception(ex)
        raise