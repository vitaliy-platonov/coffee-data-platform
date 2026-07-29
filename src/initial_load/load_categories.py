
import csv
import logging

import psycopg

import logging_config

from config import INITIAL_DATA_DIR
from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_categories(file_path) -> int:
    """
    Load categories from initial CSV file into database.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        rows_loaded = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:

                cursor.execute(
                    """
                    INSERT INTO categories (
                        category_id,
                        category_name
                    )
                    VALUES (%s, %s);
                    """,
                    (
                        row[0],
                        row[1],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Categories loaded: %s",
            rows_loaded
        )

        return rows_loaded

    except psycopg.OperationalError:
        LOGGER.exception(
            "Database connection error"
        )
        return 0

    except FileNotFoundError:
        LOGGER.exception(
            "Initial categories file not found"
        )
        return 0

    finally:
        if connection:
            connection.close()


def run() -> None:
    """
    Run categories loader.
    """

    file_path = INITIAL_DATA_DIR / "categories.csv"

    load_categories(file_path)


if __name__ == "__main__":
    run()