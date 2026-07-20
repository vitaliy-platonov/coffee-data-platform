
import logging
import pandas as pd
import os
import psycopg
from database import get_connection
from config import RAW_DATA_DIR

file_path = os.path.join(
    RAW_DATA_DIR,
    "categories",
    "categories.csv"
)

def load_categories():
    cursor = None
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} categories from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.categories CASCADE;""")

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO staging.categories (
                category_id,
                category_name)
            VALUES (%s, %s)""",
                           (row['category_id'],
                            row['category_name']))

        conn.commit()
    except Exception as error:
        logging.info(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_categories()
