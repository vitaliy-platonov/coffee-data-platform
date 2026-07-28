
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_suppliers(file_path: Path) -> None:
    """
    Load suppliers data from CSV file into the staging.suppliers table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} suppliers from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.suppliers CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_supplier_ids = set()

        for _, row in df.iterrows():

            supplier_id = row["supplier_id"]

            if supplier_id in seen_supplier_ids:
                LOGGER.warning(
                    f"Supplier {supplier_id}: duplicate supplier_id in CSV"
                )
                skipped_rows += 1
                continue

            supplier_name = normalize_text(row["supplier_name"])

            if not supplier_name:
                LOGGER.warning(
                    f"Supplier {supplier_id}: supplier_name is empty"
                )
                skipped_rows += 1
                continue

            if len(supplier_name) > 100:
                LOGGER.warning(
                    f"Supplier {supplier_id}: supplier_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            is_active = normalize_text(
                row["is_active"]
            ).lower()

            if not is_active:
                LOGGER.warning(
                    f"Supplier {supplier_id}: is_active is empty"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.suppliers (
                    supplier_id,
                    supplier_name,
                    is_active
                )
                VALUES (%s, %s, %s)
                """,
                (
                    supplier_id,
                    supplier_name,
                    is_active,
                ),
            )

            loaded_rows += 1
            seen_supplier_ids.add(supplier_id)

        conn.commit()

        LOGGER.info(
            f"Suppliers loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load suppliers")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the suppliers staging loader.
    """
    file_path = RAW_DATA_DIR / "suppliers" / "suppliers.csv"
    load_suppliers(file_path)


if __name__ == "__main__":
    run()