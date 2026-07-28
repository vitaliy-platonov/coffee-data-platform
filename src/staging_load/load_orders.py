
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.dates import parse_date
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_orders(file_path: Path) -> None:
    """
    Load orders data from CSV file into the staging.orders table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} orders from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.orders CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_order_ids = set()

        for _, row in df.iterrows():

            order_id = row["order_id"]

            if order_id in seen_order_ids:
                LOGGER.warning(
                    f"Order {order_id}: duplicate order_id in CSV"
                )
                skipped_rows += 1
                continue

            customer_id = int(row["customer_id"])
            store_id = int(row["store_id"])
            employee_id = int(row["employee_id"])

            order_date = parse_date(
                normalize_text(row["order_date"])
            )

            if order_date is None:
                LOGGER.warning(
                    f"Order {order_id}: invalid order_date"
                )
                skipped_rows += 1
                continue

            total_amount = row["total_amount"]

            if pd.isna(total_amount):
                total_amount = 0
            else:
                total_amount = float(total_amount)

            if total_amount <= 0:
                LOGGER.warning(
                    f"Order {order_id}: total_amount must be greater than 0"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.orders (
                    order_id,
                    customer_id,
                    store_id,
                    employee_id,
                    order_date,
                    total_amount
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    order_id,
                    customer_id,
                    store_id,
                    employee_id,
                    order_date,
                    total_amount,
                ),
            )

            loaded_rows += 1
            seen_order_ids.add(order_id)

        conn.commit()

        LOGGER.info(
            f"Orders loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load orders")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the orders staging loader.
    """
    file_path = RAW_DATA_DIR / "orders" / "orders.csv"
    load_orders(file_path)


if __name__ == "__main__":
    run()