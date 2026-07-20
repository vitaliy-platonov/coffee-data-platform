
import logging
import os
import psycopg
import pandas as pd
from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "suppliers",
    "suppliers.csv"
)

def load_suppliers():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} suppliers from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.suppliers CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.suppliers (
                supplier_id,
                supplier_name,
                is_active)
            VALUES (%s, %s, %s)""",
                           (row["supplier_id"], row["supplier_name"], row["is_active"]))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_suppliers()