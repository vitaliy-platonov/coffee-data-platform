
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_incremental_order_items() -> int:
    """
    Load incremental order items into database.
    """

    connection = None
    cursor = None
    rows_loaded = 0

    try:
        file_path = (
            INCREMENTAL_DATA_DIR /
            "order_items_increment.csv"
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
                    INSERT INTO order_items (
                        order_item_id,
                        order_id,
                        product_id,
                        quantity,
                        price
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (
                        row["order_item_id"],
                        row["order_id"],
                        row["product_id"],
                        row["quantity"],
                        row["price"],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Incremental order items loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except Exception:
        if connection:
            connection.rollback()

        LOGGER.exception(
            "Failed to load incremental order items"
        )

        return 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def run() -> None:
    """
    Run incremental order items loader.
    """

    load_incremental_order_items()


if __name__ == "__main__":
    run()