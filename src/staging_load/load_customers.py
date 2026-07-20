
import logging
import os

import pandas as pd
import psycopg

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "customers",
    "customers.csv"

)

def load_customers():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding= 'utf-8')
        logging.info(f"Loaded {len(df)} customers from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.customers CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.customers (
                customer_id,
                first_name,
                last_name,
                phone,
                email,
                city,
                registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                           (row["customer_id"],
                            row["first_name"],
                            row["last_name"],
                            row["phone"],
                            row["email"],
                            row["city"],
                            row["registration_date"]))

        conn.commit()

        print(df.head())
        print(df.columns)
        print(df.shape)
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_customers()
