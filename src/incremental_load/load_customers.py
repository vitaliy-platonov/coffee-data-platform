
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_incremental_customers() -> int:
    """
    Load incremental customers into database.
    """

    connection = None
    cursor = None
    rows_loaded = 0

    try:
        file_path = INCREMENTAL_DATA_DIR / "customers_increment.csv"

        connection = get_connection()

        cursor = connection.cursor()

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO customers (
                        customer_id,
                        first_name,
                        last_name,
                        phone,
                        email,
                        city,
                        registration_date
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (
                        row["customer_id"],
                        row["first_name"],
                        row["last_name"],
                        row["phone"],
                        row["email"],
                        row["city"],
                        row["registration_date"],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Incremental customers loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except Exception:
        if connection:
            connection.rollback()

        LOGGER.exception(
            "Failed to load incremental customers"
        )

        return 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def run() -> None:
    """
    Run incremental customers loader.
    """

    load_incremental_customers()


if __name__ == "__main__":
    run()