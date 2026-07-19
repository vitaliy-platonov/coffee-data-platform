
from database import get_connection
import os
import pandas as pd
import logging

from src import logger_config

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


def export_table(table_name: str, output_folder: str) -> None:
    conn = None
    cursor = None

    try:
        logging.info(f"Starting export: {table_name}")
        conn = get_connection()
        logging.info(f"Connected to PostgreSQL")
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)

        rows = cursor.fetchall()

        columns = []

        for column in cursor.description:
            columns.append(column.name)

        df = pd.DataFrame(
            data=rows,
            columns=columns
        )

        output_dir = os.path.join(
            project_root,
            "data",
            "raw",
            output_folder
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        output_file = os.path.join(
            output_dir,
            f"{table_name}.csv"
        )
        logging.info(f"Exporting table: {table_name}")

        df.to_csv(
            output_file,
            index=False
        )
        logging.info(f"Saved: {output_file}")

    except Exception as error:
        logging.error(f"Export failed: {error}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

