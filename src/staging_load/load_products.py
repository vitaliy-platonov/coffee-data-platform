
import logging
import os

import pandas as pd
import psycopg

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

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.products (
                product_id,
                product_name,
                price,
                category_id,
                supplier_id)
            VALUES (%s, %s, %s, %s, %s);
                """,
                           (row["product_id"],
                           row["product_name"],
                           row["price"],
                           row["category_id"],
                           row["supplier_id"]))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_products()