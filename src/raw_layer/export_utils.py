
import logging

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

LOGGER = logging.getLogger(__name__)


def export_table(table_name: str, output_folder: str) -> None:
    """
    Export PostgreSQL table to RAW CSV file.
    """
    conn = None
    cursor = None

    try:
        LOGGER.info(
            "Starting export: %s",
            table_name
        )

        conn = get_connection()

        LOGGER.info(
            "Connected to PostgreSQL"
        )

        cursor = conn.cursor()

        query = f"""
         SELECT *
         FROM {table_name};
         """

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = []

        for column in cursor.description:
            columns.append(column.name)

        df = pd.DataFrame(
            data=rows,
            columns=columns
        )

        output_dir = RAW_DATA_DIR / output_folder
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_dir / f"{table_name}.csv"

        LOGGER.info(
            "Exporting table: %s",
            table_name
        )

        df.to_csv(
            output_file,
            index=False
        )

        LOGGER.info(
             "Saved: %s",
            output_file
        )

    except Exception:
        LOGGER.exception(
             "Failed to export table"
        )

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

