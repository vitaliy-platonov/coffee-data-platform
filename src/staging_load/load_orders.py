
from datetime import datetime
import logging
import os
import logging_config

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "orders",
    "orders.csv"
)

def load_orders():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} orders from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.orders CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_order_ids = set()

        for _, row in df.iterrows():

            order_id = row['order_id']
            if order_id in seen_order_ids:
                logging.warning(
                    f"Order {order_id}: duplicate order_id in CSV"
                )
                skipped_rows += 1
                continue

            customer_id = int(row['customer_id'])
            store_id = int(row['store_id'])
            employee_id = int(row['employee_id'])

            order_date = row['order_date']
            if pd.isna(order_date):
                order_date = ""
            else:
                order_date = str(order_date).strip()

            try:
                order_date = datetime.strptime(
                    order_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Order {order_id}: invalid order_date"
                )
                skipped_rows += 1
                continue

            total_amount = row['total_amount']
            if pd.isna(total_amount):
                total_amount = 0
            else:
                total_amount = float(total_amount)

            if total_amount < 0:
                logging.warning(
                    f"Order {order_id}: total_amount must be greater than 0"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
            INSERT INTO staging.orders (
                order_id,
                customer_id,
                store_id,
                employee_id,
                order_date,
                total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (order_id,
                            customer_id,
                            store_id,
                            employee_id,
                            order_date,
                            total_amount))
            loaded_rows += 1
            seen_order_ids.add(order_id)

        conn.commit()
        logging.info(
            f"Orders loaded: {loaded_rows}, skipped: {skipped_rows}"
        )
    except Exception:
        logging.exception(f"Failed to load orders")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_orders()