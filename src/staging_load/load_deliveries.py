
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.dates import parse_date
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_deliveries(file_path: Path) -> None:
    """
    Load deliveries data from CSV file into the staging.deliveries table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} deliveries from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.deliveries CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_delivery_ids = set()

        for _, row in df.iterrows():

            delivery_id = row["delivery_id"]
            if delivery_id in seen_delivery_ids:
                LOGGER.warning(
                    f"Delivery {delivery_id}: duplicate delivery_id in CSV"
                )
                skipped_rows += 1
                continue

            supplier_id = int(row["supplier_id"])
            store_id = int(row["store_id"])
            product_id = int(row["product_id"])

            quantity = row["quantity"]
            if pd.isna(quantity):
                quantity = 0
            else:
                quantity = int(quantity)

            if quantity <= 0:
                LOGGER.warning(
                    f"Delivery {delivery_id}: quantity must be greater than 0"
                )
                skipped_rows += 1
                continue

            delivery_date = normalize_text(row["delivery_date"])

            delivery_date = parse_date(delivery_date)

            if delivery_date is None:
                LOGGER.warning(
                    f"Delivery {delivery_id}: invalid delivery_date"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.deliveries (
                    delivery_id,
                    supplier_id,
                    store_id,
                    product_id,
                    quantity,
                    delivery_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
               (
                   delivery_id,
                    supplier_id,
                    store_id,
                    product_id,
                    quantity,
                    delivery_date,
                    ),
            )

            loaded_rows += 1
            seen_delivery_ids.add(delivery_id)

        conn.commit()
        LOGGER.info(
            f"Deliveries loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load deliveries")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the deliveries staging loader.
    """
    file_path = RAW_DATA_DIR / "deliveries" / "deliveries.csv"
    load_deliveries(file_path)


if __name__ == "__main__":
    run()