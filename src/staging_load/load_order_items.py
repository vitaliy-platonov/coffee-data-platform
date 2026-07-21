
import logging_config
import logging
import os

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "order_items",
    "order_items.csv"
)

def load_order_items():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} order_items from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.order_items CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_order_item_ids = set()

        for _, row in df.iterrows():

            order_item_id = row["order_item_id"]
            if order_item_id in seen_order_item_ids:
                logging.warning(
                    f"Order item {order_item_id}: duplicate order_item_id in CSV"
                )
                skipped_rows += 1
                continue

            order_id = int(row["order_id"])
            product_id = int(row["product_id"])

            quantity = row["quantity"]
            if pd.isna(quantity):
                quantity = 0
            else:
                quantity = int(quantity)

            if quantity <= 0:
                logging.warning(
                    f"Order item {order_item_id}: quantity must be greater than 0"
                )
                skipped_rows += 1
                continue

            price = row["price"]
            if pd.isna(price):
                price = 0
            else:
                price = float(price)

            if price <= 0:
                logging.warning(
                    f"Order item {order_item_id}: price must be greater than 0"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO staging.order_items (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES (%s, %s, %s, %s, %s);
            """,
            (
                order_item_id,
                order_id,
                product_id,
                quantity,
                price
            ))

            loaded_rows += 1
            seen_order_item_ids.add(order_item_id)

        conn.commit()

        logging.info(
            f"Order items loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        logging.exception("Failed to load payments")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_order_items()