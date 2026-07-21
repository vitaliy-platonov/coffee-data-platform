
import logging
import logging_config
import os

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "categories",
    "categories.csv"
)

def load_categories():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} categories from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.categories CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_category_ids = set()

        for _, row in df.iterrows():

            category_id = row['category_id']
            if category_id in seen_category_ids:
                logging.warning(
                    f"Category {category_id} duplicate category_id in CSV"
                )
                skipped_rows += 1
                continue

            category_name = row['category_name']
            if pd.isna(category_name):
                category_name = ""
            else:
                category_name = str(category_name).strip()

            if not category_name:
                logging.warning(
                    f"Category {category_id}: category_name is empty"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
            INSERT INTO staging.categories (
                category_id,
                category_name)
            VALUES (%s, %s)""",
                           (category_id,
                            category_name))

            loaded_rows += 1
            seen_category_ids.add(category_id)


        conn.commit()
        logging.info(
            f"Categories loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception as error:
        logging.exception("Failed to load categories")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_categories()
