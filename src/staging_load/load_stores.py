
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.dates import parse_date
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_stores(file_path: Path) -> None:
    """
    Load stores data from CSV file into the staging.stores table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} stores from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.stores CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_store_ids = set()

        for _, row in df.iterrows():

            store_id = row["store_id"]

            if store_id in seen_store_ids:
                LOGGER.warning(
                    f"Store {store_id}: duplicate store_id in CSV"
                )
                skipped_rows += 1
                continue

            store_name = normalize_text(row["store_name"])

            if not store_name:
                LOGGER.warning(
                    f"Store {store_id}: store_name is empty"
                )
                skipped_rows += 1
                continue

            if len(store_name) > 50:
                LOGGER.warning(
                    f"Store {store_id}: store_name is longer than 50 characters"
                )
                skipped_rows += 1
                continue

            address = normalize_text(row["address"])

            if not address:
                LOGGER.warning(
                    f"Store {store_id}: address is empty"
                )
                skipped_rows += 1
                continue

            if len(address) > 200:
                LOGGER.warning(
                    f"Store {store_id}: address is longer than 200 characters"
                )
                skipped_rows += 1
                continue

            region = normalize_text(row["region"])

            if not region:
                LOGGER.warning(
                    f"Store {store_id}: region is empty"
                )
                skipped_rows += 1
                continue

            if len(region) > 100:
                LOGGER.warning(
                    f"Store {store_id}: region is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            opening_date = parse_date(
                normalize_text(row["opening_date"])
            )

            if opening_date is None:
                LOGGER.warning(
                    f"Store {store_id}: invalid opening_date"
                )
                skipped_rows += 1
                continue

            is_active = normalize_text(
                row["is_active"]
            ).lower()

            if not is_active:
                LOGGER.warning(
                    f"Store {store_id}: is_active is empty"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.stores (
                    store_id,
                    store_name,
                    address,
                    region,
                    opening_date,
                    is_active
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    store_id,
                    store_name,
                    address,
                    region,
                    opening_date,
                    is_active,
                ),
            )

            loaded_rows += 1
            seen_store_ids.add(store_id)

        conn.commit()

        LOGGER.info(
            f"Stores loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load stores")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the stores staging loader.
    """
    file_path = RAW_DATA_DIR / "stores" / "stores.csv"
    load_stores(file_path)


if __name__ == "__main__":
    run()