
import logging
import os

import pandas as pd
import psycopg

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "payments",
    "payments.csv"
)

def load_payments():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df =pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} payments from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.payments CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.payments (
                payment_id,
                order_id,
                payment_date,
                payment_method,
                amount,
                status)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (row['payment_id'],
                            row['order_id'],
                            row['payment_date'],
                            row['payment_method'],
                            row['amount'],
                            row['status']))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_payments()