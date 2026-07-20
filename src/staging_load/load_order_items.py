
import logging
import os

import pandas as pd
import psycopg

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

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.order_items (
                order_item_id,
                order_id,
                product_id,
                quantity,
                price)
            VALUES (%s, %s, %s, %s, %s);
                """,
                           (row["order_item_id"],
                           row["order_id"],
                           row["product_id"],
                           row["quantity"],
                           row["price"]))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_order_items()