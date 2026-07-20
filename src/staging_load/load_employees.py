
import logging
import os

import pandas as pd
import psycopg

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "employees",
    "employees.csv"
)

def load_employees():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path,encoding='utf-8')
        logging.info(f"Loaded {len(df)} employees from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.employees CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.employees (
                employee_id,
                first_name,
                last_name,
                hire_date,
                salary,
                position,
                is_active,
                store_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                           (row["employee_id"],
                           row["first_name"],
                           row["last_name"],
                           row["hire_date"],
                           row["salary"],
                           row["position"],
                           row["is_active"],
                           row["store_id"]))
        conn.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_employees()
