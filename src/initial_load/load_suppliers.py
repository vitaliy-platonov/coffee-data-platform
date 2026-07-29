
import csv
import logging

import psycopg

import logging_config

from config import INITIAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_suppliers(file_path) -> int:
    """
    Load suppliers from initial CSV file into database.
    """

    connection = None
    rows_loaded = 0

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO suppliers (
                        supplier_id,
                        supplier_name,
                        is_active
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (
                        row[0],
                        row[1],
                        row[2],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Suppliers loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except psycopg.OperationalError:
        LOGGER.exception(
            "Database connection error"
        )

        return 0

    except FileNotFoundError:
        LOGGER.exception(
            "Initial suppliers file not found"
        )

        return 0

    finally:
        if connection:
            connection.close()


def run() -> None:
    """
    Run suppliers loader.
    """

    file_path = INITIAL_DATA_DIR / "suppliers.csv"

    load_suppliers(file_path)


if __name__ == "__main__":
    run()