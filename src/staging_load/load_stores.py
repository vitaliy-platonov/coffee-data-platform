
from datetime import datetime
import logging
import os
import logging_config

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
        logging.info(f"Loaded {len(df)} stores from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.stores CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_store_ids = set()

        for _, row in df.iterrows():

            store_id = row['store_id']
            if store_id in seen_store_ids:
                logging.warning(
                    f"Store {store_id} duplicate store_id in CSV"
                )
                skipped_rows += 1
                continue

            store_name = row['store_name']
            if pd.isna(store_name):
                store_name = ""
            else:
                store_name = str(store_name).strip()

            if not store_name:
                logging.warning(
                    f"Store {store_id}: store_name is empty"
                )
                skipped_rows += 1
                continue

            if len(store_name) > 50:
                logging.warning(
                    f"Store {store_id}: store_name is longer than 50 characters"
                )
                skipped_rows += 1
                continue

            address = row['address']
            if pd.isna(address):
                address = ""
            else:
                address = str(address).strip()

            if not address:
                logging.warning(
                    f"Store {store_id}: address is empty"
                )
                skipped_rows += 1
                continue

            if len(address) > 200:
                logging.warning(
                    f"Store {store_id}: address is longer than 200"
                )
                skipped_rows += 1
                continue

            region = row['region']
            if pd.isna(region):
                region = ""
            else:
                region = str(region).strip()

            if not region:
                logging.warning(
                    f"Store {store_id}: region is empty"
                )
                skipped_rows += 1
                continue

            if len(region) > 100:
                logging.warning(
                    f"Store {store_id}: region is longer than 100"
                )
                skipped_rows += 1
                continue

            opening_date = row['opening_date']
            if pd.isna(opening_date):
                opening_date = ""
            else:
                opening_date = str(opening_date).strip()

            if not opening_date:
                logging.warning(
                    f"Store {store_id}: opening_date is empty"
                )
                skipped_rows += 1
                continue

            try:
                opening_date = datetime.strptime(
                    opening_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Store {store_id}: invalid opening_date"
                )
                skipped_rows += 1
                continue

            is_active = row['is_active']
            if pd.isna(is_active):
                is_active = ""
            else:
                is_active = str(is_active).strip().lower()

            if not is_active:
                logging.warning(
                    f"Store {store_id}: is_active is empty"
                )
                skipped_rows += 1
                continue

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
                           (store_id,
                            store_name,
                            address,
                            region,
                            opening_date,
                            is_active
                           ))
            loaded_rows += 1
            seen_store_ids.add(store_id)

        conn.commit()
        logging.info(
            f"Stores loaded: {loaded_rows}, skipped: {skipped_rows}"
        )
    except Exception:
        logging.exception("Failed to load stores")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
if __name__ == '__main__':
    load_stores()