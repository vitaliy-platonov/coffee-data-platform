
import logging
import os
import logging_config

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "products",
    "products.csv"
)

def load_products():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} products from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.products CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_product_ids = set()

        for _, row in df.iterrows():

            product_id = row['product_id']
            if product_id in seen_product_ids:
                logging.warning(
                    f"Product {product_id}: duplicate product_id in CSV"
                )
                skipped_rows += 1
                continue

            product_name = row['product_name']
            if pd.isna(product_name):
                product_name = ""
            else:
                product_name = str(product_name).strip()

            if not product_name:
                logging.warning(
                    f"Product {product_id}: product_name is empty"
                )
                skipped_rows += 1
                continue

            if len(product_name) > 50:
                logging.warning(
                    f"Product {product_id}: product_name longer than 50 characters"
                )
                skipped_rows += 1
                continue

            price = row['price']
            if pd.isna(price):
                price = 0
            else:
                price = float(price)

            if price < 0:
                logging.warning(
                    f"Product {product_id}: price cannot be negative"
                )
                skipped_rows += 1
                continue

            category_id = int(row['category_id'])
            supplier_id = int(row['supplier_id'])

            cursor.execute("""
            INSERT INTO staging.products (
                product_id,
                product_name,
                price,
                category_id,
                supplier_id)
            VALUES (%s, %s, %s, %s, %s);
                """,
                           (product_id,
                            product_name,
                            price,
                            category_id,
                            supplier_id))
            loaded_rows += 1
            seen_product_ids.add(product_id)
        conn.commit()
        logging.info(f"Products loaded: {loaded_rows}, skipped: {skipped_rows}")
    except Exception:
        logging.exception("Failed to load products")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_products()