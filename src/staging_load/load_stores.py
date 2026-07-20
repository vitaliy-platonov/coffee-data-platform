
import psycopg
import logging
import os
import pandas as pd
from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "stores",
    "stores.csv"
)

def load_stores():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')

        cursor.execute("""
        TRUNCATE TABLE staging.stores CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.stores (
                store_id,
                store_name,
                address,
                region,
                opening_date,
                is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
                           (
                               row['store_id'],
                               row['store_name'],
                               row['address'],
                               row['region'],
                               row['opening_date'],
                               row['is_active']
                           ))

        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
if __name__ == '__main__':
    load_stores()