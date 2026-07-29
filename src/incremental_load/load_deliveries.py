
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_incremental_deliveries() -> int:
    """
    Load incremental deliveries into database.
    """

    connection = None
    cursor = None
    rows_loaded = 0

    try:
        file_path = INCREMENTAL_DATA_DIR / "deliveries_increment.csv"

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
                    INSERT INTO deliveries (
                        delivery_id,
                        supplier_id,
                        store_id,
                        product_id,
                        quantity,
                        delivery_date
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
                        row["delivery_id"],
                        row["supplier_id"],
                        row["store_id"],
                        row["product_id"],
                        row["quantity"],
                        row["delivery_date"],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Incremental deliveries loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except Exception:
        if connection:
            connection.rollback()

        LOGGER.exception(
            "Failed to load incremental deliveries"
        )

        return 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def run() -> None:
    """
    Run incremental deliveries loader.
    """

    load_incremental_deliveries()


if __name__ == "__main__":
    run()