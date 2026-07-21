
from datetime import datetime
import logging
import os
import logging_config

import pandas as pd

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

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} deliveries from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.deliveries CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_delivery_ids = set()

        for _, row in df.iterrows():

            delivery_id = row['delivery_id']
            if delivery_id in seen_delivery_ids:
                logging.warning(
                    f"Delivery {delivery_id}: duplicate delivery_id in CSV"
                )
                skipped_rows += 1
                continue

            supplier_id = int(row['supplier_id'])
            store_id = int(row['store_id'])
            product_id = int(row['product_id'])

            quantity = row['quantity']
            if pd.isna(quantity):
                quantity = 0
            else:
                quantity = int(quantity)

            if quantity <= 0:
                logging.warning(
                    f"Delivery {delivery_id}: quantity must be greater than 0"
                )
                skipped_rows += 1
                continue

            delivery_date = row['delivery_date']
            if pd.isna(delivery_date):
                delivery_date = ""
            else:
                delivery_date = str(delivery_date).strip()

            try:
                delivery_date = datetime.strptime(
                    delivery_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Delivery {delivery_id}: invalid delivery_date"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
            INSERT INTO staging.deliveries (
                delivery_id,
                supplier_id,
                store_id,
                product_id,
                quantity,
                delivery_date)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (delivery_id,
                            supplier_id,
                            store_id,
                            product_id,
                            quantity,
                            delivery_date))
            loaded_rows += 1
            seen_delivery_ids.add(delivery_id)

        conn.commit()
        logging.info(
            f"Deliveries loaded: {loaded_rows}, skipped: {skipped_rows}"
        )
    except Exception:
        logging.exception("Failed to load deliveries")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_deliveries()