
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_incremental_orders() -> int:
    """
    Load incremental orders into database.
    """

    connection = None
    cursor = None
    rows_loaded = 0

    try:
        file_path = (
            INCREMENTAL_DATA_DIR /
            "orders_increment.csv"
        )

        connection = get_connection()

        cursor = connection.cursor()

        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO orders (
                        order_id,
                        customer_id,
                        store_id,
                        employee_id,
                        order_date,
                        total_amount
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (
                        row["order_id"],
                        row["customer_id"],
                        row["store_id"],
                        row["employee_id"],
                        row["order_date"],
                        row["total_amount"],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Incremental orders loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except Exception:
        if connection:
            connection.rollback()

        LOGGER.exception(
            "Failed to load incremental orders"
        )

        return 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def run() -> None:
    """
    Run incremental orders loader.
    """

    load_incremental_orders()


if __name__ == "__main__":
    run()