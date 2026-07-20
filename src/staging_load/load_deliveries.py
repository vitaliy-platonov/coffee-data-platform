
import logging
import os

import pandas as pd
import psycopg

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "deliveries",
    "deliveries.csv"
)

def load_deliveries():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df =pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} deliveries from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.deliveries CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.deliveries (
                delivery_id,
                supplier_id,
                store_id,
                product_id,
                quantity,
                delivery_date)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (row['delivery_id'],
                            row['supplier_id'],
                            row['store_id'],
                            row['product_id'],
                            row['quantity'],
                            row['delivery_date']))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_deliveries()