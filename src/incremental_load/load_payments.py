
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_incremental_payments() -> int:
    """
    Load incremental payments into database.
    """

    connection = None
    cursor = None
    rows_loaded = 0

    try:
        file_path = (
            INCREMENTAL_DATA_DIR /
            "payments_increment.csv"
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
                    INSERT INTO payments (
                        payment_id,
                        order_id,
                        payment_date,
                        payment_method,
                        amount,
                        status
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
                        row["payment_id"],
                        row["order_id"],
                        row["payment_date"],
                        row["payment_method"],
                        row["amount"],
                        row["status"],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Incremental payments loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except Exception:
        if connection:
            connection.rollback()

        LOGGER.exception(
            "Failed to load incremental payments"
        )

        return 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def run() -> None:
    """
    Run incremental payments loader.
    """

    load_incremental_payments()


if __name__ == "__main__":
    run()