
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.text import normalize_text


LOGGER = logging.getLogger(__name__)


def load_categories(file_path: Path) -> None:
    """
    Load categories data from CSV file into the staging.categories table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} categories from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.categories CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_category_ids = set()

        for _, row in df.iterrows():

            category_id = row["category_id"]
            if category_id in seen_category_ids:
                LOGGER.warning(
                    f"Category {category_id}: duplicate category_id in CSV"
                )
                skipped_rows += 1
                continue

            category_name = normalize_text(row["category_name"])

            if not category_name:
                LOGGER.warning(
                    f"Category {category_id}: category_name is empty"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.categories (
                    category_id,
                    category_name
                )
                VALUES (%s, %s)
                """,
               (
                    category_id,
                    category_name,
               ),
            )

            loaded_rows += 1
            seen_category_ids.add(category_id)

        conn.commit()

        LOGGER.info(
            f"Categories loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load categories")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the categories staging loader.
    """
    file_path = RAW_DATA_DIR / "categories" / "categories.csv"
    load_categories(file_path)


if __name__ == "__main__":
    run()
