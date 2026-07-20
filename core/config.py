"""
=========================================================
NetApp Health Dashboard
Configuration Loader
=========================================================
"""

import json
from pathlib import Path

from utils.logger import Logger

logger = Logger.get_logger()


# ---------------------------------------------------------
# Global Configuration Cache
# ---------------------------------------------------------

_config = None


# ---------------------------------------------------------
# Load Settings
# ---------------------------------------------------------

def load_settings():
    """
    Load settings.json only once.

    Returns:
        dict
    """

    global _config

    if _config is not None:
        return _config

    try:

        project_root = Path(__file__).resolve().parents[1]

        config_file = (
            project_root /
            "config" /
            "settings.json"
        )

        logger.info(f"Loading configuration : {config_file}")

        with open(
            config_file,
            "r",
            encoding="utf-8"
        ) as file:

            _config = json.load(file)

        logger.info("Configuration loaded successfully.")

        return _config

    except FileNotFoundError:

        logger.error("settings.json not found.")
        raise

    except json.JSONDecodeError as ex:

        logger.error(f"Invalid JSON : {ex}")
        raise

    except Exception as ex:

        logger.exception(ex)
        raise


# ---------------------------------------------------------
# Get One Setting
# ---------------------------------------------------------

def get_setting(key, default=None):
    """
    Return a single configuration value.
    """

    global _config

    if _config is None:
        load_settings()

    return _config.get(key, default)


# ---------------------------------------------------------
# Get All Settings
# ---------------------------------------------------------

def get_all_settings():
    """
    Return complete configuration dictionary.
    """

    global _config

    if _config is None:
        load_settings()

    return _config


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    settings = get_all_settings()

    print("\nConfiguration Loaded\n")

    for key, value in settings.items():

        print(f"{key} : {value}")