"""
=========================================================
NetApp Health Dashboard
Logger Module
=========================================================
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:

    _logger = None

    @staticmethod
    def get_logger(
        logger_name="NetAppHealthDashboard",
        log_level=logging.INFO
    ):
        """
        Returns a singleton logger instance.
        """

        if Logger._logger:
            return Logger._logger

        # Project Root
        project_root = Path(__file__).resolve().parents[1]

        # Log Folder
        log_folder = project_root / "logs"
        log_folder.mkdir(exist_ok=True)

        # Log File
        log_file = log_folder / "health_dashboard.log"

        # Create Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        # Prevent duplicate handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        # Log Format
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(filename)s | %(funcName)s | Line:%(lineno)d | %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S"
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Rotating File Handler
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,   # 5 MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        Logger._logger = logger

        return logger