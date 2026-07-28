
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_products(file_path: Path) -> None:
    """
    Load products data from CSV file into the staging.products table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} products from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.products CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_product_ids = set()

        for _, row in df.iterrows():

            product_id = row["product_id"]

            if product_id in seen_product_ids:
                LOGGER.warning(
                    f"Product {product_id}: duplicate product_id in CSV"
                )
                skipped_rows += 1
                continue

            product_name = normalize_text(row["product_name"])

            if not product_name:
                LOGGER.warning(
                    f"Product {product_id}: product_name is empty"
                )
                skipped_rows += 1
                continue

            if len(product_name) > 50:
                LOGGER.warning(
                    f"Product {product_id}: product_name is longer than 50 characters"
                )
                skipped_rows += 1
                continue

            price = row["price"]

            if pd.isna(price):
                price = 0
            else:
                price = float(price)

            if price < 0:
                LOGGER.warning(
                    f"Product {product_id}: price cannot be negative"
                )
                skipped_rows += 1
                continue

            category_id = int(row["category_id"])
            supplier_id = int(row["supplier_id"])

            cursor.execute(
                """
                INSERT INTO staging.products (
                    product_id,
                    product_name,
                    price,
                    category_id,
                    supplier_id
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    product_id,
                    product_name,
                    price,
                    category_id,
                    supplier_id,
                ),
            )

            loaded_rows += 1
            seen_product_ids.add(product_id)

        conn.commit()

        LOGGER.info(
            f"Products loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load products")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the products staging loader.
    """
    file_path = RAW_DATA_DIR / "products" / "products.csv"
    load_products(file_path)


if __name__ == "__main__":
    run()