
from database import get_connection
import pandas as pd
from pathlib import Path
from config import RAW_DATA_DIR
import logging

from src import logger_config

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

        output_dir = RAW_DATA_DIR / output_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{table_name}.csv"
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

