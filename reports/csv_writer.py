"""
=========================================================
NetApp Health Dashboard
CSV Report Writer
=========================================================
"""

import csv
from pathlib import Path

from utils.logger import Logger

logger = Logger.get_logger()

# ---------------------------------------------------------
# Output Directory
# ---------------------------------------------------------

OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "reports_output"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)

# ---------------------------------------------------------
# Write CSV
# ---------------------------------------------------------

def write_csv(filename, data, append=False):
    """
    Write dictionary/list data to CSV.

    Parameters
    ----------
    filename : str

    data : dict | list

    append : bool

        False = Create new file

        True = Append data
    """

    filepath = OUTPUT_DIR / filename

    # ---------------------------------------------
    # Convert dictionary into list
    # ---------------------------------------------

    if isinstance(data, dict):

        data = [data]

    if not data:

        logger.info(
            f"No data available for {filename}. Creating blank CSV."
        )

        data = [
            {
                "Status": "No Data Available"
            }
        ]

    # ---------------------------------------------
    # Write Mode
    # ---------------------------------------------

    mode = "a" if append else "w"

    file_exists = filepath.exists()

    # ---------------------------------------------
    # Open File
    # ---------------------------------------------

    with open(

        filepath,

        mode,

        newline="",

        encoding="utf-8-sig"

    ) as file:

        writer = csv.DictWriter(

            file,

            fieldnames=data[0].keys(),

            extrasaction="ignore"

        )

        # -----------------------------------------
        # Write Header
        # -----------------------------------------

        if (

            not append

            or

            not file_exists

            or

            filepath.stat().st_size == 0

        ):

            writer.writeheader()

        # -----------------------------------------
        # Write Rows
        # -----------------------------------------

        writer.writerows(data)

    logger.info(

        f"{filename} updated "

        f"({len(data)} records)"

    )

    return filepath


# ---------------------------------------------------------
# Delete Old Reports
# ---------------------------------------------------------

def clear_reports():
    """
    Delete old CSV and HTML reports
    before every execution.
    """

    if not OUTPUT_DIR.exists():

        return

    deleted = 0

    for file in OUTPUT_DIR.iterdir():

        if file.suffix.lower() in [

            ".csv",

            ".html",

            ".json"

        ]:

            try:

                file.unlink()

                deleted += 1

            except Exception as ex:

                logger.exception(ex)

    logger.info(

        f"Old reports removed : {deleted}"

    )