
import logging
import pandas as pd
import os
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

        df =pd.read_csv(file_path, encoding='utf-8')
        cursor.execute("""
        TRUNCATE TABLE staging.orders CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.orders (
                order_id,
                customer_id,
                store_id,
                employee_id,
                order_date,
                total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (row['order_id'],
                            row['customer_id'],
                            row['store_id'],
                            row['employee_id'],
                            row['order_date'],
                            row['total_amount']))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_orders()