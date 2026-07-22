"""
=========================================================
NetApp Health Dashboard
Historical Report Manager
=========================================================
"""

from pathlib import Path
from datetime import datetime

from utils.logger import Logger

logger = Logger.get_logger()


class ReportManager:


    def __init__(self):

        project_root = Path(__file__).resolve().parents[1]

        self.base_path = (
            project_root /
            "reports_output" /
            "historical"
        )

        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )


    def get_daily_folder(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        path = (
            self.base_path /
            "daily" /
            today
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path



    def get_weekly_folder(self):

        year, week, _ = datetime.now().isocalendar()

        folder_name = (
            f"{year}-W{week}"
        )

        path = (
            self.base_path /
            "weekly" /
            folder_name
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path



    def get_monthly_folder(self):

        folder_name = datetime.now().strftime(
            "%Y-%m"
        )

        path = (
            self.base_path /
            "monthly" /
            folder_name
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path



    def save_report(
            self,
            report_name,
            content,
            report_type="daily"
    ):

        if report_type == "daily":

            folder = self.get_daily_folder()

        elif report_type == "weekly":

            folder = self.get_weekly_folder()

        elif report_type == "monthly":

            folder = self.get_monthly_folder()

        else:

            raise ValueError(
                "Invalid report type"
            )


        file_path = (
            folder /
            report_name
        )


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)


        logger.info(
            f"Report saved : {file_path}"
        )


        return file_path